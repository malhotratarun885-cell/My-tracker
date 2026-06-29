import streamlit as st
from datetime import date
import plotly.graph_objects as go
import urllib.parse

# 1. पेज कॉन्फ़िगरेशन और टाइटल
st.set_page_config(page_title="CGL Tracker AI", page_icon="🎯", layout="wide")
st.title("🎯 SSC CGL Ultimate Personal Roadmap Tool")

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

# 3. महा-डेटाबेस: कम्पलीट डिटेल्ड सिलेबस
syllabus_db = {
    "Maths 🧮": {
        "Number System": ["Whole numbers, Decimals & Fractions", "LCM & HCF", "Surds & Indices"],
        "Arithmetic": ["Percentage", "Profit and Loss", "SI & CI", "Ratio & Proportion", "Time & Work", "Time & Distance", "Boat & Stream", "Ages", "Partnership"],
        "Algebra": ["Algebraic Identities", "Linear Equations", "Quadratic Equations"],
        "Geometry": ["Lines & Angles", "Triangles", "Circles", "Polygons", "Congruence & Similarity"],
        "Mensuration": ["2D figures (Square, Rectangle, Triangle, Circle)", "3D figures (Cone, Cylinder, Sphere, Hemisphere)"],
        "Trigonometry": ["Trigonometric Ratios", "Heights & Distances", "Complementary Angles"],
        "Coordinate Geometry": ["Graphs of Linear Equations"],
        "Data Interpretation": ["Tables & Bar Graphs", "Pie Charts", "Histograms & Frequency Polygons"]
    },
    "English Grammar 🔤": {
        "Parts of Speech": ["Nouns", "Pronouns", "Verbs & Infinitives", "Adverbs", "Adjectives", "Prepositions", "Conjunctions", "Articles"],
        "Sentence Structure": ["Tense & Conditional Sentences", "Subject-Verb Agreement", "Question Tags"],
        "Voice & Speech": ["Active & Passive Voice", "Direct & Indirect Speech"]
    },
    "Reasoning 🧠": {
        "Verbal Reasoning": ["Dice", "Direction and distance", "Ranking system", "Alphabet test", "Calendar", "Clock", "Blood Relation", "Coding-decoding", "Age based question", "Venn Diagram", "Syllogism", "Statement and Conclusion", "Puzzle", "Sitting Arrangement", "Series", "Missing Numbers", "Analogy", "Classification", "Argument and Assumptions", "Cube and Cuboid", "Symbol and Notation", "Matrix"],
        "Non-Verbal Reasoning": ["Mirror and Water Image", "Paper Folding & cutting", "Counting Figure", "Figure Completion", "Figure Series", "Embedded Figure"]
    },
    "GK & Science 🌍": {
        "History": ["Ancient History", "Medieval History", "Modern History"],
        "Geography": ["Physical Geography", "Indian Geography"],
        "Polity & Econ": ["Polity & Constitution", "Economics & Five Year Plans"],
        "General Science": ["Physics", "Chemistry", "Biology"],
        "Dynamic GK": ["Static GK", "Current Affairs"]
    },
    "Mock Tests 📝": {
        "Prelims Mocks": ["Sectional Mocks", "Full-Length Prelims Mocks"],
        "Mocks & PYQs": ["Full-Length Mains Mocks", "Previous Year Papers (PYQs)"]
    }
}

# कुल टॉपिक्स की संख्या पहले से गिनना (कुल 86 टॉपिक्स हैं)
TOTAL_CHAPTERS_COUNT = 86

# --- डेटा कलेक्ट करने के लिए बैकग्राउंड लूप ---
total_lectures_global = 0
completed_lectures_global = 0
today_studied_topics = []

for subject, sub_categories in syllabus_db.items():
    for sub_cat, topics in sub_categories.items():
        for topic in topics:
            unique_key = f"{subject}_{sub_cat}_{topic}".replace(" ", "_")
            if st.session_state.get(f"today_{unique_key}", False):
                today_studied_topics.append(f"{subject} -> {topic}")

# 🚀 स्क्रीन पर सबसे ऊपर ओवरव्यू डैशबोर्ड
st.subheader("📊 Today's Work Overview (आज का लेखा-जोखा)")
sum_col1, sum_col2 = st.columns([2, 1])

with sum_col1:
    st.markdown(f"📝 **आज आपने कुल {len(today_studied_topics)} टॉपिक्स पर पढ़ाई की है:**")
    if today_studied_topics:
        for t in today_studied_topics:
            st.markdown(f"✅ {t}")
    else:
        st.warning("अभी तक आपने नीचे सिलेबस में किसी topic पर 'आज यह पढ़ा है' टिक नहीं किया है।")

with sum_col2:
    st.markdown("📬 **फ़ोन पर रिपोर्ट भेजें:**")
    phone_number = "9306707297"
    st.write(f"📲 टारगेट नंबर: `{phone_number}`")
    
    report_msg = f"CGL Daily Report ({today.strftime('%d-%m-%Y')}):\n"
    report_msg += f"आज कुल {len(today_studied_topics)} टॉपिक्स पढ़े गए।\n"
    if today_studied_topics:
        report_msg += "टॉपिक्स:\n" + "\n".join([f"- {t.split('-> ')[1]}" for t in today_studied_topics])
    else:
        report_msg += "आज कोई टॉपिक मार्क नहीं किया गया।"

    encoded_msg = urllib.parse.quote(report_msg)
    whatsapp_url = f"https://wa.me/91{phone_number}?text={encoded_msg}"
    
    st.link_button("🚀 व्हाट्सएप पर रिपोर्ट भेजें", whatsapp_url, use_container_width=True)

st.markdown("---")

# 4. यूआई (UI) मैनेजमेंट - Tabs सिस्टम
st.subheader("📚 अपना पूरा सिलेबस और लेक्चर्स यहाँ ट्रैक करें:")
tabs = st.tabs(list(syllabus_db.keys()))

# ग्लोबल चैप्टर काउंटर शुरू करना
current_chapter_number = 0

for tab_idx, (subject, sub_categories) in enumerate(syllabus_db.items()):
    with tabs[tab_idx]:
        sub_col1, sub_col2 = st.columns(2)
        
        for sub_cat_idx, (sub_cat, topics) in enumerate(sub_categories.items()):
            target_col = sub_col1 if sub_cat_idx % 2 == 0 else sub_col2
            
            with target_col:
                st.markdown(f"### 📂 {sub_cat}")
                for topic in topics:
                    current_chapter_number += 1  # हर चैप्टर पर काउंट बढ़ेगा
                    remaining_chapters = TOTAL_CHAPTERS_COUNT - current_chapter_number
                    
                    unique_key = f"{subject}_{sub_cat}_{topic}".replace(" ", "_")
                    st.markdown(f"##### **🔹 {topic}**")
                    
                    # आज क्या पढ़ा?
                    st.checkbox("📖 मैंने आज यह topic पढ़ा है", key=f"today_{unique_key}")

                    # लेक्चर ट्रैकर इनपुट
                    l_col1, l_col2, l_col3 = st.columns(3)
                    with l_col1:
                        total_l = st.number_input("कुल लेक्चर्स (Total):", min_value=1, max_value=100, value=10, key=f"total_l_{unique_key}")
                    with l_col2:
                        comp_l = st.number_input("पूरे हुए (Completed):", min_value=0, max_value=int(total_l), value=0, key=f"comp_l_{unique_key}")
                    
                    pending_l = total_l - comp_l
                    with l_col3:
                        st.metric(label="⏳ पेंडिंग लेक्चर्स", value=f"{pending_l} Left")
                    
                    # 🛠️ सेल्फ-स्टडी भाइयों के लिए नया 'चैप्टर काउंटर प्रोग्रेस इंडिकेटर'
                    st.caption(f"📖 **चैप्टर नंबर: {current_chapter_number} / {TOTAL_CHAPTERS_COUNT}** | ⏳ इसके बाद `{remaining_chapters}` चैप्टर्स और बाकी हैं।")
                    
                    total_lectures_global += total_l
                    completed_lectures_global += comp_l
                    st.markdown("---")

st.markdown("---")

# 5. पाई चार्ट और प्रोग्रेस इंजन
st.subheader("📊 आपकी तैयारी का लाइव प्रोग्रेस बोर्ड")
pending_lectures_global = total_lectures_global - completed_lectures_global

if total_lectures_global > 0:
    fig = go.Figure(data=[go.Pie(
        labels=['Completed Lectures', 'Pending Lectures'],
        values=[completed_lectures_global, pending_lectures_global],
        hole=.4,
        marker_colors=['#2ec4b6', '#e71d36']
    )])
    fig.update_layout(title_text="Overall Lecture Completion Status")
    st.plotly_chart(fig, use_container_width=True)

    progress_percent = (completed_lectures_global / total_lectures_global)
    st.progress(progress_percent)
    st.write(f"**आपने पूरे सिलेबस के कुल {total_lectures_global} लेक्चर्स में से {completed_lectures_global} लेक्चर्स पूरे कर लिए हैं! ({int(progress_percent*100)}% कंप्लीट)**")
