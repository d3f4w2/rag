import os
import subprocess
import sys
from pathlib import Path


def test_cli_index_and_ask_roundtrip():
    project_root = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(project_root / "src")}

    idx = subprocess.run(
        [sys.executable, "-m", "rag.cli", "index", "--data-dir", "example-data"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert idx.returncode == 0

    ask = subprocess.run(
        [sys.executable, "-m", "rag.cli", "ask", "HSIL evidence"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert ask.returncode == 0
    assert '"evidence"' in ask.stdout
