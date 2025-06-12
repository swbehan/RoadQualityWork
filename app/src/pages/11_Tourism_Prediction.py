import logging

logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests
from plotly import graph_objects as go
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")

# Display the appropriate sidebar links for the role of the logged in user
SideBarLinks()

country = st.session_state["Nationality"]

st.title(f"Tourism Prediction For {country}")

def create_graph(country_data, country):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x= country_data['Year'], 
        y= country_data['NumTrips'], 
        name= f'Tourism Numbers in {country}',
        line= dict(color='royalblue', width=4),
    ))

    fig.add_vline(
        x=2023,  
        line=dict(color='gray', dash='dot'),
        annotation_text='Prediction',
        annotation_position='top right'
)
    fig.update_layout(
        title = f'Predicted Tourism Over the Years in {country}',
        title_x = 0.5, 
        xaxis_title = 'Years',
        yaxis_title = 'Tourism Numbers (Millions)')
    
    return fig


country_values = requests.get(f"http://web-api:4000/official/timeseries/{country}").json()

st.markdown(f"## Number of Tourists In {country}")

for i in range(2023, 2027, 1):
    for country_info in country_values:
        if country_info["TripYear"] == i:
            st.markdown(f"{i}: {country_info['NumTrips']}")

st.plotly_chart(create_graph(pd.DataFrame(country_values), country))