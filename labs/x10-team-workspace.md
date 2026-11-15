# X10 – Team workspace

> **Skills:** `clarify`, `decide`, `plan`, `exec-plan`, `review`, `ship`, `init`, and Claude Code's plugin marketplace, hooks and `AGENTS.md`
> **Pull this when:** your team works across several repos and asks "what do our agents need to know that no single repo carries?", and you have a skill and hooks (from [X9](x9-harness-workshop.md)) that more than one repo needs.

Today the rules, the repo list and your skill live in one person's repo or in one person's `~/.claude`. This exercise gives them a shared home in git: a `team-home` repo with the rules, a catalog of your repos and a plugin marketplace, so that a fresh session finds the right repo, runs the right tests and has the team's skill and hooks without anyone pasting them around. It follows the loop, once, on `team-home` itself: two stories, then a test with and without it.

Claude Code only. A team on Codex or Copilot CLI can keep `AGENTS.md` and the catalog, but the plugin format here is not checked for their hosts.

## Trigger

Pull X10 when you can point to one of these:

- **The same question, repo after repo.** A fresh session asks where the other repo is, how its tests run, or which rule applies, and the answer is in no single repo.
- **A skill or hook that one repo has and the others lack.** You wrote it in X9 (or elsewhere), and a teammate in another repo does not get it.
- **A rule in someone's head.** "Never `git add -A`" or "no personal ID numbers in logs" holds in one repo's `CLAUDE.md` and nowhere else.

Not yet if the team has one repo: that repo's own `AGENTS.md` is the place.

## Input

- **The skill and hooks from X9**, committed in one of your repos. A team that did not do X9 can use these files directly:
  - `x9-harness-workshop/examples/dot-claude/skills/changelog-entry/SKILL.md`
  - `x9-harness-workshop/examples/dot-claude/hooks/guard-git-add-all.py`, `sensor-compile.py` and `gate-tests-green.py`, registered by `x9-harness-workshop/examples/dot-claude/settings.json`
- **Two or three of your repos**, cloned to `~/work/<repo>`, ideally one with a `CLAUDE.md` or `AGENTS.md` and one without.
- **An empty repo `team-home`** that you may create in your organization's GitHub. Local first: `~/team-home`, `git init -b main`, connected to the GitHub repo. It sits outside `~/work` on purpose, so that the "without" arm in step 5 cannot find it.
- **Access for everyone** in the team to the repos and to `team-home`, and an answer from your employer to what may leave the network: code to Anthropic, repos and a marketplace on the organization's GitHub.
- **Claude Code 2.1.302 or later.** Git must reach the private marketplace without a prompt: an SSH key in `ssh-agent`, or `gh auth login` followed by `gh auth setup-git`. Claude Code has no git token of its own. Without an SSH key: `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.
- **No `CLAUDE.md`, `.claude/CLAUDE.md`, `AGENTS.md` or `CLAUDE.local.md` above `~/work` or `~/team-home`**, or the "without" arm gets rules for free (`~/.claude/CLAUDE.md` does not count). Run this for both. Empty output is right:

  ```bash
  p=~/work; while [ "$p" != / ]; do ls "$p"/CLAUDE.md "$p"/.claude/CLAUDE.md "$p"/AGENTS.md "$p"/CLAUDE.local.md 2>/dev/null; p=$(dirname "$p"); done
  ```

## Output

- `team-home` with an `AGENTS.md`, one catalog file per repo and a marketplace with one plugin that carries your skill and hooks.
- That plugin installed in one of your repos, with the skill invoked and a hook seen firing.
- A test, with and without `team-home`, on three questions, with your own answer key written before the first run.
- ADRs for the two choices that are hard to undo.

Reference files for a made-up team (Betala) are in [`x10-team-workspace/`](x10-team-workspace/README.md). Try your own first.

## Steps

Everything happens in `~/team-home`, one phase per fresh session. Start on a feature branch (`git switch -c feat/team-home-v1`), because `exec-plan` asks about a branch on `main`. Run `/andthen:init` once in the empty repo before step 1 and say that more hosts than Claude Code may become relevant. The content then goes in `AGENTS.md` and `CLAUDE.md` becomes a thin import. Keep the Project Document Index in `AGENTS.md` when you edit the rest by hand.

### 1. Clarify

```text
/andthen:clarify "Team workspace v1: one repo, team-home, with rules for all repos, a catalog of the repos and a plugin with the team's skill and hooks"
```

If `docs/PRODUCT.md` is missing, `clarify` asks for the Proportionality facts. Answer with your own numbers, for example: internal, 6 people, 3 repos (growing to a dozen), Claude Code on every machine, no server or MCP service in v1, no Backstage.

You now have `docs/PRODUCT.md` and `prd.md`. Ask yourself: which of your facts would make `clarify` strike something you first wanted?

### 2. Decide

```text
/andthen:decide docs/specs/team-home/
```

Two choices should come out as ADRs, and the spread is split in two rows because a plugin carries only skills, hooks and agents. Point the Index row for ADRs at `decisions/`: `decide` reads the location from the Index.

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
| Spread of rules | `AGENTS.md` in `team-home` for sessions that start there, or a line in each repo's own file. A `CLAUDE.md` in the plugin root is not loaded, so a plugin cannot carry what must hold on every turn | Two-way while it is a couple of repos |
| Catalog format | Markdown with frontmatter, or `catalog-info.yaml` (pays off only with Backstage) | Two-way under a dozen entries |

Renaming: the plugin's name can be moved with a `renames` table in `marketplace.json`. For the marketplace's name the documentation describes no migration: every repo's `.claude/settings.json` and every user's settings must change.

</details>

### 3. Plan

```text
/andthen:plan docs/specs/team-home/
jq -r '.stories[] | [.id, .name, (.dependsOn | join(","))] | @tsv' docs/specs/team-home/plan.json
```

Expect two stories, S01 and S02. Write the proof per story as Key Development Commands (the `fast` tier): `claude plugin validate .` and the session checks below. `team-home` has no test suite, so a proof is a command that either succeeds or does not. Ask yourself: which command proves S02, and what does it print when it fails?

### 4. Execute, review, ship

One story per fresh session:

```text
/andthen:exec-plan docs/specs/team-home/s01-<slug>.md
/andthen:review --fix docs/specs/team-home/plan.json    # after the last story
/andthen:ship docs/specs/team-home/plan.json
```

#### S01 – pointers and catalog

Files: `AGENTS.md` (rules for all repos and an "Other repos" table with path and remote), `CLAUDE.md`, and `catalog/<repo>.md` for each repo. Keep `AGENTS.md` short and hand-written: only what deviates from the default and what the agent cannot read for itself. Agent-generated context files cost more and do not help (Gloaguen et al., [arXiv 2602.11988](https://arxiv.org/abs/2602.11988)). Pick your own catalog fields, but `test` is what step 5 asks about.

`CLAUDE.md` should contain only `@AGENTS.md`. Claude Code reads `AGENTS.md` directly only when there is no `CLAUDE.md`, `.claude/CLAUDE.md` or `CLAUDE.local.md` in the start directory or above it (v2.1.277 or later). With the import the file loads either way, and `/memory` shows it. Imports are followed at most four levels deep. Check after `init` that `CLAUDE.md` is only the import.

A session in `team-home` must read the child repos: start with `claude --add-dir ~/work`, or run `/add-dir ~/work`. `--add-dir` gives file access and loads that directory's `.claude/skills/`, agents and `enabledPlugins`. Its `CLAUDE.md` and `.claude/rules/` come along only with `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`, and its `AGENTS.md` never does. Instructions do not reach child repos by themselves.

**See it: the instruction file that did not load.** Copy `team-home` to a scratch directory and remove `CLAUDE.md` in the copy:

```bash
mkdir -p ~/scratch/th && cp -R ~/team-home ~/scratch/th/ && rm ~/scratch/th/team-home/CLAUDE.md
cd ~/scratch/th/team-home && claude    # run /memory: AGENTS.md is listed
echo '# x' > CLAUDE.md                 # restart, run /memory again
```

`AGENTS.md` is gone from the list once a `CLAUDE.md` exists without the import. A file can drop out of the context without anyone editing it. `@AGENTS.md` is the insurance.

**Proof:** `wc -l AGENTS.md` is under 200, and a fresh interactive session in `team-home` handles "Open orders-api as the catalog says and tell me which branch is checked out". Ask yourself: which line in `AGENTS.md` would you remove first, and how did you know it fails the entry test? The test (Playbook §14): could a sensor, a setting or a document carry the line, or did it happen once?

<details>
<summary>Reference solution</summary>

The reference `team-home` is in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/): [`AGENTS.md`](x10-team-workspace/example-team-home/AGENTS.md), [`CLAUDE.md`](x10-team-workspace/example-team-home/CLAUDE.md) and [`catalog/orders-api.md`](x10-team-workspace/example-team-home/catalog/orders-api.md). Its catalog fields are `owner`, `stack`, `remote`, `path`, `test` and `depends_on`.

Candidates for the line to remove first in a typical `AGENTS.md`: a rule a sensor could carry (a formatting rule a linter already enforces), a rule from one incident whose cause is fixed, and anything the agent can read from the code or the README. `/doctor prompt-audit` (2.1.283) gives candidates, not an answer to the entry test.

</details>

#### S02 – a plugin in a marketplace

Move the skill and hooks out of one repo's `.claude/` into `plugins/<plugin>/` in `team-home`, following the Claude Code documentation's "Convert an existing `.claude/` setup":

1. `plugins/<plugin>/.claude-plugin/plugin.json` with `name` and `description` and no `version` (see the tip below), and the skill directory under `plugins/<plugin>/skills/`. The skill is then called `/<plugin>:<skill>`.
2. The `hooks` object from `.claude/settings.json` goes to `plugins/<plugin>/hooks/hooks.json` (same format) and the scripts to `scripts/`. Change the path from `"$CLAUDE_PROJECT_DIR"/.claude/hooks/x.py` to `"${CLAUDE_PLUGIN_ROOT}/scripts/x.py"`, quotes included, and keep the executable bit.
3. `.claude-plugin/marketplace.json` in the `team-home` root, with `source` set to `./plugins/<plugin>`.
4. Delete the originals in the repo they came from. A standalone skill and a plugin skill with the same name both load, and every matching hook runs.

Try and validate:

```bash
claude --plugin-dir ./plugins/<plugin>           # first: a session with the plugin; /reload-plugins after a change
claude plugin validate ./plugins/<plugin> && claude plugin validate .
claude plugin marketplace add ~/team-home        # local path: the plugin is read in place at every session start
cd ~/work/<child-repo> && claude plugin install <plugin>@<marketplace> --scope project
claude plugin details <plugin>                   # skills and hooks; a hook is marked harness-only
```

After you push, switch to `claude plugin marketplace add <org>/team-home`. In the child repo, `--scope project` declares the marketplace in `.claude/settings.json`, but each colleague runs `claude plugin install ... --scope project` once per clone. New commits reach colleagues with `claude plugin marketplace update <marketplace>` and `claude plugin update <plugin>@<marketplace>`.

A plugin carries skills, agents and hooks, never instructions: a `CLAUDE.md` in the plugin root is not loaded, and `validate` warns about it. `claude plugin eval <plugin>` runs each case with and without the plugin and reports the difference (`claude plugin eval init` writes the cases with you). Every run is a real model call.

**See it: the same rule in two places.** Add the line "Never run `git add -A`" to `AGENTS.md`, run `/context` and note what it costs. Then run `claude plugin details <plugin>`: the hook is listed as `harness-only`, which means it costs no model context. On a clean tree, ask a session to run `git add -A` and let the guard answer (this needs the guard from X9 in your plugin). The line costs every turn and can be ignored. The hook costs nothing until it is needed and cannot be forgotten. Remove the line again afterwards.

**Proof:** the validation, `details`, and a fresh session in the child repo where `/<plugin>:<skill>` answers and a hook fires (`/hooks` lists it). Ask yourself: why is this a hook and not a line in `AGENTS.md`? (Playbook §14: a sensor is deterministic and costs no context until it fires. A line costs every turn.)

<details>
<summary>Reference solution and tips</summary>

The finished shape is the example plugin in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/). Your own plugin carries the skill and hooks from X9 where the example carries a catalog skill and a catalog sensor.

| File | What to know |
|---|---|
| [`marketplace.json`](x10-team-workspace/example-team-home/.claude-plugin/marketplace.json) | `name`, `owner` and `plugins` are required. A user cannot have two marketplaces with the same name, so pick one nobody else picks. The entry's `name` should equal `name` in `plugin.json`, or the plugin has one name in `enabledPlugins` and another as the skill prefix |
| [`plugin.json`](x10-team-workspace/example-team-home/plugins/team-tools/.claude-plugin/plugin.json) | No `version`: then users follow your commits. If you set one and do not bump it, nobody gets the new commits. `validate` warns about a missing `version` and `author`, which is expected |
| [`hooks.json`](x10-team-workspace/example-team-home/plugins/team-tools/hooks/hooks.json) | The hook registered through `${CLAUDE_PLUGIN_ROOT}`. Your own hooks are the guard, the sensor and the stop gate from X9 |
| [`skills/catalog-entry/SKILL.md`](x10-team-workspace/example-team-home/plugins/team-tools/skills/catalog-entry/SKILL.md) | A skill in the plugin, here `/team-tools:catalog-entry <repo>`. Yours is the one from X9 |

Expected output:
- `claude plugin validate` on the plugin and on the marketplace: exit 0, "Validation passed with warnings" (version, author). The first also prints plugin-directory checks (LICENSE, icon) that matter only for a plugin submitted to the directory.
- `claude plugin details`: the skills and hooks. For the example plugin's two skills the always-on cost (skill name and description) is about 144 tokens, measured 2026-11-15.

</details>

### 5. Test it

Ask three questions of a fresh session started in `team-home` (arm A) and of one started in `~/work`, where `team-home` is not (arm B). **Write the answer key first**, in `~/x10/answers.md`, from `team-home` and your repos, before the first run. The right answer is your team's, not anyone else's.

The questions (swap repo and rule for your own): "Where is the repo web-shop on disk and which git remote does it have?", "How are the tests run in orders-api?" and "Which rule applies to personal ID numbers in logs?". The rule in question 3 lives only in `team-home`, so arm B cannot get it right. That is the point.

Run it as one fresh session per question and arm, six in all. Type `/exit` between questions, or the first answer helps the next. Auto memory is off so that no memory follows along:

```bash
cd ~/team-home && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude "Where is the repo web-shop on disk and which git remote does it have?"
cd ~/work && CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 claude "Where is the repo web-shop on disk and which git remote does it have?"
```

Run `/memory` in arm A before the first question: `AGENTS.md` should be listed. Write one row per run in `~/x10/runs.md`: question, arm, answer against the key (right, partly or wrong), and the number of files the agent opened, counted from the tool calls in the transcript. Report correctness per question, not as a sum. Both arms load `~/.claude`, so the difference is `team-home`'s. A child repo's own `CLAUDE.md` loads when the agent reads files under the start directory, so arm B gets it for free. Report that advantage, do not remove it.

Ask yourself: which number would you say aloud in a review, and which is an anecdote? One run per question and arm is an anecdote. Say so.

<details>
<summary>What to expect</summary>

- Arm A answers all three from `AGENTS.md` and the catalog, with no Read outside `catalog/` and no Grep or Glob. If it explored, the pointer was not enough: fix the pointer, not the question.
- Expect arm B to open more files and search more on questions 1 and 2, since it has no catalog to read, and to get question 3 wrong.
- There are no reference numbers for this exercise. It has not been run with a team, so none are claimed.

</details>

## Verify

- [ ] A fresh session in `team-home` answers the three questions right without exploring: no Read outside `catalog/`, no Grep or Glob. `/memory` lists `AGENTS.md`.
- [ ] The plugin is installed in a child repo, its skill is invoked in a fresh session there, and a hook fires when you provoke it (`claude plugin details <plugin>`, `/hooks`). The originals are gone from the repo they came from.
- [ ] `wc -l AGENTS.md CLAUDE.md` is under 200 (imported files count), and five random lines each pass the entry test: which sensor, setting or document could carry it, and did it happen three times? (Playbook §14)
- [ ] `claude plugin validate .` passes, and both ADRs state their door type.
- [ ] `answers.md` and `runs.md` exist with six rows, your guess beside the outcome, correctness reported per question.

<details>
<summary>Tips and traps</summary>

| Trap | What to do |
|---|---|
| The agent generates `AGENTS.md` | It costs more and does not help. `init` writes the frame, you edit the rest by hand |
| `AGENTS.md` does not load | A `CLAUDE.md` or `CLAUDE.local.md` exists in the start directory or above it. `@AGENTS.md` fixes it, or `/config` with Project instructions set to `claude-md-and-agents-md`. `/memory` shows what loaded |
| The skill or hook exists twice, or does not run | The originals are still in `.claude/` in the child repo: delete them, and `/hooks` shows what is registered. If it does not run at all, the script is not executable or `${CLAUDE_PLUGIN_ROOT}` is unquoted |
| The plugin never updates for colleagues | `version` is set and not bumped, or auto-update is off (the default for anything but Anthropic's marketplaces). Omit `version` or bump it, and run `marketplace update` |
| A colleague clones the child repo and the plugin is missing | `enabledPlugins` installs nothing, and `extraKnownMarketplaces` in a repo applies only after the trust dialog. The colleague runs `claude plugin install ... --scope project` |
| Step 5 is not comparable | Two questions in one session, auto memory on, or a `CLAUDE.md` above `~/work`. Follow step 5 as written |
| `--add-dir` is believed to load the child repo's `CLAUDE.md` | It needs the environment variable. A pointer and a fresh session in the child repo is simpler |
| Symlinks in `~/.claude` for the team | They work only personally. Use a marketplace or managed settings |
| The team wants to build Backstage | Wrong cost shape below roughly 30 to 50 engineers (Playbook §13) |

</details>

## Going further

The files for these are already in [`x10-team-workspace/example-team-home/`](x10-team-workspace/example-team-home/) and [`x10-team-workspace/measure/`](x10-team-workspace/measure/).

- **A template repo.** [`templates/golden-path/`](x10-team-workspace/example-team-home/templates/golden-path/): a new repo made from it gets a green `check` with the team's plugin active.
- **The session flow.** [`session-note/SKILL.md`](x10-team-workspace/example-team-home/plugins/team-tools/skills/session-note/SKILL.md) and [`propose-note.sh`](x10-team-workspace/example-team-home/plugins/team-tools/scripts/propose-note.sh): the skill and the script put a note on a branch and open a PR, and a human approves it. A `SessionEnd` hook is not enough: it cannot ask Claude for anything and has 1.5 seconds by default.
- **A larger measurement.** [`measure/`](x10-team-workspace/measure/): twelve `claude -p` runs and a readout (see the [README](x10-team-workspace/README.md#measure) there for prerequisites). Also a check that the catalog matches the repos, `claude plugin eval` cases for the team's plugin, and `describe --model` across several repos. A catalog that is not checked lies after a week.
- **Your case repo.** Add it to the catalog and install the team's plugin there. Treat your friction log as a test of `team-home`: whatever the agent had to ask about is missing from the catalog.

## Sizing check

*Does the team earn a `team-home`?* A team with one repo already has its place in that repo's `AGENTS.md`. With a handful of repos one file of pointers is enough, with no marketplace. At around 400 repos it becomes one file per business area, and at thousands a marketplace ([The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern)). Backstage has the wrong cost shape below roughly 30 to 50 engineers (Playbook §13). Log one line in your sizing log: which level, which facts (people, repos, hosts) justified it, and what it cost in `AGENTS.md` lines.

## References

Claude Code documentation:
- Plugins and marketplaces: [Plugins overview](https://code.claude.com/docs/en/plugins/overview), [Create a plugin](https://code.claude.com/docs/en/plugins/create) (with "Convert an existing `.claude/` setup"), [Create a marketplace](https://code.claude.com/docs/en/plugins/create-marketplace), [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference), [Manage plugins for your organization](https://code.claude.com/docs/en/plugins/org), [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals)
- Instructions: [How Claude remembers your project](https://code.claude.com/docs/en/memory) (`AGENTS.md`, `@` imports, `--add-dir`)
- Permissions and the trust dialog: [Configure permissions](https://code.claude.com/docs/en/permissions)

Also: [The Home Repo Pattern](https://www.aihero.dev/the-home-repo-pattern), [AGENTS.md](https://agents.md), and AndThen's [`plugin/README.md`](https://github.com/IT-HUSET/andthen/blob/main/plugin/README.md).
