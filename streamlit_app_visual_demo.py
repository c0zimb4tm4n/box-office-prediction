import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'data_clean_v2.csv')
film_data = pd.read_csv(file_path)

st.header('Popcorn Pulse', divider='red')
st.title('Film Analytics Dashboard')

tab1, tab2, tab3, tab4, tab5 = st.tabs(["Top Rows of the Dataset", "Distribution of Film Ratings",
                                        "Revenue by Genre", "Revenue vs. Average Rating", "Average Revenue"])
tab6, tab7, tab8, tab9, tab10 = st.tabs(["Average Rating by Genres","Way of presenting only one Genre's avg rating",
                                          "Runtime vs. Average Rating", "Average Revenue by Actor", "Average Revenue by Actress"])
tab11, tab12, tab13, tab14 = st.tabs(["Average Revenue by Director", "Average Rating by Director",
                                      "Number of Films by Genre", "Distribution of Film Runtime"])
tab15, tab16, tab17, tab18 = st.tabs(["Box Plot: Rating by Genre", "Pair Plot for Avg Rating, Runtime and Revenue",
                                      "Correlation Matrix for Avg Rating, Runtime and Revenue", "3D Scatter Plot: Runtime, Rating, and Revenue"])

with tab1:
   st.header('Top Rows of the Dataset')
   st.dataframe(film_data.head())

with tab2:
   st.header('Distribution of Film Ratings')
   fig, ax = plt.subplots()
   ax.hist(film_data['averageRating'], bins=20, color='skyblue', edgecolor='black')
   ax.set_xlabel('averageRating')
   ax.set_ylabel('Frequency')
   st.pyplot(fig)
   

with tab3:
   st.header('Revenue by Genre')
   film_data['Revenue'] = pd.to_numeric(film_data['Revenue'].replace('[\\$,]', '', regex=True), errors='coerce')
   revenue_by_genre = film_data.groupby('genres')['Revenue'].sum().sort_values(ascending=False)

   fig, ax = plt.subplots()
   revenue_by_genre.plot(kind='bar', ax=ax, color='salmon')
   ax.set_xlabel('Genres')
   ax.set_ylabel('Total Revenue')
   st.pyplot(fig)

with tab4:
   fig, ax = plt.subplots()
   ax.scatter(film_data['averageRating'], film_data['Revenue'], alpha=0.5)
   ax.set_xlabel('Average Rating')
   ax.set_ylabel('Revenue')
   ax.set_title('Revenue vs. Average Rating')
   st.pyplot(fig)

with tab5:
   average_revenue_by_genre = film_data.groupby('genres')['Revenue'].mean().sort_values(ascending=False)
   fig, ax = plt.subplots()
   average_revenue_by_genre.plot(kind='bar', color='lightgreen', ax=ax)
   ax.set_xlabel('Genre')
   ax.set_ylabel('Average Revenue')
   st.pyplot(fig)

with tab6:
   genres = film_data['genres'].unique()
   fig, axs = plt.subplots(len(genres), figsize=(10, len(genres)*5))
   for i, genre in enumerate(genres):
      genre_data = film_data[film_data['genres'] == genre]
      axs[i].hist(genre_data['averageRating'], bins=20, color='plum', edgecolor='black')
      axs[i].set_title(f'Rating Distribution for {genre}')
      axs[i].set_xlabel('Rating')
      axs[i].set_ylabel('Frequency')
   st.pyplot(fig)

with tab7:
   target_genre = 'Documentary'
   genre_data = film_data[film_data['genres'] == target_genre]
   fig, ax = plt.subplots(figsize=(10, 6))
   ax.hist(genre_data['averageRating'], bins=20, color='plum', edgecolor='black')
   ax.set_title(f'Rating Distribution for {target_genre}')
   ax.set_xlabel('Rating')
   ax.set_ylabel('Frequency')
   st.pyplot(fig)

with tab8:
   fig, ax = plt.subplots()
   ax.scatter(film_data['runtimeMinutes'], film_data['averageRating'], alpha=0.5, color='teal')
   ax.set_xlabel('Runtime (minutes)')
   ax.set_ylabel('Average Rating')
   ax.set_title('Runtime vs. Average Rating')
   st.pyplot(fig)

with tab9:
   revenue_by_actor = film_data.groupby('actor')['Revenue'].mean().sort_values(ascending=False).head(10) # Limiting to top 10 for readability
   fig, ax = plt.subplots()
   revenue_by_actor.plot(kind='bar', color='coral', ax=ax)
   ax.set_xlabel('Actor')
   ax.set_ylabel('Average Revenue')
   st.pyplot(fig)

with tab10:
   revenue_by_actress = film_data.groupby('actress')['Revenue'].mean().sort_values(ascending=False).head(10) # Limiting to top 10 for readability
   fig, ax = plt.subplots()
   revenue_by_actress.plot(kind='bar', color='coral', ax=ax)
   ax.set_xlabel('Actress')
   ax.set_ylabel('Average Revenue')
   st.pyplot(fig)

with tab11:
   revenue_by_director = film_data.groupby('director')['Revenue'].mean().sort_values(ascending=False).head(10) # Limiting to top 10 for readability
   fig, ax = plt.subplots()
   revenue_by_director.plot(kind='bar', color='coral', ax=ax)
   ax.set_xlabel('Director')
   ax.set_ylabel('Average Revenue')
   st.pyplot(fig)

with tab12:
   average_rating_by_director = film_data.groupby('director')['averageRating'].mean().sort_values(ascending=False).head(10)  # Limiting to top 10 for readability
   fig, ax = plt.subplots()
   average_rating_by_director.plot(kind='bar', color='skyblue', edgecolor='black')
   ax.set_xlabel('Director')
   ax.set_ylabel('Average Rating')
   ax.set_title('Average Rating by Director')
   st.pyplot(fig)

with tab13:
   films_by_genre = film_data['genres'].value_counts()
   fig, ax = plt.subplots()
   films_by_genre.plot(kind='bar', ax=ax, color='gold')
   ax.set_xlabel('Genres')
   ax.set_ylabel('Number of Films')
   st.pyplot(fig)

with tab14:
   fig, ax = plt.subplots()
   ax.hist(film_data['runtimeMinutes'], bins=20, color='lightblue', edgecolor='black')
   ax.set_xlabel('Runtime (minutes)')
   ax.set_ylabel('Frequency')
   ax.set_title('Distribution of Film Runtimes')
   st.pyplot(fig)

with tab15:
   fig, ax = plt.subplots(figsize=(12, 8))
   sns.boxplot(x='genres', y='averageRating', data=film_data, ax=ax)
   ax.set_xticks(ax.get_xticks())
   ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
   ax.set_title('Box Plot: Rating by Genre')
   st.pyplot(fig)

with tab16:
   selected_variables = ['averageRating', 'runtimeMinutes', 'Revenue']
   pair_plot_data = film_data[selected_variables]
   pairplot = sns.pairplot(pair_plot_data)
   st.pyplot(pairplot.fig)

with tab17:
   selected_variables = ['averageRating', 'runtimeMinutes', 'Revenue']
   correlation_matrix = film_data[selected_variables].corr()
   fig, ax = plt.subplots()
   sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
   ax.set_title('Correlation Matrix for Avg Rating, Runtime and Revenue')
   st.pyplot(fig)

with tab18:
   fig = plt.figure(figsize=(10, 8))
   ax = fig.add_subplot(111, projection='3d')
   ax.scatter(film_data['runtimeMinutes'], film_data['averageRating'], film_data['Revenue'], c='coral', marker='o', alpha=0.5)
   ax.set_xlabel('Runtime (minutes)')
   ax.set_ylabel('Average Rating')
   ax.set_zlabel('Revenue')
   ax.view_init(elev=20, azim=-45)
   ax.set_title('3D Scatter Plot: Runtime, Rating, and Revenue')
   ax.zaxis.labelpad = -2
   st.pyplot(fig)