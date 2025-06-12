import pandas as pd
import numpy as np

min_trips = 658396 
max_trips = 526338516

def standardize_data(original_data):
    original_data['Tourism St.'] = (original_data['NumTrips'] - min_trips) / (max_trips - min_trips)


def unstandardize_results(st_data):
    st_data["Predicted_Tourism"] = st_data["Predicted_Tourism"] * (max_trips - min_trips) + min_trips



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

def fit_regression(X, y):
    Xt = X.T
    XtX = np.dot(Xt, X)
    XtX_inv = np.linalg.inv(XtX)
    Xt_y = np.dot(Xt, y)
    beta = np.dot(XtX_inv, Xt_y)

    return beta


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

def get_country_prediction(data, weights_row, country, lag=3):
    """
    Predict future tourism values using pre-trained weights
    
    Args:
        data: DataFrame with historical tourism data
        weights_row: Series with weights [Y_Intercept, Covid, Lag_1, Lag_2, Lag_3]
        country: Country name
        lag: Number of lag periods
    """
    try:
        country_df = data[data['Country'] == country].copy()
        
        if country_df.empty:
            raise ValueError(f"No data found for country: {country}")
        
        country_df = country_df.sort_values('Year').reset_index(drop=True)
        
        if len(country_df) < lag + 1:
            raise ValueError(f"Not enough historical data for {country}. Need at least {lag + 1} years.")
        
        country_df['Covid'] = country_df['Year'].apply(lambda x: 1 if x in [2020, 2021] else 0)
        
        last_year = country_df['Year'].max()
        last_tourism_values = country_df['Tourism St.'].tail(lag).values
        
        y_intercept = weights_row['Y_Intercept']
        covid_weight = weights_row['Covid']
        lag_weights = [weights_row[f'Lag_{i}'] for i in range(1, lag + 1)]
        
        predictions = []
        current_lags = last_tourism_values.tolist()
        
        for i in range(3): 
            year = last_year + i + 1
            covid_indicator = 1 if year in [2020, 2021] else 0
            
            prediction = y_intercept + covid_weight * covid_indicator
            for j, lag_weight in enumerate(lag_weights):
                if j < len(current_lags):
                    prediction += lag_weight * current_lags[-(j+1)]
            
            predictions.append({
                'Country': country,
                'Year': year,
                'Predicted_Tourism': prediction
            })
            
            current_lags.append(prediction)
            if len(current_lags) > lag:
                current_lags.pop(0)
        
        final_df = pd.DataFrame(predictions)
        unstandardize_results(final_df)
        
        return final_df
        
    except Exception as e:
        print(f"Error in get_country_prediction: {str(e)}")
        raise