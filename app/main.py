import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

from pages.login import login_page
from pages.dashboard import dashboard_page
from pages.upload import upload_page
from pages.flow import flow_page
from pages.suggestions import suggestions_page
from pages.setup import setup_page
from utils.auth import check_login_status

# Load environment variables
load_dotenv()

def secrets_ready():
    return all([
        st.session_state.get("GOOGLE_CLIENT_ID"),
        st.session_state.get("GOOGLE_CLIENT_SECRET"),
        st.session_state.get("GEMINI_API_KEY"),
    ])

# Set page configuration
st.set_page_config(
    page_title="Tour Flow App",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #1E3A8A;
    }
    .stButton button {
        background-color: #1E3A8A;
        color: white;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #2563EB;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Require secrets before anything else
    if not secrets_ready():
        setup_page()
        return

    # Check if user is logged in
    if not check_login_status():
        login_page()
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.image("app/assets/logo.png", width=200, use_column_width=False)
        
        selected = option_menu(
            menu_title="Tour Flow App",
            options=["Dashboard", "Upload Plan", "Tour Flow", "Suggestions"],
            icons=["house", "upload", "arrow-right-circle", "lightbulb"],
            menu_icon="map",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f0f2f6"},
                "icon": {"color": "#1E3A8A", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px"},
                "nav-link-selected": {"background-color": "#1E3A8A", "color": "white"},
            }
        )
        
        st.markdown("---")
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.experimental_rerun()
    
    # Page routing
    if selected == "Dashboard":
        dashboard_page()
    elif selected == "Upload Plan":
        upload_page()
    elif selected == "Tour Flow":
        flow_page()
    elif selected == "Suggestions":
        suggestions_page()

if __name__ == "__main__":
    main() 