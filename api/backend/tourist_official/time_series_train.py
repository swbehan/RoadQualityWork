import requests
import pandas as pd
from plotly import graph_objects as go
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def get_country_prediction(user_input, merged_df):
    return merged_df

def merging_data(final_1plus_df):

    tourist_num = final_1plus_df
    tourist_num_copy = final_1plus_df.copy()

    min_trips = tourist_num['NumTrips'].min()
    max_trips = tourist_num['NumTrips'].max()

    tourist_num['Tourism St.'] = (tourist_num['NumTrips'] - min_trips) / (max_trips - min_trips)

    tourist_num = pd.DataFrame(final_1plus_df, columns = ['Country', 'Year', 'Tourism St.'])
    tourist_num.sort_values(by = ["Year"])

    unfiltered_predicted_tourist =pd.DataFrame(tourist_num_copy, columns = ["Country", "Year", "NumTrips"])

    return tourist_num, unfiltered_predicted_tourist

def get_lag_columns(country_df, lag = 3):

    country_df = country_df.sort_values('Year').reset_index(drop = True)
    country_df['Covid'] = country_df['Year'].apply(lambda x: 1 if x in [2020, 2021] else 0)
    country_df['Bias'] = 1
    min_year = country_df['Year'].min()
    
    index_country = country_df.index[country_df['Year'].astype(int) == min_year + 3]
    index = index_country[0]

    y_vector = []
    x_matrix = []
    x_list = []
    for i in range(index, len(country_df)): 
        if i - lag < 0:
            continue
        bias = 1 
        country = country_df.iloc[i]["Country"]
        lag_values = [country_df.iloc[i - j]['Tourism St.'] for j in range(1, lag + 1)]
        covid = country_df.iloc[i]['Covid']
        year = country_df.iloc[i]['Year']
        
        x_list = [bias, country, year, covid] + lag_values
        x_matrix.append(x_list)
        y_vector.append(country_df.iloc[i]["Tourism St."])

    x_matrix = pd.DataFrame(x_matrix)
    x_matrix.rename(columns={0: "Bias", 1: "Country", 2:"Year", 3:"Covid", 4:"lag1", 5:"lag2", 6:"lag3"}, inplace=True)


    return x_matrix, y_vector

def fit_regression_(X, y):
    Xt = X.T
    XtX = np.dot(Xt, X)
    XtX_inv = np.linalg.inv(XtX)
    Xt_y = np.dot(Xt, y)
    beta = np.dot(XtX_inv, Xt_y)

    return beta