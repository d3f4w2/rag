from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader


def extract_report_fields(pdf_path: str) -> dict[str, str | None]:
    raw_text = _extract_text(pdf_path)
    return {
        "age": _first_match(raw_text, [r"(?:年龄|Age)\s*[:：]\s*([0-9]{1,3})"]),
        "tct": _first_match(raw_text, [r"(?:TCT)\s*[:：]\s*([^\n\r]+)"]),
        "hpv": _first_match(raw_text, [r"(?:HPV)\s*[:：]\s*([^\n\r]+)"]),
        "impression": _first_match(raw_text, [r"(?:印象|Impression)\s*[:：]\s*([^\n\r]+)"]),
        "plan": _first_match(raw_text, [r"(?:建议|Plan)\s*[:：]\s*([^\n\r]+)"]),
        "followup_date": _first_match(
            raw_text,
            [r"(?:随访日期|Follow[- ]?up)\s*[:：]\s*([0-9]{4}[-/.年][0-9]{1,2}[-/.月][0-9]{1,2})"],
        ),
        "raw_text": raw_text,
    }


def _extract_text(pdf_path: str) -> str:
    path = Path(pdf_path)
    if not path.exists():
        return ""

    try:
        reader = PdfReader(str(path))
    except Exception:
        return ""

    parts: list[str] = []
    for page in reader.pages:
        try:
            parts.append(page.extract_text() or "")
        except Exception:
            parts.append("")
    return "\n".join(parts).strip()


def _first_match(text: str, patterns: list[str]) -> str | None:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1).strip() or None
    return None
