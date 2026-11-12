---
title: AndThen:init
tab: Init
token: init
order: 3
depends_on: [shared/skills.md]
---

# AndThen:init

Eyebrow: andthen:init

## What andthen:init puts in Claude’s memory

Component: "andthen:init" in the title is set in the accent colour.

Init runs once per project as a short process: it detects what is there, writes the defaults, then offers extras you choose. Below, the process step by step, with what each step reads and writes. Where those files sit among the rest of Claude’s memory is on the Claude’s memory tab.

### The key idea

`CLAUDE.md` is the only file init always puts in Claude’s memory every session, so init leaves no TODO in it. Other documents get a line in its Project Document Index, and Claude opens them only when a task matches.

## The process — How andthen:init runs, step by step

Init runs as a short process: it detects what the project has, writes the defaults, and then offers extras you choose. Click any shape to see what it reads or writes, with an example.

Interactive component: a 760 × 590 process diagram in a BPMN-like style, across the full width, with the detail card under it, also full width. On a wide screen the card puts the Example beside the text; without an Example the text takes the whole card. Three row headings: Reads · Process · Writes. Reads are data objects (a page with a folded corner) joined by a dotted association to "1 Detect"; the dashed "agents/" object joins "3 Offer extras". The process runs left to right: a thin start circle, rounded tasks, diamond gateways with an ×, a user task with a person icon, and a thick end circle, joined by solid sequence arrows. The first gateway labels its branches "none" (up) and "exists" (down); the second labels "empty repo" (up) and "has files" (right). Writes are data objects in two bands: ALWAYS, OR BY DEFAULT (plain) joined to "2b" by a dotted line marked "from 2a or 2b", and ONLY IF YOU ACCEPT (lavender, dashed objects) joined to "3 Offer extras". A "Hide offers" checkbox dims the dashed objects. The card shows the Kind as eyebrow, the Label as title, the Path in mono, the Text, and the Example in a dark code box when there is one. Card tint: reads cream, events and gateways teal, steps rust, your answer teal, writes green, offers lavender. Starts on s3.

Hint below 960 px: Scroll sideways to see the whole diagram.

Legend: Start · Task · You answer · Gateway: one path · End · Data object · Only if you accept (dashed)

Source: Based on the init skill in AndThen {andthen_version}.

| Id | Label | Subtitle | Shape | Box | Border |
| - | - | - | - | - | - |
| r1 | CLAUDE.md | AGENTS.md too | data | 24, 32, 108, 52 | solid |
| r2 | docs/ | and guidelines | data | 146, 32, 108, 52 | solid |
| r3 | README | and manifest | data | 268, 32, 108, 52 | solid |
| r4 | Task runner | Makefile, CI | data | 390, 32, 108, 52 | solid |
| r5 | Tests, UI | and workspace | data | 512, 32, 108, 52 | solid |
| r6 | agents/ | installed roles | data | 634, 32, 108, 52 | dashed |
| start | /andthen:init |  | start | 52, 238, 15 | solid |
| s1 | 1 Detect |  | task | 84, 214, 96, 48 | solid |
| g1 | Instruction file? |  | gateway | 224, 238, 20 | solid |
| g2 | Empty repo? |  | gateway | 278, 174, 18 | solid |
| ask | What is it? |  | user | 320, 104, 128, 34 | solid |
| s2a | 2a From template |  | task | 320, 154, 128, 40 | solid |
| s2b | 2b Repair in place |  | task | 320, 286, 128, 40 | solid |
| g3 | Paths meet |  | gateway | 492, 238, 20 | solid |
| s3 | 3 Offer extras |  | task | 532, 214, 112, 48 | solid |
| end | Summary | Next: clarify | end | 700, 238, 15 | solid |
| w1 | CLAUDE.md | Index and rules | data | 28, 376, 106, 52 | solid |
| w7 | Dev commands | fast and full | data | 142, 376, 106, 52 | solid |
| w9 | .gitignore | two entries | data | 256, 376, 106, 52 | solid |
| w5 | Role agents | model and effort | data | 392, 376, 108, 52 | dashed |
| w2 | Critical rules | in CLAUDE.md | data | 512, 376, 108, 52 | dashed |
| w4 | Output style | settings.json | data | 632, 376, 108, 52 | dashed |
| w3 | Personal rules | ~/.claude | data | 392, 442, 108, 52 | dashed |
| w8 | Optional docs | pick from six | data | 512, 442, 108, 52 | dashed |
| w6 | Sub-projects | for a monorepo | data | 632, 442, 108, 52 | dashed |
| w10 | Next skills | three commands | data | 392, 508, 108, 52 | dashed |

### Details

Format: id · Kind · Path · Text, then an optional Example. The card shows the Label as title.

- **start** · Start · `/andthen:init [project name]` · You run it once per project, from its root folder. Without a name it takes the folder's or the manifest's. It never overwrites: your content is kept, and it replaces only what you pick.
  Example:
  ```
  /andthen:init
  /andthen:init "todo-app"
  ```
- **r1** · Reads · `./CLAUDE.md, ./AGENTS.md` · Decides the path at the first gateway. No instruction file means a fresh one from the template; an existing one is repaired in place, keeping your content.
- **r2** · Reads · `docs/, docs/guidelines/` · Every AndThen document already there gets a line in the Project Document Index, at the path where it was found.
  Example:
  ```
  found   docs/DECISIONS.md
  writes  - **Decisions** – `docs/DECISIONS.md`: ADR index and Still Current notes. …
  ```
- **r3** · Reads · `README.md, pyproject.toml, package.json and similar` · The project name and tech stack fill the Project Overview. Only in an empty repository, with no manifest, README or source file, does init ask you what the project is.
  Example:
  ```
  pyproject.toml  name "todo-app"
                  "Modern todo application with FastAPI, HTMX, and Shoelace"
                  Python >= 3.11, FastAPI, SQLAlchemy, pytest
  ```
- **r4** · Reads · `Makefile, justfile, the CI workflow, the manifest's scripts` · Gives the fast, full and run-one-test commands that seed the Key Dev Commands document.
  Example:
  ```
  pyproject.toml has pytest  →  fast  uv run pytest -x -q
                                full  uv run pytest
  ```
- **r5** · Reads · `a test folder or test script · a UI framework, templates or a dev server · a workspace config` · Decides which extras you are offered: a test strategy, visual-validation setup, or sub-project files for a monorepo.
  Example:
  ```
  tests/                 →  offer /andthen:testing --mode strategy
  src/app/templates/     →  offer /andthen:visual-validation --mode setup
  ```
- **r6** · Reads · only for one offer · `.claude/agents/, ~/.claude/agents/` · Read only if you accept the role-agent offer: init compares what is installed with its templates and asks before it replaces a file.
- **s1** · Step · `Step 1` · Scans the project once. It asks nothing and writes nothing: what it finds picks the path and the extras.
- **g1** · Gateway · `no CLAUDE.md or AGENTS.md → 2a · one exists → 2b` · Exactly one path is taken. A project that has been through init before always takes 2b, so running init again is safe. What it does then is under the diagram.
- **g2** · Gateway · `no manifest, README or source file?` · An empty repository takes the question first. Anywhere else init takes the Project Overview from the README, the manifest and the code, and asks nothing.
- **ask** · You answer · `one question, only in an empty repository` · Before it writes anything, init asks in one question what the project is. Your answer fills the Project Overview.
  Example:
  ```
  What is this project?
  > A todo app for the course: FastAPI, HTMX and SQLite
  ```
- **s2a** · Step · `Step 2a: no instruction file` · Writes the instruction file from AndThen's template, adds an Index line for each AndThen document found, resolves or deletes every TODO, and appends the two .gitignore entries. When there is a manifest, a subagent seeds Key Dev Commands. Nothing else is created.
  Example:
  ```
  Claude Code only   →  CLAUDE.md
  Codex only         →  AGENTS.md
  both, or unclear   →  AGENTS.md, and a CLAUDE.md whose first line is @AGENTS.md
  ```
- **s2b** · Step · `Step 2b: an instruction file exists` · Keeps your content and adds only what is missing, without asking: Index lines for unlisted documents, the Index preamble, an empty Project Overview, missing sections, Key Dev Commands and the .gitignore entries. Two changes are only offered, at step 3: converting CLAUDE.md and AGENTS.md to the shared layout, and adding a missing counterpart file.
- **g3** · Gateway · `2a and 2b meet` · Whichever path ran, init goes on to the extras.
- **s3** · Step · `Step 3: offer the rest` · "Offer the rest" means the optional extras. After the defaults, init lists the ones that fit your project, one line each, and does only what you accept. Accepted, it does it now. Declining the critical rules writes a skip marker, so you are not asked again. An extra you ignore writes nothing, and the next run offers it again.
  Example (the shape, not the exact wording):
  ```
  Offers
  - Role agents oracle, implementer, reviewer, worker – pin model and effort?
  - Critical rules – adopt into CLAUDE.md?
  - Documents – Product, Decisions, Learnings, Tech Debt, Roadmap, Ubiquitous Language?
  - /andthen:testing --mode strategy – a test suite was found
  - /andthen:visual-validation --mode setup – a served UI was found
  ```
- **end** · End · `the closing summary` · Lists only what this run created or changed, one line per file with its purpose, then the offers, and how to commit review reports. It closes by recommending clarify as the first step.
  Example:
  ```
  Created  CLAUDE.md                         instructions and the Document Index
  Created  docs/KEY_DEVELOPMENT_COMMANDS.md  fast, full and run-one-test commands
  Changed  .gitignore                        .agent_temp/ and review reports
  Next: /andthen:clarify
  ```
- **w1** · Writes · always · `./CLAUDE.md, or AGENTS.md plus a CLAUDE.md that imports it` · The Project Overview, the Project Document Index, guidelines and rules. Claude Code loads it at the start of every session, which is why init leaves no TODO in it. The other documents get a line in its Index and are read only when a task matches.
  Example:
  ```
  ## Project Document Index

  Documents here are read whole when their trigger matches, so keep them short …

  - **Key Dev Commands** – `docs/KEY_DEVELOPMENT_COMMANDS.md`: dev, test, build, deploy commands. Read before running verification; update when a command changes.
  - **Agent Temp** – `.agent_temp/`: scratch workspace for reviews, research, and QA; never ship from it.
  ```
- **w7** · Writes · by default · `docs/KEY_DEVELOPMENT_COMMANDS.md` · Created when a manifest exists, by a subagent, so the templates stay out of the main context. Read when the Index points to it, before verification. exec-plan runs fast once per story and full at the end.
  Example:
  ```
  | fast         | uv run pytest -x -q             | Once per story |
  | full         | uv run pytest                   | End of run     |
  | run one test | uv run pytest {file}::{test}    | One test       |
  ```
- **w9** · Writes · always · `.gitignore` · Not memory: it keeps scratch files and review reports out of git. Delete the second line to commit review reports.
  Example:
  ```
  .agent_temp/
  *-andthen-*-review-*.md
  ```
- **w5** · Writes · if you accept · `.claude/agents/ for the team, or ~/.claude/agents/ for you` · oracle, implementer, reviewer and worker, which pin a model and effort for each subagent tier. They load at session start, so they apply from the next session. Without init, you can copy them from the plugin's templates: the Anatomy tab shows how, and the defaults.
  Example:
  ```
  ---
  name: reviewer
  model: opus
  effort: medium
  ---
  ```
- **w2** · Writes · if you accept · `# Critical Rules and Guardrails in the root instruction file` · AndThen's guardrails, adopted into the project file so they travel with the repository into CI and containers. Declined, a skip marker is written instead, and you are not asked again.
  Example:
  ```
  # Critical Rules and Guardrails
  …
  or, when you decline:
  <!-- AndThen critical rules: skipped -->
  ```
- **w4** · Writes · if you ask · `outputStyle in ~/.claude/settings.json` · Brief, plain, critical answers, the answer first. Init merges the setting and keeps your other keys. It takes effect next session.
  Example:
  ```
  "outputStyle": "andthen:concise-critical"
  ```
- **w3** · Writes · if you ask · `~/.claude/CLAUDE.md` · The same guardrails for you personally, in every project on this machine. Written only when you ask for it.
- **w8** · Writes · if you accept · `docs/PRODUCT.md, DECISIONS.md, LEARNINGS.md, TECH-DEBT-BACKLOG.md, ROADMAP.md, UBIQUITOUS_LANGUAGE.md` · You pick from one line. Each picked document gets a file from its template and a line in the Index. A document you skip is created later by the first skill that writes to it.
- **w6** · Writes · if you accept · `<sub-project>/CLAUDE.md` · For a monorepo: a light instruction file per sub-project, with its commands and the conventions that differ from the root. Claude Code reads it when it works in that folder.
- **w10** · Runs next · if you accept · `three skills, offered as commands` · Three extras run another skill instead of writing a file: describe for an existing codebase with no Architecture document, testing in strategy mode when there is a test suite, and visual-validation setup when there is a served UI.
  Example:
  ```
  /andthen:describe
  /andthen:testing --mode strategy
  /andthen:visual-validation --mode setup
  ```

## Running it again — What happens if you run andthen:init again

Init is safe to run again. Your instruction file now exists, so it always takes path 2b, and it never writes over your content. Run it again after an AndThen upgrade, or after adding documents by hand, and it fills the gaps. What it does with each thing depends on what the thing is.

Component: four columns under the process (two on a medium screen, one on a phone), in the style of the columns after ship on the Paths tab. Each column has an eyebrow, a title and a list of items, each a name with a short note. Under them, the exception as a muted line.

### Left as it is

- Eyebrow: Never touched
- Tint: green
- **Your text** · everything you wrote in `CLAUDE.md` and `AGENTS.md`
- **Existing documents** · keep their content; at most they get a line in the index
- **Your answer style** · an existing `outputStyle` is never replaced
- **A symlinked instruction file** · reported, never written through

### Filled in without asking

- Eyebrow: Step 2b
- Tint: teal
- **Index lines** · for AndThen documents not listed yet
- **The index preamble** · its opening sentences, matched to the template
- **Project Overview** · only when it is empty or a TODO
- **Missing sections** · added to the root instruction file
- **Key Dev Commands** · when there is a manifest but no document
- **.gitignore** · the two lines, when missing

### Asked first

- Eyebrow: Step 3
- Tint: lav
- **Role agents** · each file that differs from the template is named before it is replaced
- **Critical rules** · an existing policy is replaced only when you ask for an update, with the diff shown first
- **CLAUDE.md and AGENTS.md** · converting both to the shared layout, or adding the missing one

### Offered again

- Eyebrow: Next run
- Tint: cream
- **Offers you skipped** · an offer you left unanswered comes back
- **Documents not created yet** · on the same single line to pick from
- **The skill offers** · describe, testing and visual-validation, while what triggers them is still there

Exception: a no to the critical rules leaves the marker `<!-- AndThen critical rules: skipped -->`, so init does not ask again. Delete the marker to get the question back.

## Next

Component: a row of buttons that switch tabs. The first is filled, the other is outlined.

- See where every part of AndThen lives → (anatomy)
- See where Claude’s memory lives → (memory)
