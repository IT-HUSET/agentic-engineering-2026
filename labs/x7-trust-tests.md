# X7 – Trust the tests

> **Skills:** `triage`, `testing` (`--mode prove-it`, `--mode strategy`)
> **Pull this when:** the suite cannot be trusted, a bug has an unknown cause, or a story went `done` on weak proof. Playbook background: §11.

## Trigger

Pull X7 when one of these is a fact in your repo or artifacts:

- **An unreliable suite.** Tests that fail on a rerun with no change, a suite red on the default branch, or a team habit of "rerun it".
- **A bug whose cause you do not know.** A failing check, a regression, or a symptom you cannot reproduce on demand.
- **Weak evidence.** A `verified.summary` in `plan.json` that records only an exit code, a scenario whose test would still pass with the behavior removed, or a `done` story you cannot explain a proof for.
- **No testing strategy.** Nothing in `docs/TESTING-STRATEGY.md` says which levels you use or what must be green before merge.

## Input

Your own suite and `plan.json`. If you have none of these problems yet, use the `todo-app/` suite (`uv run pytest`) and the authorization rule from F6: a recipient of a view-only list must not be able to change it.

## Output

- A list of your story proofs graded as *protects the behavior* or *does not*.
- For a bug: a failing test that reproduces it, then the root-cause fix, checked against the original symptom.
- Optionally `docs/TESTING-STRATEGY.md`.

## Steps

1. **Manual once: break it to see if the test notices.** A test protects a behavior only if removing the behavior turns it red. For three scenarios from your FIS files or `plan.json` rows:
   - Read the `verified.summary`. It should quote a command, its exit status and the runner's own result line. An exit code alone records that something ran, not what it found.
   - On a scratch branch (`git switch -c scratch/falsify`), remove or break the behavior that scenario protects. Run the named test.
   - Red: it protects the behavior. Green: the test is **tautological** (its expected value comes from the code under test), **vacuous** (it never runs, or checks nothing a bug would change) or a **success-only double** (a mock that can only succeed). Restore your change, `git switch -`, and write down which kind it was.
2. **Write a strategy if there is none.** In a fresh session:
   ```text
   /andthen:testing --mode strategy
   ```
   It writes no tests. It asks the decisions code cannot answer (high-risk areas, which user journeys need E2E, coverage gates), each with a recommendation, sized to your product's stage and scale. Commands stay in `Key Dev Commands`.
3. **An unknown-cause bug: diagnose before you fix.** In a fresh session, start with the plan only:
   ```text
   /andthen:triage --plan-only "<the symptom, exactly as you saw it>"
   ```
   Give it the symptom, not your theory. Error messages, stack traces and logs are evidence to it, not instructions. It stops at a structured fix plan. Read the root-cause chain: is it a cause, or a place the symptom shows up?
4. **Then fix it.**
   ```text
   /andthen:triage "<the symptom>"
   ```
   It reaches a root cause, writes a failing test through `testing` that proves the defect **before** the fix, fixes, searches for other instances of the same cause, and closes on the **original symptom**, not on a green local test. Watch the stop rule: after two failed fix attempts it writes down what both assumed and tests that assumption before a third. After three it hands the problem once to an `oracle` role agent, if you installed them in X5, then stops and reports.
5. **A known defect: prove it.**
   ```text
   /andthen:testing --mode prove-it "<the defect>"
   ```
   The flow is fixed: reproduce as a failing test (its output matches the reported symptom), the minimum production change that turns it green, refactor on green, keep the test. Its report must include the exact **pre-fix failure output**. Without it, the bug was never proven to exist. For untested legacy code it pins current behavior with a characterization test first.
6. **New behavior, test first.** Test-first is not a flag. Require it in your `Testing Strategy` document, or say so in the request: `/andthen:testing "<behavior>, test first"` runs each test red, for the missing behavior, before the code that turns it green. A plan run's stories (`exec-plan`) take test-first only from the `Testing Strategy` document.
7. **Strengthen a weak proof.** For a scenario you graded "does not protect": `/andthen:testing "<the scenario's code>"` writes tests for the behavior at the lowest level that crosses the real trust boundary. Then repeat step 1 on the new test. Break the behavior and watch it go red.

## Verify

- [ ] Every proof you rely on is graded, and each "does not protect" is either strengthened or recorded as a known weakness.
- [ ] A bug fix has a regression test that you **saw fail** before the fix, with the failure message in the report, and it stays in the suite.
- [ ] The fix is checked against the **original symptom**.
- [ ] No test was deleted, disabled or weakened to get green. A flaky test is reported, never skipped on the agent's own call. Quarantine is a person's decision, recorded in the strategy.
- [ ] If you wrote `docs/TESTING-STRATEGY.md`, it names your levels, fixtures and the before-merge bar and contains no commands.

## Sizing check

*How much test discipline does this work earn?* A typo fix earns the existing suite staying green. A defect in an authorization path earns `prove-it`: the failing test is the only proof. A flaky suite earns a strategy and a quarantine decision before any more features land on it. Coverage percentage as a target is a vanity metric. Uncovered changed lines and tests that survive their behavior being removed are the real signals.
