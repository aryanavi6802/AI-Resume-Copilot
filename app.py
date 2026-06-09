"""AI Career Copilot — Main Streamlit Application.

UI layer only. All business logic is delegated to service modules.
"""

import streamlit as st
import json
from PyPDF2 import PdfReader

from services.gemini_service import run_agentic_pipeline
from services.sponsorship_service import check_sponsorship
from services.rag_service import store_and_retrieve
from services.export_service import export_markdown, export_json
from models.analysis_models import AnalysisResult
from database.db import (
    init_db,
    save_analysis,
    get_all_analyses,
    search_analyses,
    get_analysis_by_id,
)

# ── Initialise database ────────────────────────────────────────
init_db()

# ── Page config ─────────────────────────────────────────────────
st.set_page_config(page_title="AI Career Copilot", page_icon="🎯", layout="wide")

st.title("🎯 AI Career Copilot")
st.caption(
    "Agentic AI Pipeline • RAG Retrieval • Structured Outputs • SQLite History"
)


# ── Helper ──────────────────────────────────────────────────────
def extract_text(pdf_file) -> str:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


# ── Tabs ────────────────────────────────────────────────────────
tab_new, tab_history = st.tabs(["🔍 New Analysis", "📊 Analysis History"])

# ================================================================
# TAB 1 — NEW ANALYSIS
# ================================================================
with tab_new:
    with st.sidebar:
        st.header("📄 Resume Upload")
        res_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
        job_title = st.text_input(
            "Job Title (optional)", placeholder="e.g. Software Engineer"
        )
        st.divider()
        st.info("Upload a PDF resume and paste a job description to run the analysis.")

    st.subheader("📋 Job Description")
    jd_text = st.text_area("Paste the full job description:", height=200)

    if st.button("🚀 Run Agentic Analysis", type="primary", use_container_width=True):
        if not res_file or not jd_text:
            st.warning("Please upload a resume and paste a job description.")
        else:
            with st.spinner("Running 5-stage agentic pipeline…"):
                # 1. Extract PDF text
                resume_text = extract_text(res_file)

                # 2. Sponsorship keyword check
                spons_flag, spons_phrase = check_sponsorship(jd_text)

                # 3. RAG: chunk → embed → store → retrieve
                rag = store_and_retrieve(resume_text, jd_text)

                # 4. Agentic pipeline with retrieved context
                result = run_agentic_pipeline(
                    resume_context=rag["resume_context"] or resume_text,
                    jd_context=rag["jd_context"] or jd_text,
                    sponsorship_flag=spons_flag,
                    sponsorship_phrase=spons_phrase,
                )

                # 5. Persist to SQLite
                save_analysis(
                    resume_filename=res_file.name,
                    job_title=job_title or "Untitled",
                    match_score=result.match_score,
                    status=result.status,
                    sponsorship_flag=spons_flag,
                    analysis_json=result.to_json(),
                )

            # ── Display results ─────────────────────────────
            st.divider()

            # Sponsorship warning
            if result.sponsorship_warning:
                st.error(f"⚠️ SPONSORSHIP WARNING: {result.sponsorship_warning}")

            # Match overview
            col1, col2, col3 = st.columns(3)
            col1.metric("Match Score", f"{result.match_score}%")
            col2.metric("Status", result.status)
            col3.metric("RAG Chunks", f"{rag['resume_chunks_total']} + {rag['jd_chunks_total']}")

            st.success(f"**Key Advantage**: {result.key_advantage}")

            # Gap analysis table
            st.subheader("📊 Technical Gap Analysis")
            if result.missing_skills:
                skills_data = [
                    {"Skill": s.skill, "Priority": s.priority}
                    for s in result.missing_skills
                ]
                st.table(skills_data)
            else:
                st.info("No significant skill gaps identified.")

            # Interview prep
            st.subheader("🎤 Behavioral Interview Prep")
            for i, q in enumerate(result.behavioral_questions, 1):
                with st.expander(f"Question {i}: {q.question[:80]}…" if len(q.question) > 80 else f"Question {i}: {q.question}"):
                    st.markdown(f"**{q.question}**")
                    st.markdown(f"- **Project**: {q.project}")
                    st.markdown(f"- **Focus**: {q.focus}")

            # Agent trace
            with st.expander("🤖 Agent Trace (5 stages)"):
                for a in result.agent_trace:
                    st.markdown(f"**Stage {a.stage} — {a.agent_name}** ({a.timestamp})")
                    st.json(a.data)

            # Exports
            st.subheader("📥 Export Report")
            exp1, exp2 = st.columns(2)
            with exp1:
                st.download_button(
                    "Download Markdown (.md)",
                    export_markdown(result),
                    file_name="career_report.md",
                    mime="text/markdown",
                )
            with exp2:
                st.download_button(
                    "Download JSON (.json)",
                    export_json(result),
                    file_name="career_report.json",
                    mime="application/json",
                )

# ================================================================
# TAB 2 — ANALYSIS HISTORY
# ================================================================
with tab_history:
    st.subheader("📊 Analysis History")

    search_query = st.text_input(
        "Search by filename, job title, or status", key="history_search"
    )

    rows = search_analyses(search_query) if search_query else get_all_analyses()

    if not rows:
        st.info("No analyses found. Run your first analysis in the New Analysis tab!")
    else:
        for row in rows:
            with st.expander(
                f"**{row['resume_filename']}** — {row['job_title']} "
                f"({row['match_score']}% • {row['status']}) — {row['timestamp'][:10]}"
            ):
                try:
                    data = json.loads(row["analysis_json"])
                    result = AnalysisResult.from_dict(data)
                    st.metric("Match Score", f"{result.match_score}%")
                    st.markdown(f"**Status**: {result.status}")
                    st.markdown(f"**Key Advantage**: {result.key_advantage}")
                    if result.sponsorship_warning:
                        st.warning(result.sponsorship_warning)
                    if result.missing_skills:
                        st.markdown("**Missing Skills**:")
                        for s in result.missing_skills:
                            st.markdown(f"- {s.skill} ({s.priority})")
                    if result.behavioral_questions:
                        st.markdown("**Interview Questions**:")
                        for q in result.behavioral_questions:
                            st.markdown(f"- *{q.question}* → {q.project}")
                    c1, c2 = st.columns(2)
                    with c1:
                        st.download_button(
                            "Export MD",
                            export_markdown(result),
                            file_name=f"report_{row['id']}.md",
                            key=f"md_{row['id']}",
                        )
                    with c2:
                        st.download_button(
                            "Export JSON",
                            export_json(result),
                            file_name=f"report_{row['id']}.json",
                            key=f"json_{row['id']}",
                        )
                except Exception as e:
                    st.error(f"Error loading analysis: {e}")