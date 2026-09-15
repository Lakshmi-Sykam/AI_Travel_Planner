from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class TripRequest(BaseModel):
    origin: str = Field(..., description="Starting city / origin", example="Mumbai")
    destination: str = Field(..., description="Destination city or region", example="Goa")
    duration_days: int = Field(..., ge=1, le=30, description="Duration of the trip in days", example=4)
    budget: float = Field(..., gt=0, description="Total budget for the trip", example=20000)
    currency: str = Field(default="INR", description="Currency code (e.g. INR, USD, EUR)", example="INR")
    travel_style: str = Field(default="Budget/Backpacker", description="Travel style: Backpacker, Budget, Moderate, Luxury, Solo, Family, Romantic")
    interests: List[str] = Field(default=["Beaches", "Food", "Sightseeing"], description="List of traveler interests")
    group_size: int = Field(default=1, ge=1, description="Number of travelers")
    preferred_transport: Optional[str] = Field(default="Any / Best AI Match", description="Preferred transit mode: Any / Best AI Match, Flight / Airplane, Train / Railway, Car / Self-Drive / Cab, Bus / Coach")
    special_requirements: Optional[str] = Field(default=None, description="Dietary, mobility, or other custom notes")

class ModifyTripRequest(BaseModel):
    trip_id: str = Field(..., description="ID of the trip to modify")
    modification_prompt: str = Field(..., description="Requested change, e.g., 'Make it more relaxing and add sunset cruise on day 2'")
    current_itinerary: Optional[Dict[str, Any]] = None

class TransportOption(BaseModel):
    mode: str = Field(..., description="Flight, Train, Bus, Road/Cab, Ferry")
    provider_or_route: str = Field(..., description="Route name, airline or train name")
    estimated_cost: float = Field(..., description="Estimated cost per person")
    duration_hours: float = Field(..., description="Estimated travel time in hours")
    departure_tips: Optional[str] = None
    booking_tips: Optional[str] = None

class HotelOption(BaseModel):
    name: str = Field(..., description="Name or type of accommodation")
    area_or_neighborhood: str = Field(..., description="Location/neighborhood in destination")
    price_per_night: float = Field(..., description="Cost per night")
    total_cost: float = Field(..., description="Total stay cost for trip duration")
    amenities: List[str] = Field(default_factory=list)
    rating_approx: Optional[float] = 4.2
    why_recommended: str = Field(..., description="Why this fits the user's budget & style")

class ActivityItem(BaseModel):
    time_slot: str = Field(..., description="Morning / Afternoon / Evening / Night")
    title: str = Field(..., description="Name of place or activity")
    description: str = Field(..., description="Detailed activity description")
    cost: float = Field(default=0.0, description="Estimated entrance fee or activity cost")
    location: Optional[str] = None
    tips: Optional[str] = None

class DayPlan(BaseModel):
    day: int = Field(..., description="Day number (1, 2, ...)")
    theme: str = Field(..., description="Theme for the day, e.g., North Goa Coastal Exploration")
    activities: List[ActivityItem] = Field(default_factory=list)
    food_recommendations: List[str] = Field(default_factory=list, description="Recommended restaurants or local dishes")
    day_budget_estimate: float = Field(..., description="Estimated expense for this day")

class BudgetBreakdown(BaseModel):
    transportation: float = Field(..., description="Total transport & transit cost")
    accommodation: float = Field(..., description="Total hotel/stay cost")
    food_and_dining: float = Field(..., description="Estimated food and beverage cost")
    activities_and_entry: float = Field(..., description="Sightseeing, permits and activities")
    emergency_buffer: float = Field(..., description="Contingency buffer")
    total_estimated_cost: float = Field(..., description="Total cost sum")
    currency: str = Field(default="INR")
    is_within_budget: bool = True
    budget_advice: str = Field(..., description="Tips to save money or optimize spending")

class TripItinerary(BaseModel):
    destination_overview: str = Field(..., description="Summary of the destination, climate and vibes")
    best_time_to_visit: str = Field(...)
    weather_forecast_summary: str = Field(...)
    transport_options: List[TransportOption] = Field(default_factory=list)
    hotel_options: List[HotelOption] = Field(default_factory=list)
    selected_hotel_recommendation: Optional[HotelOption] = None
    daily_itinerary: List[DayPlan] = Field(default_factory=list)
    budget_breakdown: BudgetBreakdown
    packing_checklist: List[str] = Field(default_factory=list)
    local_customs_and_safety_tips: List[str] = Field(default_factory=list)

class TripResponse(BaseModel):
    success: bool = True
    trip_id: str
    request: TripRequest
    itinerary: TripItinerary
    raw_logs: Optional[Dict[str, Any]] = None
