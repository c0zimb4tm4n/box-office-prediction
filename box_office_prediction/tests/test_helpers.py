"""
Test cases for helpers module.
"""
# pylint: disable=missing-class-docstring,missing-function-docstring
import unittest
from unittest.mock import MagicMock
import pandas as pd
import os
import sys

current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_path)
sys.path.append(project_root)

from helpers import (
    ratings_input_validation,
    predict_rating,
    predict_revenue,
    has_crew_worked_before,
    evaluate_predicted_rating,
    evaluate_predicted_revenue,
)

class TestHelpers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_data = pd.DataFrame({
            'tconst': ['tt001', 'tt002'],
            'genres': ['Drama', 'Comedy'],
            'actor': ['Actor A', 'Actor B'],
            'actress': ['Actress A', 'Actress B'],
            'director': ['Director A', 'Director B'],
            'writer': ['Writer A', 'Writer B'],
            'Production_Company': ['Company A', 'Company B'],
            'runtimeMinutes': [120, 90],
            'averageRating': [7.5, 6.0],
            'Revenue_InflationCorrected': [100000, 200000]
        })
        cls.mock_ratings_model = MagicMock()
        cls.mock_ratings_model.predict.return_value = [7.0]
        cls.mock_revenue_model = MagicMock()
        cls.mock_revenue_model.predict.return_value = [150000]

    def test_ratings_input_validation(self):
        # Test validation with complete input
        complete_input = ratings_input_validation(
            ['Actor A'], ['Actress A'], ['Director A'], ['Writer A'], 'Company A', 'Drama'
        )
        self.assertTrue(complete_input['valid'])

        # Test validation with incomplete input
        incomplete_input = ratings_input_validation(
            [], [], [], [], None, None
        )
        self.assertFalse(incomplete_input['valid'])

    def test_predict_rating(self):
        inputs = {
            'valid': True,
            'actors': ['Actor A'],
            'actresses': ['Actress A'],
            'directors': ['Director A'],
            'writers': ['Writer A'],
            'production_company': 'Company A',
            'genre': 'Drama',
        }
        rating = predict_rating(inputs, 120, 'Drama', self.mock_ratings_model)
        self.assertEqual(rating, 7.0)

    def test_predict_revenue(self):
        revenue_input = {
            'valid': True,
            'actors': ['Actor A'],
            'actresses': ['Actress A'],
            'directors': ['Director A'],
            'writers': ['Writer A'],
            'production_company': 'Company A',
            'genre': 'Drama',
        }
        predicted_rating = 7.0
        revenue = predict_revenue(
            revenue_input, 120, 'Drama', self.mock_revenue_model, predicted_rating
        )
        self.assertEqual(revenue, 150000)

    def test_has_crew_worked_before(self):
        query = {
            'actor': ['Actor A'],
            'actress': ['Actress A'],
            'director': ['Director A'],
            'genres': ['Drama'],
        }
        result = has_crew_worked_before(self.mock_data, query)
        self.assertIn('tt001', result)

    def test_evaluate_predicted_rating(self):
        query = {'actor': ['Actor A'], 'genres': ['Drama']}
        rating_result = evaluate_predicted_rating(self.mock_data, 7.5, query)
        self.assertIn('actor', rating_result)
        self.assertEqual(rating_result['actor'][0], 'Actor A')

    def test_evaluate_predicted_revenue(self):
        query = {'actor': ['Actor A'], 'genres': ['Drama']}
        revenue_result = evaluate_predicted_revenue(self.mock_data, 100000, query)
        self.assertIn('actor', revenue_result)
        self.assertEqual(revenue_result['actor'][0], 'Actor A')

if __name__ == '__main__':
    unittest.main()
