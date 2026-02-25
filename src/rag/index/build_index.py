from __future__ import annotations

import json
from pathlib import Path

from rag.index.field_index import build_field_documents
from rag.index.vector_index import build_image_documents, build_text_documents
from rag.ingest.case_parser import parse_cases


def rebuild_index(data_dir: str, index_dir: str) -> dict[str, int]:
    cases = parse_cases(data_dir)
    field_docs = build_field_documents(cases)
    text_docs = build_text_documents(cases)
    image_docs = build_image_documents(cases)

    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)
    _write_jsonl(index_path / "field_docs.jsonl", field_docs)
    _write_jsonl(index_path / "text_docs.jsonl", text_docs)
    _write_jsonl(index_path / "image_docs.jsonl", image_docs)

    stats = {
        "cases": len(cases),
        "field_docs": len(field_docs),
        "text_docs": len(text_docs),
        "image_docs": len(image_docs),
    }
    (index_path / "stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return stats


def _write_jsonl(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")
