# Decision Log

Status: Baseline  
Last Updated: 2026-02-25

## Record Format
| id | date | decision | rationale | impact | owner | status |
|---|---|---|---|---|---|---|

## Locked Decisions
| id | date | decision | rationale | impact | owner | status |
|---|---|---|---|---|---|---|
| DEC-001 | 2026-02-24 | 使用病例中心多路检索 | 与样例数据组织方式一致，证据可追溯 | 影响数据模型与重排策略 | team | locked |
| DEC-002 | 2026-02-24 | 工作流采用 LangGraph | 多节点流程更易观测和扩展 | 影响 `workflow` 模块实现 | team | locked |
| DEC-003 | 2026-02-24 | 评估采用 RAGAS 四项指标 | 覆盖检索与回答质量 | 影响评估与门禁实现 | team | locked |
| DEC-004 | 2026-02-24 | 门禁阈值固定 0.70/0.70/0.80/0.75 | 平衡首版可达性与质量约束 | 影响发布阻断策略 | team | locked |
| DEC-005 | 2026-02-24 | 外部模型接入走 OpenAI-compatible | 减少适配成本，便于后续替换 | 影响配置与评估接口 | team | locked |
| DEC-006 | 2026-02-24 | 先文档后实现 | 降低跨会话执行偏差 | 影响当前阶段输出边界 | team | locked |
| DEC-007 | 2026-02-24 | 实施计划必须任务级（2-5分钟） | 提升跨会话连续执行稳定性 | 影响计划文档结构 | team | locked |
| DEC-008 | 2026-02-25 | 跨会话治理采用“文档+校验脚本”双轨机制 | 仅靠人工阅读无法稳定判定连续性达标 | 影响会话启动门禁、交接格式和看板约束 | team | locked |

## Change Policy
1. 任何影响默认值的改动必须新增一条记录，不修改历史条目。
2. 变更后同步更新：
   - `docs/tech/tech-stack.md`
   - `docs/architecture/system-architecture.md`
   - `docs/plans/2026-02-24-rag-implementation.md`
   - `docs/plans/progress-board.md`
