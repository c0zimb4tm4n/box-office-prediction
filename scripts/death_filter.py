"""This module filters actor, actresses and directors who are not alive anymore"""

import pandas as pd

def filter_deceased_individuals(cleaned_data_path, name_data_path, output_path):
    """
    Filters out deceased individuals from a dataset of actors, actresses, and directors.

    Parameters:
    - cleaned_data_path: str, path to the cleaned dataset of actors, actresses, and directors.
    - name_data_path: str, path to the dataset containing names and death years.
    - output_path: str, path where the filtered dataset should be saved.
    """
    # Loading the cleaned dataset
    df_v5 = pd.read_csv(cleaned_data_path)

    # Loading the dataset containing names and death years
    df_name = pd.read_csv(name_data_path, sep='\t')

    # Filtering out deceased individuals
    deceased_individuals = df_name[df_name['deathYear'] != '\\N']
    deceased_names = set(deceased_individuals['primaryName'])
    mask = (~df_v5['actor'].isin(deceased_names)) & \
           (~df_v5['actress'].isin(deceased_names)) & \
           (~df_v5['director'].isin(deceased_names))

    # Applying the filter
    df_v5_filtered = df_v5[mask]

    # Saving the filtered dataset
    df_v5_filtered.to_csv(output_path, index=False)

# Example of how to use this function:
filter_deceased_individuals(
    '../../../data/cleaned/data_clean_v5.csv',
    '../../../data/raw/name.tsv',
    '../../../data/cleaned/data_clean_v6.csv')
