from scripts.filtering import (
    infer_contract_type,
    location_allowed,
    match_interest_areas,
)


def test_match_interest_areas_public_health():
    areas = match_interest_areas("Public Health Officer", "epidemiology background")
    assert "public_health" in areas


def test_match_interest_areas_psychology_variants():
    assert "psychology_mhpss" in match_interest_areas("MHPSS Officer")
    assert "psychology_mhpss" in match_interest_areas("Psychologist")
    assert "psychology_mhpss" in match_interest_areas(
        "Mental Health and Psychosocial Support Advisor"
    )


def test_match_interest_areas_no_match():
    assert match_interest_areas("Truck Driver", "delivers supplies") == []


def test_match_interest_areas_multiple():
    areas = match_interest_areas("Project Manager - Business Process Improvement")
    assert "project_management" in areas
    assert "business_process" in areas


def test_location_allowed_psychology_is_global():
    assert location_allowed(["psychology_mhpss"], "Kenya") is True
    assert location_allowed(["psychology_mhpss"], None) is True


def test_location_allowed_other_areas_require_ch_eu_uk():
    assert location_allowed(["public_health"], "Switzerland") is True
    assert location_allowed(["public_health"], "France") is True
    assert location_allowed(["public_health"], "United Kingdom") is True
    assert location_allowed(["public_health"], "Kenya") is False
    assert location_allowed(["public_health"], None) is False


def test_infer_contract_type_prefers_stated_field():
    label, stated = infer_contract_type("some text", structured_field="Fixed-term, 6 months")
    assert label == "Fixed-term, 6 months"
    assert stated is True


def test_infer_contract_type_infers_consultancy():
    label, stated = infer_contract_type("Individual consultant needed for a short assignment")
    assert label == "Consultancy"
    assert stated is False


def test_infer_contract_type_infers_internship_over_temporary():
    # "internship" should win even though the text also contains "temporary"
    label, stated = infer_contract_type("Temporary internship position for students")
    assert label == "Internship"
    assert stated is False


def test_infer_contract_type_not_specified():
    label, stated = infer_contract_type("Join our amazing team")
    assert label == "Not specified"
    assert stated is False
