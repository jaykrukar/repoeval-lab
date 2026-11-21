"""Command-line interface: repoeval verify MANIFEST CANDIDATE [--json]."""
import argparse
from pathlib import Path
from .runner import verify


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate a candidate code directory with external tests.")
    parser.add_argument("manifest", type=Path, help="Path to task manifest.json")
    parser.add_argument("candidate", type=Path, help="Path to code under evaluation")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args(argv)
    try:
        result = verify(args.manifest, args.candidate)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    if args.json:
        print(result.to_json())
    else:
        print(f"Task: {result.task_id} | {'PASS' if result.passed else 'FAIL'} | "
              f"tests={result.tests} failures={result.failures} errors={result.errors} "
              f"skipped={result.skipped} duration={result.duration_seconds:.3f}s "
              f"timeout={result.timed_out}")
        if not result.passed:
            print(result.output)
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
