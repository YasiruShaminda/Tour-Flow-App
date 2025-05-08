import streamlit as st
from utils.auth import sign_in_with_google

def login_page():
    """Display the login page"""
    # Center the content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center;'>Welcome to Tour Flow</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Your AI-powered tour companion</p>", unsafe_allow_html=True)
        
        # Display logo (if available)
        try:
            st.image("app/assets/logo.png", width=200)
        except FileNotFoundError:
            # Logo placeholder
            st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # Login options
        st.markdown("<h2 style='text-align: center;'>Sign In</h2>", unsafe_allow_html=True)
        
        # Google Sign-In
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        
        # Call the sign in function
        signed_in = sign_in_with_google()
        
        if signed_in:
            st.success("Successfully signed in!")
            st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # For demonstration, also add a quick login button
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>For demo purposes only:</p>", unsafe_allow_html=True)
        
        if st.button("Quick Demo Login (No Auth)"):
            # Set session state for demo login
            st.session_state.logged_in = True
            st.session_state.user_info = {
                "name": "Demo User",
                "email": "demo@example.com",
                "picture": ""
            }
            st.experimental_rerun()
        
        # Footer
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray; font-size: small;'>© 2025 Tour Flow App</p>", unsafe_allow_html=True) 