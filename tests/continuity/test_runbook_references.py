from __future__ import annotations

from pathlib import Path


def test_readme_links_runbook_and_startup_command() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")
    assert "docs/plans/session-continuity-runbook.md" in readme
    assert "python tools/validate_session_continuity.py --strict" in readme


def test_runbook_contains_start_and_end_session_sections() -> None:
    runbook = Path("docs/plans/session-continuity-runbook.md").read_text(encoding="utf-8")
    assert "会话开始" in runbook
    assert "会话结束" in runbook
