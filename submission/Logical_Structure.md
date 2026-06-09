# Logical Structure — AI Career Copilot

## High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        UI["Streamlit Web App<br/>app.py"]
    end

    subgraph "Service Layer"
        SS["Sponsorship Service<br/>sponsorship_service.py"]
        RAG["RAG Service<br/>rag_service.py"]
        GS["Gemini Service<br/>gemini_service.py"]
        EX["Export Service<br/>export_service.py"]
    end

    subgraph "Data Layer"
        DB["SQLite Database<br/>db.py"]
        CHROMA["ChromaDB<br/>Vector Store"]
    end

    subgraph "External"
        GEMINI["Google Gemini 2.5 Flash"]
    end

    subgraph "Models"
        MOD["AnalysisResult<br/>analysis_models.py"]
    end

    UI --> SS
    UI --> RAG
    UI --> GS
    UI --> EX
    UI --> DB
    RAG --> CHROMA
    GS --> GEMINI
    GS --> MOD
    EX --> MOD
    DB --> MOD

    style UI fill:#4A90D9,stroke:#2C5F8A,color:#fff
    style GS fill:#7B68EE,stroke:#5A4FCF,color:#fff
    style RAG fill:#50C878,stroke:#3A9A5C,color:#fff
    style SS fill:#FF6B6B,stroke:#CC5555,color:#fff
    style EX fill:#FFB347,stroke:#CC8F39,color:#fff
    style DB fill:#DDA0DD,stroke:#B07FB0,color:#fff
    style CHROMA fill:#20B2AA,stroke:#178A82,color:#fff
    style GEMINI fill:#E91E63,stroke:#B71650,color:#fff
    style MOD fill:#87CEEB,stroke:#6BB3D0,color:#fff
```

---

## User Flow

```mermaid
flowchart TD
    A["User opens app"] --> B["Tab: New Analysis"]
    A --> H["Tab: Analysis History"]

    B --> C["Upload PDF resume"]
    C --> D["Paste job description"]
    D --> E["Click Run Agentic Analysis"]
    E --> F["View results:<br/>Score, Gaps, Interview Prep, Agent Trace"]
    F --> G["Download MD or JSON report"]

    H --> I["Search by filename / job title"]
    I --> J["View past analysis details"]
    J --> K["Re-export past report"]

    style A fill:#4A90D9,color:#fff
    style E fill:#E91E63,color:#fff
    style F fill:#50C878,color:#fff
    style G fill:#FFB347,color:#fff
```

---

## Data Flow — Complete Pipeline

```mermaid
sequenceDiagram
    actor User
    participant UI as Streamlit UI
    participant PDF as PyPDF2
    participant SS as Sponsorship Service
    participant RAG as RAG Service
    participant Chroma as ChromaDB
    participant GS as Gemini Service
    participant Gemini as Gemini 2.5 Flash
    participant DB as SQLite

    User->>UI: Upload PDF + Paste JD
    User->>UI: Click "Run Agentic Analysis"

    UI->>PDF: extract_text(pdf_file)
    PDF-->>UI: resume_text

    UI->>SS: check_sponsorship(jd_text)
    SS-->>UI: (flag, phrase)

    UI->>RAG: store_and_retrieve(resume_text, jd_text)
    RAG->>RAG: chunk_text(resume_text)
    RAG->>RAG: chunk_text(jd_text)
    RAG->>Chroma: Store resume chunks
    RAG->>Chroma: Store JD chunks
    RAG->>Chroma: Query resume with JD
    Chroma-->>RAG: Retrieved resume chunks
    RAG->>Chroma: Query JD with resume
    Chroma-->>RAG: Retrieved JD chunks
    RAG-->>UI: retrieved context

    UI->>GS: run_agentic_pipeline(context)

    GS->>Gemini: Agent 1 — Resume Parser
    Gemini-->>GS: Structured JSON
    GS->>Gemini: Agent 2 — JD Analyzer
    Gemini-->>GS: Structured JSON
    GS->>Gemini: Agent 3 — Gap Analysis
    Gemini-->>GS: Structured JSON
    GS->>Gemini: Agent 4 — Interview Prep
    Gemini-->>GS: Structured JSON
    GS->>Gemini: Agent 5 — Sponsorship Eval
    Gemini-->>GS: Structured JSON

    GS-->>UI: AnalysisResult

    UI->>DB: save_analysis(result)
    UI-->>User: Display results + downloads
```

---

## Agentic Pipeline Architecture

```mermaid
graph LR
    subgraph "Stage 1"
        A1["🤖 Agent 1<br/>Resume Parser"]
    end
    subgraph "Stage 2"
        A2["🤖 Agent 2<br/>JD Analyzer"]
    end
    subgraph "Stage 3"
        A3["🤖 Agent 3<br/>Gap Analysis"]
    end
    subgraph "Stage 4"
        A4["🤖 Agent 4<br/>Interview Prep"]
    end
    subgraph "Stage 5"
        A5["🤖 Agent 5<br/>Sponsorship Eval"]
    end

    A1 -->|"resume_data"| A3
    A2 -->|"jd_data"| A3
    A1 -->|"resume_data"| A4
    A3 -->|"gap_data"| A4
    A3 -->|"match_score + missing_skills"| RESULT["AnalysisResult"]
    A4 -->|"behavioral_questions"| RESULT
    A5 -->|"sponsorship_warning"| RESULT

    style A1 fill:#4A90D9,color:#fff
    style A2 fill:#7B68EE,color:#fff
    style A3 fill:#FF6B6B,color:#fff
    style A4 fill:#50C878,color:#fff
    style A5 fill:#FFB347,color:#fff
    style RESULT fill:#E91E63,color:#fff
```

---

## RAG Pipeline Flow

```mermaid
graph TD
    R["Resume PDF"] --> E1["PyPDF2 Text Extraction"]
    E1 --> C1["Sentence-Aware Chunking<br/>500 chars, 50 overlap"]
    C1 --> EMB1["ChromaDB Auto-Embedding"]
    EMB1 --> STORE1["resume_chunks Collection"]

    JD["Job Description"] --> C2["Sentence-Aware Chunking"]
    C2 --> EMB2["ChromaDB Auto-Embedding"]
    EMB2 --> STORE2["jd_chunks Collection"]

    STORE1 --> Q1["Query: JD → Resume<br/>Find relevant experience"]
    STORE2 --> Q2["Query: Resume → JD<br/>Find relevant requirements"]

    Q1 --> CTX["Retrieved Context"]
    Q2 --> CTX
    CTX --> AGENTS["Agentic Pipeline<br/>5 Gemini Calls"]

    style R fill:#4A90D9,color:#fff
    style JD fill:#7B68EE,color:#fff
    style CTX fill:#50C878,color:#fff
    style AGENTS fill:#E91E63,color:#fff
```

---

## Database Flow

```mermaid
graph TD
    ANALYSIS["Analysis Complete"] --> SAVE["save_analysis()"]
    SAVE --> SQLITE["SQLite: analysis_history"]

    USER["User opens History tab"] --> SEARCH{"Search query?"}
    SEARCH -->|Yes| QUERY["search_analyses(query)"]
    SEARCH -->|No| ALL["get_all_analyses()"]
    QUERY --> SQLITE
    ALL --> SQLITE
    SQLITE --> DISPLAY["Display in Streamlit"]
    DISPLAY --> EXPORT["Re-export MD / JSON"]

    style ANALYSIS fill:#50C878,color:#fff
    style SQLITE fill:#DDA0DD,color:#fff
    style EXPORT fill:#FFB347,color:#fff
```

---

## Component Interaction Summary

| Component | Depends On | Produces |
| :--- | :--- | :--- |
| `app.py` | All services, database, models | Streamlit UI |
| `gemini_service.py` | `analysis_models.py`, Gemini API | `AnalysisResult` |
| `rag_service.py` | ChromaDB | Retrieved context strings |
| `sponsorship_service.py` | None | `(bool, str)` tuple |
| `export_service.py` | `analysis_models.py` | Markdown / JSON strings |
| `db.py` | SQLite | Persisted analysis records |
| `analysis_models.py` | None | Dataclass definitions |

---

## External Services

| Service | Purpose | Auth |
| :--- | :--- | :--- |
| Google Gemini 2.5 Flash | LLM inference (5 agent calls per analysis) | API key in `.env` |
| ChromaDB | Local vector store for RAG embeddings | None (local) |
| SQLite | Local relational database for history | None (local) |
