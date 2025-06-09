import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()
style_buttons()

st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .official-hospitality {{
        font-family: 'Lato', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        color: #2a4365 !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 35px 0 50px 0 !important;
    }}
    
    .official-hospitality::before {{
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100px !important;
        height: 4px !important;
        background: linear-gradient(90deg, #3182ce, #63b3ed) !important;
        border-radius: 2px !important;
    }}
    
    .official-hospitality .name {{
        color: #3182ce !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.9em !important;
    }}
            
    .flag-accent {{
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
        height: 6px !important;
        width: 150px !important;
        margin: 15px auto !important;
        border-radius: 3px !important;
    }}
    </style>
    
    <div class="official-hospitality">
        Welcome National Tourist Director, <span class="name">{st.session_state['first_name']}</span>.
        <div class="flag-accent"></div>
    </div>
    """, unsafe_allow_html=True)

st.write('')
st.markdown("""
<style>
.welcome-collage {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    grid-template-rows: 200px 200px;
    gap: 10px;
    border-radius: 15px;
    overflow: hidden;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.collage-item {
    background-size: cover;
    background-position: center;
    position: relative;
    transition: transform 0.3s ease;
}

.collage-item:hover {
    transform: scale(1.05);
    z-index: 2;
}

.collage-main {
    grid-row: 1 / 3;
    background-image: url('https://images.unsplash.com/photo-1467269204594-9661b134dd2b?w=600');
}

.collage-top-right {
    background-image: url('https://www.insightvacations.com/wp-content/uploads/2024/01/caleb-miller-0Bs3et8FYyg-unsplash.jpg');
}

.collage-bottom-right {
    background-image: url('https://cms.inspirato.com/ImageGen.ashx?image=%2Fmedia%2F5682444%2FLondon_Dest_16531610X.jpg&width=1081.5');
}
            
.collage-bottom {
    background-image: url('https://www.planetware.com/wpimages/2020/02/france-in-pictures-beautiful-places-to-photograph-eiffel-tower.jpg');
}
            
.collage-bottom-left {
    background-image: url('https://media.cnn.com/api/v1/images/stellar/prod/130928072317-01-copenhagen-restricted.jpg?q=w_4503,h_3001,x_0,y_0,c_fill');
}

.image-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0,0,0,0.7));
    color: white;
    padding: 1rem;
    font-weight: 600;
}
</style>

<div class="welcome-collage">
    <div class="collage-item collage-main">
        <div class="image-overlay">Belgium</div>
    </div>
    <div class="collage-item collage-top-right">
        <div class="image-overlay">Italy</div>
    </div>
    <div class="collage-item collage-bottom-right">
        <div class="image-overlay">United Kingdom</div>
    </div>
    <div class="collage-item collage-bottom">
        <div class="image-overlay">France</div>
    </div>
    <div class="collage-item collage-bottom-left">
        <div class="image-overlay">Denmark</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
    <link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;600;700&display=swap" rel="stylesheet">
    
    <style>
    .official-hospitality {{
        font-family: 'Lato', sans-serif !important;
        font-size: 2.4rem !important;
        font-weight: 600 !important;
        color: #2a4365 !important;
        text-align: center !important;
        margin: 0 !important;
        line-height: 1.2 !important;
        position: relative !important;
        padding: 35px 0 50px 0 !important;
    }}
    
    .official-hospitality::before {{
        content: '' !important;
        position: absolute !important;
        top: 10px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100px !important;
        height: 4px !important;
        background: linear-gradient(90deg, #3182ce, #63b3ed) !important;
        border-radius: 2px !important;
    }}
    
    .official-hospitality .name {{
        color: #3182ce !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.9em !important;
    }}
            
    .flag-accent {{
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1) !important;
        height: 6px !important;
        width: 150px !important;
        margin: 15px auto !important;
        border-radius: 3px !important;
    }}
    </style>
    
    <div class="official-hospitality">
        What would you like to do today?
        <div class="flag-accent"></div>
    </div>
    """, unsafe_allow_html=True)

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
  