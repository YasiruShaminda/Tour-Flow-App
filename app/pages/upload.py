import streamlit as st
import pandas as pd
import datetime
from utils.parser import parse_tour_agenda
from utils.notifications import schedule_notification_for_next_item
from utils.ai_suggestions import get_place_insights

def upload_page():
    """Display the upload plan page"""
    st.header("Upload Your Tour Plan")
    
    # Instructions
    st.markdown("""
    Upload your tour agenda as a text file or paste it below. 
    The system will parse your agenda and create an interactive flow visualization.
    
    ### Format Tips
    
    For best results, ensure your itinerary includes:
    - Dates in MM/DD/YYYY format
    - Times in HH:MM AM/PM format
    - Clear activity descriptions
    - Location information
    """)
    
    # Create tabs for different input methods
    tab1, tab2, tab3 = st.tabs(["Upload File", "Paste Text", "Create Manually"])
    
    with tab1:
        # File uploader
        uploaded_file = st.file_uploader("Upload your tour agenda (TXT file)", type=["txt"])
        
        if uploaded_file is not None:
            # Read the file
            content = uploaded_file.read().decode("utf-8")
            
            # Show the raw content
            with st.expander("Raw Content Preview", expanded=False):
                st.text(content)
            
            # Process the file when the button is clicked
            if st.button("Process Tour Agenda", key="process_file"):
                process_agenda(content)
    
    with tab2:
        # Text area for pasting content
        pasted_content = st.text_area("Paste your tour agenda here", height=300)
        
        if pasted_content:
            # Process the pasted content
            if st.button("Process Tour Agenda", key="process_pasted"):
                process_agenda(pasted_content)
    
    with tab3:
        # Manual creation
        st.markdown("### Create Your Tour Agenda Manually")
        
        # Initialize session state for manual creation
        if 'manual_items' not in st.session_state:
            st.session_state.manual_items = []
        
        # Form for adding new items
        with st.form("add_item_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                # Date picker
                activity_date = st.date_input("Date", value=datetime.date.today())
                
                # Time input
                activity_time = st.time_input("Time", value=datetime.time(9, 0))
                
                # Activity type selector
                activity_type = st.selectbox(
                    "Activity Type",
                    options=["attraction", "meal", "accommodation", "transportation", "other"]
                )
            
            with col2:
                # Activity description
                activity_name = st.text_input("Activity Description")
                
                # Location
                location = st.text_input("Location")
                
                # Duration
                duration = st.number_input("Duration (minutes)", min_value=0, value=60)
            
            # Notes
            notes = st.text_area("Notes (optional)")
            
            # Submit button
            submitted = st.form_submit_button("Add to Itinerary")
            
            if submitted:
                # Create a new item
                new_item = {
                    "date": activity_date,
                    "time": activity_time.strftime("%-I:%M %p"),
                    "activity": activity_name,
                    "location": location,
                    "duration_minutes": duration,
                    "type": activity_type
                }
                
                if notes:
                    new_item["notes"] = [notes]
                
                # Add to session state
                st.session_state.manual_items.append(new_item)
                st.success("Item added to itinerary!")
        
        # Display the current manual items
        if st.session_state.manual_items:
            st.markdown("### Current Itinerary Items")
            
            # Convert to DataFrame for display
            df = pd.DataFrame(st.session_state.manual_items)
            
            # Format the display columns
            display_df = df[['date', 'time', 'activity', 'location', 'type']].copy()
            
            # Display as table
            st.dataframe(display_df, use_container_width=True)
            
            # Button to process the manual itinerary
            if st.button("Process Manual Itinerary"):
                process_manual_agenda()
            
            # Button to clear the manual itinerary
            if st.button("Clear Manual Itinerary"):
                st.session_state.manual_items = []
                st.success("Manual itinerary cleared!")
                st.experimental_rerun()
    
    # Show previous itinerary if it exists
    if 'itinerary' in st.session_state and st.session_state.itinerary:
        with st.expander("Current Processed Itinerary", expanded=False):
            # Convert to DataFrame for display
            df = pd.DataFrame(st.session_state.itinerary)
            
            # Handle missing columns
            required_cols = ['date', 'time', 'activity', 'location', 'type']
            for col in required_cols:
                if col not in df.columns:
                    df[col] = ""
            
            # Display as table
            st.dataframe(df[required_cols], use_container_width=True)
            
            # Button to clear current itinerary
            if st.button("Clear Current Itinerary"):
                st.session_state.itinerary = []
                if 'insights' in st.session_state:
                    st.session_state.insights = {}
                st.success("Itinerary cleared!")
                st.experimental_rerun()

def process_agenda(content):
    """Process the agenda content and store in session state"""
    with st.spinner("Processing your tour agenda..."):
        # Parse the content
        itinerary = parse_tour_agenda(content)
        
        # Store in session state
        st.session_state.itinerary = itinerary
        
        # Initialize insights dictionary
        if 'insights' not in st.session_state:
            st.session_state.insights = {}
        
        # Schedule notifications for the next few items
        schedule_notifications(itinerary)
        
        # Get insights for locations (background task in real app)
        fetch_insights_for_locations(itinerary)
        
        # Show success message
        st.success(f"Successfully processed {len(itinerary)} itinerary items!")
        
        # Add a button to view the tour flow
        if st.button("View Tour Flow"):
            # Redirect to the tour flow page
            st.experimental_rerun()

def process_manual_agenda():
    """Process the manually created agenda"""
    if not st.session_state.manual_items:
        st.warning("No items in manual itinerary!")
        return
    
    # Store in session state
    st.session_state.itinerary = st.session_state.manual_items
    
    # Initialize insights dictionary
    if 'insights' not in st.session_state:
        st.session_state.insights = {}
    
    # Schedule notifications for the next few items
    schedule_notifications(st.session_state.manual_items)
    
    # Get insights for locations (background task in real app)
    fetch_insights_for_locations(st.session_state.manual_items)
    
    # Show success message
    st.success(f"Successfully processed {len(st.session_state.manual_items)} itinerary items!")
    
    # Add a button to view the tour flow
    if st.button("View Tour Flow"):
        # Redirect to the tour flow page
        st.experimental_rerun()

def schedule_notifications(itinerary):
    """Schedule notifications for the itinerary items"""
    current_time = datetime.datetime.now().time()
    current_date = datetime.date.today()
    
    # Find items that are coming up soon
    for i, item in enumerate(itinerary):
        item_date = item.get('date')
        
        # Only schedule for today or future dates
        if not item_date or item_date < current_date:
            continue
        
        # Schedule notification
        notification_id = schedule_notification_for_next_item(item)
        if notification_id:
            # Store the notification ID with the item
            itinerary[i]['notification_id'] = notification_id

def fetch_insights_for_locations(itinerary):
    """Fetch insights for locations in the itinerary"""
    # In a real app, this would be done in the background to avoid blocking
    # For demo purposes, we'll just fetch for a few items
    
    # Check for Gemini API key
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if not api_key:
        # Skip insights if no API key
        return
    
    for item in itinerary[:3]:  # Just do first 3 for demo
        if 'location' in item and item['location']:
            location = item['location']
            activity_type = item.get('type')
            
            # Create a key for the location
            location_key = location.lower().replace(' ', '_')
            
            # Skip if we already have insights for this location
            if location_key in st.session_state.insights:
                continue
            
            # Get insights
            try:
                insights = get_place_insights(location, activity_type)
                st.session_state.insights[location_key] = insights
            except Exception as e:
                print(f"Error getting insights for {location}: {e}")
                continue 