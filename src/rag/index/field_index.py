from __future__ import annotations

from pathlib import Path

from rag.ingest.pdf_parser import extract_report_fields
from rag.ingest.txt_parser import parse_stain_text
from rag.models import CaseRecord


def build_field_documents(cases: list[CaseRecord]) -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []

    for case in cases:
        stain_fields = parse_stain_text(_read_text(case.txt_path))
        report_fields = extract_report_fields(case.pdf_path)
        flattened_fields = {
            "label": case.label,
            "patient_name": case.patient_name,
            "cervix_findings": stain_fields.get("cervix_findings", ""),
            "vagina_findings": stain_fields.get("vagina_findings", ""),
            "tct": report_fields.get("tct") or "",
            "hpv": report_fields.get("hpv") or "",
            "impression": report_fields.get("impression") or "",
            "plan": report_fields.get("plan") or "",
        }

        for field_name, value in flattened_fields.items():
            if not value:
                continue
            documents.append(
                {
                    "case_id": case.case_id,
                    "field": field_name,
                    "text": str(value),
                }
            )

    return documents


def _read_text(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        return ""
