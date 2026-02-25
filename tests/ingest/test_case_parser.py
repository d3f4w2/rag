from rag.ingest.case_parser import parse_cases


def test_parse_cases_reads_all_examples():
    cases = parse_cases("example-data")
    assert len(cases) == 4
    assert all(c.label in {"HSIL", "LSIL"} for c in cases)
    assert all(len(c.image_paths) == 5 for c in cases)
