import streamlit as st
import datetime
import time
import threading
from typing import Dict, Any, List, Callable

# Store for scheduled notifications
notifications = []
notification_thread = None
stop_notification_thread = False

class Notification:
    """Class to represent a notification"""
    def __init__(self, title, message, scheduled_time=None, id=None):
        self.id = id or str(int(time.time()))
        self.title = title
        self.message = message
        self.scheduled_time = scheduled_time
        self.is_read = False
        self.created_at = datetime.datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'scheduled_time': self.scheduled_time,
            'is_read': self.is_read,
            'created_at': self.created_at
        }

def initialize_notifications():
    """Initialize notifications in session state"""
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'unread_count' not in st.session_state:
        st.session_state.unread_count = 0

def add_notification(title, message, scheduled_time=None):
    """Add a notification to the list"""
    initialize_notifications()
    notification = Notification(title, message, scheduled_time)
    st.session_state.notifications.append(notification.to_dict())
    st.session_state.unread_count += 1
    return notification.id

def mark_notification_as_read(notification_id):
    """Mark a notification as read"""
    initialize_notifications()
    for i, notification in enumerate(st.session_state.notifications):
        if notification['id'] == notification_id and not notification['is_read']:
            st.session_state.notifications[i]['is_read'] = True
            st.session_state.unread_count = max(0, st.session_state.unread_count - 1)
            break

def get_unread_count():
    """Get the number of unread notifications"""
    initialize_notifications()
    return st.session_state.unread_count

def get_all_notifications():
    """Get all notifications"""
    initialize_notifications()
    return st.session_state.notifications

def schedule_notification_for_next_item(itinerary_item: Dict[str, Any], advance_minutes: int = 15):
    """
    Schedule a notification for the next itinerary item
    
    Args:
        itinerary_item: The itinerary item to schedule notification for
        advance_minutes: How many minutes in advance to send the notification
    """
    if not itinerary_item or 'time' not in itinerary_item:
        return None
    
    # Parse the time from the itinerary item
    time_str = itinerary_item.get('time', '')
    try:
        if ' ' in time_str:  # Format like "10:30 AM"
            time_parts = time_str.split(' ')
            hour_min = time_parts[0].split(':')
            hour = int(hour_min[0])
            minute = int(hour_min[1])
            
            if time_parts[1].upper() == 'PM' and hour < 12:
                hour += 12
            elif time_parts[1].upper() == 'AM' and hour == 12:
                hour = 0
        else:  # Format like "10:30"
            hour_min = time_str.split(':')
            hour = int(hour_min[0])
            minute = int(hour_min[1])
        
        # Create datetime for the notification
        today = datetime.date.today()
        if itinerary_item.get('date'):
            notification_date = itinerary_item['date']
        else:
            notification_date = today
        
        notification_time = datetime.datetime.combine(
            notification_date, 
            datetime.time(hour=hour, minute=minute)
        )
        
        # Subtract advance_minutes
        notification_time = notification_time - datetime.timedelta(minutes=advance_minutes)
        
        # If the time is in the past, don't schedule
        if notification_time < datetime.datetime.now():
            return None
        
        # Create notification message
        activity = itinerary_item.get('activity', 'upcoming activity')
        location = itinerary_item.get('location', '')
        
        title = f"Upcoming: {activity}"
        message = f"Starting in {advance_minutes} minutes"
        if location:
            message += f" at {location}"
        
        # Add the notification
        return add_notification(title, message, scheduled_time=notification_time)
    
    except Exception as e:
        print(f"Error scheduling notification: {e}")
        return None

def display_notification_bell():
    """Display the notification bell icon in the app"""
    initialize_notifications()
    unread_count = get_unread_count()
    
    if unread_count > 0:
        st.markdown(
            f"""
            <div style="position: fixed; top: 0.5rem; right: 2rem; z-index: 1000;">
                <span style="position: relative;">
                    <span style="font-size: 1.8rem; cursor: pointer;">🔔</span>
                    <span style="position: absolute; top: -0.7rem; right: -0.7rem; background-color: red; color: white; 
                           border-radius: 50%; width: 1.2rem; height: 1.2rem; display: flex; align-items: center; 
                           justify-content: center; font-size: 0.7rem; font-weight: bold;">{unread_count}</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="position: fixed; top: 0.5rem; right: 2rem; z-index: 1000;">
                <span style="font-size: 1.8rem; cursor: pointer;">🔔</span>
            </div>
            """,
            unsafe_allow_html=True
        )

def notification_worker(callback: Callable = None):
    """Background worker to check for scheduled notifications"""
    global stop_notification_thread
    
    while not stop_notification_thread:
        now = datetime.datetime.now()
        
        # In a real app, this would access a database or other persistent storage
        if 'notifications' in st.session_state:
            for notification in st.session_state.notifications:
                if (notification.get('scheduled_time') and 
                    notification.get('scheduled_time') <= now and 
                    not notification.get('is_read')):
                    # Mark as triggered
                    notification['is_triggered'] = True
                    
                    # Call callback if provided
                    if callback:
                        callback(notification)
        
        # Sleep for 1 minute
        time.sleep(60)

def start_notification_thread(callback: Callable = None):
    """Start the background notification thread"""
    global notification_thread, stop_notification_thread
    
    if notification_thread is None or not notification_thread.is_alive():
        stop_notification_thread = False
        notification_thread = threading.Thread(
            target=notification_worker,
            args=(callback,),
            daemon=True
        )
        notification_thread.start()

def stop_notification_thread():
    """Stop the background notification thread"""
    global stop_notification_thread
    stop_notification_thread = True 