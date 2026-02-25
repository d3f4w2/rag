# RAG System Architecture (Phase 1)

Status: Baseline  
Last Updated: 2026-02-24

## Related Execution Docs
1. `docs/plans/2026-02-24-rag-implementation.md`
2. `docs/plans/progress-board.md`
3. `docs/plans/decision-log.md`

## 1. 架构目标
构建“病例中心”RAG链路：多路检索、病例级重排、证据约束回答、评估门禁闭环。

## 2. 系统模块
1. Ingest
   - 解析目录结构与病例主键（`case_id`）
   - 抽取 TXT/PDF 字段，生成图像阶段 caption
2. Index
   - 字段索引（结构化信息）
   - 文本索引（TXT/PDF chunk）
   - 图像caption索引
3. Retrieval
   - 三路并行召回
   - 病例级聚合与重排
4. Workflow
   - LangGraph 编排查询流程
5. Evaluation
   - RAGAS 指标计算与阈值门禁

## 3. LangGraph 节点流
1. `normalize_query`
2. `intent_router`
3. `retrieve_fields`
4. `retrieve_text`
5. `retrieve_image_caption`
6. `merge_and_rerank_cases`
7. `compose_answer_with_citations`
8. `final_guardrail`

## 4. 数据流
1. 离线：`example-data` -> 解析 -> 三路索引
2. 在线：问题输入 -> 三路召回 -> 病例级排序 -> JSON 输出
3. 评估：问答输出 -> RAGAS -> 门禁判定 -> 报告

## 5. 输出契约
回答输出 JSON 必须包含：
1. `question`
2. `answer`
3. `evidence`
4. `sources`
5. `confidence`
6. `limits`
7. `trace_id`

`evidence` 项必须包含：
1. `case_id`
2. `source_type`
3. `source_path`
4. `quote_or_summary`
5. `relevance_score`

## 6. 错误处理与降级
1. 单路召回失败不终止主流程
2. 证据不足时输出低置信并明确提示
3. 固定追加“非诊断建议”限制说明

## 7. 一期不做
1. 在线 API 服务化
2. 实时增量索引
3. 重型多模态视觉理解
