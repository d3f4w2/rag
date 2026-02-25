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
