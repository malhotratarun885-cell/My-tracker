import streamlit as st
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import urllib.parse
import pandas as pd

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(page_title="CGL Pro Tracker", page_icon="🎯", layout="wide")

# Custom UI Styles
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 2px 2px 10px #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# 2. लॉजिक
today = date.today()
today_str = today.strftime("%Y-%m-%d")

if "streak_data" not in st.session_state: st.session_state.streak_data = {}

# साइडबार - AI Tutor & Target
st.sidebar.markdown("## ⚙️ Control Panel")
manual_hours = st.sidebar.number_input("⏱️ आज की पढ़ाई (Hours):", 0.0, 24.0, 0.0, 0.5)

# टॉपिक चयन और PYQ इंजन
syllabus = ["Whole numbers", "Profit and Loss", "Nouns", "Direction and distance", "Ancient History"]
selected_topic = st.sidebar.selectbox("📖 आज पढ़ा गया टॉपिक:", ["None"] + syllabus)
pyq_done = st.sidebar.checkbox("✅ मैंने 50 सवाल हल कर लिए हैं")

# Inspector / Improver लॉजिक
is_target_achieved = (manual_hours >= 10.0) and pyq_done
st.session_state.streak_data[today_str] = is_target_achieved
user_title = "✅ Inspector" if is_target_achieved else "⚠️ Improver"

st.title(f"🎯 SSC CGL Pro Tracker | Status: {user_title}")

# 3. डैशबोर्ड
col1, col2 = st.columns([2, 1])

with col1:
    st.info(f"**आपका स्टेटस:** {user_title}")
    st.write(f"⏱️ **स्टडी आवर्स:** {manual_hours}/10 | 🧠 **50 PYQs:** {'Done' if pyq_done else 'Pending'}")
    
    if is_target_achieved:
        st.success("🎉 शानदार! आप आज के 'Inspector' हैं।")
    else:
        st.warning("⚠️ स्ट्रीक पाने के लिए 10 घंटे और 50 सवाल पूरे करें।")

with col2:
    st.markdown("### 🔥 Consistency Heatmap")
    dates_str = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
    df_heat = pd.DataFrame({
        "Date": [d.split("-")[2] for d in dates_str],
        "Status": [1 if st.session_state.streak_data.get(d, False) else 0 for d in dates_str]
    })
    fig = px.imshow([df_heat["Status"].values], color_continuous_scale=["#ef233c", "#2ec4b6"])
    fig.update_layout(height=100, coloraxis_showscale=False, yaxis_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # WhatsApp Report
    report_msg = f"CGL Report: {user_title}, {manual_hours} Hours, 50 PYQs: {'Done' if pyq_done else 'No'}."
    st.link_button("🚀 WhatsApp Report", f"https://wa.me/919306707297?text={urllib.parse.quote(report_msg)}")

# 4. AI PYQ Button
if selected_topic != "None":
    st.sidebar.link_button(f"🔥 {selected_topic} के 50 PYQs करें", f"https://www.google.com/search?q={urllib.parse.quote(selected_topic + ' SSC CGL 50 PYQs')}")

st.markdown("---")
st.subheader("📚 सिलेबस ट्रैकर")
# (बाकी ट्रैकर टैब्स यहाँ जोड़ें)
