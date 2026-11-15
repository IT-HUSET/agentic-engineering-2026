# X9 – Harness workshop

**What you do:** build the parts of your agent harness yourselves: a subagent, a skill and three hooks, after measuring what a session loads before you type. Every step has the same shape, **guess, run, keep**: write your guess down, run the step, keep what held up. The measured answer sits in a collapsed section below each step. Open it after you have run the step, not before.

**Why it matters:** you use Claude Code and AndThen every day, but the harness decides what the agent sees, who does the work and what is enforced. Building the parts yourselves is how you find out what you cannot predict about it.

**What you have at the end:** three things your team wants to remove or move, your own subagent and skill, and three hooks (a sensor, a guard and a gate), all committed. H6–H7 continue with a pull request against your team's harness.

> **Skills:** subagent definitions, skills, hooks, `CLAUDE.md` and settings in Claude Code. AndThen is the object of study: its role agents, rules template, `hooks/` and skill guidelines · Claude Code only.

## When to pull it

Pull X9 when one of these is true for your team:

- **Cost you cannot see.** You do not know what a fresh session in your repo loads before you type, or which skills nobody calls.
- **Delegation by habit.** You hand work to subagents but have never written one, and you could not say which model runs it.
- **The same prompt a third time.** Someone on the team keeps pasting the same instructions or workflow.
- **A rule the agent breaks anyway.** `CLAUDE.md` says it, and it still happens.

**Skip it** if Claude Code or AndThen is still new to you. The foundation is the better place to start.

Claude Code's own rule of thumb for what to build ([Extend Claude Code](https://code.claude.com/docs/en/features-overview)) is also the sizing check for this exercise:

| When this happens | Add |
|---|---|
| Claude gets a convention or command wrong twice | A line in `CLAUDE.md` |
| You type the same prompt, or paste the same workflow, for the third time | A skill |
| A side task fills the conversation with output you do not read again | A subagent |
| Something must happen every time, without anyone asking | A hook |
| A second repo needs the same set | A plugin |

## Input

- One of your team's own repos and a branch to work on, with its rules, skills and hooks as they are. **Fallback:** the demo repo (below).
- Claude Code **2.1.302 or later** on every machine (`claude --version`). That version has `/skill-doctor`, `/doctor prompt-audit`, `/tasks` with the model per subagent, and fork mode.
- AndThen installed, and its four role agents installed with `/andthen:init` (needed for H3).
- `/skill-doctor` answering. It needs the session to fetch feature flags, and a session with `DISABLE_TELEMETRY` set does not.

**The demo repo.** A small Python repo with the examples installed in `.claude/`. Build it outside every directory that has a `CLAUDE.md` above it, because Claude Code reads every `CLAUDE.md` up the tree (this repo has one). `/tmp` works:

```bash
labs/x9-harness-workshop/examples/demo-repo.sh /tmp/x9/demo
```

**Files in [`x9-harness-workshop/`](x9-harness-workshop/):**

| Path | What it is | Exercise |
|---|---|---|
| `examples/demo-repo.sh <dir>` | Builds the demo repo with the examples in `.claude/` | H2–H5 fallback |
| `examples/dot-claude/agents/verifier.md` | A subagent that runs the tests and reports, on Haiku with `effort: low`, without `CLAUDE.md` | H2, H3 |
| `examples/dot-claude/skills/changelog-entry/SKILL.md` | A skill that adds a line to `CHANGELOG.md` for the staged change, with the staged diff stat read into the prompt | H4 |
| `examples/dot-claude/hooks/guard-git-add-all.py` | Guard (`PreToolUse`): denies what stages everything (`git add -A`, `git add .`, `git commit -a`) with a reason. An example, not a watertight guard | H5 |
| `examples/dot-claude/hooks/sensor-compile.py` | Sensor (`PostToolUse`): compiles the Python file that was just changed | H5 |
| `examples/dot-claude/hooks/gate-tests-green.py` | Gate (`Stop`): blocks the stop once when the tests are red | H5 |
| `examples/dot-claude/settings.json` | Registers the three hooks | H5 |
| `probes/isolation-check.sh <dir> <model>` | What an empty headless run loads, with and without your user configuration | H1 |
| `probes/subagent-markers.sh <dir> <model>` | Three codewords and a subagent asked which it knows | H2 |
| `traps/run-trap.sh <trap> <runs> <model> <out>` and `traps/trap-*/` | Three traps that run one task with and without a rule in `CLAUDE.md` | H6, optional |

The examples are an answer key and a fallback. Build your own from something your team actually repeats. The directory is called `dot-claude`, not `.claude`, so Claude Code does not load the examples while you work in this repo. `demo-repo.sh` copies it to `.claude/`.

The probes and traps run `claude -p` with `--setting-sources project --strict-mcp-config` and `--max-budget-usd 1` per run. The traps and `subagent-markers.sh` also run with a narrow `--allowedTools` list; `isolation-check.sh` does not. That flag drops your own deny rules along with the rest of your user configuration, so run them only against the demo repo or in a container.

**Versions.** The Claude Code facts here were checked against its documentation on 2026-11-15 (version 2.1.325) and AndThen `v1.1.0`. The reference results were measured on 2026-11-13 and 2026-11-15 (dates per result) on Claude Code 2.1.323 with `claude-sonnet-5-5`, one run per row unless stated. Both tools change every week, so your results may differ. Not run when the reference results were measured: `/context`, `/doctor`, `/doctor prompt-audit`, `/skill-doctor`, `/tasks`, `/subtask`, `/advisor`, `opusplan`, skill-creator, `claude plugin eval` and everything in H7. Those were checked against the documentation only.

## Output

- A list of three things your team wants to remove or move (H1).
- Your own subagent definition, committed (H2), and a routing table with the role definitions you changed (H3).
- Your own skill, committed, with the prompts you tried it on (H4).
- Three hooks, committed: a sensor, a guard and a gate (H5).
- After H6: a pull request against your team's harness, and a one-page rule policy.
- After H7: one built-in feature you tried on real work.

## Steps

### H1 – What gets loaded?

**Guess:** how many tokens does a fresh session in your repo hold before you have typed anything, and what is the largest part?

1. Everyone starts a fresh session and runs `/context`.
2. Run `/doctor`. The report compares unused skills, MCP servers and plugins with what they cost in context, points out slow hooks, and suggests what in `CLAUDE.md` Claude could read from the code instead. Claude changes nothing without a yes. Answer no now and keep the list for H6.
3. Run `/skill-doctor`: what each skill costs and how often it is used.
4. Optional: `labs/x9-harness-workshop/probes/isolation-check.sh /tmp/x9/isolation <model>` loads an empty headless session three ways and prints the tokens each one held.

- **Keep:** a list of three things your team wants to remove or move.
- **Check:** which line on your list do you pay for in every session without ever using it?

<details>
<summary>Reference result</summary>

Measured with `probes/isolation-check.sh` on 2026-11-13: an empty headless run loaded 43 711 tokens with the course owner's full user configuration and 31 002 with `--setting-sources project --strict-mcp-config`. Your number depends on your configuration. The point is the gap between the two.

</details>

### H2 – The subagent

**Guess:** one codeword is in the project's `CLAUDE.md`, one is said in the main session, and one is in the agent definition. Which of them does the subagent know?

1. Run `labs/x9-harness-workshop/probes/subagent-markers.sh /tmp/x9/markers <model>`. Compare the output with your guess.
2. **Write your own subagent** in `.claude/agents/<name>.md` for a side task your team often hands off: running the tests, reading logs, searching a module. Example: [`verifier.md`](x9-harness-workshop/examples/dot-claude/agents/verifier.md).

   | Field | What it controls |
   |---|---|
   | `description` | When Claude delegates here. The only thing Claude sees before it chooses |
   | `tools`, `disallowedTools` | What the agent may do. An agent that only reports should not get `Edit`. With `Bash` it can still write files, so a hard limit needs a hook or a permission rule |
   | `model`, `effort` | The routing, see H3 |
   | `omitClaudeMd: true` | The agent starts without `CLAUDE.md`, for tasks where the prompt is enough |
   | `skills` | Skills that are loaded in full at start |

3. Ask for it by name ("Use the verifier subagent to check the tests") and open `/tasks`. The row shows which model and effort the agent runs on.
4. Try the opposite: `/subtask <task>` starts a fork that inherits the whole conversation. Give the fork and your agent the same question, one that needs something you said earlier. *(Not run when the reference results were measured.)*

- **Keep:** the agent definition, committed in the repo.
- **Check:** what in your prompts to subagents assumes something only the main session knows?

<details>
<summary>Reference result</summary>

The subagent knew the codeword in `CLAUDE.md` and the one in its definition, not the one said in the session.

The documentation says a subagent starts with its own system prompt, the task the main session writes, every level of `CLAUDE.md`, a snapshot of the git state, and the skills its definition preloads. It does not get the conversation, files already read, skills already invoked, or the output style. The built-in Explore and Plan skip `CLAUDE.md`.

</details>

<details>
<summary>Pitfalls</summary>

- A misspelled frontmatter field is ignored without an error message. Run `claude --debug` and search for `does not recognize or apply`.
- A rule the subagent must follow that was only said in the session belongs in the task you give it.

</details>

### H3 – Model routing

**Guess:** your subagent from H2 has `model` in its definition. Which model does it run on if you set `CLAUDE_CODE_SUBAGENT_MODEL` to a different one?

1. **Test the order.** Run the agent from H2 three times and read the model on its row in `/tasks`. Write your guess for each row first.

   | Run with `verifier` (`model: haiku`) | Subagent's model |
   |---|---|
   | Nothing set | |
   | `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5-5 claude` | |
   | The same, plus `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` | |

2. **Read AndThen's routing.** Open the four role agents in `~/.claude/agents/` or `.claude/agents/`. The Subagent Model Policy in the rules template routes by the shape of the task, never by model name, and judgment work stays in the session.
3. **Change a role.** Copy `reviewer.md` into your project's `.claude/agents/`, change `model` or `effort`, ask for it ("Use the reviewer subagent to review the last commit") and read the row in `/tasks`. The project's definition wins over the installed one. Do the same with the original and compare the findings. *(Not run when the reference results were measured.)*
4. **Same task, two levels.** Give a bounded task with a done-criterion you can run to `worker` and to `implementer`, each in a fresh session. Compare the result and `/usage`. One run is an anecdote. Use a task your team actually delegates.
5. **Write your team's routing table:** task shape, role, model, effort. At least one row must differ from AndThen's default, with what you saw in step 3 or 4 as the reason.

- **Keep:** the routing table and the role definitions you changed, committed in the project's `.claude/agents/`.
- **Check:** which task did you give to a stronger model than it needed last week, and how do you know?

<details>
<summary>Answer key</summary>

| Run with `verifier` (`model: haiku`) | Subagent's model (measured) |
|---|---|
| Nothing set | Haiku |
| `CLAUDE_CODE_SUBAGENT_MODEL=claude-sonnet-5-5 claude` | Haiku. The definition wins |
| The same, plus `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` | Sonnet. The variable wins over every definition |

Claude Code takes the first one that exists: the model Claude names in the call itself, `model` in the definition, the environment variable, and last the model of whoever starts the agent. A nested subagent therefore inherits its parent's model, not the main session's.

</details>

<details>
<summary>Reference result</summary>

AndThen `v1.1.0` pins `oracle` at Fable and `high`, `implementer` at Sonnet and `high`, `reviewer` at Opus and `medium`, `worker` at Haiku and `high`.

Step 4, measured once each on the demo repo (one function and two tests): both gave green tests. The whole run cost 0.05 dollars with `worker` and 0.14 with `implementer`.

</details>

<details>
<summary>Pitfalls</summary>

- The environment variable alone changes no agent that has `model` in its definition.
- The session's `/effort` does not apply to a subagent on a different model, so set `effort` in the definition.
- `reviewer` has a lower effort than `implementer` on purpose: higher gave analysis paralysis, not more findings (`docs/MODEL-EFFORT-SELECTION-GUIDE.md` in AndThen).
- The built-in Explore is replaced by your own agent named `Explore` with its own `model`.

</details>

### H4 – Your own skill

**Guess:** will Claude choose your skill when you ask for the thing in your own words, without naming it?

1. Pick a prompt or workflow someone on the team has written at least three times.
2. Write `.claude/skills/<name>/SKILL.md`. Example: [`changelog-entry`](x9-harness-workshop/examples/dot-claude/skills/changelog-entry/SKILL.md).

   | Choice | Field |
   |---|---|
   | When it is chosen | `description`: what it does and when, in the user's words, the main case first. The listing cuts at 1 536 characters |
   | Who may invoke it | `disable-model-invocation: true` for things only a human should start |
   | Which tools should not ask | `allowed-tools` |
   | Fresh data in the prompt | ``!`command` `` or a code block opened with ```` ```! ```` runs before Claude sees the text |
   | Its own context | `context: fork` and `agent:` run the skill in a subagent. The text must then be a task, not guidelines |

3. Apply AndThen's test from `docs/SKILL-AUTHORING-GUIDELINES.md`: would the agent do the right thing without the line? If so, strike it. What remains is what only the author knows.
4. **Test the trigger** in a fresh session with three natural phrasings, one of which should not choose the skill.
5. **Test the value against a baseline.** Turn the skill off in the `/skills` menu (select it and press space; the menu writes `skillOverrides` to `.claude/settings.local.json`) and give the same prompt in a new session. Was the result worse? The skill-creator plugin makes the comparison for you and can pit two versions against each other (`/plugin install skill-creator@claude-plugins-official`, then "evaluate my <name> skill with skill-creator"). *(Not run when the reference results were measured.)*

- **Keep:** the skill, committed, with the two prompts you tested.
- **Check:** which line in your skill could Claude have done without?

<details>
<summary>Reference result</summary>

In the demo repo, the prompt "I have staged a change. Record it in the changelog." chose `changelog-entry`, and Claude wrote a line under `## Unreleased`.

</details>

<details>
<summary>Pitfalls</summary>

- If the frontmatter cannot be parsed, the skill loads without a description and is never chosen (`claude plugin validate .claude/skills`).
- The skill's text is read in once and not read again, so write it as standing instructions, not one-off steps.
- After a compaction only the skill's first 5 000 tokens remain, so the most important part goes first.

</details>

### H5 – Your own hooks

**Guess:** the agent is asked to run `git add -A`, and a hook denies it. What does the agent do next?

Three kinds, one of each. The examples are in [`examples/dot-claude/hooks/`](x9-harness-workshop/examples/dot-claude/hooks/) and registered in [`settings.json`](x9-harness-workshop/examples/dot-claude/settings.json).

| Kind | Event | Contract |
|---|---|---|
| Guard | `PreToolUse`, matcher `Bash` | Exit 2 stops the call, and stderr goes to Claude as the reason |
| Sensor | `PostToolUse`, matcher `Edit\|Write` | The tool has already run. Exit 2 shows stderr to Claude |
| Gate | `Stop` | JSON with `decision: "block"` and `reason` keeps the turn alive |

1. **The sensor:** run your team's linter or type checker on the file that was just changed. It must be fast.
2. **The guard:** pick a command your team never wants to see. Write the reason so the agent knows what to do instead.
3. **The gate:** run the test command when the agent wants to stop. Read `stop_hook_active` and let the stop through when it is true. Claude Code only gives up after eight denials in a row with no tool call between them, so a gate that denies while Claude keeps editing holds the turn alive without end. Also let the stop through when `background_tasks` is not empty: a subagent is still working and the tree is half-finished.
4. Register them in `.claude/settings.json`, check with `/hooks`, and provoke each one.
5. Read AndThen's two hooks for comparison: `hooks/scripts/block-dangerous-commands.py` (guard) and `context-hint.py` (`Stop`).

- **Keep:** the three hooks, committed.
- **Check:** show me the sensor catching an error, and tell me what it costs when nothing is wrong.

<details>
<summary>Reference result</summary>

Measured in the demo repo:

| Kind | Outcome |
|---|---|
| Guard | `git add -A` was denied. Claude staged and committed by path and said the hook had stopped the command |
| Sensor | A line with a syntax error was flagged right after the edit. Claude reported that a hook flagged it |
| Gate | Red tests stopped the finish once ("Stop hook feedback" went to Claude one time). In one run Claude fixed them, in another it explained why the tests could not pass and left them red |

The hook scripts alone, without a model: the guard denies `git add -A`, `git add .`, `git add -u`, `git commit -am` and `git commit -a -m`, and lets through `git add <file>`, `git commit -m … -- <file>` and `git commit --amend`. The sensor exits 2 on a file with a syntax error. The gate gives `decision: block` on red tests in a changed tree, and is silent when the tree is unchanged, when `background_tasks` is not empty and when `stop_hook_active` is true. The gate prompt was run twice, and only the second run had the background-work and unchanged-tree checks.

You can reproduce the script-level results without a model by piping a JSON event into a hook, for example `echo '{"tool_input":{"command":"git add -A"}}' | .claude/hooks/guard-git-add-all.py; echo $?` in the demo repo, with `CLAUDE_PROJECT_DIR` set to the repo.

</details>

<details>
<summary>Pitfalls</summary>

| Pitfall | What you do |
|---|---|
| The sensor writes to stderr and exits 0 | Claude never sees it. Exit 2 |
| The gate runs the whole suite after every reply, also after a plain question | `Stop` fires every time Claude finishes answering. Run only when the working tree has changed, as the example does |
| Your team builds its own check before commit | A project skill named `verify` is run by Claude on its own before every commit (2.1.286 and later) |
| The guard matches `git add -A` and the agent takes another route | A hook matches commands, not intent. Put the check on the result instead, in the gate |
| A rule should only apply while a certain skill runs | Put the hook in the skill's frontmatter (`hooks:`). It applies from the invocation to the end of the session |
| Your team builds a gate for something `/goal` already does | `/goal <condition>` is a built-in, session-bound gate where a model judges the condition after every turn |

</details>

### H6 – The rules under the loupe

**Guess:** which three rules in your `CLAUDE.md` would the agent follow even if you struck them?

1. Run `/doctor prompt-audit`. Claude goes through `CLAUDE.md`, skills and other configuration for outdated and contradictory instructions. *(Not run when the reference results were measured.)*
2. **Place each rule.** Go through AndThen's rules template (`CRITICAL-RULES-AND-GUARDRAILS.md`) or your team's own rules, line by line:

   | The rule is | It belongs in |
   |---|---|
   | Something the agent must always know about the project | `CLAUDE.md` |
   | Relevant only for certain files | `.claude/rules/` with `paths:` |
   | Reference material or a workflow needed sometimes | A skill |
   | Something that must hold every time | A hook or a permission rule |
   | Something Claude Code has a setting for | The setting |
   | How the answers should sound | An output style |
   | Something the agent does anyway | Nowhere |

3. **See what three rules do.** Three rules from AndThen's template were run with and without the rule in a trap. Guess the outcome for each before you open the result. Optionally build a trap of your own for a rule your team disputes, on the same pattern (`labs/x9-harness-workshop/traps/`). A trap with two arms of five runs costs about half a dollar:

   ```bash
   labs/x9-harness-workshop/traps/run-trap.sh labs/x9-harness-workshop/traps/trap-attribution 5 <model> /tmp/x9/attribution
   ```

   Set `ARMS="with without setting"` for a third arm in `trap-attribution` only. Run it only against the traps, never against your own repo (see the note on `--setting-sources` under Input).
4. **Move three rules:** one to a hook, one to a setting or a `paths:` rule, and strike one. The guard in H5 is half an example: it stops what stages everything, but not a plain `git commit` that takes another agent's staged file along. The whole rule "commit by path" needs a check of the result.

- **Keep:** a pull request against your team's harness, and a one-page rule policy: when does something become a rule, a skill, a hook or a setting?
- **Check:** which rule did you want to strike but did not dare, and what would convince you?

<details>
<summary>Reference result</summary>

Measured on Sonnet 5.5, five runs per arm, on 2026-11-13:

| Rule (from AndThen's rules template) | With | Without | What it says |
|---|---|---|---|
| "Stage by path, never `-A` or `-u`, and commit by path" (`trap-commit-by-path`) | 5 of 5 | 5 of 5 | The model did the right thing anyway in this trap |
| "Confirm a reported problem still exists before fixing it" (`trap-stale-issue`) | 5 of 5, 5–7 turns | 5 of 5, 7–9 turns | Same outcome, but 5–7 turns with the rule against 7–9 without |
| "No AI attribution anywhere" (`trap-attribution`) | 5 of 5 | 0 of 5 | The rule does the whole job, and the `attribution` setting in `.claude/settings.json` does it too (5 of 5) |

The result holds for that model and those traps.

</details>

<details>
<summary>Pitfall</summary>

No effect in a trap is not the same as no value. A rule that carries a reason the agent cannot read from the code is context (AndThen's skill guidelines), and it stays.

</details>

### H7 – Ways of working

Everyone picks a line they have never used, tries it on real work, and says what it replaced. *(Nothing in the table has been run; all of it was checked against the documentation.)*

| When you notice you | Try |
|---|---|
| wait for the agent and have a side task in the same matter | `/subtask <task>`: a fork that inherits the conversation and answers in it |
| have several independent tasks | `claude --bg "<prompt>"` per task and `claude agents` for the overview (agent view, research preview). `/background` moves the open session there |
| type "continue" over and over | `/goal <condition>`: another model judges the condition after every turn |
| need to make the same mechanical change in many places | `/batch <instruction>`: 5–30 subagents, each in its own worktree, after a plan you approve |
| have a job that is outgrowing a handful of subagents | Ask for a workflow ("use a workflow"): Claude writes a script that runs the subagents and cross-checks the findings |
| poll CI or a deploy by hand | `/loop 5m <prompt>` |
| want deeper reasoning in a single turn | `ultrathink` in the prompt, or `/effort` for the whole session |
| run everything on the top model to get a good plan | `/advisor opus` lets the main model consult a stronger model at the decision points (experimental, needs the Anthropic API). The model alias `opusplan` runs Opus in plan mode and Sonnet in execution |
| ask a question about what is already in the conversation | `/btw` |

- **Check:** what did you do by hand last week that one of the rows does?

## Verify

Show your facilitator, do not tell:

- [ ] Your own subagent: `/tasks` during a run shows the agent with the right model and effort (H2, H3).
- [ ] Your routing table, with the row that differs from AndThen's default and its reason (H3).
- [ ] Your own skill: a fresh session chooses it on a natural phrasing, with the same prompt and the skill turned off beside it (H4).
- [ ] Three hooks: `/hooks` lists them, and you provoke each one (H5).
- [ ] After H6: the pull request against the harness, and `/context` before and after.
- [ ] You can name at least one guess that was wrong and what it taught you.

## Sizing check

*Does the thing deserve a hook, a skill or a subagent?* Only when the trigger in the table at the top has actually happened. A hook for an error that never happened is a cost, and so is a skill nobody calls (`/skill-doctor` shows which). Your case repo starts with your team's harness. Test every entry in your friction log against that table before it becomes a rule.

## References

Claude Code documentation, read on 2026-11-15. The pages change often, so read them again before you rely on a detail.

| Exercise | Read |
|---|---|
| All | [Extend Claude Code](https://code.claude.com/docs/en/features-overview): when to choose `CLAUDE.md`, a skill, a subagent, a hook or a plugin. The blog post [Steering Claude Code](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) goes through the same choice. [Best practices](https://code.claude.com/docs/en/best-practices) |
| H1 | [Explore the context window](https://code.claude.com/docs/en/context-window), [Debug your configuration](https://code.claude.com/docs/en/debug-your-config) (`/context`, `/doctor`, `/hooks`), [How Claude remembers your project](https://code.claude.com/docs/en/memory), [Commands](https://code.claude.com/docs/en/commands) |
| H2 | [Create custom subagents](https://code.claude.com/docs/en/sub-agents): frontmatter, what loads at start, the fork |
| H3 | [Create custom subagents](https://code.claude.com/docs/en/sub-agents) (the section Choose a model), [Model configuration](https://code.claude.com/docs/en/model-config) (effort, `opusplan`), [Advisor](https://code.claude.com/docs/en/advisor), [Manage costs](https://code.claude.com/docs/en/costs). The blog post [Spending your effort](https://claude.dev/blog/spending-your-effort/) |
| H4 | [Extend Claude with skills](https://code.claude.com/docs/en/skills): frontmatter, dynamic context, evaluation. [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) and the [skill-creator](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator) plugin |
| H5 | [Automate actions with hooks](https://code.claude.com/docs/en/hooks-guide) (examples and troubleshooting), [Hooks reference](https://code.claude.com/docs/en/hooks) (events, exit codes, JSON output), [Keep Claude working toward a goal](https://code.claude.com/docs/en/goal) |
| H6 | [How Claude remembers your project](https://code.claude.com/docs/en/memory) (`.claude/rules/`, size, `/doctor prompt-audit`), [All settings](https://code.claude.com/docs/en/settings-reference) (`attribution`), [Configure permissions](https://code.claude.com/docs/en/permissions) |
| H7 | [Run agents in parallel](https://code.claude.com/docs/en/agents), [Agent view](https://code.claude.com/docs/en/agent-view), [Dynamic workflows](https://code.claude.com/docs/en/workflows), [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks), [Commands](https://code.claude.com/docs/en/commands) (`/batch`, `/btw`, `/subtask`) |
| Packaging | [Create a plugin](https://code.claude.com/docs/en/plugins/create), [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals) |

AndThen (`v1.1.0`): the [role agents](https://github.com/IT-HUSET/andthen/tree/main/plugin/skills/init/templates/agents/claude), the [Model & Effort Selection Guide](https://github.com/IT-HUSET/andthen/blob/main/docs/MODEL-EFFORT-SELECTION-GUIDE.md), the [rules template](https://github.com/IT-HUSET/andthen/blob/main/plugin/skills/init/templates/guidelines/CRITICAL-RULES-AND-GUARDRAILS.md), the [Skill-Authoring Guidelines](https://github.com/IT-HUSET/andthen/blob/main/docs/SKILL-AUTHORING-GUIDELINES.md) and the [hooks](https://github.com/IT-HUSET/andthen/blob/main/hooks/README.md).

## What next

After H5, look at the guesses that were wrong. Each one points to a continuation:

| Wrong guess in | Continue with |
|---|---|
| H1 What gets loaded? | H6 here, or [X10 Team workspace](x10-team-workspace.md) |
| H2 The subagent | [X5, Going further](x5-parallel-autonomy.md#going-further) |
| H3 Model routing | [X5, Going further](x5-parallel-autonomy.md#going-further) |
| H4 Your own skill | [X10 Team workspace](x10-team-workspace.md): package and share the skill and hooks as a plugin |
| H5 Your own hooks | [X5, Going further](x5-parallel-autonomy.md#going-further) (hooks as sensors in unattended runs), or H6 here |

- **H6–H7 here** if the open question is where each rule belongs, or what you do by hand that the tool already does. It needs nothing beyond H1–H5.
- **X10 Team workspace** if the open question is what your team's agents need to know that no single repo carries.
- **X5, Going further** if the open question is which steps of the loop can run without you, or when parallel agents pay off, and who holds the plan.

If you cannot decide, take the one most of your wrong guesses point to. If you guessed everything right, you are ahead of the workshop: write down what you still cannot answer about your harness, and pick the continuation from that.
