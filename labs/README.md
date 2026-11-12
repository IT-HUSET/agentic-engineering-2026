# Labs

Three parts, in order. The loop is the same everywhere: `[clarify →] plan → exec-plan → review --fix → ship`, right-sized to the work (see [CLAUDE.md](../CLAUDE.md#right-sizing-the-work)).

| Part | What | Where |
|------|------|-------|
| **1. Foundation** | The loop for one feature, once, on `todo-app/` (shared lists), ending in a pull request and a handoff | [`foundation.md`](foundation.md) |
| **2. Case work** | The loop on a case, gated by C1–C5 | below, plus `case-kit/` |
| **3. Exercise catalog** | Optional deepening: end of Day 3 if there is time, or when your case calls for one | [below](#3-exercise-catalog) |

In the foundation, paths are relative to `todo-app/`, where you start Claude Code. In case work they are relative to your case repo's root. Start every step in a fresh session (`/clear`), because each AndThen skill ends by printing the next command to paste.

## 1. Foundation

[`foundation.md`](foundation.md) has one section per step. Each takes the previous step's artifact as input and ends with a checklist and a sizing check.

| Step | Skills | You produce |
|------|--------|-------------|
| [F1 – Orientation and set up](foundation.md#f1--orientation-and-set-up) | `now-what`, `init`, `describe` | A project AndThen can navigate |
| [F2 – Clarify](foundation.md#f2--clarify) | `clarify` | `prd.md` |
| [F3 – Decide](foundation.md#f3--decide) | `decide`, `domain --mode glossary` | An ADR and a glossary |
| [F4 – Plan](foundation.md#f4--plan) | `plan` | `plan.json` and a FIS |
| [F5 – Implement](foundation.md#f5--implement) | `exec-plan <FIS>` | Committed code, proven |
| [F6 – Verify and review](foundation.md#f6--verify-and-review) | `review --fix` | A review report, findings fixed |
| [F7 – Ship and hand off](foundation.md#f7--ship-and-hand-off) | `ship`, `handoff` | A pull request and a handoff |

## 2. Case work

In a team of two to four, you take a prepared case with a brief, build it in a new GitHub repo your team creates for it, and run the loop on it, with the sizing choice for each piece of work written down. **The process is the product.** What you deliver is the artifact trail and the gates you passed, not how finished or polished the app looks. A half-built case with every gate passed is a better result than a polished app built around a skipped gate.

Five gates, each approved by your facilitator against the **files**, not the running app. Your facilitator approves a gate at your table when you are ready. Five times in the three days, every team also presents to the whole room: on the morning of day 2 (C1), midday and end of day 2 (C2, then the first PR), midday on day 3 (the second PR's plan) and at the close (C5). You walk through your decisions, the solution, the consequences and the trade-offs, with the artifacts as proof. The facilitator picks who explains, at the table and in the room, so everyone on the team needs to understand what was built and why. C1 and C5 apply to the case; C2 to C4 apply to every pull request, because AndThen ties a `plan.json` and its FIS files to a branch, so a PR is a plan.

| Gate | Passed when |
|------|-------------|
| **C1 – Case framed** | Your team's own case repo is on GitHub (one repo per team, not a fork) with `check` green (your facilitator provides the `check` script), and `docs/specs/<slug>/prd.md` (or `intent.md`) holds at least three acceptance criteria and the Proportionality facts, the test command runs, and your sizing choice is written down. |
| **C2 – Plan approved** | `plan.json` and a FIS per story exist, every scenario has a runnable proof, no `OVERSIZE:` is unresolved, each ADR in `docs/adrs/` states its door type, and the plan fits one pull request. **No `exec-plan` before C2.** |
| **C3 – First story green** | The story's `plan.json` row is `done` with a `verified.summary` quoting a check that was run (command, exit status, result line), the report has its `Reviewed:` line, and you reflected on whether the next FIS needs to change. |
| **C4 – PR opened** | `review --fix` came back `PASS` on every lens (or `FAIL` marked `**Remediated**:` with every finding behind it resolved), with no open CRITICAL or HIGH finding, every scenario traces to a run proof, and `ship` opened a PR whose text gives the proof per story and the door type. |
| **C5 – Closed** | The case repo has all its PRs, your demo has shown the six things your facilitator looks for, your friction log names one concrete next change to your harness, and your sizing log is complete. |

Day 1 ends with the case start: your team creates its case repo and repeats F1 there, so `check` is green. Day 2 is the case day. It opens with `clarify` on the brief, C1 and the first presentation, then aims for a first pull request through C2 to C4. From the first morning your facilitator shows the six things they look for in your final demo. No points, no grades: it is a conversation, so nobody aims at the wrong target. The case kit (the brief template, setup checklist for your team's repo, friction and sizing log template, and gate board) is coming in `case-kit/`.

## 3. Exercise catalog

Optional deepening. Do them at the end of Day 3 if there is time, or earlier when your case needs one or you are curious. Nothing is assigned; your facilitator may point you to one when its trigger shows up in your own artifacts. Each exercise has a **Trigger**, **Input**, **Output**, **Steps**, **Verify** and **Sizing check**.

| Exercise | Skills | Pull it when |
|----------|--------|--------------|
| [X1 – Decide and model](x1-decide-model.md) | `decide`, `domain --mode glossary`, `spike` | `clarify` showed a solution fork, or the artifacts use two names for one thing |
| [X2 – UI/UX](x2-ui-ux.md) | `ui-ux-design`, `visual-validation` | The case has a UI surface with no wireframes |
| [X3 – Strategic design](x3-strategic-design.md) | `domain --mode event-storming`, `domain --mode subdomains,contexts`, `visualize` | Several subdomains, or no one can say where a module ends. First ask whether it deserves a Domain Map |
| [X4 – Show and publish the plan](x4-show-plan.md) | `visualize`, `tracker publish` | Someone outside your session must read the plan, or it should go to a tracker |
| [X5 – Parallelize, run unattended](x5-parallel-autonomy.md) | `exec-plan --worktree`, `exec-plan --auto`, role agents, `permissions/`, `hooks/` | After C3 you choose parallel or unattended runs. Entry check: two stories with no `dependsOn` edge between them |
| [X6 – Context, brownfield, maintenance](x6-context-maintenance.md) | `describe --model`, `init`, `handoff`, `simplify-code` | Your own or an inherited repo, context rot between days, duplication after reflection |
| [X7 – Trust the tests](x7-trust-tests.md) | `triage`, `testing` | An unreliable suite, a bug with an unknown cause, or a story done on weak proof |
| [X8 – Ship in depth, backlog in](x8-ship-backlog.md) | `ship`, `tracker triage` | Your tracker is input to `clarify`, or you need to explain what `ship` landed |
