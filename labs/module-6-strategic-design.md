# Module 6 – Strategic Design

> **The loop:** `… review → ` **`strategic design`** ` → prd → plan → exec-plan`
> **You'll produce:** a subdomain map – classified subdomains, sized bounded contexts, and a context map with named seams – and you'll verify it *before* you plan a single story.

For five modules you built *one* feature, on purpose. Now you'll zoom out: "shared lists" was really slice one of a whole direction – sharing, invites, permissions, assignment, notifications. Before you plan many features, you carve the domain so the plan's story boundaries follow the *domain's* seams instead of being cut at random.

The worked feature is still **shared lists**, but as a *direction* now. This module's slice: **event-storm the collaboration direction, then carve it into subdomains and bounded contexts** – the map your plan will read.

## Before you start

You should have, from earlier modules, under `docs/specs/shared-lists/`:
- The completed view-only slice (M1–M5) – your first incision into this direction
- The M2 ADR and glossary (the sharing-model decision and the domain terms)

You'll also read the existing app code – this is a *brownfield* exercise: single-owner Task Management and a mock Identity already ship; collaboration is the new layer on top.

If you're joining at this module, your facilitator will point you at prepared versions.

## The principle (1 minute)

Plan a multi-feature direction without a map and you decompose *by accident* – stories split along whoever-grabbed-the-file lines, contexts blur, the same word means three things, and you ship a distributed monolith. One cheap move prevents it: **carve subdomains and bounded contexts first.** A subdomain map answers three system-scope questions – *where is the value* (core / supporting / generic), *where are the boundaries* (one model, one team, one vocabulary each), and *how do they integrate* (a named pattern per pair, not an arrow). That map becomes the agent's input for `plan` and your checklist.

And it's **dial-aware** – this is the *top* of the dial. Most work never gets here. One fork and one vocabulary is M2's ADR; only a genuinely multi-feature direction earns a whole map.

## Step 1 – Read the inputs like the agent will

Open the M2 ADR and glossary, and skim the app's route handlers (`routes/todo_lists.py`, `routes/todos.py`). Notice what's already true: ownership is checked *inline*, single-owner. You're not re-deciding the sharing model (M2 did that) – you're zooming out to ask *what whole shape* the collaboration direction takes, and where today's code will have to split.

## Step 2 – Manual once: event-storm and carve, by hand

Before running any skill, do a quick **Big Picture event storming**. List the collaboration events in past tense, in order, and circle the *pivotal* ones (the events that change pace or ownership):

`ListCreated` → `TodoAdded` → **`ListShared`** → **`InviteAccepted`** → **`TodoAssigned`** → `DueDateApproached` → **`ReminderSent`** → `ShareRevoked`

Now cluster the pivotal events into **subdomains**, and classify each:

- **Task Management** (core?) – lists, todos
- **Sharing & Permissions** (core? supporting?) – the new bet
- **Notifications & Reminders** (supporting? generic?)
- **Identity & Access** (generic – already mocked)

Push yourself to the hard calls:

- Which is the *real* core – the established Task Management, or the new Sharing & Permissions? (It's genuinely contested. What do you do when you can't decide?)
- Name one **hotspot** – a question the events raise that you can't answer yet (e.g. *can a Viewer be assigned a todo?*).

> 💡 This is the point of the manual step: the boxes are easy, but the *pivotal events are the boundaries*, and the "which one is core?" argument is where the judgment lives. When two subdomains are both plausibly core, the honest move is to **record it as a hotspot, not force a verdict** – the domain is modest, and naming that is the skill. The tool runs this faster; it doesn't replace the call.

Keep your board and boxes; you'll compare them to what the skill produces.

## Step 3 – With AndThen: generate the map

```bash
/andthen:architecture --mode event-storming,strategic-design "collaboration direction for the todo app"
```

This **chain** is interactive. `event-storming` will present an event timeline and **ask you to confirm it** before formalizing anything – that gate is the whole point, so don't rush past it. Then `strategic-design` turns the pivotal-event clusters into a **subdomain table, sized bounded contexts, and a context map** (it reads the real single-owner code, so you get a *Current vs Target* map and the drift between them). No code changes.

```bash
/andthen:ubiquitous-language --update shared-lists
```

This lifts the contested terms into your glossary at *system* scope – extending the M2 feature-scope glossary.

If either asks you questions, that's expected and useful – it's surfacing the causality and policy gaps your event storming raised. Answer them, or record them as hotspots for the PRD.

Now compare what they produced to your hand carve:

- Did it classify the subdomains the way you did – and how did it handle the *two-cores* tension? (A good run records it as a hotspot, doesn't force one.)
- Look at the **Current vs Target context map** – it names where today's Shared Kernel (ownership checked inline) must become a Customer/Supplier seam: *the access resolver your M2 ADR already named*. A generic "design my architecture" prompt can't ground itself in *this* repo like that.
- Look at the **named patterns** on each arrow (Shared Kernel, Customer/Supplier, Conformist) – that's the difference between a diagram and a design.

> 🎨 **UI/UX track (gated):** If the direction has a UI surface, this is where a **design system** earns its keep at system scope – `/andthen:ui-ux-design --mode design-system` (tokens, components), the visual-language twin of the subdomain map. One dialog doesn't need this; a whole collaboration surface does. No UI surface? Skip it. Full track: [`track-ui-ux-design.md`](track-ui-ux-design.md).

## Step 4 – Verify the map (the real skill)

A diagram you can't act on isn't a design. Check the map against this gate:

- [ ] Every subdomain **classified** (core/supporting/generic) with a one-line *why* – not just named
- [ ] Bounded contexts **sized** – you could name one team to own each; no God-object context
- [ ] The context map names a **pattern per pair** (Shared Kernel / Customer-Supplier / Conformist / ACL), not bare arrows
- [ ] **Contested calls are recorded as hotspots**, not forced (the two-cores tension is named, not hidden)
- [ ] **UL touchpoints** flagged for the terms that mean two things across contexts (`Member` vs `Recipient`)
- [ ] **Right-sized:** this is genuinely multi-feature – if it's really one feature, you climbed one notch too high

If a *single* boundary is genuinely contested (e.g. Lists↔Collaboration: Shared Kernel vs Customer/Supplier), that one boundary – not the whole domain – earns deeper scoring:

```bash
/andthen:architecture --mode decompose "Lists vs Collaboration boundary"
```

## Step 5 – Dial check

Ask yourself: *was an event-storming + strategic-design pass the right amount of structure here?*
- For the collaboration *direction* – **yes**: genuinely multi-feature, new subdomains on top of the existing core, non-trivial integration. That earns a map before a plan.
- For a single feature – **no**: one fork and one vocabulary is M2's `/andthen:architecture --mode trade-off` + `/andthen:ubiquitous-language`. Carving contexts for one feature *is* the architecture-astronautics failure – climb *down* the dial.

Be honest: a todo app is a *modest* domain for this. That's fine – it makes the exercise legible, and "we have two plausible cores, so we record it as a hotspot" is exactly the judgment this module teaches. Right-sizing – *has this grown past one feature?* – is the judgment this whole course is about.

## Done when

You have a verified subdomain map – classified subdomains, sized contexts, a context map with named seams, and the hotspots written down – for the collaboration direction, and you can point to where it carries M2's decision (the resolver becomes a context seam) and terms forward. You'll consume it in **Module 7** with `/andthen:prd` → `/andthen:plan` – the *same* map, where the story boundaries follow the context boundaries.

---

<sub>Stuck? Describe the *symptom* to the agent ("I can't tell if Sharing is a separate context or part of Lists"), not the fix – better input, better output. Your facilitator has a reference strategic-design report to compare against.</sub>
