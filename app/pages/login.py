import streamlit as st
from utils.auth import sign_in_with_google

def login_page():
    """Display the login page with premium UI"""
    # Use wider layout for login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Create a card-like container for login
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        # Logo and welcome text
        try:
            st.image("app/assets/logo.png", width=180, use_column_width=False)
        except:
            st.title("Tour Flow")
            
        st.markdown("<h1 style='text-align: center; font-size: 1.8rem; margin-bottom: 0;'>Welcome to Tour Flow</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-bottom: 2rem;'>Your AI-powered tour companion</p>", unsafe_allow_html=True)
        
        # Divider
        st.markdown("<hr style='margin: 1.5rem 0; opacity: 0.2;'>", unsafe_allow_html=True)
        
        # Login section
        st.markdown("<h2 style='text-align: center; font-size: 1.2rem; margin-bottom: 1.5rem;'>Sign In</h2>", unsafe_allow_html=True)
        
        # Login container
        st.markdown("<div style='background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>", unsafe_allow_html=True)
        
        # Google Sign-In
        with st.container():
            signed_in = sign_in_with_google()
            
            if signed_in:
                # Show success animation
                st.success("Successfully signed in!")
                st.markdown("""
                    <div style='text-align: center; margin-top: 1rem;'>
                        <div class='loading-spinner'></div>
                        <p>Redirecting to dashboard...</p>
                    </div>
                """, unsafe_allow_html=True)
                st.experimental_rerun()
        
        # Quick demo login option
        st.markdown("<div style='margin-top: 1.5rem; text-align: center;'>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 0.9rem; margin-bottom: 0.5rem;'>For demo purposes only:</p>", unsafe_allow_html=True)
        
        demo_btn = st.button("Quick Demo Login (No Auth)", use_container_width=True)
        if demo_btn:
            # Set session state for demo login
            st.session_state.logged_in = True
            st.session_state.user_info = {
                "name": "Demo User",
                "email": "demo@example.com",
                "picture": ""
            }
            
            # Make sure Gemini API key is set to avoid redirect to setup
            if "GEMINI_API_KEY" not in st.session_state:
                try:
                    st.session_state["GEMINI_API_KEY"] = st.secrets.get("GEMINI_API_KEY", "demo_key")
                except:
                    st.session_state["GEMINI_API_KEY"] = "demo_key"
                    
            # Make sure Google client credentials are set
            if "GOOGLE_CLIENT_ID" not in st.session_state:
                st.session_state["GOOGLE_CLIENT_ID"] = "demo_client_id"
            if "GOOGLE_CLIENT_SECRET" not in st.session_state:
                st.session_state["GOOGLE_CLIENT_SECRET"] = "demo_client_secret"
                
            st.experimental_rerun()
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Close the login container
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Footer with additional information
        st.markdown("""
            <div style='margin-top: 2rem; text-align: center;'>
                <p style='color: #64748b; font-size: 0.8rem;'>
                    Tour Flow helps you organize and enhance your travel experience with AI
                </p>
                <p style='color: #94a3b8; font-size: 0.7rem; margin-top: 1rem;'>
                    © 2023 Tour Flow App | <a href='#' style='color: #94a3b8;'>Privacy Policy</a> | <a href='#' style='color: #94a3b8;'>Terms of Service</a>
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Close the card container
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add CSS for the login card
        st.markdown("""
        <style>
            .login-card {
                background-color: #f8fafc;
                border-radius: 1rem;
                padding: 2rem;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                margin-top: 2rem;
                text-align: center;
            }
            
            .loading-spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(59, 130, 246, 0.3);
                border-radius: 50%;
                border-top-color: #3b82f6;
                animation: spin 1s ease-in-out infinite;
                margin-right: 8px;
            }
            
            @keyframes spin {
                to { transform: rotate(360deg); }
            }
            
            @media (max-width: 768px) {
                .login-card {
                    padding: 1.5rem;
                    margin-top: 1rem;
                }
            }
        </style>
        """, unsafe_allow_html=True) 