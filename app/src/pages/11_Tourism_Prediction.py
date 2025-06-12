import logging

logger = logging.getLogger(__name__)

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from modules.nav import SideBarLinks
from pages.styling_pages import offical_font


SideBarLinks()


def fetch_historical_data(nationality):
   """
   Fetch historical tourism data from the Trips table
   """
   try:
       url = f"http://web-api:4000/official/trips/{nationality}"
       response = requests.get(url)
      
       if response.status_code == 200:
           data = response.json()
           if data and isinstance(data, list) and len(data) > 0:
               df = pd.DataFrame(data)
               print(f"Historical DataFrame shape: {df.shape}")
               print(f"Historical sample data: {df.head()}")
            
               df = df.rename(columns={'TripYear': 'Year'})
              
               aggregated_df = df.groupby(['Country', 'Year'])['NumTrips'].sum().reset_index()
               aggregated_df['DataType'] = 'Historical'
              
               return aggregated_df
           else:
               return pd.DataFrame()
              
       elif response.status_code == 404:
           return pd.DataFrame()
       else:
           st.error(f"HTTP Error {response.status_code} for historical data: {response.text}")
           return pd.DataFrame()
          
   except Exception as e:
       st.error(f"Error fetching historical data: {str(e)}")
       return pd.DataFrame()


def fetch_prediction_data(nationality):
   """
   Fetch prediction tourism data from the TimeSeriesPredictions table
   """
   try:
       url = f"http://web-api:4000/official/timeseries/{nationality}"
       response = requests.get(url)
      
       if response.status_code == 200:
           data = response.json()
          
           if data and isinstance(data, list) and len(data) > 0:
               if isinstance(data[0], list):
                   df = pd.DataFrame(data, columns=['Country', 'TripYear', 'PredictedTrips'])
                   df = df.rename(columns={'TripYear': 'Year', 'PredictedTrips': 'NumTrips'})
               else:
                   df = pd.DataFrame(data)
                   if 'TripYear' in df.columns:
                       df = df.rename(columns={'TripYear': 'Year'})
                   if 'PredictedTrips' in df.columns:
                       df = df.rename(columns={'PredictedTrips': 'NumTrips'})
              
               df['DataType'] = 'Predicted'
              
               return df
           else:
               return pd.DataFrame()
              
       elif response.status_code == 404:
           return pd.DataFrame()
       else:
           return pd.DataFrame()
          
   except Exception as e:
       return pd.DataFrame()


def fetch_combined_tourism_data(nationality):
   """
   Fetch and combine both historical and prediction data
   """
   historical_df = fetch_historical_data(nationality)
   prediction_df = fetch_prediction_data(nationality)
  
   if not historical_df.empty and not prediction_df.empty:
       combined_df = pd.concat([historical_df, prediction_df], ignore_index=True)
   elif not historical_df.empty:
       combined_df = historical_df
       st.info("Only historical data available no predictions found.")
   elif not prediction_df.empty:
       combined_df = prediction_df
       st.info("Only prediction data available no historical data found.")
   else:
       return None
  
   combined_df = combined_df.sort_values('Year').reset_index(drop=True)
  
   return combined_df


nationality = st.session_state['Nationality']


def create_tourism_graph(df, country):
   """
   Create an interactive tourism graph showing both historical and predicted data with connected lines
   """
   fig = go.Figure()


   historical_data = df[df['DataType'] == 'Historical'] if 'DataType' in df.columns else df[df['Year'] < 2024]
   predicted_data = df[df['DataType'] == 'Predicted'] if 'DataType' in df.columns else df[df['Year'] >= 2024]
  
   if not historical_data.empty:
       fig.add_trace(go.Scatter(
           x=historical_data['Year'],
           y=historical_data['NumTrips'],
           mode='lines+markers',
           name='Historical Data',
           line=dict(color='#2E86AB', width=3),
           marker=dict(size=6, color='#2E86AB'),
           hovertemplate='<b>%{x}</b><br>Trips: %{y:,.0f}<br>Type: Historical<extra></extra>'
       ))
  
   if not predicted_data.empty:
       fig.add_trace(go.Scatter(
           x=predicted_data['Year'],
           y=predicted_data['NumTrips'],
           mode='lines+markers',
           name='Predictions',
           line=dict(color='#A23B72', width=3, dash='dash'),
           marker=dict(size=8, color='#A23B72', symbol='diamond'),
           hovertemplate='<b>%{x}</b><br>Predicted Trips: %{y:,.0f}<br>Type: Prediction<extra></extra>'
       ))
  
   if not historical_data.empty and not predicted_data.empty:
       last_historical_year = historical_data['Year'].max()
       last_historical_trips = historical_data[historical_data['Year'] == last_historical_year]['NumTrips'].iloc[0]
      
       first_predicted_year = predicted_data['Year'].min()
       first_predicted_trips = predicted_data[predicted_data['Year'] == first_predicted_year]['NumTrips'].iloc[0]
      
       fig.add_trace(go.Scatter(
           x=[last_historical_year, first_predicted_year],
           y=[last_historical_trips, first_predicted_trips],
           mode='lines',
           name='Connection',
           line=dict(color='gray', width=2, dash='dot'),
           showlegend=False,
           hoverinfo='skip'
       ))
      
       fig.add_vline(
           x=last_historical_year + 0.5,
           line_dash="dot",
           line_color="lightgray",
           annotation_text="Predictions →",
           annotation_position="top"
       )
  
   fig.update_layout(
       title=f"Historical Data & Predictions for {nationality}",
       xaxis_title="Year",
       yaxis_title="Number of Trips",
       font=dict(size=12),
       plot_bgcolor='white',
       paper_bgcolor='white',
       height=500,
       legend=dict(
           orientation="h",
           yanchor="bottom",
           y=1.02,
           xanchor="right",
           x=1
       )
   )
  
   fig.update_yaxes(tickformat='.0f')
  
   fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
   fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
  
   return fig


def format_number(num):
   """
   Format large numbers for display
   """
   if num >= 1_000_000:
       return f"{num/1_000_000:.1f}M"
   elif num >= 1_000:
       return f"{num/1_000:.1f}K"
   else:
       return f"{num:.0f}"


offical_font("Tourism Analytics Dashboard", False)


with st.spinner("Fetching tourism data and predictions..."):
   tourism_df = fetch_combined_tourism_data(nationality)


   tourism_df['Year'] = pd.to_numeric(tourism_df['Year'], errors='coerce')
   tourism_df['NumTrips'] = pd.to_numeric(tourism_df['NumTrips'], errors='coerce')


   fig = create_tourism_graph(tourism_df, nationality)
   st.plotly_chart(fig, use_container_width=True)
  
   historical_data = tourism_df[tourism_df['DataType'] == 'Historical'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] < 2024]
   predicted_data = tourism_df[tourism_df['DataType'] == 'Predicted'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] >= 2024]
  
   offical_font(f"Data Summary for {nationality}", False)
  
   col1, col2 = st.columns(2)
  
   with col1:
       st.markdown("### Historical Data (2012-2023)")
       if not historical_data.empty:
           hist_avg = historical_data['NumTrips'].mean()
           hist_max = historical_data['NumTrips'].max()
           hist_max_year = historical_data.loc[historical_data['NumTrips'].idxmax(), 'Year']
          
           st.metric("Average Annual Trips", format_number(hist_avg))
           st.metric("Peak Year", f"{int(hist_max_year)}", format_number(hist_max))
  
   with col2:
       st.markdown("### Predictions (2024-2026)")
       if not predicted_data.empty:
           pred_avg = predicted_data['NumTrips'].mean()
           pred_max = predicted_data['NumTrips'].max()
           pred_max_year = predicted_data.loc[predicted_data['NumTrips'].idxmax(), 'Year']
          
           st.metric("Average Predicted Trips", format_number(pred_avg))
           st.metric("Peak Predicted Year", f"{int(pred_max_year)}", format_number(pred_max))
  


   display_df = tourism_df.copy()
   display_df['NumTrips'] = display_df['NumTrips'].apply(lambda x: f"{x:,.0f}")
   display_df = display_df.rename(columns={
       'Year': 'Year',
       'NumTrips': 'Number of Trips',
       'DataType': 'Data Type'
   })
  
   column_order = ['Year','Number of Trips', 'Data Type']
   display_df = display_df[column_order]
  
   st.dataframe(display_df, use_container_width=True)


st.markdown("""
<style>
   .stMetric {
       background-color: #f0f2f6;
       padding: 10px;
       border-radius: 5px;
   }
</style>
""", unsafe_allow_html=True)