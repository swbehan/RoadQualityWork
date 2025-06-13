import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, offical_font


st.set_page_config(layout = 'wide')

SideBarLinks()
style_buttons()

offical_font("Now Researchers Can View Your Graph!", False)
st.success("🥳 Graph Post Successful")
if st.button('Go Home', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/10_Tourist_Offical_Home.py')