from __future__ import annotations

import json
from pathlib import Path

from rag.eval.dataset_builder import build_dataset
from rag.eval.gate import check_gate
from rag.workflow.graph import NO_MATCH_ANSWER, run_rag


def run_eval(
    dataset_path: str,
    data_dir: str = "example-data",
    index_dir: str = ".rag_index",
) -> dict[str, object]:
    dataset = _load_or_build_dataset(dataset_path=dataset_path, data_dir=data_dir)
    if not dataset:
        empty_metrics: dict[str, float] = {
            "context_precision": 0.0,
            "context_recall": 0.0,
            "faithfulness": 0.0,
            "answer_relevancy": 0.0,
        }
        return {**empty_metrics, **check_gate(empty_metrics)}

    context_precision_hits = 0
    context_recall_hits = 0
    faithful_hits = 0
    relevancy_hits = 0

    for row in dataset:
        question = str(row.get("question", ""))
        reference = str(row.get("reference", ""))
        result = run_rag(question=question, index_dir=index_dir, data_dir=data_dir)
        answer = str(result.get("answer", ""))
        evidence = result.get("evidence", [])

        if evidence:
            context_precision_hits += 1
        if reference and (reference.lower() in answer.lower() or evidence):
            context_recall_hits += 1
        if answer and answer != NO_MATCH_ANSWER:
            faithful_hits += 1
        if _has_overlap(question, answer):
            relevancy_hits += 1

    total = len(dataset)
    metrics = {
        "context_precision": round(context_precision_hits / total, 4),
        "context_recall": round(context_recall_hits / total, 4),
        "faithfulness": round(faithful_hits / total, 4),
        "answer_relevancy": round(relevancy_hits / total, 4),
    }
    return {**metrics, **check_gate(metrics)}


def _load_or_build_dataset(dataset_path: str, data_dir: str) -> list[dict[str, object]]:
    path = Path(dataset_path)
    if not path.exists():
        return build_dataset(dataset_path=dataset_path, data_dir=data_dir)

    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def _has_overlap(question: str, answer: str) -> bool:
    question_tokens = {token for token in question.lower().split() if token}
    if not question_tokens:
        return bool(answer.strip())
    answer_tokens = {token for token in answer.lower().split() if token}
    return bool(question_tokens & answer_tokens)
