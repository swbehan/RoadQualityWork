import logging
import streamlit as st
import requests
import pandas as pd
import json
from modules.nav import SideBarLinks
from pages.styling_pages import style_buttons, researcher_font
from pages.Tourism_Prediction import create_tourism_graph

logger = logging.getLogger(__name__)

SideBarLinks()
style_buttons()
researcher_font("View Graphs From Officials", False)

def fetch_graphs_from_database():
    """Fetch all graph data from the database"""
    try:
        response = requests.get("http://web-api:4000/official/graph")
        
        if response.status_code == 200:
            data = response.json()
            
            if isinstance(data, dict) and 'posts' in data:
                return data['posts']
            elif isinstance(data, list):
                return data 
            else:
                st.error(f"Unexpected API response format: {type(data)}")
                return []
        else:
            st.error(f"Error fetching graphs: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return []

def display_graphs(graphs):
    """Display graphs in Streamlit"""
    if graphs:
        search_term = st.text_input("🔍 Search graphs", placeholder="Search by comparison name, country, or official name...")
        
        if search_term:
            filtered_graphs = []
            search_lower = search_term.lower()
            
            for graph in graphs:
                graph_id = str(graph.get('GraphID', '')).lower()
                comparison_name = str(graph.get('ComparisonName', '')).lower()
                nationality_name = str(graph.get('NationalityName', '')).lower()
                selected_country_name = str(graph.get('SelectedCountryName', '')).lower()
                official_name = str(graph.get('OfficialName', '')).lower()
                created_at = graph.get('GraphDate', 'Unknown Date')
                
                if (search_lower in comparison_name or
                    search_lower in nationality_name or
                    search_lower in selected_country_name or
                    search_lower in official_name):
                    filtered_graphs.append(graph)
            
            graphs = filtered_graphs
            
            if not graphs:
                st.warning(f"No graphs found matching '{search_term}'")
                return
        
        st.write(f"**Showing {len(graphs)} graph(s)**")
        st.divider()
        
        for i, graph in enumerate(graphs):
            comparison_name = graph.get('ComparisonName', 'Untitled Comparison')
            nationality_name = graph.get('NationalityName', 'Unknown')
            selected_country_name = graph.get('SelectedCountryName', 'Unknown')
            official_name = graph.get('OfficialName', 'Unknown Official')
            created_at = graph.get('GraphDate', 'Unknown Date')
            
            with st.expander(f"{comparison_name} - by {official_name}", expanded=False):
                
                col1, col2, col3 = st.columns(3 )
                with col1:
                    st.write(f"**Countries:** {nationality_name} vs {selected_country_name}")
                with col2:
                    st.write(f"**Created by:** {official_name}")
                with col3:
                    st.write(f"**Date:** {created_at}")
                
                st.divider()
                
                try:
                    nationality_data = json.loads(graph.get('NationalityValues', '[]'))
                    selected_country_data = json.loads(graph.get('SelectedCountryValues', '[]'))
                    
                    df1 = pd.DataFrame(nationality_data)
                    df2 = pd.DataFrame(selected_country_data)
                    
                    if not df1.empty and not df2.empty:
                        fig = create_tourism_graph(
                            df1, 
                            df2, 
                            nationality_name, 
                            selected_country_name
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)

                        with st.form(f"research_form_{i}"):
                            title = st.text_input("Input Title to Post Here")
                            notes = st.text_area(
                                "Input Notes Here",
                                placeholder="Enter your research notes, thoughts, or queries here...",
                                height=150,
                                key=f"notes_input_{i}" 
                            )
                            
                            if notes:
                                st.caption(f"Character count: {len(notes)}")
                            
                            st.divider()
                            submitted = st.form_submit_button("📤 Submit Post", type="primary")
                            
                            if submitted:
                                if title and notes:
                                    post_data = {
                                        "Title": title,
                                        "Research": notes,
                                        "AuthorID": st.session_state["AuthorID"],
                                        "GraphTitle": comparison_name,
                                        "GraphAuthor": official_name
                                    }
                                    
                                    try:
                                        response = requests.post(
                                            "http://web-api:4000/researcher/posts",
                                            json=post_data
                                        )

                                        if response.status_code == 201:
                                            st.switch_page("pages/23_Success_Page.py")
                                        else:
                                            st.error(f"Error: {response.json()['error']}")
                                            
                                    except Exception as e:
                                        st.error(f"Connection error: {str(e)}")
                                else:
                                    st.error("Please fill in Title and Notes!")
                    else:
                        st.error("Error: Empty data for this graph")
                        
                except json.JSONDecodeError as e:
                    st.error(f"Error parsing graph data: {str(e)}")
                except Exception as e:
                    st.error(f"Error creating graph: {str(e)}")
    
    else:
        st.info("Graphs will appear here once officials create graphs.")

try:
    with st.spinner("Loading graphs from database..."):
        graphs_data = fetch_graphs_from_database()
        display_graphs(graphs_data)
        
except Exception as e:
    st.error(f"Application error: {str(e)}")
    logger.error(f"Error in graph viewer: {str(e)}")


