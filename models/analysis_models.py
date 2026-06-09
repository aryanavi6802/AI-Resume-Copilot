"""Data models for AI Resume Copilot analysis results."""

from dataclasses import dataclass, field
import json
from datetime import datetime
from typing import List


@dataclass
class MissingSkill:
    """A skill gap identified during analysis."""
    skill: str
    priority: str  # "High", "Medium", "Low"


@dataclass
class BehavioralQuestion:
    """A behavioral interview question with project mapping."""
    question: str
    project: str
    focus: str


@dataclass
class AgentOutput:
    """Structured output from an individual agent stage."""
    agent_name: str
    stage: int
    data: dict
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class AnalysisResult:
    """Complete analysis result from the agentic pipeline."""
    match_score: int
    status: str
    key_advantage: str
    missing_skills: List[MissingSkill]
    behavioral_questions: List[BehavioralQuestion]
    sponsorship_warning: str
    agent_trace: List[AgentOutput] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "match_score": self.match_score,
            "status": self.status,
            "key_advantage": self.key_advantage,
            "missing_skills": [
                {"skill": s.skill, "priority": s.priority}
                for s in self.missing_skills
            ],
            "behavioral_questions": [
                {"question": q.question, "project": q.project, "focus": q.focus}
                for q in self.behavioral_questions
            ],
            "sponsorship_warning": self.sponsorship_warning,
        }

    def to_json(self, indent=2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_markdown(self) -> str:
        lines = []
        lines.append("# AI Career Copilot — Analysis Report\n")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append("## Match Overview\n")
        lines.append(f"- **Match Score**: {self.match_score}%")
        lines.append(f"- **Status**: {self.status}")
        lines.append(f"- **Key Advantage**: {self.key_advantage}\n")
        if self.sponsorship_warning:
            lines.append(f"> ⚠️ **Sponsorship Warning**: {self.sponsorship_warning}\n")
        lines.append("## Technical Gap Analysis\n")
        lines.append("| Skill | Priority |")
        lines.append("| :--- | :--- |")
        for s in self.missing_skills:
            lines.append(f"| {s.skill} | {s.priority} |")
        lines.append("")
        lines.append("## Behavioral Interview Preparation\n")
        for i, q in enumerate(self.behavioral_questions, 1):
            lines.append(f"### Question {i}\n")
            lines.append(f"**{q.question}**\n")
            lines.append(f"- **Suggested Project**: {q.project}")
            lines.append(f"- **Focus**: {q.focus}\n")
        return "\n".join(lines)

    @classmethod
    def from_dict(cls, data: dict) -> "AnalysisResult":
        return cls(
            match_score=data.get("match_score", 0),
            status=data.get("status", "Unknown"),
            key_advantage=data.get("key_advantage", ""),
            missing_skills=[
                MissingSkill(**s) for s in data.get("missing_skills", [])
            ],
            behavioral_questions=[
                BehavioralQuestion(**q)
                for q in data.get("behavioral_questions", [])
            ],
            sponsorship_warning=data.get("sponsorship_warning", ""),
        )
