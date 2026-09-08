"""NATO's Oracle Taleo career section
(nato.taleo.net/careersection/2/jobsearch.ftl?lang=en).

PLACEHOLDER: this session's network egress is blocked to nato.taleo.net,
so the real page markup has not been inspected yet. Run
`python scripts/inspect_sources.py` from an environment with real
internet access (e.g. a GitHub Actions run) first, then replace the body
of fetch() below with real parsing based on what that prints. Oracle
Taleo career sections are sometimes configured by the site owner to
block crawlers entirely -- confirm robots.txt allows this before
building the parser, and expect to need request delay/backoff since
Taleo instances can rate-limit aggressively.
"""

from __future__ import annotations

from scripts.models import SourceResult

SOURCE_NAME = "NATO (Taleo)"


def fetch() -> SourceResult:
    return SourceResult(
        source_name=SOURCE_NAME,
        error="parser not yet implemented -- pending live-site inspection",
    )


if __name__ == "__main__":
    print(fetch())
