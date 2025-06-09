import logging
logger = logging.getLogger(__name__)
import streamlit as st
from streamlit_extras.app_logo import add_logo
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
from modules.nav import SideBarLinks
import plotly.express as px
import requests

SideBarLinks()

# add the logo
add_logo("assets/logo.png", height=400)

# set up the page
st.markdown("# Top Tourism Attractions")

countries_list = requests.get("http://web-api:4000/tourism/countrieslist").json()
for i in range(len(countries_list)):
    countries_list[i] = countries_list[i]["Country"]

countries_list = ["Select"] + countries_list
selected_country = st.selectbox("Select Country", countries_list)

if selected_country != "Select":
    st.markdown(f"### Best Tourist Attractions In {selected_country}")

    attractions_list = requests.get(f"http://web-api:4000/tourism/tourismattractions/{selected_country}").json()

    for attraction in attractions_list:
        st.markdown(f" - **{attraction['AttractionName']}:** {attraction['City']}, {attraction['Country']}")