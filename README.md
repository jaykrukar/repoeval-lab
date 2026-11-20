# RepoEval Lab

[![Tests](https://github.com/jaykrukar/repoeval-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/jaykrukar/repoeval-lab/actions/workflows/tests.yml)

A **small, working evaluation harness** for repository-style Python coding challenges: task manifests, immutable external tests, candidate submissions, result reporting, and timeouts.

> Portfolio prototype. **Not** a security sandbox, production RL environment, or evidence of previous contract experience. The runner executes candidate code. Only test trusted code on your host or use a properly isolated external container.

## Quick start

```bash
python -m pip install -e '.[dev]'
python -m repoeval examples/order-reservation/manifest.json examples/order-reservation/starter --json
# Expected: JSON report with passed=false
python -m repoeval examples/order-reservation/manifest.json examples/order-reservation/solution --json
# Expected: JSON report with passed=true
python -m pytest -q
```

## How it works

1. A JSON manifest identifies a task, an **external verifier**, and a timeout.
2. A candidate code directory is placed ahead of the verifier on Python's import path.
3. pytest runs as a subprocess with a timeout and produces a JUnit report.
4. The result captures pass/fail, test counts, and bounded debug output in JSON.

See [example verification outcomes](docs/verification_results.json): starter rejected, reference accepted.

## Files

- `src/repoeval/runner.py` — manifest validation, subprocess isolation **of execution only**, timeout handling, JUnit parsing.
- `src/repoeval/cli.py` — CLI and JSON reporting.
- `examples/order-reservation/` — original demo challenge with buggy starter, reference solution, and verifier that accepts alternative correct solutions.
- `tests/` — tests of the harness itself.

## Design decisions and limitations

- External tests prevent accidental coupling to the reference solution.
- JSON reports are easy to analyze in downstream evaluation systems.
- We do not attempt to evaluate untrusted code safely: **timeouts cannot prevent malicious filesystem, network, or resource behavior**. For such tasks add real container sandboxing, resource limits, and strict isolation.
- pytest import paths support small self-contained Python challenges. Multi-file repos and multi-language execution need explicit adapter implementations.
- Original challenge is a demonstration, not claimed to be exclusive or unknown to any online judge.

## Next improvements

Implement container-backed executors, test mutation scoring, verifier quality audits, and a task corpus with carefully reviewed specifications.

## Provenance

Initial portfolio implementation prepared with AI assistance. Review, run, understand, and extend the code before describing it as your independent engineering experience.

License: MIT.
