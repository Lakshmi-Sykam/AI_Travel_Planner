import re
import folium
import streamlit as st
from streamlit_folium import st_folium

# Major City Coordinates (for Origin and Destination resolution)
CITY_COORDINATES = {
    # Andhra Pradesh & Telangana
    "vijayawada": (16.5062, 80.6480),
    "visakhapatnam": (17.6868, 83.2185),
    "vizag": (17.6868, 83.2185),
    "guntur": (16.3067, 80.4365),
    "amaravati": (16.5417, 80.5158),
    "tirupati": (13.6288, 79.4192),
    "rajahmundry": (17.0005, 81.8040),
    "kakinada": (16.9891, 82.2475),
    "nellore": (14.4426, 79.9865),
    "kurnool": (15.8281, 78.0373),
    "kadapa": (14.4673, 78.8242),
    "anantapur": (14.6819, 77.6006),
    "hyderabad": (17.3850, 78.4867),
    "warangal": (17.9689, 79.5941),
    "secunderabad": (17.4399, 78.4983),
    
    # Major Indian Metro & Popular Cities
    "goa": (15.2993, 74.1240),
    "mumbai": (19.0760, 72.8777),
    "delhi": (28.6139, 77.2090),
    "new delhi": (28.6139, 77.2090),
    "bangalore": (12.9716, 77.5946),
    "bengaluru": (12.9716, 77.5946),
    "chennai": (13.0827, 80.2707),
    "kolkata": (22.5726, 88.3639),
    "pune": (18.5204, 73.8567),
    "ahmedabad": (23.0225, 72.5714),
    "surat": (21.1702, 72.8311),
    "jaipur": (26.9124, 75.7873),
    "udaipur": (24.5854, 73.7125),
    "jodhpur": (26.2389, 73.0243),
    "jaisalmer": (26.9157, 70.9083),
    "manali": (32.2432, 77.1892),
    "shimla": (31.1048, 77.1734),
    "kerala": (10.8505, 76.2711),
    "munnar": (10.0889, 77.0595),
    "kochi": (9.9312, 76.2673),
    "cochin": (9.9312, 76.2673),
    "thiruvananthapuram": (8.5241, 76.9366),
    "trivandrum": (8.5241, 76.9366),
    "kozhikode": (11.2588, 75.7804),
    "wayanad": (11.6854, 76.1320),
    "alleppey": (9.4981, 76.3388),
    "alappuzha": (9.4981, 76.3388),
    "varkala": (8.7379, 76.7163),
    "agra": (27.1767, 78.0081),
    "varanasi": (25.3176, 82.9739),
    "amritsar": (31.6340, 74.8723),
    "rishikesh": (30.0869, 78.2676),
    "haridwar": (29.9457, 78.1642),
    "dehradun": (30.3165, 78.0322),
    "ooty": (11.4102, 76.6950),
    "kodaikanal": (10.2381, 77.4892),
    "coimbatore": (11.0168, 76.9558),
    "madurai": (9.9252, 78.1198),
    "mysore": (12.2958, 76.6394),
    "mysuru": (12.2958, 76.6394),
    "mangalore": (12.9141, 74.8560),
    "bhubaneswar": (20.2961, 85.8245),
    "puri": (19.8135, 85.8312),
    "patna": (25.5941, 85.1376),
    "lucknow": (26.8467, 80.9462),
    "kanpur": (26.4499, 80.3319),
    "bhopal": (23.2599, 77.4126),
    "indore": (22.7196, 75.8577),
    "nagpur": (21.1458, 79.0882),
    "nashik": (19.9975, 73.7898),
    "aurangabad": (19.8762, 75.3433),
    "chandigarh": (30.7333, 76.7794),
    "guwahati": (26.1445, 91.7362),
    "shillong": (25.5788, 91.8933),
    "gangtok": (27.3314, 88.6138),
    "srinagar": (34.0837, 74.7973),
    "leh": (34.1526, 77.5771),
    "ladakh": (34.1526, 77.5771),

    # International Hubs
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

@st.cache_data(show_spinner=False, ttl=86400)
def geocode_city_online(query: str):
    """
    Dynamic geocoding fallback using OpenStreetMap Nominatim for unlisted cities/towns.
    Cached for fast subsequent lookups.
    """
    try:
        import httpx
        url = "https://nominatim.openstreetmap.org/search"
        headers = {"User-Agent": "AITravelPlanner/1.0"}
        params = {"q": query, "format": "json", "limit": 1}
        response = httpx.get(url, params=params, headers=headers, timeout=2.0)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                return (float(data[0]["lat"]), float(data[0]["lon"]))
    except Exception:
        pass
    return None

def resolve_city(name: str, fallback=(15.2993, 74.1240)):
    """
    Resolve origin and destination using exact word boundary matching,
    followed by dynamic online geocoding if not found in local catalog.
    """
    if not name:
        return fallback
    clean = str(name).lower().strip()
    
    # 1. Match from local catalog
    for city, coords in CITY_COORDINATES.items():
        if re.search(rf"\b{re.escape(city)}\b", clean):
            return coords
            
    # 2. Dynamic geocoding fallback
    online_coords = geocode_city_online(clean)
    if online_coords:
        return online_coords
        
    return fallback

resolve_location = resolve_city

# Accurate Regional Landmarks (anchored within destination zones)
LANDMARK_COORDINATES = {
    # Goa Landmarks & Beaches
    "panaji": (15.4909, 73.8278),
    "panjim": (15.4909, 73.8278),
    "baga": (15.5553, 73.7517),
    "baga beach": (15.5553, 73.7517),
    "calangute": (15.5439, 73.7553),
    "calangute beach": (15.5439, 73.7553),
    "anjuna": (15.5800, 73.7400),
    "anjuna beach": (15.5800, 73.7400),
    "vagator": (15.5997, 73.7380),
    "vagator beach": (15.5997, 73.7380),
    "candolim": (15.5186, 73.7663),
    "candolim beach": (15.5186, 73.7663),
    "aguada": (15.4925, 73.7736),
    "fort aguada": (15.4925, 73.7736),
    "chapora": (15.6058, 73.7358),
    "chapora fort": (15.6058, 73.7358),
    "old goa": (15.5030, 73.9110),
    "bom jesus": (15.5009, 73.9116),
    "basilica of bom jesus": (15.5009, 73.9116),
    "dudhsagar": (15.3144, 74.3143),
    "dudhsagar waterfalls": (15.3144, 74.3143),
    "palolem": (15.0100, 74.0232),
    "palolem beach": (15.0100, 74.0232),
    "colva": (15.2783, 73.9167),
    "colva beach": (15.2783, 73.9167),
    "miramar": (15.4833, 73.8117),
    "miramar beach": (15.4833, 73.8117),
    "fontainhas": (15.4960, 73.8320),
    "arambol": (15.6853, 73.7042),
    "morjim": (15.6322, 73.7297),
    "mandovi": (15.4990, 73.8250),
    "mandovi river": (15.4990, 73.8250),
    "donapaula": (15.4539, 73.8052),
    "dona paula": (15.4539, 73.8052),
    "sinquerim": (15.4980, 73.7690),
    "benaulim": (15.2580, 73.9210),
    "salcete": (15.2900, 73.9800),

    # Andhra Pradesh & Vijayawada Landmarks
    "kanaka durga": (16.5161, 80.6094),
    "prakasam barrage": (16.5073, 80.6053),
    "undavalli": (16.4967, 80.5802),
    "undavalli caves": (16.4967, 80.5802),
    "bhavani island": (16.5226, 80.5901),
    "mangalagiri": (16.4357, 80.5694),
    "rishi konda": (17.7816, 83.3853),
    "kailasagiri": (17.7490, 83.3422),
    "araku": (18.3273, 82.8775),
    "araku valley": (18.3273, 82.8775),
    "borra caves": (18.2804, 83.0396),

    # Delhi Landmarks
    "india gate": (28.6129, 77.2295),
    "qutub minar": (28.5245, 77.1855),
    "red fort": (28.6562, 77.2410),
    "lotus temple": (28.5535, 77.2588),
    "humayun tomb": (28.5933, 77.2507),
    "akshardham": (28.6127, 77.2773),

    # Mumbai Landmarks
    "gateway of india": (18.9220, 72.8347),
    "marine drive": (18.9432, 72.8230),
    "juhu beach": (19.0988, 72.8264),
    "bandra bandstand": (19.0473, 72.8197),
    "elephanta caves": (18.9633, 72.9315),
    "colaba": (18.9067, 72.8147),

    # Jaipur Landmarks
    "hawa mahal": (26.9239, 75.8267),
    "amber fort": (26.9855, 75.8513),
    "city palace": (26.9258, 75.8237),
    "jal mahal": (26.9656, 75.8456),
    "nahargarh": (26.9373, 75.8156),

    # Kerala Landmarks
    "tea museum": (10.0889, 77.0595),
    "mattupetty": (10.1062, 77.1246),
    "eravikulam": (10.2033, 77.0850),
    "vembanad": (9.5833, 76.4167),
    "fort kochi": (9.9658, 76.2421),
    "jew town": (9.9579, 76.2597),
}

def resolve_activity_location(name: str, dest_center: tuple, offset_seed: int = 0):
    """
    Resolve local activity and hotel coordinates.
    Guaranteed to stay anchored within the destination area.
    """
    clean = str(name).lower().strip()

    # 1. Match local destination landmarks first
    landmarks = globals().get("LANDMARK_COORDINATES", {})
    for landmark, coords in landmarks.items():
        if re.search(rf"\b{re.escape(landmark)}\b", clean):
            return coords

    # 2. Local realistic jitter around the destination center (within ~5-8km)
    base_lat, base_lng = dest_center
    jitter_lat = ((hash(clean + str(offset_seed)) % 100) - 50) * 0.0007
    jitter_lng = ((hash(clean + str(offset_seed + 7)) % 100) - 50) * 0.0007
    return (base_lat + jitter_lat, base_lng + jitter_lng)

def render_interactive_map(itinerary: dict, origin: str, destination: str):
    """
    Renders an interactive Leaflet/Folium map with trip routes, hotel markers, and daily activity pins.
    """
    dest_center = resolve_city(destination, fallback=(15.2993, 74.1240))
    origin_coords = resolve_city(origin, fallback=(19.0760, 72.8777))

    # Initialize Folium Map centered on the Destination
    m = folium.Map(
        location=dest_center,
        zoom_start=11,
        tiles="OpenStreetMap",
        control_scale=True
    )

    # Route from Origin to Destination (if distinct and within same country/region)
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

        m.fit_bounds([origin_coords, dest_center], padding=(40, 40))

    circuit_points = [dest_center]

    # Hotel Markers
    hotels = itinerary.get("hotel_options", [])
    if not hotels and "selected_hotel_recommendation" in itinerary:
        hotels = [itinerary["selected_hotel_recommendation"]]

    for h_idx, hotel in enumerate(hotels[:2]):
        hotel_name = hotel.get("name") or hotel.get("hotel_name", f"Hotel in {destination}")
        hotel_cost = hotel.get("price_per_night", "")
        hotel_loc = hotel.get("area_or_neighborhood", destination)
        hotel_coords = resolve_activity_location(f"{hotel_name} {hotel_loc}", dest_center, offset_seed=100 + h_idx)
        
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
            
            slot_coords = resolve_activity_location(
                f"{act_title} {loc_hint}", 
                dest_center=dest_center, 
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

    # Render day sightseeing circuit polyline (only connecting local destination points)
    if len(circuit_points) > 2:
        folium.PolyLine(
            locations=circuit_points[1:],
            color="#6366f1",
            weight=2.5,
            opacity=0.6,
            dash_array="4, 6",
            tooltip="🗺️ Recommended Sightseeing Route in Destination"
        ).add_to(m)

    st_folium(m, width="100%", height=450, returned_objects=[])
