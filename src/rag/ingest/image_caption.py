from pathlib import Path

_STAGE_MAP = {
    1: "baseline",
    2: "post_acetic",
    3: "post_acetic",
    4: "post_acetic",
    5: "post_iodine",
}


def stage_from_filename(filename: str) -> str:
    try:
        index = int(Path(filename).stem)
    except ValueError:
        return "unknown"
    return _STAGE_MAP.get(index, "unknown")


def make_caption(filename: str, label: str, patient_name: str) -> str:
    stage = stage_from_filename(filename)
    return f"{patient_name} {label} image {filename} at {stage}"
