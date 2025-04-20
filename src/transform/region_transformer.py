import pandas as pd

def transform_region(df_title_akas, staging_output):
    if df_title_akas.empty:
        raise ValueError("El DataFrame df_title_akas está vacío.")
    
    df = df_title_akas.copy()
    print("Columnas disponibles:", df.columns)
    print("Antes del filtro:", df.shape)
    
    # Filtrar solo por filas que tengan valores no-NaN en region y language
    df = df.dropna(subset=['region', 'language'])
    print("Después de eliminar NaN en 'region' y 'language':", df.shape)
    
    # Seleccionar columnas y eliminar duplicados
    df = df[['region', 'language']].drop_duplicates()
    print("Después de eliminar duplicados:", df.shape)
    
    if df.empty:
        raise ValueError("El DataFrame resultante está vacío después de eliminar duplicados.")
    
    # Agregar clave primaria
    df['region_key'] = range(1, len(df) + 1)
    df = df[['region_key', 'region', 'language']]
    
    # Guardar en CSV
    df.to_csv(staging_output, index=False)
    print(f"Archivo guardado en {staging_output} con {len(df)} filas.")