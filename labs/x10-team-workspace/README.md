# X10 reference files

Files for [X10 – Team workspace](../x10-team-workspace.md). Nothing here is needed to do the exercise: your own `team-home` is your answer. These are the target to compare with when you get stuck.

| Path | What it is |
|---|---|
| `example-team-home/` | A finished `team-home` for the made-up team Betala (marketplace `betala-team`, repos `orders-api`, `web-shop` and `infra`). It has the structure your own `team-home` should get. Swap `betala`, `team-tools` and `~/work` for your own names |
| `measure/` | Optional scripts for the larger measurement in "Going further": twelve `claude -p` runs and a readout. They are not part of `team-home` and are copied to `~/x10/` |

## `example-team-home/`

Marked by the part of X10 that uses it:
- **Stories S01 and S02:** pointers, catalog and a plugin in a marketplace. In the exercise the plugin carries your own skill and hooks from X9. The example plugin's catalog skill and catalog sensor only show the shape.
- **Going further:** the template repo, the session flow and the measurement. The files are finished but the exercise does not need them.

| File | Part | What it does |
|---|---|---|
| `AGENTS.md` | S01 | Rules for all repos, where things live and the "Other repos" table with path and remote |
| `CLAUDE.md` | S01 | Only `@AGENTS.md`, so the file loads whatever lies above it |
| `catalog/orders-api.md` | S01 | A catalog entry with the fields the sensor requires |
| `.claude-plugin/marketplace.json` | S02 | The marketplace `betala-team` with the plugin `team-tools` |
| `plugins/team-tools/.claude-plugin/plugin.json` | S02 | The plugin manifest, deliberately without `version` |
| `plugins/team-tools/hooks/hooks.json` | S02 | Registers the sensor as `PostToolUse` on `Write\|Edit` |
| `plugins/team-tools/scripts/check-catalog.sh` | S02 | The sensor: exit 2 with a message to the agent when a catalog entry lacks fields |
| `plugins/team-tools/skills/catalog-entry/SKILL.md` | S02 | `/team-tools:catalog-entry <repo>` writes the catalog entry |
| `templates/golden-path/Makefile` | Going further | `check` (gitleaks and the repo's tests, red until `TEST_CMD` is replaced) and `setup` |
| `templates/golden-path/.claude/settings.json` | Going further | Marketplace and plugin for the new repo |
| `templates/golden-path/AGENTS.md`, `CLAUDE.md` | Going further | Stubs that point to `team-home` |
| `plugins/team-tools/skills/session-note/SKILL.md` | Going further | `/team-tools:session-note <topic>`, started only by a human |
| `plugins/team-tools/scripts/propose-note.sh` | Going further | gitleaks, a branch in a temporary worktree, push and PR |

`decisions/`, `sessions/` and `wiki/` belong in your `team-home` but are empty here, and git does not keep empty directories.

Try it from `example-team-home/`:

```bash
claude plugin validate ./plugins/team-tools
claude plugin validate .
```

Both exit 0 with warnings about a missing `version` and `author`, which is expected. The first also prints catalog checks (LICENSE, icon) that only matter for a plugin submitted to the plugin directory.

The scripts under `plugins/team-tools/scripts/` must be executable (`chmod +x`). Git keeps the bit.

## `measure/`

`measure.sh` asks three questions with and without `team-home`, two runs per arm, and `readout.sh` counts opened files and searches in the output. Copy both and `measure-settings.json` to `~/x10/` (the scripts point there) and run them with `bash`, since they have no shebang. Prerequisites:
- **Without `~/.claude`:** `CLAUDE_CONFIG_DIR=~/x10/cfg` gives a directory with no `CLAUDE.md`, settings or plugins. Login and trust belong to the directory: run `claude` interactively once with the variable set, sign in and accept the trust dialog in `~/team-home` and `~/work`.
- **Not `--bare`:** it skips `CLAUDE.md` discovery and reads only `ANTHROPIC_API_KEY`, not your login.
- **`--tools "Read,Grep,Glob"`:** on macOS and Linux, `Grep` and `Glob` are otherwise missing and the agent searches through Bash. Both arms get the same three tools, so `readout.sh` counts only Read, Grep and Glob. In the interactive test in step 5, count Bash `find`, `grep`, `rg`, `ls` and `cat` too.
- **The `InstructionsLoaded` hook** in `measure-settings.json` logs `CLAUDE.md` files, and `AGENTS.md` only when a `CLAUDE.md` imports it. That is why arm A's `CLAUDE.md` imports the file.
- Twelve runs use plan quota (check `/usage`). `--max-turns` and `--max-budget-usd` are runaway caps, and the budget compares against a client-side list-price estimate, not a bill. If arm B searches for a long time the caps can cut it off: count that as a failure. `readout.sh` prints that estimate as `est_list_usd`.

## What has been run

- **On these files, 2026-11-15, Claude Code 2.1.323:** `claude plugin validate` on the plugin and the marketplace, `bash -n` on all scripts, `python3 -m json.tool` on all JSON, `check-catalog.sh` on synthetic input (exit 0 for a complete entry, exit 2 for one with empty fields), and `make check` in `templates/golden-path` (red, and green with a stubbed `gitleaks`).
- **On the Swedish originals, 2026-11-13 (the English files differ only in text):** `plugin marketplace add`, `plugin install` and `plugin details` against a local path, `propose-note.sh` with stubbed `gitleaks` and `gh` against a local bare repo (branch, commit and PR call, and exit 1 without a branch on a leak), `measure.sh` with a stubbed `claude`, and `readout.sh` on synthetic rows.
- **Without a model, 2026-11-15:** `gate-tests-green.py` (the X9 gate that X10's plugin carries) with `TEAM_TEST_CMD` set (blocks on red tests, silent on green) and unset (exit 0, also in a non-Python repo), and `propose-note.sh` without a git repo at `TEAM_HOME` (exit 1 with a message).
- **Not run:** the hook firing in a live session, `propose-note.sh` against real gitleaks and GitHub, `make setup` and the `--scope project` install against GitHub, `measure.sh` against a real `claude`, the `--settings` hook firing under `claude -p`, and how trust is stored under another `CLAUDE_CONFIG_DIR`.
