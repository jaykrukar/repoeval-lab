# A practical workflow for authoring coding tasks

Use this sequence for one small, deterministic task. Keep each decision reviewable.

## 1. Choose one observable skill

Write down the behavior a candidate should implement. Avoid combining unrelated API design, architecture, and debugging work in one short task. State what a correct result looks like before writing tests.

## 2. Draft the contract before the code

Specify inputs, outputs, side effects, errors, boundary behavior, and what is intentionally out of scope. Use a few concrete examples. If an example and a rule disagree, fix the task brief before proceeding.

## 3. Check that a person can solve it

Ask a reviewer who has not seen the reference solution to implement from the brief alone. Record confusing language and missing assumptions. A reference solution passing its own tests does not prove the prompt is clear.

## 4. Build an independent test oracle

Derive assertions from the written contract, not from the reference implementation. Cover normal behavior, boundaries, malformed or unusual inputs, and invariants. Review tests for accidental dependence on implementation details.

## 5. Run known implementations

The reference solution should pass. The deliberately incomplete starter should fail at least one meaningful assertion. Inspect the failures: a syntax error or broken import can make the starter fail without showing that the tests detect the intended behavior.

## 6. Try alternative correct implementations

Have a reviewer implement the task using a different reasonable approach. Check that the verifier accepts it. If it does not, determine whether the contract or verifier is too narrow.

## 7. Review false passes and false failures

Try empty values, boundary values, unrelated extra files, and common shortcuts. Then read the verifier as if you were trying to pass without implementing the contract. Add tests only when they follow from the written requirements.

## 8. Make the run reproducible

Pin the language/runtime expectations, dependencies, setup commands, timeout, and exact verifier command. Keep candidate code separate from verifier code. Save a machine-readable result but include human-readable instructions too.

## 9. Get independent review before publishing

Use the checklist and scorecard, then ask someone else to review clarity, correctness, accessibility, and whether the task is solvable as written. Treat the CLI audit as a gate for package mechanics only.

## Suggested evidence to publish

- Task prompt, starter, reference, and verifier.
- Exact run commands and runtime/dependency versions.
- Reference pass and starter failure results.
- At least one independent implementation outcome.
- Known limitations and who reviewed the task.
- A note on any AI assistance used to draft or revise task materials.
