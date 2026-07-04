import streamlit as st
import re

st.set_page_config(
    page_title="Exam Preparation Chatbot",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── SESSION STATE ──
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Summary"
if "flashcards" not in st.session_state:
    st.session_state.flashcards = []
if "revealed" not in st.session_state:
    st.session_state.revealed = {}

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

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        font-family: 'Playfair Display', serif !important;
        color: #3B2F1E;
    }

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

# ── HELPER: Parse flashcard text from backend ──
def parse_flashcards(raw_text: str):
    """
    Parses backend output format:
    1. Front: question
       Back: answer
    """
    cards = []
    # Split by numbered items like "1." "2." etc
    blocks = re.split(r'\n?\d+\.\s*', raw_text)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        # Extract Front and Back
        front_match = re.search(r'Front:\s*(.+?)(?=Back:|$)', block, re.DOTALL | re.IGNORECASE)
        back_match  = re.search(r'Back:\s*(.+?)$', block, re.DOTALL | re.IGNORECASE)
        if front_match and back_match:
            cards.append({
                "question": front_match.group(1).strip(),
                "answer":   back_match.group(1).strip()
            })
    return cards

# ── CONTENT AREA ──
if st.session_state.active_tab == "Summary":
    st.markdown("### 📄 Summary")
    st.info("Upload a PDF and click Generate Summary to see results here.")
    st.button("✨ Generate Summary")

elif st.session_state.active_tab == "Flashcards":
    st.markdown("### 🃏 Flashcards")
    st.markdown("<br>", unsafe_allow_html=True)

    count = st.slider("Number of flashcards", min_value=5, max_value=20, value=10, step=1)

    if st.button("✨ Generate Flashcards"):
        if uploaded_file:
            # ── Connect to backend here ──
            # from flashcards import generate_flashcards
            # context = extract_text(uploaded_file)
            # raw = generate_flashcards(context, count)
            # st.session_state.flashcards = parse_flashcards(raw)

            # ── Placeholder until backend is connected ──
            st.warning("Connect backend: call generate_flashcards(context, count) here.")
        else:
            st.error("Please upload a PDF first!")

    flashcards = st.session_state.flashcards

    if flashcards:
        st.markdown(f"**{len(flashcards)} Flashcards Generated**")
        st.markdown("<br>", unsafe_allow_html=True)

        for i, card in enumerate(flashcards):
            is_revealed = st.session_state.revealed.get(i, False)

            st.markdown(f"""
                <div style="
                    background-color: #EDE0C4;
                    border: 1px solid #C8AD7F;
                    border-radius: 14px;
                    padding: 22px 26px;
                    margin-bottom: 6px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
                ">
                    <div style="
                        font-size: 0.75rem;
                        font-weight: 700;
                        color: #A0845C;
                        letter-spacing: 0.1em;
                        text-transform: uppercase;
                        margin-bottom: 8px;
                        font-family: 'Nunito', sans-serif;
                    ">🃏 Card {i+1}</div>
                    <div style="
                        font-family: 'Playfair Display', serif;
                        font-size: 1.05rem;
                        color: #3B2F1E;
                        font-weight: 600;
                        margin-bottom: 12px;
                    ">{card['question']}</div>
                    {"<div style='border-top: 1px solid #C8AD7F; padding-top: 12px; font-family: Nunito, sans-serif; font-size: 0.95rem; color: #5C4827;'>💡 " + card['answer'] + "</div>" if is_revealed else ""}
                </div>
            """, unsafe_allow_html=True)

            btn_label = "🙈 Hide Answer" if is_revealed else "👁️ Reveal Answer"
            if st.button(btn_label, key=f"reveal_{i}"):
                st.session_state.revealed[i] = not is_revealed
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

    else:
        st.info("Click '✨ Generate Flashcards' to see styled flashcards here.")

elif st.session_state.active_tab == "Notes":
    st.markdown("### 📝 Notes")
    st.info("Upload a PDF and click Generate Notes to see results here.")
    st.button("✨ Generate Notes")

elif st.session_state.active_tab == "QA":
    st.markdown("### 🤖 Ask Questions")
    st.info("Upload a PDF and type your question below.")
    user_question = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed")
    st.button("Send →")