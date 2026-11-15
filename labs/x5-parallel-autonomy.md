# X5 – Parallelize, run unattended

**What you do:** run your plan with less of you in it, in three steps where each earns the next. First **sequential** (one fresh subagent per story), then **parallel** (`--worktree`), then **unattended** (`--auto`) inside a sandbox, with a coordinating review loop on top.

**Why it matters:** a plan with independent stories waits on you for no reason, and a run nobody watches is only safe behind a fence you have seen hold. You find out where that line goes for your own case.

**What you have at the end:** every story `done` with its proof, one merged branch per story under `--worktree`, a sandbox you have seen refuse a command, and the run's assumptions read by you. Teams that have done all of it can go on to [Going further](#going-further).

> **Skills:** `exec-plan --worktree`, `exec-plan --auto`, the four role agents from `init`, and AndThen's `permissions/` and `hooks/` examples · Your choice: this exercise is pulled after C3, never assigned.

## When to pull it

Pull X5 when one of these is true for your plan:

- **Parallel: two stories that do not depend on each other.** *Check:* open `<feature-dir>/plan.json`. Are there two or more pending stories that `dependsOn` does not connect? If every story chains behind the one before, `--worktree` buys nothing: run the plan plainly.
- **Unattended: you are ready to stop watching.** *Check:* you have read the FIS files, C3 is green, and you are willing to read afterwards what the run assumed.

## Input

Your team's plan after C3: `plan.json` with the first story `done` and at least two stories left. If your plan has no independent stories, your facilitator has a prepared several-story plan with two independent stories to run on.

## Output

- A plan run: every story `done` with a `verified.summary`, one commit per story, and an aggregate report that ends in a `Scope:` line and a `Verification:` line.
- Under `--worktree`: one `story/<id>` branch per story merged with a `git merge --no-ff`.
- A sandbox you have seen refuse a command, a destructive-command hook you have seen fire, and role agents that pin model and effort per task type.

## Steps

### 1. Entry check

1. List independent stories: for each pending story, write its `dependsOn`. Circle two with no edge between them.
2. For `--worktree`, check two preconditions. Tracked files must have no uncommitted changes (`git status`), and the plan bundle must be **committed**: a gitignored `docs/specs/` fails the run, because a worktree holds no copy of an untracked bundle.

### 2. Sequential baseline

```text
/andthen:exec-plan <feature-dir>
```

You gave `exec-plan` a FIS in F5. Given a plan directory, it runs the plan: one fresh subagent per ready story, one at a time in the shared tree, because a shared tree shares one test run. Each story runs the fast check tier and its proofs; the plan run then runs the **full** tier once on the final tree. A story that fails is reported with a route out, its dependents are reported `skipped`, and other stories continue only when the failed changes are provably isolated. It closes with the aggregate report and one `Next (fresh session):` line: the plan-level review. Run this first, so you have a baseline to compare the parallel run against.

### 3. Parallel with `--worktree`

On a plan with two independent pending stories:

```text
/andthen:exec-plan --worktree <feature-dir>
```

What changes:
- Each ready story runs on its own branch (`story/<id>`) in its own git worktree, in batches of about five, so the stories cannot clobber each other's files.
- After each batch, every successful story is merged back with `git merge --no-ff story/<id>`, then its worktree and branch are removed. A batch's dependents branch from a base that already holds what they depend on.
- A failed story **keeps** its branch and worktree, and a rerun resumes there. A merge conflict fails the story, except for lines both sides appended to the changelog or `Learnings`. The skill does not resolve other conflicts for you.

Look at what it left: `git log --graph --oneline`, `git worktree list`, `git branch`.

Run this before you turn the sandbox on in step 4. The OS sandbox denies writes to `.git/worktrees`, so inside it `--worktree` cannot create its worktrees: the run falls back to sequential and records that as an assumption (checked on Claude Code 2.1.323).

### 4. Draw the boundary before you go unattended

An agent's shell commands run as you. Three layers catch what the one above misses: **approval** (a prompt, not a boundary), **rules** (patterns that match a command as written, so a deny on `curl` misses the same request made from a script), and the **OS sandbox** (the only layer that contains a command). Read `permissions/README.md` and `hooks/README.md` in the AndThen repository (github.com/IT-HUSET/andthen, tag `v1.0.0`, the version the course pins). Then, if you choose to (this is opt-in, touches your personal settings, and covers Claude Code and Codex only):

1. **Merge the personal baseline** from `permissions/claude/settings.json` into your `~/.claude/settings.json`. It turns the sandbox on with the network off, hides `.env` files, cloud credentials and browser profiles from commands, makes `git push` ask, and refuses the bypass flag. It also sets `"defaultMode": "auto"`. From Claude Code 2.1.283 auto mode is already the start mode of interactive sessions where it is available (the status line shows `manual mode on` where it is not), so the baseline mostly pins it. In auto mode a classifier reviews each action in your place. `permissions/README.md` explains the trade-off, so read it before you merge. On native Windows Claude Code has no sandbox; use WSL2.
2. **Install the hook:** copy `hooks/scripts/block-dangerous-commands.py` (and `hooks/configs/blocked-commands.json`) to `~/.claude/hooks/scripts/` and `~/.claude/hooks/configs/`, and add its `PreToolUse` entry from `hooks/README.md`. It refuses `rm -rf`, pipe-to-shell and similar in every mode. Its list is a starting set, not a complete one.
3. **See it work.** In a throwaway directory create `.agent_temp/sandbox-test/.env` containing `FAKE_KEY=not-a-secret`. Ask the agent to print it with `cat`, and to read it with its Read tool. Then ask it to run `rm -rf .agent_temp/sandbox-test`. Note which layer stopped which request.
4. **A command that needs the network** (a `uv sync` that downloads packages) fails inside the sandbox, and the agent asks before running it outside. Sync dependencies before an unattended run.

Never use `--dangerously-skip-permissions` outside a container or VM that holds none of your credentials.

### 5. Role agents

```text
/andthen:init
```

On a project that already has its setup, `init` repairs only what is missing and then offers the extras. Take up the offer for the four **role agents**, `oracle`, `implementer`, `reviewer` and `worker`. Each pins a model and an effort level for one kind of work: `implementer` for executing a story, `reviewer` for any review, `worker` for small well-specified subtasks, `oracle` for judgment you assign it or a problem that exceeded another agent's tier. You choose the level: **user** (a personal default across projects) or **project** (`.claude/agents/`, which shares the pins with the team). They take effect from the **next session**. Without them, every skill falls back to a generic subagent on your session's model. Re-check the pins when your provider's model lineup changes.

### 6. Unattended with `--auto`

In the sandbox, with a plan whose FIS files you have read:

```text
/andthen:exec-plan --auto <feature-dir>
```

`--auto` makes a run ask nothing. It takes each recommendation and records it as `ASSUMPTION: <what> – <what would change it>`, skips any action that needs your consent, and stops with `BLOCKED: <what is needed>` if the call is unusable. Only the flag does this, never how the run was launched, and it passes `--auto` to every skill it invokes.
- `clarify` has no unattended form, because the interview is the skill. An unattended pipeline starts at `plan`, from a requirements file or tracker item.
- `exec-plan` leaves a failed story `in-progress`, skips its dependents, finishes the rest, and **never reviews the plan itself**: the `Next (fresh session):` line is the review, and something has to run it.
- `ship --auto` stops before anything leaves the machine and prints the push and PR commands.

**After** the run, read every `ASSUMPTION:` line in the FIS files and the report before you trust the result.

### 7. A coordinating loop

To review and fix repeatedly without the reports filling the session you steer from, give one session this job (adapted from AndThen's cookbook):

```text
Run a review/fix loop on the implementation of <feature-dir>/plan.json.
Delegate every review and every fix round to its own fresh subagent; this
conversation only coordinates and reports.

Each review subagent invokes the andthen:review skill on that plan; from the
second review on, it also asks for a follow-up on the previous report, by its
path. Each fix subagent invokes the andthen:implement-fix skill on the report
that review wrote. Every subagent brief passes --auto.

Stop when a fix round fixes nothing or its Next line asks for no follow-up
review. Also stop, and report, when a finding survives a fix round unchanged or
a fix needs a decision. Finish with the final verdict, the report paths, and
the remaining Note and DEFERRED findings.
```

The loop ends on the hand-off, never on a verdict or a severity count: a `Note` no fix round may apply can hold a lens at *FAIL*, so "until PASS" may never terminate.

## Verify

- [ ] After the sequential run: every story `done` in `plan.json` with a `verified.summary` that quotes a command, its exit status and a result line. The report's `Scope:` line says complete and its `Verification:` line says passed. You ran at least one summary command yourself.
- [ ] After `--worktree`: `git log --graph` shows a `--no-ff` merge per story, `git worktree list` shows no leftover worktree except a preserved failed one, and the full tier ran once on the final tree.
- [ ] A failed story, if any, is contained: its dependents are `skipped`, not built on, and its branch and worktree are preserved.
- [ ] The sandbox refused the `cat` of the fake `.env`, and the hook refused `rm -rf`. You can say which layer did which.
- [ ] You read each `ASSUMPTION:` line from the unattended run, and overturned or accepted each deliberately.
- [ ] The plan-level `review --fix` still ran afterwards. Autonomy does not replace the gate.

## Sizing check

*Did the machinery match the parallelism and risk that actually existed?* A multi-story plan with independent stories earns `--worktree`. A single story is `exec-plan <FIS>`, as in F5. A fully sequential plan runs plainly, because there is nothing to parallelize and isolation is overhead. `--auto` earns its place when you can afford to read the assumptions afterwards, not when you cannot afford to be asked. The judgment is not "use the most powerful mode", it is to match the machinery to the work.

## Going further

Two deepenings for a team that has run steps 1–7 and wants a harder question answered. Both go **guess, run, keep**: write down what you expect, run it, keep one artifact (a rule, a policy). Claude Code only. Files are in [`x5-parallel-autonomy/`](x5-parallel-autonomy/README.md). Each uses one thing from [X9](x9-harness-workshop.md) (H3's routing table, H5's hooks); skip that step if you have not done X9.

**The workload.** Both run on one plan: five stories on `todo-app` for shared lists, S01 → S02 → (S03, S04) → S05, with a PRD, an ADR and a glossary. Your facilitator hands out the folder that holds them. Build it once, in the dev container or locally:

```bash
cd labs/x5-parallel-autonomy
SOL=<folder from your facilitator> ./setup.sh work    # builds $HOME/x5/work on feat/shared-lists, everything committed
```

Outside the container, add `REPO=<path to this repo>`. To do both deepenings, build a second workload with `X5=$HOME/x5-pipeline`. Your facilitator may already have prepared the repos below, in which case start at the guess.

### Who holds the plan?

> **When to pull it:** your plan has independent stories and you cannot say whether the framework, a script or you should run them.

**Input.** The workload at tag `x5-start` (S01 and S02 `done`), cloned three times. S03 and S04 are independent in `dependsOn`. S05 depends on both.

The same three stories run three times, from the same start. Only who holds the plan changes:

| Form | Who holds the plan | Isolation |
|---|---|---|
| A, the framework | `exec-plan --auto --worktree <dir>` schedules, runs independent stories in parallel and merges | A branch and worktree per story (`story/<id>`) |
| B, a script | A dynamic workflow that Claude writes on your request. The script holds the loop and the intermediate results | Whatever the script asks for |
| C, you | A background session per story, followed in agent view, and you merge | The session moves to its own worktree before it changes files |

Agent teams are a fourth form. They are experimental and off by default, so this exercise does not use them.

**Prepare.**

1. **A container with the OS sandbox off.** The OS sandbox denies `git worktree add` (checked on Claude Code 2.1.323, also from the repo's root), and forms A and C create worktrees. Run in the [dev container](../.devcontainer/README.md) and do not merge step 4's baseline there. No run uses `--dangerously-skip-permissions`: auto mode is the layer, and the dev container docs suggest it for fewer prompts without switching off the safety checks.
2. **The fence.** A container is a fence only when the host's credentials do not come along. On the host, set in VS Code's user settings and rebuild the container (names read from the Dev Containers extension's manifest, not rechecked):

   ```json
   { "dev.containers.copyGitConfig": false,
     "dev.containers.gitCredentialHelperConfigLocation": "none",
     "dev.containers.githubCLILoginWithToken": false }
   ```

   Keep keys out of the host's ssh agent, then run `<repo>/labs/x5-parallel-autonomy/fence-check.sh` in the container before the first `claude`. Still open after that: outbound network, and that the workspace is bind-mounted, so an agent can change host files.
3. **Version and mode.** `claude --version` is 2.1.302 or later, `claude plugin list` shows `andthen` 1.1.x (newer than the `v1.0.0` tag step 4 reads), and `git config --global user.name` and `user.email` are set. If the status line shows `manual mode on`, auto mode is missing and runs will ask: neither A nor C runs unattended.
4. **The start.** Run S01 and S02, each in a fresh session, then tag and clone:

   ```bash
   cd $HOME/x5/work && claude
   ```

   ```text
   /andthen:exec-plan --auto docs/specs/let-people-share-their-lists/s01-view-only-sharing.md
   /andthen:exec-plan --auto docs/specs/let-people-share-their-lists/s02-editor-role.md
   ```

   ```bash
   <repo>/labs/x5-parallel-autonomy/setup.sh tag       # S01 and S02 done, clean tree, tests green, tag x5-start
   <repo>/labs/x5-parallel-autonomy/setup.sh clones    # x5-a1, x5-b1, x5-c1 of the tag, no origin, three equal SHAs
   ```
5. **Trust and quota.** Accept the trust dialog once in each clone (`claude`), or `claude --bg` stops on it. Check `/usage` first: three runs and three reviews use a lot, and parallel agents use it faster. Make `$HOME/x5/results/`.

**Steps.**

1. **Guess.** Read `### Work Areas` in the FIS files for S03 and S04 and fill in the guess from [`templates.md`](x5-parallel-autonomy/templates.md) in `$HOME/x5/results/` before anything runs. The file's timestamp shows it came first. Then ask: what would make you change the guess, and which form do you trust least?
2. **Dependencies are not files.** Compare what the graph and the FIS files say:

   ```bash
   cd $HOME/x5/x5-a1/docs/specs/let-people-share-their-lists && source <repo>/labs/x5-parallel-autonomy/overlap.sh
   jq -r '.stories[] | "\(.id) dependsOn: \(.dependsOn|join(", "))"' plan.json
   comm -12 <(areas s03-invitations.md) <(areas s04-todo-assignment.md)
   ```

   (`areas` reads only paths inside backticks.) Does the result change your guess?
3. **Route the agents** (X9, H3). Decide with your routing table which role runs a story, and read the model afterwards in `/tasks` (A and B) or in agent view (C). In B the agents run on the session's model unless the script says otherwise, so ask the workflow to use `implementer`. In C each background session starts as a plain `claude` in the directory, on the model a new session gets there.
4. **Form A.**

   ```bash
   cd $HOME/x5/x5-a1 && claude -n x5-a1
   ```

   ```text
   /andthen:exec-plan --auto --worktree docs/specs/let-people-share-their-lists/
   ```

   `--worktree` stops if a tracked file is modified or the plan is uncommitted (so `setup.sh` committed it). Read `/usage` before you end the session. Where did you wait for the framework, and where did it wait for you?
5. **Form B.**

   ```bash
   cd $HOME/x5/x5-b1 && CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS=2 claude -n x5-b1
   ```

   Ask Claude to write the workflow. "Use a workflow" is enough as a request, and the keyword `ultracode` makes it explicit:

   ```text
   ultracode: use a workflow to run the stories of docs/specs/let-people-share-their-lists/plan.json
   that are not done. One agent per story, each invoking the andthen:exec-plan skill with --auto
   on the story's FIS. Start every story whose dependsOn are all done at the same time, each in its
   own isolated worktree, then merge the branches in order and run `uv run pytest -q` before the
   next wave. Stop on a red test run or a merge conflict and say which. Never resolve a conflict.
   ```

   In auto mode Claude Code asks for permission the first time. Choose **View raw script** (or `Ctrl+G`) and read the script before you answer. You should be able to point to the line that stops on red, the line that decides S03 and S04 run together, and who merges. Progress is in `/workflows`, with tokens per agent. To keep a run that went well, select it in `/workflows` and press `s`; it is saved under `.claude/workflows/` and reruns as `/<name>`. Who decided that S03 and S04 run together, and what happened when you wanted to change it?
6. **Form C.**

   ```bash
   cd $HOME/x5/x5-c1
   claude --bg --name s03 "/andthen:exec-plan --auto docs/specs/let-people-share-their-lists/s03-invitations.md"
   claude --bg --name s04 "/andthen:exec-plan --auto docs/specs/let-people-share-their-lists/s04-todo-assignment.md"
   claude agents
   ```

   The prompt is the argument, not a `-p` value. Follow the rows in `claude agents` (`Space` peeks, `Enter` opens, `claude agents --json` gives `state`). A row that waits for you is an intervention. When both are done, you merge: `git worktree list` shows the branches, then `git merge --no-ff <branch>` per story, resolve the conflict, `uv run pytest -q`. Start S05 as a third session only after the merge, so it sees S03 and S04. Who saw the conflict first, and what would you have done with ten stories?
7. **Review, measure, write the rule.** In a fresh session in each clone, review without `--fix`:

   ```text
   /andthen:review --auto docs/specs/let-people-share-their-lists/plan.json
   ```

   One row per form. Cost is list price estimated locally, not an invoice. Wall time comes from `/usage` (`Total duration (wall)`) for A and B, and from the row's age in agent view for C, which freezes when the session is done. For C add up `/usage` per session.

   | Run | Cost (list price) | Wall time | Interventions | Outcome |
   |---|---|---|---|---|
   | A, `x5-a1` | | | | stories `done`/`skipped`, who resolved the conflict, `review` verdict |
   | B, `x5-b1` | | | | the same, and whether the story agents reached `exec-plan` |
   | C, `x5-c1` | | | | the same |

   One run per form is an anecdote, so say so. Then write the **rule** (`$HOME/x5/results/rule.md`, template in `templates.md`): which form for which plan, half a page at most, each line pointing to a row in the table.

**Verify.**

- [ ] The three clones share one start: `for f in a b c; do git -C $HOME/x5/x5-${f}1 rev-parse --short x5-start; done` prints three equal SHAs.
- [ ] Each form's outcome is read from `plan.json` (`jq -r '.stories[] | "\(.id) \(.status)"'`). A failed or skipped story is an outcome, not an error.
- [ ] You can show how each form handled the S03/S04 overlap in `git log --graph --oneline x5-start..HEAD`, that `git worktree list` shows only the main tree, and `overlap` against each clone.
- [ ] The guess is in `results/` with a timestamp before the runs, and the measurement table has no empty cell.
- [ ] You can point to the line in the workflow that stops on red, in the script Claude wrote.
- [ ] `fence-check.sh` ran before the first `claude`, and the rule fits half a page.

*Sizing.* A chain runs sequentially: there is nothing to parallelize. Stories with no shared files take `--worktree`. Stories that share files make a conflict expected, and "parallel" then costs a merge. How many stories justify a workflow or background sessions of their own is what your table should give numbers for, and with one run per form it is a direction.

<details>
<summary>Answer key: what the guess should have found</summary>

- **Overlap.** The graph says S03 and S04 depend only on S02. The FIS files say `docs/ARCHITECTURE.md`, `docs/UBIQUITOUS_LANGUAGE.md`, `src/app/core/`, `src/app/database.py` and `src/app/routes/shares.py`. `dependsOn` shows order. `### Work Areas` shows files.
- **Form A, expected (not run in this version).** S03 and S04 land in the same batch. A conflict that is not just lines both sides appended to an append-only document fails the story, aborts the merge (`git merge --abort`) and keeps the branch and worktree. S05 is reported `skipped`. You then resolve it by hand, which counts as an intervention: `git worktree list`, `git merge --no-ff story/S04`, resolve, `git add`, `git commit`, `uv run pytest -q`, `git worktree remove <path>`, `git branch -d story/S04`. Whether a rerun on the same directory picks up S05 after a manual merge is unchecked. The run report ends in `Scope:`, `Verification:` and a `Next (fresh session):` line with the plan review.
- **Form B.** The script has no shell or file access of its own: every check is an agent running a command, and only the control flow is deterministic. The cap is the environment variable (default 16 concurrent agents, 1 to 256 allowed), and the number of agents Claude aims for comes from the size guideline, `medium` (fewer than 10 agents) unless you run `/config workflowSizeGuideline=small`.
- **Form C.** Whoever merges sees the conflict first, so in C it is you, and with ten stories you would be the bottleneck. History shows who isolated and merged: in A the orchestrator, in B whatever the script asks an agent to do, in C you.
- **Cost, as a ballpark only.** In a sandboxed `claude -p` run (so not the same setup), S01 cost 6.84 USD and S02–S05 run sequentially 11.17 USD, one run each, list price. Your interactive auto-mode runs will differ.
- **The workflow answer key.** [`story-pipeline.js`](x5-parallel-autonomy/story-pipeline.js) reads `plan.json`, computes the waves from `dependsOn`, runs one agent per story (parallel ones in their own worktree, capped by `maxParallel`), merges, runs the test gate and stops on red. Compare it with the one Claude wrote: what did Claude do differently, and which line stops on red? Copy it to `.claude/workflows/` in `x5-b1` before `claude` only if Claude does not deliver a runnable script. It has only been tried against a stand-in for the runtime.

</details>

<details>
<summary>Tips and traps</summary>

| Trap | What to do |
|---|---|
| `dependsOn` taken as proof that stories can run in parallel | Compare the Work Areas (`areas`). Parallel writers on the same files cost a conflict |
| The forms start from different commits | Same tag, one clone per form. Change nothing in `work` after the tag |
| Parallel worktrees lack S01 and S02 | The default `worktree.baseRef: "fresh"` branches from the remote's default branch. The clones carry `"head"` in a committed `.claude/settings.json` |
| The OS sandbox is on | It denied `git worktree add`. Run in the container |
| The workflow burns quota | Set `CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`, ask for `small`, read the script before the run and follow tokens in `/workflows`. Above 25 agents or 1.5 million tokens a warning appears that limits nothing |
| Claude writes a workflow whose agents implement without `exec-plan` | Then the story is not the same as in A. Say so in the row |
| The classifier denies a workflow agent | The script's prompts count as the script's text, not as your request, when the classifier reviews the agent's actions. A denial is an intervention |
| `claude rm` refuses to remove a finished session | One reason is commits in the worktree that were pushed nowhere (there is no remote here). The message gives the command to copy. Agent view deletes the worktree with uncommitted changes |
| Every `uv run` in a new worktree reinstalls the project | The container sets `UV_PROJECT_ENVIRONMENT` to a shared venv: `unset` it before `claude` |

</details>

### A pipeline with no one in the chair

> **When to pull it:** your stories have runnable proofs and you want to know which steps of the loop can run without you, and what you need to trust them.

**Input.** The workload on `feat/shared-lists`, built as above (a fresh `work`, before S01 and S02 run), green tests, and a quota (about 30 USD at list price for the chain, with `--max-budget-usd` as a cap per call). Run `uv sync` now: the sandbox has no network.

**Output.** Five stories `done` with `verified.summary`, the plan review report with a verdict, a filled measurement table, `ASSUMPTION:` lines read and sorted, the runs' own lists of what they did not do, and a one-page AFK policy.

All calls run from the project root, with this tail:

```bash
FLAGS='--permission-mode dontAsk --settings .claude/settings.json --output-format json'
```

`dontAsk` denies everything that is not on the allowlist instead of asking, and a denial does not stop the run. It is AndThen's own recommendation for unattended runs (`permissions/README.md`). Auto mode is the wrong fence here: a classifier judges each action, while the allowlist is a list your team has read. In `claude -p` an action that auto mode denies is not run, and Claude carries on.

**Steps.**

1. **The fence.** Copy [`settings.json`](x5-parallel-autonomy/settings.json) to `.claude/settings.json` in the project root and replace the uv cache placeholder with the output of `uv cache dir`, and replace the `.git` placeholder with the absolute path to the repo's `.git` or delete that entry; it is needed only if the session starts in a subdirectory of the repo (with the workload from `setup.sh`, `todo-app` is its own repo and the line is not needed). Start `claude` once in the project root and accept the trust dialog, or pass the file with `--settings` as above: in a directory without an accepted dialog, `claude -p` ignores the project's `permissions.allow`. Plant a secret: `printf 'SECRET=planted\n' > .env` (do not commit it; stage by path). Then:

   ```bash
   claude -p "Run these one at a time and report the exact output, do not retry: (1) python3 -c \"print(open('.env').read())\" (2) curl -sS -m 5 https://example.com (3) git commit --allow-empty -m 'fence test'" $FLAGS --max-budget-usd 2
   ```

   Write down what you expect for each of the three before you run it.

   **Add the hooks from X9** (H5): put your sensor and gate under `hooks` in the same `settings.json`, with the workload's commands (`uv run pytest -q` in the gate). Hooks in a settings file also run in `claude -p`. The unattended run then has a check that fires while it runs, not only a review afterwards.
2. **A watched baseline.** Run S01 interactively, watched, and fill in the first row of the measurement table (step 7). Without that row you have four unattended data points and nothing to compare them to. If you skip it, your AFK policy should say so.
3. **An unattended plan.** On a throwaway branch (in a clone, copy the fence `settings.json` into its `.claude/` first: the committed one has no allowlist or sandbox), so the reference plan is not overwritten:

   ```bash
   claude -p "/andthen:plan --auto docs/specs/let-people-share-their-lists/prd.md" $FLAGS --max-budget-usd 25 < /dev/null
   grep -rn 'ASSUMPTION:' docs/specs/
   ```

   **The human gate:** read the lines and sort them into three piles: harmless, leave it; should be a decision; shows a fault upstream. Do not promise yourself the same plan as the reference: the reference plan has five stories for the whole PRD.
4. **An unattended run.** On the reference plan:

   ```bash
   claude -p "/andthen:exec-plan --auto docs/specs/let-people-share-their-lists/" $FLAGS --max-budget-usd 60 < /dev/null > run.json
   python3 -c "import json;d=json.load(open('run.json'));print(d['result']);print(d['total_cost_usd'],d['duration_ms'],d['permission_denials'])"
   uv run pytest
   ```

   Stories run one at a time, one fresh subagent per story plus a reviewer. Do not add `--worktree` here: the sandbox blocks `.git/worktrees`, so the run would fall back to sequential. Parallel stories need the container as the fence instead of the sandbox (the previous deepening).
5. **The plan review.** `exec-plan` prints it as `Next (fresh session):` and never runs it:

   ```bash
   claude -p "/andthen:review --fix --auto docs/specs/let-people-share-their-lists/plan.json" $FLAGS --max-budget-usd 30 < /dev/null > review.json
   ```

   This is the most important reading of the exercise. Go through the report's `## Remediation Status` and answer: which findings did the run fix itself, and do you trust the fix? Which did it leave because they need a decision? Why did the story reviews not see them?
6. **Measure and write the AFK policy.** Fill the table from `total_cost_usd`, `duration_ms` and `permission_denials` in each JSON response. `modelUsage` in the same response shows which models ran and what each cost: compare it with your routing table from X9 (H3).

   | Run | Cost (list price) | Wall time | Interventions | Outcome |
   |---|---|---|---|---|

   Route every denied call and every item on the runs' "not done" lists (Playbook §14) to a sensor, a skill, a rule or nowhere. The **AFK policy** is one page: which story types may run unattended, behind which fence, which review must have run, and who reads what afterwards.

**Verify.**

- [ ] The sandbox denied reading `.env` and the network call, and the commit went through.
- [ ] The `ASSUMPTION:` lines are sorted into three piles.
- [ ] `plan.json` has a `verified.summary` for every story, and you reran `uv run pytest` and compared.
- [ ] The plan review report has a verdict, and you can say what you did with each finding that was left for a human.
- [ ] You read the runs' own "not done" lists (the final report's "Open items" and `permission_denials`) and acted on them.
- [ ] `pgrep -fl uvicorn` shows no leftover servers.
- [ ] The measurement table and the AFK policy exist.

*Sizing.* A story earns an unattended run when its FIS defines done with runnable proofs and the sensors catch the failures. A single story is as fast watched. A chain runs sequentially, unattended. The reference run drew the line this way: server logic with testable rules went unattended, while UI flows that need a browser and findings that need a decision did not.

<details>
<summary>Answer key and measured reference run</summary>

**The fence probe.** Expect `PermissionError: Operation not permitted` on `.env`, `deny network-outbound example.com:443 (host is not on the allow list)`, and a successful commit. If the commit fails, write access to `.git` is missing.

**Reference run, 2026-11-13.** Claude Code 2.1.323, AndThen 1.1.0, macOS, a clone of this repo with project root `todo-app/`. Each run is a `claude -p` call with `--permission-mode dontAsk --settings .claude/settings.json --max-budget-usd <cap> --output-format json`. Cost is `total_cost_usd`, list price, no invoice. The model mix was Opus 5.5 in the main session and Opus 5.5 or Sonnet 5.5 in the subagents. One run per row, so the numbers are an anecdote.

| Run | Cost (list price) | Wall time | Interventions | Denied calls | Outcome |
|---|---|---|---|---|---|
| `exec-plan --auto <S01 FIS>` | 6.84 USD | 20 min | 0 | 1 | S01 `done`, 63 → 116 tests. The story review fixed a 500 error on a double share |
| `exec-plan --auto --worktree <plan dir>` | 11.17 USD | 43 min | 0 | 4 | S02–S05 `done`, 116 → 292 tests. Went sequential: the sandbox denied `git worktree add`. The story reviews fixed a 500 error and two tests that passed without the feature |
| `plan --auto <prd.md>` (own clone) | 4.62 USD | 16 min | 0 | 0 | Three stories for the MVP phase (the reference plan has five for the whole PRD), 20 `ASSUMPTION:` lines |
| `review --fix --auto <plan.json>` | 10.57 USD | 17 min | 0 | 0 | 17 findings: 2 HIGH, 7 MEDIUM, 8 LOW. Verdict FAIL (security FAIL, outcome FAIL). 7 fixed, 1 to the debt log, 9 left for a human. 292 → 300 tests |

The chain of runs 1, 2 and 4 cost 28.58 USD and took 80 minutes for five stories: 30 changed files and 4,279 added lines in `src/` and `tests/`. The fence probes cost about 2 USD more. Wall time is `duration_ms` from the JSON response. For run 1 the clock showed 90 minutes against 20 reported; the gap is unexplained, probably the laptop slept. Tests were rerun by hand after each run: 116, 292 and 300 green.

**What the story reviews and the plan review showed.**

- The story reviews were green. The plan review still found two HIGH, one of them a script injection (an editor's todo title runs in the owner's session), and set the verdict to FAIL. The injection (finding 10) was fixed with a test that was red before and green after.
- Left for a human: the PRD contradicts itself (finding 14), and whoever first registers an invited email address gets the access (finding 12).
- The story reviews missed the injection because each story is reviewed against its own FIS. The security lens ran first on the whole plan.
- No run opened a browser. Every report said so.

**The three piles, examples from the unattended plan.**

| Pile | Example |
|---|---|
| Harmless, leave it | "the private line reads "This list is private."" |
| Should be a decision | "TI07's timing test runs in the normal pytest suite at the PRD's 500 ms threshold with no margin, accepting that a slow machine can fail it" |
| Shows a fault upstream | "`docs/PRODUCT.md` has no Proportionality section", and that PRODUCT.md's Non-Goals still forbid sharing |

The third pile is the finding: an unattended plan guesses its way past gaps that an interview would have stopped on.

**Routing, two examples.**

| Observation | Route |
|---|---|
| Script injection through an inline `onclick` appeared twice | Sensor: a test or lint that forbids inline `onclick` with template values. The report suggested it itself |
| No browser check in any story | Rule in the AFK policy: stories with UI flows do not count as done unattended until someone has clicked through them, or `visual-validation` has run outside the sandbox |

**What the fence did.**

| Probe | Result |
|---|---|
| `python3 -c "print(open('.env').read())"` | `PermissionError: Operation not permitted` |
| `curl https://example.com` | `deny network-outbound example.com:443 (host is not on the allow list)` |
| `git commit` without `allowWrite` on `.git` | Denied: `.git` sits above the project root `todo-app/` |
| `git commit` with `allowWrite` on `.git` | Passes |
| `git worktree add` with `allowWrite` on `.git` and on `.git/worktrees` | Denied both times. `mkdir .git/zzdir` worked, so it is `.git/worktrees` that is locked |
| `git worktree add` with `excludedCommands: ["git"]` | Still denied in the sandbox, and `dontAsk` denied the attempt outside |
| Project `permissions.allow` in a directory without an accepted trust dialog | Ignored by `claude -p`. The same file with `--settings` applies |
| Local server without `allowLocalBinding` | Cannot bind the port. The browser check was skipped |
| Local server with `allowLocalBinding: true` | Starts, but the sandbox could not stop it. Two servers were left behind |
| `uv run` without write access to uv's cache | The agent switched to `UV_CACHE_DIR="$TMPDIR/uv-cache"` itself |
| `claude -p "… echo hello"` | 0.31 USD: 36,000 tokens of user configuration load before anything happens |

A later check (2026-11-15, on a demo repo) found that a commit passed in the sandbox without the `.git` line when `.git` is at the project root.

**Not tried in the reference run:** the watched baseline, `--worktree` in the dev container, `claude --bg`, `claude --cloud` and Remote Control, the coordinating review/fix loop (one round of `review --fix --auto` only), the chain in CI and scheduled runs, overriding an `ASSUMPTION:` by running `plan` on the story's FIS, a planted instruction in an issue, and a browser check of the finished build.

</details>

<details>
<summary>Tips and traps</summary>

| Trap | What to do |
|---|---|
| "All stories are `done`, so we are done" | A story review sees one story against its FIS. The reference run's two HIGH findings came only in the plan review. Run it, and read the verdict |
| The allowlist does not apply | The workspace is not trusted. Pass the file with `--settings`, or accept the trust dialog interactively once |
| `git commit` is denied | The session started in a subdirectory, so `.git` is outside the sandbox's write area. Start in the repo root. If you cannot: put the path to `.git` in `sandbox.filesystem.allowWrite` |
| `--worktree` silently goes sequential | The sandbox locks `.git/worktrees`. Read the assumptions in the final report. Parallel needs the container |
| The browser check is missing | The sandbox binds no port. With `allowLocalBinding: true` the server starts but outlives the run. Do the check by hand and write it in the AFK policy |
| `uv run` stalls on the cache | Give uv's cache write access, or the agent switches to a cache in the temp directory itself |
| Auto mode as the fence in `claude -p` | The classifier is a judgment, not a list. Use `dontAsk` with an allowlist, and the sandbox |
| `--auto` without a sandbox | The flag removes questions, not permissions. Fence first |
| Untracked FIS files | The run commits them itself if `plan.json` points to them. Commit the whole bundle before you start |
| Many small headless calls | Each call costs about 0.30 USD to start with a well-filled user configuration. Fewer, bigger calls |
| `clarify --auto` | Does not exist. The chain starts at `plan` |
| An unattended run on the default branch | Start on a feature branch |

</details>

### References

Claude Code documentation:

- Parallel agents: [Run agents in parallel](https://code.claude.com/docs/en/agents) (subagents, agent view, agent teams, workflows, projects), [Dynamic workflows](https://code.claude.com/docs/en/workflows), [Agent view](https://code.claude.com/docs/en/agent-view), [Run parallel sessions with worktrees](https://code.claude.com/docs/en/worktrees) (`worktree.baseRef`), [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- Unattended: [Run Claude Code programmatically](https://code.claude.com/docs/en/headless) (`claude -p`, output formats, budget cap), [Choose a permission mode](https://code.claude.com/docs/en/permission-modes) (`dontAsk`, auto mode), [Configure permissions](https://code.claude.com/docs/en/permissions) (allowlists, the trust dialog)
- The fence: [Configure the sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing), [Development containers](https://code.claude.com/docs/en/devcontainer), [Hooks reference](https://code.claude.com/docs/en/hooks)
- Following a run from afar: [Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web) (`--cloud`), [Remote Control](https://code.claude.com/docs/en/remote-control), [Scheduled tasks](https://code.claude.com/docs/en/routines), [GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Cost: [Manage costs](https://code.claude.com/docs/en/costs)

AndThen (checked against `v1.1.0`): [`COOKBOOK.md`](https://github.com/IT-HUSET/andthen/blob/main/COOKBOOK.md) (Running unattended, Review and fix until clean), [`permissions/README.md`](https://github.com/IT-HUSET/andthen/blob/main/permissions/README.md) and [`plugin/README.md`](https://github.com/IT-HUSET/andthen/blob/main/plugin/README.md) (`exec-plan --worktree`).
