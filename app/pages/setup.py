import streamlit as st

def setup_page():
    st.title("🔑 App Setup: Enter Your API Keys & Secrets")
    st.markdown("""
    Please enter your credentials below. These are required for authentication and AI features. 
    **They are only stored in your browser session and never uploaded.**
    """)

    with st.form("setup_form"):
        google_client_id = st.text_input("Google Client ID", value=st.session_state.get("GOOGLE_CLIENT_ID", ""))
        google_client_secret = st.text_input("Google Client Secret", type="password", value=st.session_state.get("GOOGLE_CLIENT_SECRET", ""))
        gemini_api_key = st.text_input("Gemini API Key", type="password", value=st.session_state.get("GEMINI_API_KEY", ""))
        submitted = st.form_submit_button("Save and Continue")

        if submitted:
            st.session_state["GOOGLE_CLIENT_ID"] = google_client_id.strip()
            st.session_state["GOOGLE_CLIENT_SECRET"] = google_client_secret.strip()
            st.session_state["GEMINI_API_KEY"] = gemini_api_key.strip()
            st.success("Secrets saved for this session!")
            st.experimental_rerun()

    st.info("You must fill in all fields to use the app.")