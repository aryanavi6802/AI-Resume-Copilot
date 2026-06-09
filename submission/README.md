# AI Career Copilot — Submission Documentation

**City of Los Angeles · Department of General Services**
**Agentic Software Engineering Internship**

---

## 📁 Contents

| Document | Description |
| :--- | :--- |
| [Business_Statement.md](./Business_Statement.md) | Problem, business value, users served, features, impact, and future opportunities |
| [Logical_Structure.md](./Logical_Structure.md) | Architecture diagrams, data flow, agentic pipeline, RAG workflow, database flow (Mermaid) |
| [Technical_Implementation_Guide.md](./Technical_Implementation_Guide.md) | Full reconstruction guide — setup through deployment (14 sections) |
| [Submission_Index.md](./Submission_Index.md) | Source code locations, AI workflows, and reviewer quick-start instructions |

---

## 🚀 Quick Start

```bash
cd AI-Resume-Copilot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key" > .env
streamlit run app.py
```

Open **http://localhost:8501** → Upload a PDF resume → Paste a job description → Click **Run Agentic Analysis**.

---

## 🏗️ Project Architecture

```
AI-Resume-Copilot/
├── app.py                          # Streamlit UI (presentation layer)
├── services/
│   ├── gemini_service.py           # 5-agent agentic Gemini pipeline
│   ├── rag_service.py              # ChromaDB RAG (chunk → embed → retrieve)
│   ├── sponsorship_service.py      # Keyword-based sponsorship detection
│   └── export_service.py           # Markdown / JSON report export
├── database/
│   └── db.py                       # SQLite analysis history persistence
├── models/
│   └── analysis_models.py          # Dataclass models with serialization
├── data/                           # Auto-created at runtime
│   ├── analysis_history.db         # SQLite database
│   └── chroma_db/                  # ChromaDB vector store
├── submission/                     # ← You are here
│   ├── README.md
│   ├── Business_Statement.md
│   ├── Logical_Structure.md
│   ├── Technical_Implementation_Guide.md
│   └── Submission_Index.md
├── requirements.txt
├── .env
└── README.md
```

---

## 🤖 Key Technical Highlights

| Capability | Implementation |
| :--- | :--- |
| **Agentic AI** | 5 sequential Gemini agents: Resume Parser → JD Analyzer → Gap Analysis → Interview Prep → Sponsorship Evaluator |
| **RAG Pipeline** | ChromaDB with sentence-aware chunking, cosine-similarity retrieval, bidirectional querying |
| **Structured Output** | All agents return validated JSON; parsed into typed Python dataclasses |
| **Database** | SQLite with full CRUD — every analysis auto-saved, searchable history |
| **Export** | Markdown and JSON downloadable reports |
| **Sponsorship Detection** | Dual-layer: keyword matching (7 phrases) + AI contextual risk assessment |

---

## 📖 Recommended Review Order

1. **[Business_Statement.md](./Business_Statement.md)** — Understand the problem and value proposition
2. **[Logical_Structure.md](./Logical_Structure.md)** — See the architecture and data flow diagrams
3. **[Technical_Implementation_Guide.md](./Technical_Implementation_Guide.md)** — Deep dive into implementation
4. **[Submission_Index.md](./Submission_Index.md)** — Navigate source code and AI workflows
5. **Source Code** — Start with `app.py`, then `services/gemini_service.py`

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Vector Database | ChromaDB |
| Relational Database | SQLite |
| PDF Parsing | PyPDF2 |

---

## 📬 Contact

For questions regarding this submission, please refer to the project repository or contact the submitting intern.
