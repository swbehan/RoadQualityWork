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


def create_tourism_graph(df, df_two, first_country_name, second_country_name):
    fig = go.Figure()

    historical_data = df[df['DataType'] == 'Historical'] if 'DataType' in df.columns else df[df['Year'] < 2024]
    predicted_data = df[df['DataType'] == 'Predicted'] if 'DataType' in df.columns else df[df['Year'] >= 2024]

    second_historical_data = df_two[df_two['DataType'] == 'Historical'] if 'DataType' in df_two.columns else df_two[df_two['Year'] < 2024]
    second_predicted_data = df_two[df_two['DataType'] == 'Predicted'] if 'DataType' in df_two.columns else df_two[df_two['Year'] >= 2024]
    
    #FIRST country
    if not historical_data.empty:
        fig.add_trace(go.Scatter(
            x=historical_data['Year'],
            y=historical_data['NumTrips'],
            mode='lines+markers',
            name=f'{first_country_name} - Historical',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=6, color='#2E86AB'),
            hovertemplate=f'<b>{first_country_name} - %{{x}}</b><br>Trips: %{{y:,.0f}}<br>Type: Historical<extra></extra>'
        ))

    if not predicted_data.empty:
        fig.add_trace(go.Scatter(
            x=predicted_data['Year'],
            y=predicted_data['NumTrips'],
            mode='lines+markers',
            name=f'{first_country_name} - Predictions',
            line=dict(color='#A23B72', width=3, dash='dash'),
            marker=dict(size=8, color='#A23B72', symbol='diamond'),
            hovertemplate=f'<b>{first_country_name} - %{{x}}</b><br>Predicted Trips: %{{y:,.0f}}<br>Type: Prediction<extra></extra>'
        ))

    #SECOND country
    if not second_historical_data.empty:
        fig.add_trace(go.Scatter(
            x=second_historical_data['Year'],
            y=second_historical_data['NumTrips'],
            mode='lines+markers',
            name=f'{second_country_name} - Historical',
            line=dict(color='#F18F01', width=3),
            marker=dict(size=6, color='#F18F01'),
            hovertemplate=f'<b>{second_country_name} - %{{x}}</b><br>Trips: %{{y:,.0f}}<br>Type: Historical<extra></extra>'
        ))

    if not second_predicted_data.empty:
        fig.add_trace(go.Scatter(
            x=second_predicted_data['Year'],
            y=second_predicted_data['NumTrips'],
            mode='lines+markers',
            name=f'{second_country_name} - Predictions',
            line=dict(color='#C73E1D', width=3, dash='dash'),
            marker=dict(size=8, color='#C73E1D', symbol='diamond'),
            hovertemplate=f'<b>{second_country_name} - %{{x}}</b><br>Predicted Trips: %{{y:,.0f}}<br>Type: Prediction<extra></extra>'
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
            line=dict(color='gray', width=2, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))

    if not second_historical_data.empty and not second_predicted_data.empty:
        last_historical_year_second = second_historical_data['Year'].max()
        last_historical_trips_second = second_historical_data[second_historical_data['Year'] == last_historical_year_second]['NumTrips'].iloc[0]

        first_predicted_year_second = second_predicted_data['Year'].min()
        first_predicted_trips_second = second_predicted_data[second_predicted_data['Year'] == first_predicted_year_second]['NumTrips'].iloc[0]
        
        fig.add_trace(go.Scatter(
            x=[last_historical_year_second, first_predicted_year_second],
            y=[last_historical_trips_second, first_predicted_trips_second],
            mode='lines',
            line=dict(color='gray', width=2, dash='dot'),
            showlegend=False,
            hoverinfo='skip'
        ))

    if not historical_data.empty:
        last_historical_year = historical_data['Year'].max()
        fig.add_vline(
            x=last_historical_year + 0.5,
            line_dash="dot",
            line_color="lightgray",
            annotation_text="Predictions →",
            annotation_position="top"
        )
    
    fig.update_layout(
        title=f"Tourism Comparison: {first_country_name} vs {second_country_name}",
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

  
   historical_data = tourism_df[tourism_df['DataType'] == 'Historical'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] < 2024]
   predicted_data = tourism_df[tourism_df['DataType'] == 'Predicted'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] >= 2024]
   
   countries_list = requests.get("http://web-api:4000/tourism/countrieslist").json()
   for i in range(len(countries_list)):
        countries_list[i] = countries_list[i]["Country"]

   countries_list = ["Select"] + countries_list
   selected_country = st.selectbox(f"Select Country to Compare {nationality} Against", countries_list)
   
if selected_country != "Select":
    second_country_data = fetch_combined_tourism_data(selected_country)
    second_country_data['Year'] = pd.to_numeric(second_country_data['Year'], errors='coerce')
    second_country_data['NumTrips'] = pd.to_numeric(second_country_data['NumTrips'], errors='coerce')
    
    fig = create_tourism_graph(tourism_df, second_country_data, nationality, selected_country)
    st.plotly_chart(fig, use_container_width=True)
else:
    fig = go.Figure()
    
    historical_data = tourism_df[tourism_df['DataType'] == 'Historical'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] < 2024]
    predicted_data = tourism_df[tourism_df['DataType'] == 'Predicted'] if 'DataType' in tourism_df.columns else tourism_df[tourism_df['Year'] >= 2024]
    
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
        title=f"Tourism Data for {nationality}",
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
    
    st.plotly_chart(fig, use_container_width=True)

# Data Summary Section
if selected_country != "Select":
    offical_font(f"Comparative Analysis: {nationality} vs {selected_country}", False)
    
    first_historical = historical_data
    first_predicted = predicted_data
    
    second_historical = second_country_data[second_country_data['DataType'] == 'Historical'] if 'DataType' in second_country_data.columns else second_country_data[second_country_data['Year'] < 2024]
    second_predicted = second_country_data[second_country_data['DataType'] == 'Predicted'] if 'DataType' in second_country_data.columns else second_country_data[second_country_data['Year'] >= 2024]

    st.markdown("### Historical Data Comparison (2012-2023)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{nationality}**")
        if not first_historical.empty:
            hist_avg_1 = first_historical['NumTrips'].mean()
            hist_max_1 = first_historical['NumTrips'].max()
            hist_max_year_1 = first_historical.loc[first_historical['NumTrips'].idxmax(), 'Year']
            hist_total_1 = first_historical['NumTrips'].sum()
            
            st.metric("Average Annual Trips", format_number(hist_avg_1))
            st.metric("Peak Year", f"{int(hist_max_year_1)}", format_number(hist_max_1))
            st.metric("Total Historical Trips", format_number(hist_total_1))
        else:
            st.info("No historical data available")
    
    with col2:
        st.markdown(f"**{selected_country}**")
        if not second_historical.empty:
            hist_avg_2 = second_historical['NumTrips'].mean()
            hist_max_2 = second_historical['NumTrips'].max()
            hist_max_year_2 = second_historical.loc[second_historical['NumTrips'].idxmax(), 'Year']
            hist_total_2 = second_historical['NumTrips'].sum()
            
            st.metric("Average Annual Trips", format_number(hist_avg_2))
            st.metric("Peak Year", f"{int(hist_max_year_2)}", format_number(hist_max_2))
            st.metric("Total Historical Trips", format_number(hist_total_2))
        else:
            st.info("No historical data available")
    
    with col3:
        st.markdown("**Comparison**")
        if hist_avg_1 > hist_avg_2:
            st.success(f"🏆 {nationality} leads in average trips")
        else:
            st.success(f"🏆 {selected_country} leads in average trips")
    
    st.markdown("### Predictions Comparison (2024-2026)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"**{nationality}**")
        if not first_predicted.empty:
            pred_avg_1 = first_predicted['NumTrips'].mean()
            pred_max_1 = first_predicted['NumTrips'].max()
            pred_max_year_1 = first_predicted.loc[first_predicted['NumTrips'].idxmax(), 'Year']
            pred_total_1 = first_predicted['NumTrips'].sum()
            
            st.metric("Average Predicted Trips", format_number(pred_avg_1))
            st.metric("Peak Predicted Year", f"{int(pred_max_year_1)}", format_number(pred_max_1))
            st.metric("Total Predicted Trips", format_number(pred_total_1))
        else:
            st.info("No prediction data available")
    
    with col2:
        st.markdown(f"**{selected_country}**")
        if not second_predicted.empty:
            pred_avg_2 = second_predicted['NumTrips'].mean()
            pred_max_2 = second_predicted['NumTrips'].max()
            pred_max_year_2 = second_predicted.loc[second_predicted['NumTrips'].idxmax(), 'Year']
            pred_total_2 = second_predicted['NumTrips'].sum()
            
            st.metric("Average Predicted Trips", format_number(pred_avg_2))
            st.metric("Peak Predicted Year", f"{int(pred_max_year_2)}", format_number(pred_max_2))
            st.metric("Total Predicted Trips", format_number(pred_total_2))
        else:
            st.info("No prediction data available")
    
    with col3:
        st.markdown("**Comparison**")
        if pred_avg_1 > pred_avg_2:
            st.success(f"🏆 {nationality} predicted to lead")
        else:
            st.success(f"🏆 {selected_country} predicted to lead")

if selected_country != "Select":
    st.markdown("---")
    st.markdown("### Save Graph Data")
    
    with st.form("graph_params_form"):
        comparison_name = st.text_input("Comparison Name")
        submitted = st.form_submit_button("Save Graph Parameters")
        
        if submitted and comparison_name:
            graph_params = {
                'OfficialID': st.session_state['AuthorID'],
                'NationalityValues': tourism_df.to_json(orient='records'),
                'SelectedCountryValues': second_country_data.to_json(orient='records'),
                'NationalityName': nationality,
                'SelectedCountryName': selected_country,
                'ComparisonName': comparison_name,
            }
            
            try:
                response = requests.post(
                    "http://web-api:4000/official/graph",
                    json=graph_params
                )

                if response.status_code == 201:
                    st.success("✅ Graph Posted!")
                    st.switch_page("pages/13_Official_Success_Page.py")
                else:
                    st.error(f"API returned non-success status: {response.status_code}")
                    st.error(f"Raw response: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection error: {str(e)}")