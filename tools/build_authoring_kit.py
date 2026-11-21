"""Build a deterministic ZIP bundle for the task-authoring kit."""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
KIT = "products/task-authoring-kit"
INCLUDE_FILES = ["LICENSE", "README.md", "pyproject.toml"]
INCLUDE_DIRS = ["docs", "examples", "src/repoeval", "tests", "tools", KIT]
EXCLUDED_PARTS = {"__pycache__", ".pytest_cache", ".git", "dist"}


def bundle_files() -> list[Path]:
    files = [ROOT / p for p in INCLUDE_FILES]
    for relative in INCLUDE_DIRS:
        files.extend((ROOT / relative).rglob("*"))
    return sorted(
        p for p in set(files)
        if p.is_file() and not any(part in EXCLUDED_PARTS for part in p.parts)
    )


def build_bundle(output: str | Path) -> Path:
    output = Path(output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    files = bundle_files()
    required = [
        ROOT / "pyproject.toml",
        ROOT / "src/repoeval/cli.py",
        ROOT / f"{KIT}/README.md",
        ROOT / f"{KIT}/example/manifest.json",
    ]
    missing = [path.relative_to(ROOT).as_posix() for path in required if path not in files]
    if missing:
        raise ValueError("Bundle is missing required files: " + ", ".join(missing))
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            relative = Path("repoeval-task-authoring-kit") / path.relative_to(ROOT)
            info = zipfile.ZipInfo(relative.as_posix(), date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o100644 & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/repoeval-task-authoring-kit-1.0.0.zip")
    args = parser.parse_args()
    result = build_bundle(args.output)
    print(f"Built {result} ({result.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
