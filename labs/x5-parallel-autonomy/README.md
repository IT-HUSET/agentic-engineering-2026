# X5 material: Going further

Files for the two deepenings in [`../x5-parallel-autonomy.md`](../x5-parallel-autonomy.md#going-further): **Who holds the plan?** (three forms, same plan, same start) and **A pipeline with no one in the chair** (headless, unattended, behind a fence). Both run on the same workload, built by `setup.sh`.

| File | What it does | Used in |
|---|---|---|
| `setup.sh` | `work` builds `$X5/work` (default `$HOME/x5`) as its own repo with the PRD, ADR, glossary and plan committed, `.claude/settings.json` with `worktree.baseRef: "head"` and `.claude/worktrees/` in `.gitignore`. `tag` checks that S01 and S02 are `done` in `plan.json`, that tracked files are clean and that the tests pass, then sets the tag `x5-start`. `clones` makes `x5-a1`, `x5-b1` and `x5-c1` from the tag, without `origin`, and prints three SHAs | Both |
| `settings.json` | The fence for unattended runs, used with `--permission-mode auto`: no allow rules, so the classifier reviews every shell command; `.env` denied, bypass mode disabled, `git push` asks, sandbox with no network and `autoAllowBashIfSandboxed` off (sandboxed commands still reach the classifier), token variables unset inside it, write access to the repo's `.git` and uv's cache. Replace the two placeholders. Copy it to `.claude/settings.json` | Pipeline |
| `fence-check.sh` | Checks in the container that the host's credentials did not follow you in: `SSH_AUTH_SOCK`, `ssh-add -l`, `credential.helper`, `git credential fill`, `gh auth status` and token variables. OK or WARNING per check, never prints a secret | Who holds the plan |
| `overlap.sh` | Load with `source`. `areas <fis>` lists the files under `### Work Areas`, `overlap <clone> <range>` the files both S03 and S04 committed | Who holds the plan |
| `templates.md` | The guess and the rule | Who holds the plan |
| `story-pipeline.js` | **Answer key and fallback for form B, not the starting point.** A workflow that reads `plan.json`, computes the waves from `dependsOn`, runs one agent per story (parallel ones in their own worktree, capped by `maxParallel`), merges, runs the test gate and stops on red. Arguments: `planDir`, `maxParallel`, `stopAfter` | Who holds the plan |

`setup.sh work` takes the bundle from `SOL`, the folder your facilitator hands out, and `todo-app/` from this repo (`REPO`, default `/workspaces/agentic-engineering-2026`). The folder holds `f2-shared-lists-prd.md`, `f3-shared-lists-adr.md`, `f3-shared-lists-glossary.md` and `f4-shared-lists-whole-prd/` (`plan.json` and five FIS files). `work` overwrites `.claude/settings.json`, so run it before you copy `settings.json` in.

<details>
<summary>What was checked, and what was not</summary>

Checked locally on a test repo with a stand-in for `uv` (2026-11-13 and 2026-11-15, the scripts as they were before translation):

- `bash -n` on the shell scripts, and a syntax check of `story-pipeline.js` wrapped in a function (it has top-level `await` and `return`).
- `setup.sh work` against `todo-app/`: plan committed on `feat/shared-lists`, no `MISSING` lines. `tag` refused while S01 was `pending`, refused with a modified tracked file, and passed with S01 and S02 `done` and a clean tree. `clones`: three equal SHAs, no remotes, `worktree.baseRef: "head"` in the clone.
- `areas` against the real FIS files: S03 and S04 share `docs/ARCHITECTURE.md`, `docs/UBIQUITOUS_LANGUAGE.md`, `src/app/core/`, `src/app/database.py` and `src/app/routes/shares.py`. `overlap` against a test repo with two `Story-ID:` commits returned the shared file.
- `fence-check.sh` in a clean environment (all OK) and with `SSH_AUTH_SOCK`, a token variable and a credential helper set (WARNING).
- `story-pipeline.js` against a stand-in that pretends to be the workflow runtime: a green run (four waves, two at a time), a failed story, a merge conflict, a red test and `stopAfter`.

Not checked:

- All three forms (A, B, C) and `/andthen:review` on their results.
- `setup.sh` with a real `uv` and in the real container. `fence-check.sh` in a real container with the host's credentials forwarded.
- `settings.json` under `--permission-mode auto` in a real `claude -p` run (2026-11-16): the classifier's verdicts on `uv run pytest`, `git commit` and subagent spawns, and whether `autoAllowBashIfSandboxed: false` sends sandboxed commands to the classifier. The shape follows the Claude Code documentation, not a run.
- `story-pipeline.js` against the real workflow runtime, and whether a workflow subagent can reach `andthen:exec-plan`. It uses `isolation: 'worktree'` on parallel agents, while AndThen's `story-worktrees.md` (v1.1.0) has the orchestrator create worktrees itself.
- That a rerun of `exec-plan` resumes after a manual merge, `claude --bg` with a skill as the prompt from the shell, which branch name a background session's worktree gets, and that `/usage` carries the subagents' cost.

</details>
