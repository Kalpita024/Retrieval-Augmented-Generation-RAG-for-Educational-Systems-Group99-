import streamlit as st
import re
import sys
from pathlib import Path
from io import BytesIO
from dotenv import load_dotenv

# ══════════════════════════════════════════════════════════
# BACKEND WIRING
# ══════════════════════════════════════════════════════════
# Explicitly load .env from the repo root BEFORE importing the
# generator modules. Streamlit runs app.py via exec(), which can
# confuse python-dotenv's automatic path-detection inside
# base_chain.py — loading it here guarantees GROQ_API_KEY is in
# os.environ by the time ChatGroq() is constructed.
REPO_ROOT = Path(__file__).resolve().parent
load_dotenv(REPO_ROOT / ".env")

# The generator files in src/study_tools/ use flat imports
# (e.g. "from base_chain import run_prompt"), so study_tools/
# itself must be on sys.path for those imports to resolve.
STUDY_TOOLS_DIR = REPO_ROOT / "src" / "study_tools"
sys.path.insert(0, str(STUDY_TOOLS_DIR))

from flashcard_generator import generate_flashcards      # noqa: E402
from summary_generator import generate_summary           # noqa: E402
from notes_generator import generate_notes               # noqa: E402
from chatbot import generate_chatbot_answer               # noqa: E402

# base_chain.py doesn't cap output length, so Groq reserves budget for a
# large possible response on every call — this alone can exceed the 6000
# tokens/minute free-tier limit even with a small prompt. Cap it here using
# .bind(), since direct attribute assignment on the ChatGroq pydantic model
# can be silently rejected post-init.
import base_chain  # noqa: E402
base_chain.llm = base_chain.llm.bind(max_tokens=600)

# PDF text extraction — self-contained here so the frontend doesn't
# depend on an unconfirmed function inside src/ingestion/. If your
# teammate's ingestion module exposes an extract_text(file) function,
# swap the body of extract_text_from_pdf() below to call it instead.
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader


def extract_text_from_pdf(uploaded_file) -> str:
    """Extracts and concatenates text from all pages of an uploaded PDF."""
    uploaded_file.seek(0)
    reader = PdfReader(BytesIO(uploaded_file.read()))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    uploaded_file.seek(0)
    return text.strip()


# Groq's free "on_demand" tier caps llama-3.1-8b-instant at 6000 tokens/minute
# TOTAL (prompt + completion). Roughly ~4 characters per token, so we cap the
# context we send per request well under that to leave room for the system/
# user prompt template text and the model's response tokens.
MAX_CONTEXT_CHARS = 4000


def truncate_context(text: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Trims context to stay under Groq's free-tier tokens-per-minute limit."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...content truncated to fit rate limits...]"


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
if "pdf_context" not in st.session_state:
    st.session_state.pdf_context = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None
if "summary_text" not in st.session_state:
    st.session_state.summary_text = ""
if "notes_text" not in st.session_state:
    st.session_state.notes_text = ""
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []  # list of {"role": "user"/"assistant", "content": str}

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
        # Only re-extract text if a new file was uploaded
        if st.session_state.pdf_name != uploaded_file.name:
            with st.spinner("Reading PDF..."):
                st.session_state.pdf_context = extract_text_from_pdf(uploaded_file)
                st.session_state.pdf_name = uploaded_file.name
                # Clear old results tied to the previous PDF
                st.session_state.flashcards = []
                st.session_state.revealed = {}
                st.session_state.summary_text = ""
                st.session_state.notes_text = ""
                st.session_state.chat_messages = []
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

    length = st.select_slider(
        "Summary length",
        options=["short", "medium", "long"],
        value="medium"
    )

    if st.button("✨ Generate Summary"):
        if uploaded_file and st.session_state.pdf_context:
            with st.spinner("Generating summary..."):
                try:
                    st.session_state.summary_text = generate_summary(
                        truncate_context(st.session_state.pdf_context), length=length
                    )
                except Exception as e:
                    st.error(f"Summary generation failed: {e}")
        else:
            st.error("Please upload a PDF first!")

    if st.session_state.summary_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(st.session_state.summary_text)
    else:
        st.info("Upload a PDF and click Generate Summary to see results here.")

elif st.session_state.active_tab == "Flashcards":
    st.markdown("### 🃏 Flashcards")
    st.markdown("<br>", unsafe_allow_html=True)

    count = st.slider("Number of flashcards", min_value=5, max_value=20, value=10, step=1)

    if st.button("✨ Generate Flashcards"):
        if uploaded_file and st.session_state.pdf_context:
            with st.spinner("Generating flashcards..."):
                try:
                    raw = generate_flashcards(truncate_context(st.session_state.pdf_context), count=count)
                    st.session_state.flashcards = parse_flashcards(raw)
                    st.session_state.revealed = {}
                except Exception as e:
                    st.error(f"Flashcard generation failed: {e}")
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

    topic = st.text_input("Topic (optional)", placeholder="e.g. Chapter 3 — Thermodynamics")

    if st.button("✨ Generate Notes"):
        if uploaded_file and st.session_state.pdf_context:
            with st.spinner("Generating notes..."):
                try:
                    st.session_state.notes_text = generate_notes(
                        truncate_context(st.session_state.pdf_context),
                        topic=topic if topic else "the given content"
                    )
                except Exception as e:
                    st.error(f"Notes generation failed: {e}")
        else:
            st.error("Please upload a PDF first!")

    if st.session_state.notes_text:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(st.session_state.notes_text)
    else:
        st.info("Upload a PDF and click Generate Notes to see results here.")

elif st.session_state.active_tab == "QA":
    st.markdown("### 🤖 Ask Questions")

    if not uploaded_file:
        st.info("Upload a PDF and type your question below.")
    else:
        # Render chat history
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_question = st.text_input(
        "", placeholder="Type your question here...", label_visibility="collapsed"
    )

    if st.button("Send →"):
        if not uploaded_file or not st.session_state.pdf_context:
            st.error("Please upload a PDF first!")
        elif not user_question.strip():
            st.error("Please type a question.")
        else:
            # Build chat_history string from prior turns
            history_str = "\n".join(
                f"{m['role'].capitalize()}: {m['content']}"
                for m in st.session_state.chat_messages
            )
            with st.spinner("Thinking..."):
                try:
                    answer = generate_chatbot_answer(
                        question=user_question,
                        context=truncate_context(st.session_state.pdf_context),
                        chat_history=history_str
                    )
                    st.session_state.chat_messages.append({"role": "user", "content": user_question})
                    st.session_state.chat_messages.append({"role": "assistant", "content": answer})
                    st.rerun()
                except Exception as e:
                    st.error(f"Answer generation failed: {e}")