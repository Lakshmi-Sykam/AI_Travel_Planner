from typing import Dict, Any, List
from backend.app.agents.state import TripAgentState
from backend.app.agents.llm import invoke_llm_json

def travel_agent_node(state: TripAgentState) -> Dict[str, Any]:
    """
    Agent Node: Travel & Logistics Specialist
    Calculates transport options between origin and destination based on budget and duration.
    """
    origin = state.get("origin", "Mumbai")
    destination = state.get("destination", "Goa")
    budget = state.get("budget", 20000)
    currency = state.get("currency", "INR")
    travel_style = state.get("travel_style", "Budget")
    group_size = state.get("group_size", 1)
    preferred_transport = state.get("preferred_transport", "Any / Best AI Match")

    system_prompt = (
        "You are an expert Travel & Logistics AI Agent. Your task is to recommend real-world transportation "
        "options (flights, trains, buses, cabs, rental cars) between the origin and destination considering distance, budget, travel style, and preferred transport mode. "
        "Return a JSON object with a key 'transport_options' containing an array of options with mode, provider_or_route, estimated_cost, duration_hours, departure_tips, and booking_tips."
    )
    
    prompt = f"""
    Origin: {origin}
    Destination: {destination}
    Total Budget: {currency} {budget}
    Travel Style: {travel_style}
    Group Size: {group_size}
    Preferred Transport Mode: {preferred_transport}
    
    Provide realistic transit options (prioritizing '{preferred_transport}' if specific). Format strictly as:
    {{
      "transport_options": [
        {{
          "mode": "Train / Flight / Car / Cab / Bus",
          "provider_or_route": "e.g. Vande Bharat Express / IndiGo / Self-Drive NH66 Highway / Sleeper AC Bus",
          "estimated_cost": 1500,
          "duration_hours": 8.5,
          "departure_tips": "Board early morning from Origin Central",
          "booking_tips": "Book 3-4 weeks in advance via official app for best rates"
        }}
      ]
    }}
    """
    
    llm_result = invoke_llm_json(prompt, system_prompt)
    if llm_result and "transport_options" in llm_result:
        options = llm_result["transport_options"]
    else:
        # Smart heuristic fallback
        is_flight_budget = budget >= (15000 if currency == "INR" else 200)
        options = [
            {
                "mode": "Train (Express / AC Chair Car)",
                "provider_or_route": f"Direct Express connection from {origin} to {destination}",
                "estimated_cost": 1200.0 if currency == "INR" else 25.0,
                "duration_hours": 9.0,
                "departure_tips": f"Take the morning or overnight express from {origin} Central.",
                "booking_tips": "Reserve Tatkal / AC 3-Tier tickets 2 weeks ahead."
            },
            {
                "mode": "Sleeper Bus (Multi-Axle AC)",
                "provider_or_route": f"Overnight AC Sleeper ({origin} to {destination})",
                "estimated_cost": 900.0 if currency == "INR" else 20.0,
                "duration_hours": 11.0,
                "departure_tips": "Board around 9:00 PM to save on one night's hotel cost.",
                "booking_tips": "Choose lower single berth for superior comfort."
            }
        ]
        if is_flight_budget:
            options.insert(0, {
                "mode": "Flight (Economy)",
                "provider_or_route": f"Direct flight from {origin} to {destination}",
                "estimated_cost": 3800.0 if currency == "INR" else 65.0,
                "duration_hours": 1.5,
                "departure_tips": "Reach airport 2 hours prior to departure with web check-in.",
                "booking_tips": "Compare price trackers on Tuesday/Wednesday departures."
            })

    logs = state.get("logs", [])
    logs.append({
        "agent": "Travel Agent",
        "action": f"Evaluated routes & transit from {origin} to {destination}",
        "status": f"Generated {len(options)} transport options"
    })

    return {
        "travel_options": options,
        "logs": logs
    }
