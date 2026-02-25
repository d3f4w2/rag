from __future__ import annotations

from pathlib import Path

import pytest

from rag.governance.continuity_rules import validate_repository

from .helpers import apply_fail_override, build_repo_from_pass_fixture


def test_pass_fixture_has_no_violations(tmp_path: Path) -> None:
    repo_root = build_repo_from_pass_fixture(tmp_path)
    result = validate_repository(repo_root, strict=True)
    assert result.status == "PASS"
    assert result.violations == []
    assert result.warnings == []


@pytest.mark.parametrize(
    ("override_name", "expected_code"),
    [
        ("missing_handoff_field", "R008"),
        ("no_actionable_task", "R004"),
        ("missing_steps", "R010"),
    ],
)
def test_fail_fixtures_raise_expected_errors(
    tmp_path: Path, override_name: str, expected_code: str
) -> None:
    repo_root = build_repo_from_pass_fixture(tmp_path)
    apply_fail_override(repo_root, override_name)
    result = validate_repository(repo_root, strict=True)
    codes = {item.code for item in result.violations}
    assert expected_code in codes


def test_ambiguous_next_action_is_warning_by_default_and_error_in_strict(
    tmp_path: Path,
) -> None:
    repo_root = build_repo_from_pass_fixture(tmp_path)
    apply_fail_override(repo_root, "ambiguous_next_action")

    soft = validate_repository(repo_root, strict=False)
    strict = validate_repository(repo_root, strict=True)

    assert any(item.code == "R006" for item in soft.warnings)
    assert all(item.code != "R006" for item in soft.violations)
    assert any(item.code == "R006" for item in strict.violations)
