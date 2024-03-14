"""
This module implements app tests for the app.py file.

It includes a series of unit tests for to examine the functionalities
of app.py file.
"""

# pylint: disable=import-error, wrong-import-position, too-many-public-methods

import unittest
import sys
import os

from streamlit.testing.v1 import AppTest

import numpy as np

current_script_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_script_path)
sys.path.append(project_root)

import app

class SimpleAppTest(unittest.TestCase):
    """
    Test suite for the our streamlit UI page in the project.

    The tests check if the designed streamlit pages displays as
    desired. There are various scenarios like, whether headers,
    titles, and labels are correctly listed, examing the default
    entry value, examing whether the placeholder text is as desired,
    examing whether the option list works as expected.
    """

    def setUp(self):
        """
        The function unittest framework automatically runs before
        each test.
        """
        self.at = AppTest.from_file('box_office_prediction/app.py').run(timeout=60)

    def test_headers(self):
        """
        This test checks whether the contents of the headers are
        displayed correctly as desired.
        """
        self.assertEqual(self.at.header[0].value,
                         'Box Office Genie')
        self.assertEqual(self.at.header[1].value,
                         'Top Actors by Average Revenue in Action')
        self.assertEqual(self.at.header[2].value,
                         "Actor's Performance")
        self.assertEqual(self.at.header[3].value,
                         'Top Actresses by Average Revenue in Action')
        self.assertEqual(self.at.header[4].value,
                         "Actresses' Performance")

    def test_titles(self):
        """
        This test checks whether the contents of the titles are
        displayed correctly as desired.
        """
        self.assertEqual(self.at.title[0].value, 'Movie Analytics Dashboard')
        self.assertEqual(self.at.title[1].value, 'Movie Rating Prediction')
        self.assertEqual(self.at.title[2].value, 'Movie Revenue Prediction')

    def test_tabactor_selected_genres_values(self):
        """
        This test checks whether "Action" genre is selected by default
        correctly in the "Select a genre" box in the Actors tab.
        """
        self.assertEqual(self.at.selectbox[0].value, 'Action')

    def test_tabactor_selected_genres_index(self):
        """
        This test checks whether the index value is set to the default
        genre type in the "Select a genre" box in the Actors tab.
        """
        tabactor_selected_genres_selectbox = self.at.selectbox[0]
        tabactor_selected_genres_index = (
            app.filtered_genre_options.index(app.default_genre)
        )

        self.assertEqual(tabactor_selected_genres_selectbox.index,
                         tabactor_selected_genres_index)

    def test_tabactor_selected_genres_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Select a genre" box in the Actors tab.
        """
        tabactor_selected_genres_selectbox = self.at.selectbox[0]
        tabactor_selected_genres_options = app.filtered_genre_options

        self.assertTrue(
            np.array_equal(
                tabactor_selected_genres_selectbox.options,
                tabactor_selected_genres_options
            )
        )

    def test_tabactor_actor_filter_values(self):
        """
        This test checks whether the highest revenue actor
        (Mark Ruffalo) is selected by default correctly in the
        "Select an actor" box.
        """
        tabactor_actor_filter_selectbox = self.at.selectbox[1]
        self.assertEqual(tabactor_actor_filter_selectbox.value,
                         app.highest_revenue_actor)

    def test_tabactor_actor_filter_index(self):
        """
        This test checks whether the index value is set to the default
        actor as displayed in the "Select an actor" box.
        """
        tabactor_actor_filter_selectbox = self.at.selectbox[1]
        tabactor_actor_filter_index = app.default_actor_index

        self.assertEqual(tabactor_actor_filter_selectbox.index,
                         tabactor_actor_filter_index)

    def test_tabactor_actor_filter_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Select an actor" box.
        """
        tabactor_actor_filter_selectbox = self.at.selectbox[1]
        tabactor_actor_filter_options = app.df['actor'].unique()

        self.assertTrue(
            np.array_equal(
                tabactor_actor_filter_selectbox.options,
                tabactor_actor_filter_options
            )
        )

    def test_tabactress_selected_genres_act_values(self):
        """
        This test checks whether "Action" genre is selected by default
        correctly in the "Select a genre" box in the Actresses tab.
        """
        tabactress_selected_genres_act_selectbox = self.at.selectbox[2]
        self.assertEqual(tabactress_selected_genres_act_selectbox.value,
                         app.genre_options_act[0])

    def test_tabactress_selected_genres_act_index(self):
        """
        This test checks whether the index value is set to the default
        genre type in the "Select a genre" box in the Actresses tab.
        """
        tabactress_selected_genres_act_selectbox = self.at.selectbox[2]
        tabactress_selected_genres_act_index = (
            app.filtered_genre_options_act.index(app.default_genre_act)
        )
        self.assertEqual(tabactress_selected_genres_act_selectbox.index,
                         tabactress_selected_genres_act_index)

    def test_tabactress_selected_genres_act_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Select a genre" box in the Actresses tab.
        """
        tabactress_selected_genres_act_selectbox = self.at.selectbox[2]
        tabactress_selected_genres_act_options = (
            app.filtered_genre_options_act
        )

        self.assertTrue(
            np.array_equal(
                tabactress_selected_genres_act_selectbox.options,
                tabactress_selected_genres_act_options
            )
        )

    def test_tabactress_actress_filter_values(self):
        """
        This test checks whether the highest revenue actress
        (Daisy Ridley) is selected by default correctly in the
        "Select an actress" box.
        """
        tabactress_actress_filter_selectbox = self.at.selectbox[3]
        self.assertEqual(tabactress_actress_filter_selectbox.value,
                         app.highest_revenue_actress)

    def test_tabactress_actress_filter_index(self):
        """
        This test checks whether the index value is set to the default
        actorress as displayed in the "Select an actress" box.
        """
        tabactress_actress_filter_selectbox = self.at.selectbox[3]
        tabactress_actress_filter_index = app.default_actress_index

        self.assertEqual(tabactress_actress_filter_selectbox.index,
                         tabactress_actress_filter_index)

    def test_tabactress_actress_filter_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Select an actress" box.
        """
        tabactress_actress_filter_selectbox = self.at.selectbox[3]
        tabactress_actress_filter_options = app.df['actress'].unique()

        self.assertTrue(
            np.array_equal(
                tabactress_actress_filter_selectbox.options,
                tabactress_actress_filter_options
            )
        )

    def test_genre_ratings_value(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Primary Genre" box.
        """
        genre_ratings_selectbox = self.at.selectbox[4]

        self.assertEqual(genre_ratings_selectbox.value, None)

    def test_genre_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type
        genre..." by default correctly in the "Primary Genre" box.
        """
        genre_ratings_selectbox = self.at.selectbox[4]
        genre_ratings_placeholder_text = "Type genre..."

        self.assertEqual(genre_ratings_selectbox.placeholder,
                         genre_ratings_placeholder_text)

    def test_genre_ratings_index(self):
        """
        This test checks whether there is no index value
        by default correctly in the "Primary Genre" box.
        """
        genre_ratings_selectbox = self.at.selectbox[4]
        genre_ratings_index = None

        self.assertEqual(genre_ratings_selectbox.index, genre_ratings_index)

    def test_genre_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Primary Genre" box.
        """
        genre_ratings_selectbox = self.at.selectbox[4]
        genre_ratings_options = app.genres_all

        self.assertEqual(tuple(genre_ratings_selectbox.options),
                         genre_ratings_options)

    def test_production_company_ratings_value(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Production House" box.
        """
        production_company_ratings_selectbox = self.at.selectbox[5]

        self.assertEqual(production_company_ratings_selectbox.value, None)

    def test_production_company_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type
        production house's name..." by default correctly in the
        "Production House" box.
        """
        production_company_ratings_selectbox = self.at.selectbox[5]
        production_company_ratings_placeholder_text = (
            "Type production house's name..."
        )

        self.assertEqual(production_company_ratings_selectbox.placeholder,
                         production_company_ratings_placeholder_text)

    def test_production_company_ratings_index(self):
        """
        This test checks whether there is no index value
        by default correctly in the "Production House" box.
        """
        production_company_ratings_selectbox = self.at.selectbox[5]
        production_company_ratings_index = None

        self.assertEqual(production_company_ratings_selectbox.index,
                         production_company_ratings_index)

    def test_production_company_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Production House" box.
        """
        production_company_ratings_selectbox = self.at.selectbox[5]
        production_company_ratings_options = app.production_companies

        self.assertEqual(tuple(production_company_ratings_selectbox.options),
                         production_company_ratings_options)

    def test_genre_revenue_value(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Primary Genre" box.
        """
        genre_revenue_selectbox = self.at.selectbox[6]

        self.assertEqual(genre_revenue_selectbox.value, None)

    def test_genre_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type
        genre..." by default correctly in the "Primary Genre" box.
        """
        genre_revenue_selectbox = self.at.selectbox[6]
        genre_revenue_placeholder_text = "Type genre..."

        self.assertEqual(genre_revenue_selectbox.placeholder,
                         genre_revenue_placeholder_text)

    def test_genre_revenue_index(self):
        """
        This test checks whether there is no index value
        by default correctly in the "Production House" box.
        """
        genre_revenue_selectbox = self.at.selectbox[6]
        genre_revenue_index = None

        self.assertEqual(genre_revenue_selectbox.index, genre_revenue_index)

    def test_genre_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Primary Genre" box.
        """
        genre_revenue_selectbox = self.at.selectbox[6]
        genre_revenue_options = app.genres_all

        self.assertEqual(tuple(genre_revenue_selectbox.options),
                         genre_revenue_options)

    def test_production_company_revenue_value(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Production House" box.
        """
        production_company_revenue_selectbox = self.at.selectbox[7]

        self.assertEqual(production_company_revenue_selectbox.value, None)

    def test_production_company_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type
        production house's name..." by default correctly in the
        "Production House" box.
        """
        production_company_revenue_selectbox = self.at.selectbox[7]
        production_company_revenue_placeholder_text = (
            "Type production house's name..."
        )

        self.assertEqual(production_company_revenue_selectbox.placeholder,
                         production_company_revenue_placeholder_text)

    def test_production_company_revenue_index(self):
        """
        This test checks whether there is no index value
        by default correctly in the "Production House" box.
        """
        production_company_revenue_selectbox = self.at.selectbox[7]
        production_company_revenue_index = None

        self.assertEqual(production_company_revenue_selectbox.index,
                         production_company_revenue_index)

    def test_production_company_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Production House" box.
        """
        production_company_revenue_selectbox = self.at.selectbox[7]
        production_company_revenue_options = app.production_companies

        self.assertEqual(tuple(production_company_revenue_selectbox.options),
                         production_company_revenue_options)

    def test_tabactor_top_n_actors(self):
        """
        This test checks whether the amount of top actors to be
        displayed is set to 5 by default correctly in the "Number of
        top actors to display" box in the Actors tab.
        """
        tabactor_top_n_actors_value = self.at.number_input[0].value
        self.assertEqual(tabactor_top_n_actors_value, 5)

    def test_tabactress_top_n_actors(self):
        """
        This test checks whether the amount of top actresses to be
        displayed is set to 5 by default correctly in the "Number of
        top actresses to display" box in the Actresses tab.
        """
        tabactress_top_n_actresses_value = self.at.number_input[1].value
        self.assertEqual(tabactress_top_n_actresses_value, 5)

    def test_runtime_minutes_ratings(self):
        """
        This test checks whether the length of runtime in minute is set
        to 150 by default correctly in the "Runtime in Minutes" box.
        """
        runtime_minutes_ratings_value = self.at.number_input[2].value
        self.assertEqual(runtime_minutes_ratings_value, 150)

    def test_runtime_minutes_revenue(self):
        """
        This test checks whether the length of runtime in minute is set
        to 150 by default correctly in the "Runtime in Minutes" box.
        """
        runtime_minutes_revenue_value = self.at.number_input[3].value
        self.assertEqual(runtime_minutes_revenue_value, 150)

    def test_actors_ratings(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Actor" box.
        """
        actors_ratings_multiselect = self.at.multiselect[0]

        self.assertEqual(actors_ratings_multiselect.value, [])

    def test_actors_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        actors names..." by default correctly in the "Actor" box.
        """
        actors_ratings_multiselect = self.at.multiselect[0]
        actors_ratings_placeholder_text = "Type lead actors names..."

        self.assertEqual(actors_ratings_multiselect.placeholder,
                         actors_ratings_placeholder_text)

    def test_actors_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Actor" box.
        """
        actors_ratings_multiselect = self.at.multiselect[0]
        actors_ratings_options = app.actors_all

        self.assertEqual(tuple(actors_ratings_multiselect.options),
                         actors_ratings_options)

    def test_actresses_ratings(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Actress" box.
        """
        actresses_ratings_multiselect = self.at.multiselect[1]

        self.assertEqual(actresses_ratings_multiselect.value, [])

    def test_actresses_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        actresses names..." by default correctly in the "Actress" box.
        """
        actresses_ratings_multiselect = self.at.multiselect[1]
        actresses_ratings_placeholder_text = "Type lead actresses names..."

        self.assertEqual(actresses_ratings_multiselect.placeholder,
                         actresses_ratings_placeholder_text)

    def test_actresses_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Actress" box.
        """
        actresses_ratings_multiselect = self.at.multiselect[1]
        actresses_ratings_options = app.actresses_all

        self.assertEqual(tuple(actresses_ratings_multiselect.options),
                         actresses_ratings_options)

    def test_directors_ratings(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Directors" box.
        """
        directors_ratings_multiselect = self.at.multiselect[2]

        self.assertEqual(directors_ratings_multiselect.value, [])

    def test_directors_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        directors names..." by default correctly in the
        "Directors" box.
        """
        directors_ratings_multiselect = self.at.multiselect[2]
        directors_ratings_placeholder_text = "Type directors names..."

        self.assertEqual(directors_ratings_multiselect.placeholder,
                         directors_ratings_placeholder_text)

    def test_directors_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the of results we created from the dataset
        in the "Directors" box.
        """
        directors_ratings_multiselect = self.at.multiselect[2]
        directors_ratings_options = app.directors_all

        self.assertEqual(tuple(directors_ratings_multiselect.options),
                         directors_ratings_options)

    def test_writers_ratings(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Writers" box.
        """
        writers_ratings_multiselect = self.at.multiselect[3]

        self.assertEqual(writers_ratings_multiselect.value, [])

    def test_writers_ratings_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type writers
        name..." by default correctly in the
        "Writers" box.
        """
        writers_ratings_multiselect = self.at.multiselect[3]
        writers_ratings_placeholder_text = "Type writers name..."

        self.assertEqual(writers_ratings_multiselect.placeholder,
                         writers_ratings_placeholder_text)

    def test_writers_ratings_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Writers" box.
        """
        writers_ratings_multiselect = self.at.multiselect[3]
        writers_ratings_options = app.writers_all

        self.assertEqual(tuple(writers_ratings_multiselect.options),
                         writers_ratings_options)

    def test_actors_revenue(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Actor" box.
        """
        actors_revenue_multiselect = self.at.multiselect[4]

        self.assertEqual(actors_revenue_multiselect.value, [])

    def test_actors_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        actors names..." by default correctly in the "Actor" box.
        """
        actors_revenue_multiselect = self.at.multiselect[4]
        actors_revenue_placeholder_text = "Type lead actors names..."

        self.assertEqual(actors_revenue_multiselect.placeholder,
                         actors_revenue_placeholder_text)

    def test_actors_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Actor" box.
        """
        actors_revenue_multiselect = self.at.multiselect[4]
        actors_revenue_options = app.actors_all

        self.assertEqual(tuple(actors_revenue_multiselect.options),
                         actors_revenue_options)

    def test_actresses_revenue(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Actress" box.
        """
        actresses_revenue_multiselect = self.at.multiselect[5]

        self.assertEqual(actresses_revenue_multiselect.value, [])

    def test_actresses_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        actresses names..." by default correctly in the "Actress" box.
        """
        actresses_revenue_multiselect = self.at.multiselect[5]
        actresses_revenue_placeholder_text = "Type lead actresses names..."

        self.assertEqual(actresses_revenue_multiselect.placeholder,
                         actresses_revenue_placeholder_text)

    def test_actresses_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Actress" box.
        """
        actresses_revenue_multiselect = self.at.multiselect[5]
        actresses_revenue_options = app.actresses_all

        self.assertEqual(tuple(actresses_revenue_multiselect.options),
                         actresses_revenue_options)

    def test_directors_revenue(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Directors" box.
        """
        directors_revenue_multiselect = self.at.multiselect[6]

        self.assertEqual(directors_revenue_multiselect.value, [])

    def test_directors_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type lead
        directors names..." by default correctly in the
        "Directors" box.
        """
        directors_revenue_multiselect = self.at.multiselect[6]
        directors_revenue_placeholder_text = "Type directors names..."

        self.assertEqual(directors_revenue_multiselect.placeholder,
                         directors_revenue_placeholder_text)

    def test_directors_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the
        dataset in the "Directors" box.
        """
        directors_revenue_multiselect = self.at.multiselect[6]
        directors_revenue_options = app.directors_all

        self.assertEqual(tuple(directors_revenue_multiselect.options),
                         directors_revenue_options)

    def test_writers_revenue(self):
        """
        This test checks whether the there is no input by default
        correctly in the "Writers" box.
        """
        writers_revenue_multiselect = self.at.multiselect[7]

        self.assertEqual(writers_revenue_multiselect.value, [])

    def test_writers_revenue_placeholder_text(self):
        """
        This test checks whether the placeholder text is "Type writers
        names..." by default correctly in the
        "Writers" box.
        """
        writers_revenue_multiselect = self.at.multiselect[7]
        writers_revenue_placeholder_text = "Type writers name..."

        self.assertEqual(writers_revenue_multiselect.placeholder,
                         writers_revenue_placeholder_text)

    def test_writers_revenue_options(self):
        """
        This test checks whether the selectable values as shown in the
        drop down menu match the results we created from the dataset
        in the "Writers" box.
        """
        writers_revenue_multiselect = self.at.multiselect[7]
        writers_revenue_options = app.writers_all

        self.assertEqual(tuple(writers_revenue_multiselect.options),
                         writers_revenue_options)

if __name__ == '__main__':
    unittest.main()
