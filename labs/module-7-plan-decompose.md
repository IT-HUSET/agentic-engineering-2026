# Module 7 – Scale up: Plan & Decompose

> **The loop:** `… strategic design → ` **`prd → plan`** ` → exec-plan`
> **You'll produce:** a PRD and a **plan bundle** – a `plan.json` of sequenced, dependency-aware stories plus one FIS per story – and you'll verify it *before* any story is built.

For six modules the work fit in one feature. Now it doesn't: "shared lists" is a whole direction – sharing, invites, permissions, assignment, notifications. You'll turn the subdomain map you carved in Module 6 into a plan a machine can schedule, where the story boundaries follow the *contexts* you drew, not whoever-grabs-the-file.

The worked feature is still **shared lists**, now as a multi-feature direction. This module's slice: **decompose the direction into sequenced stories with explicit dependencies** – the schedule Module 8 will execute.

## Before you start

You should have, under `docs/specs/shared-lists/`:
- The M6 **strategic-design report** – the subdomain table and context map with named seams
- The M2 **ADR + glossary** – the sharing-model decision and the domain terms
- The completed M1–M5 view-only slice – slice one of this direction

If you're joining at this module, your facilitator will point you at prepared versions.

## The principle (1 minute)

Build many features without decomposing first and you improvise the order – you discover halfway that permissions needed the invite model that wasn't built yet, and you big-bang integrate at the end. One move prevents it: **decompose into vertical, sequenced stories.** Each story is a demoable slice through all layers; each names what it *depends on* as an edge (not a sentence); and those edges fall out into **waves** – stories with no unmet dependency that can run together. The plan bundle (`plan.json` + a FIS per story) becomes the agent's schedule and your checklist.

It's **dial-aware**: a single feature is M3's one FIS. Only genuinely multi-feature work with real dependencies earns a PRD + plan.

## Step 1 – Read the inputs like the agent will

Open the M6 strategic-design report and the M2 ADR. Notice the boundaries are already drawn: Task Management, Sharing & Permissions, Notifications, Identity. You're **not** re-deciding them – `plan` reads them from the Architecture doc and treats them as fixed. Your job is to cut stories that *respect* those seams and sequence them by what actually blocks what.

## Step 2 – Manual once: slice and sequence, by hand

Before running any skill, decompose the direction yourself. Write each story as a vertical slice (something a user can see work), then draw the dependency arrows:

```
S01  Share a list (read-only) with another user
S02  Invite a non-user by link            depends on → S01
S03  Roles & permissions (viewer/editor)  depends on → S01
S04  Assign a todo to a member            depends on → S03
S05  Notify on share / assignment         depends on → S01, S04
```

Push yourself to the hard calls:

- Is "invites" **one** story or three (create link / accept / revoke)? What makes it one demoable slice vs several?
- Which stories truly **block** which? (Can you assign a todo before roles exist? Before sharing exists?)
- Which stories have **no unmet dependency** – i.e. could run *at the same time*? (That's your first wave.)

> 💡 This is the point of the manual step: the stickies are easy, but *vertical-vs-horizontal* and *what truly blocks what* are real judgments. A horizontal slice ("do all the database work first") can't be demoed alone and forces a big-bang at the end. The dependency edges are what make parallelism safe. The tool runs this faster and writes the specs; it doesn't make the call for you.

Keep your story list and arrows; you'll compare them to the plan.

## Step 3 – With AndThen: generate the PRD, then the plan

First, the PRD – *what* must be true, for whom, and what's out of scope:

```bash
/andthen:prd docs/specs/shared-lists/
```

It reads your carried artifacts (clarification, ADR, strategic-design map) and writes a self-contained `prd.md` – functional requirements, scope in/out, NFRs, a decisions log. If a load-bearing gap appears, it may pull in `clarify` rather than guess.

Then the plan bundle:

```bash
/andthen:plan docs/specs/shared-lists/
```

This reads `prd.md` (and the Architecture doc, so story scope respects the M6 boundaries) and writes **`plan.json` + one FIS per story**. It organizes stories into **phases** (often: tracer bullet → feature slices → hardening) and **waves** (W1 = no deps, W2 = depends only on W1…), generates each story's FIS with parallel sub-agents, then runs a **cross-cutting review** over the PRD + all FIS together.

If it asks you questions, that's expected – it's surfacing gaps your PRD left. Answer them or record them as deferrals.

Now compare the bundle to your hand decomposition:

- Open `plan.json`. Did its **waves** match your arrows? Where it disagreed about what blocks what – who's right?
- Look at the `dependsOn` edges and `parallel: true` flags – that's the schedule Module 8 executes, not prose.
- Read the **cross-cutting review** output: did it catch an overlap or a missing seam between two stories that you'd only have found mid-build?

## Step 4 – Verify the plan bundle (the real skill)

A plan you can't schedule isn't a plan. Check it against this gate:

- [ ] Every story is **vertical** – a slice a user can see, not a horizontal layer
- [ ] Dependencies are **story-ID edges** (`dependsOn: ["S01"]`), not sentences
- [ ] Stories are organized into **waves** – it's clear what can run together
- [ ] **Every story has a FIS** (`stories[].fis` points at a real file) – the bundle is complete
- [ ] The **cross-cutting review** ran clean – no overlapping scope, no missing integration seam, PRD ↔ FIS traceable
- [ ] **Right-sized** – this is genuinely multi-feature; if it's really one slice, you climbed one notch too high

If a *single* boundary is genuinely contested (e.g. should Lists and Collaboration split into separate modules?), that one seam – not the whole plan – earns deeper scoring:

```bash
/andthen:architecture --mode decompose "Lists vs Collaboration module boundary"
```

## Step 5 – Dial check

Ask yourself: *was a PRD + plan the right amount of structure here?*
- For the collaboration *direction* – **yes**: many features, real dependencies, spanning the subdomains you mapped. That earns decomposition.
- For a single feature – **no**: that's M3's `/andthen:spec` → one FIS → M4's `/andthen:exec-spec`. A PRD around one slice is ceremony – climb *down*.
- If a single FIS ever comes out *secretly huge* (lots of unrelated scenarios, several demos hiding inside), that's the signal to climb *up* to here – not to write a bigger FIS.

Right-sizing – *has this grown past one feature?* – is the judgment this whole course is about.

## Done when

You have a verified plan bundle – `plan.json` with sequenced, dependency-aware stories in waves, and a complete FIS for each – for the collaboration direction, and you can point to where the story boundaries follow the M6 contexts. You'll execute it in **Module 8** with `/andthen:exec-plan` – the *same* bundle, run as a schedule.

---

<sub>Stuck? Describe the *symptom* to the agent ("I can't tell if invites should be one story or three"), not the fix – better input, better output. Your facilitator has a reference plan bundle to compare against.</sub>
