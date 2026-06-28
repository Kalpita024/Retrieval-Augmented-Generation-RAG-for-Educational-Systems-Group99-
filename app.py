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

# ── GLOBAL BEIGE BACKGROUND ──
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: #F2E8D9;
    }
    [data-testid="stHeader"] {
        background-color: #F2E8D9;
    }
    [data-testid="stSidebar"] {
        background-color: #E8D5B7;
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
        <h1 style="color: #3B2F1E; font-size: 2.8rem; margin-bottom: 10px;">
            📚 Exam Preparation Chatbot
        </h1>
        <p style="color: #3B2F1E; font-size: 1.1rem; margin-bottom: 6px;">
            Transform your PDFs into:
        </p>
        <p style="color: #5C4827; font-size: 1rem;">
            ✅ Smart Summaries &nbsp;|&nbsp; 🃏 Flashcards &nbsp;|&nbsp; 📝 Study Notes &nbsp;|&nbsp; 🤖 AI Q&A
        </p>
    </div>
""", unsafe_allow_html=True)

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
        <div style="
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid #C8AD7F;
            margin-bottom: 20px;
        ">
            <h2 style="color: #3B2F1E;">📚 StudyMind</h2>
            <p style="color: #7A6040; font-size: 0.85rem;">AI Exam Assistant</p>
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