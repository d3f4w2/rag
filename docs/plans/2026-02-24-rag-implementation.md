# RAG Phase 1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a case-centric RAG CLI over `example-data` with evidence-grounded answers and RAGAS hard-gate quality checks.

**Architecture:** The codebase is split into ingest/index/retrieval/workflow/eval layers. Runtime flow uses LangGraph for query normalization, multi-route retrieval, case-level rerank, and citation-constrained answer composition. Evaluation uses a separate RAGAS pipeline with hard threshold gate.

**Tech Stack:** Python 3.11, conda (`rag` env), langchain>=1.0, langgraph, sqlite FTS5, chromadb, pydantic, pypdf, ragas, pytest.

---

## Scope Guard (for implementer)
1. 按任务顺序执行，不跳步。
2. 每个任务必须遵循 TDD：先失败、再最小实现、再通过、再提交。
3. 每完成 1 个任务，更新 `docs/plans/progress-board.md` 与 `docs/plans/session-handoff.md`。
4. 本计划中的文件路径、命令、阈值均视为锁定默认值，除非 `decision-log.md` 新增决策变更。

## Milestones
1. M1: 项目骨架与数据解析
2. M2: 检索与工作流
3. M3: 评估与门禁
4. M4: 文档收敛与回归校验

## Task Execution List

### Task 1: Bootstrap package and CLI skeleton (M1)

**Files:**
- Create: `pyproject.toml`
- Create: `src/rag/__init__.py`
- Create: `src/rag/cli.py`
- Test: `tests/cli/test_cli_help.py`

**Step 1: Write the failing test**

```python
# tests/cli/test_cli_help.py
import subprocess
import sys


def test_cli_help_shows_commands():
    proc = subprocess.run(
        [sys.executable, "-m", "rag.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0
    assert "index" in proc.stdout
    assert "ask" in proc.stdout
    assert "eval" in proc.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_cli_help.py::test_cli_help_shows_commands -v`  
Expected: FAIL with `ModuleNotFoundError` or command missing.

**Step 3: Write minimal implementation**

```python
# src/rag/cli.py
import typer

app = typer.Typer()


@app.command()
def index():
    typer.echo("index")


@app.command()
def ask():
    typer.echo("ask")


@app.command("eval")
def eval_cmd():
    typer.echo("eval")


def main():
    app()


if __name__ == "__main__":
    main()
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_cli_help.py::test_cli_help_shows_commands -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add pyproject.toml src/rag/__init__.py src/rag/cli.py tests/cli/test_cli_help.py
git commit -m "chore: bootstrap rag package and cli skeleton"
```

---

### Task 2: Add environment and dependency groups (M1)

**Files:**
- Create: `environment.yml`
- Create: `requirements/core.txt`
- Create: `requirements/eval.txt`
- Create: `requirements/dev.txt`
- Test: `tests/config/test_dependency_files.py`

**Step 1: Write the failing test**

```python
from pathlib import Path


def test_dependency_files_exist():
    assert Path("environment.yml").exists()
    assert Path("requirements/core.txt").exists()
    assert Path("requirements/eval.txt").exists()
    assert Path("requirements/dev.txt").exists()
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/config/test_dependency_files.py::test_dependency_files_exist -v`  
Expected: FAIL due to missing files.

**Step 3: Write minimal implementation**

```text
environment.yml:
- env name: rag
- python: 3.11

requirements/core.txt:
- langchain>=1.0
- langgraph
- chromadb
- pydantic
- pypdf

requirements/eval.txt:
- ragas

requirements/dev.txt:
- pytest
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/config/test_dependency_files.py::test_dependency_files_exist -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add environment.yml requirements/core.txt requirements/eval.txt requirements/dev.txt tests/config/test_dependency_files.py
git commit -m "chore: add environment and dependency groups"
```

---

### Task 3: Parse case directories into CaseRecord list (M1)

**Files:**
- Create: `src/rag/models.py`
- Create: `src/rag/ingest/case_parser.py`
- Test: `tests/ingest/test_case_parser.py`

**Step 1: Write the failing test**

```python
from rag.ingest.case_parser import parse_cases


def test_parse_cases_reads_all_examples():
    cases = parse_cases("example-data")
    assert len(cases) == 4
    assert all(c.label in {"HSIL", "LSIL"} for c in cases)
    assert all(len(c.image_paths) == 5 for c in cases)
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/ingest/test_case_parser.py::test_parse_cases_reads_all_examples -v`  
Expected: FAIL with missing module/function.

**Step 3: Write minimal implementation**

```text
CaseRecord fields:
- case_id
- label
- patient_name
- txt_path
- pdf_path
- image_paths
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/ingest/test_case_parser.py::test_parse_cases_reads_all_examples -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/models.py src/rag/ingest/case_parser.py tests/ingest/test_case_parser.py
git commit -m "feat: parse example-data into case records"
```

---

### Task 4: Parse TXT findings into structured fields (M1)

**Files:**
- Create: `src/rag/ingest/txt_parser.py`
- Modify: `src/rag/models.py`
- Test: `tests/ingest/test_txt_parser.py`

**Step 1: Write the failing test**

```python
from rag.ingest.txt_parser import parse_stain_text


def test_parse_stain_text_extracts_two_fields():
    text = "阴道镜所见(宫颈):A\n阴道镜所见(阴道):B\n"
    out = parse_stain_text(text)
    assert out["cervix_findings"] == "A"
    assert out["vagina_findings"] == "B"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/ingest/test_txt_parser.py::test_parse_stain_text_extracts_two_fields -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- clean control characters
- parse two fixed prefixes
- return dict: cervix_findings, vagina_findings
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/ingest/test_txt_parser.py::test_parse_stain_text_extracts_two_fields -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/ingest/txt_parser.py src/rag/models.py tests/ingest/test_txt_parser.py
git commit -m "feat: add structured txt findings parser"
```

---

### Task 5: Extract PDF fields with fallback (M1)

**Files:**
- Create: `src/rag/ingest/pdf_parser.py`
- Test: `tests/ingest/test_pdf_parser.py`

**Step 1: Write the failing test**

```python
from rag.ingest.pdf_parser import extract_report_fields


def test_extract_report_fields_returns_expected_keys():
    out = extract_report_fields("example-data/HSIL/刘从琴/刘从琴_检查报告_20240628095200.pdf")
    for k in ["age", "tct", "hpv", "impression", "plan", "followup_date", "raw_text"]:
        assert k in out
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/ingest/test_pdf_parser.py::test_extract_report_fields_returns_expected_keys -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- pypdf extract_text
- regex best-effort extraction
- always return full key set (None/empty fallback)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/ingest/test_pdf_parser.py::test_extract_report_fields_returns_expected_keys -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/ingest/pdf_parser.py tests/ingest/test_pdf_parser.py
git commit -m "feat: add pdf report field extractor with fallback"
```

---

### Task 6: Build image stage mapping and caption template (M1)

**Files:**
- Create: `src/rag/ingest/image_caption.py`
- Test: `tests/ingest/test_image_caption.py`

**Step 1: Write the failing test**

```python
from rag.ingest.image_caption import stage_from_filename, make_caption


def test_stage_mapping():
    assert stage_from_filename("1.jpg") == "baseline"
    assert stage_from_filename("3.jpg") == "post_acetic"
    assert stage_from_filename("5.jpg") == "post_iodine"


def test_make_caption_contains_stage():
    cap = make_caption("3.jpg", "HSIL", "刘从琴")
    assert "post_acetic" in cap
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/ingest/test_image_caption.py -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
1 -> baseline
2/3/4 -> post_acetic
5 -> post_iodine
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/ingest/test_image_caption.py -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/ingest/image_caption.py tests/ingest/test_image_caption.py
git commit -m "feat: add image stage mapping and template caption"
```

---

### Task 7: Build field/text/image index pipeline (M2)

**Files:**
- Create: `src/rag/index/field_index.py`
- Create: `src/rag/index/vector_index.py`
- Create: `src/rag/index/build_index.py`
- Test: `tests/index/test_build_index.py`

**Step 1: Write the failing test**

```python
from rag.index.build_index import rebuild_index


def test_rebuild_index_returns_stats():
    stats = rebuild_index("example-data", ".rag_index")
    assert stats["cases"] == 4
    assert stats["field_docs"] > 0
    assert stats["text_docs"] > 0
    assert stats["image_docs"] > 0
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/index/test_build_index.py::test_rebuild_index_returns_stats -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- parse cases
- write index artifacts
- return deterministic stats
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/index/test_build_index.py::test_rebuild_index_returns_stats -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/index/field_index.py src/rag/index/vector_index.py src/rag/index/build_index.py tests/index/test_build_index.py
git commit -m "feat: add index build pipeline"
```

---

### Task 8: Implement retrieval and case rerank (M2)

**Files:**
- Create: `src/rag/retrieval/retrieve.py`
- Create: `src/rag/retrieval/rerank.py`
- Test: `tests/retrieval/test_rerank.py`

**Step 1: Write the failing test**

```python
from rag.retrieval.rerank import rerank_cases


def test_rerank_cases_aggregates_three_channels():
    merged = rerank_cases(
        field_hits=[{"case_id": "A", "score": 0.9}],
        text_hits=[{"case_id": "A", "score": 0.5}],
        image_hits=[{"case_id": "B", "score": 0.8}],
    )
    assert merged[0]["case_id"] == "A"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/retrieval/test_rerank.py::test_rerank_cases_aggregates_three_channels -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- score_case = 0.45*field + 0.40*text + 0.15*image
- return sorted merged list
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/retrieval/test_rerank.py::test_rerank_cases_aggregates_three_channels -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/retrieval/retrieve.py src/rag/retrieval/rerank.py tests/retrieval/test_rerank.py
git commit -m "feat: add retrieval and case rerank"
```

---

### Task 9: Implement LangGraph workflow contract (M2)

**Files:**
- Create: `src/rag/workflow/state.py`
- Create: `src/rag/workflow/graph.py`
- Test: `tests/workflow/test_graph_contract.py`

**Step 1: Write the failing test**

```python
from rag.workflow.graph import run_rag


def test_run_rag_returns_contract_keys():
    out = run_rag("HPV16相关病例有哪些证据？")
    for k in ["question", "answer", "evidence", "sources", "confidence", "limits", "trace_id"]:
        assert k in out
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/workflow/test_graph_contract.py::test_run_rag_returns_contract_keys -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- define RagState
- wire graph nodes
- call retrieval + rerank
- compose json contract
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/workflow/test_graph_contract.py::test_run_rag_returns_contract_keys -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/workflow/state.py src/rag/workflow/graph.py tests/workflow/test_graph_contract.py
git commit -m "feat: add langgraph workflow contract"
```

---

### Task 10: Wire CLI `index` and `ask` to services (M2)

**Files:**
- Modify: `src/rag/cli.py`
- Test: `tests/cli/test_cli_index_and_ask.py`

**Step 1: Write the failing test**

```python
import subprocess
import sys


def test_cli_index_and_ask_roundtrip():
    idx = subprocess.run(
        [sys.executable, "-m", "rag.cli", "index", "--data-dir", "example-data"],
        capture_output=True,
        text=True,
    )
    assert idx.returncode == 0
    ask = subprocess.run(
        [sys.executable, "-m", "rag.cli", "ask", "HSIL证据"],
        capture_output=True,
        text=True,
    )
    assert ask.returncode == 0
    assert "\"evidence\"" in ask.stdout
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/cli/test_cli_index_and_ask.py::test_cli_index_and_ask_roundtrip -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- index --data-dir
- ask "<question>" --top-k --label-filter --json-pretty
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/cli/test_cli_index_and_ask.py::test_cli_index_and_ask_roundtrip -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/cli.py tests/cli/test_cli_index_and_ask.py
git commit -m "feat: connect cli index and ask"
```

---

### Task 11: Add RAGAS dataset builder and runner (M3)

**Files:**
- Create: `src/rag/eval/dataset_builder.py`
- Create: `src/rag/eval/ragas_runner.py`
- Test: `tests/eval/test_ragas_runner_contract.py`

**Step 1: Write the failing test**

```python
from rag.eval.ragas_runner import run_eval


def test_run_eval_returns_metric_keys():
    out = run_eval(dataset_path="eval/dataset.jsonl")
    for k in ["context_precision", "context_recall", "faithfulness", "answer_relevancy", "pass_gate"]:
        assert k in out
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/eval/test_ragas_runner_contract.py::test_run_eval_returns_metric_keys -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- build question/reference/context dataset from TXT/PDF
- run ragas metric suite
- return normalized metric dict
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/eval/test_ragas_runner_contract.py::test_run_eval_returns_metric_keys -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/eval/dataset_builder.py src/rag/eval/ragas_runner.py tests/eval/test_ragas_runner_contract.py
git commit -m "feat: add ragas dataset and runner"
```

---

### Task 12: Add hard gate and diagnostic report (M3)

**Files:**
- Create: `src/rag/eval/gate.py`
- Modify: `src/rag/cli.py`
- Test: `tests/eval/test_gate_thresholds.py`

**Step 1: Write the failing test**

```python
from rag.eval.gate import check_gate


def test_gate_fails_when_any_metric_below_threshold():
    metrics = {
        "context_precision": 0.8,
        "context_recall": 0.7,
        "faithfulness": 0.79,
        "answer_relevancy": 0.9,
    }
    out = check_gate(metrics)
    assert out["pass_gate"] is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/eval/test_gate_thresholds.py::test_gate_fails_when_any_metric_below_threshold -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
thresholds:
- context_precision >= 0.70
- context_recall >= 0.70
- faithfulness >= 0.80
- answer_relevancy >= 0.75
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/eval/test_gate_thresholds.py::test_gate_fails_when_any_metric_below_threshold -v`  
Expected: PASS.

**Step 5: Commit**

```bash
git add src/rag/eval/gate.py src/rag/cli.py tests/eval/test_gate_thresholds.py
git commit -m "feat: enforce ragas hard gate"
```

---

### Task 13: End-to-end regression and docs sync (M4)

**Files:**
- Create: `tests/e2e/test_minimal_e2e.py`
- Modify: `README.md`
- Modify: `docs/plans/progress-board.md`
- Modify: `docs/plans/session-handoff.md`

**Step 1: Write the failing test**

```python
def test_placeholder_e2e():
    assert False, "replace with real e2e command-level check"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/e2e/test_minimal_e2e.py::test_placeholder_e2e -v`  
Expected: FAIL.

**Step 3: Write minimal implementation**

```text
- run index rebuild
- run ask sample query
- run eval and check gate status
```

**Step 4: Run full tests**

Run: `pytest -v`  
Expected: PASS for all enabled tests.

**Step 5: Commit**

```bash
git add tests/e2e/test_minimal_e2e.py README.md docs/plans/progress-board.md docs/plans/session-handoff.md
git commit -m "test: add e2e regression and sync execution docs"
```

---

## Acceptance Criteria
1. 新会话无需额外提问即可选择并执行下一个任务。
2. 每个任务都有清晰的失败/通过验证命令。
3. 所有阈值、命令、路径可直接复制执行。
4. 任务状态和交接记录保持同步。

## Defaults Locked
1. RAGAS 门禁阈值固定为 `0.70/0.70/0.80/0.75`。
2. 评估模型通过 OpenAI-compatible 接口接入。
3. 技术栈基线是 `langchain>=1.0`。
4. 当前只支持 `example-data` 的目录模式。

