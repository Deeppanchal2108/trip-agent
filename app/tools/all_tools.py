from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import json
import os
from langchain_community.utilities import GoogleSerperAPIWrapper

def get_llm():
    """Get LLM instance with proper error handling"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

def recommend_activities(state):
    try:
        preferences = state.get('preferences', {})
        itinerary = state.get('itinerary', '')
        
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_gemini_api_key_here":
            # Return mock data for testing
            destination = preferences.get('destination', 'Unknown')
            interests = preferences.get('interests', [])
            
            mock_activities = f"""
# Recommended Activities for {destination}

## Day 1 Activities
- Visit the main cultural landmarks
- Explore local markets and shopping districts
- Try traditional local cuisine

## Day 2 Activities
- Take a guided tour of historical sites
- Participate in local cultural workshops
- Enjoy evening entertainment and nightlife

## Day 3 Activities
- Outdoor adventure activities
- Relaxation and wellness experiences
- Sunset viewing at scenic locations

## Special Interests: {', '.join(interests)}
- Customized activities based on your interests
- Local expert recommendations
- Hidden gems and off-the-beaten-path experiences

*This is sample activity data. Add your actual Google API key for personalized recommendations.*
            """
            return {"activity_suggestions": mock_activities.strip()}
        
        prompt = f"""
        Based on the following preferences and itinerary, suggest unique local activities:
        Preferences: {json.dumps(preferences, indent=2)}
        Itinerary: {itinerary}

        Provide suggestions in bullet points for each day if possible.
        """
        
        llm = get_llm()
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"activity_suggestions": result.strip()}
    except Exception as e:
        print(f"Error in recommend_activities: {str(e)}")
        return {"activity_suggestions": "", "warning": str(e)}


def weather_forecaster(state):
    try:
        preferences = state.get('preferences', {})
        destination = preferences.get('destination', '')
        month = preferences.get('month', '')
        
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_gemini_api_key_here":
            # Return mock data for testing
            mock_weather = f"""
# Weather Forecast for {destination} - {month}

## Temperature
- Average High: 22°C (72°F)
- Average Low: 15°C (59°F)

## Precipitation
- Rainfall: Moderate
- Humidity: 65%

## Travel Advice
- Pack light layers for variable temperatures
- Bring an umbrella for occasional showers
- Best time for outdoor activities: Morning and late afternoon

*This is sample weather data. Add your actual Google API key for real-time weather information.*
            """
            return {"weather_forecast": mock_weather.strip()}
        
        prompt = f"""
        Based on the destination and month, provide a detailed weather forecast including 
        temperature, precipitation, and advice for travelers:

        Destination: {destination}
        Month: {month}
        """
        
        llm = get_llm()
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"weather_forecast": result.strip()}
    except Exception as e:
        print(f"Error in weather_forecaster: {str(e)}")
        return {"weather_forecast": "", "warning": str(e)}


def generate_itinerary(state):
    try:
        preferences = state.get('preferences', {})
        
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_gemini_api_key_here":
            # Return mock data for testing
            destination = preferences.get('destination', 'Unknown')
            month = preferences.get('month', 'Unknown')
            budget = preferences.get('budget_type', 'mid-range')
            
            mock_itinerary = f"""
# {destination} Travel Itinerary - {month}

## Day 1: Arrival & Orientation
- **Morning:** Arrive in {destination}, check into your {budget} accommodation
- **Afternoon:** Explore the city center and get oriented
- **Evening:** Enjoy local cuisine at a recommended restaurant

## Day 2: Cultural Exploration
- **Morning:** Visit main cultural attractions
- **Afternoon:** Local market exploration
- **Evening:** Traditional dinner experience

## Day 3: Adventure & Relaxation
- **Morning:** Outdoor activities or nature exploration
- **Afternoon:** Spa or relaxation time
- **Evening:** Sunset viewing and farewell dinner

*This is a sample itinerary. Add your actual Google API key to get AI-generated personalized recommendations.*
            """
            return {"itinerary": mock_itinerary.strip()}
        
        prompt = f"""
        Using the following preferences, create a detailed itinerary:
        {json.dumps(preferences, indent=2)}

        Include sections for each day, dining options, and downtime.
        """
        
        llm = get_llm()
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"itinerary": result.strip()}
    except Exception as e:
        print(f"Error in generate_itinerary: {str(e)}")
        return {"itinerary": "", "warning": str(e)}


def fetch_useful_links(state):
    try:
        # Read API key
        api_key = os.getenv("SERPER_API_KEY")

        # If no key, return mock data
        if not api_key or api_key.strip() == "":
            destination = state.get('preferences', {}).get('destination', 'Unknown')
            return {
                "useful_links": [
                    {"title": f"Complete Travel Guide to {destination}", "link": "https://example.com/travel-guide"},
                    {"title": f"Best Time to Visit {destination}", "link": "https://example.com/best-time"},
                    {"title": f"Local Culture and Customs in {destination}", "link": "https://example.com/culture"},
                    {"title": f"Food and Dining in {destination}", "link": "https://example.com/food"},
                    {"title": f"Transportation Guide for {destination}", "link": "https://example.com/transportation"}
                ]
            }

        # Build query safely
        preferences = state.get('preferences', {})
        destination = preferences.get('destination') or "your destination"
        month = preferences.get('month') or "your travel month"
        query = f"Travel tips and guides for {destination} in {month}"

        # IMPORTANT: GoogleSerperAPIWrapper uses env var SERPER_API_KEY
        search = GoogleSerperAPIWrapper()
        search_results = search.results(query)

        organic_results = search_results.get("organic", [])
        links = [
            {"title": result.get("title", "No title"), "link": result.get("link", "")}
            for result in organic_results[:5]
        ]
        return {"useful_links": links}

    except Exception as e:
        print(f"Error in fetch_useful_links: {str(e)}")
        return {"useful_links": [], "warning": f"Failed to fetch links: {str(e)}"}

        

def food_culture_recommender(state):
    try:
        preferences = state.get('preferences', {})
        destination = preferences.get('destination', '')
        budget_type = preferences.get('budget_type', 'mid-range')
        
        # Check if API key is available
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key or api_key == "your_google_gemini_api_key_here":
            # Return mock data for testing
            mock_food_culture = f"""
# Food & Culture Guide for {destination}

## Food & Dining
### Popular Local Dishes
- Traditional signature dishes
- Street food favorites
- Regional specialties

### Recommended Dining Options
- Fine dining restaurants for {budget_type} budget
- Local family-owned establishments
- Popular food markets and stalls

## Culture & Etiquette
### Cultural Norms
- Greeting customs and traditions
- Dress code expectations
- Social interaction guidelines

### Traveler Tips
- Language basics and useful phrases
- Tipping customs
- Photography etiquette
- Respectful behavior guidelines

*This is sample cultural information. Add your actual Google API key for detailed local insights.*
            """
            return {"food_culture_info": mock_food_culture.strip()}
        
        prompt = f"""
        For a trip to {destination} 
        with a {budget_type} budget:

        1. Suggest popular local dishes and recommended dining options.
        2. Provide important cultural norms, etiquette tips, and things travelers should be aware of.

        Format the response with clear sections for 'Food & Dining' and 'Culture & Etiquette'.
        """
        
        llm = get_llm()
        result = llm.invoke([HumanMessage(content=prompt)]).content
        return {"food_culture_info": result.strip()}
    except Exception as e:
        print(f"Error in food_culture_recommender: {str(e)}")
        return {"food_culture_info": "", "warning": str(e)}
