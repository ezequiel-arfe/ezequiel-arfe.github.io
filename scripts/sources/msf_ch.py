"""MSF Switzerland vacancies page
(msf.ch/travailler-avec-nous/profils-recherches).

PLACEHOLDER: this session's network egress is blocked to msf.ch, so the
real page markup has not been inspected yet. Run
`python scripts/inspect_sources.py` from an environment with real
internet access (e.g. a GitHub Actions run) first, then replace the body
of fetch() below with real parsing based on what that prints. The `#all`
URL fragment suggests a client-side filter tab -- check whether the
initial HTML already contains the full listing or whether it's loaded
via a separate XHR/JSON endpoint (inspect the Network tab in a browser
if the raw HTML from inspect_sources.py looks like an empty shell).
"""

from __future__ import annotations

from scripts.models import SourceResult

SOURCE_NAME = "MSF Switzerland"


def fetch() -> SourceResult:
    return SourceResult(
        source_name=SOURCE_NAME,
        error="parser not yet implemented -- pending live-site inspection",
    )


if __name__ == "__main__":
    print(fetch())
