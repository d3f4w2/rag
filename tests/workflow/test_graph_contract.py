from rag.workflow.graph import run_rag


def test_run_rag_returns_contract_keys():
    out = run_rag("HPV16相关病例有哪些证据？")
    for key in [
        "question",
        "answer",
        "evidence",
        "sources",
        "confidence",
        "limits",
        "trace_id",
    ]:
        assert key in out


def test_run_rag_returns_no_match_payload_when_query_has_no_evidence(tmp_path):
    out = run_rag(
        question="definitely-not-in-the-documents",
        index_dir=str(tmp_path / "rag-index"),
    )

    assert out["evidence"] == []
    assert out["confidence"] == 0.0
    assert out["answer"] == "No matching evidence was found for the question."
