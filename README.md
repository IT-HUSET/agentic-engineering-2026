# Agentic Software Engineering 2026 – Lab

Hands-on lab for practicing the **end-to-end workflow for structured use of AI coding agents** – with spec-driven development (via **[AndThen](https://github.com/IT-HUSET/andthen)**) as the backbone.

## Prerequisites

- One of Claude Code, Codex CLI or GitHub Copilot CLI, installed and signed in.
- A plan with room for three days of agent runs. IT-HUSET staff use the company's Claude team seat; other participants bring their own subscription.
- `git`, the GitHub CLI [`gh`](https://cli.github.com) signed in (`gh auth login`), and [`uv`](https://docs.astral.sh/uv/getting-started/installation/) for the Python app.
- Basic command-line comfort.
- The prep session, live or recorded, before the course.

Don't want to install on your own machine, or on Windows without WSL2? Use the [dev container](.devcontainer/README.md), locally or in GitHub Codespaces.

## Get started

1. Create your own repo from this one and clone it (recommended). On GitHub choose **Use this template → Create a new repository**, pick your account, and tick **Include all branches**. Your day 1 changes are then saved, and your pull request opens in your own repo.
2. Install AndThen:
   ```bash
   # Claude Code
   /plugin marketplace add IT-HUSET/andthen
   /plugin install andthen@andthen

   # Codex CLI
   codex plugin marketplace add IT-HUSET/andthen
   codex plugin add andthen@andthen

   # GitHub Copilot CLI
   copilot plugin marketplace add IT-HUSET/andthen
   copilot plugin install andthen@andthen
   ```
   This installs the latest AndThen release. **Note:** the course material is based on AndThen 1.0.0 and rechecked against 1.1.0, so a later release may differ in details. Already have AndThen installed? Update it (`claude plugin update andthen@andthen` in Claude Code). If you added it from a tag or `@develop`, remove the `andthen` marketplace first (`/plugin marketplace remove andthen`; in Codex `codex plugin remove andthen@andthen`, then `codex plugin marketplace remove andthen`; in Copilot `copilot plugin marketplace remove andthen`): a marketplace stays on the ref it was added with. The labs show the `/andthen:<name>` commands of Claude Code and Copilot CLI. In Codex, ask for the skill by name: *Run the `andthen:init` skill*.
3. Check your setup from the repo root:
   ```bash
   uv run check.py
   ```
   It checks `git`, `gh`, each host it finds (signed in, AndThen installed) and the `todo-app` tests, and ends with a `GREEN` or `RED` line. One ready host is enough. Fix every `FAIL` before Day 1: everyone runs it again when Day 1 starts.
4. Read [CLAUDE.md](CLAUDE.md) for the workflow you'll practice.
5. Follow [`labs/README.md`](labs/README.md): the foundation lab first, then the case work.

The [`todo-app/`](todo-app/) directory is the lab's brownfield base – an existing FastAPI app you'll evolve by running the loop on a real feature.

## How the course runs

- **Foundation (Day 1).** The loop for one feature, once, on `todo-app/`: [`labs/foundation.md`](labs/foundation.md).
- **Case work.** The same loop on a case, with the amount of structure you choose written down and a gate at each artifact.
- **Exercise catalog.** Optional deepening (X1–X10): at the end of Day 3 if there is time, or earlier when your case calls for one. X9 and X10 are for teams that already run Claude Code and AndThen daily.

## The one idea

The differentiator in AI-assisted development isn't the model or the tool – it's the **workflow you run it through.** Most AI coding goes straight from idea to code; fine for small fixes, but complex features drift and miss requirements. The fix is a repeatable loop – clarify, plan, implement, review, ship – and the judgment to right-size it. This lab is where that clicks.
