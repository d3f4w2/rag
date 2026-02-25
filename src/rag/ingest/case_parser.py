from pathlib import Path

from rag.models import CaseRecord


def parse_cases(root: str) -> list[CaseRecord]:
    base = Path(root)
    records: list[CaseRecord] = []

    for label_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        label = label_dir.name
        for patient_dir in sorted(p for p in label_dir.iterdir() if p.is_dir()):
            txt_path = _pick_one(patient_dir, "*.txt")
            pdf_path = _pick_one(patient_dir, "*.pdf")
            image_paths = [
                str(path)
                for path in sorted(
                    patient_dir.glob("*.jpg"),
                    key=lambda path: int(path.stem),
                )
            ]

            records.append(
                CaseRecord(
                    case_id=f"{label}/{patient_dir.name}",
                    label=label,
                    patient_name=patient_dir.name,
                    txt_path=str(txt_path),
                    pdf_path=str(pdf_path),
                    image_paths=image_paths,
                )
            )

    return records


def _pick_one(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"No file matching {pattern} under {directory}")
    return matches[0]
