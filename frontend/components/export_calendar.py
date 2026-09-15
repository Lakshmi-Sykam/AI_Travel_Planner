from datetime import datetime, timedelta
import uuid

def generate_ics_calendar(trip_data: dict) -> str:
    """
    Generate standard iCalendar (.ics) format string from a synthesized trip plan.
    Enables one-click import into Google Calendar, Apple Calendar, and Outlook.
    """
    itinerary = trip_data.get("itinerary", {})
    origin = trip_data.get("origin", "Origin")
    destination = trip_data.get("destination", "Destination")
    daily_plans = itinerary.get("daily_itinerary", [])
    
    start_date = datetime.now() + timedelta(days=1)
    
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//AI Travel Planning Agent//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        f"X-WR-CALNAME:Trip to {destination}",
        "X-WR-TIMEZONE:UTC",
    ]
    
    # 1. Hotel Event
    hotels = itinerary.get("hotel_options", [])
    if not hotels and "selected_hotel_recommendation" in itinerary:
        hotels = [itinerary["selected_hotel_recommendation"]]

    if hotels:
        first_hotel = hotels[0]
        hotel_name = first_hotel.get("name") or first_hotel.get("hotel_name", f"Hotel in {destination}")
        hotel_loc = first_hotel.get("area_or_neighborhood", destination)
        hotel_cost = first_hotel.get("price_per_night", "")
        
        checkin_dt = start_date.replace(hour=14, minute=0, second=0)
        checkout_dt = (start_date + timedelta(days=len(daily_plans) or 1)).replace(hour=11, minute=0, second=0)
        
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:hotel-{uuid.uuid4()}@aitravelplanner.ai",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{checkin_dt.strftime('%Y%m%dT%H%M%S')}",
            f"DTEND:{checkout_dt.strftime('%Y%m%dT%H%M%S')}",
            f"SUMMARY:🏨 Hotel Stay: {hotel_name}",
            f"LOCATION:{hotel_loc}",
            f"DESCRIPTION:Accommodation: {hotel_name}\\nPrice: {hotel_cost}/night\\nPlanned with AI Travel Planner",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])
        
    # 2. Daily Activities
    slot_hours = {
        "Morning": (9, 12),
        "Afternoon": (13, 17),
        "Evening": (18, 21),
        "Night": (21, 23),
    }

    for d_idx, day_plan in enumerate(daily_plans):
        current_day_date = start_date + timedelta(days=d_idx)
        day_num = day_plan.get("day", d_idx + 1)
        theme = day_plan.get("theme", f"Day {day_num} Exploration")
        activities = day_plan.get("activities", [])

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
            time_slot = act.get("time_slot", "Morning")
            act_desc = act.get("description", "")
            act_cost = act.get("cost", "N/A")
            act_loc = act.get("location", destination)

            start_h, end_h = slot_hours.get(time_slot, (10, 12))
            event_start = current_day_date.replace(hour=start_h, minute=0, second=0)
            event_end = current_day_date.replace(hour=end_h, minute=0, second=0)
            
            clean_desc = f"Day {day_num} ({time_slot}): {theme}\\n\\nDetails: {act_desc}\\n\\nEstimated Cost: {act_cost}".replace("\n", "\\n")

            ics_lines.extend([
                "BEGIN:VEVENT",
                f"UID:act-{uuid.uuid4()}@aitravelplanner.ai",
                f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART:{event_start.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND:{event_end.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:Day {day_num} ({time_slot}): {act_title}",
                f"LOCATION:{act_loc}",
                f"DESCRIPTION:{clean_desc}",
                "STATUS:CONFIRMED",
                "END:VEVENT"
            ])

    ics_lines.append("END:VCALENDAR")
    return "\r\n".join(ics_lines)
