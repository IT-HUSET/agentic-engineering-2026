# X3 – Strategic design

**What you do:** map your case's domain. You run an event storm, split the domain into subdomains and bounded contexts, and record who owns what in a Domain Map.

**Why it matters:** when nobody can say which module owns a rule, stories collide over the same files and one word drifts to mean two things. The map gives each rule one home.

**What you have at the end:** an event-storm board, `docs/DOMAIN-MAP.md` with subdomains, contexts and how they integrate, and a page that draws it. Or a written decision that your case does not need one, which is a valid result.

> **Skills:** `domain --mode event-storming`, `domain --mode subdomains,contexts`, `visualize` · This exercise applies strategic DDD. It does not teach the theory from scratch.

## When to pull it

Pull X3 when one of these is true for your case:

- **Your case spans several parts of the business.** For shared lists: sharing, invites, permissions, assignment and notifications. *Check:* the PRD or `plan.json` covers features like these.
- **Stories fight over the same files,** or a FIS cannot say which module owns a rule. *Check:* the stories in `plan.json` and the work areas in each FIS.
- **One word means two things** in different parts of the system. *Check:* rows under **Overloaded Terms** in `docs/UBIQUITOUS_LANGUAGE.md`.
- **The project is domain-heavy and has no map.** *Check:* there is no `docs/DOMAIN-MAP.md`, and the case is more than a CRUD tool.

**Skip it** for a library or a CRUD tool. The Domain Map is never required, and deciding whether to model is part of the exercise.

## Input

The domain-heavy case your team works on: its PRD, and `docs/UBIQUITOUS_LANGUAGE.md` if you have one. A todo app is a modest domain for this, so the stronger input is your team's own case. If you have none, your facilitator has the shared-lists collaboration direction (sharing, invites, permissions, assignment, notifications) and a prepared strategic-design report to compare against.

## Output

- An event-storm board under `docs/models/event-storms/` and a report under `.agent_temp/reviews/` (`<scope>-domain-<agent>-<date>.md`).
- `docs/DOMAIN-MAP.md`: classified subdomains with a rationale each, bounded contexts with their owning team, and an integration pattern per channel between contexts that exchange data (current and target when the code exists).
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
- [ ] Each pair of contexts that exchange data has a **named integration pattern**, one row per channel, not a bare arrow. That is the difference between a diagram and a design.
- [ ] A contested call (the two-cores tension) is recorded in the map's Open Questions or as a hotspot, not forced.
- [ ] Terms that mean two things across contexts are in the glossary's **Overloaded Terms**, spelled exactly as the map spells the context.
- [ ] The map holds no glossary terms (the glossary holds each term once), and the story boundaries in `plan.json` follow the context boundaries.

## Sizing check

*Was an event storm plus a Domain Map the right amount of structure?* This is the largest size. For a genuinely multi-feature direction with new subdomains on top of an existing core and non-trivial integration, yes. For one feature, no: one fork and one vocabulary is `decide` plus `domain --mode glossary`, and carving contexts for a single feature is over-architecture. Climb down.
