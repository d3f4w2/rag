from __future__ import annotations

from pathlib import Path

from rag.ingest.image_caption import make_caption
from rag.ingest.pdf_parser import extract_report_fields
from rag.models import CaseRecord


def build_text_documents(cases: list[CaseRecord]) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    for case in cases:
        txt_text = _read_text(case.txt_path).strip()
        pdf_raw_text = (extract_report_fields(case.pdf_path).get("raw_text") or "").strip()
        text = txt_text or pdf_raw_text or f"{case.label} {case.patient_name}"
        documents.append(
            {
                "case_id": case.case_id,
                "source": "txt_pdf",
                "text": text,
            }
        )

    return documents


def build_image_documents(cases: list[CaseRecord]) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    for case in cases:
        for image_path in case.image_paths:
            filename = Path(image_path).name
            documents.append(
                {
                    "case_id": case.case_id,
                    "image_path": image_path,
                    "caption": make_caption(filename, case.label, case.patient_name),
                }
            )

    return documents


def _read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""
