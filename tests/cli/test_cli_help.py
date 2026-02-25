import os
import subprocess
import sys
from pathlib import Path


def test_cli_help_shows_commands():
    project_root = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(project_root / "src")}
    proc = subprocess.run(
        [sys.executable, "-m", "rag.cli", "--help"],
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 0
    assert "index" in proc.stdout
    assert "ask" in proc.stdout
    assert "eval" in proc.stdout
