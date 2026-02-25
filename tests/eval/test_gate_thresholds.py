from rag.eval.gate import check_gate


def test_gate_fails_when_any_metric_below_threshold():
    metrics = {
        "context_precision": 0.8,
        "context_recall": 0.7,
        "faithfulness": 0.79,
        "answer_relevancy": 0.9,
    }
    out = check_gate(metrics)
    assert out["pass_gate"] is False


def test_gate_passes_when_all_metrics_meet_thresholds():
    metrics = {
        "context_precision": 0.7,
        "context_recall": 0.72,
        "faithfulness": 0.8,
        "answer_relevancy": 0.75,
    }
    out = check_gate(metrics)

    assert out["pass_gate"] is True
    assert out["failed_metrics"] == {}
