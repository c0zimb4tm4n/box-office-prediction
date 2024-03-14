"""
Module to generate test data from a CSV file.
"""

import os
import random
import pandas as pd

def generate_data(filepath):
    """
    Generate test data from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        None
    """
    absolute_path = os.path.abspath(filepath)

    df = pd.read_csv(absolute_path)
    test_df = df.copy()

    for col in test_df.columns:
        test_df[col] = random.sample(test_df[col].tolist(), len(test_df[col]))
    test_df.head(1000).to_csv("test_data_movies.csv", index=False)

FILE_PATH = "./data/cleaned/data_clean_v6.csv"
generate_data(FILE_PATH)
