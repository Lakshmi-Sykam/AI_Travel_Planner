import streamlit as st
import httpx

def render_login_page(backend_url: str):
    """
    Renders an ultra-modern, cinematic nature & wanderlust themed full-screen Authentication portal.
    """
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

    # 1. Inject Dynamic 5-Scene Travel & Nature Sequence
    st.markdown("""
    <div class="travel-3d-bg">
        <div class="slide slide1"></div>
        <div class="slide slide2"></div>
        <div class="slide slide3"></div>
        <div class="slide slide4"></div>
        <div class="slide slide5"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Inject Static CSS (No f-string required)
    st.markdown("""
    <style>
        /* Base Root Background: Deep Cinematic Dark (ZERO WHITE FLASH) */
        html, body, .stApp {
            background-color: #0f172a !important;
            background: #0f172a !important;
        }

        /* 3D Animated Full-Screen Rotating Slideshow (5-Scene Travel & Nature Sequence) */
        .travel-3d-bg {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            z-index: 0 !important;
            overflow: hidden !important;
            pointer-events: none !important;
            background-color: #0f172a !important;
        }

        .travel-3d-bg .slide {
            position: absolute !important;
            top: -2% !important;
            left: -2% !important;
            width: 104% !important;
            height: 104% !important;
            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            opacity: 0;
            transition: opacity 1.5s ease-in-out !important;
        }

        /* 1. Aeroplane: Soaring in Sky (0s - 6s) */
        .travel-3d-bg .slide1 {
            background-image: linear-gradient(135deg, rgba(15, 23, 42, 0.65) 0%, rgba(3, 105, 161, 0.40) 50%, rgba(15, 23, 42, 0.75) 100%),
                              url('https://images.unsplash.com/photo-1436491865332-7a61a109cc05?auto=format&fit=crop&w=2400&q=85') !important;
            animation: slide1Anim 30s infinite ease-in-out !important;
            z-index: 1;
        }

        /* 2. Train: Scenic Mountain Railway Viaduct Journey (6s - 12s) */
        .travel-3d-bg .slide2 {
            background-image: linear-gradient(135deg, rgba(15, 23, 42, 0.60) 0%, rgba(4, 120, 87, 0.35) 50%, rgba(15, 23, 42, 0.75) 100%),
                              url('https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=2400&q=85') !important;
            animation: slide2Anim 30s infinite ease-in-out !important;
            z-index: 2;
        }

        /* 3. Nature: Tropical Turquoise Beach & Ocean Paradise (12s - 18s) */
        .travel-3d-bg .slide3 {
            background-image: linear-gradient(135deg, rgba(15, 23, 42, 0.55) 0%, rgba(6, 182, 212, 0.35) 50%, rgba(15, 23, 42, 0.70) 100%),
                              url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=2400&q=85') !important;
            animation: slide3Anim 30s infinite ease-in-out !important;
            z-index: 3;
        }

        /* 4. Train: Scenic Alpine Mountain Glacier Express (18s - 24s) */
        .travel-3d-bg .slide4 {
            background-image: linear-gradient(135deg, rgba(15, 23, 42, 0.65) 0%, rgba(2, 132, 199, 0.40) 50%, rgba(15, 23, 42, 0.75) 100%),
                              url('https://images.unsplash.com/photo-1509749837427-ac94a2553d0e?auto=format&fit=crop&w=2400&q=85') !important;
            animation: slide4Anim 30s infinite ease-in-out !important;
            z-index: 4;
        }

        /* 5. Nature: Majestic Alpine Mountain Lake & Valley Reflections (24s - 30s) */
        .travel-3d-bg .slide5 {
            background-image: linear-gradient(135deg, rgba(15, 23, 42, 0.65) 0%, rgba(5, 150, 105, 0.40) 50%, rgba(15, 23, 42, 0.75) 100%),
                              url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=2400&q=85') !important;
            animation: slide5Anim 30s infinite ease-in-out !important;
            z-index: 5;
        }

        /* Overlapping 5-slide cross-fade keyframes with ZERO white/black gaps */
        @keyframes slide1Anim {
            0% { opacity: 1; transform: scale(1.0); }
            17% { opacity: 1; transform: scale(1.04); }
            23% { opacity: 0; transform: scale(1.07); }
            95% { opacity: 0; transform: scale(1.0); }
            100% { opacity: 1; transform: scale(1.0); }
        }

        @keyframes slide2Anim {
            0%, 15% { opacity: 0; transform: scale(1.0); }
            20% { opacity: 1; transform: scale(1.0); }
            37% { opacity: 1; transform: scale(1.04); }
            43% { opacity: 0; transform: scale(1.07); }
            100% { opacity: 0; transform: scale(1.0); }
        }

        @keyframes slide3Anim {
            0%, 35% { opacity: 0; transform: scale(1.0); }
            40% { opacity: 1; transform: scale(1.0); }
            57% { opacity: 1; transform: scale(1.04); }
            63% { opacity: 0; transform: scale(1.07); }
            100% { opacity: 0; transform: scale(1.0); }
        }

        @keyframes slide4Anim {
            0%, 55% { opacity: 0; transform: scale(1.0); }
            60% { opacity: 1; transform: scale(1.0); }
            77% { opacity: 1; transform: scale(1.04); }
            83% { opacity: 0; transform: scale(1.07); }
            100% { opacity: 0; transform: scale(1.0); }
        }

        @keyframes slide5Anim {
            0%, 75% { opacity: 0; transform: scale(1.0); }
            80% { opacity: 1; transform: scale(1.0); }
            97% { opacity: 1; transform: scale(1.04); }
            100% { opacity: 0; transform: scale(1.07); }
        }

        /* Top Creator Badge & Title Tags */
        .nature-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #059669 0%, #0284c7 100%);
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-size: 0.85rem;
            font-weight: 800;
            padding: 8px 22px;
            border-radius: 9999px;
            box-shadow: 0 4px 18px rgba(5, 150, 105, 0.5);
            letter-spacing: 0.6px;
        }

        .creator-tag {
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(12px);
            border: 1.5px solid rgba(255, 255, 255, 0.3);
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800;
            font-size: 0.92rem;
            padding: 8px 24px;
            border-radius: 9999px;
            display: inline-block;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        }

        /* Sleek Glassmorphism Container (NO SOLID WHITE BACKGROUND) */
        div[data-testid="column"]:nth-child(2) [data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="column"]:nth-child(2) [data-testid="stVerticalBlockBorderWrapper"] > div,
        div[data-testid="column"]:nth-child(2) [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"],
        div[data-testid="stVerticalBlockBorderWrapper"],
        div[data-testid="stVerticalBlockBorderWrapper"] > div,
        div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"],
        div[data-testid="stForm"],
        form[data-testid="stForm"],
        .stForm {
            background-color: transparent !important;
            background: transparent !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: rgba(15, 23, 42, 0.55) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 28px !important;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6), 0 0 30px rgba(2, 132, 199, 0.2) !important;
            padding: 2.2rem !important;
        }

        div[data-testid="stForm"] {
            border: none !important;
            padding: 0 !important;
            background: transparent !important;
        }

        /* ALL HEADINGS, LABELS, PARAGRAPHS IN PURE WHITE */
        div[data-testid="stVerticalBlockBorderWrapper"] h1,
        div[data-testid="stVerticalBlockBorderWrapper"] h2,
        div[data-testid="stVerticalBlockBorderWrapper"] h3,
        div[data-testid="stVerticalBlockBorderWrapper"] h4,
        div[data-testid="stVerticalBlockBorderWrapper"] p,
        div[data-testid="stVerticalBlockBorderWrapper"] span,
        div[data-testid="stVerticalBlockBorderWrapper"] div,
        [data-testid="stForm"] label, 
        [data-testid="stForm"] label p,
        [data-testid="stForm"] p,
        [data-testid="stForm"] span,
        [data-testid="stForm"] h3 {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8) !important;
        }

        [data-testid="stForm"] label,
        [data-testid="stForm"] label p {
            font-weight: 800 !important;
            font-size: 0.98rem !important;
            margin-bottom: 6px !important;
        }

        /* Clean Glass divider */
        hr {
            border-color: rgba(255, 255, 255, 0.2) !important;
            margin: 1.2rem 0 1rem 0 !important;
        }

        /* Glass Mode Switch Buttons */
        .auth-tab-btn button {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(10px) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 9999px !important;
            padding: 10px 20px !important;
            font-size: 0.95rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
            text-shadow: 0 1px 4px rgba(0,0,0,0.6) !important;
        }

        .auth-tab-btn button:hover {
            background: rgba(255, 255, 255, 0.22) !important;
            transform: translateY(-2px) !important;
            border-color: #38bdf8 !important;
            box-shadow: 0 6px 18px rgba(56, 189, 248, 0.4) !important;
        }

        /* Active Tab Button */
        .auth-tab-active button {
            background: linear-gradient(135deg, rgba(5, 150, 105, 0.85) 0%, rgba(2, 132, 199, 0.85) 100%) !important;
            border: 2px solid #38bdf8 !important;
            border-radius: 9999px !important;
            padding: 10px 20px !important;
            font-size: 0.95rem !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            box-shadow: 0 6px 20px rgba(2, 132, 199, 0.45) !important;
        }

        .guest-card-box {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 16px !important;
            padding: 14px 16px !important;
            margin-top: 18px !important;
            margin-bottom: 10px !important;
            text-align: center !important;
        }

        /* Guest Mode Button inside the card */
        .guest-pill-btn button {
            background: rgba(255, 255, 255, 0.14) !important;
            backdrop-filter: blur(10px) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.35) !important;
            border-radius: 9999px !important;
            padding: 10px 24px !important;
            font-size: 0.95rem !important;
            font-weight: 800 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
            transition: all 0.2s ease !important;
        }

        .guest-pill-btn button:hover {
            background: rgba(255, 255, 255, 0.25) !important;
            border-color: #34d399 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(52, 211, 153, 0.4) !important;
        }

        /* Input Fields with Crisp White Background & Black Font */
        [data-testid="stForm"] input {
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
            border: 1.5px solid #cbd5e1 !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            font-size: 1rem !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08) !important;
        }

        [data-testid="stForm"] input::placeholder {
            color: #334155 !important;
            -webkit-text-fill-color: #334155 !important;
            font-weight: 500 !important;
            opacity: 0.85 !important;
        }

        [data-testid="stForm"] input:focus {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.35) !important;
            background-color: #ffffff !important;
            color: #000000 !important;
            -webkit-text-fill-color: #000000 !important;
        }

        /* Submit Action Buttons (Glowing Emerald Gradient + Bold White Text) */
        [data-testid="stForm"] button[kind="primaryFormSubmit"],
        [data-testid="stForm"] button[kind="secondaryFormSubmit"],
        [data-testid="stForm"] button {
            background: linear-gradient(135deg, #059669 0%, #0284c7 100%) !important;
            background-color: #059669 !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800 !important;
            font-size: 1.05rem !important;
            border: none !important;
            border-radius: 14px !important;
            padding: 0.75rem 1.4rem !important;
            box-shadow: 0 6px 22px rgba(2, 132, 199, 0.5) !important;
            margin-top: 14px !important;
            width: 100% !important;
        }

        [data-testid="stForm"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 26px rgba(2, 132, 199, 0.7) !important;
        }

        [data-testid="stForm"] button p,
        [data-testid="stForm"] button span {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-weight: 800 !important;
        }

        .highlight-banner {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.9) 0%, rgba(2, 132, 199, 0.9) 100%);
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            padding: 8px 16px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 0.85rem;
            text-align: center;
            margin-bottom: 14px;
            box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
            letter-spacing: 0.5px;
        }

        .feature-pill {
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            padding: 6px 16px;
            border-radius: 14px;
            font-size: 0.82rem;
            font-weight: 800;
            margin: 4px;
            display: inline-block;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
        }
    </style>
    """, unsafe_allow_html=True)

    # Top Hero Brand Title
    st.markdown("""
    <div style="text-align: center; margin-top: 0.5rem; margin-bottom: 1.5rem;">
        <div class="nature-badge">
            🌿 AUTONOMOUS MULTI-AGENT TRAVEL INTELLIGENCE
        </div>
        <h1 style="margin: 0.7rem 0 0.2rem 0; font-size: 2.8rem; font-weight: 900; color: #ffffff; text-shadow: 0 3px 14px rgba(0,0,0,0.7); letter-spacing: -0.5px;">
            ✈️ AI Travel Planner
        </h1>
        <p style="color: #f8fafc; font-size: 1.15rem; font-weight: 500; text-shadow: 0 2px 10px rgba(0,0,0,0.8); max-width: 680px; margin: 0 auto;">
            Discover breathtaking destinations, curated daily itineraries, and smart budget balancing powered by Agentic AI.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Centered Column
    col_left, col_card, col_right = st.columns([1, 1.9, 1])
    
    with col_card:
        # Wrap everything in a dedicated, unified White Container Card Box
        with st.container(border=True):
            
            # --- Dedicated White Pill Box Tab Switchers ---
            tab_col1, tab_col2 = st.columns(2)
            
            is_login = (st.session_state.auth_mode == "login")
            
            with tab_col1:
                st.markdown(f'<div class="{"auth-tab-active" if is_login else "auth-tab-btn"}">', unsafe_allow_html=True)
                if st.button("🔐 Sign In", use_container_width=True, key="switch_to_login_btn"):
                    st.session_state.auth_mode = "login"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                
            with tab_col2:
                st.markdown(f'<div class="{"auth-tab-active" if not is_login else "auth-tab-btn"}">', unsafe_allow_html=True)
                if st.button("✨ Create New Account (Free) 🚀", use_container_width=True, key="switch_to_reg_btn"):
                    st.session_state.auth_mode = "register"
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            st.write("") # Spacing

            # --- Sign In View ---
            if st.session_state.auth_mode == "login":
                with st.form("nature_login_form"):
                    st.markdown("<h3 style='margin:0 0 0.2rem 0; color:#ffffff; font-weight:900; text-shadow:0 2px 8px rgba(0,0,0,0.8);'>Welcome Back, Explorer 🌍</h3>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#f8fafc; font-size:0.95rem; margin-bottom:1rem; text-shadow:0 1px 6px rgba(0,0,0,0.8);'>Sign in to resume planning your next unforgettable journey.</p>", unsafe_allow_html=True)
                    
                    login_email = st.text_input("📧 Email Address", placeholder="Enter your email address", key="login_email_main")
                    login_password = st.text_input("🔑 Password", type="password", placeholder="Enter your password", key="login_pass_main")
                    submit_login = st.form_submit_button("🚀 Sign In to Dashboard", use_container_width=True)

                    if submit_login:
                        if not login_email or not login_password:
                            st.error("⚠️ Please enter both email and password.")
                        else:
                            try:
                                with st.spinner("Authenticating with AI Server..."):
                                    resp = httpx.post(
                                        f"{backend_url}/api/auth/login",
                                        json={"email": login_email, "password": login_password},
                                        timeout=10.0
                                    )
                                if resp.status_code == 200:
                                    data = resp.json()
                                    st.session_state.auth_token = data.get("access_token")
                                    st.session_state.user_info = data.get("user")
                                    st.success(f"✅ Welcome back, {data['user']['full_name']}!")
                                    st.rerun()
                                else:
                                    err_msg = resp.json().get("detail", "Invalid email or password")
                                    st.error(f"❌ {err_msg}")
                            except Exception as e:
                                st.error(f"❌ Server connection error: {e}. Make sure Backend is running on :8000.")

            # --- Register View ---
            else:
                with st.form("nature_register_form"):
                    st.markdown("""
                    <div class="highlight-banner">
                        🌟 NEW TRAVELER REGISTRATION • INSTANT FREE ACCESS
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<h3 style='margin:0 0 0.2rem 0; color:#ffffff; font-weight:900; text-shadow:0 2px 8px rgba(0,0,0,0.8);'>Begin Your AI Journey 🏕️</h3>", unsafe_allow_html=True)
                    st.markdown("<p style='color:#f8fafc; font-size:0.95rem; margin-bottom:1rem; text-shadow:0 1px 6px rgba(0,0,0,0.8);'>Create an account to save custom trips & generate AI itineraries.</p>", unsafe_allow_html=True)
                    
                    reg_name = st.text_input("👤 Full Name", placeholder="Enter your full name", key="reg_name_main")
                    reg_email = st.text_input("📧 Email Address", placeholder="Enter your email address", key="reg_email_main")
                    reg_password = st.text_input("🔑 Create Password", type="password", placeholder="Enter a secure password", key="reg_pass_main")
                    submit_reg = st.form_submit_button("🎉 Create Free Account & Get Started", use_container_width=True)

                    if submit_reg:
                        if not reg_name or not reg_email or not reg_password:
                            st.error("⚠️ Please fill in all registration fields.")
                        else:
                            try:
                                with st.spinner("Creating your travel account..."):
                                    resp = httpx.post(
                                        f"{backend_url}/api/auth/register",
                                        json={"full_name": reg_name, "email": reg_email, "password": reg_password},
                                        timeout=10.0
                                    )
                                if resp.status_code == 200:
                                    data = resp.json()
                                    st.session_state.auth_token = data.get("access_token")
                                    st.session_state.user_info = data.get("user")
                                    st.success("🎉 Account created successfully! Logging you in...")
                                    st.rerun()
                                else:
                                    err_msg = resp.json().get("detail", "Registration failed")
                                    st.error(f"❌ {err_msg}")
                            except Exception as e:
                                st.error(f"❌ Server connection error: {e}. Make sure Backend is running.")

            # --- Guest Quick Access Mode Box ---
            st.markdown("""
            <div class="guest-card-box">
                <div style="font-size:0.98rem; color:#ffffff; font-weight:900; margin-bottom:4px; text-shadow:0 2px 8px rgba(0,0,0,0.8);">
                    ⚡ Quick Test Without Account
                </div>
                <div style="font-size:0.86rem; color:#f1f5f9; margin-bottom:10px; text-shadow:0 1px 5px rgba(0,0,0,0.8);">
                    Explore destinations and generate sample itineraries instantly.
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="guest-pill-btn">', unsafe_allow_html=True)
            if st.button("🍃 Explore as Guest Traveler", use_container_width=True, key="guest_mode_nature_btn"):
                st.session_state.auth_token = "guest_token"
                st.session_state.user_info = {"full_name": "Guest Traveler", "email": "guest@travelplanner.local"}
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

            # Highlights footer inside card
            st.markdown("""
            <div style="margin-top: 1.2rem; text-align: center; padding-top: 0.8rem; border-top: 1px solid rgba(255, 255, 255, 0.2);">
                <span class="feature-pill">🏔️ Scenic Routes</span>
                <span class="feature-pill">🏨 Smart Hotels</span>
                <span class="feature-pill">🗺️ Route Maps</span>
                <span class="feature-pill">💰 Budget AI</span>
            </div>
            """, unsafe_allow_html=True)


def render_user_profile_sidebar():
    """
    Renders the logged-in user details & logout button in the sidebar.
    """
    if st.session_state.get("user_info"):
        user = st.session_state.user_info
        st.markdown(f"""
        <div style="background: white; border: 1.5px solid #d1fae5; border-radius: 12px; padding: 12px; margin-bottom: 12px; box-shadow: 0 2px 5px rgba(16, 185, 129, 0.08);">
            <div style="font-size: 0.75rem; color: #059669; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;">👤 Logged In Account</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #0f172a; margin-top: 2px;">{user.get('full_name', 'Traveler')}</div>
            <div style="font-size: 0.8rem; color: #64748b;">{user.get('email', '')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚪 Log Out", use_container_width=True, key="auth_logout_btn"):
            st.session_state.auth_token = None
            st.session_state.user_info = None
            st.session_state.current_trip = None
            st.rerun()






