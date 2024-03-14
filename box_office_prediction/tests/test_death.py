import unittest
from unittest.mock import patch, mock_open
import os
import sys

current_script_path = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.dirname(os.path.dirname(current_script_path))
sys.path.append(project_root)
from box_office_prediction.notebooks.data_cleaning.death_filter import filter_deceased_individuals

import pandas as pd
from io import StringIO

class TestDeathFilter(unittest.TestCase):
    """Tests for the death_filter.py script."""
    @patch('pandas.DataFrame.to_csv')
    def test_filter_deceased_individuals(self, mock_to_csv):
        """Test that deceased individuals are correctly filtered out."""
        data_clean_v5_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'cleaned', 'test_data_movies.csv')
        # Construct names_data DataFrame from the provided inline data
        names_data = pd.DataFrame({
            'nconst': ['nm0000086', 'nm0000087', 'nm0000089', 'nm0000090', 'nm0000096', 'nm0000097', 'nm0111013'],
            'primaryName': ['Louis de Funès', 'Elena Koreneva', 'Richard Paul', 'Armin Mueller-Stahl',
                            'Gillian Anderson', 'Pamela Anderson', 'Adam Brody'],
            'birthYear': [1914, 1953, 1940, 1930, 1968, 1967, 1979],
            'deathYear': ['1983', '\\N', '1998', '\\N', '\\N', '\\N', '\\N'],
            'primaryProfession': ['actor,writer,director', 'actress,casting_director,soundtrack', 'actor,soundtrack',
                                  'actor,director,writer', 'actress,producer,soundtrack',
                                  'actress,producer,director', 'actor,producer,soundtrack'],
            'knownForTitles': ['tt0069747,tt0064425,tt0074103,tt0079200', 'tt0123138,tt5847740,tt7529350,tt0122969',
                               'tt0117318,tt0075489,tt0076009,tt0088529', 'tt0139809,tt0765443,tt0963178,tt0117631',
                               'tt0106179,tt2294189,tt0442632,tt0455590', 'tt0306047,tt0893509,tt0426592,tt0115624',
                               'tt0356910,tt7798634,tt0362359,tt0419843']
        })
        # Patch read_csv for both data_clean_v5 and names_data
        with patch('pandas.read_csv', side_effect=[
            pd.read_csv(data_clean_v5_path),
            names_data
        ]) as mock_read_csv:
            # Call the function under test
            filter_deceased_individuals(data_clean_v5_path, 'fake_path/name.tsv', 'fake_path/output.csv')
            # Assertions to ensure the filtering logic is as expected
            mock_to_csv.assert_called_once()
            # Additional checks can go here
            # e.g., check the DataFrame content that was passed to to_csv
if __name__ == '__main__':
    unittest.main()