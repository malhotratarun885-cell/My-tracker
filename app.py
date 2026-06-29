import streamlit as st
from datetime import date, timedelta
import plotly.express as px
import urllib.parse
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="CGL Elite Tracker", page_icon="🎯", layout="wide")

# Modern Dark/Professional CSS
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a, #1e293b); color: white; }
    .stMetric { background-color: #1e293b; padding: 20px; border-radius: 15px; border: 1px solid #334155; }
    h1, h2, h3 { color: #22d3ee; }
    .css-1d391kg { background-color: #0f172a; }
    </style>
""", unsafe_allow_html=True)

# 2. यूजर रजिस्ट्रेशन लॉजिक
if "user_registered" not in st.session_state: st.session_state.user_registered = False

if not st.session_state.user_registered:
    st.title("🎯 CGL Elite Tracker - Login")
    st.session_state.user_name = st.text_input("अपना नाम:")
    st.session_state.user_phone = st.text_input("व्हाट्सएप नंबर (रिपोर्ट के लिए):")
    if st.button("🚀 Register & Start"):
        if st.session_state.user_name and st.session_state.user_phone:
            st.session_state.user_registered = True
            st.rerun()
    st.stop()

# 3. सिलेबस डेटाबेस
syllabus_db = {
    "Maths 🧮": ["Number System", "Profit & Loss", "Geometry", "Trigonometry", "Algebra"],
    "English 🔤": ["Nouns", "Tense", "Voice & Speech", "Vocabulary", "Reading Comp"],
    "Reasoning 🧠": ["Coding-Decoding", "Blood Relation", "Syllogism", "Series", "Puzzles"],
    "GK/GS 🌍": ["History", "Geography", "Polity", "Economics", "Science"]
}

# 4. मुख्य लॉजिक
today = date.today()
today_str = today.strftime("%Y-%m-%d")
if "streak_data" not in st.session_state: st.session_state.streak_data = {}

st.title(f"🎯 Welcome, {st.session_state.user_name}!")
st.sidebar.markdown(f"### 👤 User: {st.session_state.user_name}")

# इनपुट डेटा
manual_hours = st.sidebar.number_input("⏱️ आज की पढ़ाई (Hours):", 0.0, 24.0, 0.0, 0.5)
selected_topic = st.sidebar.selectbox("📖 आज का टॉपिक:", [t for sub in syllabus_db.values() for t in sub])
pyq_done = st.sidebar.checkbox("✅ 50 PYQs पूरे किए?")

is_target_achieved = (manual_hours >= 10.0) and pyq_done
st.session_state.streak_data[today_str] = is_target_achieved
user_title = "✅ Inspector" if is_target_achieved else "⚠️ Improver"

# डैशबोर्ड
col1, col2 = st.columns([2, 1])
with col1:
    st.metric(label="📊 Current Status", value=user_title)
    st.write(f"⏱️ **Study Hours:** {manual_hours}/10 | 🧠 **50 PYQs:** {'Done' if pyq_done else 'Pending'}")
    
with col2:
    st.subheader("🔥 Consistency")
    dates_str = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    df_heat = pd.DataFrame({"Status": [1 if st.session_state.streak_data.get(d, False) else 0 for d in dates_str]})
    fig = px.imshow([df_heat["Status"].values], color_continuous_scale=["#f43f5e", "#22d3ee"])
    fig.update_layout(height=100, coloraxis_showscale=False, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

# 5. डिटेल्ड सिलेबस ट्रैकर
st.markdown("---")
st.subheader("📚 Detailed Syllabus Tracker")
for subject, topics in syllabus_db.items():
    with st.expander(subject):
        for topic in topics:
            st.checkbox(topic, key=f"check_{topic}")

# 6. रिपोर्टर
report_msg = f"CGL Report by {st.session_state.user_name} ({st.session_state.user_phone}):\nStatus: {user_title}\nHours: {manual_hours}/10\nPYQs: {'Done' if pyq_done else 'No'}"
st.link_button("🚀 Send WhatsApp Report", f"https://wa.me/919306707297?text={urllib.parse.quote(report_msg)}", use_container_width=True)

if selected_topic:
    st.sidebar.link_button(f"🔥 {selected_topic} PYQs", f"https://www.google.com/search?q={urllib.parse.quote(selected_topic + ' SSC CGL 50 PYQs')}")
