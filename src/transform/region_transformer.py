import pandas as pd

def transform_region(df_title_akas, staging_output):
    if df_title_akas.empty:
        raise ValueError("El DataFrame df_title_akas está vacío.")
    
    df = df_title_akas.copy()
    print("Columnas disponibles:", df.columns)
    print("Antes del filtro:", df.shape)
    
    df = df.dropna(subset=['region', 'language'])
    print("Después de eliminar NaN en 'region' y 'language':", df.shape)
    
    df = df[['region', 'language']].drop_duplicates()
    print("Después de eliminar duplicados:", df.shape)
    
    if df.empty:
        raise ValueError("El DataFrame resultante está vacío después de eliminar duplicados.")
    
    region_mapping = {
        'AF': 'Afganistán', 'AL': 'Albania', 'DZ': 'Argelia', 'AR': 'Argentina', 'AM': 'Armenia',
        'AU': 'Australia', 'AT': 'Austria', 'AZ': 'Azerbaiyán', 'BD': 'Bangladesh', 'BY': 'Bielorrusia',
        'BE': 'Bélgica', 'BJ': 'Benín', 'BF': 'Burkina Faso', 'BA': 'Bosnia y Herzegovina', 'BR': 'Brasil',
        'BG': 'Bulgaria', 'BUMM': 'Myanmar', 'BZ': 'Belice', 'CA': 'Canadá', 'CH': 'Suiza',
        'CL': 'Chile', 'CN': 'China', 'CO': 'Colombia', 'CR': 'Costa Rica', 'CSHH': 'Checoslovaquia',
        'CZ': 'República Checa', 'DE': 'Alemania', 'DDDE': 'Alemania Oriental', 'DK': 'Dinamarca', 'EC': 'Ecuador',
        'EG': 'Egipto', 'ES': 'España', 'EE': 'Estonia', 'ET': 'Etiopía', 'FI': 'Finlandia',
        'FR': 'Francia', 'GB': 'Reino Unido', 'GE': 'Georgia', 'GR': 'Grecia', 'HK': 'Hong Kong',
        'HR': 'Croacia', 'HU': 'Hungría', 'ID': 'Indonesia', 'IE': 'Irlanda', 'IL': 'Israel',
        'IN': 'India', 'IQ': 'Iraq', 'IR': 'Irán', 'IS': 'Islandia', 'IT': 'Italia',
        'JM': 'Jamaica', 'JO': 'Jordania', 'JP': 'Japón', 'KZ': 'Kazajistán', 'KR': 'Corea del Sur',
        'LA': 'Laos', 'LB': 'Líbano', 'LK': 'Sri Lanka', 'LT': 'Lituania', 'LU': 'Luxemburgo',
        'LV': 'Letonia', 'MA': 'Marruecos', 'MK': 'Macedonia del Norte', 'MX': 'México', 'MY': 'Malasia',
        'MN': 'Mongolia', 'MZ': 'Mozambique', 'NL': 'Países Bajos', 'NO': 'Noruega', 'NP': 'Nepal',
        'NZ': 'Nueva Zelanda', 'PA': 'Panamá', 'PE': 'Perú', 'PH': 'Filipinas', 'PK': 'Pakistán',
        'PL': 'Polonia', 'PT': 'Portugal', 'PY': 'Paraguay', 'RO': 'Rumanía', 'RS': 'Serbia',
        'RU': 'Rusia', 'SD': 'Sudán', 'SE': 'Suecia', 'SG': 'Singapur', 'SI': 'Eslovenia',
        'SK': 'Eslovaquia', 'SN': 'Senegal', 'SR': 'Surinam', 'SUHH': 'Unión Soviética', 'TH': 'Tailandia',
        'TJ': 'Tayikistán', 'TN': 'Túnez', 'TR': 'Turquía', 'TW': 'Taiwán', 'UA': 'Ucrania',
        'US': 'Estados Unidos', 'UY': 'Uruguay', 'UZ': 'Uzbekistán', 'VE': 'Venezuela', 'VG': 'Islas Vírgenes Británicas',
        'VN': 'Vietnam', 'XAS': 'Asia', 'XEU': 'Europa', 'XNA': 'Norteamérica', 'XSA': 'Sudamérica',
        'XWG': 'Alemania Occidental', 'XWW': 'Mundial', 'XYU': 'Yugoslavia', 'YUCS': 'Yugoslavia',
        'YE': 'Yemen', 'ZA': 'Sudáfrica', 'ZM': 'Zambia', 'PR': 'Puerto Rico', 'JE': 'Jersey',
        'AE': 'Emiratos Árabes Unidos', 'CG': 'Congo', 'CM': 'Camerún'
    }
    
    df['region_name'] = df['region'].map(region_mapping)
    
    df['region_name'] = df['region_name'].fillna(df['region'])
    
    df['region_key'] = range(1, len(df) + 1)
    
    df = df[['region_key', 'region', 'region_name', 'language']]
    
    df.to_csv(staging_output, index=False)
    print(f"Archivo guardado en {staging_output} con {len(df)} filas.")
    
    return df