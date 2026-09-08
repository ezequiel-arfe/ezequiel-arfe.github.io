"""robots.txt allow-check, run immediately before scraping any source.

If a target's robots.txt disallows our user-agent (or the more general
"*" agent) for a given path, the source module should skip that URL and
report it as skipped rather than proceeding or silently ignoring the rule.
"""

from __future__ import annotations

from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

from .http import USER_AGENT


def is_allowed(url: str, user_agent: str = USER_AGENT, timeout: int = 10) -> bool:
    """Return True if fetching `url` is allowed by that site's robots.txt.

    Fails open (returns True) only if robots.txt itself can't be fetched
    at all (e.g. 404 -- no robots.txt means no restriction); any other
    fetch problem is treated conservatively.
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
    except Exception:
        # Could not retrieve robots.txt for a reason other than "missing" --
        # be conservative and disallow rather than assume it's fine.
        return False
    return parser.can_fetch(user_agent, url)
