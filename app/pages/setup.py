import streamlit as st

def setup_page():
    """Display the app setup page with improved UI"""
    st.markdown("<h1 style='text-align: center;'>🔑 App Setup</h1>", unsafe_allow_html=True)
    
    # Create a premium card-like container
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto; background-color: white; 
                padding: 2rem; border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">
        Please enter your API keys below to enable all features of Tour Flow.
    </p>
    
    <div style="background-color: #f1f5f9; border-left: 4px solid #3b82f6; 
                padding: 1rem; border-radius: 0.25rem; margin-bottom: 1.5rem;">
        <p style="margin: 0; font-size: 0.9rem;">
            <strong>Security Note:</strong> Your credentials are stored only in your browser session and are never uploaded to our servers.
            They are used only for authentication and AI features.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Close the intro container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add some space
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Create a card for the setup form
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto; background-color: white; 
                padding: 2rem; border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
    """, unsafe_allow_html=True)
    
    st.markdown("<h2 style='font-size: 1.5rem; margin-bottom: 1.5rem;'>Enter Your Credentials</h2>", unsafe_allow_html=True)
    
    with st.form("setup_form"):
        # Google OAuth Credentials Section
        st.markdown("""
        <div style="margin-bottom: 1rem;">
            <h3 style="font-size: 1.1rem; color: #334155;">Google OAuth Credentials</h3>
            <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1rem;">
                Required for Google Sign-In functionality. 
                <a href="https://console.cloud.google.com/apis/credentials" target="_blank">
                    Get from Google Cloud Console →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            google_client_id = st.text_input(
                "Google Client ID", 
                value=st.session_state.get("GOOGLE_CLIENT_ID", ""),
                placeholder="Your Google Client ID"
            )
        
        with col2:
            google_client_secret = st.text_input(
                "Google Client Secret", 
                type="password", 
                value=st.session_state.get("GOOGLE_CLIENT_SECRET", ""),
                placeholder="Your Google Client Secret"
            )
        
        # Gemini API Key Section
        st.markdown("""
        <div style="margin: 1.5rem 0 1rem 0;">
            <h3 style="font-size: 1.1rem; color: #334155;">Gemini API Key</h3>
            <p style="font-size: 0.9rem; color: #64748b; margin-bottom: 1rem;">
                Required for AI-powered tour suggestions and insights. 
                <a href="https://ai.google.dev/" target="_blank">
                    Get from Google AI Studio →
                </a>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        gemini_api_key = st.text_input(
            "Gemini API Key", 
            type="password", 
            value=st.session_state.get("GEMINI_API_KEY", ""),
            placeholder="Your Gemini API Key"
        )
        
        # Submit button with better styling
        st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Save and Continue", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            # Validate inputs
            if not google_client_id or not google_client_secret or not gemini_api_key:
                st.error("Please fill in all fields to continue.")
            else:
                # Save to session state
                st.session_state["GOOGLE_CLIENT_ID"] = google_client_id.strip()
                st.session_state["GOOGLE_CLIENT_SECRET"] = google_client_secret.strip()
                st.session_state["GEMINI_API_KEY"] = gemini_api_key.strip()
                
                # Show success message
                st.success("✅ Your credentials have been saved successfully!")
                
                # Add a redirect message and automatic refresh
                st.markdown("""
                <div style="text-align: center; margin-top: 1.5rem;">
                    <div class="loading-animation"></div>
                    <p>Redirecting to app...</p>
                </div>
                
                <style>
                    .loading-animation {
                        display: inline-block;
                        width: 20px;
                        height: 20px;
                        border: 3px solid rgba(59, 130, 246, 0.3);
                        border-radius: 50%;
                        border-top-color: #3b82f6;
                        animation: spin 1s ease-in-out infinite;
                        margin-bottom: 0.5rem;
                    }
                    
                    @keyframes spin {
                        to { transform: rotate(360deg); }
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.experimental_rerun()
    
    # Close the form container
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Add helpful tips section at the bottom
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="max-width: 800px; margin: 0 auto; background-color: #f8fafc; 
                padding: 1.5rem; border-radius: 0.5rem; 
                border: 1px solid #e2e8f0;">
        <h3 style="font-size: 1.1rem; color: #334155;">Can't get API keys right now?</h3>
        <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">
            If you're just exploring the app, you can use the "Quick Demo Login" option on the login page
            to try the app with limited functionality.
        </p>
    </div>
    """, unsafe_allow_html=True)