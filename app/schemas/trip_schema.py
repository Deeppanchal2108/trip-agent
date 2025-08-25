from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class TripPreferences(BaseModel):
    destination: str
    month: str
    budget_type: str = "mid-range"  # low, mid-range, luxury
    travel_style: str = "cultural"  # adventure, relaxation, cultural
    interests: List[str] = []

class TripRequest(BaseModel):
    preferences: TripPreferences

class TripResponse(BaseModel):
    itinerary: str
    weather_forecast: str
    activity_suggestions: str
    useful_links: List[Dict[str, str]]
    food_culture_info: str
    status: str = "success"
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[str] = None
