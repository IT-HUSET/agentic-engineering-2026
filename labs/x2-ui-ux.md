# X2 – UI/UX

> **Skills:** `ui-ux-design`, `visual-validation`
> **Pull this when:** your case has a screen that does not exist yet, or a screen you must check against a design.

## Trigger

Pull X2 when the fact is in your artifacts:

- The PRD or a FIS describes a user-facing surface: a new page, dialog, form or list, in `templates/` or the equivalent for your stack.
- `clarify` asked "does design run before planning?" and your answer is recorded as a row in the PRD's *Decisions Log*, or its `Next (fresh session):` line named `ui-ux-design`. That line asks for the design-system mode first when the project has none. For one or two screens that is over-sizing: edit the pasted line to a wireframes request (step 4).
- `docs/wireframes/<feature>/` has no wireframes for a screen the plan builds.
- A built screen needs checking against a wireframe or design reference.

**The gate comes first: does this work have a UI surface?** An API, a script or a logic change earns nothing here. Designing screens that do not exist is the design version of writing an ADR for a typo.

## Input

Your team's `<feature-dir>/prd.md` (requirements as text, a file or a PRD is required). If your case has no UI, your facilitator has the shared-lists PRD: its UI surface is a share dialog and a member list, built from the Shoelace components `todo-app/` already uses.

## Output

- **Research:** a job-to-be-done sentence, the two to five primary journeys, an information-architecture sketch, constraints (accessibility, device), and open questions.
- **Wireframes:** grayscale HTML in `docs/wireframes/<feature>/` (for example `docs/wireframes/shared-lists/`), a `page-inventory.md`, one page per screen **and** state. No design-system tokens.
- **Design system (only if the surface is broad):** `docs/design-system/DESIGN.md` (tokens and rationale) and `showcase.html`.
- **Mockups (only once a design system exists):** clickable hi-fi pages in `docs/mockups/<feature>/`, built from the design system and checked for contrast, off-token values and dead links.
- **Visual validation:** `docs/VISUAL-VALIDATION.md` once per project, then findings per screen, state and viewport, each classified P1, P2 or P3.

## Steps

1. **Gate it.** Write one line: "This work has a UI surface because ____." If you cannot finish the sentence, stop here.
2. **Manual: sketch the riskiest screen by hand.** For the share dialog, in `.agent_temp/x2-sketch.md` or on paper: the fields, the **empty** state, the **error** state ("no account for that email"), the **already shared** state, and the member list with a revoke control. Then name which existing component you would reuse (look in `src/app/templates/` and `src/app/static/`) before you invent a new one. The drawing is easy. The states it forces you to confront are the skill.
3. **Flows, if they are unclear.** In a fresh session:
   ```text
   /andthen:ui-ux-design "research the shared-lists flows" <feature-dir>/prd.md
   ```
   The skill reads your phrasing to pick the mode and says which it chose, so you can redirect. If research ends with open questions it closes on `clarify`. A request for screens that names no level runs mockups while a design system exists, else wireframes. Mockups asked for with no design system run wireframes, and the skill says so.
4. **Wireframes.** In a fresh session:
   ```text
   /andthen:ui-ux-design "wireframe the share dialog and the member list, all states" <feature-dir>/prd.md
   ```
   It builds a page inventory first, then one wireframe per screen and state, then validates them at four viewports (this needs browser automation; if none is available it says validation was not run, and why). Name several modes in one request and they run in order, each feeding the next ("research, then a design system, then mockups"). If you got here from `clarify`'s "design first" line, edit it to this wireframes request instead of running the design-system mode it names.
5. **Design system, only for a broad surface.** A whole collaboration surface across many screens earns tokens and components:
   ```text
   /andthen:ui-ux-design "create a design system for the collaboration screens" <feature-dir>/prd.md
   ```
   One dialog does not. Once `DESIGN.md` exists, "mock up the share dialog and the member list" builds clickable hi-fi mockups from its tokens into `docs/mockups/shared-lists/`.
6. **Plan from the design.** The design comes **before** `plan`, so the FIS can point at the wireframes. `ui-ux-design` closes on `plan` for your requirements. If a plan already exists, re-plan the UI stories: `/andthen:plan "story S02 of <feature-dir>/plan.json – wireframes now in docs/wireframes/shared-lists/; revise its FIS"`.
7. **Set up visual validation, once.** After the app can be served:
   ```text
   /andthen:visual-validation --mode setup
   ```
   It serves the app, proves one capture, and writes `docs/VISUAL-VALIDATION.md` with the serve command, capture tooling, routes, states and breakpoints. Only what it ran successfully is written down. `exec-plan` uses this document when it validates UI work.
8. **Validate the built screens.** After a UI story is built:
   ```text
   /andthen:visual-validation "share dialog and member list, mobile and desktop" docs/wireframes/shared-lists/
   ```
   It lists every difference from the reference **before** it gives a verdict. P1 Critical and P2 Major findings block; P3 is reported. An image it cannot read is `not judged`, never passed.

## Verify

- [ ] You passed the gate honestly: there is a UI surface.
- [ ] Every screen **and state** the plan builds has a wireframe: empty, error, already-shared and loading, not just the happy path.
- [ ] The wireframes reuse the app's real components before inventing new controls. Mockups, if you made them, use the design system's tokens.
- [ ] The FIS cites the wireframes (as an asset it builds against), so the implementer does not guess the layout.
- [ ] After the build, `visual-validation` ran with no open P1 or P2 finding, and any `not judged` region is accounted for.

## Sizing check

*Does this surface earn this much design, or any?* A share dialog earns wireframes: real states, a real interaction to get right. A single field added to an existing form earns none. A whole collaboration surface across many screens earns a design system, and mockups once you want those screens approved in its look. An API-only change earns nothing from X2. Sized the same way as `decide` and `domain`, gated on one question: is there a UI?
