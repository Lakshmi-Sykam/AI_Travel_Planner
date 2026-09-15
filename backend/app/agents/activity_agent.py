from typing import Dict, Any, List
from backend.app.agents.state import TripAgentState
from backend.app.agents.llm import invoke_llm_json
from backend.app.tools.search_tool import search_destination_attractions

def activity_agent_node(state: TripAgentState) -> Dict[str, Any]:
    """
    Agent Node: Activity, Sightseeing & Culinary Specialist
    Constructs an engaging day-by-day plan of activities, sightseeing spots, and food recommendations.
    """
    destination = state.get("destination", "Goa")
    duration_days = state.get("duration_days", 4)
    interests = state.get("interests", ["Sightseeing", "Food"])
    currency = state.get("currency", "INR")
    travel_style = state.get("travel_style", "Budget")
    
    # Retrieve relevant attractions
    attractions = search_destination_attractions(destination, interests)
    
    system_prompt = (
        "You are an expert Local Sightseeing & Cultural Activity AI Agent. Your task is to design a rich, "
        "practical day-by-day schedule with activities split into Morning, Afternoon, Evening/Night, "
        "plus authentic local dining spots."
    )

    prompt = f"""
    Destination: {destination}
    Duration: {duration_days} Days
    Interests: {", ".join(interests)}
    Travel Style: {travel_style}
    Available Key Landmarks: {[a['name'] for a in attractions]}
    
    Generate a JSON object containing a key 'daily_activities' which is an array of {duration_days} Day objects:
    {{
      "daily_activities": [
        {{
          "day": 1,
          "theme": "Arrival & Coastal Sunset Chill",
          "activities": [
            {{
              "time_slot": "Morning",
              "title": "Arrival & Check-in",
              "description": "Check into hotel, freshen up, and rent a scooter or hire local cab.",
              "cost": 0,
              "location": "Central Area",
              "tips": "Carry valid ID and keep offline maps downloaded."
            }},
            {{
              "time_slot": "Afternoon",
              "title": "Local Cafe Lunch & Beach Walk",
              "description": "Stroll down the golden sands and sample fresh seafood or local curry.",
              "cost": 300,
              "location": "Main Coastline",
              "tips": "Apply sunscreen and hydrate with tender coconut."
            }},
            {{
              "time_slot": "Evening / Sunset",
              "title": "Sunset Viewpoint & Night Market",
              "description": "Watch the sunset from the cliffside cafe followed by flea market browsing.",
              "cost": 150,
              "location": "Cliff Viewpoint",
              "tips": "Arrive by 5:30 PM for prime sunset photography."
            }}
          ],
          "food_recommendations": [
            "Authentic Thali at Local Spice Kitchen",
            "Goan Fish Curry / Poee Bread / Bebinca Dessert"
          ],
          "day_budget_estimate": 800
        }}
      ]
    }}
    """

    llm_result = invoke_llm_json(prompt, system_prompt)
    if llm_result and "daily_activities" in llm_result and len(llm_result["daily_activities"]) >= duration_days:
        daily_plans = llm_result["daily_activities"][:duration_days]
    else:
        # Structured fallback plan generator
        daily_plans = []
        themes = [
            f"Arrival, City Vibes & {destination} Heritage",
            f"Nature, Iconic Landmarks & Scenic Views",
            f"Adventure, Cultural Exploration & Local Markets",
            f"Hidden Gems, Leisure & Departure Shopping",
            f"Extended Excursions & Water Activities",
            f"Relaxed Spa & Local Culinary Masterclass",
            f"Farewell Sunset & Souvenir Hunt"
        ]
        
        for d in range(1, duration_days + 1):
            attr_idx = (d - 1) % max(1, len(attractions))
            chosen_attr = attractions[attr_idx]["name"] if attractions else f"Top Spot in {destination}"
            theme = themes[(d - 1) % len(themes)]
            
            day_plan = {
                "day": d,
                "theme": theme,
                "activities": [
                    {
                        "time_slot": "Morning (09:00 AM - 12:30 PM)",
                        "title": f"Explore {chosen_attr}",
                        "description": f"Visit {chosen_attr} during early hours to beat the crowd and enjoy pleasant morning lighting.",
                        "cost": 100.0 if currency == "INR" else 5.0,
                        "location": destination,
                        "tips": "Wear comfortable walking shoes and carry water."
                    },
                    {
                        "time_slot": "Afternoon (01:00 PM - 04:30 PM)",
                        "title": f"Culinary Experience & Cultural Stroll",
                        "description": f"Enjoy lunch at a highly-rated local bistro, followed by exploring quaint neighborhood lanes and art boutiques in {destination}.",
                        "cost": 400.0 if currency == "INR" else 15.0,
                        "location": "Old Quarter / Market Hub",
                        "tips": "Try local specialty street delicacies and fresh juices."
                    },
                    {
                        "time_slot": "Evening (05:30 PM - 09:30 PM)",
                        "title": "Golden Hour Sunset & Evening Bazaar",
                        "description": f"Witness the panoramic sunset from a famous viewpoint, then stroll through the bustling local bazaar for souvenirs and evening vibes.",
                        "cost": 250.0 if currency == "INR" else 10.0,
                        "location": "Promenade / Night Market",
                        "tips": "Bargain respectfully in flea markets."
                    }
                ],
                "food_recommendations": [
                    f"Signature regional specialty of {destination}",
                    "Famous local bakery or street food counter",
                    "Rooftop dinner with ambient acoustic music"
                ],
                "day_budget_estimate": 750.0 if currency == "INR" else 30.0
            }
            daily_plans.append(day_plan)

    logs = state.get("logs", [])
    logs.append({
        "agent": "Activity Agent",
        "action": f"Designed {duration_days}-day itinerary tailored to {len(interests)} interests",
        "status": f"Scheduled {len(daily_plans)} comprehensive day plans"
    })

    return {
        "daily_activities": daily_plans,
        "logs": logs
    }
