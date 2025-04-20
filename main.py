from src.extract.title_extractor import *
from src.extract.person_extractor import *
from src.transform.title_transformer import *
from src.transform.region_transformer import *
from src.transform.fact_transformer import *
from src.transform.director_transformer import *
from src.load.dimension_loader import *

RAW_PATH = "data/raw/"
STAGING_PATH = "data/staging/"
MASTER_PATH = "data/master/"

df_title_episode = extract_title_episode(RAW_PATH + "title.episode.tsv")
df_title_akas = extract_title_akas(RAW_PATH + "title.akas.tsv")
df_title_basics = extract_title_basics(RAW_PATH + "title.basics.tsv")
df_persona_name = extract_name_basics(RAW_PATH + "name.basics.tsv")
df_title_ratings = extract_title_ratings(RAW_PATH + "title.ratings.tsv")

transform_title_basics(df_title_basics, df_title_ratings, STAGING_PATH + "staging_title_basics.csv")
transform_region(df_title_akas, STAGING_PATH + "staging_region.csv")
transform_dim_director(
    RAW_PATH + "name.basics.tsv",
    RAW_PATH + "title.crew.tsv",
    STAGING_PATH + "staging_director.csv"
)

transform_fact_obra(
    RAW_PATH + "title.basics.tsv",
    RAW_PATH + "title.ratings.tsv",
    RAW_PATH + "title.akas.tsv",
    STAGING_PATH + "staging_region.csv",
    RAW_PATH + "title.crew.tsv",
    RAW_PATH + "name.basics.tsv",
    MASTER_PATH + "fact_obra.csv"
)

load_dim_obra(
    staging_path=STAGING_PATH + "staging_title_basics.csv",
    master_path=MASTER_PATH + "dim_obra.csv"
)

load_dim_region(
    staging_path=STAGING_PATH + "staging_region.csv",
    master_path=MASTER_PATH + "dim_region.csv"
)
