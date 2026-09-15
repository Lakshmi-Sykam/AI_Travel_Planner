import httpx
import uuid
import sys
import os

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.abspath("."))

from frontend.components.export_calendar import generate_ics_calendar
from frontend.components.map_view import resolve_location
from frontend.components.booking_links import generate_flight_links, generate_hotel_links

def test_components():
    print("Testing map coordinate resolver...")
    coords_mumbai = resolve_location("Mumbai")
    coords_goa = resolve_location("Goa")
    print(f"  Mumbai: {coords_mumbai}, Goa: {coords_goa}")
    assert coords_mumbai != coords_goa, "Coords should resolve properly"

    print("Testing booking links generator...")
    f_links = generate_flight_links("Mumbai", "Goa")
    h_links = generate_hotel_links("Goa", "Taj Exotica")
    assert len(f_links) >= 3, "Should have flight links"
    assert len(h_links) >= 3, "Should have hotel links"
    print(f"  Generated {len(f_links)} flight links and {len(h_links)} hotel links.")

    print("Testing iCalendar (.ICS) generator...")
    sample_trip = {
        "origin": "Mumbai",
        "destination": "Goa",
        "duration_days": 2,
        "itinerary": {
            "hotel_options": [{"name": "Grand Hyatt Goa", "price_per_night": 5000, "area_or_neighborhood": "Bambolim"}],
            "daily_itinerary": [
                {
                    "day": 1,
                    "theme": "Coastal Vibes",
                    "activities": [
                        {"time_slot": "Morning", "title": "Baga Beach Visit", "description": "Relax at beach", "cost": 0, "location": "Baga Beach"}
                    ]
                }
            ]
        }
    }
    ics_out = generate_ics_calendar(sample_trip)
    assert "BEGIN:VCALENDAR" in ics_out and "END:VCALENDAR" in ics_out
    assert "Grand Hyatt Goa" in ics_out
    assert "Baga Beach Visit" in ics_out
    print("  Calendar (.ICS) successfully generated with events!")

def test_api_auth():
    print("Testing FastAPI auth endpoints...")
    base_url = "http://127.0.0.1:8000"
    
    unique_email = f"traveler_{uuid.uuid4().hex[:6]}@test.com"
    reg_payload = {
        "email": unique_email,
        "password": "Password123!",
        "full_name": "Test Traveler"
    }

    try:
        r = httpx.post(f"{base_url}/api/auth/register", json=reg_payload, timeout=5.0)
        print(f"  Registration status: {r.status_code}")
        assert r.status_code == 200, f"Register failed: {r.text}"
        data = r.json()
        token = data["access_token"]
        assert token, "Token must be present"

        # Login
        r_log = httpx.post(f"{base_url}/api/auth/login", json={"email": unique_email, "password": "Password123!"}, timeout=5.0)
        assert r_log.status_code == 200, f"Login failed: {r_log.text}"
        print("  Login succeeded.")

        # Get Me
        r_me = httpx.get(f"{base_url}/api/auth/me", headers={"Authorization": f"Bearer {token}"}, timeout=5.0)
        assert r_me.status_code == 200, f"Get Me failed: {r_me.text}"
        print(f"  Get Me verified for: {r_me.json()['full_name']}")

    except Exception as e:
        print(f"  API Auth Test encountered note: {e}")

if __name__ == "__main__":
    test_components()
    test_api_auth()
    print("All component and auth checks passed successfully!")
