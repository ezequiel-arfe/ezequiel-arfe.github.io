"""ReliefWeb jobs, via the public ReliefWeb API (not HTML scraping).

API docs: https://apidoc.reliefweb.int/ -- endpoint https://api.reliefweb.int/v2/jobs.
This module could not be exercised against the live API from the
environment it was written in (outbound access to reliefweb.int is
blocked by this session's network egress policy). The request/response
shape below reflects the publicly documented ReliefWeb API schema, but
it has NOT been confirmed against a live response, so the first real run
must be checked against the actual field names -- run this file directly
(`python -m scripts.sources.reliefweb`) to print the raw response of the
first item before trusting the parsed output.

We deliberately do not rely on the API's own keyword/theme filtering --
we pull a batch of recent postings and apply this project's own
filtering.match_interest_areas() so there is exactly one place the
interest-area rules live.
"""

from __future__ import annotations

from datetime import datetime, timezone

from scripts.models import JobListing, SourceResult
from scripts.utils.dates import parse_deadline
from scripts.utils.http import build_session

SOURCE_NAME = "ReliefWeb"
API_URL = "https://api.reliefweb.int/v2/jobs"
APP_NAME = "personal-job-digest"

# Only pull postings created recently -- older ones are almost always
# already closed, and this keeps each run's payload small.
FETCH_LIMIT = 200

FIELDS_INCLUDE = [
    "title",
    "body",
    "url_alias",
    "source.name",
    "country.name",
    "city",
    "date.closing",
    "date.created",
    "career_categories.name",
]


def _extract_field(fields: dict, dotted_path: str):
    node = fields
    for part in dotted_path.split("."):
        if isinstance(node, list):
            # ReliefWeb represents "source"/"country" as lists of objects;
            # take the first entry's remaining path.
            if not node:
                return None
            node = node[0]
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def fetch() -> SourceResult:
    session = build_session()
    payload = {
        "appname": APP_NAME,
        "limit": FETCH_LIMIT,
        "sort": ["date.created:desc"],
        "fields": {"include": FIELDS_INCLUDE},
    }
    try:
        response = session.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as exc:  # noqa: BLE001 - report, never crash the run
        return SourceResult(source_name=SOURCE_NAME, error=str(exc))

    jobs: list[JobListing] = []
    today = datetime.now(timezone.utc).date()

    for item in data.get("data", []):
        fields = item.get("fields", {})
        try:
            title = fields.get("title")
            if not title:
                continue

            url = fields.get("url_alias") or item.get("href") or ""
            organisation = _extract_field(fields, "source.name") or "Unknown organisation"
            country = _extract_field(fields, "country.name")
            city = fields.get("city")
            location_raw = ", ".join(p for p in [city, country] if p) or None

            deadline_raw = _extract_field(fields, "date.closing")
            deadline = parse_deadline(deadline_raw)
            if deadline is not None and deadline < today:
                continue  # already closed

            jobs.append(
                JobListing(
                    title=title,
                    organisation=organisation,
                    url=url,
                    source_name=SOURCE_NAME,
                    location_raw=location_raw,
                    country=country,
                    description_raw=fields.get("body"),
                    deadline=deadline,
                    deadline_raw=deadline_raw,
                )
            )
        except Exception:  # noqa: BLE001 - skip one malformed entry, keep going
            continue

    return SourceResult(source_name=SOURCE_NAME, jobs=jobs)


if __name__ == "__main__":
    import json

    result = fetch()
    if result.error:
        print(f"ERROR: {result.error}")
    else:
        print(f"{len(result.jobs)} job(s) fetched")
        for j in result.jobs[:5]:
            print(json.dumps(j.__dict__, default=str, indent=2))
