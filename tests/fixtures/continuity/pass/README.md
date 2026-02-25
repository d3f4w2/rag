# fixture

## 文档入口
1. 产品需求：`docs/product/product-requirements.md`
2. 技术栈基线：`docs/tech/tech-stack.md`
3. 系统架构：`docs/architecture/system-architecture.md`
4. 实施计划（任务级）：`docs/plans/2026-02-24-rag-implementation.md`
5. 全局进度看板：`docs/plans/progress-board.md`
6. 会话交接记录：`docs/plans/session-handoff.md`
7. 决策日志：`docs/plans/decision-log.md`
8. 连续性运行手册：`docs/plans/session-continuity-runbook.md`

## 会话连续性门禁
```bash
python tools/validate_session_continuity.py --strict
```

## 新会话接续协议（必须按顺序）
1. 先看 `README.md` 确认当前阶段与文档入口。
2. 看 `docs/plans/progress-board.md` 找到首个 `not_started` 或 `blocked` 的任务。
3. 看 `docs/plans/2026-02-24-rag-implementation.md` 执行对应任务的 Step 1-5。
4. 结束会话前更新：
   - `docs/plans/progress-board.md`
   - `docs/plans/session-handoff.md`
