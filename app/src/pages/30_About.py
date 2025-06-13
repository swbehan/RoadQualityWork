import streamlit as st
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# About the Authors ")
left_col, middle_col_one, middle_col_two, right_col = st.columns(4)

with left_col:
    st.image("assets/Sean.jpeg", use_container_width=True)
    st.markdown("**Sean Behan**")
    st.text("I am a rising second year studying Computer Science with a concentration in AI with a minor in Business Administration. A fun fact about me is that I am a triplet!")

with middle_col_one:
    st.image("assets/Aidan.jpeg", use_container_width=True)
    st.markdown("**Aidan Kelly**")
    st.text("I am a rising third year studying Computer Science and Financial Technology. I enjoy watching hockey, and have been playing since I was three!")

with middle_col_two:
    st.image("assets/Gabby.jpeg", use_container_width=True)
    st.markdown("**Gabby Montalvo**")
    st.text("I am a rising second year studying Data Science and Marketing Analytics. I play five instruments, and am a coffee enthusiast working at two coffee shops!")

with right_col:
    st.image("assets/Maria.jpeg", use_container_width=True)
    st.markdown("**Maria Samos Rivas**")
    st.text("I am a rising second year studying Data Science and Finance. Though I was born in Spain, I’ve lived in DC for the last 10 years.")

st.write("# Problem EuroTour Addresses")
st.markdown(
    """
    Despite the vast amount of public data on tourism and road infrastructure within the E.U., 
    there is no unified platform that transforms this information into a meaningful guidance tool 
    for a diverse range of users. 
    - Casual road trippers often struggle to plan efficient/affordable 
    trips due to overly technical datasets on road quality, traffic, and travel costs. 
    - Meanwhile, national officials tasked with promoting tourism and improving infrastructure lack accessible 
    tools to benchmark their country’s performance, predict tourism trends, or assess the effectiveness 
    of public investment in transportation. 
    - Academic researchers face yet another barrier: while they 
    need historical and comparative data for modeling and publication, much of the available information 
    is fragmented or lacks interoperability.
    """
)

# Add a button to return to home page
if st.button("Return to Home", type="primary"):
    st.switch_page("Home.py")
