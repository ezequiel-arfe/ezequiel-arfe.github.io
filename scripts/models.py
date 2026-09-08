"""Shared data structures for the job-digest pipeline.

Every field a source doesn't explicitly provide is left as None end-to-end.
report.py is the single place that turns None into a user-facing "not
specified" string -- no other module invents a value.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime


@dataclass
class JobListing:
    title: str
    organisation: str
    url: str
    source_name: str

    location_raw: str | None = None
    country: str | None = None

    # Used only for interest-area/contract-type keyword matching; not
    # necessarily rendered in the report.
    description_raw: str | None = None

    deadline: date | None = None
    deadline_raw: str | None = None

    contract_type_label: str = "Not specified"
    contract_type_stated: bool = False

    matched_areas: list[str] = field(default_factory=list)


@dataclass
class SourceResult:
    source_name: str
    jobs: list[JobListing] = field(default_factory=list)
    error: str | None = None
    fetched_at: datetime = field(default_factory=datetime.utcnow)
