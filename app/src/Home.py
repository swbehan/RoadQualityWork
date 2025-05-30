##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")
st.title("EuroTour 🌍")
st.write('\n\n')
st.write('### Connecting Journeys, Guiding Policy, Fueling Research')
st.write('\n')
st.write('#### Welcome. Who is logging in today?')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

left_col, middle_col, right_col = st.columns(3)

with left_col:
    if st.button("Act as Jacques Bon-voyage, a European Traveler", 
                 type='primary', 
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'pol_strat_advisor'
        st.session_state['first_name'] = 'John'
        logger.info("Logging in as Political Strategy Advisor Persona")
        st.switch_page('pages/00_Pol_Strat_Home.py')

with middle_col:
    if st.button("Act as Nina Petek, a National Director of Tourism", 
                 type='primary', 
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'usaid_worker'
        st.session_state['first_name'] = 'Mohammad'
        st.switch_page('pages/10_USAID_Worker_Home.py')

with right_col:
    if st.button("Act as Ellie Willems, a European Tourism Researcher", 
                 type='primary', 
                 use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'administrator'
        st.session_state['first_name'] = 'SysAdmin'
        st.switch_page('pages/20_Admin_Home.py')




