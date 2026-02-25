from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from .helpers import apply_fail_override, build_repo_from_pass_fixture


def _run_validator(repo_root: Path, *extra_args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "tools/validate_session_continuity.py",
            "--root",
            str(repo_root),
            *extra_args,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_validator_cli_returns_zero_for_pass_fixture(tmp_path: Path) -> None:
    repo_root = build_repo_from_pass_fixture(tmp_path)
    proc = _run_validator(repo_root, "--json")
    payload = json.loads(proc.stdout)

    assert proc.returncode == 0
    assert payload["status"] == "PASS"
    assert payload["next_task_id"] == "I1"
    assert payload["next_first_command"] == (
        "python -m pytest tests/cli/test_cli_help.py::test_cli_help_shows_commands -v"
    )


def test_validator_cli_returns_one_for_fail_fixture(tmp_path: Path) -> None:
    repo_root = build_repo_from_pass_fixture(tmp_path)
    apply_fail_override(repo_root, "missing_handoff_field")

    proc = _run_validator(repo_root, "--json")
    payload = json.loads(proc.stdout)
    codes = {item["code"] for item in payload["violations"]}

    assert proc.returncode == 1
    assert payload["status"] == "FAIL"
    assert "R008" in codes
