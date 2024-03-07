import streamlit as st
import pandas as pd
import joblib


st.header('Box Office Genie', divider='red')

#setup
df = pd.read_csv('cleaned_data/data_clean_v5.csv')
actors_all = tuple(list(df['actor'].unique()))
actresses_all = tuple(list(df['actress'].unique()))
directors_all = tuple(list(df['director'].unique()))
writers_all = tuple(list(df['writer'].unique()))
production_companies = tuple(list(df['Production_Company'].unique()))
genres_all = tuple(list(df['genres'].unique()))

ratings_model = joblib.load("./helpers/ratingModelv1.joblib")

#Declaring Tabs
tab1, tab2, tab3 = st.tabs(["Movie Analytics Dashboard", "IMDb Movie Ratings Predictor", "Box Office Revenue Predictor"])

#Setting up Tabs
with tab1:
   st.header("Movie Analytics Dashboard")
   # Streamlit app layout
   st.title('CatBoost Model Prediction')
   feature1 = st.number_input('Feature 1', min_value=0.0, max_value=100.0, value=50.0)
   feature2 = st.number_input('Feature 2', min_value=0.0, max_value=100.0, value=50.0)
   # Add more features as needed
   
   

with tab2:
   st.title('Movie Rating Prediction')
   # Input fields
   actors = st.multiselect(
      'Actor',
      actors_all,
      key="actors_rating",
      placeholder="Type lead actors names...",
      max_selections=3
    )
   actresses = st.multiselect(
      'Actress',
      actresses_all,
      key="actresses_rating",
      placeholder="Type lead actresses names...",
      max_selections=3
    )
   directors = st.multiselect(
      'Directors',
      directors_all,
      key="directors_rating",
      placeholder="Type directors names...",
      max_selections=3
    )
   writers = st.multiselect(
      'Writers',
      writers_all,
      key="writers_rating",
      placeholder="Type lead actress's name...",
      max_selections=3
    )
   production_company = st.selectbox(
      'Production House',
      production_companies,
      index=None,
      key="pcs_rating",
      placeholder="Type production house's name..."
    )
   
   runtime_minutes = st.number_input('Runtime in Minutes', min_value=0, max_value=300 ,value=150)
   genre  = st.selectbox(
      'Primary Genre',
      genres_all,
      index=None,
      key="genres_rating",
      placeholder="Type genre..."
    )
   is_adult = st.selectbox('Is Adult', options=[0, 1], index=0)
   
   # Predict button
   if st.button('Predict'):
      sum_rating = 0
      for actor_predict in actors:
         for actress_predict in actresses:
            for director_predict in directors:
               for writer_predict in writers:
                  new_data = pd.DataFrame([{
                     'actor': actor_predict ,
                     'actress': actress_predict,
                     'director': director_predict,
                     'writer': writer_predict,
                     "Production_Company": production_company,
                     'runtimeMinutes': runtime_minutes,
                     'genres': genre,
                     'isAdult': 0
                  }])
                  predicted_rating = ratings_model.predict(new_data)
                  #st.write(f'Predicted Rating: {predicted_rating[0]}')
                  sum_rating = predicted_rating[0] + sum_rating
      st.write(f'Predicted Rating: {sum_rating/(len(actors)*len(actresses)*len(directors)*len(writers))}')

with tab3:
   st.title('Movie Revenue Prediction')
   # Input fields
   # actor2 = st.multiselect(
   #    'Actor',
   #    actors,
   #    key="actors_revenue",
   #    placeholder = actors if actors!= [] else "Type lead actor's name...",
   #    max_selections=3
   #  )
   # actress2 = st.text_input('Actress', value='')
   # director2 = st.text_input('Director', value='')
   # writer2 = st.text_input('Writer', value='')
   # runtime_minutes2 = st.number_input('Runtime Minutes', min_value=0, value=150)
   # genres2 = st.text_input('Genres', value='Horror')
   # is_adult2 = st.selectbox('Is Adult', options=[0, 1], index=0)

