import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
from pages.styling_pages import offical_font
import pandas as pd

SideBarLinks()
def tourism_official_data_tables():
    offical_font("Tourism Infrastructure Analytics", False)
    BASE_URL = "http://host.docker.internal:4000/offical"
    tables = {
        "Merged Data": {
            "endpoint": "/get_merged_data",
            "description": """This dataset integrates road infrastructure spending, GDP, 
            road quality scores, and tourism trip statistics by country and year to examine the correlation 
            between government road investment, infrastructure quality, and tourism performance. These values
            reveal each country's road spending as a percentage of GDP, combined with actual road quality 
            measurements, influences tourism patterns including total trip volumes and the variety of trip duration preferences."""
        },
        "Road Quality": {
            "endpoint": "/roadquality",
            "description": """This dataset tracks road infrastructure quality scores for different countries
              across multiple years, providing a standardized assessment of each nation's road network condition. 
              The quality scores enable year over year comparisons of road infrastructure improvements or deterioration 
              within countries and benchmarking across different nations."""
        },
        "Tourism Prioritization": {
            "endpoint": "/tourismprioritization",
            "description": """This dataset measures government tourism prioritization scores by country and year, 
            indicating how much emphasis each nation places on developing and promoting its tourism sector. 
            The scoring system allows for tracking changes in tourism policy focus over time within countries 
            and comparing tourism investment priorities across different nations."""
        },
        "Road Spending": {
            "endpoint": "/roadspending",
            "description": """This dataset tracks government road infrastructure spending by country and year, 
            capturing both absolute spending amounts and each nation's GDP to calculate road investment as 
            a percentage of economic output. The data enables analysis of infrastructure investment trends 
            over time within countries and allows for meaningful comparisons of road spending priorities 
            across nations regardless of economic size."""
        },
        "Trips": {
            "endpoint": "/trips",
            "description": """This dataset records tourism trip volumes by country, year, and duration category, 
            breaking down the total number of trips into different length classifications such as short, medium, 
            and long stays. The data structure allows for analysis of tourism patterns and preferences, showing 
            not just overall trip volumes but also how travelers' duration choices vary across countries and change over time"""
        }
    }
    
    def fetch_data(endpoint):
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"API Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return None, f"Connection Error: {str(e)}"
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    tab_names = list(tables.keys())
    tabs = st.tabs([f"{name}" for name in tab_names])
    
    for i, (table_name, table_info) in enumerate(tables.items()):
        with tabs[i]:
            st.subheader(f"{table_name}")
            st.markdown(f"*{table_info['description']}*")
            with st.spinner(f"Loading {table_name} data..."):
                data, error = fetch_data(table_info['endpoint'])
                if error:
                    st.error(f"Failed to load data: {error}")
                elif data:
                    try:
                        df = pd.DataFrame(data)
                        if not df.empty:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if 'Country' in df.columns:
                                    available_countries = sorted(df['Country'].unique())
                                    selected_countries = st.multiselect(
                                        "Select Countries:",
                                        options=available_countries,
                                        default=[],
                                        key=f"countries_{table_name}"
                                    )
                                else:
                                    selected_countries = []
                            
                            with col2:
                                year_columns = [col for col in df.columns if 'year' in col.lower() or 'Year' in col]
                                if year_columns:
                                    year_column = year_columns[0]
                                    available_years = sorted(df[year_column].unique())
                                    selected_years = st.multiselect(
                                        "Select Years:",
                                        options=available_years,
                                        default=[],
                                        key=f"years_{table_name}"
                                    )
                                else:
                                    selected_years = []
                                    year_column = None
                            
                            filtered_df = df.copy()
                            if selected_countries and 'Country' in df.columns:
                                filtered_df = filtered_df[filtered_df['Country'].isin(selected_countries)]
                            if selected_years and year_column:
                                filtered_df = filtered_df[filtered_df[year_column].isin(selected_years)]
                            
                            st.dataframe(
                                filtered_df,
                                use_container_width=True,
                                height=400
                            )
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Records", len(filtered_df))
                            with col2:
                                st.metric("Columns", len(filtered_df.columns))
                            with col3:
                                if 'Country' in filtered_df.columns:
                                    unique_countries = filtered_df['Country'].nunique() if 'Country' in filtered_df.columns else 0
                                    st.metric("Countries", unique_countries)
                                else:
                                    st.metric("Data Points", filtered_df.size)
                            st.markdown("---")
                            csv = filtered_df.to_csv(index=False)
                            st.download_button(
                                label=f"📥 Download {table_name} as CSV",
                                data=csv,
                                file_name=f"{table_name.lower().replace(' ', '_')}_data.csv",
                                mime="text/csv"
                            )
                        else:
                            st.warning(f"No data available in {table_name}")
                    except Exception as e:
                        st.error(f"Error processing data: {str(e)}")
                else:
                    st.warning(f"No data returned from {table_name} endpoint")

tourism_official_data_tables()