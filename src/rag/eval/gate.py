from __future__ import annotations

from typing import Mapping

THRESHOLDS: dict[str, float] = {
    "context_precision": 0.70,
    "context_recall": 0.70,
    "faithfulness": 0.80,
    "answer_relevancy": 0.75,
}


def check_gate(metrics: Mapping[str, float]) -> dict[str, object]:
    failed_metrics: dict[str, dict[str, float]] = {}
    for name, threshold in THRESHOLDS.items():
        value = float(metrics.get(name, 0.0))
        if value < threshold:
            failed_metrics[name] = {
                "value": round(value, 4),
                "threshold": threshold,
            }

    return {
        "pass_gate": len(failed_metrics) == 0,
        "thresholds": THRESHOLDS.copy(),
        "failed_metrics": failed_metrics,
    }
