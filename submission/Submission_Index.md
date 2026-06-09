# Submission Index — AI Career Copilot

**Submitted to**: City of Los Angeles, Department of General Services  
**Program**: Agentic Software Engineering Internship  
**Date**: June 9, 2026

---

## Project Summary

AI Career Copilot is a production-grade agentic AI platform that analyzes resumes against job descriptions using a 5-stage AI agent pipeline, RAG retrieval via ChromaDB, structured JSON outputs, and SQLite persistence. The system demonstrates agentic software engineering, LLM integration, database operations, and professional documentation.

---

## Submission Contents

| # | Document | Description |
| :--- | :--- | :--- |
| 1 | [Business Statement](./Business_Statement.md) | Problem, business value, users, impact, features, future opportunities |
| 2 | [Logical Structure](./Logical_Structure.md) | 6 Mermaid diagrams: architecture, user flow, data flow, agentic pipeline, RAG flow, database flow |
| 3 | [Technical Implementation Guide](./Technical_Implementation_Guide.md) | 14-section reconstruction guide: setup through deployment |
| 4 | [Submission Index](./Submission_Index.md) | This file — navigation and reviewer instructions |

---

## Source Code Locations

| File | Path | Description |
| :--- | :--- | :--- |
| `app.py` | `/app.py` | Streamlit UI — two tabs, result display, exports |
| `gemini_service.py` | `/services/gemini_service.py` | 5-agent agentic pipeline with Gemini |
| `rag_service.py` | `/services/rag_service.py` | ChromaDB RAG: chunking, embedding, retrieval |
| `sponsorship_service.py` | `/services/sponsorship_service.py` | Keyword-based sponsorship detection |
| `export_service.py` | `/services/export_service.py` | Markdown and JSON export |
| `db.py` | `/database/db.py` | SQLite CRUD for analysis history |
| `analysis_models.py` | `/models/analysis_models.py` | Dataclass models with serialization |
| `requirements.txt` | `/requirements.txt` | 5 Python dependencies |
| `README.md` | `/README.md` | Professional project documentation |

---

## Architecture Overview

| Layer | Components |
| :--- | :--- |
| **Presentation** | `app.py` (Streamlit) |
| **AI / Agentic** | `gemini_service.py` (5 agents) |
| **Retrieval** | `rag_service.py` (ChromaDB) |
| **Detection** | `sponsorship_service.py` |
| **Export** | `export_service.py` |
| **Persistence** | `db.py` (SQLite) |
| **Models** | `analysis_models.py` |

---

## AI Workflows

| Workflow | Location | Description |
| :--- | :--- | :--- |
| Agent 1: Resume Parser | `gemini_service.py` | Extracts skills, projects, education |
| Agent 2: JD Analyzer | `gemini_service.py` | Extracts requirements, responsibilities |
| Agent 3: Gap Analysis | `gemini_service.py` | Produces match score and missing skills |
| Agent 4: Interview Prep | `gemini_service.py` | Generates 3 tailored behavioral questions |
| Agent 5: Sponsorship Eval | `gemini_service.py` | AI-powered sponsorship risk assessment |
| RAG Pipeline | `rag_service.py` | Chunk → Embed → Store → Retrieve |

---

## Reviewer Instructions

### Quick Start

```bash
cd AI-Resume-Copilot
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Testing

1. Open `http://localhost:8501`
2. Upload any PDF resume in the sidebar
3. Paste a job description
4. Click **"🚀 Run Agentic Analysis"**
5. Review: Match score, gap table, interview questions
6. Expand **"🤖 Agent Trace"** to see all 5 agent outputs
7. Download reports in Markdown or JSON
8. Switch to **"📊 Analysis History"** tab to see saved results
9. Test sponsorship detection with a JD containing "no sponsorship"

### Recommended Review Order

1. [Business Statement](./Business_Statement.md) — understand the problem
2. [Logical Structure](./Logical_Structure.md) — see the architecture diagrams
3. [Technical Implementation Guide](./Technical_Implementation_Guide.md) — deep dive
4. Source code — start with `app.py`, then `services/gemini_service.py`
