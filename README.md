# RepoEval Lab

[![Tests](https://github.com/jaykrukar/repoeval-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/jaykrukar/repoeval-lab/actions/workflows/tests.yml)

A **small, working evaluation harness** for repository-style Python coding challenges: task manifests, external tests, candidate submissions, structured results, and timeouts. The included corpus has two independently specified tasks.

The repository now also includes a **Coding Evaluation Task Authoring Kit**: a CLI scaffold (`repoeval init`), a known-outcome preflight (`repoeval audit`), editable task/review templates, and a worked example. The audit verifies package mechanics only; human review is still required.

> Portfolio prototype. **Not** a security sandbox, production RL environment, or evidence of previous contract experience. The runner executes candidate code. Only test trusted code on your host or use a properly isolated external container.

## Quick start

```bash
python -m pip install -e '.[dev]'
repoeval init normalize-tags --output ./my-task
repoeval audit ./my-task --json
python -m repoeval examples/order-reservation/manifest.json examples/order-reservation/starter --json
# Expected: JSON report with passed=false
python -m repoeval examples/order-reservation/manifest.json examples/order-reservation/solution --json
# Expected: JSON report with passed=true
python -m repoeval examples/retry-after/manifest.json examples/retry-after/solution
python -m pytest -q
```

## How it works

1. A JSON manifest identifies a task, an **external verifier**, and a timeout.
2. A candidate code directory is placed ahead of the verifier on Python's import path.
3. pytest runs as a subprocess with a timeout and produces a JUnit report.
4. The result captures pass/fail, test counts, elapsed wall time, timeout state, and bounded debug output in JSON. An all-skipped verifier is not accepted as a pass.

See [example verification outcomes](docs/verification_results.json): starter rejected, reference accepted.

## Files

- `src/repoeval/runner.py` — manifest validation, subprocess isolation **of execution only**, timeout handling, JUnit parsing.
- `src/repoeval/cli.py` — CLI and JSON reporting.
- `src/repoeval/taskkit.py` — safe task scaffolding and reference/starter preflight report.
- `src/repoeval/task_template/` — packaged default prompt, reference, starter, and verifier.
- `examples/order-reservation/` — original demo challenge with buggy starter, reference solution, and verifier that accepts alternative correct solutions.
- `examples/retry-after/` — an HTTP field parsing task with boundary cases for delay-seconds, date formats, time zones, and rounding.
- `products/task-authoring-kit/` — reusable authoring workflow, checklists, worksheets, and a complete worked task.
- `tests/` — tests of the harness itself.

## Design decisions and limitations

- External tests prevent accidental coupling to the reference solution.
- JSON reports are easy to analyze in downstream evaluation systems.
- The harness disables pytest auto-loaded third-party plugins and removes shell-provided pytest option overrides for each task run.
- Reported duration is wall-clock time around the verifier subprocess; it is not CPU time or a resource limit.
- We do not attempt to evaluate untrusted code safely: **timeouts cannot prevent malicious filesystem, network, or resource behavior**. For such tasks add real container sandboxing, resource limits, and strict isolation.
- The current runner uses pytest and is limited to Python tasks. Other test frameworks and languages need explicit executor adapters.
- `repoeval audit` checks the prompt file exists, the reference passes, and the starter is rejected. It does not score clarity, solvability, fairness, test completeness, or benchmark value.
- Original challenge is a demonstration, not claimed to be exclusive or unknown to any online judge.

The retry-after task is an original portfolio exercise informed by HTTP date syntax. It is not a claim of benchmark novelty. Each verifier measures the tested contract only; it does not establish broad correctness, security, or real-world model capability.

## Next improvements

Implement container-backed executors, test mutation scoring, verifier quality audits, and a task corpus with carefully reviewed specifications.

Build a deterministic downloadable bundle with `python tools/build_authoring_kit.py`. The market listing draft and its unvalidated price hypothesis are kept separate in `launch-assets/` and excluded from customer downloads.

## Provenance

Initial portfolio implementation prepared with AI assistance. Review, run, understand, and extend the code before describing it as your independent engineering experience.

License: MIT.
