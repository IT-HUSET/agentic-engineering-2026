# X6 – Context, brownfield, maintenance

> **Skills:** `describe --model`, `init` (depth), `handoff`, `simplify-code`, and the `Learnings` and `Decisions` documents
> **Pull this when:** your case is a repo you did not write, or context decays between days. Playbook background: §10 and §14.

## Trigger

Pull X6 when you can point to one of these:

- **Own repo or brownfield.** There is no `docs/ARCHITECTURE.md`, no `docs/models/architecture-model.json`, or the Index in your `CLAUDE.md` points at nothing real. The agent keeps asking where things are.
- **Context rot between days.** The overnight handoff test failed: a fresh session did not know a decision or a convention you settled yesterday, or it repeats a mistake you already fixed.
- **Duplication at reflection.** After a story, the diff contains a helper that already existed, or two stories solved the same thing two ways.
- **Knowledge in a dead chat.** A trap or decision exists only in the transcript of a session you closed.

## Input

Your own case repo, or a repo you inherited. If you have neither, your facilitator names a suitable repo state, for example `todo-app/` treated as code you inherited and never read.

## Output

- A navigable project: a Document Index that routes to real files, `docs/ARCHITECTURE.md` and `docs/models/architecture-model.json`.
- Discovered requirements and decisions, **validated** by a human, with the confirmed ones promoted.
- Durable stores with homes: `docs/LEARNINGS.md`, `docs/DECISIONS.md`.
- A handoff a fresh session resumed from, and a behavior-preserving cleanup of one finished story's code.

## Steps

1. **Manual once: feel the boundary.** Two things you only learn by feeling them.
   - **The same small change twice.** Pick a change that touches one or two files (a created-at timestamp on each todo). Run it once at the end of a long, loaded session, and once in a fresh session that is given only the directly relevant files. Use `/context` before each to see how full the window is. Compare quality, speed and how much it re-explored. Write what you saw.
   - **A handoff by hand.** In `.agent_temp/x6-handoff.md` write: current state, key decisions, files changed, what's next, key constraints, open questions and dead ends. Run `/clear`, and resume from that file alone. Notice that some fields are **durable** (decisions, constraints: they belong in a permanent home) and some are **transient** (open questions, dead ends: they belong only in the resume note). That split is what `handoff` automates.
2. **Make the code legible, and keep a typed model.**
   ```text
   /andthen:describe --model
   ```
   Beyond the F1 output, `--model` also writes `docs/models/architecture-model.json`, a typed projection that records the commit it describes (suffixed `-dirty` when the tree differs). `plan`, `architecture` and `domain --mode contexts` read it. Refresh it after structural changes with `/andthen:describe --model-only`. Existing documents are merged into, never overwritten.
3. **Validate what it discovered.** Open `docs/requirements-discovered.md` and `docs/decisions-discovered.md`. Both are headed *Discovered – requires validation by team*, and each requirement carries evidence (file paths) and a confidence. Sit with a teammate and mark each item **confirm**, **correct** or **drop**. When a decision is confirmed, move it into `docs/DECISIONS.md`. A requirement set you confirm is valid input to `plan`.
4. **Go deeper with `init`.** Run `/andthen:init` again and take up the offers that fit your repo:
   - **Documents** you do not have yet: `Product` (with Proportionality facts), `Decisions`, `Learnings`, `Tech Debt`, `Roadmap`, `Ubiquitous Language`.
   - **Critical rules** in your root instruction file, which the team then owns. They travel with the checkout into CI and containers.
   - **`testing --mode strategy`** if your suite is thin, and **`visual-validation --mode setup`** if you serve a UI.
   - **Per-sub-project instruction files** for a monorepo.

   Then open the **Project Document Index** in your `CLAUDE.md`. It is a routing table that maps each document to its path and says when to read it. That table is how every skill, `handoff` and a fresh agent knows where to read and write. Keep the instruction file lean: documents are read whole, and every line is read on every turn of every session. Ask of each line whether removing it would cause a mistake.
5. **Give knowledge a home.** Take what you learned in the last working session and classify each item:
   - A non-obvious failure, with a clear scope: a `docs/LEARNINGS.md` bullet.
   - A load-bearing choice with no real alternative: a one-line *Still Current* entry in `docs/DECISIONS.md`.
   - A choice with real alternatives and consequences: an ADR, through `decide` (X1).
   - Open questions, things tried, dead ends: the handoff only.

   `handoff` routes in exactly these bins, but it only **writes** Learnings bullets. It *recommends* Decisions lines and `decide` runs, and never writes an ADR for you.
6. **Carry the context across a boundary.** After real work:
   ```text
   /andthen:handoff "next: wire the share dialog"
   ```
   Then `/clear` and `Resume from .agent_temp/handoff/handoff-<UTC-ts>.md`. The fresh session reads durable stores through the Index and the named artifacts by path. The handoff references them, it does not re-paste them.
7. **Simplify one finished story.** The agent's own reflection is where duplication shows. Pick a story marked `done`, or the files of one:
   ```text
   /andthen:simplify-code <paths from the story's commit>
   ```
   It records a check baseline first, simplifies for clarity, reuse and leanness while preserving behavior exactly, and re-runs the checks. It drops any cleanup that contradicts the governing FIS's *What We're NOT Doing* or *Architecture Decision*. Removing anything observable or exported needs your approval. A standalone run that changes a lot ends on a `Next (fresh session):` line for a `review` of the changed paths. `exec-plan` already runs one pass over a plan's code when it completes the last story, so this step is for older code or a story set you want cleaned separately.

## Verify

- [ ] The Document Index routes to files that exist, and a fresh agent could orient with no tribal knowledge.
- [ ] `docs/models/architecture-model.json` exists, and its `meta.revision` matches the commit you expect.
- [ ] Every discovered requirement and decision you rely on has been **validated by a human**. Discovered is not decided.
- [ ] Decisions are in `docs/DECISIONS.md`, traps are in `docs/LEARNINGS.md`, not in a closed chat.
- [ ] The handoff references artifacts by path, and the fresh session picked up mid-thought.
- [ ] At the start of a task you know what is in the window (`/context`), and it holds what the task needs rather than everything you have.
- [ ] After `simplify-code`: the checks pass as they did at baseline, no behavior changed, and each dropped cleanup is reported with its reason.

## Dial check

*How much context discipline does this project earn?* Size it to the project's **lifespan**, not its size today. A one-session script earns almost none: do not scaffold an index for a throwaway. A feature you will live with earns the Document Index and a lean instruction file immediately. A long-lived or inherited codebase earns the full cadence: `describe` to make it legible, `handoff` between sessions, durable stores kept current, a cleanup pass after each plan.
