from typing import TypedDict, List, Dict, Any, Optional

class TripAgentState(TypedDict, total=False):
    # User Inputs
    origin: str
    destination: str
    duration_days: int
    budget: float
    currency: str
    travel_style: str
    interests: List[str]
    group_size: int
    special_requirements: Optional[str]

    # Modification contexts (if modifying existing trip)
    is_modification: bool
    modification_prompt: Optional[str]
    existing_itinerary: Optional[Dict[str, Any]]

    # Tool & Node Outputs
    weather_info: Dict[str, Any]
    budget_analysis: Dict[str, Any]
    travel_options: List[Dict[str, Any]]
    hotel_options: List[Dict[str, Any]]
    daily_activities: List[Dict[str, Any]]
    final_itinerary: Dict[str, Any]
    
    # Execution telemetry
    logs: List[Dict[str, str]]
    errors: List[str]
