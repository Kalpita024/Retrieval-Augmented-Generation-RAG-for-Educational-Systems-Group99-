# Retrieval-Augmented-Generation-RAG-for-Educational-Systems-Group99-
 An AI-powered educational-systems using Retrieval-Augmented Generation (RAG) to generates summaries, important questions, flashcards, and revision note which will work as Exam Preparation Assistant
App link https://exam-prep-bot.streamlit.app

---

## 📌 Project Overview

EduGenie AI is a college group project built as part of our first-year engineering curriculum. It uses Large Language Models (LLMs), LangChain, and FAISS vector search to let students upload any academic PDF and instantly generate personalized study material from it.

The core idea is **RAG (Retrieval Augmented Generation)** — instead of the AI guessing answers, it reads your actual document and answers based on that content.

---

## ✨ Features

### 📄 Document Processing
- Upload one or more PDF files
- Automatic text extraction and chunking
- Semantic vector indexing with FAISS

### 📚 Study Tools
- **Notes Generator** — structured notes with headings and bullet points
- **Flashcards** — question-answer pairs for active recall
- **MCQ Generator** — exam-style multiple choice questions with answers
- **Question Bank** — 2-mark, 5-mark, and 10-mark questions sorted by difficulty

### 📊 Content Analysis
- **Topic Extraction** — identifies all major topics from the PDF
- **Topic Coverage** — visualizes how thoroughly each topic is covered
- **Importance Ranking** — ranks topics by exam relevance

### 📝 Exam Preparation
- **Mock Test** — interactive timed exam simulation with instant scoring
- **Revision Sheet** — condensed definitions, formulas, and key concepts
- Difficulty selector: Easy / Medium / Hard / Mixed

### 💬 AI Chat Assistant
- Ask any question about the uploaded document
- Context-aware answers using RAG
- Conversation history support

---

## 🏗️ Architecture

```
User uploads PDF
      │
      ▼
PDF Loader (PyPDF)
      │
      ▼
Text Splitter (RecursiveCharacterTextSplitter)
      │  chunk_size=1000, overlap=200
      ▼
Embeddings (Voyage AI / HuggingFace)
      │
      ▼
Vector Store (FAISS) ──── saved to disk
      │
      ▼
Retriever (top-k similarity search)
      │
      ▼
LLM (Groq — Llama 3.3 70B)
      │
      ▼
Study Tools / Analysis / Chat / Exam Prep
```

---

## ⚙️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Frontend | Streamlit | Python-based web UI |
| LLM | Groq API (Llama 3.3 70B) | Text generation |
| Embeddings | Voyage AI / HuggingFace | Semantic vector creation |
| Vector DB | FAISS | Fast similarity search |
| PDF Loading | PyPDF + LangChain | Extract text from PDFs |
| Pipeline | LangChain | Connect all components |
| Environment | python-dotenv | API key management |

---

## 📂 Project Structure

```
EduGenie/
│
├── src/
│   ├── app.py                        # Main entry point
│   │
│   ├── ingestion/
│   │   ├── pdf_loader.py             # Load PDFs with PyPDF
│   │   ├── text_splitter.py          # Chunk documents
│   │   ├── embeddings.py             # Voyage AI / HuggingFace embeddings
│   │   ├── vector_db.py              # Create and load FAISS index
│   │   └── retriever.py              # Similarity search
│   │
│   ├── model/
│   │   └── llm.py                    # Groq LLM setup
│   │
│   ├── study_tools/
│   │   ├── notes_generator.py
│   │   ├── flashcard_generator.py
│   │   ├── mcq_generator.py
│   │   └── question_bank_generator.py
│   │
│   ├── analysis/
│   │   ├── topic_extractor.py
│   │   ├── topic_coverage.py
│   │   └── importance_ranker.py
│   │
│   ├── exam_prep/
│   │   ├── mock_test_generator.py
│   │   └── revision_sheet_generator.py
│   │
│   ├── chatbot/
│   │   └── chatbot.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── prompt_service.py
│   │   └── parser_service.py
│   │
│   ├── frontend/
│   │   ├── ui/                       # Streamlit page renderers
│   │   └── components/               # Reusable UI components
│   │
│   ├── prompts/                      # .txt prompt templates
│   └── utils/
│       ├── logger.py
│       └── decorators.py
│
├── vector_store/                     # FAISS index (auto-generated)
├── saved_files/                      # Temp uploaded PDFs
├── requirements.txt
├── .env                              # API keys (never commit this)
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.10 or above
- pip

### 1. Clone the repository

```bash
git clone https://github.com/your-team/EduGenie
cd EduGenie
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
VOYAGE_API_KEY=your_voyage_api_key_here
```

Get your free API keys:
- **Groq:** https://console.groq.com
- **Voyage AI:** https://www.voyageai.com

### 5. Run the application

```bash
streamlit run src/app.py
```

Open your browser at `http://localhost:8501`

---

## 💡 How to Use

1. **Upload** one or more PDF files using the sidebar
2. Click **Process Documents** — this indexes the PDF into FAISS
3. Navigate to any tab:
   - **Study Tools** → generate notes, flashcards, MCQs, or a question bank
   - **Analysis** → extract and rank topics from your document
   - **Exam Prep** → run a mock test or generate a revision sheet
   - **Chat** → ask questions directly about your PDF

---

## 👥 Team — Group 99

| Member | Role |
|---|---|
| Member 1 | PDF Ingestion & Text Splitting |
| Member 2 | FAISS Vector Store & Retriever |
| Member 3 | Chatbot & RAG Pipeline |
| Member 4 | Notes & Summary Generator |
| Member 5 | Flashcard & MCQ Generator |
| Member 6 | LLM Integration & Services Layer |
| Member 7 | Analysis Module (Topic Extraction & Ranking) |
| Member 8 | Streamlit Frontend & UI Design |

---

## 🔮 Future Scope

- Export notes and revision sheets as PDF
- Multi-document comparison
- Voice-based question answering
- Adaptive difficulty based on user performance
- User login and study history tracking

---

## 📄 License

MIT License — free to use, modify, and distribute for educational purposes.

---

## 🙏 Acknowledgements

- [LangChain](https://www.langchain.com/) — RAG pipeline framework
- [Groq](https://groq.com/) — fast LLM inference
- [Voyage AI](https://www.voyageai.com/) — text embeddings
- [FAISS](https://faiss.ai/) — vector similarity search
- [Streamlit](https://streamlit.io/) — Python web UI framework
