# Module 3 – Specify

> **The loop:** `clarify → ` **`spec`** ` → exec-spec → review`
> **You'll produce:** a Feature Implementation Specification (FIS) – the contract for one slice of a feature – and you'll verify it *before* writing any code.

You've clarified *what* to build (Module 1) and decided *how* (Module 2: an ADR and a shared vocabulary). This module turns that into a spec an AI agent can implement and you can hold it to.

The worked feature is **shared lists** for the todo app. This module's slice: **share a list, view-only** – an owner lets another registered user *see* one of their lists without being able to change it.

## Before you start

You should have these from earlier modules, under `docs/specs/shared-lists/`:
- `requirements-clarification.md` (Module 1)
- `adr/001-sharing-model.md` and a short glossary (Module 2)

If you're joining at this module, your facilitator will point you at prepared versions.

## The principle (1 minute)

Going straight from idea to code drifts on anything non-trivial – the agent fills gaps with guesses. A spec adds **one cheap step**: write the contract first. A good FIS says *what* to build, *how you'll know it works* (acceptance scenarios), and *what it will **not** do* (scope boundaries). That document becomes the agent's input and your checklist.

## Step 1 – Read the inputs like the agent will

Open the clarification and the ADR. Notice what's already decided: the sharing model, and that view-only-with-registered-users is deliberately the *first* slice. You're not re-deciding any of that – you're specifying it.

## Step 2 – Manual once: write the acceptance scenarios by hand

Before running any skill, write **2–3 acceptance scenarios** for "share a list, view-only" in Given/When/Then form. Try it cold – push yourself to the edges:

- What happens when the owner shares with an email that isn't a registered user?
- What can the recipient *not* do? How would you observe that they can't?

> 💡 This is the point of the manual step: the format is easy, but it forces real product decisions (you just made one about non-registered emails). That thinking is the durable skill – the tool runs it faster, it doesn't replace it.

Keep your scenarios; you'll compare them to what the skill produces.

## Step 3 – With AndThen: generate the FIS

```bash
/andthen:spec docs/specs/shared-lists/
```

This reads your clarification + ADR, **analyzes the actual codebase**, and writes the FIS to `docs/specs/shared-lists/shared-lists.md`. No code changes happen.

If it asks you questions, that's expected and useful – it's finding gaps the clarification missed. Answer them, or note them as deferrals.

Now compare the generated FIS to your hand-written scenarios:
- Did it find edge cases you missed (or did you find some it didn't)?
- Look at **Code Patterns** – it references real files in *this* repo for the implementer to follow. A generic "write me a spec" prompt can't do that.
- Look at **What We're NOT Doing** – editor roles, invites, notifications, all parked on purpose.

## Step 4 – Verify the spec (the real skill)

A spec you can't verify against isn't a contract. Check the FIS against this gate:

- [ ] Every acceptance scenario is **observable** – you could click or query something to confirm it
- [ ] Each scenario traces to an expected outcome (`[OC01]` tags)
- [ ] **Scope boundaries** are explicit – you can state out loud what this won't do
- [ ] The **architecture decision** matches the ADR (it shouldn't re-open it)
- [ ] Domain terms are used consistently with your glossary
- [ ] It's **execution-sized** – one coherent feature slice, not three features hiding in a trench coat

If the FIS is secretly huge, that's a signal – the work wants more structure (`prd → plan`, Module 7), not a bigger single spec.

## Step 5 – Dial check

Ask yourself: *was a full FIS the right amount of structure here?* For view-only sharing that touches the data model and permissions – yes. For renaming a button – no, that'd be `/andthen:quick-implement`. Right-sizing is the judgment this whole course is about.

## Done when

You have a verified FIS for the view-only sharing slice, and you can point to where it carries forward the Module 1 and Module 2 decisions. You'll implement it in **Module 4** with `/andthen:exec-spec` – same spec, carried forward.

---

<sub>Stuck? Describe the *symptom* to the agent ("the scenarios don't cover X"), not the fix – better input, better output. Your facilitator has a reference FIS to compare against.</sub>
