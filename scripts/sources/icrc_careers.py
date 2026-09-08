"""careers.icrc.org listings.

PLACEHOLDER: this session's network egress is blocked to careers.icrc.org,
so the real page markup has not been inspected yet. Run
`python scripts/inspect_sources.py` from an environment with real
internet access (e.g. a GitHub Actions run) first, then replace the body
of fetch() below with real parsing based on what that prints -- do not
guess selectors without having seen the actual HTML.
"""

from __future__ import annotations

from scripts.models import SourceResult

SOURCE_NAME = "ICRC Careers"


def fetch() -> SourceResult:
    return SourceResult(
        source_name=SOURCE_NAME,
        error="parser not yet implemented -- pending live-site inspection",
    )


if __name__ == "__main__":
    print(fetch())
