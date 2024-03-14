"""
Module to test the rating prediction model
"""
import unittest
import os
import joblib
import catboost as cb
import pandas as pd
from box_office_prediction.rating_model import train_model, predict_model

#pylint: disable=invalid-name, line-too-long,duplicate-code
class TestMovieRatingModel(unittest.TestCase):
    """
    A test case class for testing the movie rating model.

    This class contains methods to test the training and prediction functionality
    of the movie rating model.

    Attributes:
        df (pandas.DataFrame): The DataFrame containing the test data.
        X_test (pandas.DataFrame): The features of the test data.
        y_test (pandas.Series): The target variable of the test data.
        model (cb.CatBoostRegressor): The trained CatBoost regression model.
    """

    def setUp(self):
        """
        Set up test data and model for testing.

        This method is executed before each test method is run.
        It loads the test data, initializes the model, and prepares
        the test features and target variables.
        """
        self.df = pd.read_csv(os.path.abspath("./data/cleaned/test_data_movies.csv"))
        features = ['actor', 'actress', 'director', 'writer', 'Production_Company', 'runtimeMinutes', 'genres', 'isAdult']
        target = 'averageRating'
        self.X_test = self.df[features]
        self.y_test = self.df[target]
        self.model = joblib.load(os.path.abspath("./box_office_prediction/models/ratingModelv2.joblib"))

    def test_train_model_type(self):
        """
        Test the type of the trained model returned by train_model function.

        This test verifies whether the train_model function returns a trained
        CatBoost regression model.
        """
        m = train_model(self.df)
        self.assertIsInstance(m, cb.CatBoostRegressor)

    def test_predict_model(self):
        """
        Test the type and correctness of the prediction scores returned by predict_model function.

        This test verifies whether the predict_model function returns a tuple
        containing the root mean squared error (RMSE) and R^2 score, and if both
        scores are of type float.
        """
        rmse, r2 = predict_model(self.X_test, self.y_test, self.model)
        self.assertIsInstance(rmse, float)
        self.assertIsInstance(r2, float)

    def test_hypothetical_movie_rating_one_shot(self):
        """
        Test the hypothetical movie rating prediction.

        This test predicts the rating of a hypothetical movie using the trained
        model and verifies whether the predicted rating falls within the expected
        range of [6.0, 8.0].
        """
        hypothetical_movie = {
            'actor': 'Leonardo Dicaprio',
            'actress': 'Kate Winslet',
            'director': 'Christopher Nolan',
            'writer': 'Steven Spielberg',
            "Production_Company": "Twentieth Century Fox",
            'runtimeMinutes': 150,
            'genres': 'Thriller',
            'isAdult': 0
        }
        new_data = pd.DataFrame([hypothetical_movie])
        value = self.model.predict(new_data)
        print(value)
        self.assertGreaterEqual(value, 6.0)
        self.assertLessEqual(value, 8.0)

    def test_predict_model_empty_data(self):
        """
        Test prediction with empty input data.

        This test verifies whether the predict_model function raises a ValueError
        when provided with an empty DataFrame for input data.
        """
        with self.assertRaises(ValueError):
            predict_model(pd.DataFrame([]), self.y_test, self.model)
if __name__ == "__main__":
    unittest.main()
