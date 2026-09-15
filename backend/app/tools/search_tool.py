from typing import List, Dict, Any

def search_destination_attractions(destination: str, interests: List[str]) -> List[Dict[str, Any]]:
    """
    Search attractions and landmarks matching traveler interests.
    """
    dest_lower = destination.lower()
    
    if "goa" in dest_lower:
        return [
            {"name": "Anjuna & Vagator Beach", "category": "Beaches / Sunsets", "est_cost": 0, "rating": 4.6, "time_needed": "3-4 hrs"},
            {"name": "Aguada Fort & Lighthouse", "category": "History / Architecture", "est_cost": 50, "rating": 4.4, "time_needed": "2 hrs"},
            {"name": "Dudhsagar Waterfalls Trek", "category": "Adventure / Nature", "est_cost": 650, "rating": 4.7, "time_needed": "5 hrs"},
            {"name": "Old Goa Churches (Basilica of Bom Jesus)", "category": "Heritage / Culture", "est_cost": 0, "rating": 4.8, "time_needed": "2.5 hrs"},
            {"name": "Palolem & Butterfly Beach (South Goa)", "category": "Serene Beaches / Kayaking", "est_cost": 300, "rating": 4.8, "time_needed": "4 hrs"},
            {"name": "Fontainhas Latin Quarter Walking Tour", "category": "Heritage / Photography", "est_cost": 0, "rating": 4.5, "time_needed": "2 hrs"},
            {"name": "Saturday Night Market / Flea Market", "category": "Shopping / Nightlife", "est_cost": 0, "rating": 4.3, "time_needed": "3 hrs"}
        ]
    elif "manali" in dest_lower:
        return [
            {"name": "Solang Valley Snow Point & Zip Lining", "category": "Adventure / Snow", "est_cost": 1000, "rating": 4.7, "time_needed": "4 hrs"},
            {"name": "Atal Tunnel & Sissu Waterfall", "category": "Scenic Drive / Nature", "est_cost": 200, "rating": 4.9, "time_needed": "5 hrs"},
            {"name": "Old Manali Cafes & Wooden Cabins", "category": "Food / Vibes", "est_cost": 0, "rating": 4.6, "time_needed": "3 hrs"},
            {"name": "Hadimba Devi Ancient Temple", "category": "Heritage / Culture", "est_cost": 20, "rating": 4.5, "time_needed": "1.5 hrs"},
            {"name": "Jogini Waterfall Hike", "category": "Trek / Nature", "est_cost": 0, "rating": 4.8, "time_needed": "3 hrs"}
        ]
    elif "jaipur" in dest_lower:
        return [
            {"name": "Amber Palace & Elephant View", "category": "History / Forts", "est_cost": 200, "rating": 4.8, "time_needed": "3.5 hrs"},
            {"name": "Hawa Mahal & Wind Cafe", "category": "Architecture / Photography", "est_cost": 50, "rating": 4.6, "time_needed": "1.5 hrs"},
            {"name": "City Palace & Jantar Mantar", "category": "Royal Heritage", "est_cost": 300, "rating": 4.7, "time_needed": "3 hrs"},
            {"name": "Nahargarh Fort Sunset Point", "category": "Scenic Sunset", "est_cost": 100, "rating": 4.8, "time_needed": "2.5 hrs"},
            {"name": "Johari Bazaar Street Food & Handicrafts", "category": "Shopping / Food", "est_cost": 0, "rating": 4.5, "time_needed": "2.5 hrs"}
        ]
    else:
        return [
            {"name": f"City Center & Historic Old Town of {destination}", "category": "Heritage & Culture", "est_cost": 50, "rating": 4.5, "time_needed": "3 hrs"},
            {"name": f"Famous Scenic Viewpoint & Promenade", "category": "Sightseeing / Views", "est_cost": 0, "rating": 4.6, "time_needed": "2 hrs"},
            {"name": f"Popular Local Market & Culinary Street", "category": "Food & Culture", "est_cost": 0, "rating": 4.7, "time_needed": "2.5 hrs"},
            {"name": f"National Landmark / Botanical Garden / Museum", "category": "Sightseeing", "est_cost": 150, "rating": 4.4, "time_needed": "3 hrs"}
        ]
