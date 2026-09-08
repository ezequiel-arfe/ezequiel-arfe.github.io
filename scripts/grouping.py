"""Groups filtered jobs by region -> organisation -> contract type, sorted
by deadline (soonest first, unknown deadlines last) within each group.
"""

from __future__ import annotations

from datetime import date

from scripts.config import (
    COUNTRY_TO_REGION,
    GLOBAL_REGION,
    PSYCH_MHPSS_AREA,
    REGION_ORDER,
    UNKNOWN_REGION,
)
from scripts.models import JobListing

Grouped = dict[str, dict[str, dict[str, list[JobListing]]]]


def region_for(job: JobListing) -> str:
    if job.country and job.country in COUNTRY_TO_REGION:
        return COUNTRY_TO_REGION[job.country]

    is_global_role = PSYCH_MHPSS_AREA in job.matched_areas
    if job.country:
        # A country we don't have a region mapping for yet (only reachable
        # for global-eligible psych/MHPSS roles, since other areas are
        # already restricted to CH/EU/UK by filtering.location_allowed).
        return job.country
    return GLOBAL_REGION if is_global_role else UNKNOWN_REGION


def _region_sort_key(region: str) -> tuple[int, str]:
    if region in REGION_ORDER:
        return (REGION_ORDER.index(region), region)
    return (len(REGION_ORDER), region)


def _deadline_sort_key(job: JobListing) -> tuple[int, date]:
    if job.deadline is None:
        return (1, date.max)
    return (0, job.deadline)


def group_and_sort(jobs: list[JobListing]) -> Grouped:
    by_region: dict[str, dict[str, dict[str, list[JobListing]]]] = {}
    for job in jobs:
        region = region_for(job)
        by_region.setdefault(region, {}).setdefault(
            job.organisation, {}
        ).setdefault(job.contract_type_label, []).append(job)

    ordered: Grouped = {}
    for region in sorted(by_region, key=_region_sort_key):
        ordered[region] = {}
        for org in sorted(by_region[region]):
            ordered[region][org] = {}
            for contract_label in sorted(by_region[region][org]):
                ordered[region][org][contract_label] = sorted(
                    by_region[region][org][contract_label],
                    key=_deadline_sort_key,
                )
    return ordered


def dedupe_by_url(jobs: list[JobListing]) -> list[JobListing]:
    """A job matching more than one interest area within the same section
    should be listed once, not once per matched area."""
    seen: dict[str, JobListing] = {}
    for job in jobs:
        seen.setdefault(job.url, job)
    return list(seen.values())
