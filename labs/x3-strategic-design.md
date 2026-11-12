# X3 – Strategic design

> **Skills:** `domain --mode event-storming`, `domain --mode subdomains,contexts`, `visualize`
> **Pull this when:** your work spans several subdomains, or nobody can say where one module ends and the next begins. This exercise applies strategic DDD. It does not teach the theory from scratch.

## Trigger

Pull X3 when you can show one of these in your artifacts:

- The PRD or `plan.json` covers several features that touch different parts of the business (for shared lists: sharing, invites, permissions, assignment, notifications).
- Two stories in `plan.json` fight over the same files, or a story's FIS cannot name which module owns a rule.
- The same word means two things in different parts of the system (`docs/UBIQUITOUS_LANGUAGE.md` has rows in **Overloaded Terms**).
- There is no `docs/DOMAIN-MAP.md` and the project is domain-heavy rather than a CRUD tool.

**The first question is always: does this deserve a Domain Map?** A library or a CRUD tool skips it. The Domain Map is never required, and deciding whether to model is part of the exercise.

## Input

The domain-heavy case your team works on: its PRD, and `docs/UBIQUITOUS_LANGUAGE.md` if you have one. A todo app is a modest domain for this, so the stronger input is your team's own case. If you have none, your facilitator has the shared-lists collaboration direction (sharing, invites, permissions, assignment, notifications) and a prepared strategic-design report to compare against.

## Output

- An event-storm board under `docs/models/event-storms/` and a report under `.agent_temp/reviews/` (`<scope>-domain-<agent>-<date>.md`).
- `docs/DOMAIN-MAP.md`: classified subdomains with a rationale each, bounded contexts with their owning team, and an integration pattern per pair of contexts (current and target when the code exists).
- An HTML page of the map from `visualize`, in `.agent_temp/visualize/`.

## Steps

1. **Decide whether to model, in writing.** One line in `.agent_temp/x3-decision.md`: "This deserves / does not deserve a Domain Map because ____." If the answer is no, the exercise ends here, and that is a good result.
2. **Manual: storm it on paper.** List the domain events in past tense, in order, and circle the **pivotal** ones (the events that change pace or ownership). For shared lists:
   `ListCreated` → `TodoAdded` → **`ListShared`** → **`InviteAccepted`** → **`TodoAssigned`** → **`ReminderSent`** → `ShareRevoked`.
   Cluster the pivotal events into subdomains and classify each as core, supporting or generic. Note one **hotspot**: a question the events raise that you cannot answer yet (*can a viewer be assigned a todo?*). When two subdomains are both plausibly core, the honest move is to record that as a hotspot, not to force a verdict.
3. **Event storming.** In a fresh session:
   ```text
   /andthen:domain --mode event-storming "<your scope>"
   ```
   The default level is Big Picture. It presents the event timeline and asks you to confirm it before it formalizes anything. That gate is the point: you are the domain expert, not the agent. A later run on the same scope continues the board. Say "aggregates" or "tactical design" to go to Design Level instead.
4. **Subdomains and bounded contexts.** In a fresh session:
   ```text
   /andthen:domain --mode subdomains,contexts "<your scope>"
   ```
   A chain runs in order. It proposes the classification and **waits for you to confirm or correct it** before writing the Domain Map, since whether a capability sets the business apart is knowledge the code does not carry. Then it proposes contexts, owners and integration patterns, and registers them only on your explicit acceptance. On existing code it shows the **current** map next to the **target**, and the drift between them.
5. **See it.**
   ```text
   /andthen:visualize docs/DOMAIN-MAP.md "the integration patterns and where the code drifts from the target"
   ```
   It writes a self-contained HTML page and renders it before handing it over; with no browser it says the page is unchecked. The page is a derived copy and goes stale when the map changes.
6. **One contested boundary gets deeper analysis, not the whole domain.** If a single seam is genuinely contested (do Lists and Collaboration split into separate modules?):
   ```text
   /andthen:architecture --mode decompose "Lists vs Collaboration boundary"
   ```
   It scores one split-or-merge decision. If the outcome binds beyond one story, record it with `decide` (X1).
7. **Carry it into the plan.** `plan` reads the Domain Map, so story boundaries follow context boundaries. Re-plan if a plan already exists and the seams moved.

## Verify

- [ ] Every subdomain is classified (core, supporting or generic) with a one-line rationale, not just a name.
- [ ] Each bounded context is sized so you could name one team to own it, with no catch-all context.
- [ ] Each pair of contexts has a **named integration pattern**, not a bare arrow. That is the difference between a diagram and a design.
- [ ] A contested call (the two-cores tension) is recorded in the map's Open Questions or as a hotspot, not forced.
- [ ] Terms that mean two things across contexts are in the glossary's **Overloaded Terms**, spelled exactly as the map spells the context.
- [ ] The map holds no glossary terms (the glossary holds each term once), and the story boundaries in `plan.json` follow the context boundaries.

## Sizing check

*Was an event storm plus a Domain Map the right amount of structure?* This is the largest size. For a genuinely multi-feature direction with new subdomains on top of an existing core and non-trivial integration, yes. For one feature, no: one fork and one vocabulary is `decide` plus `domain --mode glossary`, and carving contexts for a single feature is over-architecture. Climb down.
