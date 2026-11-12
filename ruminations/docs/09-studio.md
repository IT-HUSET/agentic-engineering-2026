---
title: AndThen Studio
tab: Studio
token: studio
order: 9
depends_on: []
source: https://github.com/IT-HUSET/andthen-studio (README)
---

# AndThen Studio

Eyebrow: Companion app

## See what AndThen writes, live

Component: "live" in the title is set in the accent colour.

AndThen leaves its work in files: the PRD, ADRs, plan.json, the FIS, review reports. Studio renders those files in your browser, live from the working tree and git, so you can read, check and discuss them while the Core Loop runs. Claude Code stays where you work; Studio is where you look.

Component: under the lead, four facts as small labelled chips, then two link buttons: the first filled, the second outlined.

- Runs on: your machine only, `http://127.0.0.1:7420`
- Reads: the artifacts of AndThen `1.0.0-rc.6` and later
- Screen: desktop browsers, no phone layout
- Status: private repository, pre-1.0

Button: Install it in the Setup tab → (setup)
Button: AndThen Studio on GitHub → (https://github.com/IT-HUSET/andthen-studio)

## Start it — One terminal of its own

Component: numbered white cards (01, 02, 03), each with title, text and an optional command in a dark box with a copy button, like the Setup steps. Each command box starts hidden behind a "Show command" button, as on the Setup tab.

1. **Start it from the project root.** In the Foundation Lab that is `todo-app/`, the same folder Claude Code runs in. Use a terminal of its own, beside Claude Code and the app: Studio holds that terminal until you stop it.
   Command: `andthen_studio`
2. **Let it open the browser.** It serves the project on `http://127.0.0.1:7420`, or the next free port up to 7429, and prints which agent CLI it will use. Started again for the same project, it opens the running Studio instead of a second one. Pages update on their own when a file or git changes, so leave the tab open.
3. **Stop it with Ctrl-C** when you are done. Nothing to clean up: its own state lives in `.agent_temp/`, which `init` puts in `.gitignore`.

Note: Started from the repository root instead, Studio finds no Document Index and searches for `plan.json` files on its own. Start it from `todo-app/`, or pass the folder: `andthen_studio todo-app`.

## The views — What Studio shows

Studio finds every artifact through the Project Document Index that `init` writes into `CLAUDE.md`. No Index, no map: run `init` first.

Component: a table with three columns. The view name in bold, then what it shows, then where it helps in the Foundation Lab as small step chips (F1–F7) that switch to the Foundation Lab tab and select that step.

| View | What it shows | In the lab |
| - | - | - |
| **Project home** | Every artifact Studio found, grouped by type: project documents, ADRs, requirements, review reports, models and boards, plus the git worktrees. The sidebar links the documents the Index names. | F1 |
| **Reader** | PRDs, ADRs, the glossary and other markdown, with a section list and linkable sections. | F2, F3 |
| **Plan board** | One plan's stories as status columns, with their dependencies and task progress. A story opens its FIS and the diff of its changes, found through its commit trailers, its branch or uncommitted work. | F4, F5 |
| **Review report** | A review report with its lens, target, verdict, finding index, coverage matrix and `## Remediation Status`. | F6 |
| **Walkthroughs** | A guided tour of a pull request or a git range such as `main...feat/shared-lists`, written by an agent, with focus points for the reviewer and a "reviewed" mark per file. | F7 |
| **Notes** | Remarks you attach to a section of any view. Copy them as markdown, or send them to an agent. | F2–F4 |
| **Atlas and boards** | The architecture or glossary model, event storms and context maps from `docs/models/`. Empty in the Foundation Lab: they need `describe --model` or `architecture`, which the extension labs use. | — |

## AI actions — Three things an agent can do from Studio

With Claude Code (or Codex) on the `PATH`, Studio can start an agent run, one at a time. Without one, it starts with AI actions off and says so.

Component: three white cards side by side (stacked on a phone), each with a title, a line on what it changes in rust, and the text.

1. **Explain** · Changes nothing. Pick a section, and the agent reads only that section and says what it means and why it is there. Good for an ADR's Reversal line or a FIS scenario you can't place.
2. **Send notes** · Changes one artifact. The agent gets your notes on an artifact and revises it through the AndThen skill that owns it: a PRD through `clarify`, a FIS through `plan`. If the run fails or leaves the file unchanged, the notes go back to your open list.
3. **Produce walkthrough** · Changes nothing in the project. The agent reads a pull request or a git range and writes a walkthrough under `.agent_temp/walkthrough/`. Source code is not touched.

## Rules for Studio — Look here, work there

Component: three white cards with rust numerals 01–03, like the Core Loop rules.

1. **The files are the truth.** Studio is a view of what AndThen wrote. When the view and a file disagree, the file wins: read it in your editor or with `git diff`.
2. **No notes while `exec-plan` runs.** Send notes edits an artifact, and a FIS edited mid-run is the same as hand-editing it. Read and write notes freely, and send them after the run.
3. **Send notes leaves a change to review.** It is the only action that edits a project file. Check it with `git diff` and commit it by path, like any other change, before the lab's next `git status` check.

## Troubleshooting

Component: a collapsed details box per question.

Summary: The home page says 0 plans

`plan.json` lives under `docs/specs/` only between F4 and F7. Before F4 there is none yet, and `ship` deletes it in F7, so 0 plans is the right answer then. A plan you parked in `.agent_temp/` is not shown either. If a plan should be there, check the Specs & Plans row in the Index, or start Studio with `--specs-dir docs/specs`.

Summary: Models, boards and tours are empty

Expected in the Foundation Lab. The atlas needs `andthen:describe --model`, event storms and context maps need `andthen:architecture`, and a walkthrough appears only after you produce one.

Summary: AI actions are off

Studio needs Claude Code `2.1.273` or later, or Codex `0.154.0` or later, on the `PATH`. Its startup output says which one it found. Point it at another executable with `--agent claude --agent-bin <path>`.

Summary: Is my version current?

`andthen_studio --version` prints the installed release. Studio never checks for updates itself: compare with the releases page, and run the install command again to update.

## Next

Component: a row of buttons that switch tabs. The first is filled, the others are outlined.

- Do the Foundation Lab → (lab)
- Walk the Core Loop → (loop)
