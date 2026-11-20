import json
from pathlib import Path
import pytest
from repoeval.runner import load_manifest, verify

EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "order-reservation"


def test_reference_solution_passes():
    result = verify(EXAMPLE / "manifest.json", EXAMPLE / "solution")
    assert result.passed, result.output
    assert result.tests >= 15
    assert result.failures == 0
    assert json.loads(result.to_json())["passed"] is True


def test_starter_solution_fails():
    result = verify(EXAMPLE / "manifest.json", EXAMPLE / "starter")
    assert not result.passed
    assert result.failures + result.errors >= 1


def test_invalid_manifest(tmp_path):
    p = tmp_path / "manifest.json"
    p.write_text('{"task_id":"x", "test_file":"../../etc/passwd"}')
    with pytest.raises(ValueError):
        load_manifest(p)


def test_missing_candidate():
    with pytest.raises(ValueError, match="Candidate directory not found"):
        verify(EXAMPLE / "manifest.json", EXAMPLE / "not-a-directory")
