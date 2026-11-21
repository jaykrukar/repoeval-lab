from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_authoring_kit import build_bundle  # noqa: E402


def test_bundle_has_expected_content_and_is_reproducible(tmp_path):
    first = build_bundle(tmp_path / "first.zip")
    second = build_bundle(tmp_path / "second.zip")
    assert first.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(first) as archive:
        names = set(archive.namelist())
    prefix = "repoeval-task-authoring-kit/"
    assert prefix + "products/task-authoring-kit/README.md" in names
    assert prefix + "products/task-authoring-kit/example/checks/test_task.py" in names
    assert prefix + "src/repoeval/taskkit.py" in names
    assert not any(".git/" in name or "__pycache__" in name for name in names)


def test_bundle_does_not_include_unrelated_launch_copy(tmp_path):
    bundle = build_bundle(tmp_path / "kit.zip")
    with zipfile.ZipFile(bundle) as archive:
        assert not any("launch-assets" in name for name in archive.namelist())
