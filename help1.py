import streamlit as st

# Force Portrait/Mobile View Style
st.set_page_config(layout="centered", page_title="SOS Mobile")

# Professional CSS for a mobile feel
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 90px;
        font-size: 18px !important;
        border-radius: 12px;
        margin-bottom: 10px;
    }
    /* Red SOS button style */
    div.stButton > button:first-child[kind="primary"] {
        background-color: #ff4b4b;
        height: 150px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 1

# Navigation Helper
def set_step(s): 
    st.session_state.step = s
    st.rerun()

def render_header():
    col_back, col_space = st.columns([1, 2])
    with col_back:
        if st.button("⬅️ Back"):
            # Go to previous step, or home if at step 2
            set_step(max(1, st.session_state.step - 1))
    st.divider()

# --- PAGE 1: START ---
if st.session_state.step == 1:
    st.markdown("<h1 style='text-align: center;'>Volunteer Network</h1>", unsafe_allow_html=True)
    st.write(" ")
    if st.button("🚨\n\nREPORT EMERGENCY", type="primary"):
        set_step(2)

# --- PAGE 2: EMERGENCY TYPE ---
elif st.session_state.step == 2:
    render_header()
    st.subheader("What happened?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🏥\nMedical"):
            st.session_state.type = "Medical"
            set_step(3)
        if st.button("🌪️\nDisaster"):
            st.session_state.type = "Disaster"
            set_step(3)
    with col2:
        if st.button("🚗\nAccident"):
            st.session_state.type = "Accident"
            set_step(3)
        

# --- PAGE 3: SUB-CATEGORIES ---
elif st.session_state.step == 3:
    render_header()
    etype = st.session_state.type
    st.subheader(f"Type: {etype}")
    
    # Selection Mapping
    mapping = {
        "Medical": ["🫀 Cardiac", "🫁 Breathing", "🧠 Stroke"],
        "Accident": ["🛣️ Road", "🏗️ Fall", "🔥 Burn", "🧪 Poison"],
        "Disaster": ["🌊 Flood", "🐍 Animal", "☀️ Heat", "🫨 Quake"]
    }

    cols = st.columns(2)
    for i, label in enumerate(mapping[etype]):
        if cols[i % 2].button(label):
            st.session_state.sub = label
            set_step(4)

# --- PAGE 4: LOCATION & SEND ---
elif st.session_state.step == 4:
    render_header()
    st.subheader("Review & Send")
    st.info(f"**Alert:** {st.session_state.type} - {st.session_state.sub}")
    st.warning("📍 Location: Detected via GPS")
    
    if st.button("SEND SOS NOW", type="primary"):
        st.success("Alert Broadcasted to Community Volunteers!")
        if st.button("Done"): set_step(1)