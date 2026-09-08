"""IATA's Cornerstone OnDemand (CSOD) career site
(iata.csod.com/ux/ats/careersite/1/home?c=iata).

PLACEHOLDER: this session's network egress is blocked to iata.csod.com,
so the real page has not been inspected yet, and this is the one source
already expected to need Playwright (modern CSOD career sites are
JS-rendered SPAs that fetch listings via a JWT-authenticated backend
API issued client-side). Two implementation options once real access is
available:
  (a) Full Playwright render + DOM scraping of the rendered job list
      (more robust, slower, needs `playwright install chromium`).
  (b) Load the page once with Playwright, extract the bearer token and
      regional API host from the page's JS/network requests, then call
      the JSON API directly with `requests` (faster, more fragile to
      CSOD frontend changes).
Start with (a) for robustness; only move to (b) if run time becomes a
problem. Do not write either without having seen the real page/network
traffic first.
"""

from __future__ import annotations

from scripts.models import SourceResult

SOURCE_NAME = "IATA (Cornerstone OnDemand)"


def fetch() -> SourceResult:
    return SourceResult(
        source_name=SOURCE_NAME,
        error="parser not yet implemented -- pending live-site inspection",
    )


if __name__ == "__main__":
    print(fetch())
