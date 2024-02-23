import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'data_clean_v2.csv')
film_data = pd.read_csv(file_path)

st.header('Popcorn Pulse', divider='red')
st.title('Film Analytics Dashboard')

tab1, tab2, tab3 = st.tabs(["Top Rows of the Dataset", "Distribution of Film Ratings", "Revenue by Genre"])

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
   # Fill NaN values with 0
   film_data['Revenue'] = pd.to_numeric(film_data['Revenue'].replace('[\$,]', '', regex=True), errors='coerce')

   # Group by 'genres' and sum 'Revenue'
   revenue_by_genre = film_data.groupby('genres')['Revenue'].sum().sort_values(ascending=False)

   # Plot the bar chart
   fig, ax = plt.subplots()
   revenue_by_genre.plot(kind='bar', ax=ax, color='salmon')
   ax.set_xlabel('Genres')
   ax.set_ylabel('Total Revenue')
   st.pyplot(fig)