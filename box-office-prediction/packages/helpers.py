import streamlit as st
import pandas as pd

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

def predict_rating(inputs, runtime_minutes, genre, ratings_model):
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
            
    
    return sum_rating/(len(inputs["actors"])*len(inputs["actresses"])*len(inputs["directors"])*len(inputs["writers"]))

def predict_revenue(revenue, runtime_minutes, genre, revenue_model, predicted_rating):
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
                        'isAdult': 0,
                        'averageRating': predicted_rating
                    }])
                    predicted_revenue = revenue_model.predict(new_data)
                    #st.write(f'Predicted Rating: {predicted_rating[0]}')
                    sum_revenue = predicted_revenue[0] + sum_revenue
         
      
    return sum_revenue/(len(revenue["actors"])*len(revenue["actresses"])*len(revenue["directors"])*len(revenue["writers"]))

