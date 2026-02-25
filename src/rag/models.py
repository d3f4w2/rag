from dataclasses import dataclass


@dataclass
class CaseRecord:
    case_id: str
    label: str
    patient_name: str
    txt_path: str
    pdf_path: str
    image_paths: list[str]
    cervix_findings: str | None = None
    vagina_findings: str | None = None
