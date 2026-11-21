# Coding Evaluation Task Authoring Kit

A practical starter pack for writing, testing, and reviewing small Python coding tasks. It combines an editable task brief, test-design worksheet, verifier audit checklist, and a worked example that can be run with RepoEval.

## Who it is for

- People building coding tasks for AI evaluations, learning exercises, or take-home practice.
- Reviewers who need a repeatable checklist for prompt, verifier, and known-solution quality.
- Educators who want a small Python task that students can run and inspect.

## What is included

- `guide/authoring-workflow.md` — step-by-step task design workflow.
- `templates/task-brief.md` — prompt and acceptance-criteria worksheet.
- `templates/test-matrix.csv` — blank test-case coverage matrix.
- `templates/review-scorecard.csv` — evidence-based manual quality review sheet.
- `checklists/verifier-review.md` — independent-oracle and false-pass review.
- `example/` — complete tag-normalization task with prompt, starter, reference, and 18 tests.
- The RepoEval CLI, which can scaffold another package and verify reference/starter behavior.

## Included license files

The guide, checklists, and blank templates are CC BY 4.0. The software and worked code example use the repository's MIT license. A buyer or redistributor must keep the notices included in the bundle.

## Quick start

From the extracted repository directory, install Python 3.10+ and run:

```bash
python -m pip install -e '.[dev]'
repoeval init normalize-tags --output ./my-first-task
repoeval audit ./my-first-task --json
```

The audit is a preflight check. It confirms expected files are present, the reference implementation passes, and the intentionally incomplete starter is rejected. A successful audit means **ready for human review**, not fair, complete, secure, or benchmark-worthy.

## Run the example

```bash
repoeval audit products/task-authoring-kit/example
repoeval verify products/task-authoring-kit/example/manifest.json \
  products/task-authoring-kit/example/solution
```

## What this kit does not claim

- It does not establish whether a task is novel, representative, or useful for a particular evaluation.
- It does not automatically judge prompt clarity, human solvability, fairness, or test completeness.
- RepoEval does not sandbox untrusted code. Its subprocess timeout is not a security boundary. Do not run unknown submissions on a computer with data or credentials you need to protect.
- It is a learning and authoring aid, not a substitute for domain-expert review.

## Licensing

The RepoEval software and code examples are MIT licensed. The guide and blank templates in this kit are licensed CC BY 4.0. The worked task and its tests are also MIT licensed. Preserve the notices when redistributing. You may adapt these materials for commercial use; do not present the author's work or results as your own.

## Version

Kit version 1.0.0. Feedback and verified improvements should be tracked through the repository issue tracker.
