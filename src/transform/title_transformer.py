import pandas as pd

def transform_title_basics(basics_df, ratings_df, staging_output):
    df = basics_df.merge(ratings_df, on='tconst', how='left')

    df['titulo'] = df['primaryTitle']
    df['titulo_original'] = df['originalTitle']
    df['tipo_obra'] = df['titleType']
    df['genero'] = df['genres'].fillna('').apply(lambda g: g.split(',')[0] if g else None)

    df = df[['tconst', 'titulo', 'titulo_original', 'tipo_obra', 'genero']]
    df.to_csv(staging_output, index=False)