# RAG Technical Stack Baseline

Status: Baseline  
Last Updated: 2026-02-24

## Related Execution Docs
1. `docs/plans/2026-02-24-rag-implementation.md`
2. `docs/plans/progress-board.md`
3. `docs/plans/decision-log.md`

## 1. 运行环境
1. 环境管理：Conda
2. 环境名称：`rag`
3. Python 版本：`3.11`（建议）

## 2. 依赖策略
核心原则：`langchain >= 1.0`，其他库以兼容性优先，不盲目追新。

### 2.1 Core
1. `langchain>=1.0`
2. `langgraph`
3. `chromadb`
4. `sqlite`（FTS5）
5. `pydantic`
6. `pypdf`

### 2.2 Eval
1. `ragas`

### 2.3 Dev
1. `pytest`

## 3. 外部模型接入
1. 使用第三方 OpenAI-compatible API
2. 配置项（示例）：
   - `OPENAI_API_KEY`
   - `OPENAI_BASE_URL`
   - `OPENAI_MODEL`
3. 评估模型与业务模型应支持解耦配置

## 4. 技术边界（一期）
1. 不接入重型视觉推理模型
2. 不实现在线服务部署体系
3. 不做实时增量索引机制

## 5. 兼容性与升级策略
1. 先保证主流程稳定，再进行依赖升级
2. 升级按“单模块逐步验证”执行
3. 升级后必须重新跑 RAGAS 门禁
