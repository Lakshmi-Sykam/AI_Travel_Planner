import urllib.parse
import streamlit as st

def generate_flight_links(origin: str, destination: str):
    """Generate direct flight search links."""
    q_str = f"Flights from {origin} to {destination}"
    enc_q = urllib.parse.quote(q_str)
    orig_clean = urllib.parse.quote(origin.strip().lower())
    dest_clean = urllib.parse.quote(destination.strip().lower())
    
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
            "url": f"https://www.skyscanner.com/transport/flights/{orig_clean}/{dest_clean}",
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

def generate_bus_links(origin: str, destination: str):
    """Generate direct bus and sleeper coach booking links."""
    orig_slug = urllib.parse.quote(origin.strip().lower())
    dest_slug = urllib.parse.quote(destination.strip().lower())
    
    return [
        {
            "name": "redBus",
            "url": f"https://www.redbus.in/bus-tickets/{orig_slug}-to-{dest_slug}",
            "icon": "🚌",
            "tag": "Volvo, Sleeper & AC Buses",
            "btn_label": "Book ➔",
            "color": "#dc2626"
        },
        {
            "name": "AbhiBus",
            "url": f"https://www.abhibus.com/bus-ticket-booking/{orig_slug}-to-{dest_slug}",
            "icon": "🎫",
            "tag": "Instant Seat Selection & Deals",
            "btn_label": "Seats ➔",
            "color": "#ea580c"
        },
        {
            "name": "MakeMyTrip Bus",
            "url": f"https://www.makemytrip.com/bus-tickets/{orig_slug}-to-{dest_slug}-bus-ticket-booking.html",
            "icon": "🚍",
            "tag": "Zero Booking Fee & Free Cancellation",
            "btn_label": "Deals ➔",
            "color": "#0284c7"
        },
        {
            "name": "IntrCity SmartBus",
            "url": f"https://www.intrcity.com/bus-tickets/{orig_slug}-to-{dest_slug}",
            "icon": "✨",
            "tag": "Premium Wi-Fi & Lounge Access",
            "btn_label": "Book ➔",
            "color": "#7c3aed"
        }
    ]

def generate_car_rental_links(origin: str, destination: str):
    """Generate direct car rental, self-drive, and outstation cab booking links."""
    orig_clean = urllib.parse.quote(origin.strip().lower())
    dest_clean = urllib.parse.quote(destination.strip().lower())
    
    return [
        {
            "name": "MakeMyTrip Outstation Cabs",
            "url": f"https://www.makemytrip.com/cabs/outstation-{orig_clean}-to-{dest_clean}-cabs.html",
            "icon": "🚗",
            "tag": "One-Way & Roundtrip Cabs",
            "btn_label": "Book ➔",
            "color": "#2563eb"
        },
        {
            "name": "Zoomcar (Self-Drive)",
            "url": f"https://www.zoomcar.com/in/{orig_clean}/search",
            "icon": "🔑",
            "tag": "Self-Drive Rental Cars by Hour/Day",
            "btn_label": "Rent ➔",
            "color": "#059669"
        },
        {
            "name": "Savaari Car Rentals",
            "url": f"https://www.savaari.com/{orig_clean}-to-{dest_clean}-cab",
            "icon": "🚕",
            "tag": "Chauffeur-Driven Outstation Taxis",
            "btn_label": "Book ➔",
            "color": "#d97706"
        },
        {
            "name": "Uber Intercity",
            "url": "https://www.uber.com/in/en/ride/intercity/",
            "icon": "⚡",
            "tag": "On-Demand Highway Cabs",
            "btn_label": "Ride ➔",
            "color": "#0f172a"
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
            "name": "MakeMyTrip Activities",
            "url": f"https://www.makemytrip.com/activities/{dest_enc}-things-to-do.html",
            "icon": "🗺️",
            "tag": "Local Sightseeing & Experiences",
            "btn_label": "Explore ➔",
            "color": "#4a90e2"
        }
    ]

def render_booking_hub(origin: str, destination: str, hotel_name: str = "", *args, **kwargs):
    """
    Renders the instant 1-Click Multi-Modal Booking Engine Hub with:
    - Train (IRCTC)
    - Flights
    - Bus & Coaches (redBus, AbhiBus)
    - Car Rentals & Outstation Cabs (MakeMyTrip, Zoomcar, Savaari)
    - Hotels & Resorts
    - Tours & Experiences
    """
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border: 1.5px solid #10b981; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #065f46; display: flex; align-items: center; gap: 8px;">
            🎫 Instant 1-Click Booking Engine Hub
        </h4>
        <p style="margin: 4px 0 0 0; font-size: 0.85rem; color: #047857;">
            Compare live prices, check train seats, book sleeper buses, reserve rental cars/cabs, and secure hotels directly across top platforms.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab_train, tab_flight, tab_bus, tab_car, tab_hotel, tab_activity = st.tabs([
        "🚆 Trains (IRCTC)", 
        "✈️ Flights", 
        "🚌 Bus & Coach", 
        "🚗 Car Rentals & Cabs", 
        "🏨 Hotels & Resorts", 
        "🎟️ Tours & Sightseeing"
    ])

    # 1. Train Tickets
    with tab_train:
        st.markdown(f"**🚆 Direct Trains & Rail Passes: {origin} ➔ {destination}**")
        t_cols = st.columns(4)
        for idx, item in enumerate(generate_train_links(origin, destination)):
            with t_cols[idx % 4]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #bbf7d0; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #166534; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #dcfce7; color: #15803d; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # 2. Flights
    with tab_flight:
        st.markdown(f"**✈️ Flight Search & Fare Comparison: {origin} ➔ {destination}**")
        f_cols = st.columns(3)
        for idx, item in enumerate(generate_flight_links(origin, destination)):
            with f_cols[idx % 3]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #bfdbfe; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #1e40af; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #dbeafe; color: #1d4ed8; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # 3. Bus & Coach
    with tab_bus:
        st.markdown(f"**🚌 Sleeper & Volvo Bus Bookings: {origin} ➔ {destination}**")
        b_cols = st.columns(4)
        for idx, item in enumerate(generate_bus_links(origin, destination)):
            with b_cols[idx % 4]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #fecaca; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #991b1b; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #fee2e2; color: #b91c1c; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # 4. Car Rentals & Cabs
    with tab_car:
        st.markdown(f"**🚗 Self-Drive Rentals & Outstation Cabs: {origin} ➔ {destination}**")
        c_cols = st.columns(4)
        for idx, item in enumerate(generate_car_rental_links(origin, destination)):
            with c_cols[idx % 4]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #fed7aa; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #9a3412; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #ffedd5; color: #c2410c; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # 5. Hotels & Resorts
    with tab_hotel:
        st.markdown(f"**🏨 Top Stays & Resorts in {destination}**")
        h_cols = st.columns(3)
        for idx, item in enumerate(generate_hotel_links(destination, hotel_name)):
            with h_cols[idx % 3]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #fef08a; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #854d0e; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #fef9c3; color: #a16207; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # 6. Activities & Tours
    with tab_activity:
        st.markdown(f"**🎟️ Guided Tours, Entry Passes & Water Sports in {destination}**")
        a_cols = st.columns(3)
        for idx, item in enumerate(generate_activities_links(destination)):
            with a_cols[idx % 3]:
                st.markdown(f"""
                <a href="{item['url']}" target="_blank" style="text-decoration: none;">
                    <div style="background: white; border: 1.5px solid #e9d5ff; border-radius: 10px; padding: 12px; margin-bottom: 10px; min-height: 95px; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.04);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 700; color: #6b21a8; font-size: 0.92rem;">{item['icon']} {item['name']}</span>
                            <span style="font-size: 0.70rem; background: #f3e8ff; color: #7e22ce; padding: 2px 7px; border-radius: 8px; font-weight: 700;">{item['btn_label']}</span>
                        </div>
                        <div style="font-size: 0.76rem; color: #64748b; margin-top: 6px;">{item['tag']}</div>
                    </div>
                </a>
                """, unsafe_allow_html=True)

    # Quick Train PNR & Route Checker
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
