from typing import Dict, Any, List
from backend.app.agents.state import TripAgentState
from backend.app.agents.llm import invoke_llm_json

def hotel_agent_node(state: TripAgentState) -> Dict[str, Any]:
    """
    Agent Node: Hotel & Accommodation Specialist
    Selects lodging options matching traveler budget, style, and neighborhood preference.
    """
    destination = state.get("destination", "Goa")
    duration_days = state.get("duration_days", 4)
    budget = state.get("budget", 20000)
    currency = state.get("currency", "INR")
    travel_style = state.get("travel_style", "Budget")
    nights = max(1, duration_days - 1)
    
    budget_analysis = state.get("budget_analysis", {})
    target_per_night = budget_analysis.get("hotel_per_night_target", (budget * 0.3) / nights)

    system_prompt = (
        "You are an expert Hotel & Stay AI Agent. Your task is to recommend realistic hotel/hostel/resort "
        "options in the destination suitable for the traveler's budget and travel style. "
        "Return a JSON object with a key 'hotel_options' containing an array of hotel objects."
    )

    prompt = f"""
    Destination: {destination}
    Duration: {duration_days} Days ({nights} Nights)
    Target Hotel Budget Per Night: ~{currency} {target_per_night:.0f}
    Travel Style: {travel_style}
    
    Provide 3 distinct accommodation choices (Budget/Hostel, Recommended Mid-tier/Boutique, Premium option). Format strictly as:
    {{
      "hotel_options": [
        {{
          "name": "e.g. Zostel / Hosteller / Heritage Portuguese Villa / Beachside Resort",
          "area_or_neighborhood": "e.g. Anjuna / Calangute / Fontainhas",
          "price_per_night": 1200,
          "total_cost": {1200 * nights},
          "amenities": ["High-speed WiFi", "Pool / Cafe", "AC", "Breakfast Included"],
          "rating_approx": 4.5,
          "why_recommended": "Central location close to top beaches and nightlife while remaining within budget."
        }}
      ]
    }}
    """

    llm_result = invoke_llm_json(prompt, system_prompt)
    if llm_result and "hotel_options" in llm_result:
        options = llm_result["hotel_options"]
    else:
        # Fallback tailored to destination & budget
        p1 = round(target_per_night * 0.7, 0)
        p2 = round(target_per_night * 1.0, 0)
        p3 = round(target_per_night * 1.5, 0)
        
        options = [
            {
                "name": f"Backpacker Social Hostel & Cafe, {destination}",
                "area_or_neighborhood": "Prime Central Backpacker Hub",
                "price_per_night": p1,
                "total_cost": p1 * nights,
                "amenities": ["Free High-speed WiFi", "Community Lounge", "AC Dorms/Privates", "Shared Kitchen"],
                "rating_approx": 4.6,
                "why_recommended": "Cost-effective, great social atmosphere to meet fellow travelers."
            },
            {
                "name": f"Boutique Heritage Inn & Garden Suites, {destination}",
                "area_or_neighborhood": "Quiet & Scenic Neighborhood",
                "price_per_night": p2,
                "total_cost": p2 * nights,
                "amenities": ["Swimming Pool", "Complimentary Breakfast", "King Bed & Balcony", "Airport Shuttle"],
                "rating_approx": 4.4,
                "why_recommended": "Best balance of comfort, cleanliness, and value for money."
            },
            {
                "name": f"Luxury View Resort & Spa, {destination}",
                "area_or_neighborhood": "Beachfront / Mountain Ridge Viewpoint",
                "price_per_night": p3,
                "total_cost": p3 * nights,
                "amenities": ["Infinity Pool", "Multi-cuisine Restaurant", "Spa & Wellness", "Panoramic Views"],
                "rating_approx": 4.8,
                "why_recommended": "Upgraded comfort with breathtaking views and premium hospitality."
            }
        ]

    logs = state.get("logs", [])
    logs.append({
        "agent": "Hotel Agent",
        "action": f"Scanned stays in {destination} for target ~{currency} {target_per_night:.0f}/night",
        "status": f"Curated {len(options)} accommodation choices"
    })

    return {
        "hotel_options": options,
        "logs": logs
    }
