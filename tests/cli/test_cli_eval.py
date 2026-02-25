import json
import os
import subprocess
import sys
from pathlib import Path


def _run_eval_command(dataset_path: Path, index_dir: Path) -> subprocess.CompletedProcess[str]:
    project_root = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PYTHONPATH": str(project_root / "src")}
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "rag.cli",
            "eval",
            "--dataset-path",
            str(dataset_path),
            "--index-dir",
            str(index_dir),
            "--data-dir",
            "example-data",
        ],
        capture_output=True,
        text=True,
        env=env,
    )


def test_cli_eval_exits_non_zero_when_gate_fails(tmp_path):
    dataset_path = tmp_path / "dataset-fail.jsonl"
    dataset_path.write_text(
        json.dumps(
            {
                "question": "definitely-not-in-the-documents",
                "reference": "missing-reference",
                "contexts": ["missing-reference"],
                "case_id": "X",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    proc = _run_eval_command(dataset_path=dataset_path, index_dir=tmp_path / "idx-fail")

    assert proc.returncode == 1
    output = json.loads(proc.stdout)
    assert output["pass_gate"] is False


def test_cli_eval_exits_zero_when_gate_passes(tmp_path):
    dataset_path = tmp_path / "dataset-pass.jsonl"
    dataset_path.write_text(
        json.dumps(
            {
                "question": "",
                "reference": "any-reference",
                "contexts": ["any-reference"],
                "case_id": "Y",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    proc = _run_eval_command(dataset_path=dataset_path, index_dir=tmp_path / "idx-pass")

    assert proc.returncode == 0
    output = json.loads(proc.stdout)
    assert output["pass_gate"] is True
