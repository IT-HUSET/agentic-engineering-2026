# X13 – Review and fix until clean

**What you do:** run AndThen's review/fix loop recipe on your finished plan from a coordinating session, then read why it stopped.

**Why it matters:** one `review --fix` is one round. When a round fixes a CRITICAL or HIGH finding, it asks for a follow-up review, and someone has to run it. The loop does that for you, but only if it stops for the right reason. "Repeat until PASS" is the stop condition most people write, and it is the wrong one.

**What you have at the end:** a chain of review reports, each one naming the report before it, one commit per fix round, and a written comparison of the stop condition you guessed with the one the recipe uses. Optionally, the loop as a project skill your team calls by name.

> **Skills:** `review`, `implement-fix` · AndThen COOKBOOK: *Review and fix until clean, from a coordinating session* · Playbook background: §11.

## When to pull it

- **Your plan is built and its review asks for more.** *Check:* the last `review --fix` ended on a `Next (fresh session):` line that asks for a follow-up review.
- **You run `review --fix` by hand, round after round,** and the reports and diffs fill the session you steer from.

## Input

Your team's built `plan.json`, after its last story is `done`. If you have none, use the `bug-hunt` branch of this repo (four planted bugs in `todo-app/`) and keep the target small: `todo-app/src/app/routes/todos.py` and `todo-app/src/app/utils.py`.

## Steps

1. **Guess first.** Before you read the recipe, write down in one line when you would stop a loop of review and fix rounds.
2. **Run the recipe.** In a fresh session on your feature branch, paste the prompt from the COOKBOOK with your plan's path:
   ```text
   Run a review/fix loop on the implementation of docs/specs/<feature>/plan.json.
   Delegate every review and every fix round to its own fresh subagent; this conversation
   only coordinates and reports.

   Each review subagent invokes the andthen:review skill on that plan; from the
   second review on, it also asks for a follow-up on the previous report, by its
   path. Each fix subagent invokes the
   andthen:implement-fix skill on the report that review wrote. Every subagent brief
   passes --auto.

   Stop when a fix round fixes nothing or its Next line asks for no follow-up review. Also
   stop, and report, when a finding survives a fix round unchanged or a fix needs a
   decision. Finish with the final verdict, the report paths, and the remaining Note and
   DEFERRED findings.
   ```
   A loop takes a while. Start it, then work on something else.
3. **Read why it stopped.** Open the reports in order. Each follow-up has a `**Follows**:` line naming the one before it. Check three things:
   - **Why did it stop?** It should name one of the recipe's stop conditions, never a verdict or a severity count.
   - **Is the final verdict the reviewer's?** The coordinator reports it. It never re-grades it.
   - **What is left?** Each `Note` and `DEFERRED` finding is now yours to decide.
4. **Compare with your guess.** Write one line: where would your stop condition have ended the loop, and what would it have missed?
5. **Optional: make it a project skill.** The COOKBOOK recipe *A recipe you run every week* shows how. Put the fixed parts in `.claude/skills/review-loop/SKILL.md` and keep the target as `$ARGUMENTS`. Symlink it at `.agents/skills/review-loop` for Codex.

<details>
<summary>Answer: why "until PASS" is the wrong stop condition</summary>

A `Note` finding is one no fix round may apply without you. One open `Note` can keep the verdict at FAIL forever, so "until PASS" may never end. The other way round, a coordinator told to reach PASS can talk itself there. The loop ends on the hand-off: the fix round's `Next` line asks for another review only after it fixed a CRITICAL or HIGH finding or left a fix partial. A blocked CRITICAL or HIGH fix is deferred and escalated, which is the "needs a decision" stop. A MEDIUM or LOW finding moved to the Tech Debt Backlog is handled, not a stop.

</details>

<details>
<summary>Reference result: the <code>bug-hunt</code> branch, all of <code>todo-app/src/</code>, 2026-11-15</summary>

Measured once per variant, so read these as a pattern, not a benchmark.

- **"Until PASS" on Claude Code:** fixed all four planted bugs, three reviews, 25 minutes. The coordinator ran the reviews in its own session and changed the reviewer's FAIL to PASS itself.
- **The recipe as a skill on Claude Code:** fixed all four bugs, kept the coordinator's context small (10 turns), and reported the reviewer's FAIL as written. A first version of the skill stopped too early on MEDIUM findings moved to the backlog: the wording left out "CRITICAL or HIGH".
- **The recipe as a skill on Codex:** fixed all four bugs and committed each fix round. It was stopped by hand after four reviews and 90 minutes, because each review found a smaller issue further from the bugs. A small target keeps the loop short.

</details>

## Verify

- `git log` shows one commit per fix round.
- Each follow-up report names the report before it in `**Follows**:`.
- The final reply names its stop reason, and its verdict matches the last report's.
- Your one-line comparison with your guess.

## Sizing check

One round of `review --fix` is the whole job when its `Next` line asks for no follow-up. The loop is worth it when a round asks for another review. A large target makes the loop long, because every review reads it all again, so point it at the plan or the paths you changed.

## Pitfalls

- **Stopping on the verdict.** "Until PASS" or "until no MEDIUM remains" can loop forever, or end with a verdict the coordinator wrote itself.
- **Running the reviews in the coordinating session.** The reports and diffs fill it, and the reviewer is no longer fresh.
- **Commits fail on Codex.** The `workspace-write` sandbox blocks writes in `.git`. Add `--add-dir <repo>/.git` when you run `codex exec`.
- **Codex's agent limit.** A long loop can log `agent thread limit reached`. In the reference run the loop carried on, but expect it on a big target.
