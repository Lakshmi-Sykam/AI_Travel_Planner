import streamlit as st

def render_airplane_flight_animation(origin: str, destination: str, duration_days: int = 1, group_size: int = 1, budget_str: str = ""):
    """
    Renders a stunning, premium luxury airplane flight animation moving from left to right across the flight path.
    Features:
    - Smooth continuous left-to-right aerodynamic flight trajectory
    - Dynamic jet contrail / smoke trail with soft glow
    - Origin & Destination radar pulses with airport markers
    - Parallax cloud drifts in the stratosphere
    - Flight HUD telemetry card (Route, Altitude, Status)
    """
    animation_html = f"""
    <div class="flight-corridor-container">
        <!-- Background Sky Gradients & Stars/Clouds -->
        <div class="sky-background">
            <div class="cloud cloud-1"></div>
            <div class="cloud cloud-2"></div>
            <div class="cloud cloud-3"></div>
            <div class="cloud cloud-4"></div>
            
            <!-- Flight Radar Arc Line -->
            <svg class="flight-arc-svg" viewBox="0 0 1000 160" preserveAspectRatio="none">
                <defs>
                    <linearGradient id="flightGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                        <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.3"/>
                        <stop offset="50%" stop-color="#0284c7" stop-opacity="0.9"/>
                        <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.3"/>
                    </linearGradient>
                </defs>
                <!-- Dashed trajectory arc -->
                <path d="M 60,110 Q 500,10 940,110" fill="none" stroke="url(#flightGradient)" stroke-width="3" stroke-dasharray="8,8" class="flight-path-arc" />
            </svg>
            
            <!-- Origin Marker (Left) -->
            <div class="airport-marker origin-marker">
                <div class="radar-pulse"></div>
                <div class="marker-icon">🛫</div>
                <div class="marker-tag">
                    <span class="city-name">{origin.upper()}</span>
                    <span class="status-sub">DEPARTURE</span>
                </div>
            </div>
            
            <!-- Moving Airplane Entity (Left to Right) -->
            <div class="airplane-flight-track">
                <div class="airplane-vessel">
                    <!-- Jet Contrail Smoke Trail Behind -->
                    <div class="contrail-trail"></div>
                    <!-- Detailed Aeroplane SVG Icon -->
                    <svg class="aeroplane-svg" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <g filter="url(#glow)">
                            <!-- Plane Body -->
                            <path d="M500.5 244.5L340.2 124.7C332.1 118.6 322.3 115.3 312.2 115.3H264.4C255.4 115.3 249.2 124.3 252.1 132.8L287.4 235.6H120.7L85.2 188.3C80.8 182.4 73.9 179 66.5 179H32.4C22.2 179 14.8 188.7 17.5 198.5L37.1 268.4L17.5 338.3C14.8 348.1 22.2 357.8 32.4 357.8H66.5C73.9 357.8 80.8 354.4 85.2 348.5L120.7 301.2H287.4L252.1 404C249.2 412.5 255.4 421.5 264.4 421.5H312.2C322.3 421.5 332.1 418.2 340.2 412.1L500.5 292.3C515.8 280.8 515.8 256 500.5 244.5Z" fill="#FFFFFF"/>
                            <!-- Wing Highlights & Cockpit -->
                            <path d="M470 268.4C465 260 448 255 425 255H310L275 145H295L440 250C460 256 475 262 470 268.4Z" fill="#38BDF8" opacity="0.85"/>
                            <circle cx="460" cy="268" r="6" fill="#F59E0B" />
                        </g>
                        <defs>
                            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                <feDropShadow dx="0" dy="2" stdDeviation="6" flood-color="#38bdf8" flood-opacity="0.9"/>
                            </filter>
                        </defs>
                    </svg>
                    <!-- Jet Engine Thruster Glow -->
                    <div class="engine-thrust"></div>
                </div>
            </div>
            
            <!-- Destination Marker (Right) -->
            <div class="airport-marker dest-marker">
                <div class="radar-pulse"></div>
                <div class="marker-icon">🛬</div>
                <div class="marker-tag">
                    <span class="city-name">{destination.upper()}</span>
                    <span class="status-sub">DESTINATION</span>
                </div>
            </div>
        </div>
        
        <!-- Live HUD Status Bar Below Corridor -->
        <div class="flight-hud-bar">
            <div class="hud-item">
                <span class="hud-label">FLIGHT STATUS</span>
                <span class="hud-value active-pulse">● EN ROUTE / CRUISE</span>
            </div>
            <div class="hud-item">
                <span class="hud-label">EXPEDITION ROUTE</span>
                <span class="hud-value highlight">{origin} ✈ {destination}</span>
            </div>
            <div class="hud-item">
                <span class="hud-label">TRIP DURATION</span>
                <span class="hud-value">{duration_days} Days Adventure</span>
            </div>
            <div class="hud-item">
                <span class="hud-label">EXPEDITION CREW</span>
                <span class="hud-value">👥 {group_size} {'Traveler' if group_size==1 else 'Travelers'}</span>
            </div>
            {"<div class='hud-item'><span class='hud-label'>EST. BUDGET</span><span class='hud-value'>" + budget_str + "</span></div>" if budget_str else ""}
        </div>
    </div>

    <style>
        .flight-corridor-container {{
            margin: 20px 0 26px 0;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 16px 40px -8px rgba(2, 132, 199, 0.45), 0 0 0 1.5px rgba(56, 189, 248, 0.4) inset;
            background: linear-gradient(135deg, #091e3a 0%, #034873 45%, #0284c7 85%, #0f172a 100%);
            position: relative;
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .sky-background {{
            position: relative;
            height: 160px;
            width: 100%;
            overflow: hidden;
        }}

        /* Flight trajectory SVG */
        .flight-arc-svg {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 2;
        }}

        .flight-path-arc {{
            animation: dashPulse 2.5s linear infinite;
        }}

        @keyframes dashPulse {{
            0% {{ stroke-dashoffset: 32; }}
            100% {{ stroke-dashoffset: 0; }}
        }}

        /* Aeroplane Moving Left to Right Animation Track */
        .airplane-flight-track {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 5;
            pointer-events: none;
            animation: flightTraversal 7s cubic-bezier(0.4, 0.0, 0.2, 1) infinite;
        }}

        .airplane-vessel {{
            position: absolute;
            width: 64px;
            height: 64px;
            transform-origin: center center;
            /* Subtly pitch along arc */
            animation: airplanePitch 7s ease-in-out infinite;
        }}

        .aeroplane-svg {{
            width: 100%;
            height: 100%;
            transform: rotate(0deg);
            filter: drop-shadow(0 4px 14px rgba(56, 189, 248, 0.8));
        }}

        /* Jet Contrail Smoke Trail */
        .contrail-trail {{
            position: absolute;
            top: 31px;
            right: 48px;
            width: 120px;
            height: 3px;
            background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.1) 30%, rgba(224, 242, 254, 0.75) 80%, #38bdf8 100%);
            border-radius: 9999px;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.8), 0 0 20px rgba(255, 255, 255, 0.5);
            animation: contrailGlow 1.2s ease-in-out infinite alternate;
        }}

        .engine-thrust {{
            position: absolute;
            top: 30px;
            right: 44px;
            width: 8px;
            height: 5px;
            background: radial-gradient(circle, #f59e0b 0%, #ef4444 80%, transparent 100%);
            border-radius: 50%;
            box-shadow: 0 0 10px #f59e0b, 0 0 18px #f97316;
            animation: thrusterPulse 0.4s infinite alternate;
        }}

        @keyframes thrusterPulse {{
            0% {{ opacity: 0.7; transform: scale(0.9); }}
            100% {{ opacity: 1.0; transform: scale(1.3); }}
        }}

        @keyframes contrailGlow {{
            0% {{ opacity: 0.6; width: 100px; }}
            100% {{ opacity: 0.95; width: 140px; }}
        }}

        /* Airplane Keyframe Moving from Left to Right along Flight Arc */
        @keyframes flightTraversal {{
            0% {{
                left: -80px;
                top: 80px;
                opacity: 0;
            }}
            5% {{
                opacity: 1;
            }}
            30% {{
                top: 25px;
            }}
            50% {{
                top: 15px;
            }}
            70% {{
                top: 30px;
            }}
            92% {{
                opacity: 1;
            }}
            100% {{
                left: calc(100% + 80px);
                top: 80px;
                opacity: 0;
            }}
        }}

        @keyframes airplanePitch {{
            0% {{ transform: rotate(-18deg) scale(0.92); }}
            25% {{ transform: rotate(-8deg) scale(1.0); }}
            50% {{ transform: rotate(0deg) scale(1.04); }}
            75% {{ transform: rotate(10deg) scale(1.0); }}
            100% {{ transform: rotate(16deg) scale(0.92); }}
        }}

        /* Airport Radar Markers */
        .airport-marker {{
            position: absolute;
            bottom: 22px;
            z-index: 4;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .origin-marker {{
            left: 36px;
        }}

        .dest-marker {{
            right: 36px;
        }}

        .marker-icon {{
            font-size: 1.6rem;
            background: rgba(15, 23, 42, 0.75);
            border: 2px solid #38bdf8;
            border-radius: 50%;
            width: 44px;
            height: 44px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 16px rgba(56, 189, 248, 0.6);
            position: relative;
            z-index: 2;
        }}

        .radar-pulse {{
            position: absolute;
            top: 2px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid #38bdf8;
            animation: radarPing 2s cubic-bezier(0, 0, 0.2, 1) infinite;
            z-index: 1;
        }}

        @keyframes radarPing {{
            0% {{
                transform: scale(0.95);
                opacity: 0.9;
            }}
            80%, 100% {{
                transform: scale(2.4);
                opacity: 0;
            }}
        }}

        .marker-tag {{
            margin-top: 6px;
            display: flex;
            flex-direction: column;
            align-items: center;
            background: rgba(15, 23, 42, 0.85);
            padding: 3px 10px;
            border-radius: 8px;
            border: 1px solid rgba(56, 189, 248, 0.4);
        }}

        .marker-tag .city-name {{
            font-size: 0.82rem;
            font-weight: 900;
            color: #ffffff;
            letter-spacing: 0.5px;
        }}

        .marker-tag .status-sub {{
            font-size: 0.62rem;
            font-weight: 700;
            color: #38bdf8;
            letter-spacing: 0.8px;
        }}

        /* Atmospheric Floating Clouds */
        .cloud {{
            position: absolute;
            background: rgba(255, 255, 255, 0.12);
            border-radius: 100px;
            pointer-events: none;
            filter: blur(4px);
        }}

        .cloud::after, .cloud::before {{
            content: '';
            position: absolute;
            background: inherit;
            border-radius: 50%;
        }}

        .cloud-1 {{
            width: 140px;
            height: 35px;
            top: 20px;
            left: -150px;
            animation: cloudDrift 22s linear infinite;
        }}
        .cloud-1::before {{ width: 50px; height: 50px; top: -20px; left: 25px; }}
        .cloud-1::after {{ width: 35px; height: 35px; top: -12px; left: 70px; }}

        .cloud-2 {{
            width: 180px;
            height: 40px;
            top: 65px;
            left: -200px;
            animation: cloudDrift 30s linear infinite 5s;
        }}
        .cloud-2::before {{ width: 60px; height: 60px; top: -25px; left: 35px; }}
        .cloud-2::after {{ width: 45px; height: 45px; top: -16px; left: 95px; }}

        .cloud-3 {{
            width: 110px;
            height: 28px;
            top: 40px;
            left: -120px;
            animation: cloudDrift 18s linear infinite 10s;
        }}

        .cloud-4 {{
            width: 160px;
            height: 36px;
            top: 100px;
            left: -180px;
            animation: cloudDrift 26s linear infinite 2s;
        }}

        @keyframes cloudDrift {{
            0% {{ left: -220px; }}
            100% {{ left: 105%; }}
        }}

        /* Live HUD Bottom Bar */
        .flight-hud-bar {{
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            background: rgba(10, 25, 47, 0.88);
            backdrop-filter: blur(12px);
            padding: 12px 24px;
            border-top: 1.5px solid rgba(56, 189, 248, 0.25);
        }}

        .hud-item {{
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}

        .hud-label {{
            font-size: 0.65rem;
            font-weight: 800;
            color: #94a3b8;
            letter-spacing: 0.8px;
            text-transform: uppercase;
        }}

        .hud-value {{
            font-size: 0.88rem;
            font-weight: 700;
            color: #f1f5f9;
        }}

        .hud-value.highlight {{
            color: #38bdf8;
            font-weight: 800;
        }}

        .hud-value.active-pulse {{
            color: #4ade80;
            animation: textPulse 1.8s ease-in-out infinite alternate;
        }}

        @keyframes textPulse {{
            0% {{ opacity: 0.75; text-shadow: 0 0 4px rgba(74, 222, 128, 0.4); }}
            100% {{ opacity: 1.0; text-shadow: 0 0 10px rgba(74, 222, 128, 0.8); }}
        }}

        @media (max-width: 680px) {{
            .flight-hud-bar {{
                flex-direction: column;
                align-items: flex-start;
                gap: 8px;
            }}
            .origin-marker {{ left: 16px; }}
            .dest-marker {{ right: 16px; }}
        }}
    </style>
    """
    st.markdown(animation_html, unsafe_allow_html=True)
