import streamlit as st
import datetime
from utils.notifications import display_notification_bell, get_all_notifications, mark_notification_as_read
from utils.parser import find_current_item, generate_next_items
from components.tour_card_component import render_current_activity, render_next_activities

def dashboard_page():
    """Display the dashboard page"""
    # Display notification bell
    display_notification_bell()
    
    # Check if we have an itinerary in session state
    if 'itinerary' not in st.session_state or not st.session_state.itinerary:
        # Show welcome message
        st.header("Welcome to Tour Flow!")
        
        # Show empty state
        st.markdown("""
        ## Get Started
        
        You don't have any tour plans yet. Let's create one!
        
        1. Go to the **Upload Plan** page to upload your tour agenda
        2. View your tour as an interactive flow chart
        3. Get personalized suggestions and insights
        """)
        
        # Quick action button
        if st.button("➕ Create New Tour Plan"):
            # Switch to upload page
            st.session_state.page = "Upload Plan"
            st.experimental_rerun()
            
        # Display sample itinerary
        st.markdown("### Example Tour Flow")
        
        # Show a sample tour item
        sample_item = {
            "time": "9:00 AM",
            "activity": "Visit the Museum of Modern Art",
            "location": "11 W 53rd St, New York, NY",
            "duration_minutes": 120,
            "type": "attraction",
            "notes": ["Don't miss the Van Gogh collection on the 5th floor", "Audio guide available for $5"]
        }
        
        render_current_activity(sample_item)
        
        return
    
    # User has an itinerary, display the dashboard
    st.header("Your Tour Dashboard")
    
    # Get the current date
    today = datetime.date.today()
    st.subheader(f"Today: {today.strftime('%A, %B %d, %Y')}")
    
    # Get current and next activities
    itinerary = st.session_state.itinerary
    current_idx = find_current_item(itinerary)
    current_item = itinerary[current_idx] if 0 <= current_idx < len(itinerary) else None
    next_items = generate_next_items(itinerary, current_idx)
    
    # Show notifications panel if there are any
    notifications = get_all_notifications()
    if notifications:
        with st.expander("📬 Notifications", expanded=True):
            for notification in notifications:
                # Display each notification
                with st.container():
                    st.markdown(f"**{notification['title']}**")
                    st.markdown(notification['message'])
                    
                    # Button to mark as read
                    if not notification.get('is_read', False):
                        if st.button("Mark as read", key=f"read_{notification['id']}"):
                            mark_notification_as_read(notification['id'])
                            st.experimental_rerun()
                    
                    st.markdown("---")
    
    # Display current activity if available
    if current_item:
        # Check if we have AI insights for this item
        insights = None
        if 'insights' in st.session_state and current_item.get('location'):
            location_key = current_item['location'].lower().replace(' ', '_')
            insights = st.session_state.insights.get(location_key)
        
        render_current_activity(current_item, insights)
    else:
        st.info("No activities scheduled for right now")
    
    # Display next activities
    if next_items:
        render_next_activities(next_items)
    else:
        st.info("No more activities scheduled")
    
    # Daily overview section
    with st.expander("📋 Daily Overview", expanded=False):
        # Filter itinerary for today's date
        today_items = [item for item in itinerary if item.get('date') == today]
        
        if today_items:
            for item in today_items:
                # Simplified card for overview
                st.markdown(f"**{item.get('time', '')}** - {item.get('activity', '')}")
                if item.get('location'):
                    st.markdown(f"📍 {item['location']}")
                st.markdown("---")
        else:
            st.info("No activities scheduled for today") 