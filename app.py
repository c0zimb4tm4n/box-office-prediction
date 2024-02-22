import streamlit as st

st.header('Popcorn Pulse', divider='red')

#Declaring Tabs
tab1, tab2, tab3 = st.tabs(["Box Office Revenue Predictor", "IMDb Movie Ratings Predictor", "Movie Analytics Dashboard"])

#Setting up Tabs
with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)