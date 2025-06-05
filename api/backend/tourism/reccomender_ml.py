import requests
import json
import requests
import pandas as pd
from plotly import graph_objects as go
import plotly.graph_objects as go
import numpy as np

def standardize_merged(df_merged):
    fuel = df_merged[["Fuel Score"]].astype(float)
    Fuel_standardize = (fuel -1) / (7-1)
    density = df_merged[["Density Score"]].astype(float)
    Density_standardize = (density -1) / (7-1)
    df_merged["Fuel Score St."] = Fuel_standardize
    df_merged["Density Score St."] = Density_standardize
    df_merged_standardized = pd.DataFrame(df_merged, columns = ["Country", "Year", "Fuel Score St.", "Density Score St."])
    df_merged_standardized['Year'] = df_merged_standardized['Year'].astype(int) 
    df_merged_standardized.loc[df_merged_standardized['Country'] == 'Slovak Republic', 'Country'] = 'Slovakia'  
    fuel_density_2019 = df_merged_standardized[df_merged_standardized['Year'] == 2019]

    return fuel_density_2019


def standardize_trips(final_1plus_df):
    trips_2019 = final_1plus_df[final_1plus_df['Year'] == 2019]
    trips_2019 = trips_2019[~trips_2019['Country'].isin([
        'European Union - 27 countries (from 2020)',
        'Albania',
        'Switzerland',
        'North Macedonia'
    ])]

    min_trips = trips_2019['NumTrips'].min()
    max_trips = trips_2019['NumTrips'].max()

    trips_2019['Tourism St.'] = (trips_2019['NumTrips'] - min_trips) / (max_trips - min_trips)

    trips_2019.drop(columns = ['NumTrips', 'Duration'])
    return trips_2019

def recommender_data(fuel_density_2019, trips_2019):
    recommender_data = pd.merge(fuel_density_2019, trips_2019, on = ['Country', 'Year'])

    recommender_data = pd.DataFrame(recommender_data, columns = ['Country', 'Year', 'Fuel Score St.', 'Density Score St.', 'Tourism St.'])
    return recommender_data

def normalize_user_input(user_input):
    """
    Takes in user preferences on a 0-10 scale for:
    - fuel: importance on saving fuel prices
    - traffic: importance avoiding traffic
    - tourism: importance of avoiding high-tourism countries

    Returns: a normalized array on a 0-1 scale
    """
    max_scale = 10
    weights = np.array([
        user_input['fuel_price'] / max_scale,
        user_input['traffic_time'] / max_scale,
        user_input['tourism_num'] / max_scale
    ])
    return weights

def compute_cosine_similarities(user_vector, country_vector):
    """
    Gets the cosine similarity between the user input and each country's vector.

    Returns: similarity score (float)
    """    
    dot_product = np.dot(user_vector, country_vector)
    user_norm = np.linalg.norm(user_vector)
    country_norm = np.linalg.norm(country_vector)

    # Prevent division by zero
    if user_norm == 0 or country_norm == 0:
        return 0

    return dot_product / (user_norm * country_norm)


def get_top_5_recommendations(user_input, recommender_data):
    """Recommends top 5 countries closest to user preferences based on cosine similarity."""

    user_vector = normalize_user_input(user_input)

    similarities = []

    for index, row in recommender_data.iterrows():
        country_vector = np.array([
            row["Fuel Score St."], 
            row["Density Score St."], 
            row["Tourism St."]
        ])

        similarity = compute_cosine_similarities(user_vector, country_vector)
        similarities.append((row["Country"], similarity))

    similarity_df = pd.DataFrame(similarities, columns=["Country", "Similarity"])
    top_5 = similarity_df.sort_values("Similarity", ascending=False).head(5)

    return top_5

