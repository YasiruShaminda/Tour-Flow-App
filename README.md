# Tour Flow App

A Streamlit application that helps travelers visualize and manage their tour itinerary with AI-powered insights and suggestions.

## Key Features

- **Tour Agenda Visualization**: Upload your tour agenda as a text file and view it as an interactive flow chart
- **AI-Powered Insights**: Get AI-generated insights about attractions, restaurants, and places you're visiting
- **Smart Suggestions**: Receive suggestions for nearby attractions, restaurants, and activities
- **Meal Time Reminders**: Get notifications for meal times with restaurant suggestions
- **Push Notifications**: Receive timely reminders for your tour activities
- **Customizable Flow**: Add, remove, or modify items in your tour plan
- **Google Sign-in**: Sign in with your Google account for personalized recommendations

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/tour-flow-app.git
cd tour-flow-app
```

2. Create a virtual environment (optional but recommended):
```
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `env.example` to `.env`
   - Add your Google and Gemini API credentials

5. Run the application:
```
streamlit run app/main.py
```

## Usage

1. Sign in with your Google account or use the demo login
2. Upload your tour agenda (see sample_agenda.txt for format reference)
3. View your tour flow visualization
4. Explore suggestions based on your location and activities
5. Customize your agenda as needed

## Sample Agenda Format

The app can parse tour agenda text files. For best results, include:
- Dates in MM/DD/YYYY format
- Times in HH:MM AM/PM format
- Activity locations starting with "at" (e.g., "at 123 Main St")
- Duration information (e.g., "Duration: 2 hours")

See `sample_agenda.txt` for an example.

## API Keys Required

To use all features, you'll need:
- Google OAuth credentials (for Google Sign-in)
- Gemini API key (for AI-powered suggestions)

## Dependencies

- Streamlit for the web interface
- Google Auth libraries for authentication
- Google Generative AI for AI-powered insights
- Pandas for data handling
- Python-dotenv for environment variable management

## Development

The project structure follows this organization:
- `app/` - Main application code
  - `components/` - Reusable UI components
  - `utils/` - Utility functions
  - `pages/` - Application pages
  - `assets/` - Static assets
- `requirements.txt` - Dependencies

## License

This project is licensed under the MIT License - see the LICENSE file for details. 