from datetime import date

from scripts.grouping import dedupe_by_url, group_and_sort, region_for
from scripts.models import JobListing


def make_job(**overrides) -> JobListing:
    defaults = dict(
        title="Some Role",
        organisation="Some Org",
        url="https://example.org/job/1",
        source_name="test",
        country="Switzerland",
        contract_type_label="Fixed-term",
        matched_areas=["public_health"],
    )
    defaults.update(overrides)
    return JobListing(**defaults)


def test_region_for_maps_known_countries():
    assert region_for(make_job(country="Switzerland")) == "Switzerland"
    assert region_for(make_job(country="France")) == "European Union"
    assert region_for(make_job(country="United Kingdom")) == "United Kingdom"


def test_region_for_global_role_unknown_country():
    job = make_job(country=None, matched_areas=["psychology_mhpss"])
    assert region_for(job) == "Global / Remote"


def test_region_for_global_role_unmapped_country_uses_country_name():
    job = make_job(country="Kenya", matched_areas=["psychology_mhpss"])
    assert region_for(job) == "Kenya"


def test_region_for_non_global_role_unknown_country():
    job = make_job(country=None, matched_areas=["public_health"])
    assert region_for(job) == "Region not specified"


def test_group_and_sort_orders_by_deadline_soonest_first():
    early = make_job(url="a", deadline=date(2026, 1, 1))
    late = make_job(url="b", deadline=date(2026, 6, 1))
    unknown = make_job(url="c", deadline=None)

    grouped = group_and_sort([late, unknown, early])
    jobs = grouped["Switzerland"]["Some Org"]["Fixed-term"]
    assert [j.url for j in jobs] == ["a", "b", "c"]


def test_group_and_sort_region_order():
    ch = make_job(url="a", country="Switzerland")
    eu = make_job(url="b", country="Germany")
    uk = make_job(url="c", country="United Kingdom")

    grouped = group_and_sort([uk, eu, ch])
    assert list(grouped.keys()) == ["Switzerland", "European Union", "United Kingdom"]


def test_dedupe_by_url_keeps_first_occurrence():
    job1 = make_job(url="dup", title="First")
    job2 = make_job(url="dup", title="Second")
    result = dedupe_by_url([job1, job2])
    assert len(result) == 1
    assert result[0].title == "First"
