import json
from pathlib import Path
import pytest
from repoeval.runner import load_manifest, verify

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "order-reservation"
RETRY_AFTER = Path(__file__).resolve().parents[1] / "examples" / "retry-after"


def test_reference_solution_passes():
    result = verify(EXAMPLE / "manifest.json", EXAMPLE / "solution")
    assert result.passed, result.output
    assert result.tests >= 15
    assert result.failures == 0
    assert result.duration_seconds >= 0
    assert json.loads(result.to_json())["passed"] is True


def test_starter_solution_fails():
    result = verify(EXAMPLE / "manifest.json", EXAMPLE / "starter")
    assert not result.passed
    assert result.failures + result.errors >= 1


def test_second_challenge_reference_passes():
    result = verify(RETRY_AFTER / "manifest.json", RETRY_AFTER / "solution")
    assert result.passed, result.output
    assert result.tests == 20


def test_second_challenge_starter_fails():
    result = verify(RETRY_AFTER / "manifest.json", RETRY_AFTER / "starter")
    assert not result.passed
    assert result.failures + result.errors == result.tests


def test_invalid_manifest(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text('{"task_id":"x", "test_file":"../../etc/passwd"}')
    with pytest.raises(ValueError):
        load_manifest(p)


def test_missing_candidate():
    with pytest.raises(ValueError, match="Candidate directory not found"):
        verify(EXAMPLE / "manifest.json", EXAMPLE / "not-a-directory")


def test_all_skipped_verifier_is_not_a_pass(tmp_path):
    task = tmp_path / "task"
    task.mkdir()
    (task / "manifest.json").write_text(
        '{"task_id":"skip-only","test_file":"test_task.py"}'
    )
    (task / "test_task.py").write_text("import pytest\n\n@pytest.mark.skip\ndef test_nothing():\n    pass\n")
    candidate = tmp_path / "candidate"
    candidate.mkdir()
    result = verify(task / "manifest.json", candidate)
    assert result.tests == result.skipped == 1
    assert not result.passed


def test_timeout_is_reported_with_duration_and_output(tmp_path):
    task = tmp_path / "task"
    candidate = tmp_path / "candidate"
    task.mkdir()
    candidate.mkdir()
    (task / "manifest.json").write_text(
        '{"task_id":"slow","test_file":"test_task.py","timeout_seconds":1}'
    )
    (task / "test_task.py").write_text(
        "import time\n\ndef test_slow():\n    print('started')\n    time.sleep(2)\n"
    )
    result = verify(task / "manifest.json", candidate)
    assert result.timed_out
    assert not result.passed
    assert result.duration_seconds >= 1
    assert "timed out" in result.output


def test_shell_pytest_options_do_not_change_task(monkeypatch):
    monkeypatch.setenv("PYTEST_ADDOPTS", "--collect-only")
    result = verify(EXAMPLE / "manifest.json", EXAMPLE / "solution")
    assert result.passed
    assert result.tests > 0
