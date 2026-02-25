# RAG Product Requirements (Phase 1)

Status: Baseline  
Last Updated: 2026-02-24

## Related Execution Docs
1. `docs/plans/2026-02-24-rag-implementation.md`
2. `docs/plans/progress-board.md`
3. `docs/plans/decision-log.md`

## 1. 产品目标
构建一个本地可运行的病例检索问答系统，用于对样例病例数据进行证据检索与结果汇总。系统输出必须可追溯到具体文件片段，并明确非诊断属性。

## 2. 目标用户
1. 项目研发人员（验证 RAG 全链路）
2. 医疗场景数据/算法协作人员（查看证据链质量）

## 3. 核心问题
1. 如何在多模态病例（TXT/PDF/JPG）中稳定检索相关证据
2. 如何保证回答不脱离证据
3. 如何用统一标准评估检索与回答质量

## 4. In Scope（一期）
1. CLI 交互：`index` / `ask` / `eval`
2. 数据源：`example-data` 目录
3. 输出：结构化 JSON（answer/evidence/sources/confidence/limits）
4. 评估：RAGAS 四项核心指标 + 硬门禁

## 5. Out of Scope（一期不做）
1. 自动诊断或治疗建议
2. 实时增量入库/目录监听
3. Web UI 或外部 API 服务
4. 深度视觉模型图像理解

## 6. 一期成功标准
1. 可完成全量索引并可查询
2. 回答包含可追溯证据路径
3. 评估链路可产出四项指标并执行阈值门禁
4. 未命中时能明确返回低置信结果而非编造答案

## 7. 非功能约束
1. 可追溯性：每条证据必须包含来源路径
2. 可解释性：回答仅基于证据汇总
3. 合规表达：固定声明“结果不构成诊断建议”

## 8. 一期验收口径（业务视角）
1. 用户给出问题后系统可返回结构化回答
2. 返回内容可以定位到 `example-data` 对应文件
3. 评估失败时明确阻断并输出诊断报告
