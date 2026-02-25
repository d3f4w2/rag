# Operational Readiness Checklist

Status: Active  
Last Updated: 2026-02-25

## Goal
在会话开始前，用统一规则判断仓库是否满足“零追问可执行 + 跨会话可连续执行”。

## Rule Catalog
| Rule ID | Severity | Check Item | Pass Condition |
|---|---|---|---|
| R001 | error | README 文档入口完整性 | `README.md` 包含 7 个核心文档入口链接 |
| R002 | error | README 接续协议完整性 | 包含“新会话接续协议”并按 1-4 步固定顺序描述 |
| R003 | error | 看板结构完整性 | `progress-board.md` 存在且任务表格可解析 |
| R004 | error | 可执行任务存在性 | 看板存在至少一个 `not_started/in_progress/blocked` 任务 |
| R005 | error | in_progress 责任人约束 | `in_progress` 任务 `owner` 不得为 `TBD` |
| R006 | warning | next_action 可执行性 | `next_action` 必须是反引号包裹命令，禁止模糊动作词 |
| R007 | error | blocked 说明完整性 | `blocked` 状态必须提供非空 `blocker` |
| R008 | error | 会话交接关键字段 | `session-handoff.md` 必须包含 `Next First Command/Updated Files/Blockers` |
| R009 | error | Next First Command 可执行性 | `Next First Command` 必须提供反引号包裹命令 |
| R010 | error | 任务步骤完整性 | 每个 Task 必须包含 `Step 1..5` |
| R011 | error | 任务验证命令完整性 | 每个 Task 必须包含至少 1 条 `Run:` 命令 |
| R012 | error | 启动校验入口可发现性 | README 必须包含 runbook 链接和严格校验命令 |

## Session Start Gate
```bash
python tools/validate_session_continuity.py --strict
```

## Session End Minimum Checklist
1. 更新 `docs/plans/progress-board.md` 的 `status` 和 `updated_at`。
2. 若状态为 `blocked`，补齐 `blocker` 和解除动作。
3. 更新 `docs/plans/session-handoff.md` 的 `Next First Command` 与 `Updated Files`。
4. 重新运行一次严格校验，保证下一个会话可冷启动接续。
