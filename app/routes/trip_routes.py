from fastapi import APIRouter, HTTPException
from app.schemas.trip_schema import TripRequest, TripResponse, ErrorResponse
from app.agents.trip_agent import trip_agent
import os
import traceback

router = APIRouter(prefix="/trip", tags=["trip"])

@router.post("/generate", response_model=TripResponse)
async def generate_trip_plan(request: TripRequest):
    """
    Generate a complete trip plan using AI agent
    """
    try:
        # Remove the strict API key validation - let tools handle mock data
        # if not os.getenv("GOOGLE_API_KEY"):
        #     raise HTTPException(status_code=500, detail="Google API key not configured")
        # if not os.getenv("SERPER_API_KEY"):
        #     raise HTTPException(status_code=500, detail="Serper API key not configured")
        
        # Prepare COMPLETE initial state for the agent
        user_state = {
            "preferences": {
                "destination": request.preferences.destination,
                "month": request.preferences.month,
                "budget_type": request.preferences.budget_type,
                "travelStyle": request.preferences.travel_style,
                "interests": request.preferences.interests
            },
            # Initialize ALL required state fields
            "itinerary": "",
            "weather_forecast": "",
            "activity_suggestions": "",
            "useful_links": [],
            "food_culture_info": ""
        }
        
        print(f"DEBUG - Initial user state: {user_state}")
        
        # Run the agent with error handling
        try:
            result = trip_agent.invoke(user_state)
            print(f"DEBUG - Agent result type: {type(result)}")
            print(f"DEBUG - Agent result: {result}")
        except Exception as agent_error:
            print(f"DEBUG - Agent execution error: {str(agent_error)}")
            print(f"DEBUG - Agent traceback: {traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"Agent execution failed: {str(agent_error)}"
            )
        
        # Handle case where result might be None
        if result is None:
            print("ERROR - Agent returned None result")
            raise HTTPException(
                status_code=500,
                detail="Agent returned None result. Check agent configuration and tool implementations."
            )
        
        # Validate result has expected keys
        expected_keys = ["itinerary", "weather_forecast", "activity_suggestions", "useful_links", "food_culture_info"]
        missing_keys = [key for key in expected_keys if key not in result]
        if missing_keys:
            print(f"WARNING - Missing keys in result: {missing_keys}")
        
        # Return the response with safe defaults
        return TripResponse(
            itinerary=result.get("itinerary", "No itinerary generated"),
            weather_forecast=result.get("weather_forecast", "No weather forecast available"),
            activity_suggestions=result.get("activity_suggestions", "No activity suggestions available"),
            useful_links=result.get("useful_links", []),
            food_culture_info=result.get("food_culture_info", "No food/culture info available"),
            message="Trip plan generated successfully!"
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"ERROR - Unexpected error: {str(e)}")
        print(f"ERROR - Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate trip plan: {str(e)}"
        )

@router.get("/health")
async def trip_health_check():
    """Health check for trip service"""
    return {
        "status": "healthy",
        "service": "trip-agent",
        "message": "Trip agent is running"
    }

@router.get("/config")
async def get_config():
    """Get configuration status (don't expose actual API keys)"""
    return {
        "google_api_configured": bool(os.getenv("GOOGLE_API_KEY")),
        "serper_api_configured": bool(os.getenv("SERPER_API_KEY")),
        "status": "ready" if os.getenv("GOOGLE_API_KEY") and os.getenv("SERPER_API_KEY") else "mock_data_mode"
    }

@router.post("/debug-agent")
async def debug_agent():
    """Debug endpoint to test the agent step by step"""
    try:
        # Test with minimal state
        test_state = {
            "preferences": {
                "destination": "Tokyo",
                "month": "April",
                "budget_type": "mid-range",
                "travelStyle": "cultural",
                "interests": ["temples"]
            },
            "itinerary": "",
            "weather_forecast": "",
            "activity_suggestions": "",
            "useful_links": [],
            "food_culture_info": ""
        }
        
        print("DEBUG - Testing agent with state:", test_state)
        
        # Test individual tools first
        from app.tools.all_tools import generate_itinerary, weather_forecaster
        
        print("DEBUG - Testing generate_itinerary tool...")
        itinerary_result = generate_itinerary(test_state)
        print(f"DEBUG - Itinerary tool result: {itinerary_result}")
        
        print("DEBUG - Testing weather_forecaster tool...")
        weather_result = weather_forecaster(test_state)
        print(f"DEBUG - Weather tool result: {weather_result}")
        
        # Now test the full agent
        print("DEBUG - Testing full agent...")
        agent_result = trip_agent.invoke(test_state)
        print(f"DEBUG - Full agent result: {agent_result}")
        
        return {
            "individual_tools": {
                "itinerary": itinerary_result,
                "weather": weather_result
            },
            "full_agent": agent_result,
            "success": agent_result is not None
        }
        
    except Exception as e:
        print(f"DEBUG ERROR: {str(e)}")
        print(f"DEBUG TRACEBACK: {traceback.format_exc()}")
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "success": False
        }