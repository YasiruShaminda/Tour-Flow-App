import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

def initialize_auth_state():
    """Initialize authentication state variables"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' not in st.session_state:
        st.session_state.user_info = None
    if 'credentials' not in st.session_state:
        st.session_state.credentials = None

def check_login_status():
    """Check if user is logged in"""
    initialize_auth_state()
    return st.session_state.logged_in

def create_oauth_flow():
    """Create OAuth flow for Google Sign-In"""
    # Get from session_state instead of env
    client_config = {
        "web": {
            "client_id": st.session_state.get("GOOGLE_CLIENT_ID", "YOUR_CLIENT_ID"),
            "client_secret": st.session_state.get("GOOGLE_CLIENT_SECRET", "YOUR_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uri": "http://localhost:8501/",
            "javascript_origins": ["http://localhost:8501"]
        }
    }
    
    # Create flow instance
    flow = Flow.from_client_config(
        client_config,
        scopes=[
            'openid',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email',
        ],
        redirect_uri=client_config['web']['redirect_uri']
    )
    
    return flow

def get_user_info(credentials):
    """Get user info from Google using credentials"""
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    return user_info

def sign_in_with_google():
    """Sign in with Google"""
    flow = create_oauth_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    
    # In a real app, you'd use a more secure method to handle state
    st.session_state.google_auth_state = state
    
    # Provide link for user to click
    st.markdown(f"[Sign in with Google]({authorization_url})", unsafe_allow_html=True)
    
    # For demo purposes, a simplified approach
    # In a production app, you'd handle the OAuth callback properly
    auth_code = st.text_input("Enter the authorization code from the redirect URL:")
    
    if auth_code:
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        
        # Store credentials in session state
        st.session_state.credentials = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Get user info
        user_info = get_user_info(credentials)
        st.session_state.user_info = user_info
        st.session_state.logged_in = True
        
        return True
    
    return False

def sign_out():
    """Sign out by clearing session state"""
    if 'logged_in' in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' in st.session_state:
        st.session_state.user_info = None
    if 'credentials' in st.session_state:
        st.session_state.credentials = None