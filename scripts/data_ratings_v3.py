"""
This module processes and cleans movie-related data sets,
including title ratings, principal names, and title basics.
"""
import concurrent.futures
import json
import re
from itertools import product

import pandas as pd
import requests
from bs4 import BeautifulSoup

#pylint: disable=invalid-name, broad-exception-caught

# Definition of data types for columns
dtype_dict1 = {"tconst": str, "nconst": str}

# Reading and filtering the title ratings
df_title_ratings = pd.read_csv(
    "../../../data/raw/title ratings.tsv", sep="\t", dtype=dtype_dict1
)
filtered_df_ratings = df_title_ratings[df_title_ratings["numVotes"] > 5000]

# Printing adjusted dataframe
print("Filtered DataFrame with titles having more than 5000 votes:", filtered_df_ratings)

# Processing other datasets with similar pattern
df_name = pd.read_csv("../../../data/raw/name.tsv", sep="\t", dtype=dtype_dict1)
df_title_basics = pd.read_csv("../../../data/raw/title basics.tsv", sep="\t")
df_title_principals = pd.read_csv(
    "../../../data/raw/title principals.tsv", sep="\t", dtype=dtype_dict1
)

# Adjusting print statements and calculations to fit within line limits
print("Unique values count for titles:", df_title_ratings["tconst"].nunique())
print("Null count for titles:", df_title_ratings["tconst"].isnull().sum())

# Creating a pivot table from title principals
pivot_table = df_title_principals.pivot_table(
    index="tconst",
    columns="category",
    values="nconst",
    aggfunc=lambda x: " ".join(str(v) for v in x),
)
pivot_table.reset_index(inplace=True)
pivot_table.columns.name = None

# Merging dataframes with corrections for line lengths
merged_df1 = pd.merge(pivot_table, filtered_df_ratings, on="tconst", how="inner")
merged_df2 = pd.merge(merged_df1, df_title_basics, on="tconst", how="left")

# Adjusting file path and removing unnecessary comments
df_w_rev = pd.read_csv("../../../data/raw/tconsts_prd_company.csv", dtype=dtype_dict1)
merged_df_rev = pd.merge(merged_df2, df_w_rev, on="tconst", how="inner")

# Function to create combinations of column entries
def create_combinations(rows, columns):
    """
    Creates all possible combinations of specified column entries in a DataFrame row.
    
    Parameters:
    - row: The row of the DataFrame to process.
    - columns: A list of column names to combine.
    
    Returns:
    A list of dictionaries representing a row with one combination of the input columns.
    """
    list_of_entries = [str(rows[col]).split() if pd.notna(rows[col]) else [None] for col in columns]
    all_combinations = list(product(*list_of_entries))

    row_data = rows.to_dict()
    expanded_rows = []
    for combo in all_combinations:
        new_row = {**row_data, **{columns[i]: combo[i] for i in range(len(columns))}}
        expanded_rows.append(new_row)

    return expanded_rows


# Defining the columns to combine
columns_to_combine = [
        "actor", "actress", "archive_footage", "archive_sound",
    "cinematographer", "composer", "director", "editor",
    "producer", "production_designer", "self", "writer"
]

# Generating expanded data based on combinations of specified columns
expanded_data_all_cols = []
for index, df_row in merged_df_rev.iterrows():
    expanded_data_all_cols.extend(create_combinations(df_row, columns_to_combine))

# Converting the list of dictionaries into a DataFrame
expanded_merged_df_rev_all_cols = pd.DataFrame(expanded_data_all_cols)

# Function to expand genres from a row into individual rows for each genre
def expand_genre(row):
    """
    Expands a row with multiple genres into separate rows for each genre.

    Parameters:
    - row: The row of the DataFrame to process.

    Returns:
    A list of dictionaries, each representing a row with a single genre.
    """
    genres = row["genres"].split(",") if pd.notna(row["genres"]) else [None]
    row_data = row.to_dict()
    expanded_rows = [ {**row_data, "genres": genre} for genre in genres ]
    return expanded_rows

# Example usage for expanding genres
expanded_data_genres = []
for index, merged_df_row in expanded_merged_df_rev_all_cols.iterrows():
    expanded_data_genres.extend(expand_genre(merged_df_row))
df_clean = pd.DataFrame(expanded_data_genres)

# Cleaning data by mapping nconst columns to names, and dropping unnecessary columns
nconst_columns = [
    "actor", "actress", "archive_footage", "archive_sound", "cinematographer",
    "composer", "director", "editor", "producer", "writer", 
    "production_designer", "self",
]

data_clean_new = df_clean.copy()
# Assuming name_dict is a predefined dictionary mapping nconst to names
# Example: name_dict = {"nconst1": "Name1", "nconst2": "Name2"}
# Creating a dictionary mapping nconst to names
name_dict = pd.Series(df_name.primaryName.values, index=df_name.nconst).to_dict()

for column in nconst_columns:
    if column in data_clean_new.columns:
        data_clean_new[column] = data_clean_new[column].apply(lambda x: name_dict.get(x, x))

# Dropping columns not needed for further analysis
data_clean_new.drop(columns=["archive_footage", "archive_sound", "originalTitle", "endYear"],
                     inplace=True)

# Handling revenue data to convert string to float assuming Revenue column exists
data_clean_new["Revenue"] = data_clean_new["Revenue"].replace(
    r"[\$,]", "", regex=True).astype(float)

# Saving the cleaned DataFrame to a CSV file
# Correcting the file path for saving the cleaned DataFrame
data_clean_new.to_csv("../../../data/cleaned/data_clean_v3.csv", index=False)


title_akas_data = pd.read_csv('../../../data/raw/title akas.tsv', sep='\t')


fil_akas = title_akas_data[title_akas_data['language'] == 'en' ]

print(fil_akas.region.value_counts().head(50))

filtered_titles = fil_akas[(
    fil_akas.region == 'CA') | (fil_akas.region == 'US')]['titleId'].unique()
index_of_title = list(filtered_titles).index('tt0120338')

#Filtered only US and CA region to avoid regional movies
fil_akas = fil_akas[(fil_akas.region == 'CA') | (fil_akas.region == 'US')]

fil_akas.describe(include='all')

unique_en_movie_ids = pd.DataFrame(list(set(fil_akas['titleId'])), columns=['tconsts_en'])
unique_en_movie_ids.to_csv("unique_en_movie_ids.csv", index=False)

unique_en_movie_ids = pd.read_csv("unique_en_movie_ids.csv")

len(set(unique_en_movie_ids))

title_basic_data_ori = df_title_basics.copy()

#cross referring the tconsts and keeping only those titles
title_basic_data_en = df_title_basics[
    df_title_basics['tconst'].isin(unique_en_movie_ids['tconsts_en'])]

title_basic_data_en_30yr = title_basic_data_en[title_basic_data_en['startYear']>1993]

title_basic_data_en_30yr.describe(include='all')

#Keeping only movies and those that have valid year
title_basic_data_en = title_basic_data_en[title_basic_data_en['titleType'] == 'movie']
title_basic_data_en = title_basic_data_en[title_basic_data_en['startYear'] != "\\N"]

title_basic_data_en.sort_values(by='startYear', axis = 0, inplace=True)

# Keeping only movies from the past. Future movies will not have box office collections
title_basic_data_en['startYear'] = title_basic_data_en['startYear'].astype(int)
title_basic_data_en = title_basic_data_en[title_basic_data_en['startYear'] <= 2023]

# Filtering on only the last 30 years
title_basic_data_en_70290yr = title_basic_data_en[
    (title_basic_data_en['startYear']<=1993) & (title_basic_data_en['startYear']>=1970)]

len(title_basic_data_en_70290yr)

title_basic_data_en_70290yr.to_csv("title_basic_data_en_70290yr.csv", index=False)

## Taking SNAPSHOT Cell
title_basic_data_en_30yr.to_csv("title_basic_data_en_30yr.csv", index=False)

# Web Scrapping
def scrape_movie_data(t_const):

    """
    Scrape movie data including worldwide collection, budget, and distributor.
    """
    try:
        worldwide_collection = ""
        distributor = ""
        budget = ""
        response = requests.get(f"https://www.boxofficemojo.com/title/{t_const}", timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        perf_summ_table = soup.find('div', class_='mojo-performance-summary-table')
        worldwide_collections = perf_summ_table.find_all('span', string=re.compile(r'.Worldwide*'))
        if worldwide_collections:
            worldwide_collection = worldwide_collections[0].parent.find_all(
                'span', class_="money")[0].text
        perf_table = soup.find('div', class_='mojo-summary-values')
        if perf_table:
            budgets = perf_table.find_all('span', string=re.compile(r'Budget'))
            if budgets:
                budget = budgets[0].next_sibling.text

            distributors = perf_table.find_all('span', string=re.compile(r'.Distributor*'))
            if distributors:
                distributor = distributors[0].next_sibling.text
                distributor = distributor[0:distributor.find("See full company information")]
        return (worldwide_collection, budget, distributor)
    except Exception as e:
        print(f"Error scraping movie {t_const}: {e}")
        return None

scrape_movie_data('tt8983210')

tconsts = title_basic_data_en['tconst'].tolist()

box_offices={}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    results = executor.map(scrape_movie_data, tconsts)

for tconst, result in zip(tconsts, results):
    box_offices[tconst] = result
    with open('box_offices.json', 'w', encoding='utf-8') as file:
        json.dump(box_offices, file)

len(title_basic_data_en['tconst'].unique())

print("hello")

data = pd.DataFrame({
    'numerical_feature_1': [1, 2, 3, 4, 5],
    'numerical_feature_2': [10, 20, 30, 40, 50],
    'categorical_feature': ['A', 'B', 'A', 'B', 'A'],
    'target': [20, 25, 30, 35, 40]
})

# Converting categorical feature to one-hot encoding
data = pd.get_dummies(data)
X = data.drop('target', axis=1)
y = data['target']

revenue1 = pd.read_csv('./revenue_prodcompany_70290yr_withbudget.csv')
revenue2 = pd.read_csv('./revenue_prodcompany_90-latyr_withbudget.csv')

revenue2.describe(include="all")

revenue_df =  pd.concat([revenue1, revenue2], ignore_index=True)

revenue_df.describe(include="all")

d = revenue_df[(revenue_df['Revenue'].notna())]

d.describe(include="all")

dt = d[(d['Production_Company'].notna())]

dt.describe(include="all")

dt.to_csv("tconsts_prd_company.csv", index=False)

revenue_df['Production_Company'].value_counts().head(20)
