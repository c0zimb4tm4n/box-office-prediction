"""
This module provides functionalities for input validation, prediction of movie ratings and revenues,
and evaluation of predicted values against historical data for movies. It utilizes machine learning
models loaded through joblib for prediction tasks.
"""
import streamlit as st
import pandas as pd

# pylint: disable=too-many-arguments,consider-iterating-dictionary,too-many-branches


def ratings_input_validation(actors, actresses, directors, writers, production_company, genre):
    """
    Validates input fields for predicting movie ratings. Replaces empty fields with default values.

    Args:
        actors (list): List of selected actors.
        actresses (list): List of selected actresses.
        directors (list): List of selected directors.
        writers (list): List of selected writers.
        production_company (str): The selected production company.
        genre (str): The selected genre.

    Returns:
        dict: A dictionary containing the validated input fields and a validity flag.
    """
    valid = True
    if genre is None:
        st.error("Please select a genre.", icon="🚨")
        valid = False
    actors = ["missing"] if not actors else actors
    actresses = ["missing"] if not actresses else actresses
    directors = ["missing"] if not directors else directors
    writers = ["missing"] if not writers else writers
    production_company = "" if production_company is None else production_company

    return {
        "valid": valid,
        "actors": actors,
        "actresses": actresses,
        "directors": directors,
        "writers": writers,
        "production_company": production_company,
        "genre": genre,
    }

def predict_rating(inputs, runtime_minutes, genre, ratings_model):
    """
    Predicts the movie rating based on user inputs using a preloaded machine learning model.

    Args:
        inputs (dict): Validated inputs including actors, actresses, directors, writers, 
        and production company.
        runtime_minutes (int): Runtime of the movie in minutes.
        genre (str): Genre of the movie.
        ratings_model: Preloaded machine learning model for predicting movie ratings.

    Returns:
        float: The predicted movie rating averaged over all combinations of inputs.
    """
    sum_rating = 0
    if inputs["valid"]:
        for actor_predict in inputs["actors"]:
            for actress_predict in inputs["actresses"]:
                for director_predict in inputs["directors"]:
                    for writer_predict in inputs["writers"]:
                        new_data = pd.DataFrame([{
                            "actor": actor_predict,
                            "actress": actress_predict,
                            "director": director_predict,
                            "writer": writer_predict,
                            "Production_Company": inputs["production_company"],
                            "runtimeMinutes": runtime_minutes,
                            "genres": genre,
                            "isAdult": 0,
                        }])
                        predicted_rating = ratings_model.predict(new_data)
                        sum_rating += predicted_rating[0]

    total_combinations = max(1, len(inputs["actors"]) * len(inputs["actresses"]) *
                             len(inputs["directors"]) * len(inputs["writers"]))
    return sum_rating / total_combinations



def predict_revenue(revenue, runtime_minutes, genre, revenue_model, predicted_rating):
    """
    Predicts the movie's revenue based on the validated inputs and a preloaded 
    machine learning model.

    Args:
        revenue (dict): Validated inputs including actors, actresses, directors, writers,
                        production company, and a validity flag.
        runtime_minutes (int): Runtime of the movie in minutes.
        genre (str): Genre of the movie.
        revenue_model: Preloaded machine learning model for predicting movie revenue.
        predicted_rating (float): The predicted movie rating.

    Returns:
        float: The predicted movie revenue averaged over all combinations of inputs.
    """
    sum_revenue = 0
    if revenue["valid"]:
        total_predictions = len(revenue["actors"]) * len(revenue["actresses"]) * \
                            len(revenue["directors"]) * len(revenue["writers"])
        if total_predictions == 0:
            return 0

        for actor_predict in revenue["actors"]:
            for actress_predict in revenue["actresses"]:
                for director_predict in revenue["directors"]:
                    for writer_predict in revenue["writers"]:
                        new_data = {
                            "actor": actor_predict,
                            "actress": actress_predict,
                            "director": director_predict,
                            "writer": writer_predict,
                            "Production_Company": revenue["production_company"],
                            "runtimeMinutes": runtime_minutes,
                            "genres": genre,
                            "isAdult": 0,
                            "averageRating": predicted_rating,
                        }
                        predicted_revenue = revenue_model.predict(pd.DataFrame([new_data]))
                        sum_revenue += predicted_revenue[0]

        return sum_revenue / total_predictions
    return 0


def has_crew_worked_before(findata, query):
    """
    Determines whether specified actors, actresses, and directors have previously 
    collaborated on movies within certain genres.

    Args:
        findata (pd.DataFrame): A pandas DataFrame containing movie data. The DataFrame
            is expected to have columns for 'tconst', 'genres', 'actor', 'actress', and
            'director', among others.
        query (dict): A dictionary specifying the crew members and genres to be checked.
            It should have four keys: 'actor', 'actress', 'director', and 'genres'. Each
            key should map to a list of strings, where 'genres' is a list of genres to
            filter the movies by, and 'actor', 'actress', 'director' are lists of names of
            the respective crew members.

    Returns:
        list: A list of strings, where each string is a 'tconst' identifier of a movie
            where at least two of the specified crew members have worked together within
            the specified genres. If no such movies exist, an empty list is returned.
    """
    print(query)
    actors, actresses, directors, genres = query.values()
    tconsts_map ={}
    for genre in genres:
        for actor in actors:
            filtered_data = findata[(findata['genres'] == genre) & (findata['actor'] == actor)]
            for tconst in filtered_data['tconst'].unique():
                if tconst in tconsts_map.keys():
                    if actor not in tconsts_map[tconst]:
                        tconsts_map[tconst].append(actor)
                else:
                    tconsts_map[tconst] = [actor]
        for actress in actresses:
            filtered_data = findata[(findata['genres'] == genre) & (findata['actress'] == actress)]
            for tconst in filtered_data['tconst'].unique():
                if tconst in tconsts_map.keys():
                    if actress not in tconsts_map[tconst]:
                        tconsts_map[tconst].append(actress)
                else:
                    tconsts_map[tconst] = [actress]
        for director in directors:
            filtered_data = findata[(findata['genres'] == genre) & (findata['director'] ==director)]
            for tconst in filtered_data['tconst'].unique():
                if tconst in tconsts_map.keys():
                    if director not in tconsts_map[tconst]:
                        tconsts_map[tconst].append(director)
                else:
                    tconsts_map[tconst] = [director]
    return ([key for key, value in tconsts_map.items() if len(value)>=2])

def evaluate_predicted_rating(findata, rating, query):
    """
    Evaluate the predicted rating by comparing it with the maximum average rating
    for factors specified in the query.

    Args:
    - findata (DataFrame): DataFrame containing the data for analysis.
    - rating (float): The predicted rating to evaluate.
    - query (dict): Dictionary containing factors as keys and lists of factor values
      as values.

    Returns:
    - results (dict): Dictionary containing the evaluation results for each factor
      specified in the query. Each key represents a factor, and the value is a list
      containing:
      - The factor value that corresponds to the maximum average rating.
      - The difference between the predicted rating and the maximum average rating.
      - The percentage difference between the predicted rating and the maximum 
      average rating.
    """
    def get_max_by_factor(factor_name):
        max_factor_rating = -1
        max_factor_value = ""
        for factor in query[factor_name]:
            avg_factor_rating = findata[findata[f"{factor_name}"] == factor][
                "averageRating"
            ].mean()
            if avg_factor_rating > max_factor_rating:
                max_factor_rating = avg_factor_rating
                max_factor_value = factor
        return (max_factor_value, max_factor_rating)

    results = {}
    for key in query.keys():
        max_val, max_rating = get_max_by_factor(f"{key}")
        if max_val != "" and max_rating != -1:
            results[f"{key}"] = [
                max_val,
                rating - max_rating,
                ((rating - max_rating) / max_rating) * 100,
            ]
    return results


def evaluate_predicted_revenue(findata, rating, query):
    """
    Evaluate the predicted revenue by comparing it with the maximum average revenue
    for factors specified in the query.

    Args:
    - findata (DataFrame): DataFrame containing the data for analysis.
    - rating (float): The predicted revenue to evaluate.
    - query (dict): Dictionary containing factors as keys and lists of factor 
    values as values.

    Returns:
    - results (dict): Dictionary containing the evaluation results for each factor
      specified in the query. Each key represents a factor, and the value is a list
      containing:
      - The factor value that corresponds to the maximum average revenue.
      - The difference between the predicted revenue and the maximum average revenue.
      - The percentage difference between the predicted revenue and the maximum 
      average revenue.
    """

    def get_max_by_factor(factor_name):
        max_factor_revenue = -1
        max_factor_value = ""
        for factor in query[factor_name]:
            avg_factor_revenue = findata[findata[f"{factor_name}"] == factor][
                "Revenue_InflationCorrected"
            ].mean()
            if avg_factor_revenue > max_factor_revenue:
                max_factor_revenue = avg_factor_revenue
                max_factor_value = factor
        return (max_factor_value, max_factor_revenue)

    results = {}
    for key in query.keys():
        max_val, max_revenue = get_max_by_factor(f"{key}")
        if max_val != "" and max_revenue != -1:
            results[f"{key}"] = [
                max_val,
                rating - max_revenue,
                ((rating - max_revenue) / max_revenue) * 100,
            ]
    return results
