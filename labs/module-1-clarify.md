# Module 1 – Frame & Clarify

> **The loop:** **`clarify`**` → design → spec → exec-spec → review`
> **You'll produce:** a clarified requirements doc – the one that turns a fuzzy idea into something you can design and spec against – and you'll verify it's decision-ready *before* any design work.

This is where the loop *starts*. You arrive with nothing but a one-line idea, and you leave with requirements solid enough for the next modules to build on. There's no prior artifact to read – the input is just a sentence.

The worked feature is **shared lists** for the todo app. This module clarifies the *whole* feature: who can share, with whom, what a recipient can do, and – just as important – what's explicitly out.

## Before you start

The base is the `todo-app/` in this repo – auth, multiple lists, todos with priority and due dates, search, a real templated UI. That's it. **No prior module artifacts are needed** – clarify is the front of the loop, so you're starting from a blank requirements slate.

If you want to see where this is heading: the doc you produce here is what Module 2 (Decide & Model) and Module 3 (Specify) read from.

## The principle (1 minute)

Hand an agent "add shared lists" and it will build *something* – confidently, and probably not what you meant. It fills the gaps with guesses, and you find them in code or in production. Clarify adds **one cheap step**: a discovery conversation that surfaces what the idea left unsaid – the **gaps** (who? with whom? to do what?), the **edge cases** (share with a non-user? share twice?), the **scope boundaries** (what's explicitly out?), and **alternatives** you hadn't considered. That conversation's output becomes the agent's input and your checklist for the whole feature.

## Step 1 – Sit with the fuzzy idea

Your starting input is one line: *"Let people share their lists."* That's it. Resist the urge to start designing. Notice how many real decisions it quietly leaves open – who counts as someone you can share with? What can they do once they have it? When does access end? Hold those open; you're about to make them explicit.

## Step 2 – Manual once: write the clarifying questions by hand

Before running any skill, write down the **questions you'd ask** about "shared lists for the todo app." Don't answer them – *list* them. Try it cold, and push past the obvious:

- **Scope** – one list or many? The whole list, or selected todos?
- **Who** – anyone? only registered users? owner-to-owner only?
- **What can a recipient do** – view only? edit? complete? reorder? delete?
- **What's explicitly out** – inviting non-users? roles? notifications? assignment?
- **The awkward edges** – share with an email that has no account? share twice? share with yourself? revoke?

> 💡 This is the point of the manual step: the deliverable of clarify isn't a form, it's the *questions* – and knowing what to ask is the durable skill. Notice that a single one-line idea just fanned out into a dozen real decisions, most of them scope and edge-case calls you'd otherwise make by accident in code. The tool runs this interrogation faster; it doesn't replace your judgment about what matters.

Keep your list; you'll compare it to what the skill asks.

## Step 3 – With AndThen: run the discovery conversation

```bash
/andthen:clarify "shared lists for the todo app"
```

This is **interactive** – not a form. It analyzes your idea and the codebase, then asks **3–5 targeted questions per round** (scope, flows, edge cases, success criteria), usually over **2–4 rounds**, and writes `docs/specs/shared-lists/requirements-clarification.md`. No code changes happen.

**Let it do its job** – this is the part that matters:
- **Don't pre-answer everything.** When it asks a question, answer *that one* and let it push back. If you dictate every answer up front, you've skipped the discovery and just written down your first guess.
- **Answer one thing vaguely on purpose** (e.g. "anyone should be able to share") and watch it probe – it'll ask whether sharing with a non-account email means an invite flow, in or out of scope. That probe is the skill earning its keep.
- **Watch for alternatives** it raises that you didn't list (an invite flow? a workspace model?). Scope them in or out deliberately.

Now compare against your hand-written questions:
- Did it ask things you missed (or did you ask things it didn't)?
- Look at **Out of Scope** and **MVP Boundary** – notice what got parked on purpose so the first slice stays small.

## Step 4 – Verify the clarification (the real skill)

A clarification you can't act on isn't done. Check the doc against this gate:

- [ ] **Gaps closed or named** – every unknown is either answered or parked in Open Questions
- [ ] **Scope boundaries explicit** – you can say out loud what this will *not* do (invites, roles, notifications)
- [ ] **An MVP / first slice is named** – there's a smallest shippable version (view-only, registered users)
- [ ] **Edge cases surfaced** – the awkward paths (non-user, duplicate, self-share, revoke) have stated expected behavior
- [ ] **Decision-ready** – Module 2 could design and Module 3 could spec from this without guessing

> 💡 Rule of thumb: if you still can't list ~3 concrete acceptance criteria from the doc, discovery isn't finished – go another round.

If the clarification is trying to pin down *all* of collaboration at once (invites + roles + assignment + notifications), that's a signal – this is a *product*, not a feature. Name the first slice, defer the rest, and note that the full thing wants `prd → plan` (Module 7), not one giant clarification.

## Step 5 – Dial check

Ask yourself: *did "shared lists" earn a full clarify conversation?* Yes – a one-line idea that fans out into a dozen scope and edge-case forks is exactly what discovery is for. For a one-liner with no real unknowns ("rename the *Done* button to *Complete*"), no – that'd be `/andthen:quick-implement`, where the requirement *is* the sentence. Right-sizing is the judgment this whole course is about.

## Done when

You have a clarified, decision-ready `requirements-clarification.md` for shared lists – gaps named, scope boundaries explicit, an MVP slice (view-only, registered users) identified. You'll carry this *same* doc into **Module 2 (Decide & Model)**, where you'll take its biggest fork – the sharing model – into an ADR and turn its new nouns into shared language.

---

<sub>Stuck? Describe the *symptom* to the agent ("we never pinned down what a recipient can actually do"), not the fix – better input, better output. Your facilitator has a reference clarification (`solutions/module-1-shared-lists-clarification.md` in the instructor materials) to compare against.</sub>
