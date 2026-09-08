"""Diagnostic tool: fetches robots.txt + a raw HTML/JSON sample from each
source's URL and prints them, truncated, to stdout.

Used during initial development (from an environment with real internet
access, e.g. a GitHub Actions run) to inspect each site's actual markup
before writing/updating that source's parser in scripts/sources/. Also
useful later if a source silently starts returning 0 jobs -- rerun this
to see whether the page structure changed.

Not part of the weekly pipeline itself.
"""

from __future__ import annotations

from scripts.utils.http import build_session
from scripts.utils.robots import is_allowed

TARGETS = {
    "unjobs": "https://unjobs.org/",
    "icrc_careers": "https://careers.icrc.org/",
    "icrc_salesforce": (
        "https://fs-2662.my.salesforce-sites.com/recruit/"
        "fRecruit__ApplyJobList?portal=Global"
    ),
    "iata_csod": "https://iata.csod.com/ux/ats/careersite/1/home?c=iata",
    "nato_taleo": "https://nato.taleo.net/careersection/2/jobsearch.ftl?lang=en",
    "msf_ch": "https://www.msf.ch/travailler-avec-nous/profils-recherches",
}

TRUNCATE_CHARS = 6000


def main() -> None:
    session = build_session()
    for name, url in TARGETS.items():
        print(f"\n{'=' * 80}\n{name} -> {url}\n{'=' * 80}")

        allowed = is_allowed(url)
        print(f"robots.txt allows fetch: {allowed}")
        if not allowed:
            print("SKIPPING body fetch -- disallowed by robots.txt")
            continue

        try:
            response = session.get(url, timeout=20)
            print(f"status: {response.status_code}")
            print(f"final url: {response.url}")
            print(f"content-type: {response.headers.get('content-type')}")
            print(f"body length: {len(response.text)} chars")
            print("--- first bytes ---")
            print(response.text[:TRUNCATE_CHARS])
        except Exception as exc:  # noqa: BLE001
            print(f"FETCH FAILED: {exc}")


if __name__ == "__main__":
    main()
