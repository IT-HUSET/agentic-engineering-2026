# X10 – Team workspace

**What you do:** each of you first writes a personal home, one file of pointers to your own repos that every session under `~/work` loads. Then you give the team's shared know-how one home in git: a `team-home` repo with the rules that apply to every repo, a catalog of your repos, and a plugin marketplace that carries the team's skills and hooks. The lines your personal homes share are its first rules. You build `team-home` with the loop, in two stories, and then test a fresh session with `team-home`, with a personal home and with neither.

**Why it matters:** today the rules, the repo list and your skill live in one person's repo or one person's `~/.claude`. A fresh session cannot find the other repo, runs the wrong tests and misses the team's hooks, so someone pastes them around.

**What you have at the end:** a personal home each, `team-home` with an `AGENTS.md`, a catalog file per repo and a plugin installed in one of your repos, two ADRs for the choices that are hard to undo, and a measured answer to "what does each one add?" from three questions asked in three arms.

> **Skills:** `clarify`, `decide`, `plan`, `exec-plan`, `review`, `ship`, `init`, and Claude Code's plugin marketplace, hooks and `AGENTS.md` · Builds on the skill and hooks from [X9](x9-harness-workshop.md). Claude Code only: a team on Codex or Copilot CLI can keep `AGENTS.md` and the catalog, but the plugin format here is not checked for their hosts.

## When to pull it

Pull X10 when one of these is true for your team:

- **The same question, repo after repo.** A fresh session asks where the other repo is, how its tests run, or which rule applies, and the answer is in no single repo.
- **A skill or hook that one repo has and the others lack.** You wrote it in X9 (or elsewhere), and a teammate in another repo does not get it.
- **A rule in someone's head.** "Never `git add -A`" or "no personal ID numbers in logs" holds in one repo's `CLAUDE.md` and nowhere else.

**Skip it** if the team has one repo. That repo's own `AGENTS.md` is the place.

## Input

- **The skill and hooks from X9**, committed in one of your repos. A team that did not do X9 can use these files directly:
  - `x9-harness-workshop/examples/dot-claude/skills/changelog-entry/SKILL.md`
  - `x9-harness-workshop/examples/dot-claude/hooks/guard-git-add-all.py`, `sensor-compile.py` and `gate-tests-green.py`, registered by `x9-harness-workshop/examples/dot-claude/settings.json`
- **Two or three of your repos**, cloned to `~/work/<repo>`, ideally one with a `CLAUDE.md` or `AGENTS.md` and one without.
- **A repo of your own for your personal home**, one per person: `~/my-home`, `git init -b main`, local or on your own GitHub account. It holds your habits, not the team's, so it does not belong in the organization's GitHub.
- **An empty repo `team-home`** that you may create in your organization's GitHub. Local first: `~/team-home`, `git init -b main`, connected to the GitHub repo. It sits outside `~/work` on purpose, so that arms B and C in step 5 cannot find it.
- **Access for everyone** in the team to the repos and to `team-home`, and an answer from your employer to what may leave the network: code to Anthropic, repos and a marketplace on the organization's GitHub.
- **Claude Code 2.1.302 or later.** Git must reach the private marketplace without a prompt: an SSH key in `ssh-agent`, or `gh auth login` followed by `gh auth setup-git`. Claude Code has no git token of its own. Without an SSH key: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.
- **No `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md` or `CLAUDE.local.md` in or above `~/work` or `~/team-home`**, or arm B in step 5 gets rules for free. Your own `~/.claude/CLAUDE.md` loads in every arm and does not count, so the loop skips `.claude/CLAUDE.md` in `$HOME`. Run it before step 0, when empty output is right. Later it finds only your own files: `~/work/CLAUDE.md` after step 0, and `~/team-home/CLAUDE.md` and `AGENTS.md` after S01:

  ```bash
  for p in ~/work ~/team-home; do
    while [ "$p" != / ]; do
      ls "$p"/CLAUDE.md "$p"/AGENTS.md "$p"/CLAUDE.local.md 2>/dev/null
      [ "$p" = "$HOME" ] || ls "$p"/.claude/CLAUDE.md 2>/dev/null
      p=$(dirname "$p")
    done
  done
  ```

## Output

- A personal home per person: `~/my-home/REPOS.md`, linked as `~/work/CLAUDE.md`.
- `team-home` with an `AGENTS.md`, one catalog file per repo and a marketplace with one plugin that carries your skill and hooks.
- That plugin installed in one of your repos, with the skill invoked and a hook seen firing.
- A test on three questions in three arms (`team-home`, a personal home, neither), with your own answer key written before the first run.
- ADRs for the two choices that are hard to undo.

Reference files for a made-up team (Betala) are in [`x10-team-workspace/`](x10-team-workspace/README.md). Try your own first.

## Steps

Step 0 happens in `~/my-home`, each of you on your own. Steps 1–4 happen in `~/team-home`, one phase per fresh session, and step 5 starts sessions in three places. Start on a feature branch (`git switch -c feat/team-home-v1`), because `exec-plan` asks about a branch on `main`. Run `/andthen:init` once in the empty repo before step 1 and say that more hosts than Claude Code may become relevant. The content then goes in `AGENTS.md` and `CLAUDE.md` becomes a thin import. Keep the Project Document Index in `AGENTS.md` when you edit the rest by hand.

### 0. Your personal home

Each of you, in parallel, before the team starts on `team-home`. No loop: it is one file of pointers, and a fresh session is the proof.

1. **Let the agent do the groundwork.** Start a session in `~/my-home` with `claude --add-dir ~/work` and ask: "List the git repos under ~/work with their path, their `origin` remote and one line on what each is, taken from its README. Draft a table in REPOS.md."
2. **Decide every line yourself.** Keep the rows for repos you work in. Add only personal rules you have typed into a session more than once, for example "answer in Swedish" or "never push without asking". Cut what the agent can read from the repo itself.
3. **Link it** with `ln -s ~/my-home/REPOS.md ~/work/CLAUDE.md`. Claude Code loads every `CLAUDE.md` in the start directory and the directories above it, so a session started in any repo under `~/work` gets your home. Commit `REPOS.md` in `~/my-home`, and edit it there: Claude's Edit and Write tools refuse to write through a symlink. The documentation does not say whether a `CLAUDE.md` symlink pointing outside the start directory asks for approval like an external import. If Claude Code asks, approve it.

**See it: the `AGENTS.md` that went missing.** Start a fresh session in a child repo that has an `AGENTS.md` and no `CLAUDE.md`, and run `/context all`. Under **Memory files** your home is listed, but the repo's `AGENTS.md` is not. Claude Code reads `AGENTS.md` only when there is no `CLAUDE.md` in the start directory or above it, and your link is one. A `CLAUDE.md` containing only `@AGENTS.md` in that repo brings it back, and S01 shows why every repo wants that line. Skip this if none of your repos has only an `AGENTS.md`.

**Proof:** in a fresh session in one child repo, `/context all` lists `~/work/CLAUDE.md` under **Memory files**, and "Where is the repo <another of your repos> on disk and which git remote does it have?" is answered with no Read and no Bash search.

**Bring it to the table.** Put your homes side by side. A line that two or more of you have is a candidate for the rules in `team-home`'s `AGENTS.md`, so bring it to step 1. A line only you have stays in your home. Ask yourself: which of your lines would a colleague disagree with?

<details>
<summary>Why not just <code>~/.claude/CLAUDE.md</code>?</summary>

`~/.claude/CLAUDE.md` loads in every session on the machine, also in repos outside `~/work`, and it is in git only if you keep `~/.claude` in git. With two repos and one machine it is enough, and then step 0 is a few lines there. A home repo pays off with a repo index you keep up to date and more than one machine to share it with.

</details>

### 1. Clarify

```text
/andthen:clarify "Team workspace v1: one repo, team-home, with rules for all repos, a catalog of the repos and a plugin with the team's skill and hooks"
```

If `docs/PRODUCT.md` is missing, `clarify` asks for the Proportionality facts. Answer with your own numbers, for example: internal, 6 people, 3 repos (growing to a dozen), Claude Code on every machine, no server or MCP service in v1, no Backstage. Bring the lines your personal homes share (step 0) to the interview: they are the first candidates for the rules.

`clarify` writes the PRD to a directory under `docs/specs/` named after the first six words of the description (here `docs/specs/team-workspace-v1-one-repo-team/`) and prints the next command with that path. Use that directory as `<spec-dir>` below. You now have `docs/PRODUCT.md` and `prd.md`. Ask yourself: which of your facts would make `clarify` strike something you first wanted?

### 2. Decide

```text
/andthen:decide <spec-dir>
```

Two choices should come out as ADRs: the spread, in two rows because a plugin cannot carry the rules (its root `CLAUDE.md` is not loaded), and the catalog format. Point the Index row for ADRs at `decisions/`: `decide` reads the location from the Index. From AndThen 1.2.0, `decide` also asks an `oracle` subagent for a second opinion on the one-way doors, and an objection it kept the decision over goes under *Consequences*.

| Choice | Options to weigh |
|---|---|
| How skills and hooks spread | A marketplace in `team-home`, copying through a template, or a submodule |
| How rules spread | `AGENTS.md` in `team-home` for sessions that start there, or a line in each repo's own file |
| Catalog format | Markdown with frontmatter, or `catalog-info.yaml` |

Write the door type on each ADR. Ask yourself: what does it cost to rename the plugin, and what does it cost to rename the marketplace?

<details>
<summary>Reference answers</summary>

| Choice | Options, briefly | Door |
|---|---|---|
| Spread of skills and hooks | A marketplace in `team-home` (a private repo works with the user's git credentials, and auto-update is off by default), copying through a template or a submodule (drifts per repo). Managed settings register a marketplace and install its plugin on every machine, but the marketplace is still needed | One-way once ten repos have `team-tools@betala-team` in their settings. The marketplace name is part of every such key, so name it right the first time |
| Spread of rules | `AGENTS.md` in `team-home` for sessions that start there, or a line in each repo's own file. A `CLAUDE.md` in the plugin root is not loaded, so the rules travel by `@` import or managed settings (see S02 for why not a `SessionStart` hook) | Two-way while it is a couple of repos |
| Catalog format | Markdown with frontmatter, or `catalog-info.yaml` (pays off only with Backstage) | Two-way under a dozen entries |

Renaming: the plugin's name can be moved with a `renames` table in `marketplace.json`. For the marketplace's name the documentation describes no migration: every repo's `.claude/settings.json` and every user's settings must change.

</details>

### 3. Plan

```text
/andthen:plan <spec-dir>
jq -r '.stories[] | [.id, .name, (.dependsOn | join(","))] | @tsv' <spec-dir>/plan.json
```

Expect two stories, S01 and S02. Write the proof per story as Key Development Commands (the `fast` tier): `claude plugin validate .` and the session checks below. `team-home` has no test suite, so a proof is a command that either succeeds or does not. Ask yourself: which command proves S02, and what does it print when it fails?

### 4. Execute, review, ship

One story per fresh session:

```text
/andthen:exec-plan <spec-dir>/s01-<slug>.md
/andthen:review --fix <spec-dir>/plan.json    # after the last story
/andthen:ship <spec-dir>/plan.json
```

#### S01 – pointers and catalog

Files: `AGENTS.md` (rules for all repos and an "Other repos" table with path and remote), `CLAUDE.md`, and `catalog/<repo>.md` for each repo. Keep `AGENTS.md` short, and decide every line yourself. Let the agent do the groundwork: reading each repo's remote, README and test command, and drafting the table and the catalog files. You choose what stays: only what deviates from the default and what the agent cannot read for itself. Context files, hand-written or generated, do not generally raise solve rates and add over 20 % inference cost, but they help with non-standard practices (Gloaguen et al., [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)). Pick your own catalog fields, but `test` is what step 5 asks about.

`CLAUDE.md` should contain only `@AGENTS.md`. Claude Code reads `AGENTS.md` directly only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the start directory or above it (v2.1.277 or later). With the import the file loads either way, and `/memory` shows it. Imports are followed at most four levels deep. Check after `init` that `CLAUDE.md` is only the import.

A session in `team-home` must read the child repos: start with `claude --add-dir ~/work`, or run `/add-dir ~/work`. `--add-dir` gives file access and loads that directory's `.claude/skills/`, agents and `enabledPlugins`. Its `CLAUDE.md` and `.claude/rules/` come along only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`, and its `AGENTS.md` never does. Instructions do not reach child repos by themselves.

**See it: the instruction file that did not load.** Copy `team-home` to a scratch directory and remove `CLAUDE.md` in the copy:

```bash
mkdir -p ~/scratch/th && cp -R ~/team-home ~/scratch/th/ && rm ~/scratch/th/team-home/CLAUDE.md
cd ~/scratch/th/team-home && claude    # run /memory: AGENTS.md is listed
echo '# x' > CLAUDE.md                 # restart, run /memory again
```

`AGENTS.md` is gone from the list once a `CLAUDE.md` exists without the import. A file can drop out of the context without anyone editing it. `@AGENTS.md` is the insurance.

**Proof**, run in `team-home` (empty output is a pass; adapt the fields and the path pattern to your own files):

```bash
[ "$(wc -l < AGENTS.md)" -lt 200 ] || echo "AGENTS.md is 200 lines or more"
for f in catalog/*.md; do for k in owner stack remote path test; do grep -Eq "^$k:[[:space:]]*[^[:space:]]" "$f" || echo "$f: $k missing"; done; done
grep -o '`~/[^`]*`' AGENTS.md | tr -d '`' | while read -r p; do [ -d "${p/#\~/$HOME}" ] || echo "missing path: $p"; done
```

The session check is manual and belongs to step 5: a fresh interactive session in `team-home` that handles "Open orders-api as the catalog says and tell me which branch is checked out". Ask yourself: which line in `AGENTS.md` would you remove first, and how did you know it fails the entry test? The test (Playbook §14, "Where a learning goes"): a line stays only when no sensor, workflow step, skill or doc could carry it, and it came up three times (capture on the third repetition).

<details>
<summary>Reference solution</summary>

The reference `team-home` is in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/): [`AGENTS.md`](x10-team-workspace/example-team-home/AGENTS.md), [`CLAUDE.md`](x10-team-workspace/example-team-home/CLAUDE.md) and [`catalog/orders-api.md`](x10-team-workspace/example-team-home/catalog/orders-api.md). Its catalog fields are `owner`, `stack`, `remote`, `path`, `test` and `depends_on`.

Candidates for the line to remove first in a typical `AGENTS.md`: a rule a sensor could carry (a formatting rule a linter already enforces), a rule from one incident whose cause is fixed, and anything the agent can read from the code or the README. `/doctor prompt-audit` (2.1.283) gives candidates, not an answer to the entry test.

</details>

#### S02 – a plugin in a marketplace

Move the skill and hooks out of one repo's `.claude/` into `plugins/<plugin>/` in `team-home`, following the Claude Code documentation's "Convert an existing `.claude/` setup":

1. `plugins/<plugin>/.claude-plugin/plugin.json` with `name` and `description` and no `version` (see the tip below), and the skill directory under `plugins/<plugin>/skills/`. The skill is then called `/<plugin>:<skill>`.
2. The `hooks` object from `.claude/settings.json` goes to `plugins/<plugin>/hooks/hooks.json` (same format) and the scripts to `scripts/`. Change the path from `"$CLAUDE_PROJECT_DIR"/.claude/hooks/x.py` to `"${CLAUDE_PLUGIN_ROOT}/scripts/x.py"`, quotes included, and keep the executable bit. The stop gate from X9 reads its test command from the environment variable `TEAM_TEST_CMD` and does nothing when it is unset, so the plugin can reach repos in any language. A repo that wants the gate sets it in the `env` block of its own `.claude/settings.json` (for example `"env": {"TEAM_TEST_CMD": "make test"}`), which applies after the trust dialog.
3. `.claude-plugin/marketplace.json` in the `team-home` root, with `source` set to `./plugins/<plugin>`.
4. Delete the originals in the repo they came from. A standalone skill and a plugin skill with the same name both load, and every matching hook runs.

Try and validate:

```bash
claude --plugin-dir ./plugins/<plugin>           # first: a session with the plugin; /reload-plugins after a change
claude plugin validate ./plugins/<plugin> && claude plugin validate .
claude plugin marketplace add ~/team-home        # local path, in your user settings: the plugin is read in place at every session start
cd ~/work/<child-repo> && claude plugin install <plugin>@<marketplace> --scope project   # writes only enabledPlugins
claude plugin details <plugin>                   # skills and hooks; a hook is marked harness-only
```

After you push, move the child repo to the GitHub source. `claude plugin marketplace remove <marketplace>` clears the local path, and also uninstalls the plugin and removes both entries from the settings files. Then, in the child repo:

```bash
claude plugin marketplace add <org>/team-home --scope project            # writes extraKnownMarketplaces to .claude/settings.json
claude plugin install <plugin>@<marketplace> --scope project             # writes enabledPlugins
```

Commit `.claude/settings.json`. In a colleague's clone the marketplace applies after the trust dialog, and each colleague runs `claude plugin install ... --scope project` once per clone. New commits reach colleagues with `claude plugin marketplace update <marketplace>` and `claude plugin update <plugin>@<marketplace>`.

A `CLAUDE.md` in the plugin root is not loaded, and `validate` warns about it. Standing text could reach every session indirectly, through a `SessionStart` hook (its output is capped at 10 000 characters) or an output style with `force-for-plugin: true` (it overrides the user's own style). This exercise uses neither: the rules stay in `AGENTS.md`, a file people can read and review, pulled in by `@` import or managed settings. `claude plugin eval <plugin>` runs each case with and without the plugin and reports the difference (`claude plugin eval init` writes the cases with you). Every run is a real model call.

**See it: the same rule in two places.** Add the line "Never run `git add -A`" to `AGENTS.md`, run `/context` and note what it costs. Then run `claude plugin details <plugin>`: the hook is listed as `harness-only`, which means it costs no model context. On a clean tree, ask a session to run `git add -A` and let the guard answer (this needs the guard from X9 in your plugin). The line is always-on context, billed on every turn, and the agent can ignore it. The hook is deterministic: it fires without anyone remembering to run it, and costs no context until it does. Remove the line again afterwards.

**Proof:** the validation, `details`, and a fresh session in the child repo where `/<plugin>:<skill>` answers and a hook fires (`/hooks` lists it). Ask yourself: why is this a hook and not a line in `AGENTS.md`? (Playbook §14: a sensor is deterministic and fires without anyone remembering to run it. A line in `AGENTS.md` is always-on context, billed on every turn.)

<details>
<summary>Reference solution and tips</summary>

The finished shape is the example plugin in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/). Your own plugin carries the skill and hooks from X9 where the example carries a catalog skill and a catalog sensor.

| File | What to know |
|---|---|
| [`marketplace.json`](x10-team-workspace/example-team-home/.claude-plugin/marketplace.json) | `name`, `owner` and `plugins` are required. A user cannot have two marketplaces with the same name, so pick one nobody else picks. The entry's `name` should equal `name` in `plugin.json`, or the plugin has one name in `enabledPlugins` and another as the skill prefix |
| [`plugin.json`](x10-team-workspace/example-team-home/plugins/team-tools/.claude-plugin/plugin.json) | No `version`: then users follow your commits. If you set one and do not bump it, nobody gets the new commits. `validate` warns about a missing `version` and `author`, which is expected |
| [`hooks.json`](x10-team-workspace/example-team-home/plugins/team-tools/hooks/hooks.json) | The hook registered through `${CLAUDE_PLUGIN_ROOT}`. Your own hooks are the guard, the sensor and the stop gate from X9 (the gate needs `TEAM_TEST_CMD`) |
| [`skills/catalog-entry/SKILL.md`](x10-team-workspace/example-team-home/plugins/team-tools/skills/catalog-entry/SKILL.md) | A skill in the plugin, here `/team-tools:catalog-entry <repo>`. Yours is the one from X9 |

Expected output:
- `claude plugin validate` on the plugin and on the marketplace: exit 0, "Validation passed with warnings" (version, author). The first also prints plugin-directory checks (LICENSE, icon) that matter only for a plugin submitted to the directory.
- `claude plugin details`: the skills and hooks. For the example plugin's two skills the always-on cost (skill name and description) is about 144 tokens, measured 2026-11-15.

</details>

### 5. Test it

Ask three questions in three arms: a fresh session started in `team-home` (arm A), one started in `~/work` with neither `team-home` nor a personal home (arm B), and one started in `~/work` with your personal home (arm C). One of you runs all three arms, with their own home. **Write the answer key first**, in `~/x10/answers.md`, from `team-home` and your repos, before the first run. The right answer is your team's, not anyone else's.

The questions (swap repo and rule for your own): "Where is the repo web-shop on disk and which git remote does it have?", "How are the tests run in orders-api?" and "Which rule applies to personal ID numbers in logs?". For question 3, pick a rule that is in `team-home` and nowhere else: not in the runner's personal home, and not in any child repo's files, where arms B and C would read or grep it. Then arms B and C should not get it right, and that is the point.

Run it as one fresh session per question and arm, nine in all. Type `/exit` between questions, or the first answer helps the next. Auto memory is off so that no memory follows along. Arm B needs your home out of the way: remove the link before its three runs, and put it back for arm C. The `-L` test makes sure only a link is removed:

```bash
cd ~/team-home && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude "Where is the repo web-shop on disk and which git remote does it have?"    # arm A
[ -L ~/work/CLAUDE.md ] && rm ~/work/CLAUDE.md                                                                                         # before arm B
cd ~/work && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude "Where is the repo web-shop on disk and which git remote does it have?"         # arm B
ln -s ~/my-home/REPOS.md ~/work/CLAUDE.md                                                                                              # before arm C
cd ~/work && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude "Where is the repo web-shop on disk and which git remote does it have?"         # arm C
```

Check what loaded before the first question in each arm. In arm A, `/memory` lists `AGENTS.md`. Before arm B, `ls -l ~/work/CLAUDE.md` must report no such file. In arm C, `/context all` lists `~/work/CLAUDE.md` under **Memory files**. Do not check arm B with `/memory`: it lists a project `CLAUDE.md` even when the file does not exist, and selecting that entry creates a real file that spoils arm B and makes the `ln -s` before arm C fail. Write one row per run in `~/x10/runs.md`: question, arm, answer against the key (right, partly or wrong), and the number of exploration calls: every Read, and every Bash `find`, `grep`, `rg`, `ls` or `cat`, outside `catalog/`, counted from the tool calls in the transcript. On macOS, Linux and WSL Claude has no Grep or Glob tool by default and searches through Bash, so those calls count. Report correctness per question, not as a sum. All three arms load `~/.claude`, so the differences are `team-home`'s and the personal home's. A child repo's own `CLAUDE.md` loads when the agent reads files under the start directory, so arms B and C get it for free. A child repo's lone `AGENTS.md` loads only in arm B, and only when the agent opens a file there with Read. In arm C your link counts as a `CLAUDE.md` above it (step 0). Report both effects, do not remove them.

Ask yourself: which number would you say aloud in a review, and which is an anecdote? One run per question and arm is an anecdote. Say so.

<details>
<summary>What to expect</summary>

- Arm A answers all three from `AGENTS.md` and the catalog, with no exploration call outside `catalog/` (no Read, no Bash `find`, `grep`, `rg`, `ls` or `cat`). If it explored, the pointer was not enough: fix the pointer, not the question.
- Expect arm B to open more files and search more on questions 1 and 2, since it has no catalog to read, and to get question 3 wrong.
- Expect arm C to answer question 1 like arm A, from your home if it lists that repo, and to open repo files on question 2 unless your home holds test commands. Question 3 is where A and C part: that difference is what the team repo adds over the personal homes.
- There are no reference numbers for this exercise. It has not been run with a team, so none are claimed.

</details>

## Verify

- [ ] Each of you has a personal home linked as `~/work/CLAUDE.md`, and a fresh session in a child repo answers where another repo is with no Read and no Bash search.
- [ ] A fresh session in `team-home` answers the three questions right without exploring: no Read and no Bash `find`, `grep`, `rg`, `ls` or `cat` outside `catalog/`. `/memory` lists `AGENTS.md`.
- [ ] The plugin is installed in a child repo, its skill is invoked in a fresh session there, and a hook fires when you provoke it (`claude plugin details <plugin>`, `/hooks`). The originals are gone from the repo they came from.
- [ ] `wc -l AGENTS.md CLAUDE.md` is under 200 (imported files count), and five random lines each pass the entry test (Playbook §14): no sensor, workflow step, skill or doc could carry the line, and it came up three times
- [ ] `claude plugin validate .` passes, and both ADRs state their door type.
- [ ] `answers.md` and `runs.md` exist with nine rows, your guess beside the outcome, correctness reported per question.

<details>
<summary>Tips and traps</summary>

| Trap | What to do |
|---|---|
| The agent writes `AGENTS.md` on its own | Context files, generated or not, add over 20 % cost without generally raising solve rates (Gloaguen et al.). Let `init` write the frame and the agent gather facts and draft, then decide every line yourself and cut what the agent can read from the code |
| A child repo's `AGENTS.md` stops loading after step 0 | Your `~/work/CLAUDE.md` counts as a `CLAUDE.md` above the repo. Add a `CLAUDE.md` containing only `@AGENTS.md` in that repo |
| `AGENTS.md` does not load | A `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` exists in the start directory or above it. `@AGENTS.md` fixes it, or `/config` with Project instructions set to `claude-md-and-agents-md`. `/memory` shows what loaded |
| The skill or hook exists twice, or does not run | The originals are still in `.claude/` in the child repo: delete them, and `/hooks` shows what is registered. If it does not run at all, the script is not executable or `${CLAUDE_PLUGIN_ROOT}` is unquoted |
| The plugin never updates for colleagues | `version` is set and not bumped, or auto-update is off (the default for anything but Anthropic's marketplaces). Omit `version` or bump it, and run `marketplace update` |
| A colleague clones the child repo and the plugin is missing | `enabledPlugins` installs nothing, and `extraKnownMarketplaces` in a repo applies only after the trust dialog. The colleague runs `claude plugin install ... --scope project` |
| Step 5 is not comparable | Two questions in one session, auto memory on, your link still in place in arm B, or a `CLAUDE.md` above `~/work`. Follow step 5 as written |
| `--add-dir` is believed to load the child repo's `CLAUDE.md` | It needs the environment variable. A pointer and a fresh session in the child repo is simpler |
| Symlinks in `~/.claude` for the team | They work only personally. Use a marketplace or managed settings |
| The team wants to build Backstage | The course's own estimate: wrong cost shape below roughly 30 to 50 engineers. A markdown catalog does the job until then |

</details>

## Going further

The files for these are already in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/) and [`x10-team-workspace/measure/`](x10-team-workspace/measure/).

- **A template repo.** [`templates/golden-path/`](x10-team-workspace/example-team-home/templates/golden-path/): a new repo made from it gets a green `check` with the team's plugin active.
- **The session flow.** [`session-note/SKILL.md`](x10-team-workspace/example-team-home/plugins/team-tools/skills/session-note/SKILL.md) and [`propose-note.sh`](x10-team-workspace/example-team-home/plugins/team-tools/scripts/propose-note.sh): the skill and the script put a note on a branch and open a PR, and a human approves it. The script finds `team-home` through `TEAM_HOME` and falls back to `~/team-home`. A `SessionEnd` hook is not enough: it cannot ask Claude for anything and has 1.5 seconds by default.
- **A larger measurement.** [`measure/`](x10-team-workspace/measure/): twelve `claude -p` runs in arms A and B, without the personal home, and a readout (see the [README](x10-team-workspace/README.md#measure) there for prerequisites). Also a check that the catalog matches the repos, `claude plugin eval` cases for the team's plugin, and `describe --model` across several repos. A catalog that is not checked lies after a week.
- **Your case repo.** Add it to the catalog and install the team's plugin there. Treat your friction log as a test of `team-home`: whatever the agent had to ask about is missing from the catalog.

### Ideas for your own team-home

None of these is part of the exercise. Pick one your team misses and build its smallest version first.

- **More team skills.** A skill for a prompt pasted three times, added to the plugin you have. Remove skills nobody calls (`claude plugin details` shows the cost).
- **A knowledge base ("LLM wiki").** Human-edited pages in `wiki/` with one pointer line in `AGENTS.md`, new pages by PR through the session flow. Context files that load every session rarely raise solve rates (Gloaguen et al., [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)), so keep pages for what differs from the defaults.
- **Onboarding.** A skill such as `/team-tools:onboard` that points a new colleague at the catalog and the rules. Step 5's three questions double as the test.
- **How the team is doing.** Numbers you already have (PR lead time from `gh`, review findings per plan, friction-log length), read at the retro. The playbook (§15) says to measure DORA outcomes and never "% of code AI-generated" or self-reported productivity. A short DevEx question at the retro (feedback loops, cognitive load, flow) is this course's own advice, not the playbook's.

## Sizing check

*Does the team earn a `team-home`?* A team with one repo already has its place in that repo's `AGENTS.md`. One person across a handful of repos has it in a personal home (step 0), and `team-home` starts paying off with a rule the whole team holds. Arm C against arm A in step 5 shows what it added. Pointers and distribution grow on different triggers, so there are two ladders:

| | Pointers (where things are) | Distribution (skills and hooks) |
|---|---|---|
| One repo | Its own `AGENTS.md` | Files in its `.claude/` |
| One person, a handful of repos | A personal home (step 0) | Files in `~/.claude/` |
| A team, a handful of repos | One file of pointers in `team-home` | A plugin in a marketplace from the second repo that needs the same setup ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)) |
| Around 400 repos | One file per business area ([The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern)) | Managed settings, when the plugin must reach every machine |

Backstage has the wrong cost shape below roughly 30 to 50 engineers (this course's estimate, not a measured figure). Log one line in your sizing log: which level on each ladder, which facts (people, repos, hosts) justified it, and what it cost in `AGENTS.md` lines.

## References

Claude Code documentation:
- Plugins and marketplaces: [Plugins overview](https://code.claude.com/docs/en/plugins/overview), [Create a plugin](https://code.claude.com/docs/en/plugins/create) (with "Convert an existing `.claude/` setup"), [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace), [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference), [Manage plugins for your organization](https://code.claude.com/docs/en/plugins/org), [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals)
- Instructions: [How Claude remembers your project](https://code.claude.com/docs/en/memory) (`AGENTS.md`, `@` imports, `--add-dir`)
- Permissions and the trust dialog: [Configure permissions](https://code.claude.com/docs/en/permissions)

Also: [The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern) and AndThen's [`plugin/README.md`](https://github.com/IT-HUSET/andthen/blob/main/plugin/README.md).
