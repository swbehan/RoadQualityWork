import pandas as pd
import numpy as np
from backend.tourist_official.time_series_train import get_lag_columns, fit_regression 

def predict_next_year(beta, X):
    return np.dot(beta, X)

def get_country_years_pred(data, country, lag = 3):

    country_df = data[data['Country'] == country]
    country_df, y = get_lag_columns(country_df, lag = lag)

    lag_cols = [f'lag{i}' for i in range(1, lag + 1)]
    feature_cols = ['Bias', 'Covid'] + lag_cols
    
    X = country_df[feature_cols].values

    beta_tourism = fit_regression(X, y)

    predictions = []
    for index, row in country_df.iterrows():
        year = row['Year']
        X_year = np.array([row[col] for col in feature_cols])
        print(X_year)
        pred_tourism = predict_next_year(beta_tourism, X_year)

        predictions.append({
            'Country': country,
            'Year': year,
            'Actual_Tourism': y[index],
            'Predicted_Tourism': pred_tourism

        })

    all_years_results = pd.DataFrame(predictions)

    return all_years_results

def get_country_prediction(data, country, lag=3):
    country_df = data[data['Country'] == country].copy()
    country_df, y = get_lag_columns(country_df, lag=lag)

    lag_cols = [f'lag{i}' for i in range(1, lag + 1)]
    feature_cols = ['Bias', 'Covid'] + lag_cols

    X = country_df[feature_cols].values

    beta_tourism = fit_regression(X, y)
    print(beta_tourism)
    last_year = country_df['Year'].max()

    last_row = country_df[country_df['Year'] == last_year].iloc[0]
    lag_values = [last_row[f'lag{i}'] for i in range(1, lag + 1)]

    tmp_x = last_row[feature_cols].to_numpy()
    x_old = np.hstack([tmp_x[:2], y[-1], tmp_x[2:4]])
    
    year_list = [last_year + 1]
    country_list = [country]
    pred_list = [predict_next_year(beta_tourism, x_old)]

    for i in range(1, lag):
        year = last_year + i + 1
        
        X_new = np.hstack([x_old[:2], pred_list[i-1], x_old[2:4]])
        pred_tourism = predict_next_year(beta_tourism, X_new)

        year_list.append(year)
        country_list.append(country)
        pred_list.append(pred_tourism)

        x_old = X_new

    predictions = {'Year': year_list,
                   'Country': country_list,
                   'Predicted_Tourism': pred_list}

    return pd.DataFrame(predictions)