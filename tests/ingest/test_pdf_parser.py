from rag.ingest.case_parser import parse_cases
from rag.ingest.pdf_parser import extract_report_fields


def test_extract_report_fields_returns_expected_keys():
    sample_case = parse_cases("example-data")[0]
    out = extract_report_fields(sample_case.pdf_path)
    expected = {"age", "tct", "hpv", "impression", "plan", "followup_date", "raw_text"}
    assert set(out.keys()) == expected
    assert isinstance(out["raw_text"], str)
    assert any(out[k] for k in expected - {"raw_text"})


def test_extract_report_fields_fallback_for_missing_file():
    out = extract_report_fields("example-data/missing.pdf")
    expected = {"age", "tct", "hpv", "impression", "plan", "followup_date", "raw_text"}
    assert set(out.keys()) == expected
    assert out["raw_text"] == ""
    for key in expected - {"raw_text"}:
        assert out[key] is None
