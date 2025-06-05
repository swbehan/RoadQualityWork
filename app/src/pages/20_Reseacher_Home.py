import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Welcome Reseacher, Ellie')
st.write('')
st.write('')
st.write('### What would you like to do today?')
if st.button('Create Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/21_Reseacher_Notes.py')

if st.button('View Existing Posts', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/22_Reseacher_View.py')


