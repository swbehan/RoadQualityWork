##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
import requests
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, style_front_image

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
style_buttons() 
style_front_image()

logger.info("Loading the Home page of the app")
st.write('\n\n')
st.write('\n')
st.markdown("""
<style>
.login-welcome {
    border: 2px solid #C1D5C0 !important;
    border-radius: 8px !important;
    padding: 25px !important;
    text-align: center !important;
    background: #FFFFFF !important; 
    margin: 15px 0 !important;
    font-size: 1.3rem !important;
    color: #0891B2 !important;
}
</style>

<div class="login-welcome">
    <strong>Welcome</strong><br>
    Please Login Below
</div>
""", unsafe_allow_html=True)

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

def fetch_users_of_type(user_type):
    """Fetch users of a specific type from API"""
    try:
        response = requests.get(f"http://host.docker.internal:4000/official/usersoftype/{user_type}")
        if response.status_code == 200:
            data = response.json()
            return data 
        else:
            st.error(f"Failed to load {user_type} users: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching {user_type} users: {str(e)}")
        return []

def display_user_buttons(users, user_type, page_path, log_message):
    """Display user buttons for a specific type"""
    if users:
        for user in users:
            user_id = user.get('UserID', 'N/A')
            user_name = user.get('Username', 'No Name')
            nationality = user.get('Nationality', 'No Nation')
            
            if st.button(f"Sign in as {user_name}, a {user_type} from {nationality}",
                       key=f"{user_type.lower()}_{user_id}",
                       type='primary',
                       use_container_width=True):
                st.session_state['authenticated'] = True
                st.session_state['role'] = user_type
                st.session_state['first_name'] = user_name
                st.session_state['AuthorID'] = user_id
                logger.info(log_message)
                st.switch_page(page_path)
    else:
        st.info(f"No {user_type} users available")

def view_users():
    """Main function to display user selection interface"""
    st.title("Select User Login")
    
    left_col, middle_col, right_col = st.columns(3)
    
    # Traveler Column
    with left_col:
        st.image("assets/traveler.jpg", use_container_width=True)
        with st.expander("Sign in as a European Tourist", expanded=False):
            users = fetch_users_of_type("Tourist")
            display_user_buttons(
                users, 
                'Tourist', 
                'pages/00_Traveler_Home.py',
                "Logging in as Traveler Persona"
            )
    
    # Official Column  
    with middle_col:
        st.image("assets/official.jpg", use_container_width=True)
        with st.expander("Sign in as a National Director of Tourism", expanded=False):
            users = fetch_users_of_type("National Official")
            display_user_buttons(
                users,
                'National Official',
                'pages/10_Tourist_Offical_Home.py', 
                "Logging in as National Director of Tourism Persona"
            )
    
    # Researcher Column
    with right_col:
        st.image("assets/researcher.jpg", use_container_width=True)
        with st.expander("Sign in as European Researcher", expanded=False):
            users = fetch_users_of_type("Researcher")
            display_user_buttons(
                users,
                'Researcher',
                'pages/20_Reseacher_Home.py',
                "Logging in as European Researcher Persona"
            )

if __name__ == "__main__":
    view_users()
