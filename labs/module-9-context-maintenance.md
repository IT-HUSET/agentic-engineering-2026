# Module 9 – Context & Maintenance discipline

> **The loop:** `… exec-plan → ` **`maintain`** ` ⟲ clarify …`
> **You'll produce:** a context spine for the project – a Document Index and durable stores – plus a brownfield map and a resumable handoff, and you'll verify your context is actually *engineered*, not hoped.

For nine modules you ran the loop forward. This one closes it: the project keeps living after the feature ships – new sessions, new people, code nobody in the room wrote. You'll name the discipline that quietly carried every prior module – **context engineering** – and learn the three moves that keep the loop alive at project and session scale.

The worked context is the **`todo-app` itself**, now treated as a long-lived, partly-inherited, multi-session project. This module's slices: **establish, recover, and carry** context.

## Before you start

You have the whole project you built across M1–M8. For the brownfield exercise, you'll deliberately treat the app as code you *inherited* and never read. No new prior-module artifact is required – this module operates on the project as a whole.

If you're joining here, your facilitator will point you at a suitable repo state.

## The principle (1 minute)

Every artifact this course produced was **carried context** – the clarification, the ADR, the glossary, the FIS, the subdomain map each filled the next step's window with just the right information. That has a name: *context engineering – filling the context window with just the right information for the next step* (Karpathy). It matters mechanically, not just aesthetically: context **decays** as the window fills (all tested models degrade with token volume – a full 1M window is worse than a fresh session), and it **dies** at session boundaries. The discipline: **capture once, give it a home, carry it across boundaries.** Three skills do that at project scale.

It's **dial-aware**: a throwaway script needs none of this; a codebase you'll live in for a year needs all of it.

## Step 1 – Feel the boundary (manual once)

Two things you can only learn by feeling them:

**Build the same tiny change twice.** Once with everything loaded; once in a fresh session with *only the directly relevant files* (e.g. "add a created-at timestamp to each todo"). Compare quality, speed, tokens.

> 💡 Most people expect the everything-loaded run to win. It usually doesn't – less context, sharper output. That result is the whole principle in one experiment: more context is not better context.

**Write a handoff by hand**, then `/clear` and resume from it alone:

```text
HANDOFF.md
  Current state    – where we are, what works
  Key decisions    – what we chose and why
  Files changed    – the surface touched
  What's next      – the very next action
  Key constraints  – the rules that must hold
  Context to keep  – the open questions / dead ends
```

Notice that some fields are *durable* (decisions, constraints – they belong in a permanent home) and some are *transient* (open questions, dead ends – they belong only in the resume note). That distinction is exactly what `/andthen:handoff` automates.

## Step 2 – With AndThen: establish the spine

```bash
/andthen:init
```

Turns an unstructured repo into one an agent can navigate cold. The centerpiece is the **Document Index** – a routing table *in your `CLAUDE.md`* mapping document types → file paths – plus durable stores (`PRODUCT.md`, `ARCHITECTURE.md`, `STACK.md`, `DECISIONS.md`, `LEARNINGS.md`). **Opt into `STATE.md` when offered** – Step 4's handoff depends on it and won't create it.

Open `CLAUDE.md` and find the Document Index. That table is how every skill (and `handoff`, and a fresh agent) knows where to read and write – AndThen adapts to *your* layout instead of imposing one.

## Step 3 – With AndThen: recover context you never wrote

Treat the app as inherited. Run:

```bash
/andthen:map-codebase
```

Read-only, "discovery not invention" – it fans out sub-agents and writes `STACK.md`, `ARCHITECTURE.md`, appends a **Conventions** section to `CLAUDE.md`, and produces:

- `requirements-discovered.md` – implicit requirements, each with **evidence (file paths) + confidence**
- `decisions-discovered.md` – the choices the code already made, stamped *"Discovered – requires validation by team"*

Open `requirements-discovered.md` and look at the confidence column. It's *inferring* intent from code and saying so – nothing is fact until you confirm it. A generic "explain this codebase" prompt states guesses as facts; this doesn't.

## Step 4 – With AndThen: carry context across the boundary

After some real work, run:

```bash
/andthen:handoff "wire up the share dialog next"
```

Instead of dumping a transcript, it **routes each fragment to its durable home**: mid-flow state → `STATE.md`, gotchas → `LEARNINGS.md`, a structural decision → *recommends* an ADR, and transient priming (open questions, dead ends) → the handoff doc itself. Then:

```text
/clear
Resume from .agent_temp/handoff/handoff-<ts>.md
```

Watch the fresh agent pick up mid-thought. It reads the durable stores *through the Document Index* and the named artifacts *by path* – the handoff doc references them, it doesn't re-paste them.

## Step 5 – Verify: is your context actually engineered?

Context you can't inspect isn't engineered – it's hoped. Check:

- [ ] **Document Index exists** and routes to real files – a fresh agent could orient with no tribal knowledge
- [ ] **Durable stores have homes** – decisions in `DECISIONS.md`, traps in `LEARNINGS.md`, not in a dead chat
- [ ] **The handoff references artifacts by path**, not by re-pasting them
- [ ] **`/context` is healthy** – watch utilization; rot climbs with absolute tokens, not just % full
- [ ] **Project memory is lean** – every line in `CLAUDE.md` spends from the ~150-instruction budget; if removing a line wouldn't cause a mistake, cut it
- [ ] **Discovered ≠ decided** – brownfield findings carry evidence + confidence and were validated by a human

## Step 6 – Dial check

Ask yourself: *how much context discipline does this project earn?*
- A one-session script – **almost none**; don't scaffold an index for a throwaway.
- A feature you'll live with – the **Document Index + lean memory** pay for themselves immediately.
- A long-lived or inherited codebase – the **full cadence**: `map-codebase` to make it legible, `handoff` between sessions, durable stores kept current.

Right-size to the project's **lifespan**, not its size today.

## Done when

You have a Document Index and durable stores, a brownfield map with evidence + confidence, and a handoff you resumed from cleanly – and you can explain why context rot makes this discipline mechanical, not optional. You've now run the whole loop *and* learned to keep it alive across a real project's life. The **Capstone** runs the entire cycle end to end – your feature, your dial.

---

<sub>Stuck? When the agent starts misremembering filenames or re-fixing fixed code, that's a full context window, not a dumb model – `/clear` and resume from a handoff. Describe the *symptom*, not the fix. Your facilitator has reference artifacts to compare against.</sub>
