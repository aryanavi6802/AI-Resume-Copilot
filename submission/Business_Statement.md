# Business Statement — AI Career Copilot

## Project Overview

AI Career Copilot is an agentic AI-powered career intelligence platform that analyzes a candidate's resume against a target job description using a multi-stage AI pipeline. The system employs five specialized AI agents, a RAG (Retrieval-Augmented Generation) pipeline with ChromaDB, structured JSON outputs, and persistent SQLite storage to deliver actionable career insights including match scoring, gap analysis, behavioral interview preparation, and visa sponsorship risk assessment.

Built as a Streamlit web application powered by Google's Gemini 2.5 Flash, the platform demonstrates production-grade agentic software engineering principles suitable for government technical evaluation.

---

## Problem Being Solved

| Problem | Description |
| :--- | :--- |
| **Resume–JD Mismatch** | Candidates apply to roles without understanding alignment, leading to low callback rates and wasted effort. |
| **Interview Unpreparedness** | Behavioral interviews require mapping project experiences to question frameworks — a task most do manually and inconsistently. |
| **Visa Sponsorship Uncertainty** | International students on F-1 visas routinely apply to positions that explicitly exclude sponsorship candidates. |
| **Unstructured AI Outputs** | Most AI tools return free-form text that cannot be programmatically processed, stored, or compared. |

---

## Business Value

### 1. Time Savings
A single analysis that would take 30–60 minutes of manual review completes in under 30 seconds across five specialized AI agents. For 50 applications, this represents **25–50 hours of saved effort**.

### 2. Decision Quality
Structured match scores and gap analyses enable candidates to prioritize high-fit opportunities and strategically upskill.

### 3. Risk Mitigation
Dual-layer sponsorship detection (keyword matching + AI contextual analysis) prevents international candidates from pursuing ineligible positions.

### 4. Institutional Memory
SQLite persistence enables candidates to track their application history, compare scores across roles, and identify improvement patterns over time.

### 5. Agentic Architecture
The multi-agent pipeline demonstrates decomposition of complex tasks into specialized, auditable stages — a pattern applicable to any government workflow automation.

---

## Users Served

| User Segment | Description |
| :--- | :--- |
| **International Students** | F-1 visa holders needing sponsorship-aware job search tools |
| **Early-Career Professionals** | Graduates optimizing application-to-interview conversion |
| **Career Services Staff** | University advisors recommending self-service resume optimization |
| **Government HR Departments** | Municipal agencies evaluating candidates against role requirements |

---

## Key Features

| Feature | Technology | Description |
| :--- | :--- | :--- |
| 5-Stage Agentic Pipeline | Gemini 2.5 Flash | Sequential AI agents: Parse → Analyze → Gap → Interview → Sponsorship |
| RAG Retrieval | ChromaDB | Semantic chunking and cosine-similarity retrieval before LLM calls |
| Structured JSON Output | JSON Schema | All agents return validated, parseable JSON |
| Analysis History | SQLite | Persistent, searchable database of all analyses |
| Multi-Format Export | Markdown / JSON | Downloadable reports in human and machine-readable formats |
| Sponsorship Radar | Keyword + AI | Dual-layer visa risk detection |
| Agent Trace | Streamlit UI | Full transparency into each agent's input/output |

---

## Quantitative and Qualitative Impact

### Quantitative
- **5 specialized AI agents** processing each analysis
- **< 30 second** end-to-end pipeline execution
- **7 sponsorship exclusion phrases** detected via keyword matching
- **2 export formats** (Markdown + JSON) for every analysis
- **100% analysis persistence** — every result stored in SQLite

### Qualitative
- **Auditability**: Agent trace provides full transparency into AI decision-making
- **Reproducibility**: Structured JSON enables consistent, comparable analyses
- **Accessibility**: Streamlit interface requires zero technical knowledge to operate

---

## Future Opportunities

| Opportunity | Description |
| :--- | :--- |
| DOCX Resume Support | Extend parser to handle Word documents |
| ATS Keyword Optimization | Suggest keywords to improve applicant tracking system pass-through |
| External Sponsorship Data | Integrate with H1BGrader / MyVisaJobs for company-level sponsorship history |
| PDF Report Generation | Professional formatted PDF exports |
| Multi-Resume Comparison | Compare multiple resume versions against the same role |
| Government Workforce Adaptation | Adapt for municipal HR departments to screen internal candidates |
| Cloud Deployment | Deploy to Streamlit Community Cloud for public access |
