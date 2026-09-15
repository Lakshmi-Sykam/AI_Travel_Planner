import folium
import streamlit as st
from streamlit_folium import st_folium

CITY_COORDINATES = {
    "goa": (15.2993, 74.1240),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "hyderabad": (17.3850, 78.4867),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "jaipur": (26.9124, 75.7873),
    "udaipur": (24.5854, 73.7125),
    "manali": (32.2432, 77.1892),
    "shimla": (31.1048, 77.1734),
    "kerala": (10.8505, 76.2711),
    "munnar": (10.0889, 77.0595),
    "paris": (48.8566, 2.3522),
    "london": (51.5074, -0.1278),
    "tokyo": (35.6762, 139.6503),
    "dubai": (25.2048, 55.2708),
    "singapore": (1.3521, 103.8198),
    "bangkok": (13.7563, 100.5018),
    "bali": (-8.4095, 115.1889),
    "new york": (40.7128, -74.0060),
    "san francisco": (37.7749, -122.4194),
    "rome": (41.9028, 12.4964),
    "amsterdam": (52.3676, 4.9041),
    "sydney": (-33.8688, 151.2093),
    "barcelona": (41.3879, 2.1699),
}

def resolve_location(name: str, fallback_center=(15.2993, 74.1240), offset_seed=0):
    """
    Resolve latitude and longitude for a city or landmark.
    """
    clean_name = str(name).lower().strip()
    for city, coords in CITY_COORDINATES.items():
        if city in clean_name:
            return coords

    base_lat, base_lng = fallback_center
    jitter_lat = ((hash(clean_name + str(offset_seed)) % 100) - 50) * 0.0008
    jitter_lng = ((hash(clean_name + str(offset_seed + 7)) % 100) - 50) * 0.0008
    return (base_lat + jitter_lat, base_lng + jitter_lng)

def render_interactive_map(itinerary: dict, origin: str, destination: str):
    """
    Renders an interactive Leaflet/Folium map with trip routes, hotel markers, and daily activity pins.
    """
    dest_center = resolve_location(destination, fallback_center=(15.2993, 74.1240))
    origin_coords = resolve_location(origin, fallback_center=(19.0760, 72.8777))

    # Initialize Folium Map
    m = folium.Map(
        location=dest_center,
        zoom_start=11,
        tiles="CartoDB positron",
        control_scale=True
    )

    # Route from Origin to Destination (if distinct)
    if origin_coords != dest_center:
        folium.PolyLine(
            locations=[origin_coords, dest_center],
            color="#3b82f6",
            weight=3,
            dash_array="8, 8",
            opacity=0.8,
            tooltip=f"✈️ Travel Route: {origin} ➔ {destination}"
        ).add_to(m)

        folium.Marker(
            location=origin_coords,
            popup=f"<b>🛫 Departure:</b> {origin}",
            tooltip=f"Origin: {origin}",
            icon=folium.Icon(color="gray", icon="plane", prefix="fa")
        ).add_to(m)

    circuit_points = [dest_center]

    # Hotel Markers
    hotels = itinerary.get("hotel_options", [])
    if not hotels and "selected_hotel_recommendation" in itinerary:
        hotels = [itinerary["selected_hotel_recommendation"]]

    for h_idx, hotel in enumerate(hotels[:2]):
        hotel_name = hotel.get("name") or hotel.get("hotel_name", f"Hotel in {destination}")
        hotel_cost = hotel.get("price_per_night", "")
        hotel_loc = hotel.get("area_or_neighborhood", destination)
        hotel_coords = resolve_location(hotel_name, fallback_center=dest_center, offset_seed=100 + h_idx)
        
        hotel_popup_html = f"""
        <div style='font-family: sans-serif; min-width: 180px;'>
            <h4 style='margin:0 0 5px 0; color:#0284c7;'>🏨 {hotel_name}</h4>
            <p style='margin:0; font-size:12px;'><b>Est. Cost:</b> {hotel_cost}/night</p>
            <p style='margin:0; font-size:12px;'><b>Area:</b> {hotel_loc}</p>
        </div>
        """
        folium.Marker(
            location=hotel_coords,
            popup=folium.Popup(hotel_popup_html, max_width=300),
            tooltip=f"🏨 Stay: {hotel_name}",
            icon=folium.Icon(color="blue", icon="bed", prefix="fa")
        ).add_to(m)
        circuit_points.append(hotel_coords)

    # Daily Activities Markers
    daily_days = itinerary.get("daily_itinerary", [])
    colors = ["green", "orange", "purple", "darkred", "cadetblue", "darkblue", "darkgreen"]

    for d_idx, day_plan in enumerate(daily_days):
        day_num = day_plan.get("day", d_idx + 1)
        color = colors[d_idx % len(colors)]
        activities = day_plan.get("activities", [])

        # Fallback if activities are structured under morning/afternoon/evening keys
        if not activities:
            for slot_key in ["morning", "afternoon", "evening"]:
                if slot_key in day_plan and isinstance(day_plan[slot_key], dict):
                    item = day_plan[slot_key]
                    activities.append({
                        "time_slot": slot_key.capitalize(),
                        "title": item.get("activity") or item.get("time", f"{slot_key.capitalize()} Activity"),
                        "description": item.get("description", ""),
                        "cost": item.get("estimated_cost", 0),
                        "location": item.get("location", destination)
                    })

        for a_idx, act in enumerate(activities):
            act_title = act.get("title") or act.get("activity") or f"Activity {a_idx+1}"
            time_slot = act.get("time_slot", "Day")
            act_desc = act.get("description", "")
            act_cost = act.get("cost", 0)
            loc_hint = act.get("location") or f"{act_title}, {destination}"
            
            slot_coords = resolve_location(
                loc_hint, 
                fallback_center=dest_center, 
                offset_seed=(d_idx * 15) + a_idx + 1
            )
            circuit_points.append(slot_coords)

            popup_html = f"""
            <div style='font-family: sans-serif; min-width: 190px;'>
                <span style='background-color:#e0f2fe; color:#0369a1; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:bold;'>
                    Day {day_num} • {time_slot}
                </span>
                <h4 style='margin:6px 0 4px 0; color:#1e293b;'>{act_title}</h4>
                <p style='margin:0; font-size:12px; color:#475569;'>{str(act_desc)[:120]}...</p>
                <p style='margin:4px 0 0 0; font-size:11px; font-weight:bold; color:#15803d;'>Est: ₹{act_cost}</p>
            </div>
            """

            folium.Marker(
                location=slot_coords,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"Day {day_num} ({time_slot}): {act_title}",
                icon=folium.Icon(color=color, icon="star", prefix="fa")
            ).add_to(m)

    # Render day circuit polyline
    if len(circuit_points) > 2:
        folium.PolyLine(
            locations=circuit_points[1:],
            color="#6366f1",
            weight=2.5,
            opacity=0.6,
            dash_array="4, 6",
            tooltip="🗺️ Recommended Sightseeing Route"
        ).add_to(m)

    st_folium(m, width="100%", height=450, returned_objects=[])
