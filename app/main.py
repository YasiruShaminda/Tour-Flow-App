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

# Function to check if necessary API keys are in session state
def secrets_ready():
    # First check if they're in st.secrets (preferred)
    try:
        if all([
            st.secrets.get("GOOGLE_CLIENT_ID"),
            st.secrets.get("GOOGLE_CLIENT_SECRET"),
            st.secrets.get("GEMINI_API_KEY"),
        ]):
            # Copy from secrets to session state for consistency
            if "GOOGLE_CLIENT_ID" not in st.session_state:
                st.session_state["GOOGLE_CLIENT_ID"] = st.secrets.get("GOOGLE_CLIENT_ID")
            if "GOOGLE_CLIENT_SECRET" not in st.session_state:
                st.session_state["GOOGLE_CLIENT_SECRET"] = st.secrets.get("GOOGLE_CLIENT_SECRET")
            if "GEMINI_API_KEY" not in st.session_state:
                st.session_state["GEMINI_API_KEY"] = st.secrets.get("GEMINI_API_KEY")
            return True
    except:
        pass
    
    # Fall back to session state if secrets aren't available
    return all([
        st.session_state.get("GOOGLE_CLIENT_ID"),
        st.session_state.get("GOOGLE_CLIENT_SECRET"),
        st.session_state.get("GEMINI_API_KEY"),
    ])

# Set page configuration
st.set_page_config(
    page_title="Tour Flow",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Modern UI CSS
st.markdown("""
<style>
    /* Main styles */
    .main {
        background-color: #f8fafc;
        color: #334155;
        font-family: 'Inter', sans-serif;
    }
    
    /* App container */
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Block container spacing */
    .block-container {
        padding: 1.5rem 1rem;
    }
    
    /* Typography */
    h1 {
        color: #0f172a;
        font-weight: 700;
        font-size: 2.25rem;
        margin-bottom: 1.5rem;
    }
    
    h2 {
        color: #1e293b;
        font-weight: 600;
        font-size: 1.75rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #334155;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 0.75rem;
    }
    
    p {
        line-height: 1.6;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #3b82f6;
        border: none;
        color: white;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Form inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox, .stMultiselect {
        border-radius: 0.375rem;
        border: 1px solid #cbd5e1;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Cards and containers */
    .card {
        background-color: white;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }
    
    .card:hover {
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    /* Success message */
    .element-container .stAlert .alert {
        border-radius: 0.375rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .card {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.75rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
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
    
    # Sidebar navigation with premium design
    with st.sidebar:
        try:
            st.image("app/assets/logo.png", width=150, use_column_width=False)
        except:
            st.title("Tour Flow")
        
        st.markdown("---")
        
        selected = option_menu(
            menu_title=None,
            options=["Dashboard", "Upload Plan", "Tour Flow", "Suggestions"],
            icons=["speedometer2", "cloud-upload", "map", "lightbulb"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0px", "background-color": "transparent"},
                "icon": {"color": "#3b82f6", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px", 
                    "text-align": "left", 
                    "margin": "0px",
                    "padding": "10px 15px",
                    "border-radius": "5px",
                    "margin-bottom": "5px"
                },
                "nav-link-selected": {
                    "background-color": "#3b82f6", 
                    "color": "white",
                    "font-weight": "600"
                },
            }
        )
        
        st.markdown("---")
        
        # User profile section
        if st.session_state.get("user_info"):
            user = st.session_state.user_info
            col1, col2 = st.columns([1, 3])
            with col1:
                if user.get("picture"):
                    st.image(user.get("picture"), width=40)
                else:
                    st.markdown("👤")
            with col2:
                st.markdown(f"**{user.get('name', 'User')}**")
                st.markdown(f"<small>{user.get('email', '')}</small>", unsafe_allow_html=True)
        
        # Sign out button
        if st.button("Sign Out", key="sign_out_btn"):
            st.session_state.logged_in = False
            # Don't clear API keys to avoid re-entering them
            st.session_state.user_info = None
            st.session_state.credentials = None
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