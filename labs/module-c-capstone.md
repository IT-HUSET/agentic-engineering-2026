# Capstone – Run the whole loop, right-sized

> **The loop:** `clarify → design → spec → exec → review → maintain` – all of it, your call
> **You'll produce:** a shipped, verified feature *and* a one-paragraph reflection on whether you sized the work right.

This is the whole course in your hands. Every module so far taught one step on a feature we handed you. Now you take a raw idea and run the *entire* loop yourself – and the first, most important decision is one no skill makes for you: **how much structure does this work deserve?**

There's no reference solution. Every Capstone is different. The point isn't to produce *the* answer – it's to right-size the loop and run it with judgment.

## Step 0 – Choose your work

Pick one:
- **Your own repo's next feature** (best – real stakes). If the agent hasn't seen this codebase, start by making it legible: `/andthen:map-codebase` and/or `/andthen:init` (Module 9). You can't run the loop well on a codebase the agent can't navigate.
- **The lab app's next feature**, from this menu – chosen to span the dial:

| Work | Roughly… |
|------|----------|
| Sort todos by due date · a "clear completed" button | a one-sentence change |
| Due-date reminders for a list · archive a list | one feature |
| An activity feed across the collaboration features | a multi-feature direction |

## Step 1 – Size it first (do this before any skill)

**Write down, in one line, the rung you're choosing and why:**

> "This is a `____` because `____`."

The rungs of the Structure Dial:

| Rung | Path | Earns it when… |
|------|------|----------------|
| **Quick** | `/andthen:quick-implement` + verify | one clear change, low risk |
| **One feature** | `clarify?` → `/andthen:spec` → `/andthen:exec-spec` | a single demoable feature with real decisions |
| **Multi-feature** | `/andthen:prd` → `/andthen:plan` → `/andthen:exec-plan` | several features with dependencies |

> 💡 This is the assessment. Sizing *after* you build is just narrating what happened. The skill is reading the work and placing it on the dial **up front** – and the dial cuts both ways: a PRD for a one-liner is as wrong as vibe-coding a five-feature direction.

## Step 2 – Run the loop at that size

Run your chosen path end to end. Some reminders from the modules:

- **Design is gated** (M2/M6). A new ADR or subdomain map only if the work earns it – `/andthen:architecture --mode trade-off` for one real fork, strategic design for a direction. One CRUD field needs neither.
- **UI/UX is gated** (track). A UI surface? `/andthen:ui-ux-design`. No UI? Skip it.
- **Carry context forward.** Each step's output feeds the next – the clarification into the spec, the ADR into the FIS, the plan into execution.
- **If you run long**, don't push a degrading window – `/andthen:handoff`, then resume in a fresh session (M9).

## Step 3 – Verify (M5, applied for real)

Tests passing is not "it works." Verify at the level the work earned:

- [ ] You can name the **observable outcome** – what you'd click or query to confirm it's done
- [ ] You ran **`/andthen:review`** at the right depth (a quick pass for small work; gap + code + security lenses for a real feature)
- [ ] You addressed findings (`/andthen:remediate-findings`) rather than waving them through
- [ ] Nothing is reported "done" on a red build/test/lint

## Step 4 – Debrief (the real finish line)

Write a short reflection – two questions:

1. **Dial-fit:** Was the structure you chose right? Where did you over- or under-structure, and how did you notice?
2. **Monday:** What will you do differently on your *real* codebase?

## Done when

You have a shipped, verified feature **and** a written dial-fit reflection. If you can say – honestly – *why* the rung you chose was the right amount of structure for this work, you have the one thing this whole course was about.

That judgment – not any single skill name – is yours to keep. The skills will change; AndThen is moving fast and will look different in six months. The loop, and the discipline of right-sizing it, won't.

---

<sub>Stuck on sizing? Describe the work to the agent and ask it to argue *both* a lighter and a heavier path – then make the call yourself. That's the skill. Your facilitator can pressure-test your dial choice before you commit.</sub>
