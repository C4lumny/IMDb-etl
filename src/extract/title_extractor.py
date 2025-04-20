import pandas as pd

def extract_title_basics(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)

def extract_title_akas(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)

def extract_title_crew(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)

def extract_title_episode(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)

def extract_title_principals(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype=str)

def extract_title_ratings(path: str) -> pd.DataFrame:
    return pd.read_csv(path, sep='\t', na_values='\\N', dtype={'averageRating': float, 'numVotes': int})