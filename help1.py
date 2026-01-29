import streamlit as st
import pandas as pd
import numpy as np
from streamlit_js_eval import streamlit_js_eval, get_geolocation
from twilio.rest import Client

# --- TWILIO CONFIG (Replace with your actual details) ---
TWILIO_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
FROM_WHATSAPP = 'whatsapp:+14155238886' 
TO_WHATSAPP = 'whatsapp:+91XXXXXXXXXX'   

def send_whatsapp_sos(etype, subtype, lat, lon, manual_addr=None):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        # Create Google Maps link if GPS is available
        loc_info = f"http://maps.google.com/?q={lat},{lon}" if lat else f"Manual Address: {manual_addr}"
        
        message_body = (
            f"🚨 *SOS EMERGENCY ALERT* 🚨\n\n"
            f"*Type:* {etype}\n"
            f"*Detail:* {subtype}\n"
            f"*Location:* {loc_info}\n"
            f"Please respond immediately!"
        )
        client.messages.create(from_=FROM_WHATSAPP, body=message_body, to=TO_WHATSAPP)
        return True
    except Exception as e:
        st.error(f"Twilio Error: {e}")
        return False

# --- UI & NAVIGATION ---
st.set_page_config(layout="centered", page_title="Community SOS")

st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 80px; font-size: 18px !important; border-radius: 15px; }
    div.stButton > button:first-child[kind="primary"] { background-color: #ff4b4b; height: 140px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Initializing Session State
if 'step' not in st.session_state: st.session_state.step = 1
if 'location' not in st.session_state: st.session_state.location = None

def set_step(s):
    st.session_state.step = s
    st.rerun()

def render_nav():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"): set_step(max(1, st.session_state.step - 1))
    with col2:
        if st.button("🏠 Home"): set_step(1)
    st.divider()

# --- GPS FETCH (Run this globally so it's ready by Step 4) ---
# We use get_geolocation() from the library directly
loc = get_geolocation()

# --- PAGE LOGIC ---

# PAGE 1: START
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>COMMUNITY HELP</h1>", unsafe_allow_html=True)
    if st.button("🚨\n\nPRESS FOR EMERGENCY", type="primary"):
        set_step(2)

# PAGE 2: EMERGENCY TYPE
elif st.session_state.step == 2:
    render_nav()
    st.subheader("What is the situation?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏥\nMedical"): st.session_state.type = "Medical"; set_step(3)
        if st.button("🌪️\nDisaster"): st.session_state.type = "Disaster"; set_step(3)
    with col2:
        if st.button("🚗\nAccident"): st.session_state.type = "Accident"; set_step(3)
        if st.button("🛑\nCancel"): set_step(1)

# PAGE 3: SUB-TYPES
elif st.session_state.step == 3:
    render_nav()
    etype = st.session_state.type
    mapping = {
        "Medical": ["🫀 Cardiac", "🫁 Breathing", "🧠 Stroke", "🐍 Animal"],
        "Accident": ["🛣️ Road", "🏗️ Fall", "🔥 Burn", "🧪 Poison"],
        "Disaster": ["🌊 Flood", "☀️ Heat", "🫨 Quake"]
    }
    cols = st.columns(2)
    for i, label in enumerate(mapping[etype]):
        if cols[i % 2].button(label):
            st.session_state.sub = label
            set_step(4)

# PAGE 4: LOCATION & SEND
elif st.session_state.step == 4:
    render_nav()
    st.subheader("Confirm Location")
    
    lat, lon, manual_addr = None, None, None

    # Check if GPS returned data
    if loc and 'coords' in loc:
        lat = loc['coords']['latitude']
        lon = loc['coords']['longitude']
        st.success(f"✅ GPS Locked: {lat:.4f}, {lon:.4f}")
        st.map(pd.DataFrame({'lat': [lat], 'lon': [lon]}))
    else:
        st.error("🚨 GPS Signal Not Found")
        manual_addr = st.text_area("Type your landmark/address:", placeholder="e.g. Near Market Gate")

    if st.button("SEND SOS NOW", type="primary"):
        if lat or manual_addr:
            success = send_whatsapp_sos(st.session_state.type, st.session_state.sub, lat, lon, manual_addr)
            if success:
                st.success("SOS DISPATCHED!")
                st.balloons()
        else:
            st.warning("Please provide a location or landmark.")