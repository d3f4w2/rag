from pathlib import Path


def test_dependency_files_exist():
    assert Path("environment.yml").exists()
    assert Path("requirements/core.txt").exists()
    assert Path("requirements/eval.txt").exists()
    assert Path("requirements/dev.txt").exists()


def test_core_requirements_include_cli_runtime():
    lines = {
        line.strip()
        for line in Path("requirements/core.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
    assert "typer" in lines
