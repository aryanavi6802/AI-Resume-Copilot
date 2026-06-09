# 🎯 AI Career Copilot

**An agentic AI-powered career intelligence platform** that analyzes resumes against job descriptions using a multi-stage AI pipeline with RAG retrieval, structured JSON outputs, and persistent analysis history.

Built for the **City of Los Angeles Department of General Services — Agentic Software Engineering Internship**.

---

## Problem

Job seekers face three high-friction problems:

| Problem | Impact |
| :--- | :--- |
| **Resume–JD Mismatch** | Low callback rates from blind applications |
| **Interview Unpreparedness** | Generic prep that doesn't leverage actual project experience |
| **Visa Sponsorship Uncertainty** | International students waste time on ineligible positions |

AI Career Copilot solves all three with a single-click agentic AI pipeline.

---

## Features

### 🤖 5-Stage Agentic Pipeline
Five specialized AI agents process each analysis sequentially:

1. **Resume Parser** — Extracts skills, projects, and experience
2. **JD Analyzer** — Extracts requirements and qualifications
3. **Gap Analysis Engine** — Produces match score and missing skills
4. **Interview Prep Generator** — Creates tailored behavioral questions
5. **Sponsorship Evaluator** — Assesses visa sponsorship risk

### 🔍 RAG Pipeline (ChromaDB)
- Sentence-aware document chunking
- Cosine-similarity semantic retrieval
- Bidirectional querying (JD→Resume, Resume→JD)
- Retrieved context passed to AI agents

### 📊 Structured JSON Output
All AI agents return validated JSON. The final output follows a strict schema with match score, status, missing skills, behavioral questions, and sponsorship warnings.

### 🗄️ SQLite Analysis History
- Every analysis is automatically persisted
- Searchable history by filename, job title, or status
- View and re-export past analyses

### 📥 Multi-Format Export
- **Markdown** (.md) — human-readable report
- **JSON** (.json) — machine-readable structured data

### 🛡️ Sponsorship Radar
- Keyword-based detection of 7 common exclusion phrases
- AI-powered contextual risk assessment via Agent 5

---

## Architecture

```
AI-Resume-Copilot/
├── app.py                          # Streamlit UI (presentation layer)
├── services/
│   ├── gemini_service.py           # 5-agent Gemini pipeline
│   ├── rag_service.py              # ChromaDB RAG pipeline
│   ├── sponsorship_service.py      # Keyword sponsorship detection
│   └── export_service.py           # Markdown / JSON export
├── database/
│   └── db.py                       # SQLite persistence
├── models/
│   └── analysis_models.py          # Dataclass models
├── data/                           # Auto-created at runtime
│   ├── analysis_history.db         # SQLite database
│   └── chroma_db/                  # ChromaDB vector store
├── submission/                     # Documentation for review
│   ├── Business_Statement.md
│   ├── Logical_Structure.md
│   ├── Technical_Implementation_Guide.md
│   └── Submission_Index.md
├── requirements.txt
├── .env
└── README.md
```

---

## Tech Stack

| Component | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| LLM SDK | google-generativeai |
| Vector Database | ChromaDB |
| Database | SQLite |
| PDF Parsing | PyPDF2 |
| Environment | python-dotenv |

---

## RAG Pipeline

```
Resume PDF → Text Extraction → Sentence-Aware Chunking → ChromaDB Embeddings
                                                              ↓
Job Description → Sentence-Aware Chunking → ChromaDB Embeddings
                                                              ↓
                                         Cosine Similarity Retrieval
                                                              ↓
                                          Retrieved Context → Gemini Agents
```

---

## Database Design

**Table: `analysis_history`**

| Column | Type | Description |
| :--- | :--- | :--- |
| id | INTEGER PK | Auto-incrementing identifier |
| timestamp | TEXT | ISO 8601 timestamp |
| resume_filename | TEXT | Original PDF filename |
| job_title | TEXT | User-provided job title |
| match_score | INTEGER | AI-generated match percentage |
| status | TEXT | Strong Match / Potential / Gap Heavy |
| sponsorship_flag | INTEGER | 0 or 1 |
| analysis_json | TEXT | Full structured JSON result |

---

## Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/AI-Resume-Copilot.git
cd AI-Resume-Copilot

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API key
echo "GOOGLE_API_KEY=your_key_here" > .env

# 5. Run the application
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## Screenshots

> *Screenshots will be added after deployment.*

| Screen | Description |
| :--- | :--- |
| New Analysis | Upload resume, paste JD, run pipeline |
| Results | Match score, gap table, interview questions |
| Agent Trace | Expandable view of all 5 agent outputs |
| History | Searchable table of past analyses |

---

## Future Improvements

- DOCX resume support
- Resume keyword suggestions for ATS optimization
- Integration with H1BGrader / MyVisaJobs sponsorship databases
- PDF report export with professional formatting
- Multi-resume comparison
- Batch application analysis
- Migration to Google Gen AI SDK
- Deployment to Streamlit Community Cloud

---

## License

This project was developed for the City of Los Angeles Department of General Services Agentic Software Engineering Internship program.
