from __future__ import annotations

from pathlib import Path

from rag.governance.continuity_rules import validate_repository


def test_repository_current_state_passes_strict_continuity_validation() -> None:
    result = validate_repository(Path.cwd(), strict=True)
    assert result.status == "PASS"
    assert result.next_task_id is not None
    assert result.next_first_command is not None
