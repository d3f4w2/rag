from __future__ import annotations

import shutil
from pathlib import Path


FIXTURES_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "continuity"


def _copy_tree(source: Path, destination: Path) -> None:
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        target = destination / relative
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item, target)


def build_repo_from_pass_fixture(target_root: Path) -> Path:
    _copy_tree(FIXTURES_ROOT / "pass", target_root)
    return target_root


def apply_fail_override(target_root: Path, override_name: str) -> Path:
    _copy_tree(FIXTURES_ROOT / "fail" / override_name, target_root)
    return target_root
