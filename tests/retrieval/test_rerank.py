from rag.retrieval.rerank import rerank_cases


def test_rerank_cases_aggregates_three_channels():
    merged = rerank_cases(
        field_hits=[{"case_id": "A", "score": 0.9}],
        text_hits=[{"case_id": "A", "score": 0.5}],
        image_hits=[{"case_id": "B", "score": 0.8}],
    )
    assert merged[0]["case_id"] == "A"
