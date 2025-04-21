import pandas as pd

def transform_fact_obra(path_basics, path_ratings, path_akas, path_region_staging, 
                        path_title_crew, path_name_basics, master_output):
    # Cargar los datos básicos
    print("Cargando datos...")
    basics = pd.read_csv(path_basics, sep='\t', na_values='\\N', dtype=str)
    ratings = pd.read_csv(path_ratings, sep='\t', na_values='\\N')
    region_dim = pd.read_csv(path_region_staging)
    
    print(f"Registros en basics: {len(basics)}")
    print(f"Registros en ratings: {len(ratings)}")
    print(f"Registros en region_dim: {len(region_dim)}")
    
    # Cargar datos de akas
    print("Cargando akas (solo columnas necesarias)...")
    akas = pd.read_csv(path_akas, sep='\t', na_values='\\N', 
                       usecols=['titleId', 'region', 'language', 'isOriginalTitle', 'ordering'],
                       dtype=str)
    print(f"Registros en akas: {len(akas)}")
    
    # Cargar datos de directores
    print("Cargando datos de directores...")
    crews = pd.read_csv(path_title_crew, sep='\t', na_values='\\N',
                       usecols=['tconst', 'directors'], dtype=str)
    print(f"Registros en crews: {len(crews)}")
    
    names = pd.read_csv(path_name_basics, sep='\t', na_values='\\N',
                       usecols=['nconst', 'primaryName'], dtype=str)
    print(f"Registros en names: {len(names)}")
    
    # Procesar regiones y lenguajes
    print("Filtrando akas...")
    akas_valid = akas[akas['region'].notna() & akas['language'].notna()]
    print(f"Akas con región y lenguaje válidos: {len(akas_valid)}")
    
    print("Creando mapa de regiones para cada título...")
    akas_original = akas_valid[akas_valid['isOriginalTitle'] == '1']
    akas_original = akas_original.sort_values('ordering').drop_duplicates('titleId')
    
    missing_titles = set(basics['tconst']) - set(akas_original['titleId'])
    print(f"Títulos sin versión original: {len(missing_titles)}")
    
    akas_others = akas_valid[akas_valid['titleId'].isin(missing_titles)]
    akas_others = akas_others.sort_values('ordering').drop_duplicates('titleId')
    
    akas_map = pd.concat([akas_original, akas_others])
    print(f"Total de títulos con información de región/lenguaje: {len(akas_map)}")
    
    print(f"Top 5 regiones: {akas_map['region'].value_counts().head()}")
    print(f"Top 5 lenguajes: {akas_map['language'].value_counts().head()}")
    
    # Procesar directores - Extraer el director principal de cada título
    print("Procesando directores principales...")
    crews['director_principal'] = crews['directors'].fillna('').apply(
        lambda d: d.split(',')[0] if d and d != '\\N' else None)
    
    # Crear un mapa de directores principales
    director_map = crews[crews['director_principal'].notna()][['tconst', 'director_principal']]
    print(f"Títulos con director principal identificado: {len(director_map)}")
    
    # Unir con la información de nombres de directores
    director_map = director_map.merge(names, left_on='director_principal', right_on='nconst', how='left')
    director_map.rename(columns={'primaryName': 'nombre_director'}, inplace=True)
    director_map['nombre_director'] = director_map['nombre_director'].fillna('Desconocido')
    
    # Unir los datos básicos
    print("Uniendo basics con ratings...")
    df = basics.merge(ratings, on='tconst', how='left')
    
    # Unir con información de región/lenguaje
    print("Asignando región y lenguaje a cada título...")
    df = df.merge(akas_map[['titleId', 'region', 'language']], 
                 left_on='tconst', right_on='titleId', how='left')
    
    print(f"Títulos sin región/lenguaje asignado: {df['region'].isna().sum()}")
    df['region'] = df['region'].fillna('UNK')
    df['language'] = df['language'].fillna('UNK')
    
    # Unir con información de directores
    print("Asignando director principal a cada título...")
    df = df.merge(director_map[['tconst', 'director_principal', 'nombre_director']], 
                 on='tconst', how='left')
    print(f"Títulos sin director asignado: {df['director_principal'].isna().sum()}")
    
    # Procesar región/language
    print("Obteniendo region_key de la dimensión de regiones...")
    region_lang_pairs = df[['region', 'language']].drop_duplicates()
    missing_pairs = region_lang_pairs.merge(region_dim, on=['region', 'language'], how='left')
    missing_count = missing_pairs['region_key'].isna().sum()
    
    if missing_count > 0:
        print(f"Hay {missing_count} combinaciones region/language que no existen en region_dim")
        missing = missing_pairs[missing_pairs['region_key'].isna()][['region', 'language']]
        max_key = region_dim['region_key'].max() if len(region_dim) > 0 else 0
        missing['region_key'] = range(max_key + 1, max_key + 1 + len(missing))
        
        region_dim_extended = pd.concat([region_dim, missing])
    else:
        region_dim_extended = region_dim
    
    df = df.merge(region_dim_extended, on=['region', 'language'], how='left')
    print(f"Registros sin region_key después del merge: {df['region_key'].isna().sum()}")
    
    # Crear columnas finales
    print("Creando columnas finales...")
    df['obra_key'] = range(1, len(df) + 1)
    df['anio_lanzamiento'] = pd.to_numeric(df['startYear'], errors='coerce')
    df['duracion_min'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')
    df['is_adult'] = pd.to_numeric(df['isAdult'], errors='coerce')
    df['genero'] = df['genres'].fillna('').apply(lambda g: g.split(',')[0] if g else None)
    df['tipo_obra'] = df['titleType']
    
    # Columnas finales con la información de director
    df = df[['obra_key', 'tconst', 'primaryTitle', 'anio_lanzamiento', 'duracion_min', 'is_adult',
             'averageRating', 'numVotes', 'tipo_obra', 'genero', 'region_key',
             'region', 'region_name', 'language', 'director_principal', 'nombre_director']]
    
    # Guardar resultado
    df.to_csv(master_output, index=False)
    print(f"✅ Archivo guardado correctamente en {master_output}")