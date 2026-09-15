import streamlit as st
import httpx
import json
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

import importlib
import components.booking_links
import components.auth_ui
importlib.reload(components.booking_links)
importlib.reload(components.auth_ui)
from components.booking_links import render_booking_hub
from components.export_pdf import generate_pdf_itinerary
from components.export_calendar import generate_ics_calendar
from components.map_view import render_interactive_map
from components.auth_ui import render_login_page, render_user_profile_sidebar

# Page configuration
st.set_page_config(
    page_title="AI Travel Planning Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Modern Luxury Travel Ambient Background */
    .stApp {
        background: linear-gradient(180deg, rgba(240, 249, 255, 0.90) 0%, rgba(248, 250, 252, 0.94) 100%),
                    url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=2400&q=80') !important;
        background-attachment: fixed !important;
        background-size: cover !important;
        background-position: center top !important;
    }

    /* Sidebar Luxury Glass Effect */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.92) 0%, rgba(241, 245, 249, 0.96) 100%) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-right: 1.5px solid rgba(2, 132, 199, 0.15) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.04) !important;
    }

    /* Main Hero Header Banner */
    .main-header {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 40%, #0f172a 100%);
        padding: 2.2rem 2.4rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 16px 36px -8px rgba(2, 132, 199, 0.35), 0 0 0 1px rgba(255, 255, 255, 0.15) inset;
        position: relative;
        overflow: hidden;
    }

    .main-header::after {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 320px;
        height: 320px;
        background: radial-gradient(circle, rgba(56, 189, 248, 0.25) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    
    /* Modern Glassmorphic Cards & Forms */
    .stForm, div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.90) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border: 1.5px solid rgba(226, 232, 240, 0.9) !important;
        border-radius: 20px !important;
        padding: 1.8rem 2rem !important;
        box-shadow: 0 12px 32px rgba(15, 23, 42, 0.06) !important;
    }

    .agent-card {
        background: rgba(255, 255, 255, 0.94);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(203, 213, 225, 0.8);
        border-radius: 14px;
        padding: 1.3rem;
        margin-bottom: 1rem;
        transition: all 0.25s ease;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
    }
    .agent-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 24px rgba(2, 132, 199, 0.12);
        border-color: #38bdf8;
    }

    /* Metric Cards Glass Elevation */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        border: 1.5px solid rgba(226, 232, 240, 0.9) !important;
        border-radius: 16px !important;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.04) !important;
        transition: transform 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px) !important;
        border-color: #0284c7 !important;
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.12) !important;
    }

    /* Modern Tabs Styling */
    div[data-baseweb="tab-list"] {
        background: rgba(241, 245, 249, 0.85) !important;
        backdrop-filter: blur(10px) !important;
        padding: 6px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(203, 213, 225, 0.8) !important;
        gap: 8px !important;
    }
    div[data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 20px !important;
        color: #475569 !important;
        transition: all 0.2s ease !important;
    }
    div[data-baseweb="tab"][aria-selected="true"] {
        background: #0284c7 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.35) !important;
    }

    /* Badges */
    .badge-pill {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        margin-right: 6px;
        margin-bottom: 6px;
        letter-spacing: 0.3px;
    }
    .badge-blue { background: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }
    .badge-green { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-purple { background: #f3e8ff; color: #7e22ce; border: 1px solid #e9d5ff; }
    .badge-amber { background: #fef3c7; color: #b45309; border: 1px solid #fde68a; }

    /* Buttons */
    .stButton>button {
        border-radius: 12px;
        font-weight: 700;
        padding: 0.65rem 1.4rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.25);
    }
</style>
""", unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:8000"

# Session State Initialization
if "current_trip" not in st.session_state:
    st.session_state.current_trip = None
if "agent_logs" not in st.session_state:
    st.session_state.agent_logs = []
if "saved_trips" not in st.session_state:
    st.session_state.saved_trips = []
if "auth_token" not in st.session_state:
    st.session_state.auth_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

# Gating: Display Authentication Page FIRST if user is not logged in
if not st.session_state.auth_token or not st.session_state.user_info:
    render_login_page(BACKEND_URL)
    st.stop()

# Helper: Check backend status
def check_backend():
    try:
        r = httpx.get(f"{BACKEND_URL}/health", timeout=3.0)
        return r.status_code == 200, r.json() if r.status_code == 200 else {}
    except Exception:
        return False, {}

# Helper: Fetch saved trips
def fetch_saved_trips(mine_only: bool = False):
    try:
        headers = {}
        if st.session_state.auth_token:
            headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
        
        params = {"mine_only": mine_only} if st.session_state.auth_token else {}
        r = httpx.get(f"{BACKEND_URL}/api/trips", headers=headers, params=params, timeout=5.0)
        if r.status_code == 200:
            st.session_state.saved_trips = r.json()
    except Exception:
        pass

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/airplane-take-off.png", width=60)
    st.title("Travel Agent AI")
    st.caption("Multi-Agent Itinerary Orchestrator")
    
    # User Profile & Logout Widget
    render_user_profile_sidebar()
    
    is_online, health_data = check_backend()
    if is_online:
        st.success("🟢 Backend & Agent Engine Active")
        groq_cfg = health_data.get("groq_configured", False)
        model_name = health_data.get("llm_model", "llama-3.3-70b-versatile")
        if groq_cfg:
            st.info(f"⚡ LLM: **Groq ({model_name})**")
        else:
            st.warning("⚠️ Groq API key not set in `.env` (Smart Fallback Engine Active)")
    else:
        st.error("🔴 Backend Offline (Start FastAPI server on :8000)")

    st.divider()
    st.subheader("📚 Saved Trips")
    
    # Trip Filter toggle for logged in users
    mine_filter = False
    if st.session_state.user_info:
        filter_option = st.radio("Trip Filter", ["All Community Trips", "My Saved Trips"], index=1, horizontal=True)
        mine_filter = (filter_option == "My Saved Trips")

    if st.button("🔄 Refresh Trips", use_container_width=True):
        fetch_saved_trips(mine_only=mine_filter)
    
    fetch_saved_trips(mine_only=mine_filter)
    
    if st.session_state.saved_trips:
        for trip in st.session_state.saved_trips[:8]:
            t_col1, t_col2 = st.columns([4, 1])
            with t_col1:
                label = f"📍 {trip['origin']} ➔ {trip['destination']} ({trip['duration_days']}D)"
                if st.button(label, key=f"trip_btn_{trip['id']}", use_container_width=True):
                    st.session_state.current_trip = trip
                    st.rerun()
            with t_col2:
                if st.button("🗑️", key=f"del_btn_{trip['id']}", help="Delete trip"):
                    headers = {}
                    if st.session_state.auth_token:
                        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
                    try:
                        httpx.delete(f"{BACKEND_URL}/api/trips/{trip['id']}", headers=headers, timeout=5.0)
                        fetch_saved_trips(mine_only=mine_filter)
                        st.rerun()
                    except Exception:
                        pass
    else:
        st.caption("No trips found. Generate your first journey!")

# Main Header Banner
st.markdown("""
<div class="main-header">
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.16); backdrop-filter: blur(8px); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 9999px; padding: 5px 18px; font-size: 0.82rem; font-weight: 800; letter-spacing: 0.6px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        🌿 AUTONOMOUS MULTI-AGENT TRAVEL DASHBOARD
    </div>
    <h1 style="margin:0; font-size: 2.5rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 10px rgba(0,0,0,0.3);">✈️ AI Travel Planning Agent</h1>
    <p style="margin: 0.6rem 0 0.8rem 0; opacity: 0.95; font-size: 1.08rem; font-weight: 400; max-width: 850px; text-shadow: 0 1px 4px rgba(0,0,0,0.2);">
        Orchestrating autonomous route discovery, smart budget distribution, interactive maps, live booking links & itinerary exports.
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab_create, tab_itinerary, tab_refine = st.tabs(["✨ Plan New Trip", "📋 Itinerary Dashboard", "💬 Modify Plan"])

# TAB 1: Plan New Trip
with tab_create:
    st.subheader("🎯 Configure Your Journey")
    
    with st.form("trip_form"):
        col1, col2 = st.columns(2)
        with col1:
            origin = st.text_input("🛫 Starting From (Origin)", value="Mumbai", placeholder="e.g. Mumbai, Delhi, New York")
            destination = st.text_input("🏖️ Destination", value="Goa", placeholder="e.g. Goa, Manali, Paris, Dubai")
            duration_days = st.slider("📅 Duration (Days)", min_value=1, max_value=14, value=4)
            group_size = st.number_input("👥 Number of Members / Travelers", min_value=1, max_value=30, value=2, step=1, help="Total number of people going on this journey")
        
        with col2:
            currency = st.selectbox("💱 Currency", options=["INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"], index=0)
            curr_code = currency.split()[0]
            
            default_budget = 20000.0 if curr_code == "INR" else 500.0
            max_budget = 200000.0 if curr_code == "INR" else 5000.0
            step_budget = 1000.0 if curr_code == "INR" else 50.0
            
            budget = st.number_input(
                f"💰 Total Budget ({curr_code})", 
                min_value=1000.0 if curr_code == "INR" else 50.0, 
                max_value=max_budget, 
                value=default_budget, 
                step=step_budget
            )
            
            travel_style = st.selectbox(
                "🎒 Travel Style",
                options=[
                    "Budget / Backpacker",
                    "Balanced & Relaxed",
                    "Romantic / Honeymoon",
                    "Adventure & Thrill",
                    "Family Friendly",
                    "Luxury & Boutique"
                ],
                index=0
            )

            preferred_transport = st.selectbox(
                "🚆 Preferred Transport Mode",
                options=[
                    "🌟 Any / Best AI Match",
                    "🚆 Train / Railway (IRCTC)",
                    "✈️ Flight / Airplane",
                    "🚗 Car / Self-Drive Cab / Road Trip",
                    "🚌 Bus / Coach"
                ],
                index=0,
                help="Tell the AI Agent whether to prioritize Trains, Flights, or Road/Cab routes."
            )

        st.markdown("**🎨 Select Traveler Interests & Vibe**")
        interests_list = [
            "🏖️ Beaches & Watersports",
            "🏛️ Heritage & Monuments",
            "🍲 Street Food & Local Dining",
            "🌄 Nature, Hikes & Scenic Views",
            "🎉 Nightlife & Music",
            "🛍️ Shopping & Flea Markets",
            "🧘 Wellness, Yoga & Spa",
            "📸 Photography Spots"
        ]
        selected_interests = st.multiselect(
            "Interests",
            options=interests_list,
            default=["🏖️ Beaches & Watersports", "🍲 Street Food & Local Dining", "🏛️ Heritage & Monuments"]
        )

        special_reqs = st.text_area(
            "📝 Special Notes or Preferences (Optional)",
            placeholder="e.g. Prefer vegetarian food, need train sleeper class or rental car info, traveling with friends."
        )

        submitted = st.form_submit_button("🚀 Orchestrate AI Travel Plan", use_container_width=True)

    if submitted:
        if not origin or not destination:
            st.error("Please enter both origin and destination.")
        else:
            with st.status(f"🤖 Multi-Agent Orchestrator planning for {group_size} travelers ({preferred_transport})...", expanded=True) as status:
                st.write("🔍 **Tool Orchestrator:** Analyzing weather trends & calculating budget distribution...")
                st.write(f"✈️ **Travel Agent:** Scouting optimal transit routes ({preferred_transport}) & pricing...")
                st.write(f"🏨 **Hotel Agent:** Selecting prime accommodations matching budget...")
                st.write("🏖️ **Activity Agent:** Crafting day-by-day sightseeing and culinary highlights...")
                st.write("⚖️ **Synthesis Agent:** Verifying financial balance & final itinerary...")

                payload = {
                    "origin": origin,
                    "destination": destination,
                    "duration_days": duration_days,
                    "budget": budget,
                    "currency": curr_code,
                    "travel_style": travel_style,
                    "preferred_transport": preferred_transport,
                    "interests": [i.split(" ", 1)[-1] for i in selected_interests],
                    "group_size": int(group_size),
                    "special_requirements": special_reqs
                }

                try:
                    headers = {}
                    if st.session_state.auth_token:
                        headers["Authorization"] = f"Bearer {st.session_state.auth_token}"
                    
                    res = httpx.post(f"{BACKEND_URL}/api/plan-trip", json=payload, headers=headers, timeout=60.0)
                    if res.status_code == 200:
                        data = res.json()
                        st.session_state.current_trip = {
                            "id": data["trip_id"],
                            "origin": origin,
                            "destination": destination,
                            "duration_days": duration_days,
                            "budget": budget,
                            "currency": curr_code,
                            "travel_style": travel_style,
                            "group_size": int(group_size),
                            "itinerary": data["itinerary"]
                        }
                        st.session_state.agent_logs = data.get("raw_logs", {}).get("logs", [])
                        status.update(label="✅ Itinerary Successfully Generated!", state="complete", expanded=False)
                        st.balloons()
                        st.success("Your plan is ready! Switch to the **📋 Itinerary Dashboard** tab to view.")
                    else:
                        status.update(label="❌ Failed to generate plan", state="error")
                        st.error(f"Error {res.status_code}: {res.text}")
                except Exception as e:
                    status.update(label="❌ Connection Error", state="error")
                    st.error(f"Could not connect to backend: {e}")

# TAB 2: Itinerary Dashboard
with tab_itinerary:
    current = st.session_state.current_trip
    if not current:
        st.info("👈 Please create a plan in the 'Plan New Trip' tab or select a saved trip from the sidebar.")
    else:
        itinerary = current.get("itinerary", {})
        budget_data = itinerary.get("budget_breakdown", {})
        g_size = current.get("group_size", 1)

        # Header summary
        st.markdown(f"## 📍 {current['origin']} to {current['destination']} ({current['duration_days']} Days • 👥 {g_size} {'Member' if g_size == 1 else 'Members'})")
        
        col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
        with col_s1:
            st.metric("Total Budget", f"{current['currency']} {current['budget']:,.0f}")
        with col_s2:
            est_cost = budget_data.get("total_estimated_cost", current['budget'])
            st.metric("Estimated Cost", f"{current['currency']} {est_cost:,.0f}", delta=f"{current['currency']} {current['budget'] - est_cost:,.0f} remaining")
        with col_s3:
            per_person = est_cost / g_size if g_size > 0 else est_cost
            st.metric("Cost Per Person", f"{current['currency']} {per_person:,.0f}")
        with col_s4:
            st.metric("👥 Members", f"{g_size} {'Person' if g_size == 1 else 'Persons'}")
        with col_s5:
            st.metric("Best Season", itinerary.get("best_time_to_visit", "Oct - Mar"))

        # Overview & Weather
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.94); backdrop-filter: blur(12px); border: 1.5px solid rgba(226, 232, 240, 0.9); padding: 1.2rem 1.5rem; border-radius: 16px; margin: 1.2rem 0; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.04);">
            <p style="margin:0 0 0.5rem 0; font-size:1.08rem; color:#0f172a; font-weight:500; line-height:1.6;">{itinerary.get('destination_overview', '')}</p>
            <div style="display:inline-flex; align-items:center; gap:6px; background:#f0fdf4; border:1px solid #bbf7d0; padding:4px 12px; border-radius:9999px; margin-top:4px;">
                <span style="font-size:0.92rem; color:#15803d; font-weight:700;">🌤️ Weather Forecast:</span>
                <span style="font-size:0.92rem; color:#166534; font-weight:600;">{itinerary.get('weather_forecast_summary', '')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 1-Click Booking Hub
        hotel_list = itinerary.get("hotel_options", [])
        top_hotel = hotel_list[0].get("name", "") if hotel_list else ""
        render_booking_hub(current["origin"], current["destination"], top_hotel)

        # Interactive Map Section
        st.markdown("### 🗺️ Interactive Route & Sightseeing Map")
        st.caption("Explore interactive pins for accommodation, daily attractions, and transit paths.")
        try:
            render_interactive_map(itinerary, current["origin"], current["destination"])
        except Exception as e:
            st.caption(f"Map notice: {e}")

        st.divider()

        # Budget Donut Chart & Category Breakdown
        st.markdown("### 💰 Budget & Expense Analysis")
        col_b1, col_b2 = st.columns([1, 1])
        
        with col_b1:
            labels = ['Transportation', 'Accommodation', 'Food & Dining', 'Activities & Entry', 'Contingency Buffer']
            values = [
                budget_data.get('transportation', 0),
                budget_data.get('accommodation', 0),
                budget_data.get('food_and_dining', 0),
                budget_data.get('activities_and_entry', 0),
                budget_data.get('emergency_buffer', 0)
            ]
            
            fig = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=.45,
                marker=dict(colors=['#0284c7', '#38bdf8', '#10b981', '#f59e0b', '#8b5cf6'])
            )])
            fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=260)
            st.plotly_chart(fig, use_container_width=True)

        with col_b2:
            st.markdown(f"""
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 1rem;">
                <h4 style="margin:0 0 0.5rem 0; color:#0f172a;">💡 Budget Optimization Advice</h4>
                <p style="color:#334155; font-size:0.95rem; margin-bottom: 0.8rem;">{budget_data.get('budget_advice', '')}</p>
                <div style="font-size:0.88rem; color:#64748b;">
                    <div>• <b>Transit:</b> {current['currency']} {budget_data.get('transportation', 0):,.0f}</div>
                    <div>• <b>Hotels:</b> {current['currency']} {budget_data.get('accommodation', 0):,.0f}</div>
                    <div>• <b>Food:</b> {current['currency']} {budget_data.get('food_and_dining', 0):,.0f}</div>
                    <div>• <b>Activities:</b> {current['currency']} {budget_data.get('activities_and_entry', 0):,.0f}</div>
                    <div>• <b>Buffer:</b> {current['currency']} {budget_data.get('emergency_buffer', 0):,.0f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Day by Day Schedule
        st.markdown("### 📅 Day-by-Day Schedule")
        daily_plans = itinerary.get("daily_itinerary", [])
        for day in daily_plans:
            d_num = day.get("day", 1)
            theme = day.get("theme", "")
            with st.expander(f"🌟 Day {d_num}: {theme}", expanded=(d_num == 1)):
                for act in day.get("activities", []):
                    st.markdown(f"""
                    <div style="background: white; border-left: 4px solid #0284c7; padding: 8px 12px; margin-bottom: 8px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                        <span class="badge-pill badge-blue">{act.get('time_slot', '')}</span>
                        <b>{act.get('title', '')}</b>
                        <p style="margin: 4px 0; color: #334155; font-size: 0.95rem;">{act.get('description', '')}</p>
                        <small style="color: #64748b;">📍 {act.get('location', '')} | 💰 Est: {current['currency']} {act.get('cost', 0)} | 💡 Tip: {act.get('tips', 'Enjoy!')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                foods = day.get("food_recommendations", [])
                if foods:
                    st.markdown(f"🍴 **Dining Highlights:** {', '.join(foods)}")

        st.divider()

        # Transport & Accommodation Options
        col_t, col_h = st.columns(2)
        with col_t:
            st.markdown("### ✈️ Transit Options")
            for t in itinerary.get("transport_options", []):
                st.markdown(f"""
                <div class="agent-card">
                    <b>{t.get('mode', '')}</b> - {t.get('provider_or_route', '')}
                    <div style="margin: 6px 0; color:#0284c7; font-weight:600;">Est. Cost: {current['currency']} {t.get('estimated_cost', 0)} | ~{t.get('duration_hours', 0)} hrs</div>
                    <small style="color:#64748b;">• {t.get('departure_tips', '')}<br>• {t.get('booking_tips', '')}</small>
                </div>
                """, unsafe_allow_html=True)

        with col_h:
            st.markdown("### 🏨 Recommended Stays")
            for h in itinerary.get("hotel_options", []):
                st.markdown(f"""
                <div class="agent-card">
                    <b>{h.get('name', '')}</b> ({h.get('rating_approx', 4.5)} ⭐)
                    <div style="margin: 4px 0; color:#0f766e; font-weight:600;">{current['currency']} {h.get('price_per_night', 0)}/night (Total: {current['currency']} {h.get('total_cost', 0)})</div>
                    <small style="color:#475569;">📍 {h.get('area_or_neighborhood', '')}</small><br>
                    <small style="color:#64748b;">✨ {', '.join(h.get('amenities', []))}</small>
                </div>
                """, unsafe_allow_html=True)

        # Packing & Safety Tips
        st.divider()
        col_p, col_s = st.columns(2)
        with col_p:
            st.markdown("### 🎒 Packing Checklist")
            for item in itinerary.get("packing_checklist", []):
                st.checkbox(item, key=f"pack_{item[:15]}")
        with col_s:
            st.markdown("### 🛡️ Local Customs & Safety")
            for tip in itinerary.get("local_customs_and_safety_tips", []):
                st.markdown(f"• {tip}")

        # Export Suite (PDF, Calendar, Markdown, JSON)
        st.divider()
        st.markdown("### 📥 Export & Calendar Sync")
        col_e1, col_e2, col_e3, col_e4 = st.columns(4)
        
        with col_e1:
            try:
                pdf_bytes = generate_pdf_itinerary(current)
                st.download_button(
                    "📕 Download PDF Itinerary",
                    data=pdf_bytes,
                    file_name=f"itinerary_{current['destination'].lower()}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"PDF export notice: {e}")

        with col_e2:
            try:
                ics_data = generate_ics_calendar(current)
                st.download_button(
                    "📅 Add to Calendar (.ICS)",
                    data=ics_data,
                    file_name=f"trip_{current['destination'].lower()}.ics",
                    mime="text/calendar",
                    help="Import directly to Google Calendar, Apple Calendar & Outlook",
                    use_container_width=True
                )
            except Exception as e:
                st.caption(f"Calendar export error: {e}")

        with col_e3:
            md_content = f"""# AI Travel Itinerary: {current['origin']} to {current['destination']}
**Duration:** {current['duration_days']} Days
**Budget:** {current['currency']} {current['budget']:,.0f}
**Generated by:** AI Travel Planning Agent

## Overview
{itinerary.get('destination_overview', '')}

## Budget Breakdown
- Transport: {current['currency']} {budget_data.get('transportation', 0)}
- Accommodation: {current['currency']} {budget_data.get('accommodation', 0)}
- Food: {current['currency']} {budget_data.get('food_and_dining', 0)}
- Activities: {current['currency']} {budget_data.get('activities_and_entry', 0)}
- Buffer: {current['currency']} {budget_data.get('emergency_buffer', 0)}
- Total: {current['currency']} {budget_data.get('total_estimated_cost', 0)}

## Daily Schedule
"""
            for day in daily_plans:
                md_content += f"\n### Day {day.get('day')}: {day.get('theme')}\n"
                for act in day.get("activities", []):
                    md_content += f"- **{act.get('time_slot')}**: {act.get('title')} - {act.get('description')}\n"

            st.download_button(
                "📄 Download Markdown (.md)",
                data=md_content,
                file_name=f"itinerary_{current['destination'].lower()}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_e4:
            st.download_button(
                "💾 Download JSON Data",
                data=json.dumps(current, indent=2),
                file_name=f"itinerary_{current['destination'].lower()}.json",
                mime="application/json",
                use_container_width=True
            )

# TAB 3: Modify Plan
with tab_refine:
    st.subheader("💬 Refine & Modify Itinerary")
    if not st.session_state.current_trip:
        st.info("Please generate or select a trip first before modifying.")
    else:
        trip = st.session_state.current_trip
        st.markdown(f"Modifying active plan: **{trip['origin']} ➔ {trip['destination']}**")
        
        mod_input = st.text_area(
            "What would you like to change?",
            placeholder="e.g. 'Make day 2 more relaxed, swap morning trek with a beach sunset cafe, and keep budget under ₹18,000'"
        )

        if st.button("✨ Apply AI Modifications", use_container_width=True):
            if not mod_input:
                st.warning("Please enter your modification instruction.")
            else:
                with st.spinner("AI Modification Agent revising itinerary..."):
                    try:
                        res = httpx.post(f"{BACKEND_URL}/api/modify-trip", json={
                            "trip_id": trip["id"],
                            "modification_prompt": mod_input
                        }, timeout=45.0)
                        if res.status_code == 200:
                            updated_data = res.json()
                            st.session_state.current_trip["itinerary"] = updated_data["updated_itinerary"]
                            st.success("✅ Itinerary updated successfully! Check the 'Itinerary Dashboard' tab.")
                            st.rerun()
                        else:
                            st.error(f"Error {res.status_code}: {res.text}")
                    except Exception as e:
                        st.error(f"Could not connect to backend: {e}")

# Global Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px 0; color: #64748b; font-size: 0.9rem;">
    ✈️ <b>AI Travel Planning Agent</b>
    <br><span style="font-size: 0.8rem; opacity: 0.8;">Powered by FastAPI • Streamlit • LangGraph • Groq LLaMA 3.3</span>
</div>
""", unsafe_allow_html=True)
