# Agentic Software Engineering 2026 – Lab

Hands-on lab for practicing the **end-to-end workflow for structured use of AI coding agents** – with spec-driven development (via **[AndThen](https://github.com/IT-HUSET/andthen)**) as the backbone.

## Prerequisites

- Claude Code installed and authenticated (a Claude.ai account with Claude Code access).
- Basic command-line comfort.
- The prep session, live or recorded, before the course.
- The recorded prerequisite videos (working as an architect, strategic DDD, and others) before Day 1. Your facilitator shares the links.

## Get started

1. Install AndThen:
   ```bash
   /plugin marketplace add IT-HUSET/andthen
   /plugin install andthen
   ```
2. Read [CLAUDE.md](CLAUDE.md) for the workflow you'll practice.
3. Follow the lab steps your facilitator provides (exercises land here as the lab is built out).

The [`todo-app/`](todo-app/) directory is the lab's brownfield base – an existing FastAPI app you'll evolve by running the loop on a real feature.

## The one idea

The differentiator in AI-assisted development isn't the model or the tool – it's the **workflow you run it through.** Most AI coding goes straight from idea to code; fine for small fixes, but complex features drift and miss requirements. The fix is a repeatable loop – clarify, spec, implement, verify, review – and the judgment to right-size it. This lab is where that clicks.
