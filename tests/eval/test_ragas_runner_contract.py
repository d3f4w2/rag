from rag.eval.ragas_runner import run_eval


def test_run_eval_returns_metric_keys():
    out = run_eval(dataset_path="eval/dataset.jsonl")
    for key in [
        "context_precision",
        "context_recall",
        "faithfulness",
        "answer_relevancy",
        "pass_gate",
    ]:
        assert key in out
