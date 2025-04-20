import pandas as pd

def transform_dim_director(path_name_basics, path_title_crew, staging_output):
    """
    Crear dimensión de directores combinando información de name.basics y title.crew
    """
    print("Cargando datos de nombres y crews...")
    # Cargar name.basics con solo las columnas que necesitamos
    names = pd.read_csv(path_name_basics, sep='\t', na_values='\\N',
                       usecols=['nconst', 'primaryName', 'birthYear', 'deathYear', 'primaryProfession'],
                       dtype={'nconst': str, 'primaryName': str, 'primaryProfession': str})
    
    # Cargar title.crew con solo las columnas de directores
    crews = pd.read_csv(path_title_crew, sep='\t', na_values='\\N',
                       usecols=['tconst', 'directors'],
                       dtype={'tconst': str, 'directors': str})
    
    print(f"Registros en names: {len(names)}")
    print(f"Registros en crews: {len(crews)}")
    
    # Expandir la lista de directores (cada fila será un par tconst-director)
    print("Procesando directores...")
    crews_expanded = crews[crews['directors'].notna()].copy()
    
    # Crear un DataFrame que contenga todos los pares tconst-director
    director_pairs = []
    
    for _, row in crews_expanded.iterrows():
        directors = row['directors'].split(',')
        for director in directors:
            if director != '\\N':  # Ignorar valores nulos
                director_pairs.append({'tconst': row['tconst'], 'nconst': director})
    
    directors_df = pd.DataFrame(director_pairs)
    print(f"Total de pares título-director: {len(directors_df)}")
    
    # Contar cuántas películas ha dirigido cada director
    director_counts = directors_df['nconst'].value_counts().reset_index()
    director_counts.columns = ['nconst', 'num_dirigidas']
    
    # Unir con la información biográfica
    directors = director_counts.merge(names, on='nconst', how='left')
    
    # Crear columnas finales
    directors['director_key'] = range(1, len(directors) + 1)
    directors['nombre'] = directors['primaryName']
    directors['anio_nacimiento'] = pd.to_numeric(directors['birthYear'], errors='coerce')
    directors['anio_fallecimiento'] = pd.to_numeric(directors['deathYear'], errors='coerce')
    directors['profesion_principal'] = directors['primaryProfession'].fillna('').apply(
        lambda p: p.split(',')[0] if p else None)
    
    # Seleccionar columnas finales
    result = directors[['director_key', 'nconst', 'nombre', 'anio_nacimiento', 'anio_fallecimiento',
                        'profesion_principal', 'num_dirigidas']]
    
    # Guardar resultado
    result.to_csv(staging_output, index=False)
    print(f"✅ Dimensión de directores guardada en {staging_output} con {len(result)} registros.")
    
    # Devolver el DataFrame para uso posterior
    return result