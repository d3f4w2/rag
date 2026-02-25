from __future__ import annotations

from pathlib import Path


RULE_IDS = [f"R{i:03d}" for i in range(1, 13)]


def test_operational_readiness_checklist_exists_with_all_rules() -> None:
    path = Path("docs/plans/operational-readiness-checklist.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for rule_id in RULE_IDS:
        assert rule_id in text


def test_decision_log_contains_continuity_guardrail_decision() -> None:
    text = Path("docs/plans/decision-log.md").read_text(encoding="utf-8")
    assert "DEC-008" in text
    assert "文档+校验脚本" in text
