# Module 4 – Implement

> **The loop:** `clarify → spec → ` **`exec-spec`** ` → review`
> **You'll produce:** a verified, attested implementation of the view-only sharing slice – the *same* FIS you specified in Module 3, now realized in code.

In Module 3 you wrote the **contract** (the FIS) and verified it – without writing any code. This module hands that contract to an AI agent, which implements it task by task and proves each acceptance scenario. You stay in charge: you set the intent and boundaries; the agent fills in the code within them.

The worked feature is still **shared lists**. This module's slice is the one you specified: **share a list, view-only**.

## Before you start

You should have the FIS from Module 3 at:
- `docs/specs/shared-lists/shared-lists.md`

If you're joining at this module, your facilitator will point you at a prepared version. Open it now and skim the **Implementation Tasks** (TI01–TI04) and the **Acceptance Scenarios** (S01–S05) – that's the agent's to-do list and your checklist.

## The principle (1 minute)

Without a spec, "implement this" is open-ended – the agent generates and you hope. With the FIS, implementation is **bounded and checked**: the agent runs an internal **implement → verify → evaluate** loop (build, run tests, lint, repeat until green) and then **attests every acceptance scenario** against real evidence. The rule of thumb: *you own the bread (intent, boundaries), the agent owns the filling (code within them)*.

## Step 1 – Read the FIS like the agent will

Open `shared-lists.md`. Look at one task – **TI01** (the `ListShare` model) – and read its **Verify** line. Notice the FIS already tells you which existing file to mirror (`models/todo_list.py#TodoList`) and exactly what to verify (a duplicate `(list, user)` share raises an integrity error). You're not designing – you're about to execute a contract.

## Step 2 – Manual once: implement one task by hand

Before running any skill, implement **just TI01** yourself:

1. Mirror `models/todo_list.py#TodoList` to create the `ListShare` model (fields per the FIS), and register the table in `database.py` the way the other models are.
2. Write the one test from TI01's **Verify** line – creating two `ListShare` rows for the same `(list, user)` raises an integrity error.
3. **Run that test.** Green or red.

> 💡 That tiny implement → verify loop is the unit `exec-spec` repeats for *every* task. The point of doing it once by hand is to feel it: the FIS told you what to build and how to check it – you executed, then verified. The tool runs this loop faster and ×4, it doesn't replace the judgment.

Keep your work; you'll watch the agent do the same across all four tasks.

## Step 3 – With AndThen: implement the spec

```bash
/andthen:exec-spec docs/specs/shared-lists/shared-lists.md
```

This reads the FIS and implements it **task by task, in order**. For each task it implements the change, **runs that task's `Verify` line before moving on**, and **marks the checkbox immediately** – no batching. Then it runs a cross-cutting pass (build, tests, lint, format, an independent code+gap review) and **attests each acceptance scenario** before declaring done.

Watch for two things as it runs:
- **Checkboxes flip as each `Verify` passes** – the same loop you just did by hand, automated across TI01–TI04.
- **The Chain Attestation** at the end – the agent puts *words* to each link (this task evidences that scenario, which exercises that outcome). It's showing its work, not just claiming "done."

## Step 4 – Verify the implementation (the real skill)

The agent attested. You still verify – it's cheap, because the FIS told you exactly what to check:

- [ ] Every acceptance scenario **S01–S05** is checked and traces to evidence (a named test or an observable result)
- [ ] The build is green and the **real test suite** passes – *run it yourself*, don't just read the claim
- [ ] The **direct-request** test for **S03** exists – server-side enforcement, not just hidden UI buttons
- [ ] No task checkbox is `[x]` without a passing `Verify` behind it

> ⚠️ **Tests pass ≠ it works.** Green tests prove the scenarios you *wrote* in Module 3. Whether those were the *right* and *complete* scenarios is Module 5's question. If a scenario can't be attested because it was written un-observably, that's a signal to fix the *spec*, then re-run.

## Step 5 – Dial check

Ask yourself: *was `exec-spec` the right amount of structure here?* For a feature with a real FIS and four tasks across the data model – yes, you want the task-by-task loop and scenario attestation. For renaming a button there's no FIS to execute – that'd be `/andthen:quick-implement` (same verify discipline, no contract). Right-sizing the executor to the work is the judgment this course is about.

## Done when

You have an implemented, verified, attested view-only sharing slice – S01–S05 demonstrably green – and you can point to how each piece traces back to the Module 3 FIS. You'll **review** it in **Module 5** with `/andthen:review`, which asks what the tests didn't: missing scenarios, security gaps, spec-vs-code drift.

---

<sub>Stuck? Describe the *symptom* to the agent ("the S03 test passes even when I remove the check"), not the fix – and don't hand-edit code mid-run; let the loop remediate or stop and amend the FIS. Your facilitator has a reference to compare against.</sub>
