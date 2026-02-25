from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from rag.index.build_index import rebuild_index
from rag.retrieval.rerank import rerank_cases
from rag.retrieval.retrieve import retrieve_channels
from rag.workflow.state import RagState

NO_MATCH_ANSWER = "No matching evidence was found for the question."


def run_rag(
    question: str,
    index_dir: str = ".rag_index",
    data_dir: str = "example-data",
    top_k: int = 3,
    label_filter: str | None = None,
) -> dict[str, object]:
    _ensure_index(index_dir=index_dir, data_dir=data_dir)
    state = RagState(question=question)
    channels = retrieve_channels(
        question=question,
        index_dir=index_dir,
        top_k=top_k,
        label_filter=label_filter,
    )
    state.field_hits = channels["field_hits"]
    state.text_hits = channels["text_hits"]
    state.image_hits = channels["image_hits"]
    state.ranked_cases = rerank_cases(
        field_hits=state.field_hits,
        text_hits=state.text_hits,
        image_hits=state.image_hits,
    )
    state.evidence = [
        {"case_id": str(item["case_id"]), "score": round(float(item["score"]), 4)}
        for item in state.ranked_cases[:top_k]
    ]
    state.answer = _compose_answer(state)

    return {
        "question": question,
        "answer": state.answer,
        "evidence": state.evidence,
        "sources": [
            str(Path(index_dir) / "field_docs.jsonl"),
            str(Path(index_dir) / "text_docs.jsonl"),
            str(Path(index_dir) / "image_docs.jsonl"),
        ],
        "confidence": state.evidence[0]["score"] if state.evidence else 0.0,
        "limits": [
            "This is a deterministic baseline workflow without semantic embeddings.",
            "Scores are simple rule-based relevance estimates.",
        ],
        "trace_id": str(uuid4()),
    }


def _ensure_index(index_dir: str, data_dir: str) -> None:
    index_path = Path(index_dir)
    required = [
        index_path / "field_docs.jsonl",
        index_path / "text_docs.jsonl",
        index_path / "image_docs.jsonl",
    ]
    if all(path.exists() for path in required):
        return
    rebuild_index(data_dir=data_dir, index_dir=index_dir)


def _compose_answer(state: RagState) -> str:
    if not state.evidence:
        return NO_MATCH_ANSWER
    case_ids = ", ".join(str(item["case_id"]) for item in state.evidence)
    return f"Top evidence cases: {case_ids}."
