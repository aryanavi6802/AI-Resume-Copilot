# Technical Implementation Guide — AI Career Copilot

> **Purpose**: Step-by-step instructions to rebuild the application from scratch.

---

## 1. Tech Stack

| Layer | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| LLM SDK | `google-generativeai` |
| Vector Database | ChromaDB |
| Relational Database | SQLite (built-in) |
| PDF Parsing | PyPDF2 |
| Environment | python-dotenv |

---

## 2. Setup

```bash
mkdir AI-Resume-Copilot && cd AI-Resume-Copilot
python3 -m venv .venv
source .venv/bin/activate
pip install streamlit google-generativeai PyPDF2 python-dotenv chromadb
echo "GOOGLE_API_KEY=your_key" > .env
```

---

## 3. Folder Structure

```
AI-Resume-Copilot/
├── app.py                      # Streamlit UI layer
├── services/
│   ├── __init__.py
│   ├── gemini_service.py       # 5-agent agentic pipeline
│   ├── rag_service.py          # ChromaDB RAG pipeline
│   ├── sponsorship_service.py  # Keyword sponsorship detection
│   └── export_service.py       # MD / JSON export
├── database/
│   ├── __init__.py
│   └── db.py                   # SQLite persistence
├── models/
│   ├── __init__.py
│   └── analysis_models.py      # Dataclass models
├── data/                       # Auto-created at runtime
│   ├── analysis_history.db
│   └── chroma_db/
├── submission/                 # Documentation
├── requirements.txt
├── .env
└── README.md
```

---

## 4. Frontend Architecture

**Framework**: Streamlit (Python-native, no JavaScript).

**Page Config**: `st.set_page_config(page_title="AI Career Copilot", layout="wide")`

**Layout — Two Tabs**:

| Tab | Purpose |
| :--- | :--- |
| 🔍 New Analysis | Upload resume, paste JD, run pipeline, view results, download exports |
| 📊 Analysis History | Search and view past analyses, re-export reports |

**Sidebar**: PDF file uploader + optional job title input.

**Results Display**: `st.metric()` for score, `st.table()` for gap analysis, `st.expander()` for interview questions and agent trace, `st.download_button()` for exports.

---

## 5. Backend Architecture

No separate backend server. Streamlit process runs all logic. Architecture follows a **service-oriented pattern** within a single process:

- `app.py` → UI only, delegates all logic
- `services/` → Business logic modules
- `database/` → Persistence layer
- `models/` → Data structures

---

## 6. Database Schema

**File**: `database/db.py`  
**Engine**: SQLite via Python `sqlite3`  
**Path**: `data/analysis_history.db` (auto-created)

```sql
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    resume_filename TEXT NOT NULL,
    job_title TEXT DEFAULT '',
    match_score INTEGER DEFAULT 0,
    status TEXT DEFAULT '',
    sponsorship_flag INTEGER DEFAULT 0,
    analysis_json TEXT NOT NULL
);
```

**Functions**: `init_db()`, `save_analysis()`, `get_all_analyses()`, `get_analysis_by_id()`, `search_analyses()`

---

## 7. AI Workflow — Agentic Pipeline

**File**: `services/gemini_service.py`

### Agent Architecture

Each agent is a Python function that:
1. Constructs a focused prompt
2. Calls `model.generate_content(prompt)` via the Gemini SDK
3. Parses JSON from the response
4. Returns an `AgentOutput` dataclass

### Pipeline Stages

| Stage | Agent | Input | Output |
| :--- | :--- | :--- | :--- |
| 1 | Resume Parser | resume context | skills, projects, experience, education |
| 2 | JD Analyzer | JD context | job title, required/preferred skills, responsibilities |
| 3 | Gap Analysis | Agent 1 + Agent 2 output | match_score, status, key_advantage, missing_skills |
| 4 | Interview Prep | Agent 1 + Agent 3 output | 3 behavioral questions with project mappings |
| 5 | Sponsorship Eval | JD text + keyword detection | sponsorship_warning, risk_level |

### Data Flow Between Agents

```
Agent 1 (resume_data) ──┐
                         ├──→ Agent 3 (gap_data) ──┐
Agent 2 (jd_data) ──────┘                          ├──→ Agent 4 (questions)
Agent 1 (resume_data) ─────────────────────────────┘
Agent 5 (sponsorship) ─── independent
```

### Orchestrator

`run_agentic_pipeline()` executes all 5 stages sequentially and assembles the final `AnalysisResult`.

---

## 8. RAG Pipeline

**File**: `services/rag_service.py`

### Step 1: Chunking
`chunk_text()` splits text using sentence-aware splitting:
- Splits at sentence boundaries (`.`, `!`, `?`)
- Target chunk size: 500 characters
- Overlap: 50 characters
- Fallback: character-based splitting when no sentence boundaries exist

### Step 2: Embedding & Storage
ChromaDB auto-generates embeddings using its built-in ONNX MiniLM-L6-V2 model. Two collections are created per analysis:
- `resume_chunks` — cosine similarity space
- `jd_chunks` — cosine similarity space

### Step 3: Retrieval
Bidirectional semantic retrieval:
- **JD → Resume**: Query resume collection with JD text to find relevant experience
- **Resume → JD**: Query JD collection with resume text to find relevant requirements
- Top-k = 5 chunks per direction

### Step 4: Context Injection
Retrieved chunks are concatenated and passed to the agentic pipeline as `resume_context` and `jd_context`.

---

## 9. Prompt Flow

Each agent receives a prompt with:
1. **Role assignment**: "You are Agent N: [Name]"
2. **Input data**: Either raw text or JSON from previous agents
3. **Output schema**: Exact JSON structure to return
4. **Instruction**: "Return ONLY valid JSON"

### JSON Parsing

`_parse_json_response()` handles three cases:
1. Direct JSON parsing
2. Extraction from ` ```json ``` ` code fences
3. Extraction of first `{...}` block via regex

---

## 10. Structured Output Schema

```json
{
  "match_score": 85,
  "status": "Strong Match",
  "key_advantage": "Strong Python and ML background",
  "missing_skills": [
    {"skill": "Kubernetes", "priority": "High"},
    {"skill": "GraphQL", "priority": "Medium"}
  ],
  "behavioral_questions": [
    {
      "question": "Tell me about a time you led a technical project",
      "project": "AI Resume Copilot",
      "focus": "Leadership and technical decision-making"
    }
  ],
  "sponsorship_warning": ""
}
```

---

## 11. Error Handling

| Scenario | Handler |
| :--- | :--- |
| Missing resume or JD | `st.warning()` prevents pipeline execution |
| Missing API key | `ValueError` raised by `_get_model()` |
| Gemini API failure | `try/except` in `app.py` displays `st.error()` |
| JSON parse failure | `_parse_json_response()` tries 3 extraction strategies |
| Empty PDF text | RAG returns raw text as fallback context |
| ChromaDB errors | `try/except` on collection deletion |

---

## 12. Export Formats

**Markdown**: `result.to_markdown()` generates a formatted report with headers, tables, and bullet points.

**JSON**: `result.to_json()` generates pretty-printed JSON matching the structured output schema.

Both are served via `st.download_button()`.

---

## 13. Deployment

### Local (Current)
```bash
source .venv/bin/activate
streamlit run app.py
# → http://localhost:8501
```

### Streamlit Community Cloud
1. Push to GitHub
2. Go to share.streamlit.io
3. Select repo, set main file to `app.py`
4. Add `GOOGLE_API_KEY` as a secret
5. Deploy

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 14. Reconstruction Checklist

1. Create folder structure with `__init__.py` files
2. Create `models/analysis_models.py` with dataclasses
3. Create `services/sponsorship_service.py` with keyword matching
4. Create `database/db.py` with SQLite CRUD
5. Create `services/rag_service.py` with ChromaDB pipeline
6. Create `services/gemini_service.py` with 5-agent pipeline
7. Create `services/export_service.py` with MD/JSON output
8. Create `app.py` with Streamlit UI and two tabs
9. Create `requirements.txt` with 5 packages
10. Create `.env` with API key
11. Run `pip install -r requirements.txt`
12. Run `streamlit run app.py`
13. Test: upload PDF, paste JD, verify all 5 agents execute
14. Test: verify history tab shows saved analysis
15. Test: verify MD and JSON downloads
