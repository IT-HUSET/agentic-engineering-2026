---
title: Foundation Lab
tab: Foundation Lab
token: lab
order: 8
depends_on: [shared/icons.md]
source: labs/foundation.md
---

# Foundation Lab

Eyebrow: Labs · Part 1

## Run the Core Loop for one feature, once

Component: "Core Loop" in the title is set in the accent colour.

You build one real feature on the course's todo app, shared lists, from a one-line idea to a merged pull request. Every step leaves a file on disk that the next step reads, and ends with a checklist and a sizing check.

Component: under the lead, three facts as small labelled chips, then a link button.

- Project root: `todo-app/`
- Branch: `feat/shared-lists`
- Feature: shared lists, an owner lets another registered user see one of their lists

Button: Read the full lab on GitHub → (https://github.com/IT-HUSET/agentic-engineering-2026/blob/main/labs/foundation.md)

## How to work through it

Component: one compact box holding a bulleted list, worded as in labs/foundation.md. Each item opens with a bold lead-in. The two commands under the first item are a tight numbered list. No cards, numbers or tip box.

- **Project root is `todo-app/`.** Start Claude Code there, from the repository root:
  1. `cd todo-app`
  2. `claude`

  Every path in the lab, such as `docs/specs/...`, is relative to it.
- **One fresh session per step.** Most steps end with a `Next (fresh session):` line. Run `/clear`, then paste it. Each step reads the files the previous one wrote, not the chat.
- **`<feature-dir>`** is the folder `clarify` prints for your PRD in F2, such as `docs/specs/<slug>/`. For example, if it prints `Wrote docs/specs/shared-lists/prd.md`, your `<feature-dir>` is `docs/specs/shared-lists/`. Write it down, because later steps use it. The copy boxes on the step cards use the reference run's folder, `docs/specs/let-people-share-their-lists/`: if yours differs, replace it when you paste.
- **Answer the questions.** `clarify`, `decide` and `plan` interview you, each question with a recommended answer. The recommendation is a starting point, not a default to accept unread.
- **Joining late or stuck?** Your facilitator has a prepared PRD, ADR, glossary and FIS. For F5, ask for the FIS together with its `plan.json`.

## The seven steps (F1–F7)

Interactive component: a rail of the seven steps, F1 to F7, with "/clear" between them and each step's output under its pill. Arrow keys move along the rail. Selecting a step shows its card, tinted by the step's Tint: the step number, Skills, Title, Input, a green start rule, the Steps as a numbered list, then a side column with the Output box (icon, title, text), a green start rule, the commands with copy buttons, any Prompt as plain text with no copy button, any Stop line as a red rule across the column with the stop icon before its text (the Steps list then carries a bare red rule at the same point). The start rules are 3 px in the green accent, the Stop rules 3 px in red; when the columns sit side by side, each pair is drawn level, the higher rule moving down, and any Example link, in their order, then, when the step has a Studio field, a lavender "In AndThen Studio · optional" box with the Studio command and its copy button, the text and a link to the Studio tab, the Verify checklist and the Sizing check, and Previous / Next buttons. Each command box starts hidden behind a "Show command" button, as on the Setup tab.

Component: Verify items are checkboxes. Ticks are remembered in this browser only. A progress line above the rail counts the ticks across all steps, with a Reset button. Each pill shows its own count when at least one box is ticked.

Hint under the card: Pick a step on the rail, or use the arrow keys. Tick the checks as you go; they stay in this browser.

### F1 – Orientation and set up

- Tint: rust
- Skills: now-what, init, describe
- Input: A clone of your own repo, created from the course repo, Claude Code signed in, and AndThen installed as in the Setup tab.
- Output: folder · A project AndThen can navigate · A Document Index in CLAUDE.md, the Key Dev Commands document and two .gitignore entries, committed on your branch.
- Command: `git switch -c feat/shared-lists` (1. Start a branch)
- Command: `uv run pytest` (2. Check the tree is healthy)
- Command: `./run.sh` (2. Start the app in its own terminal; stop it with Ctrl-C)
- Command: `bash run.sh` (2. Or this, if ./run.sh won't start, for example on Windows)
- Prompt: Add a short module docstring (comment) to the file `src/app/utils.py` explaining what it's for. (3. Ask Claude Code; a prompt, not a shell command)
- Command: `git diff --stat` (3. See how big the change is)
- Command: `git diff src/app/utils.py` (3. Read the diff)
- Command: `uv run pytest` (3. Re-run the tests)
- Example: 3. Worked example: how to judge the diff → (warmup)
- Command: `git restore src/app/utils.py` (3. Discard the change when you're done)
- Stop: **Stop.** Go on only when `git status --short src/` prints nothing and `uv run pytest` is green: from step 4 on, AndThen reads and writes this tree, so start it from a clean baseline.
- Command: `/andthen:now-what` (4. From todo-app/, let it route the repo, and say yes to init)
- Command: `/andthen:init` (5. now-what will suggest init; or run it yourself)
- Command: `ls docs/KEY_DEVELOPMENT_COMMANDS.md` (5. Check the F1 verify point: CLAUDE.md has a Project Document Index, and its paths are real)
- Example: 5. Worked example: what the Index looks like → (index)
- Example: 7. Worked example: right-sizing shared lists → (dial)
- Command: `git status --short` (8. See what init wrote: only CLAUDE.md, .gitignore and docs/KEY_DEVELOPMENT_COMMANDS.md should show up)
- Command: `git add CLAUDE.md .gitignore docs` (8. Stage by path, never git add -A)
- Command: `git commit -m "Set up AndThen"` (8. Commit the setup)
- Command: `git log --oneline -1` (8. Check the commit: the latest one should be Set up AndThen)
- Command: `git status --short` (8. Check the tree: no M or A lines left, only ?? for local files)
- Studio command: `andthen_studio` (After step 5: start it in a terminal of its own, from todo-app/, and leave it running for the whole lab)
- Studio: Project home shows what the Document Index points at. Expand Project documents and open Key Dev Commands from the sidebar. 0 plans is right for now, and Models stay empty: `describe` wrote no model here.

Steps:

1. **Start a branch.** Everything ends in a pull request, and AndThen commits to the current branch: `git switch -c feat/shared-lists`.
2. **Warm up (A): know the ground.** Run `uv run pytest`. Then start the app in its own terminal with `./run.sh` or `bash run.sh`, open http://localhost:8000 (demo@example.com / demo123) and click around. Lists belong to one owner, and nothing is shared. Stop it with Ctrl-C.
3. **Warm up (B): one change, no skills.** Ask the agent for something tiny and safe, such as a module docstring in `src/app/utils.py`. Read the diff and re-run the tests, then discard it with `git restore src/app/utils.py`.

   Stop line: a bare red rule, level with the Stop line in the side column.

4. **Let `now-what` route a bare repo.** Run `/andthen:now-what` in Claude Code, started in `todo-app/`. It prints the Core Loop and offers `init`; answer yes. (Started in the repository root instead, it reads the root `CLAUDE.md`, and `init` writes the Index there: restart in `todo-app/`.)
5. **`init`.** It asks nothing here. It adds the Project Document Index to `CLAUDE.md`, with short Overview, Guidelines and Key Development Commands sections, writes the Key Dev Commands document and adds two `.gitignore` entries. `PRODUCT.md` and `ARCHITECTURE.md` get an Index entry too. Ignore the extra offers in its summary for now.
6. **`describe`: read the map of the code.** Don't run it here. Read the prepared output in `docs/` while your facilitator runs it on screen. If `todo-app/docs/` is missing or empty, tell your facilitator before you go on.
7. **Learn to right-size.** Learn the three sizes and the entry test: if you can't list three acceptance criteria, start with `clarify`; otherwise start with `plan`.
8. **Commit the setup.** Stage by path, never `git add -A`: `git add CLAUDE.md .gitignore docs`, then `git commit -m "Set up AndThen"`.

Verify:

- `uv run pytest` passes on a clean tree.
- `CLAUDE.md` has a Project Document Index, and its paths are real.
- `docs/KEY_DEVELOPMENT_COMMANDS.md` lists a test command, and you ran it by hand.
- `.gitignore` contains `.agent_temp/`.
- You picked one discovered requirement you would confirm and one you would doubt.
- You can state the entry test and the three sizes.

Sizing check: Did the app earn `init` and `describe`? A codebase you will live in for weeks earns both once, up front. A throwaway script earns neither.

### F2 – Clarify

- Tint: red
- Skills: clarify
- Input: One line, "Let people share their lists." Nothing else.
- Output: doc · prd.md · The PRD in your feature folder, plus the Proportionality facts and the amended Non-Goal in docs/PRODUCT.md.
- Text: 2. Write three acceptance criteria by hand, in .agent_temp/f2-my-criteria.md
- Example: 2. Worked example: three acceptance criteria → (criteria)
- Stop: **Stop.** Go on only when your three criteria are in `.agent_temp/f2-my-criteria.md`: once `clarify` starts asking, yours can no longer be written unanchored.
- Command: `/andthen:clarify "let people share their lists"` (3. Run the interview, in a fresh session)
- Text: 3. Scope: ask for the whole sharing direction in phases, with view-only sharing as the first slice. Leave how access is modeled for F3
- Command: `ls docs/specs/` (4. Find your <feature-dir>)
- Example: 4. Worked example: where the PRD lands → (prd)
- Text: 5. Check the Non-Goal in docs/PRODUCT.md, and ask the agent to amend the Value Propositions line and the Decisions Log row that still keep lists private
- Command: `git add docs CLAUDE.md` (6. Optional: commit the PRD now. Stage by path; CLAUDE.md sits outside docs/)
- Command: `git commit -m "Add shared-lists PRD"` (6. Optional: commit the PRD, PRODUCT.md and the new Index lines)
- Studio: Reader: open `prd.md` under Requirements. Jump with the section list to Out of Scope and Open Questions for step 6. Pin a note on a section you doubt: copy your notes as markdown into the comparison, or send them and let `clarify` revise the PRD, then commit it again.

Steps:

1. **Sit with the fuzzy idea.** Resist designing. Who can you share with, what can they do, and when does access end?
2. **Manual: write three acceptance criteria by hand.** Before any skill runs, keep them in `.agent_temp/f2-my-criteria.md`. Push one to an awkward edge: an email with no account, sharing twice, sharing with yourself, revoking. Add one line on what you would leave out.

   Stop line: a bare red rule, level with the Stop line in the side column.

3. **With AndThen: run the interview.** In a fresh session, run `clarify`. Answer the questions and let it push back. Answer one thing vaguely on purpose and watch it probe. Its first scope is the smallest MVP: ask instead for the whole sharing direction (sharing, invitations, roles, notifications) in phases, with view-only sharing between registered users as the first slice, and leave how access is modeled for F3. A fresh reviewer then usually puts Notes to you, some blocking: answer them, they are often real contradictions with the code.
4. **Read the PRD.** It lands in `docs/specs/<slug>/prd.md`, and that folder is your `<feature-dir>`: write it down. The PRD outlives the branch, so read it carefully. It is long for a one-line idea: start with the MVP boundary, Out of Scope and the `If` rules.
5. **Check the Non-Goal, then finish the job.** `clarify` curates the Non-Goals in `docs/PRODUCT.md`, so the sharing bullet should now be narrowed to what you still reject, or gone. Two lines outside that section are still yours: the Value Propositions line "Lists stay private to their owner" and the Decisions Log row that says the same. Ask the agent to amend them, so the whole product document agrees with the PRD.
6. **Compare with your hand-written criteria.** What did it ask that you missed, and the other way round? The PRD writes each criterion as a rule (`While …, when …, the system shall …`), with an `If …, then the system shall …` rule per unwanted condition: compare your awkward edge with those. Read Out of Scope: what was parked so the first slice stays small?

Verify:

- You can list three testable acceptance criteria from the PRD, including an `If` rule for an unwanted condition.
- You can say what it will not do: invites, roles, notifications.
- A smallest shippable slice is named: view-only, registered users.
- The awkward edges have an expected behavior, or sit in Open Questions on purpose.
- `docs/PRODUCT.md` has stage, scale and technical non-goals, and no longer says sharing is out.

Sizing check: Did shared lists earn a full `clarify`? Yes, one line fans out into a dozen forks. A sentence with no real unknowns goes to `implement-fix`.

### F3 – Decide

- Tint: cream
- Skills: decide, domain --mode glossary
- Input: The PRD from F2, and the design fork in it: how is "this user may see that list" modeled?
- Output: seal · ADR + glossary · An ADR in docs/adrs/ with its row in docs/DECISIONS.md, and docs/UBIQUITOUS_LANGUAGE.md.
- Command: `/andthen:decide docs/specs/let-people-share-their-lists` (1. /andthen:decide <feature-dir>: settle the fork, in a fresh session)
- Text: 2. Read the ADRs in docs/adrs/ and their rows in docs/DECISIONS.md, then the PRD's Open Questions line, which now names the ADR
- Stop: **Stop.** Go on only when you can name the ADR's Reversal line and the floor option it turned down: the glossary names what the ADR settled, so a wrong ADR spreads into every term.
- Command: `/andthen:domain --mode glossary shared lists` (3. Name the terms, in a fresh session. It asks nothing and prints no Next line)
- Text: 4. Read the glossary in docs/UBIQUITOUS_LANGUAGE.md, and its Avoid column
- Command: `git status --short` (5. See what F2 and F3 wrote: the PRD, the PRODUCT.md changes, the ADR, DECISIONS.md, the glossary and CLAUDE.md)
- Command: `git add docs CLAUDE.md` (5. Stage by path; CLAUDE.md sits outside docs/, so name it)
- Command: `git commit -m "Add shared-lists PRD, ADR and glossary"` (5. Commit the design artifacts)
- Command: `git status --short` (5. Check the tree: no M or A lines left, only ?? for local files)
- Studio: Reader: open the ADR under Architecture decisions and find Alternatives Considered in its section list, and the Reversal line under Consequences. Explain a section you can't place. Decisions and Ubiquitous Language are in the sidebar.

Steps:

1. **Settle the fork with `decide`.** Point it at the PRD. Confirm how it sorts the decision points, then the options, criteria and weights before it researches; that gate is the point. After the research it recommends one option: accept it, refine it or go deeper. You just decided, so the ADR goes in as `Accepted`.
2. **Read the ADR.** It lands in `docs/adrs/` with a row in `docs/DECISIONS.md`. Find the Reversal line, a one-way or a two-way door, and Alternatives Considered, including the floor option. Then open the PRD: its Open Questions line on the sharing model now names the ADR, with its own text intact.

   Stop line: a bare red rule, level with the Stop line in the side column.

3. **Name the terms.** In a fresh session, run the glossary for shared lists. It asks nothing and prints no `Next` line.
4. **Read the glossary.** It lands in `docs/UBIQUITOUS_LANGUAGE.md`. Its Avoid column bans the synonyms the spec must not use.
5. **Commit the design artifacts.** Stage by path, never `git add -A`: `git add docs CLAUDE.md`, because the Index in `CLAUDE.md` gained lines too. Then `git commit -m "Add shared-lists PRD, ADR and glossary"`.

Verify:

- The ADR states one option, with the criteria that decided it.
- Alternatives Considered includes the floor option, and Reversal names the door type.
- `docs/DECISIONS.md` has a row for the ADR.
- The PRD's Open Questions row for the sharing model names the ADR, and reads as before otherwise.
- The glossary has one name per concept, with banned synonyms under Avoid.

Sizing check: Did this fork earn an ADR? For the sharing model, yes. A question only running code can answer goes to `spike` instead.

### F4 – Plan

- Tint: green
- Skills: plan
- Input: The PRD, the ADR and the glossary. plan finds them through the Index, so you paste nothing in.
- Output: stack · FIS + plan.json · One FIS for the vertical slice and a one-story plan.json, with story S01 pending. A vertical slice is a thin piece of the feature through every layer (data, routes, UI, tests) that you can demo on its own.
- Command: `/andthen:plan docs/specs/let-people-share-their-lists` (1. /andthen:plan <feature-dir>: plan the whole PRD, in a fresh session. The slowest run of the day: write your skeleton in step 2 while it works. Don't run exec-plan on it)
- Example: 1. Worked example: what plan wrote → (plan-files)
- Text: 1. Then park it: move plan.json and the FIS files to .agent_temp/whole-prd-plan/, and keep prd.md
- Example: 1. Worked example: where the parked plan goes → (parked)
- Text: 2. Manual: write your own FIS skeleton in .agent_temp/f4-my-fis.md
- Example: 2. Worked example: a hand-written FIS skeleton → (fis)
- Stop: **Stop.** Go on only when your own skeleton is in `.agent_temp/f4-my-fis.md` and the whole-PRD plan is parked: once `plan` writes its FIS, yours can no longer be written unanchored.
- Command: `/andthen:plan "docs/specs/let-people-share-their-lists/ as one story: share a list view-only with a registered user, and revoke"` (3. /andthen:plan "<feature-dir>/ as one story: …": plan the vertical slice as one story, in a fresh session. Read the Decided: and Assumed: lists it closes with)
- Command: `git status --short` (3. Check the tree: plan.json and the vertical slice's FIS are the only new files under docs/. prd.md may show M: step 5 deals with it)
- Text: 4. Compare the FIS with your skeleton, and check that its Architecture Decision points at your ADR
- Example: 4. Worked example: which files to compare → (compare)
- Command: `git diff docs/specs/let-people-share-their-lists/prd.md` (5. Before F5, don't skip this: did planning change the PRD, such as which refusal a request gets?)
- Command: `git add docs/specs/let-people-share-their-lists/prd.md` (5. If it changed and you agree, stage the PRD by path)
- Command: `git commit -m "Amend shared-lists PRD from planning"` (5. Commit the PRD change)
- Command: `git status --short` (5. Check the tree: under docs/, only plan.json and the s01 FIS are uncommitted. exec-plan commits them with the story)
- Text: 5. Then tick off Verify below against the FIS, above all: every scenario has a proof and traces to an Expected Outcome, and plan.json has one story, S01, pending
- Studio: Plan board: after step 1, the whole-PRD plan shows its stories as columns with their dependsOn edges. Count them before you park it; parked in `.agent_temp/`, it leaves the board. After step 3 the board shows one story, S01, pending: open it to read the FIS.

Steps:

1. **Plan the whole PRD, and only read it.** In a fresh session, run `plan` on your `<feature-dir>`. It drafts the stories a batch at a time, so this is the slowest run of the day: start it, then write your skeleton in step 2 while it works. Its final round can ask twenty questions or more: take the recommendations unless one is wrong. Read how many stories it makes, their `dependsOn` edges, any `OVERSIZE:` line (a well-cut plan has none), and whether S01 is a walking skeleton, the thinnest end-to-end path the other stories build on. Then move `plan.json` and the FIS files to `.agent_temp/whole-prd-plan/`. `prd.md` stays, and a requirement the final round changed stays in it until step 5. (AndThen may then suggest `exec-plan`. Don't run it: this plan is only for reading.)
2. **Manual: write your own FIS skeleton.** In `.agent_temp/f4-my-fis.md`: intent, outcomes, three scenarios, what you are not doing, and tasks with a Verify line.

   Stop line: a bare red rule, level with the Stop line in the side column.

3. **Plan the vertical slice as one story.** In a fresh session, run `plan` with the vertical slice. Read the `Decided:` and `Assumed:` lists it closes with; `Assumed:` stays empty when you answered every item. (AndThen may then suggest `exec-plan`. That is F5, after step 5.)
4. **Compare the FIS with your skeleton.** What did it add that you missed, and the other way round? Check that its Architecture Decision points at your ADR.
5. **Commit any PRD change, and tick off Verify.** F5 starts with nothing uncommitted but the bundle. Read `git diff <feature-dir>/prd.md`: if planning changed it and you agree, commit it by path. Leave `plan.json` and the FIS uncommitted: `exec-plan` commits them with the story. Then tick off Verify below against the FIS: every scenario has a proof and traces to an Expected Outcome, and `plan.json` has one story, S01, `pending`.

Verify:

- Every acceptance scenario is observable and has a proof.
- Each scenario traces to an Expected Outcome.
- What We're NOT Doing is explicit.
- The FIS follows your ADR and uses your glossary's terms.
- No unresolved `OVERSIZE:`, and plan.json has one story, S01, pending, with no dependencies.

Sizing check: Was a FIS the right amount? For sharing that touches the data model and permissions, yes. If it comes out secretly huge, split it into stories instead of writing a bigger spec.

### F5 – Implement

- Tint: teal
- Skills: exec-plan
- Input: The FIS and plan.json from F4, with uv run pytest green and nothing else uncommitted: exec-plan commits the two with the story.
- Output: code · Code + tests · The vertical slice committed, and story S01 done in plan.json with a verified summary.
- Command: `pwd` (1. Check where you are: the path should end in todo-app)
- Command: `cd todo-app` (1. If it doesn't, move there from the repository root)
- Text: 2. Read ### Implementation Tasks in the FIS before you run it: one task and its Verify line
- Example: 2. Worked example: one task and its Verify line → (task)
- Stop: **Stop.** Go on only when you can say what one task's Verify line proves, and only the FIS and `plan.json` are uncommitted: `exec-plan` builds and commits the whole story in one run.
- Command: `/andthen:exec-plan docs/specs/let-people-share-their-lists/s01-shared-lists.md` (3. /andthen:exec-plan <feature-dir>/s01-<name>.md: run the FIS, in a fresh session. Use the Next line at the very end of its report)
- Text: 4. Read ## Implementation Observations at the end of the FIS, <feature-dir>/s01-<name>.md: review fixes, DRIFT lines, NOTICED BUT NOT TOUCHING
- Example: 4. Worked example: what to point out → (observations)
- Command: `./run.sh` (5. The browser check is yours: start the app from todo-app/ and open http://localhost:8000. Stop it with Ctrl-C)
- Text: 5. Or, in the Claude desktop app, ask Claude: start the app here and open it in the browser panel
- Text: 5. Sign in as demo@example.com / demo123. In a private window of your own browser, sign up a second user with an @example.com email
- Text: 5. As the demo user, share a list from its settings (the pencil). Reload the other window, check "Shared with me", then revoke
- Studio: Plan board, left open during step 3: S01 moves to done when the run commits, without a reload. Then open S01 for its FIS and the diff of its changes. Read and write notes, but send none while the run is going.

Steps:

1. **Start in `todo-app/`.** `exec-plan` runs from the project root, and the FIS path is relative to it. In the fresh session, run `pwd`: if it doesn't end in `todo-app`, run `cd todo-app` from the repository root first.
2. Read the FIS the way the agent will: one task and its Verify line.

   Stop line: a bare red rule, level with the Stop line in the side column.

3. **Run it.** Your session writes the code task by task, each passing its check before the next, so this is the long part. Then come the full proof run, a quick review by a fresh reviewer (findings, not a verdict: that is F6) and one simplify pass, which may add a `refactor` commit. Use the `Next` line at the very end of the report.
4. **Read what the run left in the FIS.** Open `<feature-dir>/s01-<name>.md`, i.e. `docs/specs/let-people-share-their-lists/s01-shared-lists.md` in `todo-app/` – the same file you passed to `exec-plan` – and scroll to its last section, `## Implementation Observations`, with `## Discovered Requirements` above it if the run found a requirement the spec missed. It holds what the reviewer found and how it was fixed, each `#### DRIFT` line, if any, where the code knowingly differs from the spec (no DRIFT section means the run claims the code matches the spec, a claim F6 tests), the small tidies made on the way, `NOTICED BUT NOT TOUCHING` items left for later, and any check that did not run. Read the plain bullets too: a small reinterpretation can sit in one of them. For each, decide: accept it, take it to F6, or leave it for later. `ship` in F7 keeps what is worth keeping and drops the FIS.
5. **Run the browser check yourself.** Green tests are not the same as seeing it work, and the proof run records a check that needs a person in a browser as not run: that one is yours. From `todo-app/`, start the app with `./run.sh`, or, in the Claude desktop app, ask Claude to start it and open it in the browser panel. Use two users: sign in as the demo user, `demo@example.com` / `demo123`, in one window, and sign up a new user in a private window of your own browser, since the browser panel's tabs share one sign-in. Give the new user an `@example.com` email: registration refuses `.test`. As the demo user, open a list's settings with the pencil and share it with the new user's email. Reload the other window: the list sits under "Shared with me", with no change controls. Revoke, reload again, and it is gone. Stop the server with Ctrl-C, or ask Claude to stop it if Claude started it.

Verify:

- Story S01 is done, and verified.summary quotes a check that ran: command, exit status, result line.
- You ran that command yourself and got the same result.
- `git log -3` shows the `Story-ID: S01` and `Plan:` trailers, a `refactor` commit if the simplify pass changed something, and `git status` is clean.
- S01's `completedTaskIds` in plan.json lists every task, each with a passing proof line in the report.
- In the browser, the recipient can read the shared list but not change it, and loses it after a revoke.
- The `Reviewed:` line says a fresh reviewer looked, and you know what it left open.

Sizing check: Tests pass is not it works. Green tests prove the scenarios you wrote. Whether they were the right ones is the question for F6.

### F6 – Verify and review

- Tint: lav
- Skills: review --fix
- Input: The committed vertical slice (one thin piece of the feature through data, routes, UI and tests), plan.json with S01 done, and the FIS's acceptance scenarios as your own checklist.
- Output: checklist · Review report · Findings sorted into Fix and Note, with the Fix ones applied and committed.
- Text: 1. Verify yourself: how could a viewer send a change without the button? Then find what refuses it, in the routes and in tests/test_sharing.py
- Command: `uv run pytest` (2. Make one change route's check let a viewer through, then run the tests from todo-app/: at least one must fail)
- Example: 2. Worked example: the three moves in the reference run → (falsify)
- Command: `git restore src/app/routes/todos.py` (2. Put the check back with git restore <file>, where <file> is the file you changed. In the reference run:)
- Stop: **Stop.** Go on only when `git status --short src/` prints nothing: the review must read your real check, not the one you changed.
- Command: `/andthen:review --fix docs/specs/let-people-share-their-lists/plan.json` (3. /andthen:review --fix <feature-dir>/plan.json: run the review, in a fresh session from todo-app/. Compare its report with what you found)
- Example: 3. Worked example: what the review left behind → (review-output)
- Text: 4. Decide every Note in the report yourself: fix it, record it as tech debt, or drop it. No "while I'm here" cleanup
- Command: `/clear` (5. Does the report end on Next (fresh session): /andthen:review …? Then start a fresh session)
- Command: `/andthen:review --fix docs/specs/let-people-share-their-lists/plan.json` (5. /andthen:review --fix <feature-dir>/plan.json: then run the follow-up review from todo-app/)
- Command: `uv run pytest` (6. No fix round left? Run the tests yourself from todo-app/)
- Text: 7. PASS, or FAIL with a Remediated line and every finding resolved, and a Next line for ship? Go to F7. Otherwise read what still blocks it
- Studio: Review report: open it under Review reports. The verdict, the finding index, the coverage matrix to spot-check a scenario, and Remediation Status at the end. A follow-up review shows up as a second report beside the first.

Steps:

1. **Look for a gap yourself:** can a viewer change a view-only list by sending the request directly? Check that the server refuses it, not just a hidden button. One thing is not your bug: a stranger gets 403 on todo routes but 404 on list routes. That predates the feature (`GAP-D08` in `docs/requirements-discovered.md`).
2. **Falsify the test.** Change the server-side check on one change route so that it lets a viewer through – for example, use the read check instead of the owner check. Keep the code running: commenting the check out only crashes the route, and a crash fails tests for the wrong reason. Run `uv run pytest`: at least one test must fail. Then put the check back with `git restore`. Green means the suite is lying.

   Stop line: a bare red rule, level with the Stop line in the side column.

3. **Run the review**, and compare its report with what you found. One reviewer runs every lens in one long pass, the heaviest step for your quota. The report is not all it leaves. With `--fix` it applies the Fix findings in one round, commits the verified change by path, and marks each finding's outcome under `## Remediation Status` at the end of the report. A finding you defer goes into `docs/TECH-DEBT-BACKLOG.md` once you approve it. The skill's final output, not the report, ends on the `Next` line: a follow-up review in a fresh session when it fixed a CRITICAL or HIGH finding, else `ship`. Your report will not match the reference run: other findings, other severities, maybe no fix at all. Steps 4–7 are the same whatever it found.
4. **Decide every Note yourself.** The run ends on one question covering every Note: slow down here. Fix it, record it as tech debt, or drop it. Resist "while I'm here" cleanup.
5. **Run the follow-up review, if the report asks for one.** Does the run end on `Next (fresh session): /andthen:review … --fix`? Then type `/clear` (or open a new session) and paste that line from `todo-app/`. The session that applied a fix is not the one to judge it. The follow-up checks the fixes. No follow-up line means skip to step 6.
6. **Run `uv run pytest` yourself** from `todo-app/`, once no fix round is left. The agent ran the tests too; this is your own check of its claim, and a run before a later fix round no longer counts.
7. **Go on to F7 when the last report says PASS**, or FAIL with a `**Remediated**:` line under its title and every finding behind it resolved, and the output ends on `Next (fresh session):` for `ship`. Otherwise its verdict and `## Remediation Status` say what still blocks it: an open CRITICAL or HIGH finding, a deferred one included. Settle that first.

Verify:

- The last report says PASS, or FAIL with a Remediated line and every finding resolved; no CRITICAL or HIGH finding is open; the output ends on a Next line for ship.
- Every scenario traces to evidence that ran, and you spot-checked one.
- A direct request from a viewer is refused server-side, and a test would fail without the check.
- Every Fix is resolved, and every Note is decided by you.
- Any follow-up review the report asked for has run, and `uv run pytest` passes after the last fix round.

Sizing check: A full review fits a change to authorization on mutating routes. A one-line copy tweak needs only `review --quick`.

### F7 – Ship and hand off

- Tint: rust
- Skills: ship, handoff
- Input: A reviewed branch: plan.json with S01 done, a clean last review, and the Next line for ship it printed. The pull request goes to your own repo.
- Output: pr · Pull request + handoff · A merged pull request, new Learnings, and a handoff a fresh session can resume from.
- Command: `git status --short` (1. From todo-app/: what is uncommitted? Usually nothing: review --fix committed its fixes)
- Command: `git log --oneline main..HEAD` (1. The commits that will leave your machine)
- Command: `git ls-files docs/specs/let-people-share-their-lists` (1. git ls-files <feature-dir>: tracked are prd.md, plan.json and the FIS. The review report is gitignored)
- Stop: **Stop.** Go on only when step 1 looks right: `ship` commits what is left, then asks once before it pushes and deletes `plan.json` and the FIS.
- Command: `/clear` (2. Start a fresh session)
- Command: `/andthen:ship docs/specs/let-people-share-their-lists/plan.json` (2. /andthen:ship <feature-dir>/plan.json: paste the Next line from F6's last report, from todo-app/)
- Text: 3. Does it name open work? Answer no and go back to F6. Otherwise read which Learnings it writes and what it only recommends
- Text: 4. Before you say yes, read the PR text: intent, outcomes, proof of each, one-way or two-way door, where to read closely, what stays open, and the Ship summary
- Text: 4. Your own repo as the target? Accept the recommended delete and say yes. A clone of the course repo? Say no: it prints the title, the body and the commands. No remote? Answer keep
- Text: 4. Didn't push? Copy the title and body into .agent_temp/f7-pr.md now: the PR text exists only in this session
- Command: `git ls-files docs/specs/let-people-share-their-lists` (5. git ls-files <feature-dir>: only prd.md is left, with a Shipped line at the top)
- Command: `git log --oneline --stat -3` (5. The Learnings commit and the deletion of plan.json and the FIS)
- Prompt: Show the Implementation Observations of the deleted FIS from git history next to the new bullets in docs/LEARNINGS.md. (5. Ask Claude Code; each new bullet should trace to one)
- Stop: **Stop.** Go on only when each new Learnings bullet traces to an observation in the deleted FIS: once the branch is merged and deleted, that history is gone from your clone.
- Text: 6. Merge on github.com: open the pull request, choose Squash and merge, confirm, then Delete branch
- Command: `gh pr merge <PR URL> --squash --delete-branch` (6. Or from here, with the URL ship printed)
- Command: `git switch main` (6. After a merge on github.com, update your clone: you are still on the feature branch)
- Command: `git pull` (6. Bring the squash commit into your main)
- Command: `git branch -D feat/shared-lists` (6. Delete the local branch. -D, because git does not see the squash commit as the same changes)
- Stop: **Stop.** Go on only when `git status -sb` prints `## main...origin/main` and `git branch` no longer lists `feat/shared-lists`: the handoff should describe the merged work. Didn't push, so no merge? Go on.
- Command: `/andthen:handoff "next: frame my case repo – init, describe, test command"` (7. Hand off, then open the file it writes under .agent_temp/handoff/)
- Command: `/clear` (8. Start a fresh session)
- Prompt: Resume from .agent_temp/handoff/handoff-<UTC-ts>.md (8. Paste the resume line handoff printed, with its timestamp)
- Prompt: What is the state of the shared-lists work and what is the next step? (8. Then ask, without retyping any context)
- Studio: Walkthroughs: before you merge in step 6, produce a walkthrough of the pull request by its number, or of the range `main...feat/shared-lists`. It is an agent run: give it a few minutes. Then go through its focus points and mark each file reviewed. After a `ship` that deleted the bundle, the home page shows 0 plans.

Steps:

1. **Look before you ship.** From `todo-app/`, run `git status --short`, `git log --oneline main..HEAD` and `git ls-files <feature-dir>`. The tree should be clean: `exec-plan` and `review --fix` committed their work, and `ship` leaves alone anything it cannot tie to the branch. The log is what will leave your machine: the story commit, any `refactor` commit and the review's fixes. `plan.json` and the FIS are tracked, because `exec-plan` committed them with the story. The review report is not, because it is gitignored.

   Stop line: a bare red rule, level with the Stop line in the side column.

2. **Run `ship` in a fresh session.** Type `/clear` (or open a new session) and paste the `Next (fresh session):` line from F6's last report, from `todo-app/`.
3. **Read what it does before it asks.** First it checks for open work: a story not done, or an open CRITICAL or HIGH finding, a deferred one included. If it names any, answer no and go back to F6. Shipping past a blocker is a decision, not a default. Then it lands what the FIS learned: the real traps in `## Implementation Observations` become `docs/LEARNINGS.md` bullets, and the rest it only recommends, such as a `Decisions` line or a `decide` run. It commits the Learnings and anything still uncommitted. Then it asks once before anything leaves the machine: the base branch, the commits leaving, the title and the body, and, for a ready plan, whether to delete `plan.json` and the FIS, which govern one branch and never merge. It recommends deleting them. `prd.md` stays.
4. **Read the PR text before you say yes.** Once the FIS is deleted and the review report stays local, the PR is where the intent survives. Check that it puts the merge decision first: what the change is for, the outcomes, the proof of each (`verified.summary` and the review's verdict), whether it is a one-way or a two-way door and what breaks if it is wrong, and what it knowingly leaves open, such as the findings you deferred to tech debt. It names where a reviewer should read closely and ends on a `## Ship summary` section. The proof comes from `verified.summary`, written before F6's fixes, so its test count can be lower than your last run: the PR should say so. Could a reviewer who never saw your chat tell what it is for and how it was proved? Then answer. Your own repo as the target: accept the recommended delete and say yes. A clone of the course repo, which you cannot push to: say no, and `ship` prints the title, the body and the commands, and deletes nothing. No remote at all: answer keep. Didn't push? Copy the title and body into `.agent_temp/f7-pr.md` now: the PR text exists only in this session.
5. **Check what it left.** If you said yes: `git ls-files <feature-dir>` shows only `prd.md`, which gains a `> **Shipped**:` line at the top (`ls` also shows the gitignored review report), and `git log --oneline --stat -3` shows the Learnings commit and the deletion of `plan.json` and the FIS. If you answered keep, the bundle stays with a `shipped` marker. Open `docs/LEARNINGS.md` and read the new bullets: often only one passes the test for a durable trap, and the output says why it left out the rest. The FIS is gone from the branch but not from history, so ask Claude to show its observations next to them: each bullet should trace to one.

   Stop line: a bare red rule, level with the Stop line in the side column.

6. **Merge the pull request.** GitHub does not let you approve your own pull request, and your own repo needs no approval, so merging is the decision. Merge on github.com or with `gh` from here: both give the same result. The web page is the recommendation: you see exactly what gets merged, you pick the merge method with one click, and it is how most teams work. Choose **Squash and merge**, confirm, and click **Delete branch**. The branch becomes one commit on `main`, and `plan.json` and the FIS, added and deleted on the branch, never reach `main`'s history. That is why step 5 comes first: once the branch is gone, the FIS lives on only in the pull request on GitHub. From here, `gh pr merge <PR URL> --squash --delete-branch` does the same with the URL `ship` printed. Then update your clone, because you are still on the feature branch: `git switch main`, `git pull`, and `git branch -D feat/shared-lists`. The last one needs `-D`, because git does not see the squash commit as the same changes. Merged with `gh … --delete-branch`? It has already switched you to `main` and deleted the local branch, so run only `git pull`. Didn't push? Skip this step.

   Stop line: a bare red rule, level with the Stop line in the side column.

7. **Hand off.** Run `handoff` with the next focus. It sends durable knowledge to `docs/LEARNINGS.md`, recommends a `decide` run for a structural decision instead of writing an ADR, and writes the rest to `.agent_temp/handoff/handoff-<UTC-ts>.md`: the next focus, where you are, open questions, what was tried, the next skill, and an index of artifacts by path. Open the file: it should name artifacts by path, not paste them. Secrets are redacted, but the file is not private.
8. **Test the handoff.** Type `/clear` (or open a new session), paste the `Resume from …` line `handoff` printed, and ask what the state of the shared-lists work is and what the next step is. The fresh session should answer from the handoff and the files it points to, without you retyping anything. If it can't, fix the handoff, not the prompt.

Verify:

- The PR body states intent, outcomes, proof per outcome, and door type with blast radius, before any per-story detail.
- If you said yes: plan.json and the FIS are gone from the branch, and prd.md remains with a Shipped line.
- Each new Learnings bullet traces to an Implementation Observation in the FIS in git history.
- If you pushed: the pull request is squash-merged, and your clone is on an up-to-date `main` with the feature branch deleted.
- The handoff names artifacts by path instead of pasting them.
- A fresh session resumed from the handoff alone.

Sizing check: A plan earns the full close-out. A one-sentence fix runs `implement-fix`, then `ship`. A short task that finishes in one sitting needs no handoff.

## Worked example: judging the warm-up diff

Component: a dialog with the id `warmup`, opened by the Example link on the F1 card. Eyebrow "F1 · Step 3", a Close button, then the content below. The diff is shown as a code block with removed lines and added lines in two colours. The five questions are a numbered list, each with a "Check" line and a "Here" line. Good and Less good sit side by side, and stack on a narrow screen.

Asked to "Add a short module docstring to src/app/utils.py explaining what it's for", one agent run returned the diff below. Your agent's answer will differ; the questions stay the same.

```diff
-"""Shared utility functions for templates and routes."""
+"""Shared utility functions for templates and routes.
+
+Due-date checks (is_overdue, is_due_today) and date formatting for display
+and for HTML date inputs (format_date, format_date_input). The route modules
+register them as Jinja template globals.
+"""
```

### Five questions

1. **Did it do what I asked?** Check: compare it with your instruction, word for word. Here: partly. You asked for a short docstring, but one already existed, and the agent extended it without asking.
2. **Is it true?** Check: test every claim against the code. Here: yes. The function names exist (`grep -n "^def" src/app/utils.py`), and the Jinja registration is in three route files.
3. **Did it stay in scope?** Check: `git diff --stat` lists only the files and lines you expected. Here: yes. Only the docstring in one file changed, and no code.
4. **Does it fit its surroundings?** Check: look at the code around it, its style, length and tone. Here: doubtful. Every other docstring in the file is one line, and this one runs to six.
5. **Did anything break?** Check: `uv run pytest`. Here: no, 58 passed.

### Good

- Everything it says is true and checked.
- The change is small and stays in one file.
- No logic changed, and the tests pass.
- It kept the old line instead of overwriting it.

### Less good

- **It didn't ask.** With a docstring already there, the best answer might have been "There is one already. Do you want me to extend it?"
- **It repeats the code.** The function names are now in the code and in the docstring. Add a function, and the docstring is wrong unless someone remembers to update it.
- **"Short" was read generously.** It is longer than every other docstring in the file.

What I would have done: left the existing line alone, or added at most one sentence on why the module exists, not what it contains.

The point of the exercise: you own every line, even when the agent wrote it. The five questions come back at full scale in F6, when `review` judges a whole feature.

## Worked example: the Project Document Index

Component: a dialog with the id `index`, opened by the Example link on the F1 card, built like the warm-up example. Eyebrow "F1 · Step 5", a Close button, then the content below. The two Index listings are dark code blocks; in the second, the note saying which skill adds each line is muted. How to read an entry is a short definition list.

After `init`, `todo-app/CLAUDE.md` has a `## Project Document Index` section. Agents read it to find the project's documents, and skills add a line to it each time they create one.

### Right after init

```markdown
## Project Document Index

Documents here are read whole when their trigger matches, so keep them short ...
Create a document that does not exist yet, and its entry here, from
`project-document-templates.md`, or through a subagent ...

- **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: dev, test, build, deploy commands. Read before running verification; update when a command changes.
- **Agent Temp** – `.agent_temp/`: scratch workspace for reviews, research, and QA; never ship from it.
```

The two paragraphs are rules for the agent: read a document only when its trigger matches the task, and create a missing one from AndThen's template, with its line here. Only two entries exist yet, because only those two exist.

### How to read an entry

- **Name**, such as `Key Dev Commands`: what the skills look for, so it never changes.
- **Path**: where the file lives, relative to `todo-app/`.
- **What it holds**: one line on the content.
- **When**: the trigger, such as "Read before running verification". The agent opens the file only then, not all the time.

### How it grows

Each skill appends its line when it creates a document. After F1 to F3 the list looks roughly like this:

```markdown
- **Product** – `docs/PRODUCT.md`: vision, personas, non-goals ...        ← clarify, F2
- **Specs & Plans** – `docs/specs/<version-or-feature>/`: prd.md, plan.json, one FIS per story ...   ← clarify / plan, F2 and F4
- **Decisions** – `docs/DECISIONS.md`: ADR index and Still Current notes ...   ← decide, F3
- **ADRs** – `docs/adrs/`. Read the ADR a decision cites before revisiting it ...   ← decide, F3
- **Ubiquitous Language** – `docs/UBIQUITOUS_LANGUAGE.md`: canonical terms and the synonyms to avoid ...   ← domain --mode glossary, F3
- **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: ...   ← init, F1
- **Agent Temp** – `.agent_temp/`: ...   ← init, F1
```

The wording comes from AndThen's templates; the shortened lines above only show the shape.

### Check it

The F1 check "its paths are real" means every path in the Index exists. Run `ls docs/KEY_DEVELOPMENT_COMMANDS.md` from `todo-app/`. `.agent_temp/` need not exist yet: the first skill that writes there creates it.

## Worked example: right-sizing shared lists

Component: a dialog with the id `dial`, opened by the Example link on the F1 card, built like the other worked examples. Eyebrow "F1 · Step 7", a Close button, then the content below. The three sizes are a three-column table that scrolls sideways on a narrow screen. The entry test sits in a highlighted box. The two questions under "How big is the work?" are a definition list.

There are three sizes, and the entry test tells you where to start. Here is the reasoning for this lab's feature.

### The three sizes

| Work | Path | Structure |
|------|------|-----------|
| A fix you can state in one sentence | `implement-fix` → `ship` | Minimal |
| One real feature | [`clarify` →] `plan` → `exec-plan` → `review --fix` → `ship` | One FIS and a one-story `plan.json` |
| Several features | the same chain, with `plan <dir>` | A FIS per story; independent stories can run in parallel |

The entry test: if you can't list three acceptance criteria, start with `clarify`; otherwise start with `plan`.

### 1. How big is the work?

- **Can you state it as a fix in one sentence?** No. It touches the data model, permissions and the UI.
- **Is it several separate features?** No. It is one thing: sharing a list.
- **Size:** one real feature, the middle size.

### 2. Start with clarify or plan?

Ask yourself: can I list three testable acceptance criteria right now? All you have is one line, "Let people share their lists". Try to write three criteria and you hit open questions at once:

- Who can you share with: only registered users, or any email address?
- What can the recipient do: read, change, or delete?
- What happens when you share twice, or with yourself?
- How and when does sharing end?

Until those are answered, three criteria won't hold. So you start with `clarify`: it interviews you and writes a PRD. Had the answers existed already, say in a tracker item, you would start with `plan`.

### Compare: a one-sentence fix

A bug such as "Creating a todo leaves priority empty instead of low" fits in one sentence, with one clear right answer. That is the smallest size: `implement-fix`, then `ship`, with no spec.

Not sure which size? `/andthen:now-what` applies the entry test for you.

## Worked example: three acceptance criteria

Component: a dialog with the id `criteria`, opened by the Example link on the F2 card, built like the other worked examples. Eyebrow "F2 · Step 2", a Close button, then the content below. The criteria file is a dark code block with a Copy button, so it can be pasted straight into the file.

One way to write them, in `.agent_temp/f2-my-criteria.md`. Yours may differ; the point is to make the decisions on purpose, before any skill runs.

```markdown
# Share a list – my acceptance criteria

1. Share with a registered user
   Given I own the list "Groceries" and bob@example.com has an account
   When I share "Groceries" with bob@example.com
   Then Bob sees "Groceries" among his lists and can read its todos

2. The recipient can only read
   Given Bob can see my shared list "Groceries"
   When Bob tries to add, change or delete a todo in it,
        in the UI or by sending the request directly
   Then the change is refused and the list stays as it was

3. Awkward edge: an email with no account
   Given no account exists for carol@example.com
   When I share "Groceries" with carol@example.com
   Then I see "No user with that email" and nothing is shared

Out of scope: inviting people without an account, edit rights, notifications.
```

### What to notice

- **Each criterion is a decision.** Registered users only, read-only, and a clear answer for an unknown email. Writing them forced those calls.
- **Each one is testable.** Given sets up the state, When is one action, Then is something you can observe.
- **Criterion 2 covers the direct request**, not just a hidden button. F6 comes back to exactly that.
- **Other edges you could pick:** sharing the same list twice, sharing with yourself, revoking access.

Keep the file. In step 5 you compare it with the PRD that `clarify` writes.

## Worked example: where the PRD lands

Component: a dialog with the id `prd`, opened by the Example link on the F2 card, built like the other worked examples. Eyebrow "F2 · Step 4", a Close button, then the content below. The project tree is a dark code block with muted notes; its lines never wrap, and it scrolls sideways on a narrow screen.

`clarify` prints the path when it is done, such as `Wrote docs/specs/shared-lists/prd.md`. That folder is your `<feature-dir>`: write it down, because F3 to F7 all take it.

```text
todo-app/
├── CLAUDE.md                          ← the Index gains lines for the new documents
├── docs/
│   ├── KEY_DEVELOPMENT_COMMANDS.md    from init in F1
│   ├── PRODUCT.md                     new: stage, scale, technical non-goals
│   └── specs/
│       └── shared-lists/              ← your <feature-dir>
│           └── prd.md                 ← the PRD
├── src/
└── tests/
```

The folder name is chosen by `clarify`, so yours may differ from `shared-lists`. Run `ls docs/specs/` from `todo-app/` to see it.

In F4, `plan` writes `plan.json` and the FIS (`s01-….md`) into the same folder. In F7, `ship` deletes those two and keeps `prd.md`: the PRD is the one planning file that outlives the branch.

## Worked example: what plan wrote

Component: a dialog with the id `plan-files`, opened by the Example link on the F4 card, built like the other worked examples. Eyebrow "F4 · Step 1", a Close button, then the content below. The project tree is a dark code block with muted notes, like the F2 tree; its lines never wrap, and it scrolls sideways on a narrow screen.

`plan` writes its files beside `prd.md` in your `<feature-dir>`. Run on the whole PRD, it decides how many stories the work needs and writes one FIS per story. One run cut this PRD into two:

```text
todo-app/
├── docs/
│   ├── adrs/                               from decide in F3
│   ├── DECISIONS.md                        from decide in F3
│   ├── UBIQUITOUS_LANGUAGE.md              from domain in F3
│   └── specs/
│       └── let-people-share-their-lists/   ← your <feature-dir>
│           ├── prd.md                      the PRD, from F2
│           ├── plan.json                   ← new: the stories and their dependsOn
│           ├── s01-share-a-list-….md       ← new: the FIS for story S01
│           └── s02-recipient-leaves-….md   ← new: the FIS for story S02
├── src/
└── tests/
```

Your stories and their names may differ: `plan` picks the cut. This step is for reading only, so open the files, don't run them:

- **`plan.json`**: under `stories`, each story's `scope`, and `dependsOn`. Here S02 depends on S01, so the two cannot run at the same time.
- **Each FIS**: its Intent, its scenarios, and What We're NOT Doing. See where the cut between the stories falls against your ADR and glossary.
- **`plan`'s output**: any `OVERSIZE:` line, and the `Decided:` and `Assumed:` lists it closes with.

Then park the files: move `plan.json` and the `s*.md` files to `.agent_temp/whole-prd-plan/`. `prd.md` stays, because step 3 plans from it again.

## Worked example: where the parked plan goes

Component: a dialog with the id `parked`, opened by the Example link on the F4 card, built like the other worked examples. Eyebrow "F4 · Step 1", a Close button, then the content below. The commands are a dark code block with a Copy button. The project tree is a dark code block with muted notes, like the F2 tree; its lines never wrap, and it scrolls sideways on a narrow screen.

Park the whole-PRD plan before step 3, or the one-story plan lands next to it. Run these from `todo-app/`, folder names adjusted to your `<feature-dir>`:

```bash
mkdir -p .agent_temp/whole-prd-plan
mv docs/specs/let-people-share-their-lists/plan.json docs/specs/let-people-share-their-lists/s*.md .agent_temp/whole-prd-plan/
```

After the move, the project looks like this:

```text
todo-app/
├── .agent_temp/                            ← git ignores it (init added it in F1)
│   └── whole-prd-plan/                     ← new: the parked plan, read only
│       ├── plan.json
│       ├── s01-share-a-list-….md
│       └── s02-recipient-leaves-….md
├── docs/
│   └── specs/
│       └── let-people-share-their-lists/   ← your <feature-dir>
│           └── prd.md                      ← stays: step 3 plans from it again
├── src/
└── tests/
```

Use the `.agent_temp/` inside `todo-app/`. Git ignores that one, so the parked plan never ends up in a commit. A `.agent_temp/` in the repository root is not ignored.

Check it: `ls docs/specs/let-people-share-their-lists/` shows `prd.md` only.

## Worked example: a hand-written FIS skeleton

Component: a dialog with the id `fis`, opened by the Example link on the F4 card, built like the other worked examples. Eyebrow "F4 · Step 2", a Close button, then the content below. The skeleton is a dark code block with a Copy button, so it can be pasted straight into the file.

One way to write it, in `.agent_temp/f4-my-fis.md`, for the vertical slice **share a list, view-only**. Yours may differ; the format is easy, and the decisions are in the scenarios.

```markdown
# Share a list view-only – my FIS skeleton

## Intent
A household member follows another member's list as it is right now, without copying it, while only the owner can change it.

## Expected Outcomes
- [OC1] The owner shares a list with a registered user by email, and can revoke it.
- [OC2] The recipient reads the list and all its todos under "Shared with me".
- [OC3] The recipient can change nothing, in the UI or by a direct request.

## Acceptance Scenarios
S01 [OC1, OC2] Share with a registered user
  Given Alice owns "Groceries" and bob@example.com has an account
  When Alice shares "Groceries" with bob@example.com
  Then Bob sees "Groceries" under "Shared with me", marked with
       Alice's email, and can open it and read every todo

S02 [OC1] Awkward edge: an email with no account
  Given no account exists for carol@example.com
  When Alice shares "Groceries" with carol@example.com
  Then she sees "No user with that email" and no share is stored

S03 [OC3] The recipient cannot change it, even directly
  Given "Groceries" is shared with Bob
  When Bob sends PATCH /api/todos/{id}/toggle for one of its todos,
       outside the UI
  Then he gets 403 and the todo is unchanged

## What We're NOT Doing
- Leave (the recipient drops the list): a later story
- Edit rights, invitations for emails without an account, notifications
- Reordering shared lists in the sidebar

## Tasks
T1 Add ListShare as ADR-001 decides
   Verify: uv run pytest tests/test_sharing.py -k model
           (a duplicate share fails; deleting the list removes its shares)
T2 Add get_owned_list and get_readable_list (ADR-002), and switch
   every list and todo route to one of them
   Verify: grep -n "_verify_list_access" src/app/routes/todos.py finds nothing,
           and uv run pytest is green
T3 Share and revoke routes, and the Share section in list settings
   Verify: uv run pytest tests/test_sharing.py -k share (S01, S02)
T4 "Shared with me" in the sidebar, and a list view with no change controls
   for the recipient
   Verify: uv run pytest tests/test_sharing.py -k recipient (S03);
           inspect: signed in as Bob, no add field, pencil or trash icon
```

### What to notice

- **Each scenario names its outcome.** The [OC] tags show what proves what. OC1 promises revoke, but no scenario proves it: a gap like that is what step 4 should catch.
- **S03 sends the request directly.** A hidden button is not a refusal. The server has to say no, and the scenario says how you see it: 403, and the todo unchanged.
- **Every task has a Verify you can run or inspect.** "It works" is not a Verify. A test name, a command or a thing to look at is.
- **The tasks lean on the ADRs.** T1 and T2 follow ADR-001 and ADR-002 instead of redesigning the model or the access check.
- **Not doing is a decision too.** Leave is in the PRD (FR5), but this slice parks it on purpose.

Keep the file. In step 4 you compare it with the FIS `plan` writes: expect it to add the scenarios you skipped, such as revoke, sharing twice and an empty email, and a proof for every change route, not just one.

## Worked example: one task and its Verify line

Component: a dialog with the id `task`, opened by the Example link on the F5 card, built like the other worked examples. Eyebrow "F5 · Step 2", a Close button, then the content below. The task is a dark code block with muted notes, like the F2 tree; its lines never wrap, and it scrolls sideways on a narrow screen. The three Verify forms are a bulleted list.

Open the FIS, `<feature-dir>/s01-<name>.md`, and find `### Implementation Tasks` under Implementation Plan. The agent takes the tasks in order and moves on only when a task's Verify passes. Here is TI04 from S01:

```text
- **TI04** Every change route refuses a       ← what must be true
  recipient's direct request and leaves
  the list unchanged
  - Depends on TI02.                          ← the order
  - **Verify**: `tests/test_sharing.py#       ← the check
    test_recipient_change_requests_refused`
    – one parametrized case per S11
    request, each asserting its status and
    that the list … match a snapshot taken
    before the request
  - **SATISFIES**: S11                        ← the scenario
```

Read each task in four parts:

- **The task line** says what must be true when the task is done, not how to code it.
- **Depends on** sets the order. TI04 needs the access helpers TI02 adds.
- **Verify** is what the agent runs before it moves on. It opens with a target, then says after the dash what must be true. Here one test sends all nine of S11's requests and compares the list with a snapshot.
- **SATISFIES** traces the task back to its scenarios. Open S11 under Acceptance Scenarios: its Then is what the test asserts.

A Verify target comes in one of three forms. All three appear in S01:

- **Test**: `tests/test_sharing.py#test_duplicate_share_row_is_refused` (TI01) runs that one test, which passes or fails.
- **Command**: `cmd: uv run pytest -x -q` (TI02) runs in your shell, and exit 0 is a pass.
- **Inspection**: `inspect: src/app/static/js/app.js#openEditListDialog` (TI09) runs nothing: someone has to read it. The Final Validation Checklist at the end of the FIS covers it with a manual run.

**Ask of every task: could you run its Verify yourself and see it pass or fail?** A Verify written as plain prose, with no target, is a gap to fix in the FIS before you run it.

## Worked example: what to point out

Component: a dialog with the id `observations`, opened by the Example link on the F5 card, built like the other worked examples. Eyebrow "F5 · Step 4", a Close button, then the content below. The table scrolls sideways on a narrow screen.

One run of S01 left these bullets under `## Implementation Observations` at the end of `docs/specs/let-people-share-their-lists/s01-shared-lists.md`. Your run writes its own, but they fall into the same kinds:

| In the FIS | What to point out | Then |
|------------|-------------------|------|
| **Review repair (F1, code-defect, fixed)** | All 89 tests were green, yet a fresh reviewer found a real bug: switching quickly between two lists' settings could share the wrong list. The fix is proved only by a browser run, because the project has no JS test runner. | Accept, knowing that this proof is manual. |
| **Blank email · TI10 timing** | Quiet reinterpretations. "Email is required" is a message the PRD never names, and the timing test warms up once although the FIS says it times one GET. Each is a small drift written as a plain bullet. | Accept, or take to F6 if the spec should say it. |
| **Tidies** | Changes no task carries: an unused query removed, a lookup moved behind the access helper, an empty-list hint hidden from recipients. | Find each in the story's commit and check it belongs in the change. |
| **Not run** | The review ran the code lens only. The security lens never ran on a change that is mostly authorization. | Take to F6: the plan-level review runs it. |
| **NOTICED BUT NOT TOUCHING** | Two real problems outside the story: one click can send several requests, and deleting a user would orphan their shares. | Later: Tech Debt, not this branch. |
| **TI09 inspection · Layout** | Checked by hand only. The dialog staying open and where "Shared with me" sits have no automated test. | Accept, and look at them yourself in F6. |

**No `#### DRIFT` section is a claim, not a fact.** The run writes DRIFT only for a divergence it knows about. Here two plain bullets hold small reinterpretations, so read every bullet as "the spec said X, the run did Y".

## Worked example: falsify one check

Component: a dialog with the id `falsify`, opened by the Example link on the F6 card, built like the other worked examples. Eyebrow "F6 · Step 2", a Close button, then the content below. Code and test output are dark code blocks whose lines never wrap; they scroll sideways on a narrow screen.

In the reference run, each change route looks up the list through an owner check. Three moves, all from `todo-app/`:

**1. Change one line.** Open `src/app/routes/todos.py` and find this line in `update_todo`:

```text
list_obj = get_owned_list(db, todo.list_id, user_id)
```

Swap `get_owned_list` for `get_readable_list`, and save. It is already imported at the top of the file, so nothing else changes. `get_owned_list` returns the list only to its owner; `get_readable_list` also returns it to anyone it is shared with. After the swap a viewer passes the check, and the update goes through.

**2. Run the tests:** `uv run pytest`. One test must fail:

```text
FAILED tests/test_sharing.py::test_recipient_change_requests_refused[update todo]
1 failed, 88 passed
```

Save the file first: unsaved, the tests run the old code and stay green, which looks like a lying suite but isn't.

**3. Put the check back:** `git restore src/app/routes/todos.py`. Then `git status --short src/` prints nothing.

Your run may name or place the check differently. Look for where a change route – update, toggle or delete – fetches the list and refuses anyone who doesn't own it. Or ask Claude: "Which line in the update route refuses a viewer? Show me, don't change it."

**Why not just comment the check out?** The route would crash, and a crash fails tests whether or not they check the right thing. A check that lets a viewer through keeps the code running, so only a test that asserts the refusal goes red.

## Worked example: what the review left behind

Component: a dialog with the id `review-output`, opened by the Example link on the F6 card, built like the other worked examples. Eyebrow "F6 · Step 3", a Close button, then the content below. The run's closing lines are a dark code block whose lines never wrap; it and the table scroll sideways on a narrow screen.

In the reference run, `review --fix` found five things: one HIGH (an owner could inject CSS into a recipient's page through the list colour) and four LOW. It closed like this:

```text
Report: docs/specs/let-people-share-their-lists/let-people-share-their-lists-andthen-mixed-review-claude-2026-11-05.md
Report annotation: written (## Remediation Status)
Tech-debt entries written: 0 entries
Next (fresh session): /andthen:review docs/specs/let-people-share-their-lists/plan.json --fix
```

Each line points at something the run left behind:

| Where | What the reference run left | Then |
|-------|-----------------------------|------|
| **The report**, beside `plan.json` | The verdict first, `Overall readiness: Needs Fixes`, one label per lens (code, gap, security, outcome), a Coverage Matrix, and each finding routed Fix or Note. Gitignored, so it stays on your machine. | Compare the findings with what you found in steps 1–2. |
| **Your branch** | The two Fix findings applied: a colour check in `src/app/routes/todo_lists.py`, and tests in `tests/test_sharing.py` that failed before the check. `uv run pytest` passed with 102 tests. The reference run, on AndThen 1.0, left them uncommitted; from 1.1, `review --fix` commits the verified change by path. | Read the fix commit with `git show`. |
| **`## Remediation Status`**, the report's last section | One line per finding: the two Fix findings RESOLVED with evidence, the three Notes SURFACED and untouched. The header gains a `**Remediated**:` line. | Decide each SURFACED Note in step 4. |
| **`docs/TECH-DEBT-BACKLOG.md`** | Nothing yet: the review defers nothing on its own. Deferring the three Notes afterwards wrote three Low entries, each with its blocker and the report as source, and added a `Tech Debt` row to the Project Document Index. | Only what you approve is written. |
| **The `Next` line** | A follow-up review, because the run fixed a HIGH finding, and the session that applied a fix is not the one to judge it. | Run it in a fresh session before `ship`. |

**The verdict is the one before the fixes.** The verdict line records what the reviewer found: Needs Fixes in the reference run, FAIL from AndThen 1.1. The `**Remediated**:` line says fixes came after it, and only the follow-up review gives a new verdict.

## What's next

Component: a closing line, then a row of buttons. The first is filled, the second is outlined.

You have run the whole Core Loop once. The case work runs the same loop on a real case, with a gate at each artifact.

- Back to the Core Loop → (loop)
- Read the labs overview on GitHub → (https://github.com/IT-HUSET/agentic-engineering-2026/blob/main/labs/README.md)
