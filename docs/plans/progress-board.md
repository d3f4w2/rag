# RAG Progress Board

Status: Batch 4 complete (Task 10-12)  
Last Updated: 2026-02-25

## Status Enum
- `not_started`
- `in_progress`
- `blocked`
- `done`
- `verified`

## Board
| task_id | task_name | milestone | status | owner | start_at | updated_at | next_action | blocker | artifact |
|---|---|---|---|---|---|---|---|---|---|
| D1 | README入口重构 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 持续维护导航链接 | none | `README.md` |
| D2 | 产品文档基线 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 需求变更时同步更新 | none | `docs/product/product-requirements.md` |
| D3 | 技术栈文档基线 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 实施前补充版本冻结策略 | none | `docs/tech/tech-stack.md` |
| D4 | 架构文档基线 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 实施前补齐模块输入输出 | none | `docs/architecture/system-architecture.md` |
| D5 | 实施计划任务化 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 按任务开始执行 | none | `docs/plans/2026-02-24-rag-implementation.md` |
| D6 | 会话交接模板 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 每次会话结束更新 | none | `docs/plans/session-handoff.md` |
| D7 | 决策日志模板 | M0 | done | codex | 2026-02-24 | 2026-02-24 | 新决策及时记录 | none | `docs/plans/decision-log.md` |
| D8 | 连续性验收清单与Runbook | M0 | done | codex | 2026-02-25 | 2026-02-25 | 持续维护规则与SOP | none | `docs/plans/operational-readiness-checklist.md` |
| D9 | 连续性校验脚本与测试 | M0 | verified | codex | 2026-02-25 | 2026-02-25 | `python tools/validate_session_continuity.py --strict` | none | `tools/validate_session_continuity.py` |
| I1 | Task 1-2 bootstrap and deps | M1 | done | codex | 2026-02-25 | 2026-02-25 | `python -m pytest tests/ingest/test_txt_parser.py::test_parse_stain_text_extracts_two_fields -v` | none | `docs/plans/2026-02-24-rag-implementation.md` |
| I2 | Task 3-6 ingest pipeline | M1 | done | codex | 2026-02-25 | 2026-02-25 | `python -m pytest tests/index/test_build_index.py::test_rebuild_index_returns_stats -v` | none | `docs/plans/2026-02-24-rag-implementation.md` |
| I3 | Task 7-10 检索与工作流 | M2 | verified | codex | 2026-02-25 | 2026-02-25 | `D:\miniconda\envs\rag\python.exe -m pytest tests/workflow/test_graph_contract.py -v` | none | `docs/plans/2026-02-24-rag-implementation.md` |
| I4 | Task 11-12 评估与门禁 | M3 | verified | codex | 2026-02-25 | 2026-02-25 | `D:\miniconda\envs\rag\python.exe -m pytest tests/eval/test_ragas_runner_contract.py tests/eval/test_gate_thresholds.py -v` | none | `docs/plans/2026-02-24-rag-implementation.md` |
| I5 | Task 13 回归与收敛 | M4 | not_started | TBD | - | 2026-02-25 | `python -m pytest tests/e2e/test_minimal_e2e.py::test_placeholder_e2e -v` | none | `docs/plans/2026-02-24-rag-implementation.md` |

## Board Update Rules
1. 每次会话至少更新一次 `status` 和 `updated_at`。
2. `blocked` 必须填写 `blocker`。
3. 执行结束前同步写入 `docs/plans/session-handoff.md`。
4. `next_action` 必须是可直接复制执行的反引号命令，禁止“继续推进”类模糊表述。
