"""
This script filters out deceased individuals from a dataset of actors, actresses, and directors.
It reads the cleaned data, 
then filters out individuals listed as deceased in the 'name.tsv' dataset,
and saves the filtered data to a new file (data_clean_v6.csv).
"""

import pandas as pd

# Loading the cleaned dataset
df_v5 = pd.read_csv('../../../data/cleaned/data_clean_v5.csv')

# Loading the dataset containing names and death years
df_name = pd.read_csv('../../../data/raw/name.tsv', sep='\t')

# Filtering out deceased individuals
deceased_individuals = df_name[df_name['deathYear'] != '\\N']
deceased_names = set(deceased_individuals['primaryName'])
mask = (~df_v5['actor'].isin(deceased_names)) & \
       (~df_v5['actress'].isin(deceased_names)) & \
       (~df_v5['director'].isin(deceased_names))

# Applying the filter
df_v5_filtered = df_v5[mask]

# Saving the filtered dataset
df_v5_filtered.to_csv('../../../data/cleaned/data_clean_v6.csv', index=False)
