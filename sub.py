import streamlit as st

st.set_page_config(page_title="Community Volunteering App", layout="centered")

st.title("🤝 Community Volunteering App")
st.subheader("📞 Official Helpline Numbers (India)")

helplines = [
    {"category": "🚨 Emergency", "name": "National Emergency", "number": "112"},
    {"category": "🚨 Emergency", "name": "Police", "number": "100"},
    {"category": "🚨 Emergency", "name": "Fire", "number": "101"},
    {"category": "🚑 Medical", "name": "Ambulance", "number": "108"},
    {"category": "🚑 Medical", "name": "Medical Emergency", "number": "102"},
    {"category": "👩 Women", "name": "Women Helpline", "number": "181"},
    {"category": "👩 Women", "name": "Women Police Helpline", "number": "1091"},
    {"category": "👶 Children", "name": "Childline", "number": "1098"},
    {"category": "🧠 Mental Health", "name": "Tele-MANAS", "number": "14416"},
    {"category": "🧠 Mental Health", "name": "Tele-MANAS (Toll Free)", "number": "18008914416"},
    {"category": "💻 Cyber Safety", "name": "Cyber Crime Helpline", "number": "1930"},
    {"category": "👴 Senior Citizens", "name": "Senior Citizen Helpline", "number": "14567"},
]

st.info("📱 Tap a number to call (works best on mobile devices).")

current_category = None

for h in helplines:
    if h["category"] != current_category:
        st.markdown(f"### {h['category']}")
        current_category = h["category"]

    st.markdown(
        f"""
        **{h['name']}**  
        <a href="tel:{h['number']}" style="font-size:18px; text-decoration:none;">
            📞 {h['number']}
        </a>
        <hr>
        """,
        unsafe_allow_html=True
    )