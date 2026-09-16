import streamlit as st
import streamlit.components.v1 as components

def render_airplane_flight_animation(origin: str, destination: str, duration_days: int = 1, group_size: int = 1, budget_str: str = ""):
    """
    Renders an animated flight visualization matching the reference illustration.
    Features:
    - Aeroplane moving smoothly from LEFT-BOTTOM to RIGHT-TOP across the sky and globe
    - Swirling dashed flight trajectory lines wrapping around the Earth globe
    - Floating white clouds on a clean sky-blue backdrop
    - Clear Origin and Destination location pins on the globe
    - Live itinerary route telemetry badge
    """
    clean_origin = str(origin).replace('"', '&quot;').replace('<', '&lt;')
    clean_destination = str(destination).replace('"', '&quot;').replace('<', '&lt;')

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
    box-shadow: 0 14px 36px -8px rgba(71, 140, 204, 0.35), 0 0 0 1.5px rgba(255, 255, 255, 0.8) inset;
    background: #ffffff;
    position: relative;
    width: 100%;
}}

/* Sky Canvas Matching Reference Image */
.sky-canvas {{
    background: linear-gradient(180deg, #8dc6eb 0%, #7dbbe4 50%, #88c2ea 100%);
    height: 400px;
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
    top: 25px;
    left: 20%;
    animation: cloudDriftSlow 32s linear infinite;
}}

.fl-cloud-2 {{
    top: 85px;
    left: -120px;
    animation: cloudDriftSlow 24s linear infinite 4s;
}}

.fl-cloud-3 {{
    top: 40px;
    right: -100px;
    animation: cloudDriftSlow 28s linear infinite 10s;
}}

.fl-cloud-4 {{
    top: 170px;
    left: 6%;
    animation: cloudDriftSlow 22s linear infinite 2s;
}}

@keyframes cloudDriftSlow {{
    0% {{ transform: translateX(-180px); }}
    100% {{ transform: translateX(1150px); }}
}}

/* Globe Stage & Sphere */
.globe-stage {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 330px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.earth-sphere {{
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: #d8eefe;
    position: absolute;
    bottom: 20px;
    box-shadow: 0 14px 34px rgba(30, 80, 130, 0.22), inset -14px -14px 28px rgba(45, 100, 150, 0.16), inset 8px 8px 22px rgba(255, 255, 255, 0.85);
    border: 4px solid rgba(255, 255, 255, 0.92);
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

/* Clean Map Pins on Globe with Distinct Badges */
.globe-pin {{
    position: absolute;
    z-index: 12;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer;
}}

.pin-head {{
    width: 24px;
    height: 32px;
    background: #e85d68;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.28);
    animation: pinHover 2s ease-in-out infinite;
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

.origin-pin {{
    top: 20px;
    left: 28px;
}}

.dest-pin {{
    top: 65px;
    right: 22px;
}}

.waypoint-pin {{
    bottom: 24px;
    left: 88px;
}}

.pin-badge {{
    background: rgba(15, 23, 42, 0.88);
    color: #ffffff;
    font-size: 0.68rem;
    font-weight: 800;
    padding: 2px 7px;
    border-radius: 6px;
    margin-top: 5px;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.35);
}}

@keyframes pinHover {{
    0%, 100% {{ transform: rotate(-45deg) translateY(0); }}
    50% {{ transform: rotate(-45deg) translateY(-6px); }}
}}

/* Dashed Orbit Trajectory Swirls around the Globe */
.orbit-trails-svg {{
    position: absolute;
    top: 10px;
    width: 520px;
    height: 320px;
    pointer-events: none;
    z-index: 6;
}}

.orbit-dash-primary {{
    animation: orbitDashLoop 2.4s linear infinite;
}}

.orbit-dash-secondary {{
    animation: orbitDashLoop 1.9s linear infinite;
}}

@keyframes orbitDashLoop {{
    0% {{ stroke-dashoffset: 36; }}
    100% {{ stroke-dashoffset: 0; }}
}}

/* Aeroplane Motion from LEFT-BOTTOM to RIGHT-TOP */
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
    width: 190px;
    height: 100px;
    animation: flightLeftBottomToRightTop 7.5s cubic-bezier(0.35, 0.05, 0.45, 0.95) infinite;
}}

.modern-airliner-svg {{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 16px 20px rgba(15, 45, 80, 0.32));
}}

/* Contrail Smoke Trail Extending from Left-Bottom */
.jet-contrail {{
    position: absolute;
    top: 54px;
    left: -65px;
    width: 100px;
    height: 3.5px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 25%, #ffffff 100%);
    border-radius: 9999px;
    box-shadow: 0 0 12px rgba(255,255,255,0.95);
    animation: contrailGlow 1.2s infinite alternate;
}}

@keyframes contrailGlow {{
    0% {{ opacity: 0.6; width: 80px; }}
    100% {{ opacity: 1.0; width: 120px; }}
}}

/* Precise Trajectory: Left Bottom (Ascent) -> Above Globe -> Right Top */
@keyframes flightLeftBottomToRightTop {{
    0% {{
        left: -190px;
        top: 290px;
        transform: scale(0.60) rotate(-12deg);
        opacity: 0;
    }}
    8% {{
        opacity: 1;
    }}
    30% {{
        left: 12%;
        top: 190px;
        transform: scale(0.80) rotate(-18deg);
    }}
    55% {{
        left: 36%;
        top: 90px;
        transform: scale(0.98) rotate(-24deg);
    }}
    78% {{
        left: 64%;
        top: 25px;
        transform: scale(1.12) rotate(-26deg);
        opacity: 1;
    }}
    94% {{
        opacity: 1;
    }}
    100% {{
        left: calc(100% + 190px);
        top: -65px;
        transform: scale(1.22) rotate(-28deg);
        opacity: 0;
    }}
}}

/* Bottom Itinerary Route Bar */
.flight-route-strip {{
    position: absolute;
    bottom: 12px;
    left: 18px;
    right: 18px;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 9px 20px;
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
    width: 36px;
    height: 36px;
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
    font-size: 1.0rem;
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
    font-size: 0.74rem;
    font-weight: 800;
    color: #0284c7;
    letter-spacing: 0.6px;
}}

.route-line-anim {{
    width: 140px;
    height: 3px;
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
    .sky-canvas {{ height: 430px; }}
    .earth-sphere {{ width: 170px; height: 170px; bottom: 85px; }}
    .orbit-trails-svg {{ width: 340px; }}
    .flight-route-strip {{ flex-direction: column; gap: 8px; align-items: flex-start; }}
    .route-line-anim {{ width: 100%; }}
    .jet-motion-wrapper {{ width: 140px; height: 75px; }}
}}
</style>
</head>
<body>
    <div class="globe-flight-showcase">
        <div class="sky-canvas">
            <!-- Floating Clouds -->
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
                <!-- Orbit Swirl Trajectory Lines Wrapping from Bottom-Left around Globe to Top-Right -->
                <svg class="orbit-trails-svg" viewBox="0 0 520 320" preserveAspectRatio="xMidYMid meet">
                    <defs>
                        <linearGradient id="orbitGrad1" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
                            <stop offset="40%" stop-color="#ffffff" stop-opacity="0.85"/>
                            <stop offset="100%" stop-color="#ffffff" stop-opacity="0.95"/>
                        </linearGradient>
                    </defs>
                    <!-- Lower orbit loop -->
                    <path d="M 80,270 C 40,230 110,185 260,205 C 380,225 450,265 390,290 C 330,310 170,295 130,250" 
                          fill="none" stroke="url(#orbitGrad1)" stroke-width="2.5" stroke-dasharray="8,8" class="orbit-dash-primary" />
                    <!-- Ascending orbit curve from bottom-left wrapping around globe to top-right -->
                    <path d="M 130,250 C 95,200 190,145 350,155 C 445,162 475,195 435,225 C 380,250 235,220 170,150 C 110,90 220,35 430,25" 
                          fill="none" stroke="url(#orbitGrad1)" stroke-width="3" stroke-dasharray="10,8" class="orbit-dash-secondary" />
                </svg>

                <!-- 3D Style Globe Sphere -->
                <div class="earth-sphere">
                    <div class="globe-ocean">
                        <svg class="continents-svg" viewBox="0 0 240 240">
                            <path d="M40,70 Q60,40 100,50 Q130,60 120,95 Q100,120 70,110 Q40,105 40,70 Z" fill="#8dc6eb"/>
                            <path d="M85,115 Q120,110 135,140 Q145,175 110,200 Q80,215 70,180 Q65,140 85,115 Z" fill="#8dc6eb"/>
                            <path d="M140,45 Q180,35 210,65 Q220,100 185,120 Q160,110 150,85 Q135,65 140,45 Z" fill="#8dc6eb"/>
                            <path d="M165,130 Q205,125 215,160 Q200,195 170,185 Q150,170 165,130 Z" fill="#8dc6eb"/>
                        </svg>
                    </div>

                    <!-- Origin Pin -->
                    <div class="globe-pin origin-pin" title="Departure: {clean_origin}">
                        <div class="pin-head">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-badge">🛫 {clean_origin}</div>
                    </div>

                    <!-- Destination Pin -->
                    <div class="globe-pin dest-pin" title="Destination: {clean_destination}">
                        <div class="pin-head dest-color">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-badge">🛬 {clean_destination}</div>
                    </div>

                    <!-- Waypoint Pin -->
                    <div class="globe-pin waypoint-pin">
                        <div class="pin-head waypoint-color">
                            <div class="pin-dot"></div>
                        </div>
                    </div>
                </div>

                <!-- Modern Commercial Airliner Moving from LEFT-BOTTOM to RIGHT-TOP -->
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

            <!-- Route Banner Bar Overlay -->
            <div class="flight-route-strip">
                <div class="route-badge departure-badge">
                    <span class="badge-icon">🛫</span>
                    <div>
                        <div class="badge-label">DEPARTURE</div>
                        <div class="badge-city">{clean_origin}</div>
                    </div>
                </div>
                <div class="route-connector">
                    <span class="route-line-anim"></span>
                    <span class="route-status">✈️ AI ITINERARY ACTIVE</span>
                </div>
                <div class="route-badge arrival-badge">
                    <span class="badge-icon">🛬</span>
                    <div>
                        <div class="badge-label">DESTINATION</div>
                        <div class="badge-city">{clean_destination}</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    components.html(html_code, height=415, scrolling=False)
