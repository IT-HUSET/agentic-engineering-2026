# Module 8 – Orchestrate & Parallelize

> **The loop:** `… prd → plan → ` **`exec-plan`** ` → maintain`
> **You'll produce:** the collaboration stories implemented in the app – each one review-gated and the whole plan drift-checked – and you'll choose the isolation and autonomy level deliberately.

In Module 7 you produced a schedule: a `plan.json` of sequenced stories in waves, each with its own FIS. Now you run it. The new skill isn't writing code – it's **orchestration**: deciding what runs together, keeping parallel work from colliding, and trusting the gates that make autonomous execution safe.

The worked feature is still **shared lists**. This module's slice: **execute the M7 plan bundle**, and make a real choice about *how* – plain sub-agents, Agent Teams, or Teams with isolated worktrees.

## Before you start

You should have, under `docs/specs/shared-lists/`:
- The M7 **plan bundle** – `plan.json` (stories, waves, `dependsOn`, `parallel`) and one **FIS per story**

Every schedulable story must already have its FIS – `exec-plan` won't invent them. If you're joining here, your facilitator will point you at a prepared bundle.

## The principle (1 minute)

Run a multi-story plan by hand and you improvise the order, lose track of which story broke the build, and let a half-finished story unblock the next one. `exec-plan` turns the plan into a **supervised run**: it spawns a worker per story in the current wave, each worker runs `/andthen:exec-spec` (implement) then `/andthen:quick-review` (gate), the orchestrator waits for the wave to go green, then schedules the next – and finishes with a whole-plan `review --mode gap`. Autonomy *with brakes*: nothing is marked done on a red tree, and a failed story can't unblock its dependents.

It's **dial-aware**: one story is M4's `exec-spec`. Parallel isolation (worktrees) only pays off when stories genuinely run at the same time.

## Step 1 – Read the schedule like the orchestrator will

Open `plan.json`. Find Wave 1 – the stories with no unmet `dependsOn`; those run together. Trace one dependency edge (e.g. "assign a todo" `dependsOn` "roles & permissions") and confirm why it *must* wait. This is the schedule the orchestrator executes; you're reading it before it runs.

## Step 2 – Manual once: run one story, then reason about isolation

First, run a single story the way `exec-plan` runs each one – by hand:

```bash
/andthen:exec-spec docs/specs/shared-lists/<story-S01>.fis.md
/andthen:quick-review
```

That's the unit `exec-plan` repeats per story: implement, then gate. Feel it once so the orchestration isn't magic.

Now reason about **isolation**. Two Wave-1 stories are marked `parallel: true`, and both will write `plan.json` and the State doc:

- If two agents edit those files at the same time, what happens?
- What would have to be true for them to run concurrently *without* clobbering each other?

> 💡 This is the point of the manual step: `exec-spec` + `quick-review` is the whole per-story loop – `exec-plan` just schedules it many times. And the moment you imagine two agents writing the same file, you've discovered *why* parallel execution needs **worktree isolation**: each story works in its own git worktree and merges back sequentially, so there's no race. You don't reach for that machinery until real parallelism exists.

## Step 3 – With AndThen: run the plan

Portable mode (works with any agent – runs the waves, sub-agent per story, no concurrency within a wave's writes):

```bash
/andthen:exec-plan docs/specs/shared-lists/
```

If you're in Claude Code with Agent Teams enabled, you can run it as a coordinated team. **Important:** `--team` *alone* still runs stories sequentially – true parallel execution needs `--worktree` (each parallel story isolated in its own worktree, merged sequentially):

```bash
/andthen:exec-plan --team --worktree docs/specs/shared-lists/
```

Either way, watch the run:

- **Waves are honored** – Wave 1 starts; Wave 2 waits until its dependencies are green.
- **Each story passes its gate** – `exec-spec` implements, `quick-review` blocks until accepted findings are fixed; no story goes "done" on a red build/test/lint.
- **A whole-plan backstop** – after every story, a final `review --mode gap` re-reads the PRD + all changes and flags cross-story drift.

If a story fails, watch what *doesn't* happen: its dependents don't run on a broken foundation – they're recorded `skipped`, and independent stories keep going.

## Step 4 – Verify the run (the real skill)

A run that *reports* success isn't the same as one that *is* successful. Check it against this gate:

- [ ] **Every completed story is green** – build, targeted tests, lint, types all pass; none marked done on a red tree
- [ ] **Per-story review cleared** – `quick-review` findings were remediated, not waved through
- [ ] **The whole-plan `review --mode gap` passed** – or its findings were remediated, not ignored
- [ ] **Failures are contained** – a failed story's dependents are `skipped`, not silently built on
- [ ] **Worktrees resolved** (if you used them) – merged on success, preserved (not lost) on failure
- [ ] **Right-sized run** – you used Teams/worktrees only because real parallelism existed; a sequential plan ran plainly

## Step 5 – Dial check

Ask yourself: *was this orchestration level the right amount?*
- A multi-story plan with independent waves – **yes** to `exec-plan`; Teams + worktrees *if* the parallelism and isolation needs are real.
- A single story – **no**: that's M4's `/andthen:exec-spec`. Don't wrap one story in plan machinery.
- A fully sequential plan – `exec-plan`, but **skip worktrees**: there's nothing to parallelize, so the isolation overhead buys nothing.

The judgment isn't "use the most powerful mode" – it's **match the machinery to the parallelism and risk that actually exist.** That's the dial, applied to *how* you run.

## Done when

The collaboration stories are implemented and green, each review-gated, the whole plan drift-checked, and you can explain *why* you chose the isolation level you did. The project is now substantially bigger – which is exactly what **Module 9** addresses: keeping a long-lived, multi-session, partly-inherited codebase maintainable.

---

<sub>Stuck? Describe the *symptom* to the agent ("story S03 fails its tests, here's the output"), not the fix – and remember a red gate is work to finish, not a caveat. Your facilitator has a reference run to compare against.</sub>
