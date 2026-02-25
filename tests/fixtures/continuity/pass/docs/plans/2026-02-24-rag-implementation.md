# RAG Phase 1 Implementation Plan

### Task 1: Bootstrap package and CLI skeleton (M1)

**Step 1: Write the failing test**
Create `tests/cli/test_cli_help.py`.

**Step 2: Run test to verify it fails**
Run: `python -m pytest tests/cli/test_cli_help.py::test_cli_help_shows_commands -v`

**Step 3: Write minimal implementation**
Create `src/rag/cli.py` with `index` / `ask` / `eval` commands.

**Step 4: Run test to verify it passes**
Run: `python -m pytest tests/cli/test_cli_help.py::test_cli_help_shows_commands -v`

**Step 5: Commit**
Run: `git commit -m "chore: bootstrap rag package and cli skeleton"`
