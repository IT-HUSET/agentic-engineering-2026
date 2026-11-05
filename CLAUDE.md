# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The **participant repository** for a hands-on course on **structured agentic software engineering** – the end-to-end workflow for getting reliable results from AI coding agents. You'll run the loop using **[AndThen](https://github.com/IT-HUSET/andthen)**, with spec-driven development as its backbone: from a fuzzy idea, to clarified requirements, to a spec, to a verified implementation, to a review, to a pull request.

This repo is for **learning by doing**. Follow the labs in [`labs/`](labs/README.md); the goal is the workflow and the judgment to right-size it, not just the code.

## Setup

Install AndThen as a Claude Code plugin:

```bash
/plugin marketplace add IT-HUSET/andthen@develop
/plugin install andthen@andthen
```

Your facilitator can pin an exact release tag (`IT-HUSET/andthen@v1.0.0-rc.<N>`) before the course; use the line they give you. If an older AndThen (0.x) is installed, run `/plugin marketplace remove andthen` first, because both marketplaces share a name.

Then, when unsure where to start, run `/andthen:now-what`: it inspects the project and routes you to the right skill.

## The workflow you'll practice

> idea → [**`clarify`**] → **`plan`** → **`exec-plan`** → **`review --fix`** → **`ship`**

- **`clarify`** interviews you about a vague idea (gaps, edge cases, scope) and writes the PRD. Optional: skip it when the requirements already exist.
- **`decide`** (optional, between `clarify` and `plan`) settles a technical choice that binds beyond one story or is costly to reverse, and records it as an ADR. **`domain --mode glossary`** fixes one name per concept.
- **`plan`** writes the **Feature Implementation Specification (FIS)**: what to build, the proof for each acceptance scenario, when it's done. It decides whether the work is one story or several and writes a `plan.json` beside the FIS files. No code changes.
- **`exec-plan`** builds a FIS, or runs a plan directory with one fresh subagent per story. A story is `done` only on a quoted line from a check that actually ran, and a fresh reviewer checks each one.
- **`review --fix`** reviews the finished work as a whole (spec fit, code, security, outcome) and applies the findings marked `Fix`.
- **`ship`** lands what was learned, drops the plan files, and opens the pull request after your one yes.

Every skill works standalone. Each pipeline step ends by printing the next command to paste, so run each step in a fresh session (`/clear`).

### Right-sizing the work

Part of the skill is choosing *how much structure* a piece of work deserves:

| Work | Path |
|------|------|
| A fix you can state in one sentence | `implement-fix "<request>"` → `ship`. Unknown cause or broken build: `triage` first |
| One real feature | [`clarify` →] `plan` → `exec-plan <FIS>` → `review --fix` → `ship` |
| Several features | [`clarify` →] `plan <dir>` → `exec-plan <dir>` → `review --fix` → `ship` (`--worktree` runs independent stories in parallel) |

The entry test: if you can't list three acceptance criteria, start with `clarify`; otherwise start with `plan`. `--worktree` and `--auto` are switches, not sizes. Design is right-sized the same way: none for a typo, an ADR or wireframe for a feature, a Domain Map for a multi-feature product.

## Working conventions

- Let the spec lead. Resist jumping straight to code – the whole point is that a spec first produces more reliable, verifiable results.
- AndThen runs from the project root. In the foundation lab that is `todo-app/`; paths like `docs/specs/...` are relative to it.
- Verify before claiming done: run the real build and tests. "It works" is only true if you checked.
- Describe symptoms, not fixes, when something's wrong – better input produces better agent output.
- Don't hand-edit code in the middle of an `exec-plan` run. Let it finish, or stop and amend the FIS.
