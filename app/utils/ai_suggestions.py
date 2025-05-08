import streamlit as st
import google.generativeai as genai
from typing import Dict, Any, List

# Configure the Gemini API
def configure_genai():
    """Configure the Gemini API with API key from session_state"""
    api_key = st.session_state.get("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
    else:
        raise ValueError("GEMINI_API_KEY is not set. Please enter it in the setup page.")

def get_place_insights(location: str, activity_type: str = None) -> Dict[str, Any]:
    """
    Get insights about a location using Gemini API
    
    Args:
        location: Name of the location
        activity_type: Type of activity (e.g., meal, attraction, etc.)
        
    Returns:
        Dictionary with insights about the place
    """
    try:
        configure_genai()
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create prompt based on activity type
        if activity_type == 'meal':
            prompt = f"""
            Provide insights about {location} as a dining destination:
            1. Brief description (2-3 sentences)
            2. Famous dishes or cuisine style
            3. Best time to visit
            4. One interesting fact
            Format as JSON with keys: description, famous_dishes, best_time, fun_fact
            """
        elif activity_type == 'attraction':
            prompt = f"""
            Provide insights about {location} as a tourist attraction:
            1. Brief description (2-3 sentences)
            2. Main highlights or features
            3. Recommended time to spend there
            4. One interesting fact
            Format as JSON with keys: description, highlights, recommended_time, fun_fact
            """
        else:
            prompt = f"""
            Provide concise insights about {location}:
            1. Brief description (2-3 sentences)
            2. Key features or attractions
            3. One interesting fact
            Format as JSON with keys: description, key_features, fun_fact
            """
        
        response = model.generate_content(prompt)
        
        # Parse the response to extract JSON
        response_text = response.text
        
        # Simple processing to extract JSON - in a real app, use a more robust method
        import json
        import re
        
        # Find JSON content using regex
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            # Fallback to a simple structure if JSON extraction fails
            return {
                "description": response_text[:200] + "...",
                "error": "Could not parse structured data"
            }
            
    except Exception as e:
        return {
            "error": str(e),
            "description": f"Failed to get insights for {location}"
        }

def get_nearby_suggestions(location: str, activity_type: str = None) -> List[Dict[str, Any]]:
    """
    Get suggestions for nearby places based on current location and activity type
    
    Args:
        location: Current location
        activity_type: Type of suggestion needed (meal, attraction, etc.)
        
    Returns:
        List of dictionaries with suggestions
    """
    try:
        configure_genai()
        model = genai.GenerativeModel('gemini-1.5-pro')
        
        # Create prompt based on activity type
        if activity_type == 'meal':
            prompt = f"""
            Suggest 3 good restaurants or cafes near {location}:
            1. Name
            2. Cuisine type
            3. Brief description (1-2 sentences)
            4. Estimated price range ($, $$, $$$)
            Format as JSON array with objects containing keys: name, cuisine, description, price_range
            """
        elif activity_type == 'attraction':
            prompt = f"""
            Suggest 3 interesting attractions or places to visit near {location}:
            1. Name
            2. Type of attraction
            3. Brief description (1-2 sentences)
            4. Estimated time needed to visit
            Format as JSON array with objects containing keys: name, type, description, estimated_time
            """
        else:
            prompt = f"""
            Suggest 3 interesting places to check out near {location}:
            1. Name
            2. Type of place
            3. Brief description (1-2 sentences)
            Format as JSON array with objects containing keys: name, type, description
            """
        
        response = model.generate_content(prompt)
        
        # Process response to extract JSON
        import json
        import re
        
        response_text = response.text
        
        # Find JSON array using regex
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
        else:
            # Fallback to simple structure
            return [{
                "name": "Error retrieving suggestions",
                "description": "Could not parse structured data from AI response"
            }]
            
    except Exception as e:
        return [{
            "name": "Error",
            "description": f"Failed to get suggestions: {str(e)}"
        }]

def get_meal_suggestions(location: str, meal_type: str) -> List[Dict[str, Any]]:
    """
    Get meal suggestions for breakfast, lunch or dinner near a location
    
    Args:
        location: Current location
        meal_type: Type of meal (breakfast, lunch, dinner)
        
    Returns:
        List of dictionaries with meal suggestions
    """
    return get_nearby_suggestions(location, 'meal') 