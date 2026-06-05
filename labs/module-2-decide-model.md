# Module 2 – Decide & Model

> **The loop:** `clarify → ` **`decide & model`** ` → spec → exec-spec → review`
> **You'll produce:** an ADR (the *why* behind one design fork) and a short glossary (one name per concept) – and you'll verify both *before* you write the spec.

You've clarified *what* to build (Module 1). Before you write the contract, there's one consequential choice to settle and one vocabulary to fix. Decide them here, once, and the spec gets unambiguous and the agent stops guessing.

The worked feature is **shared lists** for the todo app. This module's slice: **the sharing-model decision** – how an owner↔recipient↔list relationship is modeled (and what to call the pieces) before any of it is specced.

## Before you start

You should have this from earlier modules, under `docs/specs/shared-lists/`:
- `requirements-clarification.md` (Module 1)

If you're joining at this module, your facilitator will point you at a prepared version.

## The principle (1 minute)

Going straight from clarify to spec bakes an *unmade decision* into the contract – the agent picks a sharing model for you, mid-build, and you find out in review. Two cheap moves prevent it:
- An **approach fork** deserves an **ADR** – it records the decision *and the why*, so nobody re-litigates it later.
- **Ubiquitous language** fixes one name per concept, so the spec reads one way, not three.

Both become the agent's input and your checklist. And both are **dial-aware**: a trivial change (rename a button) has no fork and no new words – you'd skip this whole module.

## Step 1 – Read the inputs like the agent will

Open the clarification. Notice what's already settled: that view-only-with-registered-users is the *first* slice, and that the owner can revoke. You're not re-deciding scope here – you're deciding *how* to model it and what to *call* it.

## Step 2 – Manual once: decide and name, by hand

Before running any skill, do both moves by hand.

**The trade-off.** The sharing-model fork has three real options. Fill in this table – and assign a weight to each criterion (which one decides it?):

| Criterion (weight?) | Per-list access-grant | Workspace-ownership | Invite-link |
|---------------------|:---------------------:|:-------------------:|:-----------:|
| Per-user revocation | ? | ? | ? |
| Fits the current single-owner model | ? | ? | ? |
| Room for future roles / assignment | ? | ? | ? |

Pick one option and write a one-line *why*. Then jot **5 glossary terms** for the domain – one canonical name each, plus the synonyms you're banning:

- **Owner**, **Recipient**, **Share** (the `ListShare` record), **Role**, **Viewer**

> 💡 This is the point of the manual step: the table is easy, but choosing *and weighting* the criteria forces the real judgment (you just decided revocation matters more than abstraction). That thinking is the durable skill – the tool runs it faster, it doesn't replace it.

Keep your table and terms; you'll compare them to what the skills produce.

## Step 3 – With AndThen: generate the ADR, then the glossary

```bash
/andthen:architecture --mode trade-off "sharing model for shared lists"
```

This is **interactive**. It will present a proposed set of criteria and weights and **ask you to confirm or adjust** before it scores anything – that gate is the whole point, so don't rush past it. It then researches each option and writes an **ADR** (the decision, the alternatives, the consequences). No code changes.

```bash
/andthen:ubiquitous-language shared-lists
```

This reads the codebase + your ADR and writes a **glossary** – canonical term, synonyms to avoid, and bounded context for each.

If either asks you questions, that's expected and useful – it's surfacing axes the clarification left implicit. Answer them, or note them as deferrals.

Now compare what they produced to your hand version:
- Did the trade-off weight a criterion differently than you did? Whose weighting is more defensible?
- Look at the ADR's **Alternatives Considered** – the rejected options and *why*. A generic "pick a sharing model" prompt gives you the pick, not the *why* that survives later argument.
- Look at the glossary's **Avoid** column – it bans the synonyms ("collaborator", "guest") that would otherwise drift into the spec.

> 🎨 **UI/UX track (gated):** If your feature has a UI surface, wireframe the screens here too – `/andthen:ui-ux-design --mode wireframes`. The low-fi screens become a FIS input in Module 3, exactly like the ADR. No UI surface? Skip it. Full track: [`track-ui-ux-design.md`](track-ui-ux-design.md).

## Step 4 – Verify the ADR + glossary (the real skill)

A decision you can't justify isn't decided; a term nobody uses isn't ubiquitous. Check both against this gate:

- [ ] The ADR's **decision is clear** – one option, stated plainly
- [ ] It's **justified** – weighted criteria and rejected alternatives, not a bare preference
- [ ] **Consequences** are named – what gets easier, what gets harder
- [ ] Glossary terms are **crisp and canonical** – one name per concept, synonyms in the Avoid column
- [ ] Both are **ready to feed the FIS** – Module 3 can inline the chosen option and the terms verbatim

If the "one decision" is secretly a tangle of subdomains (workspaces, notifications, billing), that's a signal – the work wants strategic design (`architecture --mode event-storming,strategic-design`, Module 6), not one ADR.

## Step 5 – Dial check

Ask yourself: *was a trade-off ADR + glossary the right amount of structure here?*
- For the sharing model – **yes**: a real fork with different long-term consequences, plus new terms the spec must use consistently.
- For renaming a button – **no**: no fork, no new vocabulary → skip straight to `/andthen:quick-implement` or `/andthen:spec`. An ADR there is over-engineering.

Right-sizing – *does this fork even earn an ADR?* – is the judgment this whole course is about.

## Done when

You have a verified ADR and glossary for the sharing-model decision, and you can point to the chosen option and the terms the next step will carry. You'll consume both in **Module 3** with `/andthen:spec` – the ADR becomes a one-line Architecture Decision in the FIS, and the glossary becomes the spec's vocabulary.

---

<sub>Stuck? Describe the *symptom* to the agent ("my criteria don't separate the options"), not the fix – better input, better output. Your facilitator has a reference ADR and glossary to compare against.</sub>
