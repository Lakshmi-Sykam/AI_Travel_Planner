import streamlit as st
import streamlit.components.v1 as components

def render_airplane_flight_animation(origin: str, destination: str, duration_days: int = 1, group_size: int = 1, budget_str: str = ""):
    """
    Renders an animated flight visualization of an aeroplane traveling from Origin (Location 1) to Destination (Location 2).
    Features:
    - Departure beacon at Location 1 (Origin) & Arrival beacon at Location 2 (Destination)
    - Airplane taking off from Location 1, looping around the globe along the flight path, and arriving at Location 2
    - Trailing dashed flight corridor connecting both locations
    - Real-time animated flight status telemetry tracker
    """
    clean_origin = str(origin).strip() if str(origin).strip() else "Origin"
    clean_destination = str(destination).strip() if str(destination).strip() else "Destination"

    html_code = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    background: transparent;
    overflow: hidden;
    padding: 4px;
}}

.globe-flight-showcase {{
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 16px 40px -8px rgba(56, 140, 210, 0.38), 0 0 0 1.5px rgba(255, 255, 255, 0.85) inset;
    background: #ffffff;
    position: relative;
    width: 100%;
}}

/* Sky Canvas Matching Illustration */
.sky-canvas {{
    background: linear-gradient(180deg, #8dc6eb 0%, #7dbbe4 50%, #88c2ea 100%);
    height: 420px;
    position: relative;
    overflow: hidden;
    border-radius: 24px;
}}

/* Soft Floating Clouds */
.fl-cloud {{
    position: absolute;
    pointer-events: none;
    filter: drop-shadow(0 4px 10px rgba(0, 50, 100, 0.08));
}}

.fl-cloud-1 {{
    top: 22px;
    left: 18%;
    animation: cloudDriftSlow 32s linear infinite;
}}

.fl-cloud-2 {{
    top: 90px;
    left: -120px;
    animation: cloudDriftSlow 24s linear infinite 4s;
}}

.fl-cloud-3 {{
    top: 35px;
    right: -100px;
    animation: cloudDriftSlow 28s linear infinite 10s;
}}

.fl-cloud-4 {{
    top: 180px;
    left: 4%;
    animation: cloudDriftSlow 22s linear infinite 2s;
}}

@keyframes cloudDriftSlow {{
    0% {{ transform: translateX(-180px); }}
    100% {{ transform: translateX(1150px); }}
}}

/* Globe Stage & Earth Sphere */
.globe-stage {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 340px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.earth-sphere {{
    width: 230px;
    height: 230px;
    border-radius: 50%;
    background: #d8eefe;
    position: absolute;
    bottom: 22px;
    box-shadow: 0 16px 36px rgba(30, 80, 130, 0.24), inset -14px -14px 28px rgba(45, 100, 150, 0.16), inset 8px 8px 22px rgba(255, 255, 255, 0.85);
    border: 4px solid rgba(255, 255, 255, 0.95);
    overflow: visible;
    animation: globeGentleBob 4.5s ease-in-out infinite alternate;
}}

@keyframes globeGentleBob {{
    0% {{ transform: translateY(0px); }}
    100% {{ transform: translateY(-7px); }}
}}

.globe-ocean {{
    width: 100%;
    height: 100%;
    border-radius: 50%;
    position: relative;
    overflow: hidden;
}}

.continents-svg {{
    width: 100%;
    height: 100%;
    animation: continentShift 24s ease-in-out infinite alternate;
}}

@keyframes continentShift {{
    0% {{ transform: translateX(-5px) scale(1.0); }}
    100% {{ transform: translateX(7px) scale(1.02); }}
}}

/* Location 1 & Location 2 Map Pins with Glowing Radar Pulses */
.globe-pin {{
    position: absolute;
    z-index: 14;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.radar-ping {{
    position: absolute;
    top: -2px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 2px solid #ef4444;
    animation: radarRipple 2s ease-out infinite;
}}

@keyframes radarRipple {{
    0% {{ transform: scale(0.5); opacity: 1; }}
    100% {{ transform: scale(2.2); opacity: 0; }}
}}

.pin-head {{
    width: 26px;
    height: 34px;
    background: #e85d68;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    animation: pinHover 2s ease-in-out infinite;
    position: relative;
    z-index: 2;
}}

.pin-head.origin-color {{
    background: #0284c7;
}}

.pin-head.dest-color {{
    background: #ef4444;
    animation-delay: 0.5s;
}}

.pin-head.waypoint-color {{
    background: #f43f5e;
    width: 18px;
    height: 24px;
    animation-delay: 1.0s;
}}

.pin-dot {{
    width: 9px;
    height: 9px;
    background: #ffffff;
    border-radius: 50%;
    transform: rotate(45deg);
}}

/* Location 1: Origin (Left Side of Globe) */
.origin-pin {{
    top: 30px;
    left: 24px;
}}

/* Location 2: Destination (Right Side of Globe) */
.dest-pin {{
    top: 75px;
    right: 20px;
}}

.waypoint-pin {{
    bottom: 22px;
    left: 92px;
}}

.pin-badge {{
    background: rgba(15, 23, 42, 0.92);
    color: #ffffff;
    font-size: 0.72rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    margin-top: 6px;
    white-space: nowrap;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.28);
    border: 1px solid rgba(255, 255, 255, 0.4);
}}

.origin-badge {{
    border-left: 3px solid #38bdf8;
}}

.dest-badge {{
    border-left: 3px solid #ef4444;
}}

@keyframes pinHover {{
    0%, 100% {{ transform: rotate(-45deg) translateY(0); }}
    50% {{ transform: rotate(-45deg) translateY(-6px); }}
}}

/* Dashed Trajectory connecting Location 1 (Origin) to Location 2 (Destination) */
.orbit-trails-svg {{
    position: absolute;
    top: 10px;
    width: 540px;
    height: 330px;
    pointer-events: none;
    z-index: 6;
}}

.orbit-dash-primary {{
    animation: orbitDashLoop 2.4s linear infinite;
}}

.orbit-dash-secondary {{
    animation: orbitDashLoop 1.8s linear infinite;
}}

@keyframes orbitDashLoop {{
    0% {{ stroke-dashoffset: 36; }}
    100% {{ stroke-dashoffset: 0; }}
}}

/* Airplane Vessel Moving from Location 1 (Left-Bottom) to Location 2 (Right-Top) */
.flying-jet-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 20;
}}

.jet-motion-wrapper {{
    position: absolute;
    width: 200px;
    height: 110px;
    animation: flightLocation1ToLocation2 7.5s cubic-bezier(0.35, 0.05, 0.45, 0.95) infinite;
}}

.modern-airliner-svg {{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 16px 22px rgba(15, 45, 80, 0.35));
}}

/* Contrail Smoke Trail */
.jet-contrail {{
    position: absolute;
    top: 58px;
    left: -70px;
    width: 110px;
    height: 4px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 25%, #ffffff 100%);
    border-radius: 9999px;
    box-shadow: 0 0 14px rgba(255,255,255,0.95);
    animation: contrailGlow 1.2s infinite alternate;
}}

@keyframes contrailGlow {{
    0% {{ opacity: 0.6; width: 85px; }}
    100% {{ opacity: 1.0; width: 130px; }}
}}

/* Flight Trajectory Keyframe from Location 1 (Origin) to Location 2 (Destination) */
@keyframes flightLocation1ToLocation2 {{
    0% {{
        left: -190px;
        top: 290px;
        transform: scale(0.60) rotate(-14deg);
        opacity: 0;
    }}
    8% {{
        opacity: 1;
    }}
    30% {{
        /* Passing above Location 1 (Origin) */
        left: 12%;
        top: 185px;
        transform: scale(0.82) rotate(-18deg);
    }}
    55% {{
        /* Mid-flight altitude over globe */
        left: 36%;
        top: 85px;
        transform: scale(1.0) rotate(-24deg);
    }}
    78% {{
        /* Cruising towards Location 2 (Destination) */
        left: 65%;
        top: 20px;
        transform: scale(1.15) rotate(-26deg);
        opacity: 1;
    }}
    94% {{
        opacity: 1;
    }}
    100% {{
        left: calc(100% + 190px);
        top: -70px;
        transform: scale(1.24) rotate(-28deg);
        opacity: 0;
    }}
}}

/* Bottom Route Strip with Live Flight Progress Indicator */
.flight-route-strip {{
    position: absolute;
    bottom: 12px;
    left: 18px;
    right: 18px;
    background: rgba(255, 255, 255, 0.96);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 10px 22px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 24px rgba(15, 45, 80, 0.12);
    z-index: 25;
}}

.route-badge {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.badge-icon {{
    font-size: 1.4rem;
    background: #eff6ff;
    border: 1.5px solid #bfdbfe;
    border-radius: 10px;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.badge-label {{
    font-size: 0.65rem;
    font-weight: 800;
    color: #64748b;
    letter-spacing: 0.6px;
}}

.badge-city {{
    font-size: 1.05rem;
    font-weight: 900;
    color: #0f172a;
}}

.route-connector {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
}}

.route-status {{
    font-size: 0.76rem;
    font-weight: 800;
    color: #0284c7;
    letter-spacing: 0.6px;
}}

.route-line-anim {{
    width: 160px;
    height: 4px;
    background: linear-gradient(90deg, #38bdf8, #0284c7, #38bdf8);
    border-radius: 9999px;
    position: relative;
    overflow: hidden;
}}

.route-line-anim::after {{
    content: '';
    position: absolute;
    top: 0;
    left: -50%;
    width: 50%;
    height: 100%;
    background: #ffffff;
    animation: lineGlide 1.8s infinite;
}}

@keyframes lineGlide {{
    0% {{ left: -50%; }}
    100% {{ left: 100%; }}
}}

@media (max-width: 680px) {{
    .sky-canvas {{ height: 440px; }}
    .earth-sphere {{ width: 170px; height: 170px; bottom: 85px; }}
    .orbit-trails-svg {{ width: 340px; }}
    .flight-route-strip {{ flex-direction: column; gap: 8px; align-items: flex-start; }}
    .route-line-anim {{ width: 100%; }}
    .jet-motion-wrapper {{ width: 150px; height: 80px; }}
}}
</style>
</head>
<body>
    <div class="globe-flight-showcase">
        <div class="sky-canvas">
            <!-- Floating Stratosphere Clouds -->
            <div class="fl-cloud fl-cloud-1">
                <svg viewBox="0 0 100 60" width="85" height="51">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.95"/>
                </svg>
            </div>
            <div class="fl-cloud fl-cloud-2">
                <svg viewBox="0 0 100 60" width="75" height="45">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.9"/>
                </svg>
            </div>
            <div class="fl-cloud fl-cloud-3">
                <svg viewBox="0 0 100 60" width="105" height="63">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.95"/>
                </svg>
            </div>
            <div class="fl-cloud fl-cloud-4">
                <svg viewBox="0 0 100 60" width="65" height="39">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.85"/>
                </svg>
            </div>

            <!-- Central Orbit & Globe Stage -->
            <div class="globe-stage">
                <!-- Flight Orbit Lines Connecting Location 1 to Location 2 -->
                <svg class="orbit-trails-svg" viewBox="0 0 540 330" preserveAspectRatio="xMidYMid meet">
                    <defs>
                        <linearGradient id="orbitGrad1" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
                            <stop offset="40%" stop-color="#ffffff" stop-opacity="0.85"/>
                            <stop offset="100%" stop-color="#ffffff" stop-opacity="0.95"/>
                        </linearGradient>
                    </defs>
                    <path d="M 80,270 C 40,230 110,185 260,205 C 380,225 450,265 390,290 C 330,310 170,295 130,250" 
                          fill="none" stroke="url(#orbitGrad1)" stroke-width="2.5" stroke-dasharray="8,8" class="orbit-dash-primary" />
                    <path d="M 130,250 C 95,200 190,145 350,155 C 445,162 475,195 435,225 C 380,250 235,220 170,150 C 110,90 220,35 430,25" 
                          fill="none" stroke="url(#orbitGrad1)" stroke-width="3" stroke-dasharray="10,8" class="orbit-dash-secondary" />
                </svg>

                <!-- Earth Globe -->
                <div class="earth-sphere">
                    <div class="globe-ocean">
                        <svg class="continents-svg" viewBox="0 0 240 240">
                            <path d="M40,70 Q60,40 100,50 Q130,60 120,95 Q100,120 70,110 Q40,105 40,70 Z" fill="#8dc6eb"/>
                            <path d="M85,115 Q120,110 135,140 Q145,175 110,200 Q80,215 70,180 Q65,140 85,115 Z" fill="#8dc6eb"/>
                            <path d="M140,45 Q180,35 210,65 Q220,100 185,120 Q160,110 150,85 Q135,65 140,45 Z" fill="#8dc6eb"/>
                            <path d="M165,130 Q205,125 215,160 Q200,195 170,185 Q150,170 165,130 Z" fill="#8dc6eb"/>
                        </svg>
                    </div>

                    <!-- Location 1 Pin (Departure / Origin) -->
                    <div class="globe-pin origin-pin">
                        <div class="radar-ping"></div>
                        <div class="pin-head origin-color">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-badge origin-badge">🛫 {clean_origin}</div>
                    </div>

                    <!-- Location 2 Pin (Arrival / Destination) -->
                    <div class="globe-pin dest-pin">
                        <div class="radar-ping"></div>
                        <div class="pin-head dest-color">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-badge dest-badge">🛬 {clean_destination}</div>
                    </div>

                    <!-- Mid-route Waypoint Pin -->
                    <div class="globe-pin waypoint-pin">
                        <div class="pin-head waypoint-color">
                            <div class="pin-dot"></div>
                        </div>
                    </div>
                </div>

                <!-- Modern Commercial Airliner Moving from Location 1 to Location 2 -->
                <div class="flying-jet-container">
                    <div class="jet-motion-wrapper">
                        <!-- Jet Contrail Smoke Trail -->
                        <div class="jet-contrail"></div>
                        
                        <!-- High Definition Airliner SVG Vector -->
                        <svg class="modern-airliner-svg" viewBox="0 0 540 280" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <filter id="planeShadow" x="-20%" y="-20%" width="140%" height="140%">
                                    <feDropShadow dx="-4" dy="14" stdDeviation="10" flood-color="#1e3a8a" flood-opacity="0.35"/>
                                </filter>
                                <linearGradient id="wingNavyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#476994"/>
                                    <stop offset="50%" stop-color="#2c4d75"/>
                                    <stop offset="100%" stop-color="#1e3553"/>
                                </linearGradient>
                                <linearGradient id="bodyWhiteGloss" x1="0%" y1="0%" x2="0%" y2="100%">
                                    <stop offset="0%" stop-color="#ffffff"/>
                                    <stop offset="70%" stop-color="#f8fafc"/>
                                    <stop offset="100%" stop-color="#cbd5e1"/>
                                </linearGradient>
                            </defs>

                            <g filter="url(#planeShadow)">
                                <!-- Left/Upper Main Wing (Navy Blue) -->
                                <path d="M155,145 L60,45 C55,40 65,35 78,42 L245,130 Z" fill="url(#wingNavyGrad)"/>
                                <path d="M60,45 L48,32 C46,29 52,28 58,32 L78,42 Z" fill="#1e293b"/>

                                <!-- Horizontal Stabilizer / Left Tail Wing -->
                                <path d="M185,190 L160,205 C156,207 158,212 163,211 L210,195 Z" fill="url(#wingNavyGrad)"/>

                                <!-- Vertical Stabilizer Fin (White with subtle trim) -->
                                <path d="M190,185 L180,135 C178,128 186,128 191,133 L230,180 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>

                                <!-- Fuselage Body (Aerodynamic White Passenger Jet) -->
                                <path d="M180,185 C240,165 370,120 440,95 C465,86 480,92 475,102 C465,122 390,175 305,202 C255,218 200,205 180,185 Z" fill="url(#bodyWhiteGloss)"/>

                                <!-- Cockpit Windshield (Black / Dark Navy) -->
                                <path d="M445,95 C458,92 468,95 464,102 C458,107 448,108 438,105 Z" fill="#0f172a"/>
                                
                                <!-- Cabin Windows Array -->
                                <circle cx="415" cy="115" r="2.5" fill="#334155"/>
                                <circle cx="395" cy="122" r="2.5" fill="#334155"/>
                                <circle cx="375" cy="129" r="2.5" fill="#334155"/>
                                <circle cx="355" cy="136" r="2.5" fill="#334155"/>
                                <circle cx="335" cy="143" r="2.5" fill="#334155"/>
                                <circle cx="315" cy="150" r="2.5" fill="#334155"/>
                                <circle cx="295" cy="157" r="2.5" fill="#334155"/>
                                <circle cx="275" cy="164" r="2.5" fill="#334155"/>

                                <!-- Jet Engine 1 -->
                                <path d="M225,128 C220,120 240,115 250,122 L245,138 C238,140 230,135 225,128 Z" fill="#1e293b"/>
                                <ellipse cx="248" cy="123" rx="4" ry="7" fill="#0f172a"/>

                                <!-- Right/Lower Main Wing (Navy Blue) -->
                                <path d="M265,175 L380,245 C388,250 395,248 392,240 L305,162 Z" fill="url(#wingNavyGrad)"/>

                                <!-- Jet Engine 2 -->
                                <path d="M315,188 C310,182 328,178 338,185 L332,198 C325,200 318,195 315,188 Z" fill="#1e293b"/>
                                <ellipse cx="336" cy="186" rx="4" ry="7" fill="#0f172a"/>
                            </g>
                        </svg>
                    </div>
                </div>
            </div>

            <!-- Route Banner Bar Overlay with Departure & Arrival -->
            <div class="flight-route-strip">
                <div class="route-badge departure-badge">
                    <span class="badge-icon">🛫</span>
                    <div>
                        <div class="badge-label">LOCATION 1 (ORIGIN)</div>
                        <div class="badge-city">{clean_origin}</div>
                    </div>
                </div>
                <div class="route-connector">
                    <span class="route-line-anim"></span>
                    <span class="route-status">✈️ FLIGHT EN ROUTE</span>
                </div>
                <div class="route-badge arrival-badge">
                    <span class="badge-icon">🛬</span>
                    <div>
                        <div class="badge-label">LOCATION 2 (DESTINATION)</div>
                        <div class="badge-city">{clean_destination}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    components.html(html_code, height=435, scrolling=False)
