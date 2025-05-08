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
    # Get client ID and secret from session state or secrets
    client_id = st.session_state.get("GOOGLE_CLIENT_ID")
    client_secret = st.session_state.get("GOOGLE_CLIENT_SECRET")
    
    # Check if we have the values in session_state
    if not client_id or not client_secret:
        try:
            # Try to get from secrets
            client_id = st.secrets.get("GOOGLE_CLIENT_ID")
            client_secret = st.secrets.get("GOOGLE_CLIENT_SECRET")
        except:
            # Fallback to defaults (which won't work but prevent errors)
            client_id = "YOUR_CLIENT_ID"
            client_secret = "YOUR_CLIENT_SECRET"
    
    # Store in session state for future use
    st.session_state["GOOGLE_CLIENT_ID"] = client_id
    st.session_state["GOOGLE_CLIENT_SECRET"] = client_secret
    
    client_config = {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uri": "https://tourflow.streamlit.app/",
            "javascript_origins": ["https://tourflow.streamlit.app"]
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
    
    # Create a better looking button for Google Sign-In
    google_btn = """
    <a href="{}" target="_blank" style="display: inline-block; 
       background-color: white; color: #444; 
       border-radius: 5px; border: thin solid #888; box-shadow: 1px 1px 1px grey;
       white-space: nowrap; height: 40px; padding: 0 15px;">
      <img width="20px" style="margin-right:8px; margin-top:10px;" 
           src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Google_%22G%22_Logo.svg/512px-Google_%22G%22_Logo.svg.png" />
      <span style="position:relative; top:-6px;">Sign in with Google</span>
    </a>
    """
    st.markdown(google_btn.format(authorization_url), unsafe_allow_html=True)
    
    # For demo purposes, a simplified approach to handle the OAuth code
    # In a production app, you'd handle the OAuth callback properly
    st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    auth_code = st.text_input("Enter the authorization code from the redirect URL:", 
                              help="After clicking the button above, copy the code from the URL you're redirected to")
    
    if auth_code:
        try:
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
            
            # Make sure we have the Gemini API key in the session state
            # If it's not already there, try to get it from secrets
            if "GEMINI_API_KEY" not in st.session_state:
                try:
                    st.session_state["GEMINI_API_KEY"] = st.secrets.get("GEMINI_API_KEY", "")
                except:
                    # If not in secrets, it will be requested in the setup page
                    pass
            
            return True
        except Exception as e:
            st.error(f"Error authenticating: {str(e)}")
            return False
    
    return False

def sign_out():
    """Sign out by clearing session state"""
    if 'logged_in' in st.session_state:
        st.session_state.logged_in = False
    if 'user_info' in st.session_state:
        st.session_state.user_info = None
    if 'credentials' in st.session_state:
        st.session_state.credentials = None