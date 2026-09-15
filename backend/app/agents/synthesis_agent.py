from typing import Dict, Any, List
from backend.app.agents.state import TripAgentState

def synthesis_agent_node(state: TripAgentState) -> Dict[str, Any]:
    """
    Agent Node: Master Synthesis & Budget Reconciliation Agent
    Unifies all sub-agent outputs into a coherent, production-ready travel itinerary.
    """
    destination = state.get("destination", "Goa")
    origin = state.get("origin", "Mumbai")
    duration_days = state.get("duration_days", 4)
    total_budget = state.get("budget", 20000)
    currency = state.get("currency", "INR")
    weather_info = state.get("weather_info", {})
    budget_analysis = state.get("budget_analysis", {})
    travel_options = state.get("travel_options", [])
    hotel_options = state.get("hotel_options", [])
    daily_activities = state.get("daily_activities", [])

    group_size = state.get("group_size", 1)

    # Pick best-fit hotel and transport for budget
    selected_hotel = hotel_options[1] if len(hotel_options) > 1 else (hotel_options[0] if hotel_options else None)
    selected_transit = travel_options[0] if travel_options else None

    # Calculate actual estimated budget sum
    transit_cost = (selected_transit.get("estimated_cost", 0) * 2 * group_size) if selected_transit else (total_budget * 0.3) # Round trip for all members
    hotel_cost = selected_hotel.get("total_cost", 0) if selected_hotel else (total_budget * 0.35)
    
    # Sum daily activity and food estimates
    activities_sum = sum(
        sum(act.get("cost", 0) for act in day.get("activities", []))
        for day in daily_activities
    )
    food_sum = budget_analysis.get("food_target", total_budget * 0.20)
    buffer_sum = round(total_budget * 0.05, 2)
    
    total_calculated_cost = round(transit_cost + hotel_cost + food_sum + activities_sum + buffer_sum, 2)
    is_within_budget = total_calculated_cost <= (total_budget * 1.10) # 10% tolerance

    budget_breakdown = {
        "transportation": round(transit_cost, 2),
        "accommodation": round(hotel_cost, 2),
        "food_and_dining": round(food_sum, 2),
        "activities_and_entry": round(activities_sum, 2),
        "emergency_buffer": round(buffer_sum, 2),
        "total_estimated_cost": total_calculated_cost,
        "currency": currency,
        "is_within_budget": is_within_budget,
        "budget_advice": budget_analysis.get(
            "budget_advice", 
            "Budget fits well. Book train/flight tickets early to lock in lower transit costs."
        )
    }

    # Packing and safety tips
    clothing_advice = weather_info.get("clothing_advice", "Light cotton clothes, comfortable walking footwear.")
    packing_checklist = [
        "Government Photo ID & Booking Confirmations",
        clothing_advice,
        "Power Bank & Universal Charging Adapter",
        "Basic First-Aid & Personal Prescriptions",
        "Sunscreen, Sunglasses & Reusable Water Bottle"
    ]

    safety_tips = [
        f"Keep emergency helpline numbers saved for {destination}.",
        "Use authorized metered taxis or ride-hailing apps for late-night transits.",
        "Stay hydrated and prefer freshly prepared warm meals or popular bustling eateries.",
        "Respect local dress codes and cultural norms at sacred or historical sites."
    ]

    destination_overview = (
        f"{destination} offers a captivating blend of cultural heritage, scenic vistas, and flavorful cuisine. "
        f"This curated {duration_days}-day itinerary from {origin} has been balanced to maximize your experience "
        f"while maintaining financial discipline within your {currency} {total_budget:,.0f} budget."
    )

    final_itinerary = {
        "destination_overview": destination_overview,
        "best_time_to_visit": weather_info.get("best_season", "October to March"),
        "weather_forecast_summary": f"Expected: {weather_info.get('temperature_range', '22-32°C')}, {weather_info.get('condition', 'Pleasant and sunny')}",
        "transport_options": travel_options,
        "hotel_options": hotel_options,
        "selected_hotel_recommendation": selected_hotel,
        "daily_itinerary": daily_activities,
        "budget_breakdown": budget_breakdown,
        "packing_checklist": packing_checklist,
        "local_customs_and_safety_tips": safety_tips
    }

    logs = state.get("logs", [])
    logs.append({
        "agent": "Synthesis Orchestrator",
        "action": "Compiled unified travel plan and finalized budget verification",
        "status": f"Successfully finalized {duration_days}-day trip to {destination}"
    })

    return {
        "final_itinerary": final_itinerary,
        "logs": logs
    }
