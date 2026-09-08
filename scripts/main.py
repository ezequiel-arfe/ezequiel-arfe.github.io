"""Orchestrator for the weekly job digest.

Usage:
    python -m scripts.main             # fetch, filter, group, and email
    python -m scripts.main --dry-run   # same, but print the report and
                                        # skip sending email entirely
"""

from __future__ import annotations

import argparse
import logging
import sys
from datetime import datetime, timezone

from scripts.config import MAIN_SECTION_AREAS, PSYCH_MHPSS_AREA
from scripts.filtering import (
    infer_contract_type,
    location_allowed,
    match_interest_areas,
)
from scripts.grouping import dedupe_by_url, group_and_sort
from scripts.models import JobListing, SourceResult
from scripts.report import build_email
from scripts.sources import SOURCE_REGISTRY

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
log = logging.getLogger("job_digest")


def fetch_all_sources() -> list[SourceResult]:
    results: list[JobListing]
    results = []
    for fetch_fn in SOURCE_REGISTRY:
        source_name = getattr(fetch_fn, "__module__", str(fetch_fn))
        try:
            result = fetch_fn()
        except Exception as exc:  # noqa: BLE001 - one source must never kill the run
            log.exception("Source %s raised unexpectedly", source_name)
            result = SourceResult(source_name=source_name, error=str(exc))
        if result.error:
            log.warning("Source %s failed: %s", result.source_name, result.error)
        else:
            log.info("Source %s: %d job(s) fetched", result.source_name, len(result.jobs))
        results.append(result)
    return results


def annotate_job(job: JobListing) -> None:
    """Fills in matched_areas and contract_type_label/stated in place.
    A source may already have set an explicit, stated contract type
    (contract_type_stated=True) -- that is never overwritten."""
    job.matched_areas = match_interest_areas(job.title, job.description_raw or "")
    if not job.contract_type_stated:
        label, stated = infer_contract_type(f"{job.title} {job.description_raw or ''}")
        job.contract_type_label = label
        job.contract_type_stated = stated


def filter_and_split(
    source_results: list[SourceResult],
) -> tuple[list[JobListing], list[JobListing]]:
    """Returns (psych_mhpss_jobs, main_section_jobs)."""
    today = datetime.now(timezone.utc).date()
    psych_jobs: list[JobListing] = []
    main_jobs: list[JobListing] = []

    for result in source_results:
        for job in result.jobs:
            annotate_job(job)

            if job.deadline is not None and job.deadline < today:
                continue  # already closed

            if not location_allowed(job.matched_areas, job.country):
                continue

            if PSYCH_MHPSS_AREA in job.matched_areas:
                psych_jobs.append(job)
            elif any(area in job.matched_areas for area in MAIN_SECTION_AREAS):
                main_jobs.append(job)

    return dedupe_by_url(psych_jobs), dedupe_by_url(main_jobs)


def run(dry_run: bool) -> int:
    source_results = fetch_all_sources()
    psych_jobs, main_jobs = filter_and_split(source_results)

    psych_grouped = group_and_sort(psych_jobs)
    main_grouped = group_and_sort(main_jobs)

    subject, html_body, text_body = build_email(psych_grouped, main_grouped, source_results)

    if dry_run:
        print(text_body)
        return 0

    from scripts.emailer import send_email  # imported lazily: only needed for a real send

    send_email(subject, html_body, text_body)
    log.info("Email sent.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Weekly job digest pipeline")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the composed report instead of sending an email.",
    )
    args = parser.parse_args()
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
