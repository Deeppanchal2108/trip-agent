# Fix 1: Update your trip_agent.py with proper state management

from langgraph.graph import StateGraph, END
from typing import Dict, Any, TypedDict
from IPython.display import Image, display
from app.tools.all_tools import (
    recommend_activities,
    weather_forecaster,
    generate_itinerary,
    fetch_useful_links,
    food_culture_recommender,
)

class TripState(TypedDict):
    """
    Trip state holds all the data throughout the workflow
    """
    preferences: Dict[str, Any]
    itinerary: str
    weather_forecast: str
    activity_suggestions: str
    useful_links: list
    food_culture_info: str


def node_generate_itinerary(state: TripState) -> Dict[str, Any]:
    """Generate itinerary and return state update"""
    print("DEBUG: Running node_generate_itinerary")
    result = generate_itinerary(state)
    print(f"DEBUG: generate_itinerary returned: {result}")
    
    # Return the state update - this is crucial!
    return {
        "itinerary": result.get("itinerary", ""),
        # Keep existing state
        **{k: v for k, v in state.items() if k != "itinerary"}
    }

def node_weather(state: TripState) -> Dict[str, Any]:
    """Get weather forecast and return state update"""
    print("DEBUG: Running node_weather")
    result = weather_forecaster(state)
    print(f"DEBUG: weather_forecaster returned: {result}")
    
    return {
        "weather_forecast": result.get("weather_forecast", ""),
        **{k: v for k, v in state.items() if k != "weather_forecast"}
    }

def node_activities(state: TripState) -> Dict[str, Any]:
    """Get activity suggestions and return state update"""
    print("DEBUG: Running node_activities")
    result = recommend_activities(state)
    print(f"DEBUG: recommend_activities returned: {result}")
    
    return {
        "activity_suggestions": result.get("activity_suggestions", ""),
        **{k: v for k, v in state.items() if k != "activity_suggestions"}
    }

def node_links(state: TripState) -> Dict[str, Any]:
    """Fetch useful links and return state update"""
    print("DEBUG: Running node_links")
    result = fetch_useful_links(state)
    print(f"DEBUG: fetch_useful_links returned: {result}")
    
    return {
        "useful_links": result.get("useful_links", []),
        **{k: v for k, v in state.items() if k != "useful_links"}
    }

def node_food(state: TripState) -> Dict[str, Any]:
    """Get food culture info and return state update"""
    print("DEBUG: Running node_food")
    result = food_culture_recommender(state)
    print(f"DEBUG: food_culture_recommender returned: {result}")
    
    return {
        "food_culture_info": result.get("food_culture_info", ""),
        **{k: v for k, v in state.items() if k != "food_culture_info"}
    }

# ---- Build the graph ----
workflow = StateGraph(TripState)

# Add nodes
workflow.add_node("generate_itinerary", node_generate_itinerary)
workflow.add_node("weather", node_weather)
workflow.add_node("activities", node_activities)
workflow.add_node("links", node_links)
workflow.add_node("food", node_food)

# Set entry point
workflow.set_entry_point("generate_itinerary")

# Chain execution
workflow.add_edge("generate_itinerary", "weather")
workflow.add_edge("weather", "activities")
workflow.add_edge("activities", "links")
workflow.add_edge("links", "food")
workflow.add_edge("food", END)

# Compile agent
trip_agent = workflow.compile()

display(Image(trip_agent.get_graph().draw_mermaid_png()))


# ---- Test runner with better debugging ----
if __name__ == "__main__":
    user_state = {
        "preferences": {
            "destination": "Tokyo",
            "month": "April",
            "budget_type": "mid-range",
            "travelStyle": "cultural",
            "interests": ["temples", "food", "anime"]
        },
        "itinerary": "",
        "weather_forecast": "",
        "activity_suggestions": "",
        "useful_links": [],
        "food_culture_info": ""
    }
    
    print("DEBUG: Starting agent with state:", user_state)
    result = trip_agent.invoke(user_state)
    print("DEBUG: Final result:", result)
    print("\n---- Final Trip Plan ----\n")
    if result:
        for key, value in result.items():
            print(f"{key}: {value[:100]}..." if isinstance(value, str) and len(value) > 100 else f"{key}: {value}")
    else:
        print("ERROR: Agent returned None!")