"""Gemini AI service with multi-stage agentic pipeline.

Agents:
  1. Resume Parser — extracts structured candidate profile
  2. JD Analyzer — extracts structured job requirements
  3. Gap Analysis Engine — compares profile vs requirements
  4. Interview Prep Generator — creates tailored behavioral questions
  5. Sponsorship Evaluator — assesses visa sponsorship risk
"""

import google.generativeai as genai
import json
import os
import re
from dotenv import load_dotenv
from datetime import datetime
from models.analysis_models import (
    AnalysisResult,
    MissingSkill,
    BehavioralQuestion,
    AgentOutput,
)

load_dotenv()

_model = None


def _get_model():
    global _model
    if _model is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment.")
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel("models/gemini-2.5-flash")
    return _model


def _parse_json_response(text: str) -> dict:
    """Extract and parse JSON from an LLM response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    for pattern in [r"```json\s*(.*?)\s*```", r"```\s*(.*?)\s*```"]:
        m = re.search(pattern, text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except json.JSONDecodeError:
                continue
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except json.JSONDecodeError:
            pass
    raise ValueError(f"Could not parse JSON from response: {text[:300]}")


def _call_agent(prompt: str, agent_name: str, stage: int) -> AgentOutput:
    model = _get_model()
    response = model.generate_content(prompt)
    data = _parse_json_response(response.text)
    return AgentOutput(
        agent_name=agent_name,
        stage=stage,
        data=data,
        timestamp=datetime.now().isoformat(),
    )


# ── Agent 1 ─────────────────────────────────────────────────────
def _agent_parse_resume(resume_context: str) -> AgentOutput:
    prompt = f"""You are Agent 1: Resume Parser.
Extract structured information from this resume text.

Resume Text:
{resume_context}

Return ONLY valid JSON:
{{
  "skills": ["skill1", "skill2"],
  "projects": [
    {{"name": "Name", "description": "Brief desc", "technologies": ["t1"]}}
  ],
  "experience_years": "estimated years",
  "education": "highest degree and field",
  "summary": "one sentence candidate summary"
}}"""
    return _call_agent(prompt, "Resume Parser", 1)


# ── Agent 2 ─────────────────────────────────────────────────────
def _agent_analyze_jd(jd_context: str) -> AgentOutput:
    prompt = f"""You are Agent 2: Job Description Analyzer.
Extract structured requirements from this job description.

Job Description:
{jd_context}

Return ONLY valid JSON:
{{
  "job_title": "extracted or inferred title",
  "required_skills": ["skill1", "skill2"],
  "preferred_skills": ["skill1"],
  "experience_required": "years or level",
  "key_responsibilities": ["resp1", "resp2"]
}}"""
    return _call_agent(prompt, "JD Analyzer", 2)


# ── Agent 3 ─────────────────────────────────────────────────────
def _agent_gap_analysis(resume_data: dict, jd_data: dict) -> AgentOutput:
    prompt = f"""You are Agent 3: Gap Analysis Engine.
Compare the candidate profile against job requirements.

Candidate Profile:
{json.dumps(resume_data, indent=2)}

Job Requirements:
{json.dumps(jd_data, indent=2)}

Return ONLY valid JSON:
{{
  "match_score": <number 0-100>,
  "status": "<Strong Match | Potential | Gap Heavy>",
  "key_advantage": "one sentence",
  "missing_skills": [
    {{"skill": "name", "priority": "High or Medium or Low"}}
  ],
  "matching_skills": ["skill1"]
}}"""
    return _call_agent(prompt, "Gap Analysis Engine", 3)


# ── Agent 4 ─────────────────────────────────────────────────────
def _agent_interview_prep(resume_data: dict, gap_data: dict) -> AgentOutput:
    prompt = f"""You are Agent 4: Interview Preparation Generator.
Create behavioral interview questions tailored to the candidate.

Candidate Profile:
{json.dumps(resume_data, indent=2)}

Gap Analysis:
{json.dumps(gap_data, indent=2)}

Generate exactly 3 questions mapped to the candidate's actual projects.

Return ONLY valid JSON:
{{
  "behavioral_questions": [
    {{
      "question": "question text",
      "project": "project name from resume",
      "focus": "what this evaluates"
    }}
  ]
}}"""
    return _call_agent(prompt, "Interview Prep Generator", 4)


# ── Agent 5 ─────────────────────────────────────────────────────
def _agent_sponsorship_eval(
    jd_text: str, keyword_flag: bool, keyword_phrase: str
) -> AgentOutput:
    detection = (
        f"WARNING — phrase detected: '{keyword_phrase}'"
        if keyword_flag
        else "No exclusion phrases detected."
    )
    prompt = f"""You are Agent 5: Sponsorship Risk Evaluator.
Assess visa sponsorship risk for international candidates.

Job Description:
{jd_text}

Keyword Detection Result: {detection}

Return ONLY valid JSON:
{{
  "sponsorship_warning": "risk assessment or empty string if safe",
  "risk_level": "None | Low | Medium | High",
  "explanation": "brief explanation"
}}"""
    return _call_agent(prompt, "Sponsorship Evaluator", 5)


# ── Orchestrator ────────────────────────────────────────────────
def run_agentic_pipeline(
    resume_context: str,
    jd_context: str,
    sponsorship_flag: bool,
    sponsorship_phrase: str,
) -> AnalysisResult:
    """Execute the full 5-stage agentic pipeline and return an AnalysisResult."""
    trace = []

    # Stage 1 → 2 → 3 → 4 → 5
    a1 = _agent_parse_resume(resume_context)
    trace.append(a1)

    a2 = _agent_analyze_jd(jd_context)
    trace.append(a2)

    a3 = _agent_gap_analysis(a1.data, a2.data)
    trace.append(a3)

    a4 = _agent_interview_prep(a1.data, a3.data)
    trace.append(a4)

    a5 = _agent_sponsorship_eval(jd_context, sponsorship_flag, sponsorship_phrase)
    trace.append(a5)

    return AnalysisResult(
        match_score=a3.data.get("match_score", 0),
        status=a3.data.get("status", "Unknown"),
        key_advantage=a3.data.get("key_advantage", ""),
        missing_skills=[
            MissingSkill(skill=s["skill"], priority=s["priority"])
            for s in a3.data.get("missing_skills", [])
        ],
        behavioral_questions=[
            BehavioralQuestion(
                question=q["question"], project=q["project"], focus=q["focus"]
            )
            for q in a4.data.get("behavioral_questions", [])
        ],
        sponsorship_warning=a5.data.get("sponsorship_warning", ""),
        agent_trace=trace,
    )
