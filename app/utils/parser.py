import re
import datetime
from typing import List, Dict, Any

def parse_tour_agenda(text: str) -> List[Dict[str, Any]]:
    """
    Parse a raw text tour agenda into structured data.
    
    Args:
        text: Raw text containing tour agenda
        
    Returns:
        List of dictionaries with structured tour itinerary items
    """
    # Initialize the itinerary list
    itinerary = []
    
    # Split the text into lines
    lines = text.strip().split('\n')
    
    # Regular expressions for different patterns
    time_pattern = r'(\d{1,2}:\d{2}\s*(AM|PM|am|pm)?)'
    date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})'
    duration_pattern = r'(\d+)\s*(hour|hr|hrs|h|min|minute|minutes)'
    location_pattern = r'at\s+([^\.,]+)'
    
    current_item = {}
    current_date = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check if this is a new date
        date_match = re.search(date_pattern, line)
        if date_match and (len(line) < 30 or line.lower().startswith(('day', 'date'))):
            try:
                date_str = date_match.group(1)
                # Try to parse the date
                if '/' in date_str:
                    parts = date_str.split('/')
                else:
                    parts = date_str.split('-')
                
                if len(parts) == 3:
                    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
                    if year < 100:  # Handle two-digit years
                        year += 2000
                    current_date = datetime.date(year, month, day)
                continue
            except:
                # If date parsing fails, just continue
                pass
        
        # Start a new item if we detect a time
        time_match = re.search(time_pattern, line)
        if time_match:
            # If we have a previous item, save it
            if current_item and 'activity' in current_item:
                itinerary.append(current_item)
            
            # Start a new item
            current_item = {'date': current_date}
            
            # Extract time
            time_str = time_match.group(1)
            current_item['time'] = time_str
            
            # Extract activity (everything after the time)
            activity_text = line[time_match.end():].strip()
            if activity_text:
                # Remove leading dash or colon
                activity_text = re.sub(r'^[-:]\s*', '', activity_text)
                current_item['activity'] = activity_text
            else:
                current_item['activity'] = "Unknown activity"
        
        # If we're in a current item, try to extract more details
        elif current_item:
            # Try to extract location
            location_match = re.search(location_pattern, line)
            if location_match:
                current_item['location'] = location_match.group(1).strip()
            
            # Try to extract duration
            duration_match = re.search(duration_pattern, line)
            if duration_match:
                amount = duration_match.group(1)
                unit = duration_match.group(2)
                if unit.startswith(('min', 'minute')):
                    duration_minutes = int(amount)
                else:  # hours
                    duration_minutes = int(amount) * 60
                
                current_item['duration_minutes'] = duration_minutes
            
            # If no specific detail was found, append to notes
            if not (location_match or duration_match):
                if 'notes' not in current_item:
                    current_item['notes'] = []
                current_item['notes'].append(line)
        
        # If we don't have a current item yet, this might be a header or other info
        else:
            continue
    
    # Add the last item if it exists
    if current_item and 'activity' in current_item:
        itinerary.append(current_item)
    
    # Infer types of activities
    for item in itinerary:
        activity = item['activity'].lower()
        
        if any(word in activity for word in ['breakfast', 'lunch', 'dinner', 'meal', 'eat']):
            item['type'] = 'meal'
        elif any(word in activity for word in ['museum', 'gallery', 'visit', 'tour', 'monument', 'attraction']):
            item['type'] = 'attraction'
        elif any(word in activity for word in ['hotel', 'check-in', 'check-out', 'accommodation', 'room']):
            item['type'] = 'accommodation'
        elif any(word in activity for word in ['transport', 'bus', 'train', 'flight', 'drive', 'taxi']):
            item['type'] = 'transportation'
        else:
            item['type'] = 'other'
    
    return itinerary

def generate_next_items(itinerary: List[Dict[str, Any]], current_index: int, count: int = 3) -> List[Dict[str, Any]]:
    """Get the next few items from the itinerary after the current one"""
    if current_index < 0 or current_index >= len(itinerary):
        return []
    
    end_index = min(current_index + count + 1, len(itinerary))
    return itinerary[current_index+1:end_index]

def find_current_item(itinerary: List[Dict[str, Any]]) -> int:
    """Find the current item in the itinerary based on current time"""
    now = datetime.datetime.now()
    current_date = now.date()
    current_time = now.strftime("%-I:%M %p")
    
    # First, find items for today
    today_items = [i for i, item in enumerate(itinerary) 
                   if item.get('date') == current_date]
    
    if not today_items:
        # If no items for today, return the first item
        return 0
    
    # Find the current or next activity
    for idx in today_items:
        item_time = itinerary[idx].get('time', '')
        # Compare times (simple string comparison works if format is consistent)
        if item_time > current_time:
            # Return the previous item if not the first
            return max(0, idx - 1)
    
    # If we're past all activities for today, return the last one
    return today_items[-1] 