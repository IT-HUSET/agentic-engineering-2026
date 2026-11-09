# Foundation – the loop for one feature, once

> **The loop:** `[clarify →] plan → exec-plan → review --fix → ship`, with design between `clarify` and `plan` when the work earns it.
> **You'll produce:** one real feature on `todo-app/` (shared lists), from a one-line idea to an open pull request, with every step's artifact on disk and checked.

This is Day 1's foundation. You run the whole loop for **one feature, once**, on the lab app, so that in the case work you can run it on your own case and spend your attention on judgment, not on commands. Each section below is one step. Each step takes the previous step's artifact as **input**, produces one **output**, and ends with a **verify** checklist and a **sizing check**: *was that the right amount of structure?*

The worked feature is **shared lists**: an owner lets another registered user see one of their lists. The idea is deliberately fuzzy, which is the point.

| Step | Skills | Output |
|------|--------|--------|
| [F1 – Orient and set up](#f1--orient-and-set-up) | `now-what`, `init`, `describe` | A project AndThen can navigate |
| [F2 – Clarify](#f2--clarify) | `clarify` | `prd.md` |
| [F3 – Decide](#f3--decide) | `decide`, `domain --mode glossary` | An ADR and a glossary |
| [F4 – Plan](#f4--plan) | `plan` | `plan.json` and a FIS |
| [F5 – Implement](#f5--implement) | `exec-plan <FIS>` | Committed code, proven |
| [F6 – Verify and review](#f6--verify-and-review) | `review --fix` | A review report, findings fixed |
| [F7 – Ship and hand off](#f7--ship-and-hand-off) | `ship`, `handoff` | A pull request and a handoff |

## How to work through it

- **Project root is `todo-app/`.** Start Claude Code there (`cd todo-app && claude`). Every path below, such as `docs/specs/...`, is relative to it.
- **One fresh session per step.** Most pipeline steps end by printing a `Next (fresh session):` line with the full command (`init` and `decide` do so only in some cases, so use this lab's order when there is none). Run `/clear`, then paste it. Each step reads the files the previous one wrote, not the chat.
- **`<feature-dir>`** is the directory `clarify` prints for your PRD in F2 (it looks like `docs/specs/<something>/`). Write it down. Later steps use it.
- **Answer the questions.** `clarify`, `decide` and `plan` interview you, each question with a recommended answer. The recommendation is a starting point, not a default to accept unread.
- **Joining late or stuck?** Your facilitator has a prepared version of each upstream artifact (PRD, ADR, glossary, FIS). Ask for the one you need, and do not paste them over your own. For F5 you need a **bundle**, not a bare FIS: `exec-plan` requires a FIS whose `**Plan**:` and `**Story-ID**:` header points at a `plan.json` that holds that story, so ask for the FIS and its `plan.json` together.
- **Describe symptoms, not fixes**, when something is off ("the scenarios don't cover a non-registered email"). Better input gives better output.

The *Agentic Engineering Playbook* has a chapter behind each step if you want the background: F1 §6 and §10, F2 §6, F3 §5, F4 §6 and §7, F5 §6 and §11, F6 §11, F7 §6 and §14. Your facilitator has the link.

---

## F1 – Orient and set up

**Skills:** `now-what`, `init`, `describe`. You also meet **right-sizing**.

### Input

- A clone of your fork of this repo (recommended, see the [README](../README.md#get-started)), Claude Code authenticated, AndThen installed as in the [README](../README.md#get-started).
- The prep session (live or recorded).

### Steps

1. **Check the install.** Open a terminal in `todo-app/`. In Claude Code run `/plugin` and confirm `andthen` is installed. If `/andthen:` commands are unknown, restart Claude Code.
2. **Start a branch.** Everything ends in a pull request, and AndThen commits to the current branch.
   ```bash
   git switch -c feat/shared-lists
   ```
3. **Warm up: know the ground.** The first move in any agentic session is to check the tree is healthy.
   ```bash
   uv run pytest
   ./run.sh        # runs in the foreground
   ```
   Run `./run.sh` in its own terminal, open http://localhost:8000 (`demo@example.com` / `demo123`), and stop it with Ctrl-C when you're done. Click around. Lists belong to one owner. There is no sharing.
4. **Warm up: one change, no skills.** Ask the agent for something tiny and safe, for example: *"Add a short module docstring to `src/app/utils.py` explaining what it's for."* Read the diff and re-run the tests. Say out loud what it got right and what you would have done differently. You own every line. When you've formed a view, discard the change: `git restore src/app/utils.py`.
5. **Let `now-what` route a bare repo.** In Claude Code, started in `todo-app/`, run:
   ```text
   /andthen:now-what
   ```
   It inspects the project (setup, codebase, workflow state), prints the chain `clarify (optional) → plan → exec-plan → review --fix → ship`, and offers `init` because the project has no Project Document Index yet. Answer yes.
6. **`init`.** It asks nothing in an existing repository. It adds the **Project Document Index** to the `CLAUDE.md` in `todo-app/` without rewriting what is there, writes a `Key Dev Commands` document with the project's fast and full test commands, and adds two `.gitignore` entries (`.agent_temp/` and review reports). Documents already in `docs/` (see step 7) get an Index entry too. Its closing summary then offers extras one line each (role agents, critical rules, `describe`, more documents, a testing strategy, visual validation). **Ignore the offers for now.** An ignored offer writes nothing, and the catalog exercises pick them up when a case needs them.
7. **`describe`: read the map of the code.** `describe` maps an existing codebase into `docs/ARCHITECTURE.md`, `docs/requirements-discovered.md` and `docs/decisions-discovered.md`. It fans out subagents, so **do not run it here**. The output of a prepared run is already committed in `todo-app/docs/`, and your facilitator re-runs `/andthen:describe` on screen. You run it yourself on your case repo in C1. If `todo-app/docs/` is missing or empty, tell your facilitator before you go on.
8. **Learn to right-size.** Your facilitator introduces it. This is the whole course in one table:

   | Work | Path | Structure |
   |------|------|-----------|
   | A fix you can state in one sentence | `implement-fix "<request>"` → `ship` | Minimal. Unknown cause or broken build: `triage` first |
   | One real feature | [`clarify` →] `plan` → `exec-plan <FIS>` → `review --fix` → `ship` | One story: one FIS, a one-story `plan.json` |
   | Several features | [`clarify` →] `plan <dir>` → `exec-plan <FIS>` per story → `review --fix` → `ship` | Several stories, a FIS each. `plan` prints the first ready story's command and each story's report names the next. `exec-plan <dir>` runs every story in one sweep, the form for `--auto` and `--worktree` runs, and `--worktree` runs independent stories in parallel |

   The entry test: **if you can't list three acceptance criteria, start with `clarify`; otherwise start with `plan`.** `now-what` applies it for you. `--worktree` and `--auto` are switches, not sizes.

   **Proportionality** sizes the details within a size. `clarify`, `decide`, `plan` and the design skills size what they propose against three facts in `docs/PRODUCT.md`: the project's stage, its scale, and its standing technical non-goals. The first of them you run asks once if the facts are missing, and records your answers.
9. **Commit the setup.** AndThen builds on a tree you can read at a glance, so commit what `init` wrote. Stage by path, never `git add -A`:
   ```bash
   git status --short
   git add CLAUDE.md .gitignore docs
   git commit -m "Set up AndThen"
   ```
   The status should list only the files `init` wrote (the Index in `CLAUDE.md`, `.gitignore`, `docs/KEY_DEVELOPMENT_COMMANDS.md`). If something else shows up, find out why before you commit.
### Output

A project AndThen can navigate: a Document Index in `todo-app/CLAUDE.md`, `docs/KEY_DEVELOPMENT_COMMANDS.md`, the `.gitignore` entries, and the committed `describe` output in `docs/`. You are on branch `feat/shared-lists`, with the setup files committed and a clean tree.

### Verify

- [ ] `uv run pytest` passes on a clean tree. Not a formality: a green suite is what lets you trust an agent's changes later.
- [ ] `CLAUDE.md` in `todo-app/` has a `## Project Document Index` section, and every path in it that exists is real.
- [ ] `docs/KEY_DEVELOPMENT_COMMANDS.md` lists a test command, and you ran that exact command by hand and it passed.
- [ ] `.gitignore` contains `.agent_temp/`.
- [ ] In the committed `docs/requirements-discovered.md`, find one discovered requirement. Read its evidence and confidence. It is headed *Discovered – requires validation by team*: it is the code's story about itself, not yet a fact. Name one you would confirm and one you would doubt.
- [ ] You can state the entry test and the three sizes.

### Sizing check

*Did the app earn `init` and `describe`?* A throwaway script earns neither. A codebase you will live in for weeks, or one you inherited, earns both once, up front. The one-line docstring change in step 4 was the smallest size: no spec, just verify. `implement-fix` is the AndThen version of it.

---

## F2 – Clarify

**Skill:** `clarify`.

### Input

One line: **"Let people share their lists."** Nothing else. There is no prior PRD; `clarify` is the front of the loop. `todo-app/docs/PRODUCT.md` is already committed and carries a Non-Goals entry saying sharing is out. `clarify` will surface it. Contradicting it is your call, and you should say so explicitly. If the file is missing, tell your facilitator.

### Steps

1. **Sit with the fuzzy idea.** Resist designing. Notice how many decisions that one line leaves open: who can you share with, what can they do, when does access end?
2. **Manual once: write three acceptance criteria by hand.** Before running any skill, write three acceptance criteria for "share a list", in Given/When/Then form or plain sentences. Push one to an awkward edge: sharing with an email that has no account, sharing twice, sharing with yourself, revoking. Add one line on what you would leave **out**. Keep it in `.agent_temp/f2-my-criteria.md`.

   The criteria are the point, not the format. Writing them forces product decisions you would otherwise make by accident in code. The tool runs the interrogation faster; it does not replace your judgment about what matters.
3. **With AndThen: run the interview.** In a fresh session:
   ```text
   /andthen:clarify "let people share their lists"
   ```
   What to expect:
   - It states the scope (a feature, so it writes a PRD) and where the file will land.
   - If `docs/PRODUCT.md` has no Proportionality facts, it asks for all three in one question: stage, scale, standing technical non-goals. Answer honestly for the lab app (a prototype, a handful of users, one SQLite file, no external services).
   - It interviews you in rounds, each question with a recommendation first. It always asks at least one round and waits for real answers.
   - Then it plays the settled picture back and asks you to confirm it. If the scope adds screens no wireframes cover, it also asks whether design runs before planning. For now answer no; wireframes are the catalog exercise X2.
   - A fresh reviewer checks the PRD and may put Notes to you. Answer them.

   **Let it do its job.** Answer the question asked, and let it push back. If you dictate every answer up front you have skipped discovery and written down your first guess. Answer one thing vaguely on purpose ("anyone should be able to share") and watch it probe.
4. **Read the PRD.** It prints the path relative to the project root, `docs/specs/<slug>/prd.md`. That directory is your `<feature-dir>`. The PRD is the one planning file that outlives the branch, and every story is cut from it, so this is where you read it carefully.
5. **Compare with your hand-written criteria.** Did it ask things you missed, or did you ask things it didn't? The PRD writes each requirement's acceptance criteria as one rule each (`While <precondition>, when <trigger>, the system shall <response>`), with an `If <unwanted condition>, then the system shall <response>` rule per unwanted condition: compare your awkward edge with those `If` rules. Look at **Out of Scope** and the MVP boundary: what got parked on purpose so the first slice stays small?

### Output

`<feature-dir>/prd.md`, and Proportionality facts in `docs/PRODUCT.md`. The skill closes on one `Next (fresh session):` line: usually `decide`, because the sharing model is a design fork that binds beyond one story.

### Verify

- [ ] You can list at least three concrete, testable acceptance criteria from the PRD, including an `If` rule for an unwanted condition. If you can't, discovery isn't done: go another round.
- [ ] Scope boundaries are explicit. You can say out loud what this will **not** do (invites, roles, notifications).
- [ ] A smallest shippable slice is named (view-only, registered users).
- [ ] The awkward edges (non-user, duplicate, self-share, revoke) have stated expected behavior, or sit in Open Questions on purpose.
- [ ] `docs/PRODUCT.md` has a Proportionality section with stage, scale and technical non-goals.
- [ ] The PRD is **decision-ready**: someone could design and plan from it without guessing.

### Sizing check

*Did "shared lists" earn a full `clarify` conversation?* Yes. A one-line idea that fans out into a dozen scope and edge-case forks is what discovery is for. For a sentence with no real unknowns ("rename the *Done* button to *Complete*"), no: that is `implement-fix`, where the requirement is the sentence. If your clarification is trying to pin down all of collaboration at once (invites, roles, assignment, notifications), that is a product, not a feature. Name the first slice and defer the rest.

---

## F3 – Decide

**Skills:** `decide`, then `domain --mode glossary`. You apply what the Day 1 talk on working as an architect covered. This step does not re-teach it.

### Input

`<feature-dir>/prd.md` from F2. Open its *Decisions Log*, *Constraints & Assumptions* and *Open Questions*. The design fork to find: **how is "this user may see that list" modeled?** Three real options: an access grant per list, ownership at a workspace level, or an invite link.

### Steps

1. **Settle the fork with `decide`.** In a fresh session, point it at the PRD:
   ```text
   /andthen:decide <feature-dir>
   ```
   What to expect:
   - It lists the decision points and sorts each: already settled by the code or an ADR (cited, not asked), a requirement (goes back to the PRD via `clarify`), a choice that binds beyond one story or is costly to reverse (decided now), or local to one story (left to `plan`). You can add, drop or move a point.
   - A decision where no option stands out is **contested** and gets a weighted trade-off. It proposes options, criteria and weights and asks you to confirm or adjust **before** researching. That gate is the whole point, so don't rush it. It compares five options unless you name a count; say *"compare three options"* if it proposes more.
   - Each decision is labelled a **one-way or two-way door**: costly or cheap to reverse. Close options on a two-way door skip the analysis, because either pick is cheap to undo. Expect it to tell you when a fork does not earn one.
   - Before it writes anything it plays the settled set back and asks whether the ADRs go in as `Accepted` or `Proposed`. You just decided, so `Accepted`.
2. **Read the ADR.** It lands in `docs/adrs/` (`ADR-001…`) and is registered in `docs/DECISIONS.md`. Find the **Reversal** line: which kind of door is it, and what would reversing it take? Find **Alternatives Considered**: the rejected options and why, plus the floor option (do nothing, or extend what exists).
3. **Name the terms.** In a fresh session:
   ```text
   /andthen:domain --mode glossary shared lists
   ```
   It reads the code, the PRD and your ADR, pulls out the domain terms (list, owner, recipient or member, share, invitation), clusters synonyms under one canonical term, and flags words that mean two things. It merges into any existing glossary rather than overwriting it.
4. **Read the glossary.** It lands in `docs/UBIQUITOUS_LANGUAGE.md`. Look at the **Avoid** column: it bans the synonyms ("collaborator", "guest") that would otherwise drift into the spec. `plan` reads this document next.
5. **Commit the design artifacts.** `plan` and `exec-plan` start from a readable tree. Stage by path, never `git add -A`:
   ```bash
   git status --short
   git add docs
   git commit -m "Add shared-lists PRD, ADR and glossary"
   ```
   The status should list the PRD, the Proportionality update in `docs/PRODUCT.md`, the ADR, `docs/DECISIONS.md`, `docs/UBIQUITOUS_LANGUAGE.md` and any `docs/research/` trade-off files. Review reports and `.agent_temp/` are gitignored.

### Output

An ADR in `docs/adrs/` with its row in `docs/DECISIONS.md`, and `docs/UBIQUITOUS_LANGUAGE.md`.

### Verify

- [ ] The ADR's decision is one option, stated plainly, with a reason that names the criteria that decided it.
- [ ] **Alternatives Considered** includes the rejected options and the floor option, and the **Reversal** line says one-way or two-way and what reversing takes.
- [ ] `docs/DECISIONS.md` has a row for the ADR, with the status you chose.
- [ ] Glossary terms are canonical: one name per concept, banned synonyms in **Avoid**, no mechanism or rationale smuggled into a cell.
- [ ] Both are ready for the next step: the FIS can cite the ADR and use the terms verbatim.

### Sizing check

*Did this fork earn an ADR and a glossary?* For the sharing model, yes: a real fork with different long-term consequences, and new words the spec must use consistently. For renaming a button, no: no fork, no new vocabulary, straight to `implement-fix` or `plan`. Two ways to go the other direction: a question only running code can answer goes to `spike` (X1), and a tangle of subdomains and unclear boundaries across many features wants a Domain Map (X3), not one ADR.

---

## F4 – Plan

**Skill:** `plan`, run twice. Once to see how it sizes the whole PRD, then once as a single story.

### Input

`<feature-dir>/prd.md`, the ADR and `docs/DECISIONS.md`, and the glossary. `plan` reads the Index documents whose triggers match, so you don't paste any of them in.

### Steps

1. **Plan the whole PRD, and only read it.** In a fresh session:
   ```text
   /andthen:plan <feature-dir>
   ```
   `plan` decides whether the PRD is one story or several, asks about missing requirements, writes `plan.json` and a FIS per story, reviews them together, then runs a final round of open questions. **Do not run `exec-plan` on the result.** Read:
   - `plan.json`: how many stories, each one's `scope`, and the `dependsOn` edges between them. Which could run at the same time?
   - Any `OVERSIZE:` line. It means one FIS is too big for a single run; the skill asks whether to split it or keep it.
   - Where the story seams fall relative to your ADR and glossary.

   If your PRD's scope was narrow and you got one story, that is an answer too: your PRD is one story. Your facilitator shows what a several-story plan looks like on a wider scope.

   Then park the result so the next run starts clean:
   ```bash
   mkdir -p .agent_temp/whole-prd-plan
   mv <feature-dir>/plan.json <feature-dir>/s*.md .agent_temp/whole-prd-plan/
   ```
2. **Manual once: write the FIS skeleton for the slice you will build.** The slice is **share a list, view-only**: an owner lets one registered user *read* one of their lists, and can revoke. Before running the skill, write in `.agent_temp/f4-my-fis.md`:
   - **Intent**: one sentence, why this exists.
   - **Expected Outcomes**: two or three, one sentence each.
   - **Acceptance Scenarios**: three in Given/When/Then, including the awkward ones. What happens when the owner shares with an email that isn't registered? What can the recipient *not* do, and how would you observe that they can't?
   - **What We're NOT Doing**: what is parked on purpose.
   - **Tasks**: three or four, each with a `Verify` line: a command you could run or a thing you could inspect.

   The format is easy; the real decisions are in the scenarios (you just made one about non-registered emails). The tool writes it faster and grounds it in the code; it does not make the calls for you.
3. **With AndThen: plan it as one story.** In a fresh session:
   ```text
   /andthen:plan "<feature-dir>/ as one story: share a list view-only with a registered user, and revoke"
   ```
   "As one story" overrides the sizing: a vertical slice that fits one fresh-context run is one story. Expect a requirements round, a self-review by a fresh reviewer, and a final round of open questions that closes with `Decided:` and `Assumed:` lists. Read them: each open item is listed with what settled it. The skill writes no code.
4. **Compare with your skeleton.** Did it find edge cases you missed, or the other way round? Look at how it grounds tasks in real files in this repo (routes, models, templates), and at **What We're NOT Doing** and **Architecture Decision**, which should point at your ADR.

### Output

`<feature-dir>/s01-<name>.md` (the FIS) and a one-story `<feature-dir>/plan.json` beside it, with story `S01` `pending`. (Story IDs and scenario IDs both start at `S01`; this lab always says "story S01" or "scenario S03" to keep them apart.) The skill closes on `Next (fresh session): /andthen:exec-plan <fis-path>`.

### Verify

A spec you can't verify against isn't a contract.

- [ ] Every acceptance scenario is **observable**: you could click or query something to confirm it, and it has a way to be proved, either a bound `Proof` on an existing test or a task `Verify` with a `cmd:` or `inspect:` form.
- [ ] Each scenario traces to an Expected Outcome (`[OC01]` tags).
- [ ] **What We're NOT Doing** is explicit; you can say what this won't do.
- [ ] The **Architecture Decision** matches your ADR instead of reopening it, and the FIS uses your glossary's terms.
- [ ] It is **execution-sized**: no unresolved `OVERSIZE:`, one coherent slice rather than three features in a trench coat.
- [ ] `plan.json` has one story, story `S01`, `status: pending`, `dependsOn: []`.

### Sizing check

*Was a FIS the right amount of structure?* For view-only sharing, which touches the data model and permissions: yes. For renaming a button: no, that is `implement-fix`. The other direction matters just as much: if the FIS comes out secretly huge, with unrelated scenarios and several demos hiding in it, climb to several stories rather than writing a bigger spec. That is what step 1 showed you.

---

## F5 – Implement

**Skill:** `exec-plan <FIS>`.

### Input

The FIS and `plan.json` from F4. Start on `feat/shared-lists` with `uv run pytest` green and `git status` showing nothing but the F4 bundle (`plan.json` and the FIS), which `exec-plan` commits with the story. If anything else is uncommitted, commit it by path first.

### Steps

1. **Read the FIS the way the agent will.** Open `<feature-dir>/s01-<name>.md`. Read one task and its `Verify` line. The FIS tells you what to build and how to check it. You own the intent and the boundaries; the agent owns the code inside them.
2. **Run it.** In a fresh session, paste the line `plan` printed:
   ```text
   /andthen:exec-plan <feature-dir>/s01-<name>.md
   ```
   There is no hand-implementation step here: the loop you would do by hand (change, run the check, repeat) is what the skill runs, task by task. Watch for:
   - **Tasks in FIS order**, each passing its `Verify` before the next. Tests are written through the `testing` skill.
   - **Falsifiability**: a test must fail when the behavior it protects is removed.
   - **The full proof run.** After the tasks it runs the project's checks and every proof the FIS names, and keeps one line per proof: what ran, the exit status, the runner's own result line.
   - **A fresh reviewer.** It spawns a reviewer that did not write the code (`review --quick --fix`) over the story's changes.
   - **Commit.** A commit with a brief subject and `Story-ID:` and `Plan:` trailers, and the story's row in `plan.json` set to `done`. Each finished story then gets one `simplify-code` pass over its code, as a separate `refactor` commit carrying the story's trailers.
   - **The report.** It ends with a `Reviewed:` line (what reviewed the change, what stays open), a Chain Attestation (one sentence per Expected Outcome), and `Next (fresh session):`.

   If it stops on a red gate, that is work to finish, not a caveat. A failed story ends with a route out: `review --fix` over the story's changed paths, then `exec-plan` again on the same FIS.
3. **Read what it learned.** Open the `## Implementation Observations` section at the bottom of the FIS: traps, drift from the spec, things it noticed but did not touch. In the case work this is the **reflection between stories**: before the next FIS runs, you check it against what this story taught you.

### Output

The slice in code, committed. `plan.json` shows story `S01` as `done` with a `verified` summary.

### Verify

The agent attested. You still check, and it is cheap because the FIS says exactly what to check.

- [ ] In `plan.json`, story `S01` is `status: done` and `verified.summary` quotes a **run** check: the command, its exit status, and the runner's own result line. "Looks right" and an exit code alone don't count.
- [ ] **Run that command yourself.** Same result?
- [ ] `git log -3` shows the story commit with `Story-ID: S01` (the story) and `Plan:` trailers (and a `refactor` commit from the simplify pass each done story gets). `git status` is clean: you started with only the F4 bundle uncommitted, and `exec-plan` committed it with the story.
- [ ] Every task is checked in the FIS and none is checked without a passing `Verify` behind it.
- [ ] The report's `Reviewed:` line says a fresh reviewer looked, and you know what it left open.

> **Tests pass is not it works.** Green tests prove the scenarios you *wrote* in F4. Whether those were the right and complete scenarios is F6's question. If a scenario could not be proved because it was written un-observably, fix the *spec*, then re-run.

### Sizing check

*Was `exec-plan` on a FIS the right amount of structure?* For a feature with a real FIS and tasks across the data model and permissions: yes, you want the task-by-task proof loop. For a one-sentence change there is no FIS to execute, and `implement-fix` gives you the same verify discipline without a contract. Several stories would mean `exec-plan` on each story's FIS in turn, a fresh session each, or `exec-plan <dir>` to run every story in one sweep (the form for `--auto` and `--worktree` runs).

---

## F6 – Verify and review

**Skill:** `review --fix`.

### Input

The committed slice from F5, `plan.json` (story `S01` done) and the FIS. Re-read the FIS's **Acceptance Scenarios**: that is your independent checklist, not the agent's attestation.

### Steps

1. **Manual once: hunt for a gap yourself.** Pick the acceptance scenario where a recipient must **not** be able to change a view-only list, *including by sending the request directly* (in the reference FIS this is scenario S03; yours may be numbered differently). Your repo ships no planted bug. The hunt is a test of your own implementation, in three moves, from a clean tree:
   - **Try it as the viewer, bypassing the UI.** Open the mutating handlers (`src/app/routes/todos.py`, `src/app/routes/todo_lists.py`). Then send a mutating request as the recipient directly: replay an owner's request from the browser's network tab with the viewer's session cookie (*copy as cURL*), or write a few lines in a scratch test with the test client. Does the server refuse it (403), or is the only thing stopping a viewer a hidden button in the template?
   - **Read the scenario's test.** Does it drive the **route**, or only click the UI? A test that only clicks the UI never asked the real question.
   - **Falsify the test.** Comment out the server-side check in one handler, run `uv run pytest`, then put it back with `git restore <file>`. Red means a test protects the rule. **Green means the suite is lying**: it asserted what the UI shows, not the invariant the server must hold.

   Either outcome is useful. If the server refuses and the test goes red, you have confirmed the rule by evidence, which is what review will also do. If not, you found the gap yourself. Reading code against the contract is the durable skill; the tool confirms it faster. Keep your notes for step 3.
2. **With AndThen: run the plan-level review.** In a fresh session, paste the line `exec-plan` printed:
   ```text
   /andthen:review --fix <feature-dir>/plan.json
   ```
   Review runs in a fresh reviewer that did not write the code, against the FIS and PRD as the intent baseline. It picks the lenses itself and typically chains them: `code`, `gap` (does it match the FIS), `security` where its trigger fires (this diff touches authorization), and `outcome` (does it solve the PRD's problem). It proves coverage before it gives a verdict, then routes each finding **Fix** (mechanical, safe to apply) or **Note** (surfaced for you). `--fix` then applies the Fix findings in one round, with no re-review. The report is written beside `plan.json` and is gitignored by default.
3. **Compare the report with your hunt.** Did review prove the bypass you suspected, citing the unguarded handler? Did it confirm the scenarios that genuinely pass, and correctly dismiss things you parked in **What We're NOT Doing** (no "you forgot editor roles")?
4. **Settle the rest.** Open `## Remediation Status` in the report. Fix findings are resolved or deferred with a reason. **Note** findings are untouched until you decide: fix it, or defer it on purpose. A Fix blocked by an open decision lands in `docs/TECH-DEBT-BACKLOG.md` after you approve it. If the report ends on a `Next (fresh session):` follow-up review (it fixed a CRITICAL or HIGH finding, so a session that did not apply the fixes should re-read), run it.

   Resist "while I'm here" cleanup. Findings are routed, not a flat to-do list. If you spot something out of scope, surface it; don't bundle it in.
5. **Re-run the checks yourself** after the fixes: `uv run pytest`.

### Output

A review report beside `plan.json`, the Fix-routed findings applied in your working tree (the skill leaves them uncommitted; `ship` commits them), and a report that ends on a `Next (fresh session):` line for `ship`.

### Verify

- [ ] The overall readiness is **Ready** and no CRITICAL or HIGH finding is open. A *deferred* one counts as open. If a Note you chose to keep holds readiness back, you can say why.
- [ ] Every acceptance scenario traces to evidence that was actually run, in the report's coverage matrix, and you spot-checked one.
- [ ] The direct-request path is refused server-side, and a test that drives the route would fail if the check were removed.
- [ ] Every **Fix** finding is resolved with evidence, and every **Note** is decided by you, not waved through.
- [ ] No fix crept past the FIS (no editor roles, no notifications).
- [ ] `uv run pytest` passes after the fixes, and you can say in one sentence how much you trust this change and why.

### Sizing check

*Was a full `review` the right weight?* For an authorization-bearing feature touching mutating routes, yes: a missed enforcement check is a real vulnerability, so you want spec fit, code, and security together. For a one-line copy tweak mid-flow, a full report is overkill: `review --quick` gives one pass's findings inline. Match the review weight to the risk of the change. If the feature has a UI surface, the UI lens is `visual-validation` (X2).

---

## F7 – Ship and hand off

**Skills:** `ship`, `handoff`.

### Input

A reviewed branch: `plan.json` with story `S01` done, a clean review, and the `Next (fresh session):` line for `ship` that `review` printed. The pull-request target is your fork of this repo.

### Steps

1. **Look before you ship.** `git status` and `git log --oneline`. The plan bundle (`plan.json` and the FIS) is tracked, because `exec-plan` committed it with the story.
2. **Run `ship`.** In a fresh session:
   ```text
   /andthen:ship <feature-dir>/plan.json
   ```
   What it does, in order:
   - **Checks for open work** (a story not done, an open CRITICAL or HIGH finding) and asks once whether to ship anyway.
   - **Lands what the FIS learned.** It reads each FIS's `## Implementation Observations` and writes the real traps as `docs/LEARNINGS.md` bullets. The rest it *recommends* (a `Decisions` line, a `decide` run); it does not write them for you.
   - **Writes the pull request** for a reviewer deciding whether to merge: the intent, the outcomes, the proof of each (from `verified.summary`), the review's verdict, and whether the change is a **one-way or two-way door** and what breaks if it is wrong. It also names where a reviewer should read closely and what stays open, and ends on a fixed `## Ship summary` section.
   - **Commits** the review's fixes still in your working tree and the Learnings.
   - **Asks once before anything leaves the machine**: base branch, the commits leaving, the title and the body. For a ready plan the same question asks whether to **delete `plan.json` and the FIS** (they govern one branch and never merge), recommending deletion.
3. **Read the PR text before you say yes.** Does it put what the merge decision needs first? Could a reviewer who never saw your chat tell what the change is for, and how it was proved? With your fork as the target, accept the recommended delete and say yes. Without a fork, say no: the skill prints the title, the body and the commands to run later, and deletes nothing. (`ship --auto` stops before anything leaves the machine and prints the same commands.)
4. **Check the aftermath.** `docs/LEARNINGS.md` has the new bullets, and `git log` shows the Learnings commit. If you said yes: the bundle's deletion is committed before the push, `git ls-files <feature-dir>` shows only `prd.md` (a `ls` would also show the review report, which is gitignored), and `prd.md` gains a `> **Shipped**: ...` header line. If you said no, the bundle is still there and nothing is stamped.
5. **Hand off.** A session that has to end mid-work, or the end of a day, is a boundary your context does not survive. Run:
   ```text
   /andthen:handoff "next: frame my case repo – init, describe, test command"
   ```
   It sorts what the session knows by durability. Defensive knowledge goes to `docs/LEARNINGS.md`. A structural decision with real trade-offs is *recommended* to `decide`, never written as an ADR. Everything transient goes into `.agent_temp/handoff/handoff-<UTC-ts>.md`: next focus, where we are, open questions, what was tried, the recommended next skill, and an Index of artifacts by path. Secrets are redacted, but the file is not private.
6. **The handoff test.** This is the check that your artifacts, not your chat, carry the work. Run `/clear` (or open a new session), and paste the resume line the skill printed:
   ```text
   Resume from .agent_temp/handoff/handoff-<UTC-ts>.md
   ```
   Then ask: *"What is the state of the shared-lists work and what is the next step?"* The fresh session should answer correctly from the handoff and the files it points to, without you retyping any context. If it can't, the handoff is missing something: fix the handoff, not the prompt.

### Output

An open pull request (or its title, body and commands ready), new `docs/LEARNINGS.md` bullets, a branch whose plan bundle is deleted (if you pushed), and a handoff a fresh session resumed from.

### Verify

- [ ] The PR body states intent, outcomes, proof per outcome, and door type with blast radius, before any per-story detail.
- [ ] If you said yes: `plan.json` and the FIS are gone from the branch; `prd.md` remains and carries a `> **Shipped**:` line. You know why: specs govern one branch and never merge, so the PR body and the PRD carry the intent afterwards. If you said no, the bundle is intact.
- [ ] Each new Learnings bullet traces to an Implementation Observation you can find in the FIS in git history.
- [ ] The handoff names artifacts **by path**; it does not paste them.
- [ ] The fresh session passed the handoff test.

### Sizing check

*Did the change need `ship`'s full close-out?* For a plan: yes. For a one-sentence fix: `implement-fix` then `ship`, which just commits and opens the PR with no bundle to land. When the plan is not ready, `ship` asks whether to keep the bundle and recommends keeping it while it opens the PR without the close-out, which is the per-story PR case. `handoff` is for a session that must end mid-work or has grown heavy; a short task that finishes in one sitting needs none.

---

## What's next

You have run the whole loop once, and it ends at a pull request. The case work is the same loop on a case you are handed or one of your own, with your sizing choices written down and a gate at each artifact. You repeat F1 on the case repo as the first part of C1. See [`labs/README.md`](README.md).
