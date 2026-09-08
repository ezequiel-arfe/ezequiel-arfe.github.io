"""Shared HTTP session for source modules: retries, backoff, and a
descriptive User-Agent so we behave as a good citizen against sites we
scrape at most once a week.
"""

from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

USER_AGENT = (
    "job-digest-bot/1.0 (+personal weekly job-search digest; "
    "contact: mysonntags@gmail.com)"
)

DEFAULT_TIMEOUT = 20


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get(session: requests.Session, url: str, **kwargs) -> requests.Response:
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    response = session.get(url, **kwargs)
    response.raise_for_status()
    return response
