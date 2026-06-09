"""Sponsorship risk detection service.

Uses keyword matching to flag job descriptions that contain
common visa-sponsorship exclusion phrases.
"""

NO_SPONSORSHIP_TERMS = [
    "not provide sponsorship",
    "no sponsorship",
    "citizens only",
    "authorized to work in the US without",
    "will not employ those",
    "temporary visas",
    "not eligible for hire",
]


def check_sponsorship(jd_text: str) -> tuple:
    """Check job description for sponsorship restriction language.

    Returns:
        (has_warning: bool, matched_phrase: str)
    """
    jd_lower = jd_text.lower()
    for term in NO_SPONSORSHIP_TERMS:
        if term.lower() in jd_lower:
            return True, term
    return False, ""
