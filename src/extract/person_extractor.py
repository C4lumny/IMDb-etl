import pandas as pd

def extract_name_basics(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)
