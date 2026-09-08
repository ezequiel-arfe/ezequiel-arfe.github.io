"""Registry of job source fetchers.

Each entry's `fetch()` takes no arguments and returns a
scripts.models.SourceResult. A fetch() must never raise for an
individual-job parsing problem -- skip that job and keep going -- but
main.py wraps the whole call anyway so a totally broken source still
degrades to a SourceResult with `error` set rather than crashing the run.
"""

from __future__ import annotations

from typing import Callable

from scripts.models import SourceResult

from . import (
    icrc_careers,
    icrc_salesforce,
    iata_csod,
    msf_ch,
    nato_taleo,
    reliefweb,
    unjobs,
)

SOURCE_REGISTRY: list[Callable[[], SourceResult]] = [
    reliefweb.fetch,
    unjobs.fetch,
    icrc_careers.fetch,
    icrc_salesforce.fetch,
    nato_taleo.fetch,
    msf_ch.fetch,
    iata_csod.fetch,
]
