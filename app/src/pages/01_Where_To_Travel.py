import logging
logger = logging.getLogger(__name__)
import pandas as pd
import streamlit as st
from streamlit_extras.app_logo import add_logo
import world_bank_data as wb
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from modules.nav import SideBarLinks

# Call the SideBarLinks from the nav module in the modules directory
SideBarLinks()

st.header('Lost on where to travel in Europe?')
st.subheader('No Worries! Input your preferences below!')

with st.form("traveler_form"):

    costSlider = st.slider("How important is saving money on fuel/travel cost?", 0, 10, 5)
    trafficSlider = st.slider("How much do you value avoiding long travel times/traffic?", 0, 10, 5)
    tourismSlider = st.slider("How important is avoiding high tourims levels?", 0, 10, 5)

    submitted = st.form_submit_button("📤 Submit Research Post", type="primary")





