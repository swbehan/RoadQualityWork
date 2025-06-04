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

def delete_post(post_id):
    """Delete a post by ID"""
    try:
        response = requests.delete(f"http://host.docker.internal:4000/researcher/delete_post/{post_id}")
        
        if response.status_code == 200:
            return True
        else:
            st.error(f"Delete failed: {response.json().get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return False

def display_posts(posts):
    """Display posts in user-friendly Streamlit format"""
    if posts:
        st.success(f"✅ Found {len(posts)} posts")
        
        # Add search functionality
        search_term = st.text_input("🔍 Search posts", placeholder="Search by title or content...")
        
        # Filter posts if search term provided
        if search_term:
            filtered_posts = []
            for post in posts:
                title = str(post.get('Title', '')).lower()
                research = str(post.get('Research', '')).lower()
                author_name = str(post.get('ResearcherName', '')).lower()
                field_of_study = str(post.get('FieldOfStudy', '')).lower()
                
                search_lower = search_term.lower()
                if (search_lower in title or 
                    search_lower in research or 
                    search_lower in author_name or 
                    search_lower in field_of_study):
                    filtered_posts.append(post)
            posts = filtered_posts
            
            if not posts:
                st.warning(f"No posts found matching '{search_term}'")
                return
        
        st.write(f"**Showing {len(posts)} posts**")
        st.divider()
        
        # Display each post
        for post in posts:
            # Extract data from the post dictionary
            research_post_id = post.get('ResearchPostID', 'N/A')
            title = post.get('Title', 'No Title')
            post_date = post.get('PostDate', 'No Date')
            research_content = post.get('Research', 'No Content')
            author_id = post.get('AuthorID', 'N/A')
            author_name = post.get('ResearcherName', 'Unknown Author')
            field_of_study = post.get('FieldOfStudy', 'Unknown Field')
            
            # Create expandable section for each post
            with st.expander(f"📄 {title} ({author_name})", expanded=False):
                # Post metadata
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write("**📅 Posted:**", str(post_date))
                    st.write("**👤 Author:**", author_name)
                    st.write("**🎓 Field:**", field_of_study)
                
                with col2:
                    st.write("**🆔 Post ID:**", research_post_id)
                
                st.divider()
                
                # Post content
                st.write("**📝 Research Content:**")
                st.write(research_content)
                
                # Delete button
                if st.button(f"🗑️ Delete Post", key=f"delete_{research_post_id}", type="secondary"):
                    if delete_post(research_post_id):
                        st.success(f"✅ Post {research_post_id} deleted successfully!")
                        st.rerun()  # Refresh the page to show updated posts
                    else:
                        st.error(f"❌ Failed to delete post {research_post_id}")
                
                st.write("---")
    
    else:
        st.info("📭 No posts found. Create your first post!")

def view_posts_page():
    """Main function to fetch and display posts"""
    st.title("📖 View Research Posts")
    
    # Add refresh button
    if st.button("🔄 Refresh Posts"):
        st.rerun()
    
    try:
        # Make GET request to Flask API
        response = requests.get("http://host.docker.internal:4000/researcher/get_all_posts")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('posts', [])
            
            # Display posts using your function
            display_posts(posts)
            
        else:
            st.error(f"❌ Failed to load posts: {response.status_code}")
            try:
                error_data = response.json()
                st.error(f"Error: {error_data.get('error', 'Unknown error')}")
            except:
                st.error(f"Response: {response.text}")
    
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API. Make sure your Flask server is running.")
    except requests.exceptions.Timeout:
        st.error("❌ Request timed out. Please try again.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")

# Usage:
# Call this function in your Streamlit app
if __name__ == "__main__":
    view_posts_page()