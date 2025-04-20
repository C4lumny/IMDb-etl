from src.extract.title_extractor import *
from src.extract.person_extractor import *

# Rutas
RAW_PATH = "data/raw/"
MASTER_PATH = "data/master/"

# df_title_episode = extract_title_episode(RAW_PATH + "title.episode.tsv")
df_title_basics = extract_title_basics(RAW_PATH + "title.basics.tsv")
df_persona_name = extract_name_basics(RAW_PATH + "name.basics.tsv")

# df_persona_name_filter = df_persona_name[df_persona_name['primaryName'] == 'Dwayne Johnson']
df_title_basics_filter = df_title_basics[df_title_basics['tconst'].isin(['tt6443346','tt2283362','tt1397514','tt1469304'])]
print(df_title_basics_filter.head(20))
# print(df_persona_name_filter.head(20))

