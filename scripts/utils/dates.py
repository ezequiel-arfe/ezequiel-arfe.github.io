"""Deadline parsing helpers.

Never guess a date from context -- if a source's date string can't be
parsed confidently, return None and keep the raw text so report.py can
show it as-is rather than silently dropping it.
"""

from __future__ import annotations

from datetime import date

from dateutil import parser as dateutil_parser


def parse_deadline(raw: str | None) -> date | None:
    if not raw or not raw.strip():
        return None
    try:
        return dateutil_parser.parse(raw, fuzzy=True).date()
    except (ValueError, OverflowError):
        return None
