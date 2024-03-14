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

def has_crew_worked_before(findata, query):
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
            filtered_data = findata[(findata['genres'] == genre) & (findata['director'] == director)]
            for tconst in filtered_data['tconst'].unique():
                if tconst in tconsts_map.keys():
                    if director not in tconsts_map[tconst]:
                        tconsts_map[tconst].append(director)
                else:
                    tconsts_map[tconst] = [director] 
    return ([key for key, value in tconsts_map.items() if len(value)>=2])

def evaluate_predicted_rating(findata, rating, query):
    def get_max_by_factor(factor_name):
        max_factor_rating = -1
        max_factor_value =""
        for factor in query[factor_name]:
            avg_factor_rating = findata[findata[f'{factor_name}'] == factor]['averageRating'].mean()
            if avg_factor_rating>max_factor_rating:
                max_factor_rating = avg_factor_rating
                max_factor_value = factor
        return (max_factor_value, max_factor_rating)
    results = {}
    for key in query.keys():
        max_val, max_rating = get_max_by_factor(f'{key}')
        if max_val!= "" and max_rating!=-1:
            results[f'{key}'] = [max_val, rating-max_rating, ((rating-max_rating)/max_rating)*100]
    return results



def evaluate_predicted_revenue(findata, rating, query):
    def get_max_by_factor(factor_name):
        max_factor_revenue = -1
        max_factor_value =""
        for factor in query[factor_name]:
            avg_factor_revenue = findata[findata[f'{factor_name}'] == factor]['Revenue_InflationCorrected'].mean()
            if avg_factor_revenue>max_factor_revenue:
                max_factor_revenue = avg_factor_revenue
                max_factor_value = factor
        return (max_factor_value, max_factor_revenue)
    results = {}
    for key in query.keys():
        max_val, max_revenue = get_max_by_factor(f'{key}')
        if max_val!= "" and max_revenue!=-1:
            results[f'{key}'] = [max_val, rating-max_revenue, ((rating-max_revenue)/max_revenue)*100]
    return results
