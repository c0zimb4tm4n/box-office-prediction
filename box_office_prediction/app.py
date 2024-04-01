"""
A Streamlit app designed to deliver insights into the film industry by 
offering functionalities for analyzing movie data, predicting IMDb ratings, 
and estimating box office revenues. Utilizing a combination of pandas for 
data manipulation, joblib for model loading, and plotly for interactive 
visualizations, this app presents a user-friendly interface for exploring 
various aspects of movie performance.

Features:
- Movie Analytics Dashboard: Allows users to explore top 
performers (actors and actresses) based on average revenue 
within selected genres. It also provides historical revenue trends 
for these top performers, offering insights into their commercial success over time.
- IMDb Movie Ratings Predictor: Enables users to predict IMDb 
ratings for hypothetical or upcoming movies based on input 
parameters such as genre, cast (actors and actresses), 
directors, writers, production house, and runtime.
- Box Office Revenue Predictor: Similar to the ratings 
predictor, this feature estimates potential box office revenue 
for movies based on similar input parameters, enriched with the 
predictive power of pre-loaded machine learning models.

Usage:
- Users interact with the app through a series of tabs, 
each dedicated to a specific functionality. Selection 
widgets allow for the customization of inputs, while 
action buttons trigger data processing and the generation 
of visualizations and predictions.
- The 'Movie Analytics Dashboard' tab provides filters 
for genre selection and displays charts representing 
top actors and actresses by revenue, alongside detailed 
performance trends.
- In the 'IMDb Movie Ratings Predictor' and 'Box Office 
Revenue Predictor' tabs, users fill in a series of inputs 
related to the movie's characteristics. Upon submission, 
the app uses pre-trained models to predict ratings and 
revenues, respectively, displaying the outcomes and 
offering comparative insights based on historical data.

Dependencies:
- pandas: For data manipulation and analysis.
- plotly: For generating interactive visualizations.
- streamlit: For creating and running the web app.
- joblib: For loading pre-trained machine learning models.
"""


# pylint: disable=invalid-name,import-error

import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from helpers import (
    ratings_input_validation,
    predict_rating,
    predict_revenue,
    evaluate_predicted_rating,
    evaluate_predicted_revenue,
    has_crew_worked_before,
)
import subprocess
import os

st.header("Box Office Genie", divider="grey")


####setup####
## Reading the data for front-end ##


df = pd.read_csv("data/cleaned/data_clean_v6.csv")

actors_all = list(df["actor"].unique())
actors_all.remove("missing")
actors_all.sort()
actors_all = tuple(actors_all)

actresses_all = list(df["actress"].unique())
actresses_all.remove("missing")
actresses_all.sort()
actresses_all = tuple(actresses_all)

directors_all = list(df["director"].unique())
directors_all.remove("missing")
directors_all.sort()
directors_all = tuple(directors_all)

writers_all = list(df["writer"].unique())
writers_all.remove("missing")
writers_all.sort()
writers_all = tuple(writers_all)

production_companies = list(df["Production_Company"].unique())
production_companies.sort()
production_companies = tuple(production_companies)

genres_all = list(df["genres"].unique())
genres_all.sort()
genres_all = tuple(genres_all)

## pulling the model ##
# Check if the files exist before downloading
if not os.path.exists("box_office_prediction/models/revenueModelv2.joblib"):
    subprocess.run(["gdown", "--id", "1zea9X4Rbw-2_VmHQlyajNPT3Fd3ngZ5B","-O", "box_office_prediction/models/revenueModelv2.joblib"])

if not os.path.exists("box_office_prediction/models/ratingModelv2.joblib"):
    subprocess.run(["gdown", "--id", "1ypQ1VkEJp8c3If2941axznVLgST4mSyU","-O", "box_office_prediction/models/ratingModelv2.joblib"])


ratings_model = joblib.load("box_office_prediction/models/ratingModelv2.joblib")

#### Declaring Tabs ####
tab1, tab2, tab3 = st.tabs(
    [
        "Movie Analytics Dashboard",
        "IMDb Movie Ratings Predictor",
        "Box Office Revenue Predictor",
    ]
)

# Setting up Tabs
with tab1:
    st.title("Movie Analytics Dashboard")

    tabactor, tabactress = st.tabs(["Actors", "Actresses"])

    with tabactor:
        genre_options = sorted(df["genres"].unique())
        excluded_genres = ["Documentary", "News", "Western"]
        filtered_genre_options = [
            genre for genre in genre_options if genre not in excluded_genres
        ]
        default_genre = genre_options[0]
        selected_genres = st.selectbox(
            "Select a genre:",
            options=filtered_genre_options,
            index=filtered_genre_options.index(default_genre),
        )

        st.header(f"Top Actors by Average Revenue in {selected_genres}")
        top_n_actors = st.number_input(
            "Number of top actors to display:", min_value=1, value=5, step=1
        )

        genre_filtered_df = df[df["genres"].str.contains(selected_genres)]

        actor_movie_counts = (
            genre_filtered_df.groupby("actor")["tconst"]
            .nunique()
            .reset_index(name="movie_count")
        )
        qualified_actors = actor_movie_counts[actor_movie_counts["movie_count"] >= 3][
            "actor"
        ]
        filtered_df = genre_filtered_df[
            genre_filtered_df["actor"].isin(qualified_actors)
        ]
        top_actors_df = (
            filtered_df.groupby("actor")["Revenue_InflationCorrected"]
            .mean()
            .nlargest(top_n_actors)
            .reset_index()
        )

        custom_red_scale = [[0, "lightcoral"], [0.5, "red"], [1.0, "darkred"]]
        fig_top_actors = px.bar(
            top_actors_df,
            x="actor",
            y="Revenue_InflationCorrected",
            title=f"Top {top_n_actors} Actors by Average Revenue",
            labels={"actor": "Actor", "Revenue_InflationCorrected": "Average Revenue"},
            color_discrete_sequence=["#C81621"],
            color="Revenue_InflationCorrected",
            color_continuous_scale=custom_red_scale,
            hover_data={"Revenue_InflationCorrected": ":,.0f"},
        )

        st.plotly_chart(fig_top_actors)

        highest_revenue_actor = top_actors_df["actor"].iloc[0]

        st.header("Actor's Performance")

        default_actor_index = (
            list(df["actor"].unique()).index(highest_revenue_actor)
            if highest_revenue_actor in df["actor"].unique()
            else 0
        )
        actor_filter = st.selectbox(
            "Select an actor:", options=df["actor"].unique(), index=default_actor_index
        )

        df["Revenue_InflationCorrected"] = df.groupby("tconst")[
            "Revenue_InflationCorrected"
        ].transform("mean")
        df_unique_tconsts = df.drop_duplicates(subset=["actor", "tconst"])
        filtered_df = df_unique_tconsts[
            (df_unique_tconsts["actor"] == actor_filter)
            & (
                df_unique_tconsts["genres"].apply(
                    lambda x: any(genre in x for genre in selected_genres)
                )
            )
        ]

        grouped_df = (
            filtered_df.groupby(["startYear", "genres"])["Revenue_InflationCorrected"]
            .sum()
            .reset_index()
        )
        title_list_df = (
            filtered_df.groupby(["startYear", "genres"])["primaryTitle"]
            .apply(list)
            .reset_index()
        )
        merged_df = pd.merge(grouped_df, title_list_df, on=["startYear", "genres"])
        fig = px.line(
            merged_df,
            x="startYear",
            y="Revenue_InflationCorrected",
            color="genres",
            markers=True,
            title=("Historical Revenue Trend for " + actor_filter +
               ": ℹ️ Double click on a Genre Below ℹ️"),
            labels={
                "startYear": "Year",
                "Revenue_InflationCorrected": "Revenue",
                "genres": "Genre",
            },
            hover_data=["primaryTitle"],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "Year: %{x}",
                    "Revenue: %{y}",
                    "Movie(s) appeared in: %{customdata[0]}",
                ]
            )
        )

        st.plotly_chart(fig)

    with tabactress:
        genre_options_act = sorted(df["genres"].unique())
        excluded_genres_act = ["Documentary", "News", "Western"]
        filtered_genre_options_act = [
            genre for genre in genre_options_act if genre not in excluded_genres_act
        ]
        default_genre_act = genre_options_act[0]
        selected_genres_act = st.selectbox(
            "Select a genre: ",
            options=filtered_genre_options_act,
            index=filtered_genre_options_act.index(default_genre_act),
        )

        st.header(f"Top Actresses by Average Revenue in {selected_genres_act}")
        top_n_actresses = st.number_input(
            "Number of top actresses to display:", min_value=1, value=5, step=1
        )

        genre_filtered_df = df[df["genres"].str.contains(selected_genres_act)]

        actress_movie_counts = (
            genre_filtered_df.groupby("actress")["tconst"]
            .nunique()
            .reset_index(name="movie_count")
        )
        qualified_actresses = actress_movie_counts[
            actress_movie_counts["movie_count"] >= 3
        ]["actress"]
        filtered_df = genre_filtered_df[
            genre_filtered_df["actress"].isin(qualified_actresses)
        ]
        top_actresses_df = (
            filtered_df.groupby("actress")["Revenue_InflationCorrected"]
            .mean()
            .nlargest(top_n_actresses)
            .reset_index()
        )

        custom_red_scale = [[0, "lightcoral"], [0.5, "red"], [1.0, "darkred"]]
        fig_top_actresses = px.bar(
            top_actresses_df,
            x="actress",
            y="Revenue_InflationCorrected",
            title=f"Top {top_n_actresses} Actresses by Average Revenue",
            labels={
                "actress": "Actress",
                "Revenue_InflationCorrected": "Average Revenue",
            },
            color_discrete_sequence=["#C81621"],
            color="Revenue_InflationCorrected",
            color_continuous_scale=custom_red_scale,
            hover_data={"Revenue_InflationCorrected": ":,.0f"},
        )

        st.plotly_chart(fig_top_actresses)

        highest_revenue_actress = top_actresses_df["actress"].iloc[0]

        st.header("Actresses' Performance")

        default_actress_index = (
            list(df["actress"].unique()).index(highest_revenue_actress)
            if highest_revenue_actress in df["actress"].unique()
            else 0
        )
        actress_filter = st.selectbox(
            "Select an actress:",
            options=df["actress"].unique(),
            index=default_actress_index,
        )

        df["Revenue_InflationCorrected"] = df.groupby("tconst")[
            "Revenue_InflationCorrected"
        ].transform("mean")
        df_unique_tconsts = df.drop_duplicates(subset=["actress", "tconst"])
        filtered_df = df_unique_tconsts[
            (df_unique_tconsts["actress"] == actress_filter)
            & (
                df_unique_tconsts["genres"].apply(
                    lambda x: any(genre in x for genre in selected_genres)
                )
            )
        ]

        grouped_df = (
            filtered_df.groupby(["startYear", "genres"])["Revenue_InflationCorrected"]
            .sum()
            .reset_index()
        )
        title_list_df = (
            filtered_df.groupby(["startYear", "genres"])["primaryTitle"]
            .apply(list)
            .reset_index()
        )
        merged_df = pd.merge(grouped_df, title_list_df, on=["startYear", "genres"])
        fig = px.line(
            merged_df,
            x="startYear",
            y="Revenue_InflationCorrected",
            color="genres",
            markers=True,
            title=("Historical Revenue Trend for " + actress_filter +
               ": ℹ️ Double click on a Genre Below ℹ️"),
            labels={
                "startYear": "Year",
                "Revenue_InflationCorrected": "Revenue",
                "genres": "Genre",
            },
            hover_data=["primaryTitle"],
        )

        fig.update_traces(
            hovertemplate="<br>".join(
                [
                    "Year: %{x}",
                    "Revenue: %{y}",
                    "Movie(s) appeared in: %{customdata[0]}",
                ]
            )
        )
        st.plotly_chart(fig)


with tab2:
    st.title("Movie Rating Prediction")
    # Input fields
    genre_ratings = st.selectbox(
        "Primary Genre",
        genres_all,
        index=None,
        key="genres_rating",
        placeholder="Type genre...",
    )
    actors_ratings = st.multiselect(
        "Actor",
        actors_all,
        key="actors_rating",
        placeholder="Type lead actors names...",
        max_selections=3,
    )
    actresses_ratings = st.multiselect(
        "Actress",
        actresses_all,
        key="actresses_rating",
        placeholder="Type lead actresses names...",
        max_selections=3,
    )
    directors_ratings = st.multiselect(
        "Directors",
        directors_all,
        key="directors_rating",
        placeholder="Type directors names...",
        max_selections=2,
    )
    writers_ratings = st.multiselect(
        "Writers",
        writers_all,
        key="writers_rating",
        placeholder="Type writers name...",
        max_selections=3,
    )
    production_company_ratings = st.selectbox(
        "Production House",
        production_companies,
        index=None,
        key="pcs_rating",
        placeholder="Type production house's name...",
    )

    runtime_minutes_ratings = st.number_input(
        "Runtime in Minutes",
        min_value=0,
        max_value=300,
        value=150,
        key="runtime_rating",
    )

    # is_adult = st.selectbox('Is Adult', options=[0, 1], index=0)

    col1, col2 = st.columns(2)
    # input validation
    inputs = {}
    predicted_rating = -1
    # Predict button
    with col1:
        if st.button("Predict Rating"):
            inputs = ratings_input_validation(
                actors_ratings,
                actresses_ratings,
                directors_ratings,
                writers_ratings,
                production_company_ratings,
                genre_ratings,
            )
            predicted_rating = predict_rating(
                inputs, runtime_minutes_ratings, genre_ratings, ratings_model
            )
            if inputs["valid"] is True:
                st.write(f"Predicted Ratings: {round(predicted_rating,2)}")
                with col2:
                    if inputs:
                        st.write("### Quick Insights")
                        # Define the content for each insight
                        query = {
                            "actor": inputs["actors"],
                            "actress": inputs["actresses"],
                            "director": inputs["directors"],
                            "genres": [genre_ratings],
                        }
                        prev_work = has_crew_worked_before(df, query)
                        ratings_results = evaluate_predicted_rating(df, predicted_rating, query)
                        print(ratings_results)
                        unique_content = ""
                        if prev_work:
                            unique_content += "**The crew has previously worked in:** \n\n"
                            for tconst in prev_work:
                                link = f"https://www.imdb.com/title/{tconst}"
                                matching_row = df.loc[df['tconst'] == tconst]
                                primary_title = matching_row['primaryTitle'].iloc[0]
                                link = f"https://www.imdb.com/title/{tconst}"
                                unique_content += f"- [{primary_title}]({link}) \n\n"
                            st.info(unique_content)

                        for key in list(ratings_results.keys()):
                            isnegative = ratings_results[key][2] < 0
                            if ratings_results[key][0] != "missing":
                                sentence = "The predicted rating is "
                                sentence += f"**{round(abs(ratings_results[key][2]))}%** "
                                if isnegative:
                                    sentence += "lower "
                                else:
                                    sentence += "higher "
                                sentence += f"than the average {ratings_results[key][0]} movie"
                                if isnegative:
                                    st.error(sentence)
                                else:
                                    st.success(sentence)


with tab3:
    revenue_model = joblib.load("box_office_prediction/models/revenueModelv2.joblib")

    st.title("Movie Revenue Prediction")
    # Input fields

    genre_revenue = st.selectbox(
        "Primary Genre",
        genres_all,
        index=None,
        key="genres_revenue",
        placeholder=genre_ratings if genre_ratings is not None else "Type genre...",
    )
    actors_revenue = st.multiselect(
        "Actor",
        actors_all,
        default=None if actors_ratings == [] else actors_ratings,
        key="actors_revenue",
        placeholder="Type lead actors names...",
        max_selections=3,
    )
    actresses_revenue = st.multiselect(
        "Actress",
        actresses_all,
        default=None if actresses_ratings == [] else actresses_ratings,
        key="actresses_revenue",
        placeholder="Type lead actresses names...",
        max_selections=3,
    )
    directors_revenue = st.multiselect(
        "Directors",
        directors_all,
        default=None if directors_ratings == [] else directors_ratings,
        key="directors_revenue",
        placeholder="Type directors names...",
        max_selections=2,
    )
    writers_revenue = st.multiselect(
        "Writers",
        writers_all,
        default=None if writers_ratings == [] else writers_ratings,
        key="writers_revenue",
        placeholder="Type writers name...",
        max_selections=3,
    )
    production_company_revenue = st.selectbox(
        "Production House",
        production_companies,
        index=None,
        key="pcs_revenue",
        placeholder=production_company_ratings
        if production_company_ratings is not None
        else "Type production house's name...",
    )

    runtime_minutes_revenue = st.number_input(
        "Runtime in Minutes",
        min_value=0,
        max_value=300,
        value=runtime_minutes_ratings,
        key="runtime_revenue",
    )
    # is_adult = st.selectbox('Is Adult', options=[0, 1], index=0)

    colrev1, colrev2 = st.columns(2)
    # Predict button
    predicted_revenue = -1
    # input validation
    revenue = {}
    with colrev1:
        if st.button("Predict Revenue"):
            revenue = ratings_input_validation(
                actors_revenue,
                actresses_revenue,
                directors_revenue,
                writers_revenue,
                production_company_revenue,
                genre_revenue,
            )
            try:
                if revenue != inputs:
                    predicted_rating = predict_rating(
                        revenue, runtime_minutes_revenue, genre_revenue, ratings_model
                    )
                predicted_revenue = predict_revenue(
                    revenue,
                    runtime_minutes_revenue,
                    genre_revenue,
                    revenue_model,
                    predicted_rating,
                )

            except NameError as e:
                predicted_rating = predict_rating(
                    revenue, runtime_minutes_revenue, genre_revenue, ratings_model
                )
                predicted_revenue = predict_revenue(
                    revenue,
                    runtime_minutes_revenue,
                    genre_revenue,
                    revenue_model,
                    predicted_rating,
                )
            if revenue["valid"] is True:
                st.write(
                    f"Predicted Revenue: ${round(predicted_revenue / 1_000_000, 1) } million"
                )
                with colrev2:
                    if revenue:
                        st.write("### Quick Insights")
                        # Define the content for each insight
                        query = {
                            "actor": revenue["actors"],
                            "actress": revenue["actresses"],
                            "director": revenue["directors"],
                            "genres": [genre_revenue],
                        }
                        prev_work = has_crew_worked_before(df, query)
                        revenue_results = evaluate_predicted_revenue(df, predicted_revenue, query)
                        print(revenue_results)
                        unique_content = ""
                        if prev_work:
                            unique_content += "**The crew has previously worked in:** \n\n"
                            for tconst in prev_work:
                                link = f"https://www.imdb.com/title/{tconst}"
                                primary_title = df[df['tconst'] == tconst]['primaryTitle'].iloc[0]
                                unique_content += f"- [{primary_title}]({link}) \n\n"
                            st.info(unique_content)

                        for key in list(revenue_results.keys()):
                            isnegative = revenue_results[key][2] < 0
                            if revenue_results[key][0] != "missing":
                                sentence = "The revenue rating is "
                                sentence += f"**{round(abs(revenue_results[key][2]))}%** "
                                if isnegative:
                                    sentence += "lower "
                                else:
                                    sentence += "higher "
                                sentence += f"than the average {revenue_results[key][0]} movie"
                                if isnegative:
                                    st.error(sentence)
                                else:
                                    st.success(sentence)
