import streamlit as st
import streamlit.components.v1 as components

def render_airplane_flight_animation(origin: str, destination: str, duration_days: int = 1, group_size: int = 1, budget_str: str = ""):
    """
    Renders an animated flight visualization inspired by the globe-looping commercial airplane illustration.
    Using streamlit.components.v1.html ensures zero Markdown indentation issues (prevents raw code display).
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
    padding: 6px;
}}

.globe-flight-showcase {{
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 14px 36px -8px rgba(71, 140, 204, 0.35), 0 0 0 1.5px rgba(255, 255, 255, 0.8) inset;
    background: #ffffff;
    position: relative;
    width: 100%;
}}

/* Sky Canvas Matching Image Pastel Blue */
.sky-canvas {{
    background: linear-gradient(180deg, #8dc6eb 0%, #7dbbe4 50%, #88c2ea 100%);
    height: 380px;
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
    left: -100px;
    animation: cloudFloat 22s linear infinite;
}}

.fl-cloud-2 {{
    top: 110px;
    left: -120px;
    animation: cloudFloat 28s linear infinite 6s;
}}

.fl-cloud-3 {{
    top: 45px;
    left: -150px;
    animation: cloudFloat 34s linear infinite 14s;
}}

.fl-cloud-4 {{
    top: 140px;
    left: -80px;
    animation: cloudFloat 20s linear infinite 3s;
}}

@keyframes cloudFloat {{
    0% {{ transform: translateX(-150px); }}
    100% {{ transform: translateX(1100px); }}
}}

/* Globe Center Stage */
.globe-stage {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 300px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

/* Earth Sphere */
.earth-sphere {{
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: #d8eefe;
    position: absolute;
    bottom: 25px;
    box-shadow: 0 12px 30px rgba(30, 80, 130, 0.22), inset -12px -12px 25px rgba(45, 100, 150, 0.15), inset 8px 8px 20px rgba(255, 255, 255, 0.8);
    border: 3.5px solid rgba(255, 255, 255, 0.9);
    overflow: visible;
    animation: globeBob 4s ease-in-out infinite alternate;
}}

@keyframes globeBob {{
    0% {{ transform: translateY(0px); }}
    100% {{ transform: translateY(-8px); }}
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
    animation: continentDrift 20s ease-in-out infinite alternate;
}}

@keyframes continentDrift {{
    0% {{ transform: translateX(-4px) scale(1.0); }}
    100% {{ transform: translateX(6px) scale(1.02); }}
}}

/* Location Pins on Globe */
.globe-pin {{
    position: absolute;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
}}

.pin-head {{
    width: 22px;
    height: 30px;
    background: #e85d68;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.25);
    animation: pinBounce 2s ease-in-out infinite;
}}

.pin-head.dest-color {{
    background: #ef4444;
    animation-delay: 0.4s;
}}

.pin-head.waypoint-color {{
    background: #f43f5e;
    width: 16px;
    height: 22px;
    animation-delay: 0.8s;
}}

.pin-dot {{
    width: 8px;
    height: 8px;
    background: #ffffff;
    border-radius: 50%;
    transform: rotate(45deg);
}}

.origin-pin {{
    top: 22px;
    left: 32px;
}}

.dest-pin {{
    top: 70px;
    right: 24px;
}}

.waypoint-pin {{
    bottom: 22px;
    left: 80px;
}}

.pin-tooltip {{
    background: rgba(15, 23, 42, 0.92);
    color: #ffffff;
    font-size: 0.70rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 6px;
    margin-top: 4px;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.3);
}}

@keyframes pinBounce {{
    0%, 100% {{ transform: rotate(-45deg) translateY(0); }}
    50% {{ transform: rotate(-45deg) translateY(-5px); }}
}}

/* Dashed Orbit Trajectory SVG */
.orbit-trails-svg {{
    position: absolute;
    top: 15px;
    width: 480px;
    height: 300px;
    pointer-events: none;
    z-index: 6;
}}

.orbit-dash {{
    animation: orbitDashAnim 2.5s linear infinite;
}}

.orbit-dash-fast {{
    animation: orbitDashAnim 1.8s linear infinite;
}}

@keyframes orbitDashAnim {{
    0% {{ stroke-dashoffset: 32; }}
    100% {{ stroke-dashoffset: 0; }}
}}

/* Airplane Flight Motion (Left to Right Swirl) */
.flying-jet-container {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 15;
}}

.jet-motion-wrapper {{
    position: absolute;
    width: 160px;
    height: 85px;
    animation: planeFlightFlyby 7.5s cubic-bezier(0.45, 0.05, 0.55, 0.95) infinite;
}}

.modern-airliner-svg {{
    width: 100%;
    height: 100%;
    filter: drop-shadow(0 14px 16px rgba(15, 45, 80, 0.3));
}}

/* Trailing Contrail Behind Jet */
.jet-contrail {{
    position: absolute;
    top: 44px;
    left: -35px;
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 20%, #ffffff 100%);
    border-radius: 9999px;
    box-shadow: 0 0 10px rgba(255,255,255,0.9);
    animation: contrailFade 1.2s infinite alternate;
}}

@keyframes contrailFade {{
    0% {{ opacity: 0.6; width: 40px; }}
    100% {{ opacity: 1.0; width: 70px; }}
}}

/* Keyframes: Flight trajectory sweeping from left across top-right */
@keyframes planeFlightFlyby {{
    0% {{
        left: -180px;
        top: 130px;
        transform: scale(0.65) rotate(18deg);
        opacity: 0;
    }}
    8% {{
        opacity: 1;
    }}
    35% {{
        left: 18%;
        top: 70px;
        transform: scale(0.85) rotate(24deg);
    }}
    60% {{
        left: 48%;
        top: 25px;
        transform: scale(1.05) rotate(22deg);
    }}
    85% {{
        left: 78%;
        top: 5px;
        transform: scale(1.15) rotate(20deg);
        opacity: 1;
    }}
    100% {{
        left: calc(100% + 180px);
        top: -15px;
        transform: scale(1.2) rotate(18deg);
        opacity: 0;
    }}
}}

/* Bottom Route Strip */
.flight-route-strip {{
    position: absolute;
    bottom: 12px;
    left: 18px;
    right: 18px;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1.5px solid rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 10px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 8px 24px rgba(15, 45, 80, 0.12);
    z-index: 20;
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
    .sky-canvas {{ height: 420px; }}
    .earth-sphere {{ width: 160px; height: 160px; bottom: 80px; }}
    .orbit-trails-svg {{ width: 320px; }}
    .flight-route-strip {{ flex-direction: column; gap: 8px; align-items: flex-start; }}
    .route-line-anim {{ width: 100%; }}
    .jet-motion-wrapper {{ width: 120px; height: 65px; }}
}}
</style>
</head>
<body>
    <div class="globe-flight-showcase">
        <div class="sky-canvas">
            <!-- Floating Clouds -->
            <div class="fl-cloud fl-cloud-1">
                <svg viewBox="0 0 100 60" width="90" height="54">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.95"/>
                </svg>
            </div>
            <div class="fl-cloud fl-cloud-2">
                <svg viewBox="0 0 100 60" width="75" height="45">
                    <path d="M20,45 A15,15 0 0,1 32,25 A22,22 0 0,1 68,22 A18,18 0 0,1 85,45 Z" fill="#FFFFFF" opacity="0.9"/>
                </svg>
            </div>
            <div class="fl-cloud fl-cloud-3">
                <svg viewBox="0 0 100 60" width="110" height="66">
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
                <!-- Orbit Swirl Lines -->
                <svg class="orbit-trails-svg" viewBox="0 0 500 320" preserveAspectRatio="xMidYMid meet">
                    <defs>
                        <linearGradient id="orbitGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#ffffff" stop-opacity="0.3"/>
                            <stop offset="50%" stop-color="#ffffff" stop-opacity="0.95"/>
                            <stop offset="100%" stop-color="#ffffff" stop-opacity="0.95"/>
                        </linearGradient>
                    </defs>
                    <path d="M 90,260 C 50,220 120,180 250,200 C 370,220 440,260 380,285 C 320,305 180,290 140,250" 
                          fill="none" stroke="url(#orbitGrad)" stroke-width="2.5" stroke-dasharray="8,8" class="orbit-dash" />
                    <path d="M 140,250 C 110,210 200,160 340,170 C 430,178 460,205 420,230 C 370,255 240,230 180,170 C 120,110 210,60 380,50" 
                          fill="none" stroke="url(#orbitGrad)" stroke-width="3" stroke-dasharray="10,8" class="orbit-dash-fast" />
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
                    <div class="globe-pin origin-pin">
                        <div class="pin-head">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-tooltip">🛫 {clean_origin}</div>
                    </div>

                    <!-- Destination Pin -->
                    <div class="globe-pin dest-pin">
                        <div class="pin-head dest-color">
                            <div class="pin-dot"></div>
                        </div>
                        <div class="pin-tooltip">🛬 {clean_destination}</div>
                    </div>

                    <!-- Waypoint Pin -->
                    <div class="globe-pin waypoint-pin">
                        <div class="pin-head waypoint-color">
                            <div class="pin-dot"></div>
                        </div>
                    </div>
                </div>

                <!-- Commercial Airplane Vessel Soaring from Left to Right -->
                <div class="flying-jet-container">
                    <div class="jet-motion-wrapper">
                        <div class="jet-contrail"></div>
                        <svg class="modern-airliner-svg" viewBox="0 0 540 280" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <defs>
                                <filter id="planeShadow" x="-20%" y="-20%" width="140%" height="140%">
                                    <feDropShadow dx="-4" dy="12" stdDeviation="10" flood-color="#1e3a8a" flood-opacity="0.35"/>
                                </filter>
                                <linearGradient id="wingBlueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                    <stop offset="0%" stop-color="#476994"/>
                                    <stop offset="50%" stop-color="#2c4d75"/>
                                    <stop offset="100%" stop-color="#1e3553"/>
                                </linearGradient>
                                <linearGradient id="bodyWhiteGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                                    <stop offset="0%" stop-color="#ffffff"/>
                                    <stop offset="70%" stop-color="#f1f5f9"/>
                                    <stop offset="100%" stop-color="#cbd5e1"/>
                                </linearGradient>
                            </defs>

                            <g filter="url(#planeShadow)">
                                <!-- Left/Upper Main Wing -->
                                <path d="M155,145 L60,45 C55,40 65,35 78,42 L245,130 Z" fill="url(#wingBlueGrad)"/>
                                <path d="M60,45 L48,32 C46,29 52,28 58,32 L78,42 Z" fill="#1e293b"/>

                                <!-- Horizontal Stabilizer -->
                                <path d="M185,190 L160,205 C156,207 158,212 163,211 L210,195 Z" fill="url(#wingBlueGrad)"/>

                                <!-- Tail Fin -->
                                <path d="M190,185 L180,135 C178,128 186,128 191,133 L230,180 Z" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5"/>

                                <!-- Main Fuselage Body -->
                                <path d="M180,185 C240,165 370,120 440,95 C465,86 480,92 475,102 C465,122 390,175 305,202 C255,218 200,205 180,185 Z" fill="url(#bodyWhiteGrad)"/>

                                <!-- Cockpit Windshield -->
                                <path d="M445,95 C458,92 468,95 464,102 C458,107 448,108 438,105 Z" fill="#0f172a"/>
                                
                                <!-- Cabin Windows -->
                                <circle cx="415" cy="115" r="2.5" fill="#334155"/>
                                <circle cx="395" cy="122" r="2.5" fill="#334155"/>
                                <circle cx="375" cy="129" r="2.5" fill="#334155"/>
                                <circle cx="355" cy="136" r="2.5" fill="#334155"/>
                                <circle cx="335" cy="143" r="2.5" fill="#334155"/>
                                <circle cx="315" cy="150" r="2.5" fill="#334155"/>
                                <circle cx="295" cy="157" r="2.5" fill="#334155"/>
                                <circle cx="275" cy="164" r="2.5" fill="#334155"/>

                                <!-- Engine 1 -->
                                <path d="M225,128 C220,120 240,115 250,122 L245,138 C238,140 230,135 225,128 Z" fill="#1e293b"/>
                                <ellipse cx="248" cy="123" rx="4" ry="7" fill="#0f172a"/>

                                <!-- Lower Wing -->
                                <path d="M265,175 L380,245 C388,250 395,248 392,240 L305,162 Z" fill="url(#wingBlueGrad)"/>

                                <!-- Engine 2 -->
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
    components.html(html_code, height=395, scrolling=False)
