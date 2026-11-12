---
title: AndThen Anatomy
tab: Anatomy
token: anatomy
order: 5
depends_on: []
source: AndThen 1.1.0 – plugin/README.md, skills/init/references/offers.md, skills/init/templates/, hooks/README.md, permissions/README.md (https://github.com/IT-HUSET/andthen); the plugin folders under ~/.claude/plugins/
---

# AndThen Anatomy

Eyebrow: Where things live

## Every part of AndThen, and where it lives

Component: "where it lives" in the title is set in the accent colour.

AndThen lives in three places: Claude Code's folder on your machine, the plugin it installed, and the project you work in. This tab maps all three, says where you set what, and shows how AndThen picks a model for each kind of work.

Component: under the lead, a row of link buttons that scroll to the three sections below, the first filled, the others outlined.

- The map → (#an-map)
- Where do I set…? → (#an-set)
- Models → (#an-models)

## The map — Three places on disk

Click a file or folder to see what it is, who writes it and when you touch it yourself. Paths are shown the macOS and Linux way; on Windows, `~` is your user folder, such as `C:\Users\<you>`.

Interactive component: three white cards side by side (stacked on a phone), one per place, each with an eyebrow, a title and a tree of clickable nodes indented by Level, a folder or file icon before each name (a name ending in "/" is a folder). Under the cards, a detail card for the selected node: its full path, what it is, who writes it, and when you touch it. Starts on the project's `CLAUDE.md`. Up and down arrow keys move through all nodes in order.

### machine

- Eyebrow: Your machine
- Title: Claude Code's folder
- Root: ~/.claude/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `~/.claude/` | 0 | Claude Code's home on your machine: your personal settings, plugins and agents, shared by every project. | Claude Code | Rarely, and never inside `plugins/` by hand. |
| `settings.json` | 1 | Your personal settings: the plugins you enabled, the marketplaces you added, the output style, hooks and permissions. | Claude Code and the `/plugin` commands; `init` adds `outputStyle` when you ask | When adding the marketplace clashes with an old entry (see Setup), or to set `"outputStyle": "andthen:concise-critical"`. |
| `agents/` | 1 | Role agents for every project (user level): `oracle`, `implementer`, `reviewer` and `worker`, each pinning a model and effort. Empty until you accept `init`'s offer or copy the templates here. | `init`, when you accept the role-agents offer at user level | To change which model a role uses everywhere. See Models. |
| `output-styles/` | 1 | Your own output styles. Needed only if your Claude Code version does not list `andthen:concise-critical`. | you | Rarely. |
| `plugins/` | 1 | Every plugin and marketplace Claude Code knows about. | the `/plugin` commands | Never by hand. Read the two JSON files to see what you run. |
| `known_marketplaces.json` | 2 | Each marketplace and the source it follows: for AndThen, `IT-HUSET/andthen`: the latest release by default, `@develop` for pre-releases, or a release tag. | `/plugin marketplace add` | Read it to see which branch or tag you follow. |
| `installed_plugins.json` | 2 | Each installed plugin, its version and the folder it loads from. | `/plugin install` | Read it to see which AndThen version is installed. |
| `marketplaces/andthen/` | 2 | A clone of the whole AndThen repository: the plugin plus the README, COOKBOOK, CHANGELOG, hooks and permissions. | `/plugin marketplace add`, and each update | Read the COOKBOOK here, and copy hooks or permissions from it. |
| `COOKBOOK.md` | 3 | Recipes: which path for which situation, and the artifact table the Paths tab is built from. | AndThen's authors | When you wonder how the skills fit together. |
| `hooks/` | 3 | Optional Claude Code hooks: one blocks destructive shell commands, one hints when the context is getting large, two notify you. | AndThen's authors | Copy the ones you want into your settings. Nothing is installed for you. |
| `permissions/` | 3 | Example permission and sandbox settings that keep shell commands away from your secrets and the network. | AndThen's authors | Copy what you need. Nothing is installed for you. |
| `cache/andthen/andthen/1.1.0/` | 2 | The installed copy that Claude Code actually loads, one folder per version. Its contents are the middle card. | `/plugin install`, and each update | Never. An update replaces it. |

### plugin

- Eyebrow: The plugin
- Title: What AndThen is made of
- Root: plugins/cache/andthen/andthen/<version>/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `<version>/` | 0 | The plugin as installed. You read it, you never edit it: an update replaces the folder. | AndThen's release | Read it to see exactly what a skill does. |
| `.claude-plugin/plugin.json` | 1 | The manifest: the plugin's name and version, and the folder of output styles it registers. | AndThen's release | Read the version. |
| `skills/` | 1 | The 21 skills, one folder each. `/andthen:<skill>` runs the folder of that name. | AndThen's release | Never by hand. |
| `<skill>/SKILL.md` | 2 | The skill itself: a description that says when it triggers, the argument hint, the rules, the workflow and the follow-up line it closes on. | AndThen's release | Read it when a skill surprises you: the answer is in here. |
| `<skill>/references/` | 2 | Detailed procedures the skill reads only when it needs them, such as `decide`'s `trade-off.md` or `ui-ux-design`'s `mode-wireframes.md`. | AndThen's release | Read it for the details behind a step. |
| `<skill>/agents/openai.yaml` | 2 | The skill's display name and default prompt in Codex. It is not a model setting. | AndThen's release | Never. |
| `init/templates/` | 2 | What `init` copies into your project or your machine. | AndThen's release | Read it to see what an offer installs. |
| `CLAUDE.template.md` | 3 | The starting point for a project's `CLAUDE.md`: the Project Document Index, project rules and Conventions. | AndThen's release | Never: `init` copies it. |
| `agents/claude/` | 3 | The four role agents with their model and effort pins, ready to copy. `agents/codex/` and `agents/copilot/` hold the same for Codex and Copilot CLI. | AndThen's release | Never: `init` copies them, and you edit the copies. |
| `guidelines/CRITICAL-RULES-AND-GUARDRAILS.md` | 3 | The critical-rules starter `init` offers for your `CLAUDE.md`. | AndThen's release | Never: once adopted, the copy in `CLAUDE.md` is yours. |
| `output-styles/concise-critical.md` | 3 | Brief, plain, critical answers, answer first. The plugin registers it as `andthen:concise-critical`. | AndThen's release | Never: you turn it on in `settings.json`. |
| `references/` | 1 | Contracts several skills share: `plan.schema.json`, `fis-contract.md`, `review-calibration.md`, `unattended-runs.md`, `project-document-templates.md`. | AndThen's release | Read it when you wonder what a `plan.json` or a FIS must contain. |

### project

- Eyebrow: Your project
- Title: What AndThen adds to a repo
- Root: todo-app/

| Node | Level | What it is | Written by | When you touch it |
| - | - | - | - | - |
| `todo-app/` | 0 | The project root, where you start Claude Code and every skill runs. | you | Always start here. |
| `CLAUDE.md` | 1 | Claude's memory for this project: the Project Document Index that tells every skill where documents live, your project rules, and the Conventions `describe` adds. | `init`, then each skill that creates a document adds its Index line | To move a document, add a rule or adopt the critical rules. The Init tab shows it in detail. |
| `.claude/agents/` | 1 | Role agents for this project only (project level), shared with the team through git. A project agent wins over a user agent with the same name. | `init`, when you accept the role-agents offer at project level, or you, copying the templates | To pin models for the whole team. See Models. |
| `docs/` | 1 | The documents the Index names. Each is created by the first skill that writes to it. | the skills | Read them; edit them when the project changes. |
| `KEY_DEVELOPMENT_COMMANDS.md` | 2 | The dev, test and build commands, including the `fast` and `full` check tiers `exec-plan` runs. | `init` | When a test or build command changes. |
| `PRODUCT.md` | 2 | Vision, principles, non-goals and the Proportionality facts (stage, scale, technical non-goals) that size every proposal. | the first of `clarify`, `decide`, `plan` or `architecture` to need them | When the stage or scale changes. |
| `DECISIONS.md` and `adrs/` | 2 | The ADR index, Still Current lines and the ADRs themselves. | `decide` | Read before reopening a choice. |
| `UBIQUITOUS_LANGUAGE.md` | 2 | One name per concept, and the synonyms to avoid. | `domain --mode glossary`, `clarify` | When a term settles. |
| `LEARNINGS.md` | 2 | Traps worth remembering: “watch out for X”, a non-obvious failure that bit someone. Why a choice was made belongs in `DECISIONS.md`. | `ship`, `triage`, `handoff` | Read at the start of a task. |
| `TECH-DEBT-BACKLOG.md` | 2 | Fixes deferred with their blockers, by severity, so a finding you put off is not lost. | `review --fix` and `implement-fix` for a finding you defer, `triage` | Read when you work in an area with a listed item. An entry you can state in one sentence is an `implement-fix`. |
| `specs/<feature>/` | 2 | The PRD, and while the branch lives, `plan.json`, the FIS files and review reports. `ship` deletes the plan files on your yes, or keeps them marked `shipped`. | `clarify`, `plan`, `exec-plan`, `review` | Read the PRD; let the skills own the rest. |
| `research/`, `models/`, `wireframes/`, `design-system/` | 2 | Trade-off analyses, typed models, wireframes, clickable mockups (in `mockups/`, one folder per feature) and the design system, each when its skill runs. | `decide`, `describe --model`, `domain`, `ui-ux-design` | Commit them; read them before revisiting. |
| `REVIEW-POLICY.md`, `ISSUE-TRACKER.md`, `VISUAL-VALIDATION.md`, `TESTING-STRATEGY.md` | 2 | Optional settings documents for reviews, the issue tracker, screen capture and tests. | you (Review Policy), `tracker setup`, `visual-validation --mode setup`, `testing --mode strategy` | When you want to change how that skill behaves. |
| `.agent_temp/` | 1 | Scratch space, never committed: `reviews/`, `handoff/`, `spike/`, `visualize/`, and Studio's notes. | the skills, and Studio | Read handoffs and reports; clean it out when you like. |
| `.gitignore` | 1 | `init` adds `.agent_temp/` and the review-report pattern. | `init` | Delete the review-report line to commit reports. |

## Where do I set — Where do I set…?

Each setting AndThen honours has one place, and every skill reads it from there, so a change made once holds for every later run.

Component: a table with three columns, Question, Where and How, in a white box that scrolls sideways on a narrow screen. Code in the Where column is mono.

| Question | Where | How |
| - | - | - |
| Which model a kind of work uses | `.claude/agents/<role>.md` (project) or `~/.claude/agents/<role>.md` (you) | Change `model` and `effort` in the frontmatter, then start a new session. No such file yet? Copy them from the plugin's templates, as under Models. |
| Which model runs without role agents | your session | `/model` in Claude Code, or the model picker in the app. Every subagent inherits it. |
| How briefly Claude answers | `~/.claude/settings.json` | Set `"outputStyle": "andthen:concise-critical"` and start a new session. A project setting overrides it. |
| Where a document lives | `CLAUDE.md`, Project Document Index | Move the file and edit its Index line. Skills find documents by entry name, so keep the names. |
| Which commands prove the code works | `docs/KEY_DEVELOPMENT_COMMANDS.md` | Edit the `fast` and `full` rows. `exec-plan` runs `fast` per story and `full` on the final tree. |
| Rules every session must follow | `CLAUDE.md` | Add them under Project-Specific Guidelines and Rules, or adopt the Critical Rules section `init` offers. |
| Which AndThen version you run | `~/.claude/plugins/known_marketplaces.json` and `installed_plugins.json` | Update with `/plugin marketplace update andthen` and `/plugin update andthen@andthen`, then restart. To switch branch or tag, remove the marketplace and add it again as `IT-HUSET/andthen@<ref>`. |
| What a review skips or adds | `docs/REVIEW-POLICY.md` | Write it from the starter in AndThen's README, then run `/andthen:init seed Review Policy` to add its Index line. |
| Your issue tracker, and where requirements live after a merge | `docs/ISSUE-TRACKER.md` | Run `/andthen:tracker setup`. `Record: repo` keeps `prd.md`; `Record: tracker` keeps it in the issues. |
| Whether review reports are committed | `.gitignore` | Delete the review-report line `init` added. |
| Blocking dangerous shell commands | the `hooks` in your `settings.json` | Copy `block-dangerous-commands.py` from the AndThen repository's `hooks/` and register it as a PreToolUse hook. |
| Running a skill without questions | the command itself | Add `--auto`: open decisions become `ASSUMPTION:` lines. `clarify` has no unattended form. |

## Models — Which model does what

AndThen never names a model in a prompt. Each skill hands work to a role: the installed role agent when there is one, else a subagent on your session's model, with judgment work kept in your session.

Component: four white cards side by side (two by two on a tablet, stacked on a phone), one per role: the role name in mono, its model and effort as two small chips, and what it is used for.

| Role | Model | Effort | Used for |
| - | - | - | - |
| `oracle` | fable | high | Judgment you assign it, such as a design or a second opinion, and hard problems another agent hands over because they exceed its tier. |
| `implementer` | sonnet | high | One medium or large unit of pinned work: building a story, writing a plan story's FIS, research that weighs sources. |
| `reviewer` | opus | medium | Every review, of any target, returning findings and a verdict. |
| `worker` | haiku | high | Small, well-specified subtasks: lookups, scans, mechanical edits. |

### Install and change them

Component: numbered white cards (01–05), like the Setup steps, each command hidden behind a "Show command" button.

1. **Check what you have.** If neither `~/.claude/agents/` nor the project's `.claude/agents/` exists, every skill runs on your session's model: change that with `/model` in Claude Code, or with the model picker in the app. From `todo-app/`:
   Command: `ls ~/.claude/agents .claude/agents`
2. **Get the files: let `init` offer them.** Run `init` again. On a project that is already set up it takes the repair path, keeps everything you have, and offers the role agents among its extras. Choose project level to share the pins with the team, or user level for yourself.
   Command: `/andthen:init`
3. **Or copy the templates yourself.** They ship with the plugin. This copies all four into the project, from `todo-app/` in Git Bash:
   Command: `mkdir -p .claude/agents && cp ~/.claude/plugins/cache/andthen/andthen/{andthen_version}/skills/init/templates/agents/claude/*.md .claude/agents/`
4. **Change a pin.** Open the role's file, such as `.claude/agents/reviewer.md`, and edit `model` and `effort` in its frontmatter. Keep `name` as it is: a skill asks for the role by that name.
5. **Start a new session in `todo-app/`.** Agent definitions load when a session starts, and the project's agents apply only to sessions started in `todo-app/`, where its `.claude/agents/` lives.

Note: Never edit the templates inside the plugin: an update replaces them. Edit your copies, and check their pins again when the model lineup changes.

## Next

Component: a row of buttons that switch tabs. The first is filled, the others are outlined.

- See what andthen:init writes → (init)
- Back to Setup → (setup)
- Explore the skills → (skills)
