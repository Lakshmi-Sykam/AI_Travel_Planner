from typing import Dict, Any

def get_weather_info(destination: str) -> Dict[str, Any]:
    """
    Get weather overview and climate forecast for travel destination.
    Provides seasonal climate insights and packing recommendations.
    """
    dest_lower = destination.lower()
    
    # Generic climate database heuristics for common destinations
    if "goa" in dest_lower:
        return {
            "temperature_range": "24°C - 33°C",
            "condition": "Pleasant, coastal breeze with sunny afternoons",
            "best_season": "October to March (Peak), Monsoon (June-Sep for lush greens)",
            "clothing_advice": "Light cottons, swimwear, sunglasses, flip-flops, sunscreen SPF 50+"
        }
    elif "manali" in dest_lower or "shimla" in dest_lower or "kashmir" in dest_lower or "ladakh" in dest_lower:
        return {
            "temperature_range": "5°C - 18°C",
            "condition": "Chilly mornings/nights with crisp mountain air",
            "best_season": "March to June (Summer), Dec to Feb (Snow)",
            "clothing_advice": "Thermal innerwear, fleece jackets, sturdy walking boots, woollen caps"
        }
    elif "kerala" in dest_lower or "munnar" in dest_lower:
        return {
            "temperature_range": "20°C - 29°C",
            "condition": "Tropical warmth, lush mist in hill stations",
            "best_season": "September to March",
            "clothing_advice": "Breathable cottons, light layer for hills, umbrella/rain jacket"
        }
    elif "jaipur" in dest_lower or "rajasthan" in dest_lower or "udaipur" in dest_lower:
        return {
            "temperature_range": "15°C - 31°C",
            "condition": "Warm sunny days with cooler desert evenings",
            "best_season": "October to March",
            "clothing_advice": "Cotton shirts, sun hats, scarf for dust/sun, light jacket for evenings"
        }
    elif "dubai" in dest_lower or "paris" in dest_lower or "bali" in dest_lower or "tokyo" in dest_lower:
        return {
            "temperature_range": "22°C - 32°C",
            "condition": "International travel climate standard",
            "best_season": "Spring & Autumn months",
            "clothing_advice": "Smart casuals, comfortable walking shoes, universal power adapter"
        }
    else:
        return {
            "temperature_range": "20°C - 30°C",
            "condition": "Moderate seasonal weather with clear skies",
            "best_season": "October to April",
            "clothing_advice": "Comfortable casual travel attire, sunscreen, walking sneakers"
        }
