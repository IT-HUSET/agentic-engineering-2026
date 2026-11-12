---
title: Claude’s memory
tab: Claude’s memory
token: memory
order: 10
depends_on: []
---

# Claude’s memory

Eyebrow: Claude Code memory

## What Claude reads, and what it remembers

Claude Code starts every session by reading instruction files from several places, and keeps notes of its own between sessions. Below, where each file lives and when it loads, then how you open and manage them with `/memory`. The files andthen:init writes carry an “init” badge.

## Where it lives — Global or project: where Claude’s memory lives

Claude Code reads instructions from several places. Some follow you into every project, some travel with the repository, and some stay with you alone. Click a box to see the path and when it loads.

Interactive component: 680 × 512 diagram beside a sticky detail card. An ORGANIZATION band (cream) across the top, then three columns: GLOBAL · YOU, EVERY PROJECT (teal), PROJECT · SHARED IN GIT (green), PROJECT · ONLY YOU (lavender). Below, LOAD ORDER AT SESSION START: Managed policy → Global files → Project, root → here, + MEMORY.md, with the caption "Nothing overrides: every file is joined into context, and the one closest to your folder is read last." The card takes the column tint. Starts on b1.

Hint below 960 px: Scroll sideways to see the whole diagram.

Legend: Loaded at session start (solid) · Loaded on demand (dashed) · Written by andthen:init (rust "init" badge)

Source: Based on [How Claude remembers your project](https://code.claude.com/docs/en/memory) in the Claude Code docs, October 2026.

| Id | Label | Subtitle | Box (x, y, w, h) | Border | Badge |
| - | - | - | - | - | - |
| org | Managed policy CLAUDE.md | Set by IT · session start | 32, 62, 616, 48 | solid |  |
| a1 | ~/.claude/CLAUDE.md | Session start | 32, 162, 176, 48 | solid |  |
| a2 | ~/.claude/rules/ | Session start | 32, 220, 176, 48 | solid |  |
| b1 | ./CLAUDE.md | Session start | 252, 162, 176, 48 | solid | init |
| b2 | .claude/rules/ | Session start | 252, 220, 176, 48 | solid |  |
| b3 | Path-scoped rules | When files match | 252, 278, 176, 48 | dashed |  |
| b4 | sub/CLAUDE.md | When Claude works there | 252, 336, 176, 48 | dashed | init |
| c1 | CLAUDE.local.md | Session start | 472, 162, 176, 48 | solid |  |
| c2 | MEMORY.md | Claude writes · 200 lines | 472, 220, 176, 48 | solid |  |
| c3 | Memory topic files | Claude reads when needed | 472, 278, 176, 48 | dashed |  |

### Details

Format: id · Title · Kind · Tint · Path · Text.

- **org** · Managed policy CLAUDE.md · Organization · session start · cream · `macOS: /Library/Application Support/ClaudeCode/CLAUDE.md · Linux and WSL: /etc/claude-code/CLAUDE.md · Windows: C:\Program Files\ClaudeCode\CLAUDE.md` · Organization-wide instructions managed by IT or DevOps, for every user on the machine. It is loaded first, before your own files.
- **a1** · ~/.claude/CLAUDE.md · Global · session start · teal · `~/.claude/CLAUDE.md` · Your personal preferences for every project on this machine. Loaded after the managed policy and before any project file. You write it.
- **a2** · ~/.claude/rules/ · Global · session start · teal · `~/.claude/rules/*.md` · Personal rule files for every project, one topic per file. They load before project rules. Neither set overrides the other, so keep them consistent.
- **b1** · ./CLAUDE.md · Project · shared in git · session start · green · `./CLAUDE.md or ./.claude/CLAUDE.md` · Team instructions checked into git: build commands, conventions, architecture. Claude also loads the CLAUDE.md in every folder above the one you start in. andthen:init writes this file. With no CLAUDE.md at all, Claude reads AGENTS.md instead.
- **b2** · .claude/rules/ · Project · shared in git · session start · green · `.claude/rules/*.md` · Topic rule files, found recursively. Without a paths field they load at launch with the same priority as .claude/CLAUDE.md.
- **b3** · Path-scoped rules · Project · shared in git · on demand · green · `.claude/rules/*.md with paths: in the frontmatter` · Rules with a file pattern, such as src/api/**/*.ts. They load only when Claude works with matching files, which keeps the context small.
- **b4** · sub/CLAUDE.md · Project · shared in git · on demand · green · `<subfolder>/CLAUDE.md` · Instruction files in folders below where you started. Each one loads once Claude reads, writes or edits a file in that folder. andthen:init can write these for a monorepo.
- **c1** · CLAUDE.local.md · Project · only you · session start · lav · `./CLAUDE.local.md, listed in .gitignore` · Your private notes for this project, such as sandbox URLs or test data. It loads right after CLAUDE.md in the same folder, so it is read last at that level. It exists only in the worktree where you created it.
- **c2** · MEMORY.md · Auto memory · Claude writes · session start · lav · `~/.claude/projects/<project>/memory/MEMORY.md` · The auto memory index that Claude keeps itself, one line per memory. The first 200 lines or 25KB load every session. All worktrees of the repo share it, but it stays on this machine.
- **c3** · Memory topic files · Auto memory · Claude writes · on demand · lav · `~/.claude/projects/<project>/memory/*.md` · One file per memory, of type user, feedback, project or reference. They are not loaded at startup; Claude reads them when it needs them. Browse, edit or delete them with /memory.

## Manage your memory — Open and manage it with /memory

Type `/memory` in a Claude Code session to see every memory file for this project and for you, open one in your editor, and turn auto memory on or off. Pick what you want to do.

Interactive component: a list of goal buttons, each showing the command on the right ("just say it" when the command is a sentence), beside a rust card with the eyebrow "Command", the goal as title, the command with a copy button, the text and a muted note. Starts on the first goal. Each command box starts hidden behind a "Show command" button, as on the Setup tab.

| Goal | Command | Text | Note |
| - | - | - | - |
| See and edit my memory files | `/memory` | Lists your CLAUDE.md, CLAUDE.local.md and other memory files for you and for this project. Select one to open it in your editor. A user or project CLAUDE.md that does not exist yet is listed too, and selecting it creates it. | A GUI editor such as VS Code opens a separate window and you can keep working. A terminal editor such as Vim takes over the terminal until you exit. |
| See what Claude has saved about me | `/memory` | Choose the option to open the auto memory folder. MEMORY.md is the index, and each memory is its own markdown file that you can edit or delete. | The folder is ~/.claude/projects/<project>/memory/. When Claude says "Saved 2 memories" or "Recalled 2 memories", it is writing or reading there. |
| Turn auto memory on or off | `/memory` | Use the auto memory toggle. It saves autoMemoryEnabled in your user settings, ~/.claude/settings.json, so it applies to all your projects. | To turn it off for one project only, set "autoMemoryEnabled": false in that project’s settings. |
| Check which files loaded | `/context` | Shows what is in the context right now. Look under Memory files to see which CLAUDE.md and rules files loaded when the session started. | Files in subfolders and path-scoped rules load later, when Claude works with matching files. |
| Make Claude remember something | `remember that we use pnpm, not npm` | Just say it. When you ask Claude to remember something, it saves it to auto memory, which only you have. | For an instruction the whole team should follow, say "add this to CLAUDE.md" instead, or edit the file through /memory. |
| Find outdated or conflicting instructions | `/doctor prompt-audit` | Claude checks your instruction files for instructions written for older models, references to files that no longer exist, and files that contradict each other. You get a report with proposed edits. | Nothing changes until you ask Claude to apply the edits. Requires Claude Code v2.1.283 or later. |

## Next

Component: a row with one filled button that switches tabs.

- Back to what andthen:init writes → (init)
