from __future__ import annotations

import json
from pathlib import Path

from rag.ingest.case_parser import parse_cases
from rag.ingest.pdf_parser import extract_report_fields
from rag.ingest.txt_parser import parse_stain_text


def build_dataset(dataset_path: str, data_dir: str = "example-data") -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for case in parse_cases(data_dir):
        txt_content = Path(case.txt_path).read_text(encoding="utf-8", errors="ignore")
        txt_fields = parse_stain_text(txt_content)
        pdf_fields = extract_report_fields(case.pdf_path)

        reference = (
            f"label={case.label};"
            f"cervix={txt_fields.get('cervix_findings', '')};"
            f"vagina={txt_fields.get('vagina_findings', '')};"
            f"hpv={pdf_fields.get('hpv') or ''};"
            f"impression={pdf_fields.get('impression') or ''}"
        )
        rows.append(
            {
                "question": f"What evidence supports case {case.case_id}?",
                "reference": reference,
                "contexts": [reference],
                "case_id": case.case_id,
            }
        )

    output = Path(dataset_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")

    return rows
