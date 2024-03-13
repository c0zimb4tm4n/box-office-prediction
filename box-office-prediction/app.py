import streamlit as st
import pandas as pd
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# local_css("styles.css")


def ratings_input_validation(actors, actresses, directors, writers, production_company, genre):
   valid = True
   if genre == None:
      st.error('Please select a genre.', icon="🚨")
      valid = False
   if actors == []:
      actors = ["missing"]
   if actresses == []:
      actresses = ["missing"]
   if directors == []:
      directors = ["missing"]
   if writers == []:
      writers = ["missing"]
   if production_company == None:
      production_company = ""
      
   return {
      "valid": valid,
      "actors":  actors, 
      "actresses": actresses, 
      "directors": directors, 
      "writers": writers, 
      "production_company": production_company, 
      "genre": genre
   }

st.header('Box Office Genie', divider='grey')

#setup
df = pd.read_csv("../data/cleaned/data_clean_v6.csv")
actors_all = list(df['actor'].unique())
actors_all.remove("missing")
actors_all.sort()
actors_all = tuple(actors_all)

actresses_all = list(df['actress'].unique())
actresses_all.remove("missing")
actresses_all.sort()
actresses_all = tuple(actresses_all)

directors_all = list(df['director'].unique())
directors_all.remove("missing")
directors_all.sort()
directors_all = tuple(directors_all)

writers_all = list(df['writer'].unique())
writers_all.remove("missing")
writers_all.sort()
writers_all = tuple(writers_all)

production_companies = list(df['Production_Company'].unique())
production_companies.sort()
production_companies = tuple(production_companies)

genres_all = list(df['genres'].unique())
genres_all.sort()
genres_all = tuple(genres_all)

ratings_model = joblib.load("./models/ratingModelv1.joblib")

#Declaring Tabs
tab1, tab2, tab3 = st.tabs(["Movie Analytics Dashboard", "IMDb Movie Ratings Predictor", "Box Office Revenue Predictor"])









#Setting up Tabs
with tab1:
   st.header("Movie Analytics Dashboard")

   #st.title('XXXX')

   #genre_options = df['genres'].unique()
   #selected_genres = st.multiselect('Select genres:', options=genre_options, default=genre_options)
   genre_options = sorted(df['genres'].unique())  # Sorting genres alphabetically
   default_genre = genre_options[0]  # Setting the default genre to the first genre alphabetically
   selected_genres = st.selectbox('Select a genre:', options=genre_options, index=genre_options.index(default_genre))
   

   # Create tabs for actors and actresses
   tabactor, tabactress = st.tabs(["Actors", "Actresses"])


   with tabactor:

      # Top actors by average revenue
      st.header('Top Actors by Average Revenue in Selected Genres')
      top_n_actors = st.number_input('Number of top actors to display:', min_value=1, value=5, step=1)
      genre_filtered_df = df[df['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]
      top_actors_df = genre_filtered_df.groupby('actor')['Revenue_InflationCorrected'].mean().nlargest(top_n_actors).reset_index()
      fig_top_actors = px.bar(top_actors_df, x='actor', y='Revenue_InflationCorrected',
                              title=f'Top {top_n_actors} Actors by Average Revenue',
                              labels={'Revenue_InflationCorrected': 'Average Revenue'})
      st.plotly_chart(fig_top_actors)


      st.header("Actor's Performance")
      actor_filter = st.selectbox('Select an actor:', df['actor'].unique())
      filtered_df = df[(df['actor'] == actor_filter) & (df['genres'].apply(lambda x: any(genre in x for genre in selected_genres)))]
      grouped_df = filtered_df.groupby(['startYear', 'genres'])['Revenue_InflationCorrected'].sum().reset_index()
      title_list_df = filtered_df.groupby(['startYear', 'genres'])['primaryTitle'].apply(list).reset_index()
      merged_df = pd.merge(grouped_df, title_list_df, on=['startYear', 'genres'])
      fig = px.line(merged_df, x='startYear', y='Revenue_InflationCorrected', color='genres', markers=True,
                     title=f'Historical Revenue Trend for {actor_filter} Across Selected Genres',
                     labels={'startYear': 'Year', 'Revenue_InflationCorrected': 'Revenue', 'genres': 'Genre'},
                     hover_data=['primaryTitle'])
      st.plotly_chart(fig)


      

   with tabactress:
   # Top actresses by average revenue
      st.header('Top Actresses by Average Revenue in Selected Genres')
      top_n_actresses = st.number_input('Number of top actresses to display:', min_value=1, value=5, step=1)
      top_actresses_df = genre_filtered_df.groupby('actress')['Revenue_InflationCorrected'].mean().nlargest(top_n_actresses).reset_index()
      fig_top_actresses = px.bar(top_actresses_df, x='actress', y='Revenue_InflationCorrected',
                                 title=f'Top {top_n_actresses} Actresses by Average Revenue',
                                 labels={'Revenue_InflationCorrected': 'Average Revenue'})
      st.plotly_chart(fig_top_actresses)

      st.header("Actress's Performance")
      actress_filter = st.selectbox('Select an actress:', df['actress'].unique())
      filtered_df = df[(df['actress'] == actress_filter) & (df['genres'].apply(lambda x: any(genre in x for genre in selected_genres)))]
      grouped_df = filtered_df.groupby(['startYear', 'genres'])['Revenue_InflationCorrected'].sum().reset_index()
      fig = px.line(grouped_df, x='startYear', y='Revenue_InflationCorrected', color='genres',
                     title=f'Historical Revenue Trend for {actress_filter} Across Selected Genres',
                     labels={'startYear': 'Year', 'Revenue_InflationCorrected': 'Revenue', 'genres': 'Genre'})
      st.plotly_chart(fig)


   production_revenue_df = genre_filtered_df.groupby('Production_Company')['Revenue_InflationCorrected'].sum().reset_index()

   fig = px.treemap(production_revenue_df, path=['Production_Company'], values='Revenue_InflationCorrected',
                  title='Market Share of Production Houses in Selected Genres',
                  labels={'Production_Company': 'Production House', 'Revenue_InflationCorrected': 'Revenue'},
                  color='Revenue_InflationCorrected', color_continuous_scale='RdYlGn',
                  hover_data={'Production_Company': True, 'Revenue_InflationCorrected': ':,.2f'})

   fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
   st.plotly_chart(fig)












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
      max_selections=2
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
   
   runtime_minutes =  st.number_input(
      'Runtime in Minutes', 
      min_value=0, 
      max_value=300 ,
      value=150,
      key="runtime_rating",
      )
   
   genre  = st.selectbox(
      'Primary Genre',
      genres_all,
      index=None,
      key="genres_rating",
      placeholder="Type genre..."
    )
   #is_adult = st.selectbox('Is Adult', options=[0, 1], index=0)
   
   # Predict button
   if st.button('Predict Rating'):

      #input validation 
      inputs = ratings_input_validation(actors, actresses, directors, writers, production_company, genre)

      sum_rating = 0
      if inputs["valid"] == True:
         for actor_predict in inputs["actors"]:
            for actress_predict in inputs["actresses"]:
               for director_predict in inputs["directors"] :
                  for writer_predict in inputs["writers"]:
                     new_data = pd.DataFrame([{
                        'actor': actor_predict ,
                        'actress': actress_predict,
                        'director': director_predict,
                        'writer': writer_predict,
                        "Production_Company": inputs["production_company"],
                        'runtimeMinutes': runtime_minutes,
                        'genres': genre,
                        'isAdult': 0
                     }])
                     predicted_rating = ratings_model.predict(new_data)
                     #st.write(f'Predicted Rating: {predicted_rating[0]}')
                     sum_rating = predicted_rating[0] + sum_rating
         
      
         st.write(f'Predicted Rating: {sum_rating/(len(inputs["actors"])*len(inputs["actresses"])*len(inputs["directors"])*len(inputs["writers"]))}')

with tab3:
   revenue_model = joblib.load("./models/revenueModelv2.joblib")
   st.title('Movie Revenue Prediction')
   # Input fields
   actors = st.multiselect(
      'Actor',
      actors_all,
      key="actors_revenue",
      placeholder="Type lead actors names...",
      max_selections=3
    )
   actresses = st.multiselect(
      'Actress',
      actresses_all,
      key="actresses_revenue",
      placeholder="Type lead actresses names...",
      max_selections=3
    )
   directors = st.multiselect(
      'Directors',
      directors_all,
      key="directors_revenue",
      placeholder="Type directors names...",
      max_selections=2
    )
   writers = st.multiselect(
      'Writers',
      writers_all,
      key="writers_revenue",
      placeholder="Type lead actress's name...",
      max_selections=3
    )
   production_company = st.selectbox(
      'Production House',
      production_companies,
      index=None,
      key="pcs_revenue",
      placeholder="Type production house's name..."
    )
   
   runtime_minutes = st.number_input(
      'Runtime in Minutes', 
      min_value=0, 
      max_value=300 ,
      value=150,
      key="runtime_revenue",
      )
   genre  = st.selectbox(
      'Primary Genre',
      genres_all,
      index=None,
      key="genres_revenue",
      placeholder="Type genre..."
    )
   #is_adult = st.selectbox('Is Adult', options=[0, 1], index=0)
   
   # Predict button
   if st.button('Predict Revenue'):

      #input validation 
      revenue = ratings_input_validation(actors, actresses, directors, writers, production_company, genre)

      sum_revenue = 0
      if revenue["valid"] == True:
         for actor_predict in revenue["actors"]:
            for actress_predict in revenue["actresses"]:
               for director_predict in revenue["directors"] :
                  for writer_predict in revenue["writers"]:
                     new_data = pd.DataFrame([{
                        'actor': actor_predict ,
                        'actress': actress_predict,
                        'director': director_predict,
                        'writer': writer_predict,
                        "Production_Company": revenue["production_company"],
                        'runtimeMinutes': runtime_minutes,
                        'genres': genre,
                        'isAdult': 0
                     }])
                     predicted_revenue = revenue_model.predict(new_data)
                     #st.write(f'Predicted Rating: {predicted_rating[0]}')
                     sum_revenue = predicted_revenue[0] + sum_revenue
         
      
         st.write(f'Predicted Rating: {sum_revenue/(len(revenue["actors"])*len(revenue["actresses"])*len(revenue["directors"])*len(revenue["writers"]))}')

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



