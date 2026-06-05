# Module 5 – Verify & Review

> **The loop:** `clarify → spec → exec-spec → ` **`review`**
> **You'll produce:** a reviewed, remediated view-only sharing slice – every acceptance scenario independently confirmed, the findings triaged and fixed – and you'll be able to say *how much to trust it*.

In Module 4 the agent implemented the FIS and **attested** that every scenario was green. That was the builder grading its own homework – real and useful, but not independent. This module runs the independent pass: you confirm the scenarios yourself, let `review` find what the tests didn't, and fix the findings that matter.

The worked feature is still **shared lists**. This module's slice is the one you built: **share a list, view-only** – now under review.

## Before you start

You should have, from Module 4, the implemented view-only slice in the codebase, plus the FIS it was built from:
- `docs/specs/shared-lists/shared-lists.md`

Open the FIS now and re-read the **Acceptance Scenarios** (S01–S05). That's your independent checklist – not the agent's attestation, *yours*.

If you're joining at this module, your facilitator will point you at a prepared implementation and FIS.

## The principle (1 minute)

**Tests pass ≠ it works.** A green suite proves the scenarios you *wrote* – it says nothing about the ones you forgot, the spec the code quietly drifted from, or a rule that's enforced in the UI but not on the server. Review is the cheap, independent pass that asks three questions: does it **match the spec** (gap), is the **code sound** (code), and is it **safe** (security)? That's how you turn "the agent said done" into "I checked, and here's how much I trust it."

## Step 1 – Read the implementation like a reviewer

Open the diff (or the changed files) for the view-only slice and read it *against the FIS*, not on its own. The FIS is your baseline: it already told you what "done" means (S01–S05) and what's deliberately out of scope ("What We're NOT Doing"). You're not re-deciding the feature – you're checking whether the code kept the contract.

## Step 2 – Manual once: hunt the gap by hand

Before running any skill, hunt for one gap yourself – a planted-bug-style read. Focus on **S03**: *"recipient cannot mutate a view-only list, including via a direct request."*

- Open the mutating route handlers (`routes/todos.py`, `routes/todo_lists.py`). Does each one check the access role and **refuse a viewer (403)** – or is the only thing stopping a viewer the hidden button in the template?
- Picture the bypass: a viewer sends `POST /lists/<id>/todos` *directly*, no browser. Does the server stop it?
- Look at the S03 test. Does it drive the **route**, or only click the UI? A test that only clicks UI never asked the real question.

> 💡 This is the point of the manual hunt: a suite can be **all green while S03 is violated**, because the test asserted what the UI shows, not the invariant the server must hold. Finding that gap by reading the code against the contract is the durable skill – the tool confirms it faster, it doesn't replace the judgment.

Keep your notes; you'll compare them to what the skill finds.

## Step 3 – With AndThen: review the change

```bash
/andthen:review docs/specs/shared-lists/shared-lists.md
```

This reads the change set **and the FIS as the intent baseline**, runs the right lenses, and writes one consolidated report to a review file. It changes no code – review is read-only. On this auth-bearing surface it resolves to a **gap + code + security** chain (it auto-adds the security lens because the diff touches authorization paths – you didn't have to ask).

Need a faster, mid-flow sanity check on a smaller change instead? `/andthen:quick-review` runs a fresh-context critic pass inline, no report file.

Now compare the report to your hand hunt:
- Did review **prove** the S03 bypass you suspected – citing the unguarded route, tying it to S03 and OC02? (Or did you find something it didn't?)
- Look at the **security findings** – grounded in *this* repo's actual route handlers. A generic "review my code" prompt can't do that.
- Look at the **gap findings** – they also *confirm* the scenarios that genuinely pass, and correctly **dismiss** Non-Goals (no "you forgot editor roles" – that's out of scope on purpose).
- Note each finding's `Routing: Fix | Note` tag – that's what the next step reads.

> 🎨 **UI/UX track (gated):** If your feature has a UI surface, add the UI lens here – `/andthen:ui-ux-design --mode review` plus `/andthen:visual-validation`, which screenshots the built screens and checks them against your wireframes across breakpoints (the UI half of "tests pass ≠ it works"). No UI surface? Skip it. Full track: [`track-ui-ux-design.md`](track-ui-ux-design.md).

## Step 4 – Remediate, then verify (the real skill)

Hand the report to remediation:

```bash
/andthen:remediate-findings <path-to-the-review-report>.md
```

This applies only the **Fix**-bucket findings (the real defects), **surfaces Note findings** for you to decide on, and **re-validates** – it won't auto-apply anything that contradicts a FIS Non-Goal. Then gate the loop on this checklist:

- [ ] Every acceptance scenario **S01–S05** independently confirmed – by you, not just the M4 attestation
- [ ] The **S03 direct-request** path returns **403** server-side, with a test that drives the route (not just the button)
- [ ] Every **Fix** finding is RESOLVED with evidence; every **Note** finding is consciously decided (fixed or deferred on purpose)
- [ ] No remediation crept past the FIS (no editor roles, no notifications snuck in)
- [ ] You can state, in one sentence, **how much you trust this change – and why**

> ⚠️ Findings are **routed, not a flat to-do list.** Resist "while I'm here" cleanup – that breaks traceability and ships untested changes. If you spot something out of scope, surface it; don't bundle it into this remediation.

## Step 5 – Dial check

Ask yourself: *was a full `review` chain the right amount of structure here?* For an auth-bearing feature touching mutating routes – yes; a missed enforcement check is a real vulnerability, so you want gap + code + security. For a one-line copy tweak mid-flow, the full report is overkill – that's `/andthen:quick-review`. Matching the review weight to the risk of the change is the judgment this course is about.

## Done when

You have a **reviewed, remediated** view-only sharing slice: every scenario confirmed by you, the S03 server-side bypass closed, findings triaged. That completes the **single-feature loop** – `clarify → spec → exec-spec → review`, idea to verified, reviewed, trustworthy change. You now own a complete, repeatable workflow. The full day carries the *same* shared-lists feature into **scale-up** (`prd → plan → exec-plan`): how the loop holds when one feature becomes many.

---

<sub>Stuck? Describe the *symptom* to the agent ("the S03 test passes even when I remove the server-side check"), not the fix – better input, better output. Your facilitator has a reference review report to compare against once the implementation exists.</sub>
