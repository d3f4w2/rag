from pathlib import Path


def test_dependency_files_exist():
    assert Path("environment.yml").exists()
    assert Path("requirements/core.txt").exists()
    assert Path("requirements/eval.txt").exists()
    assert Path("requirements/dev.txt").exists()
