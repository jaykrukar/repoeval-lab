import json
from pathlib import Path

import pytest

from repoeval.cli import main
from repoeval.taskkit import audit_task, create_task


def test_create_and_audit_task_template(tmp_path):
    task_dir = create_task("normalize-tags", tmp_path / "normalize-tags")
    manifest = json.loads((task_dir / "manifest.json").read_text())
    assert manifest["task_id"] == "normalize-tags"
    result = audit_task(task_dir)
    assert result["ready_for_human_review"]
    assert result["reference"]["tests"] == 18
    assert not result["starter"]["passed"]


def test_cli_init_and_audit(tmp_path, capsys):
    target = tmp_path / "cli-task"
    assert main(["init", "normalize-tags", "--output", str(target)]) == 0
    assert "Created task workspace" in capsys.readouterr().out
    assert main(["audit", str(target), "--json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["ready_for_human_review"]


def test_legacy_verify_invocation_remains_supported(capsys):
    root = Path(__file__).resolve().parents[1]
    assert main([
        str(root / "examples/order-reservation/manifest.json"),
        str(root / "examples/order-reservation/solution"),
    ]) == 0
    assert "PASS" in capsys.readouterr().out


@pytest.mark.parametrize("task_id", ["../escape", "Uppercase", "two--hyphens", "white space"])
def test_invalid_task_id_is_rejected(task_id, tmp_path):
    with pytest.raises(ValueError, match="task_id"):
        create_task(task_id, tmp_path / "output")


def test_create_never_overwrites_existing_directory(tmp_path):
    target = tmp_path / "existing"
    target.mkdir()
    (target / "keep.txt").write_text("preserve me")
    with pytest.raises(FileExistsError):
        create_task("safe-task", target)
    assert (target / "keep.txt").read_text() == "preserve me"


def test_audit_fails_if_reference_is_broken(tmp_path):
    from repoeval.taskkit import create_task

    task_dir = create_task("normalize-tags", tmp_path / "normalize-tags")
    (task_dir / "solution/tag_normalizer.py").write_text("def broken(:\n")
    report = audit_task(task_dir)
    assert not report["ready_for_human_review"]
    assert not report["checks"]["reference_passes"]
