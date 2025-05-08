import streamlit as st
from typing import Dict, Any
from datetime import datetime

# Define card colors based on activity type - using more subtle, premium colors
CARD_COLORS = {
    'meal': '#FEF9C3',         # Subtle yellow
    'attraction': '#E0F2FE',    # Subtle blue
    'accommodation': '#DCFCE7', # Subtle green
    'transportation': '#F3E8FF', # Subtle purple
    'other': '#F1F5F9'          # Subtle gray
}

# Define card icons for each type
CARD_ICONS = {
    'meal': '🍽️',
    'attraction': '🏛️',
    'accommodation': '🏨',
    'transportation': '🚆',
    'other': '📌'
}

def render_tour_card(item: Dict[str, Any], is_current: bool = False, show_insights: bool = False):
    """
    Render a tour item as a premium card
    
    Args:
        item: Tour item dictionary
        is_current: Whether this is the current item
        show_insights: Whether to show AI insights
    """
    # Get card color and icon based on activity type
    card_type = item.get('type', 'other')
    card_color = CARD_COLORS.get(card_type, CARD_COLORS['other'])
    card_icon = CARD_ICONS.get(card_type, CARD_ICONS['other'])
    
    # Add extra styling for current item
    border_style = "border-left: 4px solid #3b82f6;" if is_current else ""
    shadow_style = "box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);" if is_current else "box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);"
    
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
    
    # Card HTML with premium design
    card_html = f"""
    <div style="background-color: {card_color}; border-radius: 0.5rem; padding: 1.25rem; margin-bottom: 1rem; 
                {border_style} {shadow_style} transition: transform 0.2s ease, box-shadow 0.2s ease;"
         onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(0, 0, 0, 0.1)';" 
         onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='{shadow_style.replace('style=', '').replace('\"', '')}'" 
         onclick="this.style.transform='scale(0.98)'; setTimeout(() => this.style.transform='translateY(0)', 100);">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center;">
                <div style="background-color: white; width: 2rem; height: 2rem; border-radius: 0.375rem; 
                            display: flex; align-items: center; justify-content: center; margin-right: 0.75rem;">
                    <span style="font-size: 1rem;">{card_icon}</span>
                </div>
                <div style="font-weight: 600; font-size: 1.1rem; color: #0f172a;">{time_str}</div>
            </div>
            <div style="font-size: 0.85rem; color: #64748b; background-color: white; 
                        padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-weight: 500;">
                {duration_str if duration_str else "Duration unknown"}
            </div>
        </div>
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; color: #1e293b;">{activity}</div>
    """
    
    # Add location if available
    if location:
        card_html += f"""
        <div style="display: flex; align-items: center; font-size: 0.9rem; color: #4b5563; margin-bottom: 0.5rem;">
            <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" 
                 stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
                 style="margin-right: 0.375rem;">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                <circle cx="12" cy="10" r="3"></circle>
            </svg>
            {location}
        </div>
        """
    
    # Add notes if available
    notes = item.get('notes', [])
    if notes:
        card_html += '<div style="margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid rgba(0,0,0,0.05);">'
        card_html += '<div style="font-size: 0.85rem; font-weight: 600; margin-bottom: 0.375rem; color: #4b5563;">Notes:</div>'
        card_html += '<ul style="margin: 0; padding-left: 1.25rem; font-size: 0.85rem; color: #4b5563;">'
        for note in notes:
            card_html += f'<li style="margin-bottom: 0.25rem;">{note}</li>'
        card_html += '</ul></div>'
    
    # Add insights section if requested
    if show_insights and is_current and 'insights' in item:
        insights = item.get('insights', {})
        if insights:
            card_html += f"""
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" 
                         stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" 
                         style="margin-right: 0.375rem;">
                        <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                    </svg>
                    <div style="font-size: 0.95rem; font-weight: 600; color: #3b82f6;">AI Insights</div>
                </div>
            """
            
            if 'description' in insights:
                card_html += f'<div style="font-size: 0.9rem; margin-bottom: 0.75rem; color: #4b5563;">{insights["description"]}</div>'
            
            if card_type == 'attraction' and 'highlights' in insights:
                card_html += f"""
                <div style="font-size: 0.85rem; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600; color: #1e293b;">Highlights:</span> 
                    <span style="color: #4b5563;">{insights["highlights"]}</span>
                </div>
                """
            
            if card_type == 'meal' and 'famous_dishes' in insights:
                card_html += f"""
                <div style="font-size: 0.85rem; margin-bottom: 0.5rem;">
                    <span style="font-weight: 600; color: #1e293b;">Famous dishes:</span> 
                    <span style="color: #4b5563;">{insights["famous_dishes"]}</span>
                </div>
                """
            
            if 'fun_fact' in insights:
                card_html += f"""
                <div style="background-color: white; border-radius: 0.375rem; padding: 0.75rem; margin-top: 0.75rem; 
                            font-size: 0.85rem; color: #4b5563;">
                    <span style="font-weight: 600; color: #1e293b;">Fun fact:</span> {insights["fun_fact"]}
                </div>
                """
                
            card_html += '</div>'
    
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
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("""
            <h2 style="font-size: 1.5rem; color: #0f172a; margin-bottom: 1rem; display: flex; align-items: center;">
                <span style="background-color: #3b82f6; color: white; width: 2rem; height: 2rem; 
                       border-radius: 0.375rem; display: inline-flex; align-items: center; 
                       justify-content: center; margin-right: 0.75rem; font-size: 1rem;">⏱️</span>
                Current Activity
            </h2>
        """, unsafe_allow_html=True)
        render_tour_card(item, is_current=True, show_insights=True)
    
    with col2:
        st.markdown("""
            <h2 style="font-size: 1.25rem; color: #0f172a; margin-bottom: 1rem;">
                Quick Actions
            </h2>
        """, unsafe_allow_html=True)
        
        # Card container for actions
        st.markdown("""
            <div style="background-color: white; border-radius: 0.5rem; 
                 box-shadow: 0 1px 3px rgba(0,0,0,0.1); padding: 1rem;">
        """, unsafe_allow_html=True)
        
        # Actions button for this item with icons and better styling
        if st.button("🗺️ Navigate", key=f"nav_{item.get('id', 'current')}", use_container_width=True):
            pass
            
        if st.button("✏️ Edit Details", key=f"edit_{item.get('id', 'current')}", use_container_width=True):
            pass
        
        # Type-specific actions
        if item.get('type') == 'meal':
            if st.button("🍽️ See Menu", key="see_menu", use_container_width=True):
                pass
        elif item.get('type') == 'attraction':
            if st.button("🎟️ Check Tickets", key="check_tickets", use_container_width=True):
                pass
        
        if st.button("🔔 Set Reminder", key="set_reminder", use_container_width=True):
            pass
            
        st.markdown("</div>", unsafe_allow_html=True)

def render_next_activities(items: list, max_items: int = 3):
    """Render upcoming activities"""
    if not items:
        st.markdown("""
            <div style="background-color: #f8fafc; border-radius: 0.5rem; padding: 1.5rem; 
                 text-align: center; border: 1px dashed #cbd5e1;">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" 
                     stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <p style="color: #64748b; margin-top: 0.5rem;">No upcoming activities found</p>
            </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown("""
        <h2 style="font-size: 1.5rem; color: #0f172a; margin-bottom: 1rem; display: flex; align-items: center;">
            <span style="background-color: #3b82f6; color: white; width: 2rem; height: 2rem; 
                   border-radius: 0.375rem; display: inline-flex; align-items: center; 
                   justify-content: center; margin-right: 0.75rem; font-size: 1rem;">📋</span>
            Coming Up Next
        </h2>
    """, unsafe_allow_html=True)
    
    # Show only up to max_items
    for i, item in enumerate(items[:max_items]):
        render_tour_card(item, is_current=False)

def render_suggestion_card(suggestion: Dict[str, Any], key_prefix: str = "sugg"):
    """Render a suggestion card with premium styling"""
    name = suggestion.get('name', 'Unknown place')
    desc = suggestion.get('description', '')
    place_type = suggestion.get('type', suggestion.get('cuisine', ''))
    price_range = suggestion.get('price_range', '')
    
    # Create a unique key for this suggestion
    key = f"{key_prefix}_{name.replace(' ', '_').lower()}"
    
    # Premium styled card
    st.markdown(f"""
        <div style="background-color: white; border-radius: 0.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
                    padding: 1.25rem; margin-bottom: 1rem; transition: transform 0.2s ease, box-shadow 0.2s ease;"
             onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 6px 16px rgba(0, 0, 0, 0.1)';" 
             onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)';">
            <div style="font-size: 1.1rem; font-weight: 600; color: #0f172a; margin-bottom: 0.5rem;">{name}</div>
    """, unsafe_allow_html=True)
    
    if place_type:
        st.markdown(f"""
            <div style="display: inline-block; background-color: #f1f5f9; padding: 0.25rem 0.5rem; 
                        border-radius: 0.25rem; font-size: 0.8rem; color: #4b5563; margin-bottom: 0.75rem;">
                {place_type}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"""
        <div style="font-size: 0.9rem; color: #4b5563; margin-bottom: 0.75rem;">{desc}</div>
    """, unsafe_allow_html=True)
    
    if price_range:
        st.markdown(f"""
            <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 1rem;">
                <span style="font-weight: 500;">Price:</span> {price_range}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add to Plan", key=f"add_{key}", use_container_width=True):
            pass
    with col2:
        if st.button("🗺️ View on Map", key=f"map_{key}", use_container_width=True):
            pass 