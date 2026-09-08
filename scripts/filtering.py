"""Interest-area matching, location filtering, and contract-type inference.

Nothing here fabricates data: matching only ever narrows or labels what a
source already provided.
"""

from __future__ import annotations

from scripts.config import (
    ALLOWED_NON_GLOBAL_COUNTRIES,
    CONTRACT_KEYWORD_BUCKETS,
    INTEREST_AREAS,
    NOT_SPECIFIED,
    PSYCH_MHPSS_AREA,
)


def match_interest_areas(title: str, description: str = "") -> list[str]:
    """Return the list of interest-area keys whose keywords appear in the
    given title/description (case-insensitive substring match)."""
    text = f"{title} {description}".lower()
    matched = []
    for area, keywords in INTEREST_AREAS.items():
        if any(keyword in text for keyword in keywords):
            matched.append(area)
    return matched


def location_allowed(matched_areas: list[str], country: str | None) -> bool:
    """Psychology/MHPSS roles are open to any location. Every other
    interest area requires a Switzerland/EU/UK location."""
    if PSYCH_MHPSS_AREA in matched_areas:
        return True
    return country in ALLOWED_NON_GLOBAL_COUNTRIES


def infer_contract_type(
    raw_text: str | None, structured_field: str | None = None
) -> tuple[str, bool]:
    """Return (label, is_stated). Prefers a source's own structured field;
    otherwise buckets the raw text by keyword. Returns (NOT_SPECIFIED,
    False) when neither yields anything -- never guesses a specific type."""
    if structured_field and structured_field.strip():
        return structured_field.strip(), True

    text = (raw_text or "").lower()
    for label, keywords in CONTRACT_KEYWORD_BUCKETS:
        if any(keyword in text for keyword in keywords):
            return label, False

    return NOT_SPECIFIED, False
