from __future__ import annotations

from pathlib import Path

from rag.governance.continuity_rules import validate_repository


def test_cold_start_resolution_is_stable_three_times() -> None:
    observed = []
    for _ in range(3):
        result = validate_repository(Path.cwd(), strict=True)
        assert result.status == "PASS"
        assert result.next_task_id is not None
        assert result.next_first_command is not None
        observed.append((result.next_task_id, result.next_first_command))

    assert len(set(observed)) == 1
