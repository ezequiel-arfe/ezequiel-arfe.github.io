from scripts.filtering import infer_contract_type


def test_infers_permanent():
    label, stated = infer_contract_type("This is a permanent position based in Geneva")
    assert label == "Permanent"
    assert stated is False


def test_infers_fixed_term_from_temporary_keyword():
    label, stated = infer_contract_type("A temporary assignment of 12 months")
    assert label == "Fixed-term"
    assert stated is False


def test_case_insensitive_matching():
    label, _ = infer_contract_type("OPEN-ENDED CONTRACT")
    assert label == "Permanent"


def test_empty_text_not_specified():
    label, stated = infer_contract_type("")
    assert label == "Not specified"
    assert stated is False


def test_none_text_not_specified():
    label, stated = infer_contract_type(None)
    assert label == "Not specified"
    assert stated is False
