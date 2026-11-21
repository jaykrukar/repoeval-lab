# Verifier review checklist

Review each item and record evidence. “Yes” should mean you inspected the relevant artifact or run; it should not be inferred from the reference passing.

## Contract alignment

- [ ] Every assertion maps to a written requirement.
- [ ] The prompt and tests use the same definitions and edge-case behavior.
- [ ] Tests check observable outcomes rather than private implementation details.

## Test coverage

- [ ] Normal examples are covered.
- [ ] Boundary and empty inputs are covered where relevant.
- [ ] Invalid types or malformed input are covered where specified.
- [ ] Important invariants and side effects are checked.
- [ ] Test names and failure messages make the expected behavior clear.

## Oracle quality

- [ ] Test expectations were derived from the contract independently of the reference code.
- [ ] At least one alternative correct implementation was attempted.
- [ ] A plausible incorrect shortcut is rejected by a meaningful assertion.
- [ ] The starter fails for a task-behavior reason, not only a setup or import error.
- [ ] Tests are deterministic and do not depend on network access, wall-clock time, or ambient machine state unless explicitly required.

## Reproducibility and safety

- [ ] Runtime and dependency versions are documented.
- [ ] The command and setup work from a clean checkout.
- [ ] Timeouts and output limits are documented accurately.
- [ ] Untrusted candidate execution happens only inside a real, appropriately configured sandbox.

## Human review

- [ ] A reviewer can solve from the prompt without access to the reference implementation.
- [ ] The review records confusing or missing instructions.
- [ ] The task's limitations, intended audience, and AI assistance are disclosed.

Record exceptions and evidence in `review-scorecard.csv`. This checklist is a prompt for review, not a certification.
