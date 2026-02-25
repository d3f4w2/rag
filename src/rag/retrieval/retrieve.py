from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def retrieve_channels(
    question: str,
    index_dir: str = ".rag_index",
    top_k: int = 5,
    label_filter: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    query = question.lower().strip()
    field_docs = _load_jsonl(Path(index_dir) / "field_docs.jsonl")
    text_docs = _load_jsonl(Path(index_dir) / "text_docs.jsonl")
    image_docs = _load_jsonl(Path(index_dir) / "image_docs.jsonl")

    return {
        "field_hits": _score_channel(field_docs, query, top_k, label_filter),
        "text_hits": _score_channel(text_docs, query, top_k, label_filter),
        "image_hits": _score_channel(image_docs, query, top_k, label_filter),
    }


def _score_channel(
    docs: list[dict[str, Any]],
    query: str,
    top_k: int,
    label_filter: str | None,
) -> list[dict[str, float]]:
    scored: list[dict[str, float]] = []
    for doc in docs:
        case_id = str(doc.get("case_id", ""))
        if not case_id:
            continue
        if label_filter and not case_id.startswith(f"{label_filter}/"):
            continue
        text = " ".join(str(v) for v in doc.values()).lower()
        if query:
            if query not in text:
                continue
            score = 1.0
        else:
            score = 0.5
        scored.append({"case_id": case_id, "score": score})

    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows
