import streamlit as st

# Initialize session state to track which page the user is on
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'emergency_type' not in st.session_state:
    st.session_state.emergency_type = None

def go_to(page_num):
    st.session_state.page = page_num

# --- PAGE 1: START ---
if st.session_state.page == 1:
    st.title("Community Safety App")
    if st.button("🚨 NEED HELP", use_container_width=True, type="primary"):
        go_to(2)

# --- PAGE 2: SELECT TYPE ---
elif st.session_state.page == 2:
    st.header("Select Emergency Type")
    
    col1, col2, col3 = st.columns(3)
    if col1.button("🏥 Medical"):
        st.session_state.emergency_type = "Medical"
        go_to(3)
    if col2.button("🚗 Accident"):
        st.session_state.emergency_type = "Accident"
        go_to(3)
    if col3.button("🌪️ Disaster"):
        st.session_state.emergency_type = "Disaster"
        go_to(3)
    
    if st.button("← Back"): go_to(1)

# --- PAGE 3: SUB-CATEGORIES ---
elif st.session_state.page == 3:
    etype = st.session_state.emergency_type
    st.header(f"Details: {etype}")

    options = []
    if etype == "Medical":
        options = ["Trauma (Bleeding, Fractures)", "Cardiac (Chest Pain)", "Respiratory (Choking)", "Neurological (Stroke)"]
    elif etype == "Accident":
        options = ["Road Accident", "Falls", "Burns", "Poisoning"]
    else: # Disaster
        options = ["Floods/Earthquakes", "Heatstroke/Cold Exposure", "Animal Bites/Stings"]

    selection = st.radio("Specify the situation:", options)
    
    if st.button("Confirm & Next"):
        st.session_state.sub_type = selection
        go_to(4)
    if st.button("← Back"): go_to(2)

# --- PAGE 4: LOCATION ---
elif st.session_state.page == 4:
    st.header("Incident Location")
    st.warning("Fetching Current GPS Coordinates...")
    
    # In a real app, you'd use geolocator logic here
    st.write(f"**Report:** {st.session_state.emergency_type} - {st.session_state.sub_type}")
    st.write("Location: 12.9716° N, 77.5946° E (Sample Bangalore Lat/Long)")
    
    if st.button("SEND SOS NOW", type="primary"):
        st.success("Alert sent to nearest volunteers and emergency services!")
        if st.button("Reset"): go_to(1)