---
title: AndThen Core Loop
tab: Core Loop
token: loop
order: 6
depends_on: [shared/skills.md, shared/icons.md]
---

# Core Loop

Eyebrow: The workflow you'll practice

## From a fuzzy idea to a verified pull request

AndThen chains a few skills into the Core Loop. Each step writes something the next step reads, and ends by printing the command to paste next.

Formula: idea → [clarify] → plan → exec-plan → review --fix → ship

Component: the formula as a mono line, with a red dot before "idea" and [clarify] muted.

## How much structure does the work need?

Interactive component: three pill buttons, one per path. The chosen path sets the note under the buttons, the rail of steps and the commands in the stage card. Default path: feature, step plan.

| Path | Label | Start | Steps | Note |
| - | - | - | - | - |
| feature | One feature | idea | clarify, decide, plan, exec-plan, review, ship | One real feature runs the full Core Loop on a single FIS. Start with clarify if you can’t list three acceptance criteria. Otherwise start with plan. |
| several | Several features | idea | clarify, decide, plan, exec-plan, review, ship | Several features share the same Core Loop, run on a plan directory. plan splits the work into stories, and exec-plan builds them one story at a time, or the whole directory in one sweep. |
| fix | A one-sentence fix | fix | triage, implement-fix, ship | A fix you can state in one sentence skips the spec. Unknown cause or broken build? Run triage first. |

Component: the rail. The start label with a red dot, then each step as a pill with its number, name and "optional" when it applies (dashed border). Under each pill, a tag with the step’s Result icon and Tag from shared/skills.md. Between steps a "/clear" marker; arrow keys move along the rail.

## Stages

Component: stage card for the selected step, tinted by the stage Tint, with its number, Role, Title, Summary and When, a muted note box under When when the step has a Note for the chosen path, then a Result box (icon, title, text from shared/skills.md), Reads, the commands with copy buttons, an "In AndThen Studio" strip when the step has a Studio field (lavender, with the text and a link to the Studio tab), a "Then /clear and paste the next command" line, and Previous / Next buttons. On the last step the line reads "That’s the Core Loop. The pull request is open." Each command box starts hidden behind a "Show command" button, as on the Setup tab.

Hint under the card: Pick a step on the rail, or use the arrow keys. Dashed steps are optional.

Commands may differ per path; a line `Command (several): …` applies only to that path, and so does `Note (several): …`, whose bold opening is the box’s label. A command with a note shows the note above it.

### clarify

- Skill: clarify
- Tint: rust
- Optional: yes
- Role: Requirements
- Title: Clarify what you want
- Summary: Interviews you about a vague idea: the gaps, the edge cases and the scope. Then it writes the PRD.
- When: **Optional.** Skip it when the requirements already exist. Entry test: if you can’t list three acceptance criteria, start here.
- Reads: Your idea, in your own words
- Command: `/andthen:clarify`
- Studio: Reader: open the PRD under Requirements, read it section by section, and pin a note on what you doubt.

### decide

- Skill: decide
- Tint: red
- Optional: yes
- Role: Decisions
- Title: Settle the costly choices
- Summary: Settles a technical choice that binds beyond one story or is costly to reverse, and records it as an ADR.
- When: **Optional.** Runs between clarify and plan. Its companion `domain --mode glossary` fixes one name per concept.
- Reads: The PRD and the open technical question
- Command: `/andthen:decide`; `/andthen:domain --mode glossary` (One name per concept)
- Studio: Reader: the ADR under Architecture decisions, and Decisions and Ubiquitous Language in the sidebar. Explain a section you can't place.

### plan

- Skill: plan
- Tint: cream
- Role: Specification
- Title: Write the spec
- Summary: Writes the Feature Implementation Specification (FIS): what to build, the proof for each acceptance scenario, and when it’s done.
- When: **No code changes.** Plan decides whether the work is one story or several.
- Reads: The PRD, or requirements you already have
- Command (feature): `/andthen:plan`
- Command (several): `/andthen:plan <dir>`
- Studio: Plan board: the stories as columns with their dependencies. A story opens its FIS.

### exec-plan

- Skill: exec-plan
- Tint: green
- Role: Implementation
- Title: Build against the spec
- Summary: Builds a FIS, or runs a plan directory with one fresh subagent per story. A story is done only on a quoted line from a check that actually ran, and a fresh reviewer checks each one. Each finished story then gets a simplify pass, and what it found is carried into the FIS files of stories not yet started.
- When: **Hands off while it runs.** Don’t hand-edit code mid-run. Let it finish, or stop and amend the FIS.
- Reads: A FIS, or a plan directory
- Command (feature): `/andthen:exec-plan <FIS>`
- Command (several): `/andthen:exec-plan <first ready FIS>` (The line plan prints: one story at a time, each run names the next); `/andthen:exec-plan <dir>` (Or every story in one sweep); `/andthen:exec-plan <dir> --worktree` (Run independent stories in parallel)
- Studio: Plan board, left open: the story moves to done as the run commits, and opens the diff of its changes.

### review --fix

- Skill: review
- Tint: teal
- Role: Review
- Title: Review the whole
- Summary: Reviews the finished work as a whole: spec fit, code, security and outcome. Then it gives a PASS or FAIL verdict, applies the findings marked Fix and commits them.
- When: **Whole-change view.** exec-plan already checked each story; this looks at how they fit together.
- Reads: The finished change and its spec
- Command: `/andthen:review --fix`
- Studio: Review report: the verdict, the finding index and `## Remediation Status`, one report per review round.

### ship

- Skill: ship
- Tint: lav
- Role: Delivery
- Title: Ship it
- Summary: Lands what was learned, opens the pull request after your one yes, and once every story is done offers to drop the plan files.
- When: **You stay in control.** Nothing is opened until you say yes.
- Reads: The reviewed work and its plan files
- Command: `/andthen:ship`
- Note (several): **Only part of the plan built?** `ship` checks first. While stories are left, it names them and asks once whether to ship anyway, and recommends keeping the plan: `plan.json` and the FIS files stay, go into the pull request with the work, and the remaining stories keep reading them. The Learnings step waits too. The pull request names what is still open. The last `ship`, once every story is done and reviewed, lands the Learnings and asks to delete the plan, recommending yes. `prd.md` stays, with a Shipped line.
- Studio: Walkthroughs: a guided tour of the pull request before you merge it. After the last `ship` the plan board is empty, because it deletes `plan.json`.

### triage

- Skill: triage
- Tint: red
- Optional: yes
- Role: Diagnosis
- Title: Find the cause first
- Summary: Investigates the problem down to a root cause, fixes it under a failing test and commits the fix. --plan-only stops at the fix plan.
- When: **Optional.** Only when the cause is unknown or the build is broken. Describe symptoms, not fixes.
- Reads: Symptoms: errors, failing tests, logs
- Command: `/andthen:triage`

### implement-fix

- Skill: implement-fix
- Tint: rust
- Role: Small fix
- Title: Make the fix
- Summary: For a fix you can state in one sentence. It skips the spec and goes straight to a verified change, committed.
- When: **Right-size it.** If you can’t say it in one sentence, it’s a feature. Use plan instead.
- Reads: Your one-sentence request
- Command: `/andthen:implement-fix "<request>"`
- Studio: Walkthroughs: a git range such as `main...HEAD` gives a tour of the fix before ship.

## Product and PRD — PRODUCT.md and prd.md: two levels of requirements

`clarify` writes both, at different levels. `docs/PRODUCT.md` describes the whole product, and there is one per project. `prd.md` describes one feature, and every feature gets its own, in its folder under `docs/specs/`.

Component: two tinted cards side by side, joined by a labelled arrow (stacked, with a downward arrow, below 1080 px), in the same style as the cards in Plan, stories and FIS. Each card has an eyebrow, the file name in mono, a short text, its rows and a note. Under the cards, how clarify picks the level as a subheading and a lead, then the rule of thumb in a muted box.

### The documents

#### docs/PRODUCT.md

- Eyebrow: Product · one per project
- Tint: teal
- Arrow: sizes
- Text: What the product is, and how big what gets built may be. It sits above every PRD.
- Row: Holds · vision, target users, value propositions, non-goals and success metrics
- Row: Proportionality · stage, scale and standing technical non-goals
- Row: Written by · `clarify` at product scope, or the first of `clarify`, `decide`, `plan` and `architecture` that needs the Proportionality facts
- Row: Read by · every skill that proposes something
- Note: Long-lived. It changes when the stage or the scale changes.

#### prd.md

- Eyebrow: Feature · one per feature
- Tint: cream
- Text: What one feature must do, and how you know it is done. It lives in the feature’s folder, `docs/specs/<feature>/`.
- Row: Holds · the problem, the requirements (FR1, FR2 …) with priority, what is in and out of scope, the MVP boundary, constraints and a decisions log
- Row: Written by · `clarify` at feature scope, the default
- Row: Read by · `plan`, which turns it into the FIS, and the outcome lens of `review`
- Row: Shipped · `ship` adds a Shipped line when it deletes the plan; an amendment through `clarify` removes it
- Note: The PRD is anchored in the product. In the lab’s shared-lists PRD, email and notifications are out because `docs/PRODUCT.md` says prototype, one SQLite file and no external services. `clarify` drops or flags a capability those facts don’t carry, citing the anchor.

### How clarify picks the level

Feature scope is the default and writes `prd.md`. Product scope applies when you name it (“clarify the product vision”), when the input is a file named `PRODUCT*.md`, or when the request talks about vision, positioning or product strategy. Then `clarify` writes the Product document instead of a PRD.

### Rule of thumb

Tip: What the product is, and how big it may get, belongs in `PRODUCT.md`. What one feature must do, and how you know it is done, belongs in `prd.md`.

## Plan, stories and FIS — How the plan, its stories and their specs fit together

`plan` writes two kinds of file: one `plan.json` for the plan directory, and one FIS per story. A story is a slice of the work, and a FIS belongs to exactly one story. Tasks live only inside a FIS. Even a single feature gets a `plan.json`, with one story, S01.

Component: three tinted cards joined by labelled arrows (stacked, with downward arrows, below 1080 px): the PRD, then plan.json with its stories as rows (the first highlighted), then that story’s FIS with its four parts. A dashed border marks the optional PRD. Each card has an eyebrow, the file name in mono, a short text, its rows and a note. Under the diagram, the slicing rules as four white cards with rust numerals (two across below 1080 px, one on a phone), then the naming tip in a muted box.

### The files

#### prd.md

- Eyebrow: Requirements · optional
- Tint: cream
- Arrow: plan
- Text: What the work must do, from `clarify`. `plan` can also start from requirements you already have, a tracker item or a one-line request.

#### plan.json

- Eyebrow: One per plan directory
- Tint: rust
- Arrow: fis
- Text: The plan’s state. For each story: its dependencies (`dependsOn`), its status, which of its FIS tasks are done (`completedTaskIds`), and a pointer to its FIS. `plan` writes it; after that, the session building a story updates that story’s row. It says nothing about how to build anything. It lives on the branch. `ship` deletes it on your yes; kept, it gets a `shipped` marker as a record.
- Row: S01 · Lists have owners · `s01-lists-have-owners.md` · done
- Row: S02 · Share a list · depends on S01 · in-progress
- Row: S03 · Sort by due date · no dependencies · done
- Row: S04 · Revoke a share · depends on S02 · pending
- Note: Mid-run: S01 and S03 are done, S02 is being built, and S04 waits for S02. A story becomes done only together with `verified`: when, and which check that actually ran proved it. You set skipped by hand.
- Note: A story is a delivery piece, not an agile user story (“As a user I want…”). The FIS’s acceptance scenarios come closest to that.

#### s01-lists-have-owners.md

- Eyebrow: FIS · one per story
- Tint: green
- Text: The spec for one story: what to build, how each part is proved, and when it is done.
- Row: OC01 … · Expected Outcomes · two to four, one sentence each
- Row: S01 … · Acceptance Scenarios · Given, When, Then, each with its Proof
- Row: SC01 … · Structural Criteria · what the story’s diff must not break
- Row: TI01 … · Implementation Tasks · a state that must be true, with Verify (the check that proves it) and SATISFIES (the scenarios it moves forward)
- Note: `plan.json` records only which tasks are done, in `completedTaskIds`, so a stopped run resumes where it left off.

### When does it become vertical slices

`plan` decides in its step 3, One story or several. A story is by definition a vertical slice: something you can demo through every layer.

1. **One story when it fits.** The work stays one story when it is one vertical slice that fits a single exec run in a fresh context with headroom, about 12 tasks.
2. **Otherwise the fewest slices.** `plan` cuts the fewest stories that cover the source, none overlapping. It never cuts by layer, such as endpoint, handler and UI on their own.
3. **Too big splits thinner.** A story that comes back `OVERSIZE:` is cut into thinner vertical slices.
4. **Seams and overlaps.** Where module boundaries are strong, the work splits along them and `sharedDecisions` pins the interface. Stories that would touch mostly the same files are merged, except a walking skeleton: when the main flow crosses several stories, the first is its thinnest end-to-end path, and the stories that thicken it depend on it.

### Watch the names

Tip: Two numberings share the letter S. Story IDs in `plan.json` are `S01`, `S02` …, and so are the acceptance scenarios inside a FIS. In a FIS, `**Story-ID**: S03` names the story; `S01 [OC01]` further down is a scenario.

## Parallel stories — How AndThen decides what can run at once

Only a plan directory can run stories in parallel, and only when you add `--worktree`. A single FIS is always built as one piece. Two skills share the decision: `plan` draws the dependencies when it cuts the stories, and `exec-plan` reads them again before every batch.

Component: the example plan as a small table, then two lanes, one per command. Each lane has its command in mono, the stories as pills joined by arrows, and a muted note. Stories that run at the same time sit stacked in a dashed box labelled "at once", and the --worktree lane has a "merge" marker after each batch. Under the lanes, three white cards with rust numerals 01–03, like the rules, and the prerequisites as a muted line. Stacked on a phone.

### Example plan

| Story | Name | Depends on |
| - | - | - |
| s01 | Lists have owners | – |
| s02 | Share a list | s01 |
| s03 | Sort by due date | – |
| s04 | Revoke a share | s02 |

### Lanes

Box label: at once
Merge label: merge

- `/andthen:exec-plan <dir>` · s01 → s03 → s02 → s04 · One story at a time, in plan order as each becomes ready, because a shared working tree shares one test run.
- `/andthen:exec-plan <dir> --worktree` · [s01, s03] → merge → s02 → merge → s04 → merge · s01 and s03 depend on nothing, so they start together, each in its own worktree. s02 waits for s01 to be merged, and s04 for s02.

### Who decides

1. **plan draws the edges.** `dependsOn` holds causal edges only: a story depends on another only when it uses something that story produces, a contract or a decision. Stories that would touch mostly the same files are merged into one, and an interface two stories share is pinned in `sharedDecisions`. plan’s last line names `exec-plan` on the first ready story’s FIS, and each story run names the next. Running the whole directory, with or without `--worktree`, is your call.
2. **exec-plan takes one wave at a time.** Before each batch it re-reads `plan.json` and takes the stories whose dependencies are all done. With `--worktree` it starts up to about five of them at once, each a fresh subagent on its own `story/<id>` branch in its own worktree.
3. **The merge has the last word.** Each finished story is merged with `git merge --no-ff` before the next batch starts, so the stories that depend on it start from a base that has its work. A merge conflict fails the story, unless both sides only added lines to an append-only document such as Learnings. A failed story keeps its worktree, and the stories that depend on it are skipped. After each merged batch, one simplify pass covers its stories, and what they found goes into the FIS files of stories not yet started.

Prerequisites: `--worktree` stops before the first story when a tracked file has uncommitted changes, or when `plan.json` is not committed, because a worktree holds only what was committed.

## Rules of the Core Loop — Small steps, clean hand-offs

Component: three white cards with rust numerals 01–03.

1. **Every skill works standalone.** Start at whichever step fits. Requirements already written? Go straight to `plan`.
2. **Each step prints the next command.** When a step finishes, the last thing it shows is the command to paste for the next one.
3. **One fresh session per step.** Run `/clear` between steps. The files on disk carry the work forward, so each skill starts from the spec instead of a long chat.

## Next

Component: a row of buttons that switch tabs. The first is filled, the others are outlined.

- Do the Foundation Lab → (lab)
- Other paths, and what each step leaves → (paths)
- Use AndThen Studio → (studio)
