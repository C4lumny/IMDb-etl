import pandas as pd
import os

def load_dim_obra(staging_path, master_path):
    df = pd.read_csv(staging_path)
    df['obra_key'] = range(1, len(df) + 1)
    df = df[['obra_key', 'tconst', 'titulo', 'titulo_original', 'tipo_obra', 'genero']]
    df.to_csv(master_path, index=False)
    print("✅ Dimensión Obra cargada.")

def load_dim_region(staging_path, master_path):
    df = pd.read_csv(staging_path)
    df.to_csv(master_path, index=False)
    print("✅ Dimensión Región cargada.")
