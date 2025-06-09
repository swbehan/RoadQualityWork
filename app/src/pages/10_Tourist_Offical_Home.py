import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, collage_form, offical_font

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
style_buttons()
offical_font(st.session_state['first_name'], True)
st.write('')
collage_form('https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=600',
             'https://www.insightvacations.com/wp-content/uploads/2024/01/caleb-miller-0Bs3et8FYyg-unsplash.jpg',
             'https://cms.inspirato.com/ImageGen.ashx?image=%2Fmedia%2F5682444%2FLondon_Dest_16531610X.jpg&width=1081.5',
             'https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg',
             'https://media.cnn.com/api/v1/images/stellar/prod/130928072317-01-copenhagen-restricted.jpg?q=w_4503,h_3001,x_0,y_0,c_fill',
             'Belgium',
             'Italy',
             'United Kingdom',
             'France',
             'Denmark')

offical_font("What would you like to do today?", False)
if st.button('Predict Value Based on Regression Model', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/11_Tourism_Prediction.py')

if st.button('View the Simple API Demo', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/12_API_Test.py')

if st.button("View Classification Demo",
             type='primary',
             use_container_width=True):
  st.switch_page('pages/13_Classification.py')
  