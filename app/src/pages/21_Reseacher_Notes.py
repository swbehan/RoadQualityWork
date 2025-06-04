import logging
import streamlit as st
import requests
import pandas as pd
from PIL import Image
import json
from modules.nav import SideBarLinks

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

# Page title
st.title("Research Post & Data Upload")

with st.form("research_form"):
    # Text Area section
    st.header("📝 Jot down thoughts and queries")
    title = st.text_input("Input Title to Post Here")
    notes = st.text_area(
        "Input Notes Here",
        placeholder="Enter your research notes, thoughts, or queries here...",
        height=150,
        key="notes_input"
    )
    
    # Display character count
    if notes:
        st.caption(f"Character count: {len(notes)}")
    
    st.divider()
    
    # Image upload section (simplified - no tabs needed)
    st.header("📁 Image Upload")
    st.subheader("Upload Images")
    
    image_files = st.file_uploader(
        "Choose image files",
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],  # ← Only image files
        accept_multiple_files=True,
        key="image_files"
    )
    
    if image_files:
        for img_file in image_files:
            st.write(f"**Filename:** {img_file.name}")
            st.write(f"**File size:** {img_file.size} bytes")
            
            try:
                from PIL import Image
                image = Image.open(img_file)
                st.image(image, caption=img_file.name, use_column_width=True)
            except Exception as e:
                st.error(f"Error displaying image: {e}")
            
            st.write("---")
    
    # Submit button (this should now appear)
    submitted = st.form_submit_button("📤 Submit Research Post", type="primary")
    
    if submitted:
        if title and notes:
            # Prepare data for API
            post_data = {
                "Title": title,
                "Research": notes,
                "AuthorID": 1
            }
            
            try:
                # Make POST request to Flask API
                response = requests.post(
                    "http://web-api:4000/researcher/new_post",
                    json=post_data
                )

                if response.status_code == 201:
                    st.success("✅ Post created successfully!")
                    result = response.json()
                    st.info(f"ResearchPostID: {result['ResearchPostID']}")
                else:
                    st.error(f"❌ Error: {response.json()['error']}")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
        else:
            st.error("❌ Please fill in Title and Notes!")

# Action buttons (outside form for separate functionality)
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💾 Save Notes", type="secondary"):
        if 'notes_input' in st.session_state and st.session_state.notes_input:
            st.success("Notes saved successfully!")
        else:
            st.warning("No notes to save!")

with col2:
    if st.button("🗑️ Clear All"):
        st.rerun()

with col3:
    if st.button("📋 Export Summary"):
        notes_value = st.session_state.get('notes_input', '')
        image_files_count = len(st.session_state.get('image_files', []) or [])
        
        summary = f"""
Research Session Summary
========================
Notes: {notes_value if notes_value else 'No notes entered'}
Images Uploaded: {image_files_count}
"""
        st.download_button(
            label="Download Summary",
            data=summary,
            file_name="research_summary.txt",
            mime="text/plain"
        )