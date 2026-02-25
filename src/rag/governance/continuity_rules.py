from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


ACTIONABLE_STATUSES = {"not_started", "in_progress", "blocked"}
REQUIRED_DOC_LINKS = (
    "docs/product/product-requirements.md",
    "docs/tech/tech-stack.md",
    "docs/architecture/system-architecture.md",
    "docs/plans/2026-02-24-rag-implementation.md",
    "docs/plans/progress-board.md",
    "docs/plans/session-handoff.md",
    "docs/plans/decision-log.md",
)
REQUIRED_PROTOCOL_STEPS = (
    "先看 `README.md`",
    "看 `docs/plans/progress-board.md`",
    "看 `docs/plans/2026-02-24-rag-implementation.md`",
    "结束会话前更新",
)
REQUIRED_HANDOFF_FIELDS = (
    "- Next First Command:",
    "- Updated Files:",
    "- Blockers:",
)
AMBIGUOUS_ACTION_HINTS = (
    "继续推进",
    "按任务开始执行",
    "完成后推进",
    "推进",
)


@dataclass(frozen=True)
class Finding:
    code: str
    file: str
    message: str
    suggestion: str
    severity: str

    def to_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "file": self.file,
            "message": self.message,
            "suggestion": self.suggestion,
            "severity": self.severity,
        }


@dataclass(frozen=True)
class ValidationResult:
    status: str
    next_task_id: str | None
    next_first_command: str | None
    violations: list[Finding]
    warnings: list[Finding]

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "next_task_id": self.next_task_id,
            "next_first_command": self.next_first_command,
            "violations": [item.to_dict() for item in self.violations],
            "warnings": [item.to_dict() for item in self.warnings],
        }


def validate_repository(root: Path, strict: bool = False) -> ValidationResult:
    root = root.resolve()
    violations: list[Finding] = []
    warnings: list[Finding] = []

    _check_readme(root, violations)
    next_task_id, board_command = _check_progress_board(root, violations, warnings)
    handoff_command = _check_session_handoff(root, violations)
    _check_implementation_plan(root, violations)

    if strict and warnings:
        violations.extend(
            Finding(
                code=item.code,
                file=item.file,
                message=item.message,
                suggestion=item.suggestion,
                severity="error",
            )
            for item in warnings
        )
        warnings = []

    next_first_command = board_command or handoff_command
    status = "PASS" if not violations else "FAIL"
    return ValidationResult(
        status=status,
        next_task_id=next_task_id,
        next_first_command=next_first_command,
        violations=violations,
        warnings=warnings,
    )


def _check_readme(root: Path, violations: list[Finding]) -> None:
    readme_path = root / "README.md"
    if not readme_path.exists():
        violations.append(
            Finding(
                code="R001",
                file="README.md",
                message="缺失 README.md，无法作为跨会话入口。",
                suggestion="创建 README.md 并补齐文档入口与接续协议。",
                severity="error",
            )
        )
        return

    text = readme_path.read_text(encoding="utf-8")
    missing_links = [item for item in REQUIRED_DOC_LINKS if item not in text]
    if missing_links:
        violations.append(
            Finding(
                code="R001",
                file="README.md",
                message=f"README 缺少文档入口链接: {', '.join(missing_links)}",
                suggestion="在 README 的“文档入口”中补齐缺失链接。",
                severity="error",
            )
        )

    if "新会话接续协议" not in text or any(step not in text for step in REQUIRED_PROTOCOL_STEPS):
        violations.append(
            Finding(
                code="R002",
                file="README.md",
                message="README 缺少完整的新会话接续协议顺序说明。",
                suggestion="补齐“新会话接续协议”并按固定顺序列出四步。",
                severity="error",
            )
        )

    if (
        "docs/plans/session-continuity-runbook.md" not in text
        or "python tools/validate_session_continuity.py --strict" not in text
    ):
        violations.append(
            Finding(
                code="R012",
                file="README.md",
                message="README 未声明 runbook 链接或严格校验启动命令。",
                suggestion="补充 runbook 链接与 `python tools/validate_session_continuity.py --strict`。",
                severity="error",
            )
        )


def _check_progress_board(
    root: Path, violations: list[Finding], warnings: list[Finding]
) -> tuple[str | None, str | None]:
    board_path = root / "docs" / "plans" / "progress-board.md"
    if not board_path.exists():
        violations.append(
            Finding(
                code="R003",
                file="docs/plans/progress-board.md",
                message="缺失 progress-board.md。",
                suggestion="创建进度看板并维护任务表格。",
                severity="error",
            )
        )
        return None, None

    text = board_path.read_text(encoding="utf-8")
    table_lines = [line.strip() for line in text.splitlines() if line.strip().startswith("|")]
    if len(table_lines) < 3:
        violations.append(
            Finding(
                code="R003",
                file="docs/plans/progress-board.md",
                message="进度看板表格格式不完整。",
                suggestion="确保看板包含表头、分隔行和至少一条任务行。",
                severity="error",
            )
        )
        return None, None

    rows = []
    for line in table_lines[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 10:
            violations.append(
                Finding(
                    code="R003",
                    file="docs/plans/progress-board.md",
                    message=f"无法解析任务行: {line}",
                    suggestion="确保每行都包含 10 个列值。",
                    severity="error",
                )
            )
            continue
        rows.append(
            {
                "task_id": cells[0],
                "status": cells[3],
                "owner": cells[4],
                "next_action": cells[7],
                "blocker": cells[8],
            }
        )

    actionable_rows = [row for row in rows if row["status"] in ACTIONABLE_STATUSES]
    if not actionable_rows:
        violations.append(
            Finding(
                code="R004",
                file="docs/plans/progress-board.md",
                message="看板没有可执行任务（not_started/in_progress/blocked）。",
                suggestion="至少保留一个可执行任务并给出 next_action。",
                severity="error",
            )
        )
        return None, None

    next_task_id = actionable_rows[0]["task_id"]
    next_command = _extract_backtick_command(actionable_rows[0]["next_action"])

    for row in actionable_rows:
        if row["status"] == "in_progress" and row["owner"] in {"TBD", "-", ""}:
            violations.append(
                Finding(
                    code="R005",
                    file="docs/plans/progress-board.md",
                    message=f"{row['task_id']} 为 in_progress 但 owner 未明确。",
                    suggestion="将 owner 从 TBD 更新为明确负责人。",
                    severity="error",
                )
            )

        if row["status"] == "blocked" and row["blocker"] in {"none", "None", "-", ""}:
            violations.append(
                Finding(
                    code="R007",
                    file="docs/plans/progress-board.md",
                    message=f"{row['task_id']} 为 blocked 但 blocker 为空。",
                    suggestion="填写阻塞原因和解除动作。",
                    severity="error",
                )
            )

        if not _looks_executable_action(row["next_action"]):
            warnings.append(
                Finding(
                    code="R006",
                    file="docs/plans/progress-board.md",
                    message=f"{row['task_id']} 的 next_action 不可直接执行。",
                    suggestion="将 next_action 改为反引号包裹的可执行命令。",
                    severity="warning",
                )
            )

    return next_task_id, next_command


def _check_session_handoff(root: Path, violations: list[Finding]) -> str | None:
    handoff_path = root / "docs" / "plans" / "session-handoff.md"
    if not handoff_path.exists():
        violations.append(
            Finding(
                code="R008",
                file="docs/plans/session-handoff.md",
                message="缺失 session-handoff.md。",
                suggestion="创建会话交接文档并使用模板字段。",
                severity="error",
            )
        )
        return None

    text = handoff_path.read_text(encoding="utf-8")
    missing_fields = [field for field in REQUIRED_HANDOFF_FIELDS if field not in text]
    if missing_fields:
        violations.append(
            Finding(
                code="R008",
                file="docs/plans/session-handoff.md",
                message=f"会话交接缺少关键字段: {', '.join(missing_fields)}",
                suggestion="补齐 Next First Command / Updated Files / Blockers 字段。",
                severity="error",
            )
        )
        return None

    next_command = _extract_next_first_command(text)
    if not next_command:
        violations.append(
            Finding(
                code="R009",
                file="docs/plans/session-handoff.md",
                message="Next First Command 未提供可执行命令。",
                suggestion="在 Next First Command 下提供反引号包裹的命令。",
                severity="error",
            )
        )
    return next_command


def _check_implementation_plan(root: Path, violations: list[Finding]) -> None:
    plan_path = root / "docs" / "plans" / "2026-02-24-rag-implementation.md"
    if not plan_path.exists():
        violations.append(
            Finding(
                code="R010",
                file="docs/plans/2026-02-24-rag-implementation.md",
                message="缺失实施计划文件。",
                suggestion="创建任务级实施计划并补齐 Step 1-5。",
                severity="error",
            )
        )
        return

    text = plan_path.read_text(encoding="utf-8")
    task_matches = list(re.finditer(r"^### Task .+$", text, flags=re.MULTILINE))
    if not task_matches:
        violations.append(
            Finding(
                code="R010",
                file="docs/plans/2026-02-24-rag-implementation.md",
                message="实施计划中未找到 Task 定义。",
                suggestion="添加至少一个 `### Task N` 任务段落。",
                severity="error",
            )
        )
        return

    for index, match in enumerate(task_matches):
        start = match.start()
        end = task_matches[index + 1].start() if index + 1 < len(task_matches) else len(text)
        task_title = match.group(0).strip()
        section = text[start:end]

        missing_steps = [
            str(step_number)
            for step_number in range(1, 6)
            if f"**Step {step_number}:" not in section
        ]
        if missing_steps:
            violations.append(
                Finding(
                    code="R010",
                    file="docs/plans/2026-02-24-rag-implementation.md",
                    message=f"{task_title} 缺少 Step {', '.join(missing_steps)}。",
                    suggestion="补齐 Step 1-5，保证任务可逐步执行。",
                    severity="error",
                )
            )

        if "Run: `" not in section:
            violations.append(
                Finding(
                    code="R011",
                    file="docs/plans/2026-02-24-rag-implementation.md",
                    message=f"{task_title} 未提供可执行的验证命令。",
                    suggestion="在步骤中补充 `Run: ` 命令和预期结果。",
                    severity="error",
                )
            )


def _extract_backtick_command(text: str) -> str | None:
    match = re.search(r"`([^`]+)`", text)
    if not match:
        return None
    command = match.group(1).strip()
    return command or None


def _looks_executable_action(action: str) -> bool:
    command = _extract_backtick_command(action)
    if command:
        return True

    if any(hint in action for hint in AMBIGUOUS_ACTION_HINTS):
        return False

    return False


def _extract_next_first_command(text: str) -> str | None:
    marker = "- Next First Command:"
    if marker not in text:
        return None

    tail = text.split(marker, maxsplit=1)[1]
    return _extract_backtick_command(tail)
