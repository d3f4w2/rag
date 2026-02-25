from rag.ingest.case_parser import parse_cases
from rag.ingest.pdf_parser import extract_report_fields


def test_extract_report_fields_returns_expected_keys():
    sample_case = parse_cases("example-data")[0]
    out = extract_report_fields(sample_case.pdf_path)
    for key in ["age", "tct", "hpv", "impression", "plan", "followup_date", "raw_text"]:
        assert key in out
