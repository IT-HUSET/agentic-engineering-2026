# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The **participant repository** for a hands-on lab on **spec-driven development (SDD)** with AI coding agents. You'll practice the SDD workflow using **[AndThen](https://github.com/IT-HUSET/andthen)** — going from a fuzzy feature idea to a spec, then to a verified implementation, then a review.

This repo is for **learning by doing**. Follow the lab steps; the goal is the workflow, not just the code.

## Setup

Install AndThen as a Claude Code plugin:

```bash
/plugin marketplace add IT-HUSET/andthen
/plugin install andthen
```

Then, when unsure where to start, run `/andthen:now-what` — it inspects the project and routes you to the right skill.

## The SDD workflow you'll practice

> idea → **`/andthen:clarify`** → **`/andthen:spec`** → **`/andthen:exec-spec`** → **`/andthen:review`** → ship.

- **`clarify`** turns a vague idea into solid requirements by probing gaps and edge cases.
- **`spec`** produces a **Feature Implementation Specification (FIS)** — the contract: what to build, how to verify it, when it's done. No code changes here.
- **`exec-spec`** implements against the FIS and attests each acceptance scenario.
- **`review`** gives a focused pass (code / gap / security) before you ship.

For bigger scope, the path extends through `prd` → `plan` → `exec-plan`. Every skill also works standalone — you don't have to run the whole pipeline.

## Working conventions

- Let the spec lead. Resist jumping straight to code — the lab's whole point is that a spec first produces more reliable, verifiable results.
- Verify before claiming done: run the real build/tests; "it works" is only true if you checked.
- Describe symptoms, not fixes, when something's wrong — better input produces better agent output.
