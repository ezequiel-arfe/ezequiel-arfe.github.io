"""ICRC's Salesforce fRecruit job portal
(fs-2662.my.salesforce-sites.com/recruit/fRecruit__ApplyJobList).

PLACEHOLDER: this session's network egress is blocked to this domain, so
the real page markup has not been inspected yet. Run
`python scripts/inspect_sources.py` from an environment with real
internet access (e.g. a GitHub Actions run) first, then replace the body
of fetch() below with real parsing based on what that prints. Note:
older Salesforce Visualforce ("fRecruit") sites often paginate via
ViewState postbacks requiring a requests.Session with cookie/hidden-field
handling rather than simple GET+parse -- confirm this from the real
response before assuming a simple approach works. Also confirm this
domain's robots.txt allows fetching -- Force.com sites often ship a
blanket deny.
"""

from __future__ import annotations

from scripts.models import SourceResult

SOURCE_NAME = "ICRC (Salesforce fRecruit portal)"


def fetch() -> SourceResult:
    return SourceResult(
        source_name=SOURCE_NAME,
        error="parser not yet implemented -- pending live-site inspection",
    )


if __name__ == "__main__":
    print(fetch())
