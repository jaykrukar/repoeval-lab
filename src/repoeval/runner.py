"""Run an externally supplied pytest verifier against a candidate repository.

WARNING: The runner executes arbitrary Python code. Timeouts are *not* a security
boundary. Run only trusted submissions or use a real sandbox/container.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class VerificationResult:
    task_id: str
    passed: bool
    exit_code: int | None
    tests: int
    failures: int
    errors: int
    skipped: int
    timed_out: bool
    duration_seconds: float
    output: str

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, sort_keys=True)


def load_manifest(path: Path) -> dict:
    """Validate an intentionally small, auditable manifest schema."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Manifest must be a JSON object")
    if not isinstance(data.get("task_id"), str) or not data["task_id"].strip():
        raise ValueError("Manifest requires a nonempty task_id")
    if not isinstance(data.get("test_file"), str) or not data["test_file"].strip():
        raise ValueError("Manifest requires a nonempty test_file")
    timeout = data.get("timeout_seconds", 15)
    if type(timeout) is not int or not 1 <= timeout <= 300:
        raise ValueError("timeout_seconds must be an integer from 1 to 300")
    task_root = path.parent.resolve()
    for key in ("test_file", "prompt_file"):
        value = data.get(key)
        if value is None and key == "prompt_file":
            continue
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a nonempty relative path")
        target = (path.parent / value).resolve()
        if not target.is_file() or not target.is_relative_to(task_root):
            raise ValueError(f"{key} must identify a file inside the manifest directory")
    for key in ("starter_dir", "solution_dir"):
        if key not in data:
            continue
        value = data[key]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} must be a nonempty relative path")
        target = (path.parent / value).resolve()
        if not target.is_dir() or not target.is_relative_to(task_root):
            raise ValueError(f"{key} must identify a directory inside the manifest directory")
    data["timeout_seconds"] = timeout
    return data


def _junit_counts(xml: Path) -> tuple[int, int, int, int]:
    if not xml.exists():
        return (0, 0, 0, 0)
    root = ET.parse(xml).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    if suite is None:
        return (0, 0, 0, 0)
    return tuple(int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped"))


def verify(manifest_path: str | Path, candidate_dir: str | Path) -> VerificationResult:
    manifest_path = Path(manifest_path).resolve()
    candidate_dir = Path(candidate_dir).resolve()
    if not candidate_dir.is_dir():
        raise ValueError(f"Candidate directory not found: {candidate_dir}")
    manifest = load_manifest(manifest_path)
    verifier = (manifest_path.parent / manifest["test_file"]).resolve()
    env = dict(os.environ)
    # Explicitly prioritize submitted source over modules from the verifier location.
    inherited_pythonpath = env.pop("PYTHONPATH", "")
    env["PYTHONPATH"] = os.pathsep.join(
        part for part in (str(candidate_dir), inherited_pythonpath) if part
    )
    # Do not let shell configuration silently add tests or plugins to a task run.
    env.pop("PYTEST_ADDOPTS", None)
    env.pop("PYTEST_PLUGINS", None)
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    with tempfile.TemporaryDirectory(prefix="repoeval-") as tmp:
        junit = Path(tmp) / "results.xml"
        command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
                   str(verifier), f"--junitxml={junit}"]
        started = time.monotonic()
        try:
            result = subprocess.run(
                command, cwd=candidate_dir, env=env, capture_output=True,
                text=True, timeout=manifest["timeout_seconds"], check=False,
            )
            duration = round(time.monotonic() - started, 6)
            try:
                counts = _junit_counts(junit)
            except (ET.ParseError, OSError, ValueError) as exc:
                return VerificationResult(
                    task_id=manifest["task_id"], passed=False,
                    exit_code=result.returncode, tests=0, failures=0,
                    errors=1, skipped=0, timed_out=False,
                    duration_seconds=duration,
                    output=(result.stdout + "\n" + result.stderr +
                            f"\nInvalid JUnit report: {exc}")[-8000:].strip(),
                )
            output = (result.stdout + "\n" + result.stderr)[-8000:].strip()
            return VerificationResult(
                task_id=manifest["task_id"],
                passed=(result.returncode == 0 and counts[0] > counts[3]),
                exit_code=result.returncode, tests=counts[0], failures=counts[1],
                errors=counts[2], skipped=counts[3], timed_out=False,
                duration_seconds=duration, output=output,
            )
        except subprocess.TimeoutExpired as exc:
            duration = round(time.monotonic() - started, 6)
            partial = exc.stdout or b""
            partial_err = exc.stderr or b""
            if isinstance(partial, bytes):
                partial = partial.decode("utf-8", errors="replace")
            if isinstance(partial_err, bytes):
                partial_err = partial_err.decode("utf-8", errors="replace")
            return VerificationResult(
                task_id=manifest["task_id"], passed=False, exit_code=None,
                tests=0, failures=0, errors=0, skipped=0, timed_out=True,
                duration_seconds=duration,
                output=(str(partial) + "\n" + str(partial_err) +
                        "\nVerification timed out; no result accepted.")[-8000:].strip(),
            )
