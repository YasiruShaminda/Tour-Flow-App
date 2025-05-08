import streamlit as st
from typing import Dict, Any
from datetime import datetime

# Define card colors based on activity type
CARD_COLORS = {
    'meal': '#FFEAA7',  # Light yellow
    'attraction': '#A0E7E5',  # Light teal
    'accommodation': '#B5EAD7',  # Light green
    'transportation': '#FFCFDF',  # Light pink
    'other': '#E2F0CB'  # Light lime
}

def render_tour_card(item: Dict[str, Any], is_current: bool = False, show_insights: bool = False):
    """
    Render a tour item as a card
    
    Args:
        item: Tour item dictionary
        is_current: Whether this is the current item
        show_insights: Whether to show AI insights
    """
    # Get card color based on activity type
    card_type = item.get('type', 'other')
    card_color = CARD_COLORS.get(card_type, CARD_COLORS['other'])
    
    # Add extra styling for current item
    border_style = "border-left: 4px solid #1E3A8A;" if is_current else ""
    shadow_style = "box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);" if is_current else ""
    
    # Format time and activity
    time_str = item.get('time', 'No time specified')
    activity = item.get('activity', 'No activity specified')
    location = item.get('location', '')
    duration = item.get('duration_minutes', 0)
    
    # Format duration
    duration_str = ""
    if duration:
        if duration < 60:
            duration_str = f"{duration} min"
        else:
            hours = duration // 60
            minutes = duration % 60
            if minutes == 0:
                duration_str = f"{hours} hr"
            else:
                duration_str = f"{hours} hr {minutes} min"
    
    # Card HTML
    card_html = f"""
    <div style="background-color: {card_color}; border-radius: 10px; padding: 15px; margin-bottom: 15px; 
                {border_style} {shadow_style}">
        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
            <div style="font-weight: bold; font-size: 1.1rem;">{time_str}</div>
            <div style="font-size: 0.9rem; color: #555;">
                {duration_str if duration_str else ""}
            </div>
        </div>
        <div style="font-size: 1.2rem; margin-bottom: 8px;">{activity}</div>
        {f'<div style="font-size: 0.9rem; color: #555; margin-bottom: 8px;">📍 {location}</div>' if location else ''}
    """
    
    # Add notes if available
    notes = item.get('notes', [])
    if notes:
        notes_html = '<div style="margin-top: 10px; font-size: 0.9rem; color: #555;">'
        for note in notes:
            notes_html += f'<div>• {note}</div>'
        notes_html += '</div>'
        card_html += notes_html
    
    # Add insights section if requested
    if show_insights and is_current and 'insights' in item:
        insights = item.get('insights', {})
        if insights:
            insights_html = '<div style="margin-top: 15px; border-top: 1px solid rgba(0,0,0,0.1); padding-top: 10px;">'
            insights_html += '<div style="font-weight: bold; margin-bottom: 5px;">✨ Insights</div>'
            
            if 'description' in insights:
                insights_html += f'<div style="font-size: 0.9rem; margin-bottom: 5px;">{insights["description"]}</div>'
            
            if card_type == 'attraction' and 'highlights' in insights:
                insights_html += f'<div style="font-size: 0.9rem;"><b>Highlights:</b> {insights["highlights"]}</div>'
            
            if card_type == 'meal' and 'famous_dishes' in insights:
                insights_html += f'<div style="font-size: 0.9rem;"><b>Famous dishes:</b> {insights["famous_dishes"]}</div>'
            
            if 'fun_fact' in insights:
                insights_html += f'<div style="font-size: 0.9rem; margin-top: 5px;"><b>Fun fact:</b> {insights["fun_fact"]}</div>'
                
            insights_html += '</div>'
            card_html += insights_html
    
    # Close the main div
    card_html += "</div>"
    
    # Render with streamlit
    st.markdown(card_html, unsafe_allow_html=True)

def render_current_activity(item: Dict[str, Any], insights: Dict[str, Any] = None):
    """Render the current activity card with additional details"""
    if not item:
        st.info("No current activity found")
        return
    
    # Add insights to the item if provided
    if insights:
        item['insights'] = insights
    
    # Create columns for a better layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Current Activity")
        render_tour_card(item, is_current=True, show_insights=True)
    
    with col2:
        st.subheader("Quick Actions")
        
        # Actions button for this item
        st.button("📍 Navigate", key=f"nav_{item.get('id', 'current')}")
        st.button("✏️ Edit Details", key=f"edit_{item.get('id', 'current')}")
        
        # Type-specific actions
        if item.get('type') == 'meal':
            st.button("🍽️ See Menu", key="see_menu")
        elif item.get('type') == 'attraction':
            st.button("🎟️ Check Tickets", key="check_tickets")
        
        st.button("🔔 Set Reminder", key="set_reminder")

def render_next_activities(items: list, max_items: int = 3):
    """Render upcoming activities"""
    if not items:
        st.info("No upcoming activities found")
        return
    
    st.subheader("Coming Up Next")
    
    # Show only up to max_items
    for i, item in enumerate(items[:max_items]):
        render_tour_card(item, is_current=False)

def render_suggestion_card(suggestion: Dict[str, Any], key_prefix: str = "sugg"):
    """Render a suggestion card"""
    name = suggestion.get('name', 'Unknown place')
    desc = suggestion.get('description', '')
    place_type = suggestion.get('type', suggestion.get('cuisine', ''))
    price_range = suggestion.get('price_range', '')
    
    # Create a unique key for this suggestion
    key = f"{key_prefix}_{name.replace(' ', '_').lower()}"
    
    with st.container():
        # Card with light styling
        st.markdown(f"**{name}**")
        if place_type:
            st.markdown(f"*{place_type}*")
        st.markdown(desc)
        if price_range:
            st.markdown(f"Price: {price_range}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("➕ Add to Plan", key=f"add_{key}")
        with col2:
            st.button("📍 View on Map", key=f"map_{key}")
        
        st.markdown("---") 