import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.success("🥳 Post Successful")
if st.button('View Existing Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Reseacher_View.py')