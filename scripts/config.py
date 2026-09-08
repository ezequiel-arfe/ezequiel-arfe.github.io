"""Static configuration: keyword lists and location/region tables.

Extend these lists as needed -- they are the only place matching rules
live, so widening the search (a new keyword, a new source, a new region)
never requires touching the pipeline logic itself.
"""

from __future__ import annotations

# --- Interest areas -----------------------------------------------------
# The "psychology_mhpss" key is special-cased throughout the pipeline: it
# is the only area exempt from the Switzerland/EU/UK location filter, and
# it is rendered as its own section in the report, separate from the rest.

INTEREST_AREAS: dict[str, list[str]] = {
    "psychology_mhpss": [
        "psycholog",  # matches psychologist / psychology / psychological
        "mhpss",
        "mental health",
        "psychosocial",
        "counsellor",
        "counselor",
        "counselling",
        "counseling",
    ],
    "public_health": [
        "public health",
        "epidemiolog",
        "health system",
        "community health",
        "health promotion",
        "global health",
    ],
    "information_management": [
        "information management",
        "information manager",
        "im officer",
        "data management",
        "knowledge management",
    ],
    "monitoring_evaluation": [
        "monitoring and evaluation",
        "monitoring & evaluation",
        "m&e officer",
        "m&e specialist",
        "mel officer",
        "results based management",
        "results-based management",
    ],
    "business_process": [
        "business process",
        "process improvement",
        "process re-engineering",
        "process reengineering",
        "business analyst",
    ],
    "project_management": [
        "project manager",
        "project management",
        "project coordinator",
        "programme manager",
        "program manager",
        "programme officer",
    ],
}

# The five areas that make up the report's "main section" (equal priority,
# no ranking among them). psychology_mhpss is deliberately excluded here --
# it gets its own section.
MAIN_SECTION_AREAS: list[str] = [
    key for key in INTEREST_AREAS if key != "psychology_mhpss"
]
PSYCH_MHPSS_AREA = "psychology_mhpss"

# --- Locations ------------------------------------------------------------

EU_COUNTRIES: set[str] = {
    "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", "Czechia",
    "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany",
    "Greece", "Hungary", "Ireland", "Italy", "Latvia", "Lithuania",
    "Luxembourg", "Malta", "Netherlands", "Poland", "Portugal", "Romania",
    "Slovakia", "Slovenia", "Spain", "Sweden",
}

SWITZERLAND = "Switzerland"
UNITED_KINGDOM = "United Kingdom"

# Countries allowed for every interest area except psychology_mhpss.
ALLOWED_NON_GLOBAL_COUNTRIES: set[str] = EU_COUNTRIES | {
    SWITZERLAND,
    UNITED_KINGDOM,
}

# Maps a country name to the region bucket used for report grouping.
# Anything not listed here falls back to its raw country/location string
# (see grouping.py) rather than being silently dropped.
_COUNTRY_TO_REGION_OVERRIDES: dict[str, str] = {
    SWITZERLAND: "Switzerland",
    UNITED_KINGDOM: "United Kingdom",
}
for _c in EU_COUNTRIES:
    _COUNTRY_TO_REGION_OVERRIDES[_c] = "European Union"

COUNTRY_TO_REGION: dict[str, str] = _COUNTRY_TO_REGION_OVERRIDES

# Preferred display order for regions; anything else sorts alphabetically
# after these.
REGION_ORDER: list[str] = [
    "Switzerland",
    "European Union",
    "United Kingdom",
    "Global / Remote",
]

UNKNOWN_REGION = "Region not specified"
GLOBAL_REGION = "Global / Remote"

# --- Contract type inference -----------------------------------------------
# Checked in this order; the first bucket whose keyword appears in the raw
# text wins. Order matters: e.g. "internship" must be checked before
# "temporary" since internship postings often also use that word.

CONTRACT_KEYWORD_BUCKETS: list[tuple[str, list[str]]] = [
    ("Internship", ["internship", "intern position", "traineeship", "trainee"]),
    ("Consultancy", ["consultant", "consultancy", "individual contractor"]),
    ("Fixed-term", [
        "fixed-term", "fixed term", "temporary", "short-term", "short term",
        "limited duration",
    ]),
    ("Permanent", ["permanent", "open-ended", "open ended", "indefinite"]),
]

NOT_SPECIFIED = "Not specified"
