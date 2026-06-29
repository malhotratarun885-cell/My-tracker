import streamlit as st
from datetime import date
import plotly.graph_objects as go

# 1. पेज कॉन्फ़िगरेशन और टाइटल
st.set_page_config(page_title="CGL Tracker AI", page_icon="🎯", layout="wide")
st.title("🎯 SSC CGL Personal Roadmap AI Tool")

# 2. लाइव काउंटडाउन इंजन (Date Logic)
today = date.today()
prelims_date = date(2026, 9, 10)  # 10 सितम्बर 2026
mains_date = date(2026, 12, 10)   # 10 दिसम्बर 2026

days_to_pre = (prelims_date - today).days
days_to_main = (mains_date - today).days

# स्क्रीन पर काउंटडाउन दिखाना
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📅 आज की तारीख", value=today.strftime("%d %B, %Y"))
with col2:
    st.metric(label="⏳ Prelims Countdown (10 Sep)", value=f"{days_to_pre} Days Left", delta=f"-{days_to_pre}")
with col3:
    st.metric(label="🏆 Mains Countdown (10 Dec)", value=f"{days_to_main} Days Left", delta=f"-{days_to_main}")

st.markdown("---")

# 3. सिलेबस का डेटाबेस (6 सेक्शन्स और उनके सब-सेक्शन्स)
syllabus = {
    "English": ["Grammar (Error/Fillers)", "Vocabulary (Syn/Ant/Idioms)", "Reading Comprehension", "Cloze Test & Para Jumbles"],
    "Maths": ["Arithmetic (Percentage/P&L/SI-CI)", "Arithmetic (Ratio/Time & Work/Speed)", "Advanced (Algebra/Geometry)", "Advanced (Mensuration/Trigonometry/DI)"],
    "GK": ["History & Geography", "Polity & Constitution", "General Science (Phy/Chem/Bio)", "Static GK & Current Affairs"],
    "Reasoning": ["Verbal (Analogy/Syllogism/Blood Rel)", "Coding-Decoding & Series", "Non-Verbal (Mirror/Paper Cutting)", "Matrix & Embedded Figures"],
    "Economics": ["Micro & Macro Economics", "Indian Economy & Five Year Plans", "Budget & Banking Systems", "Inflation, Demand & Supply"],
    "Mock Tests": ["Sectional Mocks", "Full-Length Prelims Mocks", "Full-Length Mains Mocks", "Previous Year Papers (PYQs)"]
}

# 4. यूआई (UI) और यूजर इनपुट
st.subheader("📚 अपना सिलेबस स्क्रॉल करें और मार्क करें:")

total_topics = 0
completed_topics = 0

cols = st.columns(6)

for i, (subject, topics) in enumerate(syllabus.items()):
    with cols[i]:
        st.markdown(f"### **{subject}**")
        for topic in topics:
            total_topics += 1
            is_done = st.checkbox(topic, key=f"{subject}_{topic}")
            if is_done:
                completed_topics += 1
                st.caption("✅ Done")
            else:
                days_allocated = st.number_input("⏰ Days allowed:", min_value=1, max_value=30, value=5, key=f"time_{subject}_{topic}")

st.markdown("---")

# 5. पाई चार्ट इंजन
st.subheader("📊 आपकी तैयारी का प्रोग्रेस चार्ट")

incomplete_topics = total_topics - completed_topics

if total_topics > 0:
    fig = go.Figure(data=[go.Pie(
        labels=['Completed Topics', 'Syllabus Left'],
        values=[completed_topics, incomplete_topics],
        hole=.4,
        marker_colors=['#2ec4b6', '#e71d36']
    )])
    fig.update_layout(title_text="Overall Syllabus Completion Status")
    st.plotly_chart(fig, use_container_width=True)

    progress_percent = (completed_topics / total_topics)
    st.progress(progress_percent)
    st.write(f"**आपने कुल {total_topics} में से {completed_topics} टॉपिक्स पूरे कर लिए हैं! ({int(progress_percent*100)}% Complete)**")
