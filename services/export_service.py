"""Export service — Markdown and JSON report generation."""

from models.analysis_models import AnalysisResult


def export_markdown(result: AnalysisResult) -> str:
    """Generate a downloadable Markdown report."""
    return result.to_markdown()


def export_json(result: AnalysisResult) -> str:
    """Generate a downloadable JSON report."""
    return result.to_json(indent=2)
