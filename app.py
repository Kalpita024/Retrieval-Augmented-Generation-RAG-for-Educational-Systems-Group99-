import streamlit as st

st.set_page_config(
    page_title="Exam Preparation Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ──
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Summary"

# ── GLOBAL BEIGE BACKGROUND + FONTS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Nunito:wght@400;600;700&display=swap');

    [data-testid="stAppViewContainer"] {
        background-color: #F2E8D9;
        font-family: 'Nunito', sans-serif;
    }
    [data-testid="stHeader"] {
        background-color: #F2E8D9;
    }
    [data-testid="stSidebar"] {
        background-color: #E8D5B7;
        font-family: 'Playfair Display', serif !important;
    }

    /* Apply Playfair only to text elements, NOT icons */
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif !important;
        color: #3B2F1E;
    }

    /* Keep icon fonts untouched so they render as icons, not text */
    [data-testid="stSidebar"] [data-testid="stIconMaterial"],
    [data-testid="stSidebar"] .material-icons,
    [data-testid="stSidebar"] [class*="icon"] {
        font-family: 'Material Symbols Rounded', sans-serif !important;
    }

    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #3B2F1E !important;
    }
    p, div, label {
        font-family: 'Nunito', sans-serif !important;
    }
    .stButton > button {
        font-family: 'Playfair Display', serif !important;
        font-size: 1.1rem !important;
        background-color: #D4B896 !important;
        color: #3B2F1E !important;
        border: 1px solid #C8AD7F !important;
        border-radius: 10px !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background-color: #C8AD7F !important;
        color: #fff !important;
    }
</style>
""", unsafe_allow_html=True)

# ── HERO SECTION ──
st.markdown("""
    <div style="
        background-color: #D4B896;
        padding: 50px 40px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 30px;
        border: 2px solid #C8AD7F;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    ">
        <h1 style="
            color: #3B2F1E;
            font-size: 2.8rem;
            font-family: 'Playfair Display', serif;
            margin-bottom: 10px;
        ">
            📚 Exam Preparation Chatbot
        </h1>
        <p style="
            color: #3B2F1E;
            font-size: 1.1rem;
            font-family: 'Nunito', sans-serif;
            margin-bottom: 6px;
        ">
            Transform your PDFs into:
        </p>
        <p style="
            color: #5C4827;
            font-size: 1rem;
            font-family: 'Nunito', sans-serif;
        ">
            ✅ Smart Summaries &nbsp;|&nbsp; 🃏 Flashcards &nbsp;|&nbsp; 📝 Study Notes &nbsp;|&nbsp; 🤖 AI Q&A
        </p>
    </div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 24px 0 20px 0;
            border-bottom: 2px solid #C8AD7F;
            margin-bottom: 20px;
        ">
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 2.4rem;
                font-weight: 700;
                color: #3B2F1E;
                line-height: 1.1;
            ">
                📚 StudyMind
            </div>
            <div style="
                font-family: 'Playfair Display', serif;
                font-size: 1rem;
                color: #7A6040;
                margin-top: 4px;
            ">
                ~ AI Exam Assistant ~
            </div>
            <div style="
                margin-top: 10px;
                background: linear-gradient(90deg, #C8AD7F, #D4B896, #C8AD7F);
                height: 3px;
                border-radius: 10px;
            "></div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Upload your PDF")
    uploaded_file = st.file_uploader("", type=["pdf"], label_visibility="collapsed")

    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} uploaded!")
    else:
        st.info("👆 Upload a PDF to get started")

    st.markdown("---")
    st.markdown("### 🗂️ Navigate")

    if st.button("📄 Summary"):
        st.session_state.active_tab = "Summary"

    if st.button("🃏 Flashcards"):
        st.session_state.active_tab = "Flashcards"

    if st.button("📝 Notes"):
        st.session_state.active_tab = "Notes"

    if st.button("🤖 Ask Questions"):
        st.session_state.active_tab = "QA"
  
# ── CONTENT AREA ──
if st.session_state.active_tab == "Summary":
    st.markdown("### 📄 Summary")
    st.info("Upload a PDF and click Generate Summary to see results here.")
    st.button("✨ Generate Summary")

elif st.session_state.active_tab == "Flashcards":
    st.markdown("### 🃏 Flashcards")
    st.info("Upload a PDF and click Generate Flashcards to see results here.")
    st.button("✨ Generate Flashcards")

elif st.session_state.active_tab == "Notes":
    st.markdown("### 📝 Notes")
    st.info("Upload a PDF and click Generate Notes to see results here.")
    st.button("✨ Generate Notes")

elif st.session_state.active_tab == "QA":
    st.markdown("### 🤖 Ask Questions")
    st.info("Upload a PDF and type your question below.")
    user_question = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
    st.button("Send →")