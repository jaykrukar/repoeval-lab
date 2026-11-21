"""Task authoring helpers. These checks verify packaging and outcomes, not task quality."""
from __future__ import annotations

from importlib.resources import files
import json
from pathlib import Path
import re

from .runner import load_manifest, verify


_TASK_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def create_task(task_id: str, output: str | Path) -> Path:
    """Create a new task from the built-in starter template without overwriting files."""
    if not _TASK_ID.fullmatch(task_id):
        raise ValueError("task_id must use lowercase letters, digits, and single hyphens")
    destination = Path(output).expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"Output already exists; choose a new path: {destination}")

    template = files("repoeval").joinpath("task_template")

    def copy_tree(source, target: Path) -> None:
        for entry in source.iterdir():
            child = target / entry.name
            if entry.is_dir():
                child.mkdir()
                copy_tree(entry, child)
            else:
                contents = entry.read_bytes()
                if entry.name.endswith((".json", ".md", ".py")):
                    contents = contents.replace(b"__TASK_ID__", task_id.encode("ascii"))
                with child.open("xb") as output_file:
                    output_file.write(contents)

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    copy_tree(template, destination)
    return destination


def _result_summary(result) -> dict:
    return {
        "passed": result.passed,
        "tests": result.tests,
        "failures": result.failures,
        "errors": result.errors,
        "skipped": result.skipped,
        "timed_out": result.timed_out,
        "duration_seconds": result.duration_seconds,
    }


def audit_task(task_dir: str | Path) -> dict:
    """Check task structure and the expected reference-pass/starter-fail behavior."""
    root = Path(task_dir).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"Task directory not found: {root}")
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise ValueError("Task directory must contain manifest.json")
    manifest = load_manifest(manifest_path)
    starter = root / manifest.get("starter_dir", "starter")
    solution = root / manifest.get("solution_dir", "solution")
    prompt_file = root / manifest.get("prompt_file", "CHALLENGE.md")
    if not prompt_file.resolve().is_relative_to(root):
        raise ValueError("prompt_file must identify a file inside the task directory")
    if not starter.is_dir() or not starter.resolve().is_relative_to(root):
        raise ValueError("starter_dir must identify a directory inside the task directory")
    if not solution.is_dir() or not solution.resolve().is_relative_to(root):
        raise ValueError("solution_dir must identify a directory inside the task directory")
    reference_result = verify(manifest_path, solution)
    starter_result = verify(manifest_path, starter)
    structure = {
        "prompt_file": manifest.get("prompt_file", "CHALLENGE.md"),
        "test_file": manifest["test_file"],
        "starter_dir": manifest.get("starter_dir", "starter"),
        "solution_dir": manifest.get("solution_dir", "solution"),
    }
    return {
        "task_id": manifest["task_id"],
        "checks": {
            "prompt_present": prompt_file.is_file(),
            "reference_passes": reference_result.passed,
            "starter_is_rejected": not starter_result.passed,
            "verifier_has_executed_tests": reference_result.tests > 0,
        },
        "reference": _result_summary(reference_result),
        "starter": _result_summary(starter_result),
        "ready_for_human_review": all([
            prompt_file.is_file(),
            reference_result.passed,
            not starter_result.passed,
            reference_result.tests > 0,
        ]),
        "scope_note": (
            "This checks package structure and two known implementations only. "
            "It does not score prompt clarity, human solvability, test completeness, "
            "security, fairness, or benchmark value."
        ),
    }


def audit_json(task_dir: str | Path) -> str:
    return json.dumps(audit_task(task_dir), indent=2, sort_keys=True)
