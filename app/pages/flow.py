import streamlit as st
import pandas as pd
from utils.parser import find_current_item, generate_next_items
from components.tour_card_component import render_tour_card
from utils.notifications import display_notification_bell

def flow_page():
    """Display the tour flow page"""
    # Display notification bell
    display_notification_bell()
    
    st.header("Your Tour Flow")
    
    # Check if we have an itinerary in session state
    if 'itinerary' not in st.session_state or not st.session_state.itinerary:
        # Show empty state
        st.info("You don't have a tour plan yet. Please upload or create one in the Upload Plan page.")
        
        # Quick action button
        if st.button("➕ Create New Tour Plan"):
            # Switch to upload page
            st.session_state.page = "Upload Plan"
            st.experimental_rerun()
            
        return
    
    # User has an itinerary, display the flow
    itinerary = st.session_state.itinerary
    
    # Filter options
    st.markdown("### Filter Your Tour Flow")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Get unique dates from itinerary
        dates = list(set(item.get('date') for item in itinerary if 'date' in item))
        dates.sort()  # Sort dates
        
        selected_date = st.selectbox(
            "Select Date",
            options=[None] + dates,
            format_func=lambda x: "All Dates" if x is None else x.strftime("%m/%d/%Y"),
            index=0
        )
    
    with col2:
        # Filter by activity type
        activity_types = ["All Types", "attraction", "meal", "accommodation", "transportation", "other"]
        selected_type = st.selectbox("Activity Type", options=activity_types, index=0)
    
    with col3:
        # Search
        search_term = st.text_input("Search", placeholder="Enter keywords...")
    
    # Apply filters
    filtered_itinerary = itinerary
    
    if selected_date:
        filtered_itinerary = [item for item in filtered_itinerary if item.get('date') == selected_date]
    
    if selected_type != "All Types":
        filtered_itinerary = [item for item in filtered_itinerary if item.get('type') == selected_type]
    
    if search_term:
        search_term = search_term.lower()
        filtered_itinerary = [
            item for item in filtered_itinerary 
            if (search_term in item.get('activity', '').lower() or 
                search_term in item.get('location', '').lower() or 
                any(search_term in note.lower() for note in item.get('notes', [])))
        ]
    
    # Display flow visualization
    st.markdown("### Tour Timeline")
    
    # Find current activity
    current_idx = find_current_item(itinerary)
    
    # If we have no items after filtering
    if not filtered_itinerary:
        st.info("No activities match your filter criteria.")
        return
    
    # Create the flow visualization
    for i, item in enumerate(filtered_itinerary):
        # Check if this is the current item in the original itinerary
        original_idx = itinerary.index(item)
        is_current = (original_idx == current_idx)
        
        # Create columns for the card and actions
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Render the card
            render_tour_card(item, is_current=is_current)
        
        with col2:
            # Action buttons
            st.button("✏️ Edit", key=f"edit_{i}")
            st.button("🗑️ Delete", key=f"delete_{i}")
            
            # Spacer
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            # Move buttons
            if i > 0:
                st.button("⬆️ Move Up", key=f"up_{i}")
            if i < len(filtered_itinerary) - 1:
                st.button("⬇️ Move Down", key=f"down_{i}")
    
    # Edit modal (in a real app, this would be a proper modal)
    st.markdown("### Edit Activity")
    st.markdown("Select an activity above and click Edit to modify its details.")
    
    # Add new activity button
    if st.button("➕ Add New Activity"):
        # Redirect to the upload page's manual creation tab
        st.session_state.create_new = True
        st.experimental_rerun()
    
    # Export options
    st.markdown("### Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📤 Export as CSV"):
            # Convert to DataFrame for export
            df = pd.DataFrame(itinerary)
            # In a real app, this would download a CSV file
            st.success("In a real app, this would download a CSV file.")
    
    with col2:
        if st.button("📱 Export to Calendar"):
            # In a real app, this would export to calendar
            st.success("In a real app, this would export to your calendar app.") 