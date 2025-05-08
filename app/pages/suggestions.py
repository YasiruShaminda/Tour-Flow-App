import streamlit as st
import datetime
from utils.parser import find_current_item
from utils.ai_suggestions import get_nearby_suggestions, get_meal_suggestions
from components.tour_card_component import render_suggestion_card
from utils.notifications import display_notification_bell, add_notification

def suggestions_page():
    """Display the suggestions page"""
    # Display notification bell
    display_notification_bell()
    
    st.header("Personalized Suggestions")
    
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
    
    # User has an itinerary, display suggestions
    itinerary = st.session_state.itinerary
    
    # Find current activity
    current_idx = find_current_item(itinerary)
    
    if current_idx < 0 or current_idx >= len(itinerary):
        st.warning("Could not determine your current activity.")
        return
    
    current_item = itinerary[current_idx]
    
    # Display current location
    current_location = current_item.get('location', 'Unknown location')
    current_activity = current_item.get('activity', 'Unknown activity')
    
    st.subheader(f"Based on your current location: {current_location}")
    st.markdown(f"**Current activity:** {current_activity}")
    
    # Create tabs for different types of suggestions
    tab1, tab2, tab3, tab4 = st.tabs([
        "Nearby Attractions", 
        "Restaurants & Food", 
        "Shopping", 
        "Local Events"
    ])
    
    with tab1:
        st.markdown("### Nearby Attractions")
        
        # Initialize session state for attractions
        if 'nearby_attractions' not in st.session_state:
            st.session_state.nearby_attractions = []
            
        # Button to get suggestions
        if st.button("🔍 Find Nearby Attractions") or st.session_state.nearby_attractions:
            if not st.session_state.nearby_attractions:
                with st.spinner("Finding nearby attractions..."):
                    # Get suggestions from AI
                    try:
                        suggestions = get_nearby_suggestions(current_location, 'attraction')
                        st.session_state.nearby_attractions = suggestions
                    except Exception as e:
                        st.error(f"Error getting suggestions: {e}")
                        
                        # For demo, provide sample suggestions if API fails
                        st.session_state.nearby_attractions = [
                            {
                                "name": "Central Park",
                                "type": "Park",
                                "description": "Iconic urban park with walking paths, lakes, and open spaces.",
                                "estimated_time": "2-3 hours"
                            },
                            {
                                "name": "Metropolitan Museum of Art",
                                "type": "Museum",
                                "description": "World-class art museum with extensive collections.",
                                "estimated_time": "3-4 hours"
                            },
                            {
                                "name": "Top of the Rock",
                                "type": "Observation Deck",
                                "description": "Spectacular views of Manhattan from Rockefeller Center.",
                                "estimated_time": "1 hour"
                            }
                        ]
            
            # Display suggestions
            for suggestion in st.session_state.nearby_attractions:
                render_suggestion_card(suggestion, "attr")
    
    with tab2:
        st.markdown("### Restaurant Suggestions")
        
        # Initialize session state for restaurants
        if 'nearby_restaurants' not in st.session_state:
            st.session_state.nearby_restaurants = []
        
        # Check time of day for meal type suggestion
        now = datetime.datetime.now()
        hour = now.hour
        
        if 6 <= hour < 11:
            meal_type = "breakfast"
        elif 11 <= hour < 15:
            meal_type = "lunch"
        elif 17 <= hour < 22:
            meal_type = "dinner"
        else:
            meal_type = "meal"
        
        # Button to get suggestions
        if st.button(f"🍽️ Find {meal_type.title()} Places") or st.session_state.nearby_restaurants:
            if not st.session_state.nearby_restaurants:
                with st.spinner(f"Finding {meal_type} places..."):
                    # Get suggestions from AI
                    try:
                        suggestions = get_meal_suggestions(current_location, meal_type)
                        st.session_state.nearby_restaurants = suggestions
                        
                        # Add a meal notification
                        add_notification(
                            f"Time for {meal_type}!",
                            f"Here are some {meal_type} suggestions near {current_location}"
                        )
                    except Exception as e:
                        st.error(f"Error getting suggestions: {e}")
                        
                        # For demo, provide sample suggestions if API fails
                        st.session_state.nearby_restaurants = [
                            {
                                "name": "The Local Grill",
                                "cuisine": "American",
                                "description": "Casual dining with burgers and steaks.",
                                "price_range": "$$"
                            },
                            {
                                "name": "Pasta Palace",
                                "cuisine": "Italian",
                                "description": "Authentic Italian pasta and pizza.",
                                "price_range": "$$"
                            },
                            {
                                "name": "Sushi Spot",
                                "cuisine": "Japanese",
                                "description": "Fresh sushi and Japanese specialties.",
                                "price_range": "$$$"
                            }
                        ]
            
            # Display suggestions
            for suggestion in st.session_state.nearby_restaurants:
                render_suggestion_card(suggestion, "rest")
    
    with tab3:
        st.markdown("### Shopping Suggestions")
        
        # Sample shopping suggestions (in a real app, these would come from the API)
        shopping_suggestions = [
            {
                "name": "Local Artisan Market",
                "type": "Market",
                "description": "Local crafts, souvenirs, and handmade goods."
            },
            {
                "name": "City Center Mall",
                "type": "Shopping Mall",
                "description": "Major retail stores and boutiques in downtown."
            },
            {
                "name": "Vintage Finds",
                "type": "Thrift Store",
                "description": "Unique vintage clothing and accessories."
            }
        ]
        
        # Display suggestions
        for suggestion in shopping_suggestions:
            render_suggestion_card(suggestion, "shop")
    
    with tab4:
        st.markdown("### Local Events")
        
        # Sample events (in a real app, these would come from the API)
        events = [
            {
                "name": "Farmers Market",
                "type": "Market",
                "description": "Local produce and artisan foods, open Saturday 8am-1pm."
            },
            {
                "name": "Live Jazz at The Blue Note",
                "type": "Music",
                "description": "Evening jazz performances starting at 8pm."
            },
            {
                "name": "Historical Walking Tour",
                "type": "Tour",
                "description": "Guided walking tour of historic district, starts at 10am daily."
            }
        ]
        
        # Display suggestions
        for event in events:
            render_suggestion_card(event, "event")
    
    # Add ability to save favorites
    st.markdown("---")
    st.subheader("Your Saved Favorites")
    
    # Initialize saved favorites in session state
    if 'saved_favorites' not in st.session_state:
        st.session_state.saved_favorites = []
    
    if not st.session_state.saved_favorites:
        st.info("You haven't saved any favorites yet. Click 'Add to Plan' on any suggestion to save it!")
    else:
        # Display saved favorites
        for favorite in st.session_state.saved_favorites:
            with st.container():
                st.markdown(f"**{favorite.get('name', 'Unknown place')}**")
                st.markdown(favorite.get('description', ''))
                if st.button("🗑️ Remove", key=f"remove_{favorite.get('name', '').replace(' ', '_').lower()}"):
                    st.session_state.saved_favorites.remove(favorite)
                    st.experimental_rerun()
                st.markdown("---") 