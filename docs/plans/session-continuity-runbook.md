# Session Continuity Runbook

Status: Active  
Last Updated: 2026-02-25

## 会话开始
1. 运行严格校验命令：
   - `python tools/validate_session_continuity.py --strict`
2. 读取输出中的 `Next Task` 和 `Next First Command`。
3. 执行 `Next First Command`，进入对应任务。
4. 若校验失败：按 violations 的 suggestion 先修复文档，再重新执行第 1 步。

## 会话进行中
1. 每完成一个任务，立即回写看板状态。
2. 任何 `blocked` 必须同步写入 `blocker` 和解除动作。
3. 任何任务切换必须同步更新 `Next First Command`。

## 会话结束
1. 更新 `docs/plans/progress-board.md`：
   - `status`
   - `updated_at`
   - `next_action`
2. 更新 `docs/plans/session-handoff.md`：
   - `Completed / In Progress`
   - `Next First Command`
   - `Updated Files`
   - `Blockers`
3. 结束前再次执行：
   - `python tools/validate_session_continuity.py --strict`
4. 若未通过严格校验，不得宣告会话可交接。
