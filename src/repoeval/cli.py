"""Command-line interface for task authoring and deterministic verification."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .runner import verify
from .taskkit import audit_task, create_task


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="repoeval",
        description="Scaffold, preflight, and verify repository-style Python coding tasks.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    verify_parser = commands.add_parser("verify", help="run an external verifier on a candidate")
    verify_parser.add_argument("manifest", type=Path, help="Path to task manifest.json")
    verify_parser.add_argument("candidate", type=Path, help="Path to candidate code directory")
    verify_parser.add_argument("--json", action="store_true", help="Emit structured JSON")

    init_parser = commands.add_parser("init", help="scaffold a new task authoring workspace")
    init_parser.add_argument("task_id", help="lowercase task slug, such as normalize-tags")
    init_parser.add_argument("--output", type=Path, help="destination directory (default: ./<task_id>)")

    audit_parser = commands.add_parser("audit", help="check a task package and known starter/reference outcomes")
    audit_parser.add_argument("task_dir", type=Path, help="Task directory created from the authoring template")
    audit_parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    return parser


def _legacy_verify_args(argv: list[str]) -> list[str]:
    """Keep the original `repoeval MANIFEST CANDIDATE` invocation working."""
    if argv and argv[0] not in {"verify", "init", "audit", "-h", "--help"}:
        return ["verify", *argv]
    return argv


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = _parser()
    args = parser.parse_args(_legacy_verify_args(argv))
    try:
        if args.command == "init":
            destination = args.output or Path.cwd() / args.task_id
            created = create_task(args.task_id, destination)
            print(f"Created task workspace: {created}")
            print("Next: edit CHALLENGE.md and starter/, then run `repoeval audit <path>`. ")
            return 0
        if args.command == "audit":
            result = audit_task(args.task_dir)
            if args.json:
                print(json.dumps(result, indent=2, sort_keys=True))
            else:
                state = "READY FOR HUMAN REVIEW" if result["ready_for_human_review"] else "NEEDS WORK"
                print(f"Task: {result['task_id']} | {state}")
                for name, passed in result["checks"].items():
                    print(f"{'PASS' if passed else 'FAIL'} {name}")
                print(result["scope_note"])
            return 0 if result["ready_for_human_review"] else 1

        result = verify(args.manifest, args.candidate)
    except (FileExistsError, ValueError, OSError) as exc:
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
