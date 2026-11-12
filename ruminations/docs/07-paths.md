---
title: AndThen Paths
tab: Paths
token: paths
order: 7
depends_on: []
source: AndThen 1.1.0 – plugin/README.md and COOKBOOK.md (https://github.com/IT-HUSET/andthen), labs/x2-ui-ux.md
---

# AndThen Paths

Eyebrow: Paths and artifacts

## What can you do, and when?

Component: "when" in the title is set in the accent colour.

The Core Loop is the main road. AndThen has more paths beside it: a quick fix, a design detour, a bug hunt, a new domain. This tab shows which path fits your situation, what each step leaves behind, and what you can do once the pull request is merged.

Component: under the lead, a row of link buttons that scroll to the five sections below, the first filled, the others outlined.

- Pick a path → (#paths-pick)
- What is left → (#paths-left)
- After ship → (#paths-next)
- Example: ui-ux-design → (#paths-ui)
- Example: decide and spike → (#paths-decide)

## Which path — Pick your situation

Every skill works standalone, so you start where your situation is. Not sure? `/andthen:now-what` inspects the project and routes you.

Interactive component: a list of situation buttons on the left and a card on the right (stacked on a phone). The card shows the situation as title, the chain of skills as pills with arrows between them (an optional skill in brackets is dashed), the text, a "You get" line, and the commands with copy buttons. Each command box starts hidden behind a "Show command" button, as on the other tabs. A Link line becomes a button under the commands: a tab token switches tab, a #anchor scrolls to that section. Starts on the first situation. Up and down arrow keys move through the list.

### fix

- Situation: A fix you can say in one sentence
- Chain: implement-fix, ship
- Text: No spec. `implement-fix` makes the smallest safe change, re-validates it and commits it. On `main` it first asks whether to start a feature branch. `ship` writes the pull request and pushes it after your yes.
- You get: A verified change and a pull request. Nothing else is written.
- Command: `/andthen:implement-fix "<request>"`
- Command: `/andthen:ship`

### feature

- Situation: One real feature, with edges
- Chain: [clarify], plan, exec-plan, review --fix, ship
- Text: The Core Loop on one FIS. Start with `clarify` if you can't list three acceptance criteria; otherwise start with `plan`.
- You get: The code with its tests, a pull request that states intent and proof, and the PRD when `clarify` ran.
- Command: `/andthen:plan docs/specs/<feature>/`
- Command: `/andthen:exec-plan docs/specs/<feature>/s01-<name>.md`
- Link: Walk the Core Loop → (loop)

### idea

- Situation: An idea without three acceptance criteria
- Chain: clarify, [decide], plan
- Text: `clarify` interviews you in rounds about gaps, edge cases and scope, then writes the PRD. With `--brief` it stops at `intent.md`, a short document to edit or share before the PRD.
- You get: `prd.md` in its feature folder, or `intent.md` with `--brief`.
- Command: `/andthen:clarify "<your idea in one line>"`
- Command: `/andthen:clarify --brief "<your idea in one line>"`

### choice

- Situation: A technical choice that is costly to reverse
- Chain: decide, plan
- Text: `decide` lists the decision points and interviews you on those that bind beyond one story. Ask for a comparison and it runs a weighted trade-off. A question only measurement can settle goes to `spike` instead.
- You get: One ADR per decision in `docs/adrs/`, each with a row in `docs/DECISIONS.md`, and the PRD rows it settles now cite it. No code changes.
- Command: `/andthen:decide docs/specs/<feature>/`
- Command: `/andthen:decide "compare three options for <the choice>"`
- Link: See the worked example → (#paths-decide)

### screens

- Situation: Screens that don't exist yet
- Chain: ui-ux-design, plan, exec-plan, visual-validation
- Text: Design comes before the spec, so the FIS can point at the wireframes instead of inventing the screens. The worked example below walks it through for shared lists.
- You get: Wireframes in `docs/wireframes/<feature>/`. For a broad surface, a design system in `docs/design-system/`, and then clickable mockups in `docs/mockups/<feature>/`.
- Command: `/andthen:ui-ux-design "wireframe <the screens>, all states" docs/specs/<feature>/prd.md`
- Link: See the worked example → (#paths-ui)

### bug

- Situation: A bug or a broken build
- Chain: triage
- Text: Describe symptoms, not fixes. `triage` finds the root cause, fixes it and checks the fix against the original symptom. To pin a bug with a failing test first, use `testing --mode prove-it`.
- You get: A root-cause fix. Traps go to `docs/LEARNINGS.md`, deferred fixes to `docs/TECH-DEBT-BACKLOG.md`.
- Command: `/andthen:triage "<what you see>"`
- Command: `/andthen:testing --mode prove-it "<the bug>"`

### existing

- Situation: A codebase AndThen has never seen
- Chain: init, describe
- Text: `init` writes the Project Document Index, so every skill knows where documents live. `describe` maps the code without changing it.
- You get: The Architecture document, `requirements-discovered.md` and `decisions-discovered.md` for the team to review, and a Conventions section in `CLAUDE.md`.
- Command: `/andthen:init`
- Command: `/andthen:describe`

### domain

- Situation: A new or tangled domain
- Chain: domain
- Text: You are the domain expert. Event storming puts the domain's events, actors and open questions on one board. The Domain Map classifies its parts and draws their boundaries; the glossary fixes one name per concept.
- You get: An event storm board in `docs/models/event-storms/`, `docs/DOMAIN-MAP.md` and `docs/UBIQUITOUS_LANGUAGE.md`.
- Command: `/andthen:domain --mode event-storming "<scope>"`
- Command: `/andthen:domain --mode subdomains,contexts,glossary "<scope>"`

### spike

- Situation: A question only running code can answer
- Chain: spike, decide
- Text: A throwaway build in its own worktree, then a verdict: the answer, the evidence and what it did not cover. Spike code is never merged. The verdict feeds `clarify`, `decide` or `plan`.
- You get: A Spike Verdict in the chat, and the code on a `spike/<slug>` branch as evidence.
- Command: `/andthen:spike "<the one question>"`
- Link: See the worked example → (#paths-decide)

### pause

- Situation: Work that has to stop half-way
- Chain: handoff
- Text: `handoff` compacts the session into a document. After `/clear`, a fresh session resumes from it without you retyping anything.
- You get: `.agent_temp/handoff/handoff-<UTC-ts>.md`, local and not private.
- Command: `/andthen:handoff "next: <the focus>"`
- Prompt: Resume from .agent_temp/handoff/handoff-<UTC-ts>.md

### unsure

- Situation: I'm not sure where to start
- Chain: now-what
- Text: `now-what` reads the state of the project, such as a PRD, a plan or a review report on disk, and hands over to the skill that fits, after asking "Run it?".
- You get: One recommended next step, run or printed.
- Command: `/andthen:now-what "<what you want, in one sentence>"`

## What is left — What each step leaves behind

Each step writes something the next step reads. Some files stay for good, some live only on the branch, and some never leave your machine.

Interactive component: a timeline with one column per stage and one row per artifact. Each artifact is a bar from the stage that writes it to where it ends, styled by its Kind: a solid bar that runs on into "After merge" for kept (on `main`, or on GitHub for the pull request), a dashed bar that stops at Ship with a cross for branch, a dotted grey bar for local. A legend above names the three kinds. Clicking a row, or Enter on it, opens its card under the timeline: path, written by, read by, and the note. The timeline scrolls sideways in its own box on a narrow screen.

| Stage | Label |
| - | - |
| req | Requirements |
| design | Design |
| plan | Plan |
| build | Build |
| review | Review |
| ship | Ship |
| after | After merge |

| Artifact | Path | Written by | Read by | From | To | Kind | Note |
| - | - | - | - | - | - | - | - |
| Product facts | `docs/PRODUCT.md` | `clarify`, or the first of `decide`, `plan` or `architecture` to need the stage and scale | every skill that proposes something | req | after | kept | The anchor that sizes what gets built: stage, scale and technical non-goals. |
| PRD | `docs/specs/<feature>/prd.md` | `clarify` | `plan`, `review` (gap and outcome) | req | after | kept | The product record. It survives the merge, so the why is still there next year. When `ship` deletes the plan, it gains a Shipped line. |
| ADRs and Decisions | `docs/adrs/`, `docs/DECISIONS.md` | `decide` | every skill at task start | design | after | kept | One ADR per costly choice, with its alternatives and what reversing takes. |
| Glossary | `docs/UBIQUITOUS_LANGUAGE.md` | `domain --mode glossary`, and `clarify` for settled terms | every skill that names things | design | after | kept | One name per concept, and the synonyms to avoid. |
| Wireframes and design system | `docs/wireframes/`, `docs/design-system/` | `ui-ux-design` | `plan`, `exec-plan`, `visual-validation` | design | after | kept | The FIS cites them, and the built screens are checked against them. The design system stays; `ship` asks whether to delete the feature's wireframe and mockup folders, and recommends it once the screens are built. |
| Trade-off research | `docs/research/<topic>/` | `decide`, for a contested decision | the ADR, your reviewers | design | after | kept | The evidence behind an ADR: the research, the weighted matrix and the recommendation. Committed with the ADR. |
| Spike | branch `spike/<slug>` | `spike` | `decide` and `plan`, through its verdict | design | after | local | Never merged. AndThen keeps the branch as evidence; delete it once the verdict is recorded in the ADR. |
| Plan | `docs/specs/<feature>/plan.json` | `plan`, then `exec-plan` for each story's status | `exec-plan`, `review`, `ship` | plan | ship | branch | The stories, their dependencies and status. `ship` asks whether to delete it, and recommends it: a plan governs one branch. Kept, it gets a `shipped` marker. |
| FIS | `docs/specs/<feature>/s01-<name>.md` | `plan` | `exec-plan`, `review`, `ship` | plan | ship | branch | Deleted by `ship` on your yes, after its Implementation Observations have become Learnings. The PR and git history keep it. |
| Code and tests | the source tree | `exec-plan`, one commit per story plus any `refactor` commit; `review --fix` and `implement-fix` commit their fixes | `review`, your team | build | after | kept | One squash commit on `main` after the merge. |
| Review report | beside the reviewed spec, else `.agent_temp/reviews/` | `review` | `implement-fix`, `ship` | review | after | local | Gitignored by default: a working file for one run. Its verdict goes into the PR text. |
| Tech Debt | `docs/TECH-DEBT-BACKLOG.md` | `review --fix` and `implement-fix` for findings you defer, `triage` | the skill working in that area | review | after | kept | Each entry names its blocker. Only what you approve is written. |
| Learnings | `docs/LEARNINGS.md` | `ship`, from the FIS observations; also `triage` and `handoff` | every skill at task start | ship | after | kept | The traps worth remembering, one bullet each. |
| Pull request | on GitHub | `ship`, after your yes | your reviewers | ship | after | kept | Intent, outcomes, the proof of each, the door type, where to read closely, and a closing Ship summary. With a squash merge it is where the FIS's story lives on. |
| Handoff | `.agent_temp/handoff/` | `handoff` | the next fresh session | req | after | local | Written at any step. Under `.agent_temp/`, so never committed. |

### After ship

Component: three columns under the timeline (stacked on a phone), built from the table's Kind: "Kept after the merge" (kept), "Only in the PR and git history" (branch), "Never leaves your machine" (local). Each lists its artifacts' names with their paths.

## After ship — What you can do next

The branch is merged, and `plan.json` is gone unless you kept it at ship. The documents that stayed point to what comes next.

Component: white cards in a grid, three across (one on a phone). Each card has a title, the text and its command, hidden behind a "Show command" button.

1. **Build the next feature** · The PRD's Out of Scope and Open Questions are a ready backlog. Start a new branch from `main` and pick one. · `/andthen:clarify "<the next idea>"`
2. **Pay down tech debt** · Every deferred finding sits in `docs/TECH-DEBT-BACKLOG.md` with its blocker. An entry you can state in one sentence is an `implement-fix`. · `/andthen:implement-fix "<an entry from docs/TECH-DEBT-BACKLOG.md>"`
3. **Act on what ship recommended** · `ship` writes only Learnings and the PRD's Shipped line. It recommends the rest, such as a `decide` run for a design change no ADR records yet. · `/andthen:decide "<the change ship named>"`
4. **Check the outcome** · Did the feature solve the PRD's problem for its users? The outcome lens reads the PRD against what was built. · `/andthen:review --mode outcome docs/specs/<feature>/prd.md`
5. **Triage the incoming issues** · New ideas and bugs pile up in the tracker. `tracker triage` labels and routes each one; you ratify every write. · `/andthen:tracker triage "the ten oldest"`
6. **Stop for the day** · Hand off with the next focus, so tomorrow's fresh session starts from files, not memory. · `/andthen:handoff "next: <the focus>"`

## Worked example — ui-ux-design for shared lists

The same feature as the Foundation Lab, now with its screens designed before the spec. The share dialog has real states to get right, so it earns wireframes. One dialog does not earn a design system.

Component: a horizontal flow of the steps as small pills with arrows (stacked on a phone), then a two-column block: on the left the numbered steps, each with its command hidden behind a "Show command" button; on the right the file tree in a dark box with notes in muted colour. Under it, "What you do with them" as numbered cards, and the sizing check as a muted line.

Flow: prd.md → research → wireframes → [design system] → plan → exec-plan → visual-validation

### Steps

1. **Research the flows, if they are unclear.** The answer comes in the chat, with no file: the job to be done, two to five journeys, a sketch of the navigation, constraints and open questions. Open questions send you back to `clarify`.
   Command: `/andthen:ui-ux-design "research the shared-lists flows" docs/specs/let-people-share-their-lists/prd.md`
2. **Wireframe every screen and state.** It writes a page inventory first, then one grayscale HTML page per screen and state, then checks them at four viewports.
   Command: `/andthen:ui-ux-design "wireframe the share dialog and the member list, all states" docs/specs/let-people-share-their-lists/prd.md`
3. **A design system, only for a broad surface.** A whole collaboration area across many screens earns tokens and component styles. One dialog does not. Once `DESIGN.md` exists, asking it to mock up the screens builds clickable mockups from its tokens in `docs/mockups/<feature>/`.
   Command: `/andthen:ui-ux-design "create a design system for the collaboration screens" docs/specs/let-people-share-their-lists/prd.md`
4. **Plan from the design.** `ui-ux-design` closes on this command. The FIS cites the wireframes, so `exec-plan` builds to them.
   Command: `/andthen:plan docs/specs/let-people-share-their-lists/`
5. **Check the built screens.** Set up the capture procedure once, then compare the built screens with the wireframes.
   Command: `/andthen:visual-validation --mode setup`
   Command: `/andthen:visual-validation "share dialog and member list, mobile and desktop" docs/wireframes/shared-lists/`

### The artifacts

```
docs/
├── wireframes/shared-lists/   one folder per feature
│   ├── index.html              ← open this: every wireframe as a preview
│   ├── page-inventory.md       every screen and state, checked off
│   ├── share-dialog.html       one page per screen…
│   ├── share-dialog-error.html …and one per state
│   ├── member-list-empty.html
│   ├── screenshots/            the check's captures, per viewport
│   └── validation-report.md    what the check found
└── design-system/              only for a broad surface
    ├── DESIGN.md               tokens and the reasons behind them
    ├── tokens.css
    └── showcase.html
```

Note: The wireframe file names are examples: the page inventory decides them.

### What you do with them

1. **Open `docs/wireframes/shared-lists/index.html` in a browser.** Every screen should be there, and every state: empty, error ("no account for that email"), already shared, loading.
2. **Hold it against `page-inventory.md`.** No page skipped for looking "similar" to another. A missing state is a screen the agent will invent later.
3. **Commit them with the PRD.** The FIS cites them while the branch builds. At ship, `ship` asks whether to delete the feature's wireframe folder, and recommends it once the screens are built and validated. The design system stays.
4. **Plan from them.** The FIS names the wireframes as the asset to build against, and `exec-plan` builds to them instead of guessing the layout.
5. **Validate what was built.** `visual-validation` lists every difference from the wireframes before its verdict. P1 and P2 findings block; P3 is reported.

Sizing check: One field added to an existing form earns no wireframes. A dialog with real states earns wireframes. A whole surface across many screens earns a design system, and mockups once you want those screens approved in its look. An API change earns nothing from this skill.

## Worked example — decide, architecture and spike for todo search

A next feature for the todo app: search your own todos and those in lists shared with you. How to search is a real choice: the options sit close, one breaks a standing non-goal, and one question only running code can answer. The PRD is already in place, in `docs/specs/search-todos/prd.md`.

Component: the same layout as the ui-ux-design example: the flow as pills, the numbered steps with their commands hidden behind "Show command" buttons beside the file tree, then "What you do with them" as numbered cards and the sizing check as a muted line.

Flow: prd.md → architecture → decide → trade-off → spike → ADR → plan

### Steps

1. **Ask for advice on the shape.** `architecture` in advise mode answers in the chat and writes nothing. Here it routes search through the read check from ADR-002, so the todos in a shared list are found and nobody else's are. A fork worth recording goes on to `decide`.
   Command: `/andthen:architecture "how should todo search fit with the list access helpers, so shared lists are searched but nobody else's?"`
2. **Frame the decision.** `decide` lists the decision points and sorts them. Where access is checked is settled by ADR-002, so it is cited, not asked. How results are ranked is local to one story and left to `plan`. How to search binds beyond one story and no option stands out, so it gets a weighted trade-off.
   Command: `/andthen:decide "compare three options for searching todos, from docs/specs/search-todos/prd.md"`
3. **Confirm the criteria before the research.** The first gate: the decision context, the options and a weight per criterion. An external search engine is flagged by the one-SQLite non-goal in `docs/PRODUCT.md`. The floor option, a plain `LIKE` query on what exists, is always in the set. Adjust the weights now, because wrong weights waste the research.
4. **Spike what research cannot settle.** Whether FTS5 is built into the `sqlite3` module your Python ships, and how fast each option is on 10,000 todos, only running code can tell. `decide` hands the question to `spike`, which builds in its own worktree, commits on a `spike/<slug>` branch, removes the worktree and reports a Spike Verdict: the question, the answer with numbers, how to rerun it, and what it did not cover. The verdict folds back into the trade-off as evidence. Run on its own, the command is:
   Command: `/andthen:spike "is FTS5 in our Python's sqlite3, and how fast are LIKE and FTS5 on 10,000 todos?"`
5. **Accept the recommendation and choose the ADR status.** The second gate: the chosen option, what it buys over the floor, and which criteria decided it and which only broke ties. Accept it, refine the weights, or ask for a deeper look at one option. Then `decide` plays back the settled set and asks whether the ADR goes in as `Accepted` or `Proposed`.
6. **Keep the result, remove the spike code.** Check that the verdict's numbers made it into the ADR or `research.md`. AndThen keeps the spike branch as evidence by default; once the result lives in the ADR, deleting it is your call. The worktree is already gone, and the branch needs `-D` because it was never merged.
   Command: `git worktree list`
   Command: `git branch -D spike/<slug>`
7. **Plan from the decision.** `decide` closes on this command. The FIS's Architecture Decision cites the new ADR.
   Command: `/andthen:plan docs/specs/search-todos/`

### The artifacts

```
docs/
├── adrs/
│   └── ADR-003-<title>.md      the decision and its door type
├── DECISIONS.md                one new Current ADRs row
└── research/
    └── todo-search/
        ├── research.md         findings per option
        ├── tradeoff-matrix.md  a weighted score per criterion
        └── recommendation.md   the report: read it first
.agent_temp/spike/<slug>/       the worktree, removed at the end
spike/<slug>                    the spike code, never merged
```

Note: The names are examples: `decide` picks the ADR title and the topic folder, `spike` the branch name. A decision with several independent dimensions also gets `design-tree.md`.

### What you do with them

1. **Read `recommendation.md` first.** Its Executive Summary gives the answer in one paragraph, and How to Read This Report explains the weights. Check which criteria decided it and which only broke ties.
2. **Read the ADR's Reversal line and Alternatives.** A one-way door deserves a slow read. The floor option and the flagged external engine are both listed, each with the reason it lost.
3. **Make the spike result durable.** The Spike Verdict's numbers and its rerun command belong in the ADR's References or in `research.md`. Record the decision and its evidence, never the code.
4. **Remove the spike code.** With the verdict recorded, delete the `spike/<slug>` branch. Spike code is never merged or reused: the real implementation is written fresh from the FIS.
5. **Commit the decision with the PRD.** `git add docs` takes the ADR, `DECISIONS.md` and the research folder. `plan` and every later skill read them through the Index.

Sizing check: Close options on a two-way door need no trade-off: pick one. A load-bearing choice with no real alternative is one Still Current line in `DECISIONS.md`. A contested choice gets the trade-off and an ADR. A question only measurement settles gets a spike, and only then.

## Next

Component: a row of buttons that switch tabs. The first is filled, the others are outlined.

- Do the Foundation Lab → (lab)
- Back to the Core Loop → (loop)
- Explore the skills → (skills)
