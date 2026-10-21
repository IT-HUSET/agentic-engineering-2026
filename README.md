# Agentic Software Engineering 2026 – Lab

Hands-on lab for practicing the **end-to-end workflow for structured use of AI coding agents** – with spec-driven development (via **[AndThen](https://github.com/IT-HUSET/andthen)**) as the backbone.

## Prerequisites

- Claude Code installed and authenticated (a Claude.ai account with Claude Code access).
- Basic command-line comfort.
- The prep session, live or recorded, before the course.
- The recorded prerequisite videos (working as an architect, strategic DDD, and others) before Day 1. Your facilitator shares the links.

## Get started

1. Fork this repo to your own GitHub account and clone your fork (recommended). Your day 1 changes are then saved, and your pull request has somewhere to go. Run `gh repo set-default <your-account>/agentic-engineering-2026` in the clone, so pull requests open in your fork and not against the course repo.
2. Install AndThen:
   ```bash
   /plugin marketplace add IT-HUSET/andthen@develop
   /plugin install andthen@andthen
   ```
   Your facilitator can pin an exact release tag before the course and will tell you if the lines differ. If you have AndThen 0.x installed, run `/plugin marketplace remove andthen` first.
3. Read [CLAUDE.md](CLAUDE.md) for the workflow you'll practice.
4. Follow [`labs/README.md`](labs/README.md): the foundation lab first, then the case work.

The [`todo-app/`](todo-app/) directory is the lab's brownfield base – an existing FastAPI app you'll evolve by running the loop on a real feature.

## How the course runs

- **Foundation (Day 1).** The loop for one feature, once, on `todo-app/`: [`labs/foundation.md`](labs/foundation.md).
- **Case work.** The same loop on a case, with the amount of structure you choose written down and a gate at each artifact.
- **Exercise catalog.** Optional exercises (X1–X8) you pull when your case calls for them.

## The one idea

The differentiator in AI-assisted development isn't the model or the tool – it's the **workflow you run it through.** Most AI coding goes straight from idea to code; fine for small fixes, but complex features drift and miss requirements. The fix is a repeatable loop – clarify, plan, implement, review, ship – and the judgment to right-size it. This lab is where that clicks.
