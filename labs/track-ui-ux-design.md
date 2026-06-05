# Cross-cutting track – UI/UX Design (gated)

> **The loop:** `clarify → design → spec → exec-spec → review` – with a design thread running *alongside* it **if your feature has a UI surface**.
> **You'll produce:** clarified flows, low-fi wireframes (a FIS input), and a validated UI – each at the loop step where it belongs. And first, you'll decide whether to run this track *at all*.

This isn't a separate module – it's a thread you weave through the modules you're already running. The catch, and the whole point: **only run it if your feature has a UI surface.** No screens to design? Skip the entire track and stay on the dial.

The worked feature is **shared lists**, and it *does* have a UI: a share dialog, a member list, permission badges, notification toasts – real Shoelace components in the `todo-app/`. So for this feature, the track is in play.

## First: the gate

Before anything, ask one question: **does this feature have a UI surface?**

- **No** (an API, a script, a logic change) → you're done with this track. Don't design screens that don't exist. Go back to the loop.
- **Yes** → continue. The four moves below slot into M1, M2, M6, and M5.

> 💡 This gate *is* the skill. Running UI/UX work on a feature with no UI is the design version of over-engineering – the same failure as writing an ADR for a typo. Most of knowing this track is knowing when to skip it.

## The four touchpoints

Each move runs **inside** its host module, on the *same* feature you're already carrying:

| In this module… | Run this | What you get |
|-----------------|----------|--------------|
| **M1 Frame & Clarify** | `/andthen:ui-ux-design --mode research "shared-lists flows"` | journeys, information architecture, flows – discovery for the *UX*, the way `clarify` does for requirements |
| **M2 Decide & Model** | `/andthen:ui-ux-design --mode wireframes "share dialog + member list"` | low-fi screens that become a **FIS input**, exactly like the ADR |
| **M6 Strategic Design** | `/andthen:ui-ux-design --mode design-system "collaboration UI"` | tokens + components at **system scope**, next to the subdomain map |
| **M5 Verify & Review** | `/andthen:ui-ux-design --mode review` + `/andthen:visual-validation` | the **UI verification lens** – the built screens checked against your wireframes |

## Manual once: design one move by hand

Before running any skill, design **the share dialog** by hand – it's the slice with the clearest UI:

- **Sketch the flow:** owner opens a list → clicks Share → enters an email → picks a role → the recipient appears. Now break it: what happens with no account? an already-shared user? sharing with yourself?
- **Wireframe it low-fi:** the fields, the **empty state**, the **error state**, the member list with permission badges. Boxes and labels – not pixels.
- **Name what's already there:** which existing Shoelace component fits? which spacing/color tokens does the app already use? Reuse before you invent.

> 💡 The point of the manual step: the hard part isn't the drawing, it's the **states the drawing forces you to confront** – the empty, error, and "already shared" paths. Those are the same edge cases Module 1's clarify surfaced, now made visual. The skill draws faster; it doesn't replace your judgment about which states exist.

Keep your sketch; you'll compare it to what the skill produces.

## With AndThen: run the move for your host step

```bash
# In Module 2, the highest-value one – wireframes become a FIS input:
/andthen:ui-ux-design --mode wireframes "share dialog + member list"
```

This reads your requirements (and the app's existing UI), and writes low-fi screens to `docs/wireframes/`. Modes also chain – `--mode research,design-system,wireframes` shares context, so flows feed the design system and tokens feed the wireframes. No code changes.

Compare to your hand sketch:
- Did it cover **every state** – empty, error, already-shared, loading – or did you miss one (or did it)?
- Look at how it **reuses the app's real Shoelace components** instead of inventing controls. A generic "design a share dialog" prompt can't see *this* codebase.
- Notice the wireframe is now a **FIS input** – in Module 3, it sits next to the ADR as something the spec inlines.

In Module 5, close the loop on the UI:

```bash
/andthen:ui-ux-design --mode review <the-implemented-ui>
/andthen:visual-validation
```

`visual-validation` screenshots the built UI and checks it against your wireframes across breakpoints – the UI half of "tests pass ≠ it works."

## Verify: the gate, then the design

- [ ] **Gate honestly:** this feature actually has a UI surface (if not, you shouldn't be here)
- [ ] **Edges designed** – empty, error, and "already shared" states exist, not just the happy path
- [ ] **Reuses the system** – existing Shoelace components/tokens before any new control
- [ ] **Wireframes are FIS-ready** – Module 3 can inline them as an input next to the ADR
- [ ] **Built UI matches intent** – `visual-validation` confirms the screens against the wireframes, across breakpoints

## Dial check

Ask: *does this UI surface earn this much design – or any?*
- A **share dialog** earns wireframes – real states, a real interaction to get right.
- A **whole collaboration surface** across many screens (Module 6 scope) earns a design system.
- An **API-only change** earns *nothing* from this track – skip it.

Same dial, same judgment as the architecture track in M2/M6 – just gated on "is there a UI?"

## Done when

For a feature with a UI surface: you've run the design move at each host step (flows in M1, wireframes into the FIS in M2, a design system in M6 if the surface is broad, validation in M5), and you can point to where each fed the *same* artifact its host module produced. For a feature with no UI surface: you correctly skipped the whole track – which is also "done."

---

<sub>Stuck? Describe the *symptom* ("the share dialog has no error state for a non-account email"), not the fix – better input, better output. Reference wireframes/tokens for shared-lists are generated in the live dogfood; your facilitator will point you at them once they exist.</sub>
