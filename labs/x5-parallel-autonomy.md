# X5 – Parallelize, run unattended

> **Skills:** `exec-plan --worktree`, `exec-plan --auto`, the four role agents from `init`, and AndThen's `permissions/` and `hooks/` examples
> **Pull this when:** after C3 your team chooses to run stories in parallel, or without you watching. This one is your choice: under the course's current recommendation it is pulled, not assigned.

The order matters, and each step earns the next: **sequential** (one fresh subagent per story), then **parallel** (`--worktree`), then **unattended** (`--auto`) inside a sandbox, with a coordinating loop on top.

## Trigger

The entry condition is a fact in your plan, not a feeling:

- **Parallel:** open `<feature-dir>/plan.json`. Are there **two or more pending stories where neither depends on the other** (`dependsOn` does not connect them)? If every story chains behind the previous one, `--worktree` buys nothing: run the plan plainly.
- **Unattended:** you have FIS files you have read, a green C3, and you are willing to read what the run assumed after the fact.

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

### 4. Draw the boundary before you go unattended

An agent's shell commands run as you. Three layers catch what the one above misses: **approval** (a prompt, not a boundary), **rules** (patterns that match a command as written, so a deny on `curl` misses the same request made from a script), and the **OS sandbox** (the only layer that contains a command). Read `permissions/README.md` and `hooks/README.md` in the AndThen repository (github.com/IT-HUSET/andthen, branch `develop`). Then, if your facilitator agrees (this is opt-in and touches your personal settings):

1. **Merge the personal baseline** from `permissions/claude/settings.json` into your `~/.claude/settings.json`. It turns the sandbox on with the network off, hides `.env` files, cloud credentials and browser profiles from commands, makes `git push` ask, and refuses the bypass flag. It also sets `"defaultMode": "auto"`, so merging it changes your permission mode: in auto mode a classifier reviews each action in your place. `permissions/README.md` explains the trade-off, so read it before you merge. On native Windows Claude Code has no sandbox; use WSL2.
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

The loop ends on the hand-off, never on a verdict or a severity count: a `Note` no fix round may apply can hold readiness at *Needs Fixes*, so "until Ready" may never terminate.

## Verify

- [ ] After the sequential run: every story `done` in `plan.json` with a `verified.summary` that quotes a command, its exit status and a result line. The report's `Scope:` line says complete and its `Verification:` line says passed. You ran at least one summary command yourself.
- [ ] After `--worktree`: `git log --graph` shows a `--no-ff` merge per story, `git worktree list` shows no leftover worktree except a preserved failed one, and the full tier ran once on the final tree.
- [ ] A failed story, if any, is contained: its dependents are `skipped`, not built on, and its branch and worktree are preserved.
- [ ] The sandbox refused the `cat` of the fake `.env`, and the hook refused `rm -rf`. You can say which layer did which.
- [ ] You read each `ASSUMPTION:` line from the unattended run, and overturned or accepted each deliberately.
- [ ] The plan-level `review --fix` still ran afterwards. Autonomy does not replace the gate.

## Dial check

*Did the machinery match the parallelism and risk that actually existed?* A multi-story plan with independent stories earns `--worktree`. A single story is `exec-plan <FIS>`, as in F5. A fully sequential plan runs plainly, because there is nothing to parallelize and isolation is overhead. `--auto` earns its place when you can afford to read the assumptions afterwards, not when you cannot afford to be asked. The judgment is not "use the most powerful mode", it is to match the machinery to the work.
