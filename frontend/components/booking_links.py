import urllib.parse
import streamlit as st

def generate_flight_links(origin: str, destination: str):
    """Generate direct flight search links."""
    q_str = f"Flights from {origin} to {destination}"
    enc_q = urllib.parse.quote(q_str)
    
    return [
        {
            "name": "Google Flights",
            "url": f"https://www.google.com/travel/flights?q={enc_q}",
            "icon": "✈️",
            "tag": "Live Price Tracking",
            "btn_label": "Search ➔",
            "color": "#0284c7"
        },
        {
            "name": "Skyscanner",
            "url": f"https://www.skyscanner.com/transport/flights/{urllib.parse.quote(origin.lower())}/{urllib.parse.quote(destination.lower())}",
            "icon": "🌐",
            "tag": "Cheapest Month Deals",
            "btn_label": "Deals ➔",
            "color": "#0284c7"
        },
        {
            "name": "MakeMyTrip Flights",
            "url": f"https://www.makemytrip.com/flight/search?itinerary={urllib.parse.quote(origin)}-{urllib.parse.quote(destination)}",
            "icon": "🎫",
            "tag": "Domestic Deals",
            "btn_label": "Book ➔",
            "color": "#0284c7"
        }
    ]

def generate_train_links(origin: str, destination: str):
    """Generate direct train and rail search links for Indian Railways (IRCTC) & global rail."""
    clean_orig = urllib.parse.quote(origin.strip())
    clean_dest = urllib.parse.quote(destination.strip())
    
    return [
        {
            "name": "IRCTC Official Rail",
            "url": "https://www.irctc.co.in/nget/train-search",
            "icon": "🚆",
            "tag": "Official Railway Booking",
            "btn_label": "Book ➔",
            "color": "#16a34a"
        },
        {
            "name": "ConfirmTkt (Tatkal)",
            "url": f"https://www.confirmtkt.com/trains/search?from={clean_orig}&to={clean_dest}",
            "icon": "🎟️",
            "tag": "Tatkal & Seat Predictor",
            "btn_label": "Seats ➔",
            "color": "#16a34a"
        },
        {
            "name": "MakeMyTrip Rail",
            "url": f"https://www.makemytrip.com/railways/{clean_orig}-to-{clean_dest}-train-tickets.html",
            "icon": "⚡",
            "tag": "Zero Cancellation Fee",
            "btn_label": "Book ➔",
            "color": "#16a34a"
        },
        {
            "name": "ixigo Trains",
            "url": f"https://www.ixigo.com/trains/{clean_orig}-to-{clean_dest}-trains",
            "icon": "📍",
            "tag": "Live Running Status & PNR",
            "btn_label": "Status ➔",
            "color": "#16a34a"
        }
    ]

def generate_hotel_links(destination: str, hotel_name: str = ""):
    """Generate direct hotel search links."""
    dest_enc = urllib.parse.quote(destination)
    query_enc = urllib.parse.quote(f"{hotel_name} {destination}" if hotel_name else destination)
    
    return [
        {
            "name": "Booking.com",
            "url": f"https://www.booking.com/searchresults.html?ss={dest_enc}",
            "icon": "🏨",
            "tag": "Free Cancellation Deals",
            "btn_label": "Deals ➔",
            "color": "#003580"
        },
        {
            "name": "Agoda",
            "url": f"https://www.agoda.com/search?text={dest_enc}",
            "icon": "🌴",
            "tag": "VIP Stays & Resort Rates",
            "btn_label": "Deals ➔",
            "color": "#5392f9"
        },
        {
            "name": "TripAdvisor Hotels",
            "url": f"https://www.tripadvisor.com/Search?q={query_enc}",
            "icon": "🦉",
            "tag": "Verified Reviews & Rates",
            "btn_label": "Deals ➔",
            "color": "#34e0a1"
        }
    ]

def generate_activities_links(destination: str):
    """Generate direct tour and activity booking links."""
    dest_enc = urllib.parse.quote(destination)
    
    return [
        {
            "name": "GetYourGuide",
            "url": f"https://www.getyourguide.com/s/?q={dest_enc}",
            "icon": "🎟️",
            "tag": "Skip-the-Line Entry Passes",
            "btn_label": "Tickets ➔",
            "color": "#ff5533"
        },
        {
            "name": "Viator (TripAdvisor)",
            "url": f"https://www.viator.com/search/{dest_enc}",
            "icon": "⛵",
            "tag": "Guided Day Trips & Tours",
            "btn_label": "Tickets ➔",
            "color": "#008768"
        },
        {
            "name": "Rome2Rio Transit",
            "url": f"https://www.rome2rio.com/s/Mumbai/{dest_enc}",
            "icon": "🗺️",
            "tag": "Bus, Train & Ferry Routes",
            "btn_label": "Tickets ➔",
            "color": "#4a90e2"
        }
    ]

def render_booking_hub(origin: str, destination: str, hotel_name: str = "", *args, **kwargs):
    """
    Renders the instant 4-Column Booking Hub showing Train Tickets (IRCTC), Flights, Hotels, and Tours side-by-side.
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border: 1.5px solid #10b981; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #065f46; display: flex; align-items: center; gap: 8px;">
            🎫 Instant 1-Click Booking Engine Hub
        </h4>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #047857;">
            Compare live prices, check IRCTC train seat availability, and book your tickets across top global platforms.
        </p>
    </div>
    """, unsafe_allow_html=True)

    b_col1, b_col2, b_col3, b_col4 = st.columns(4)

    # 1. Train Tickets (IRCTC & Partners)
    with b_col1:
        st.markdown("#### 🚆 Train Tickets")
        for item in generate_train_links(origin, destination):
            st.markdown(f"""
            <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                <div style="background: white; border: 1.5px solid #bbf7d0; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; min-height: 85px; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #166534; font-size: 0.90rem;">{item['icon']} {item['name']}</span>
                        <span style="font-size: 0.70rem; background: #dcfce7; color: #15803d; padding: 2px 6px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                    </div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">{item['tag']}</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # 2. Flights & Transit
    with b_col2:
        st.markdown("#### ✈️ Flights & Transit")
        for item in generate_flight_links(origin, destination):
            st.markdown(f"""
            <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; min-height: 85px; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #1e293b; font-size: 0.90rem;">{item['icon']} {item['name']}</span>
                        <span style="font-size: 0.70rem; background: #e0f2fe; color: #0369a1; padding: 2px 6px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                    </div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">{item['tag']}</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # 3. Hotels & Stays
    with b_col3:
        st.markdown("#### 🏨 Hotels & Resorts")
        for item in generate_hotel_links(destination, hotel_name):
            st.markdown(f"""
            <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; min-height: 85px; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #1e293b; font-size: 0.90rem;">{item['icon']} {item['name']}</span>
                        <span style="font-size: 0.70rem; background: #fef3c7; color: #b45309; padding: 2px 6px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                    </div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">{item['tag']}</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # 4. Tours & Experiences
    with b_col4:
        st.markdown("#### 🎟️ Tours & Sightseeing")
        for item in generate_activities_links(destination):
            st.markdown(f"""
            <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                <div style="background: white; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 12px; margin-bottom: 10px; min-height: 85px; transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,0,0,0.03);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 700; color: #1e293b; font-size: 0.90rem;">{item['icon']} {item['name']}</span>
                        <span style="font-size: 0.70rem; background: #f3e8ff; color: #7e22ce; padding: 2px 6px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                    </div>
                    <div style="font-size: 0.74rem; color: #64748b; margin-top: 4px;">{item['tag']}</div>
                </div>
            </a>
            """, unsafe_allow_html=True)

    # Quick Train PNR / Live Status Tool Widget
    with st.expander("🔍 Live Train PNR & Running Status Quick Checker", expanded=False):
        pnr_col1, pnr_col2 = st.columns([3, 1])
        with pnr_col1:
            pnr_input = st.text_input("Enter 10-Digit PNR Number or Train Number / Name", placeholder="e.g. 12051 (Jan Shatabdi) or 4512398712", key=f"pnr_tool_input_{origin}_{destination}")
        with pnr_col2:
            st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
            if pnr_input:
                clean_pnr = urllib.parse.quote(pnr_input.strip())
                check_url = f"https://www.confirmtkt.com/pnr-status/{clean_pnr}" if len(pnr_input.strip()) == 10 and pnr_input.strip().isdigit() else f"https://www.confirmtkt.com/train-running-status/{clean_pnr}"
                st.markdown(f'<a href="{check_url}" target="_blank"><button style="background: #16a34a; color: white; border: none; padding: 8px 16px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%;">Check Status ➔</button></a>', unsafe_allow_html=True)
            else:
                st.button("Check Status", disabled=True, use_container_width=True, key=f"pnr_btn_disabled_{origin}_{destination}")
