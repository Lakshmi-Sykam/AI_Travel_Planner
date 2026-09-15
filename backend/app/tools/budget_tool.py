from typing import Dict, Any

def analyze_and_distribute_budget(
    total_budget: float, 
    duration_days: int, 
    travel_style: str = "Budget",
    currency: str = "INR"
) -> Dict[str, Any]:
    """
    Computes recommended budget allocations based on style and duration.
    Calculates reasonable split across Transit, Hotels, Food, Activities, and Buffer.
    """
    style_lower = travel_style.lower()
    
    # Define allocation percentages according to travel style
    if "backpacker" in style_lower or "budget" in style_lower:
        transport_pct = 0.32
        hotel_pct = 0.28
        food_pct = 0.22
        activity_pct = 0.12
        buffer_pct = 0.06
    elif "luxury" in style_lower:
        transport_pct = 0.25
        hotel_pct = 0.45
        food_pct = 0.18
        activity_pct = 0.08
        buffer_pct = 0.04
    else:  # Moderate / Standard / Family / Solo
        transport_pct = 0.30
        hotel_pct = 0.35
        food_pct = 0.20
        activity_pct = 0.10
        buffer_pct = 0.05

    transport_alloc = round(total_budget * transport_pct, 2)
    hotel_alloc = round(total_budget * hotel_pct, 2)
    food_alloc = round(total_budget * food_pct, 2)
    activity_alloc = round(total_budget * activity_pct, 2)
    buffer_alloc = round(total_budget * buffer_pct, 2)
    
    hotel_per_night = round(hotel_alloc / max(1, duration_days - 1), 2)
    food_per_day = round(food_alloc / duration_days, 2)
    activity_per_day = round(activity_alloc / duration_days, 2)

    is_tight = (total_budget / max(1, duration_days)) < (2500 if currency == "INR" else 40)

    advice = (
        "Budget is tight for this duration. Consider staying in reputable youth hostels/guesthouses, "
        "using sleeper trains/state buses, and enjoying authentic street food or local thalis."
        if is_tight else
        "Comfortable budget. Allows for AC train/budget flights, boutique 3-star stays or Airbnbs, "
        "and balanced cafe & restaurant dining."
    )

    return {
        "transport_target": transport_alloc,
        "hotel_target": hotel_alloc,
        "hotel_per_night_target": hotel_per_night,
        "food_target": food_alloc,
        "food_per_day_target": food_per_day,
        "activity_target": activity_alloc,
        "activity_per_day_target": activity_per_day,
        "buffer_target": buffer_alloc,
        "is_tight_budget": is_tight,
        "budget_advice": advice,
        "currency": currency
    }
