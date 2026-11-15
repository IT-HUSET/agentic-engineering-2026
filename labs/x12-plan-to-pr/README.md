# X12 preparation kit: plan to PR

## Status

**2026-11-16, not offered.** AndThen 1.2.0 is tagged `v1.2.0` (`cee221357d7fce0468581eba6974d9559dab4dda`, 2026-11-15) and exists on `origin/develop` only. `origin/main` is still 1.1.0, so participants who install the latest release get 1.1.0 until 1.2.0 is merged there (D9). The runner does not depend on that: it loads its own pinned checkout and rejects anything below 1.2.0.

The `ship` skill at `v1.2.0` states that `--auto` authorises pushing the branch and opening the PR, and that incomplete publication ends `BLOCKED:`. That is a source check. The offline tests use fake tools; no model, PR, Actions runner or remote container has been exercised.

**Offer condition (D33):** the pinned `v1.2.0` is verified in the remote container, and the full-chain rehearsal in the [activation checklist](#activation-checklist-with-v120) has passed.

## Whose runner

**Decided 2026-11-16 (D33):** X12 is individual, like X11. Each participant runs it on their own X11 VM, in their own repo, with their own token from `claude setup-token`. Model use counts against the participant's own plan (IT-HUSET team seat or own plan, D11). There is no shared runner, shared token or team seat. A token is tied to the person who ran `setup-token` ([authentication](https://code.claude.com/docs/en/authentication#generate-a-long-lived-token)); keep it a secret of that one repo and never share it. Anthropic points shared secrets to API keys, which is why a shared runner is out of scope.

The facilitator may prepare the host paths and the pinned AndThen checkout in section 2 before the course. The participant then registers the runner and stores the two secrets.

## What it does

The controller runs inside the disposable devcontainer from [X11](../x11-remote-environment.md). GitHub's self-hosted runner runs **outside** that container, on the VM. The controller starts a fresh headless Claude Code session per stage:

```text
approved pushed plan
  → exec-plan --auto
  → review --fix --auto, repeated while its Next line asks for a follow-up review
  → one read-only follow-up review of the final revision (code, gap, security)
  → the configured real final checks
  → ship --auto (--publish only)
  → verify the remote head and the PR
```

**The loop ends on the hand-off, never on the verdict** (AndThen COOKBOOK, "Review and fix until clean"). A Note no fix round may apply can hold readiness at FAIL, so waiting for PASS may never end. A fix round's `Next (fresh session):` line asks for another review only after it fixed a CRITICAL or HIGH finding or left a fix partial. The controller continues on that line (projected as `next_review`, or found in the result text) or on the same condition read from the report's `## Remediation Status`. A CRITICAL or HIGH finding still `DEFERRED`, `UNRESOLVED` or `SURFACED` when no follow-up is asked needs a decision and stops the job. `max_fix_rounds` (at most 3) is a backstop: still asking at the limit stops the job.

**Ready to ship** follows `plan-schema.md` § Shipping: every story `done` (with a `verified.summary`) or `skipped`, and the confirmation review leaves no CRITICAL or HIGH finding open (`DEFERRED` counts as open). The review verdict is not a gate. The configured final checks must also pass.

Before `ship` the controller requires the remote branch to still sit at the approved SHA and no PR to exist. After `ship` it requires `plan.json` to still exist, the final checks to pass again, the remote head to equal the local head and exactly one open PR into the base at that head, the one `ship` reported. A `BLOCKED` result (also in the result text), a permission denial, a plugin that did not load, a failed check or an exhausted limit stops the job with a saved reason. The controller never substitutes its own PR publisher for `ship`.

## Files and local proof

| File | Purpose |
|---|---|
| `run.py` | Sequential controller: review loop, shipping gate, real checks, PR verification |
| `test_run.py` | Offline tests with stand-in Claude/GitHub CLIs and real local Git repositories |
| `config.example.json` | One trusted repository, branch prefix, base, fix-round limit, stage budget and final-check argv |
| `settings.example.json` | Deny rules and one allow rule; the permission mode is `auto`, set by `run.py` |
| `workflow.example.yml` | Inactive `workflow_dispatch` template for the X11 VM |

**Facilitator rehearsal, not a participant step.** From the participant repository root:

```bash
python3 -B -m unittest discover -s labs/x12-plan-to-pr -p 'test_*.py' -v
```

Read the tests as the job contract. Find the case where the agent exits 0 but reports `BLOCKED`, and the case where a real check exits non-zero: neither may reach `ship`. The suite writes fixtures under `.agent_temp/x12-tests/`, cleans only its own, and uses neither model credentials nor the network. Its simulated 1.2.0 manifest is a fixture. It proves the controller's branching, not an agent's ability to implement or review a feature.

## 1. Prepare the trusted course repository

- Use your own course repo with the course `.devcontainer/` at its root. Adjust its dependency step and the final checks. AndThen's project root and the Git root must be the same directory.
- Commit the kit, the reviewed devcontainer configuration and the workflow on the **default branch** before dispatch. Put the template at `.github/workflows/x12-plan-to-pr.yml` and keep it a template until the activation checks pass.
- Use a single-container configuration in ordinary JSON. The workflow's Python override builder does not parse JSONC or orchestrate Docker Compose.
- Use `init` to install the approved role agents into the **project** before preparing the plan. Do not rely on a runner account's personal plugins, agents, hooks or credentials.
- Finish the outer loop, commit every FIS and `plan.json`, approve C2 for that exact commit, then push a non-default branch under the configured prefix. An untracked plan, a dirty tree or a story left unfinished is rejected.
- The workflow takes branch, full lowercase 40-character source SHA and repo-relative `plan.json` path as data. The C2 checkbox attests approval of that SHA; an unchecked box fails the first step with "C2 not approved". Execution is restricted to the configured repository and to whoever may dispatch it, which is you.

Do not enable fork, issue or comment events or run contributor code here. The job has shell access inside a container that holds your model and GitHub credentials. That fits your own repo and your own VM, not hostile code.

## 2. Prepare the VM and controlled configuration

Follow X11 first. The runner service account needs Docker access, Dev Container CLI and Python 3.10 or later. Docker-group access gives that account control of the VM; keep its Azure login and host credentials elsewhere. Do not forward SSH agents or mount `/var/run/docker.sock` into the agent container.

Register a repository-scoped Linux x64 GitHub Actions runner with the extra label `x12`. Configure its service to survive SSH disconnects. The runner connects out to GitHub and needs no public webhook endpoint.

Create the host paths for the actual runner service account:

```bash
x12_runner_user='<runner-service-account>'
sudo install -d -o "$x12_runner_user" -g "$x12_runner_user" /var/lib/x12/state /var/lib/x12/host-jobs /opt/x12
sudo install -d -m 0755 /etc/x12
```

Install AndThen at the pinned tag and record what resolved:

```bash
git clone https://github.com/IT-HUSET/andthen.git /opt/x12/andthen
git -C /opt/x12/andthen checkout --detach v1.2.0
git -C /opt/x12/andthen rev-parse HEAD   # expect cee221357d7fce0468581eba6974d9559dab4dda
```

The plugin is at `/opt/x12/andthen/plugin`; record its manifest version and the Claude Code version. Do not edit the checkout from a workload run. The container receives it read-only at `/opt/andthen`, and `--plugin-dir` selects it explicitly. The controller rejects a manifest older than 1.2.0 before any agent call, and each stage checks that the AndThen plugin loaded from that path. CLI-local plugins replace same-name marketplace plugins, but managed `enabledPlugins` policy can prevent an override; check the startup metadata in the rehearsal.

Copy `config.example.json` to `/etc/x12/config.json` and edit the **host** copy:

- `repository`: the one permitted `owner/repo`, matching `X12_REPOSITORY`.
- `base`, `branch_prefix`: the PR target and the allowed source prefix.
- `plugin_dir`, `settings`, `state_dir`: keep the container paths in the example.
- `checks`: the application's real build/test/lint/type-check commands as argv arrays, run from the repo root without a shell. The example runs `todo-app`'s tests with `uv run --directory todo-app pytest -q`. Configure every gate the approved work needs, including browser checks. No UI check is implied by `pytest`.
- `max_fix_rounds`: the fix-loop backstop, 3 at most.
- `stage_budget_usd`: a runaway cap passed to every stage as `--max-budget-usd`. It is Claude Code's client-side list-price estimate, not a bill. On a subscription seat the real limit is the seat's plan usage (D11). The workflow's `timeout-minutes` bounds the whole job.

The workflow checks the controller out of the **default branch** and mounts it, the plugin and `/etc/x12` into the container read-only; only `/x12-state` is writable. The agent can therefore edit the workload but not its own controller, plugin or configuration. A probe step fails the job before credentials are provided if the container is privileged or those three mounts are missing or writable. The container's `remoteUser` must be able to write `/var/lib/x12/state` through the state mount; Dev Container CLI normally adjusts the UID, but the rehearsal must show it.

The override reuses the Dockerfile, Features and lifecycle setup of the trusted devcontainer configuration; it builds no second tool image. Relative build paths still resolve against the workload's original `.devcontainer/devcontainer.json`.

## 3. Credentials and repository settings

Repository **variables**:

| Variable | Value |
|---|---|
| `X12_REPOSITORY` | The trusted `owner/repo` |
| `X12_GIT_NAME` | The course Git author name |
| `X12_GIT_EMAIL` | The course Git author email |

Repository **secrets**, created through the organisation's approved route:

| Secret | Scope |
|---|---|
| `X12_CLAUDE_CODE_OAUTH_TOKEN` | Output of `claude setup-token`, run by **you** and passed to the job as `CLAUDE_CODE_OAUTH_TOKEN`. Model requests only; usage counts against your plan limits (D11) |
| `X12_GITHUB_TOKEN` | Only this case repo, contents read/write and pull requests read/write; add issues access only if the plan's tracker mode requires it |

Never set `ANTHROPIC_API_KEY` in the job. In `-p` mode a present API key always wins over the subscription token, so a stray key would silently switch billing. The controller stops if `CLAUDE_CODE_OAUTH_TOKEN` is missing or if `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` is set. Do not add `--bare`: bare mode never reads `CLAUDE_CODE_OAUTH_TOKEN`.

A course GitHub App installation token is preferable for `X12_GITHUB_TOKEN` where the organisation supplies one; the template does not mint tokens. Rehearse token lifetime, branch policy and required CI checks. Actions' default token is read-only here and is not the publication token. `GITHUB_TOKEN` event behaviour and organisation approvals can affect follow-on checks, so verify the required checks on the rehearsal PR.

`actions/checkout` uses `persist-credentials: false`. The launch adds the repository-local helper `!gh auth git-credential`; `GH_TOKEN` alone would authenticate `gh` but not Git push. The helper holds no token. Credentials reach only `docker exec`, through its inherited environment, after container setup and the mount check. They are never literal arguments or build inputs. `claude auth status` and `gh auth status` must succeed before execution.

### Workload settings and MCP

Every stage starts with `--permission-mode auto` ([permission modes](https://code.claude.com/docs/en/permission-modes#eliminate-permission-prompts-with-auto-mode)). A classifier model reviews each action that no rule settles, so `settings.example.json` carries deny rules and a single allow rule for `Skill`, and no broad `Bash` or `Agent` allow: auto mode drops those on entry anyway. Never a bypass mode (`--dangerously-skip-permissions`, `bypassPermissions`) and no `dontAsk`; a test pins this.

- **Deny rules** apply in every mode. The controller adds push/PR/API deny patterns before every stage but `ship`. They catch mistakes; they do not contain arbitrary shell scripts or stop a process reading credentials it holds.
- **`ship`** is the one stage that pushes. Its prompt states the authorization for this branch and base, which the classifier reads as your instruction.
- **A blocked action does not run, and the agent keeps working.** A `-p` run has no prompt to fall back to, and repeated blocks (3 in a row, 20 in total) do not stop it. The controller stops the job on any entry in `permission_denials`.
- **Availability.** Auto mode needs a supported model and plan, and an organisation can disable it. When unavailable, the session starts in Manual mode, where unlisted calls are denied, so the first stage stops on a denial instead of running unreviewed. Confirm in the rehearsal that `auto` is active.
- The classifier is a second model, not a guarantee. The dedicated VM/container and your own repo remain the boundary. Never use the kit in a container with unrelated personal or cloud credentials.

**Open hardening item.** Without `--bare`, `claude -p` runs the hooks in the workload's committed `.claude/settings.json` and connects its `.mcp.json` servers, even in a folder it never trusted ([permissions: what runs before you trust a folder](https://code.claude.com/docs/en/permissions#what-runs-before-you-trust-a-folder)). `--setting-sources user --strict-mcp-config` would skip both. They are not added, because the docs do not say that the fence passed through `--settings` still applies under `--setting-sources user`, or that project skills and the role agents installed by `init` keep loading (their frontmatter hooks still run). The pinned AndThen plugin ships no hooks or MCP servers, so it would not be affected. To close this item, rehearse the flags on a copy of a stage's argv and check that `system/init` still shows the one pinned plugin and that a deny rule from `settings.example.json` still denies.

## 4. Dispatch and inspect

The workflow's inputs are `branch`, `source_sha`, `plan`, the C2 checkbox and **publish**. Leave publish off for the first model rehearsal. From a prepared container the equivalent invocation is:

```bash
python3 /opt/x12-control/labs/x12-plan-to-pr/run.py \
  --config /opt/x12-config/config.json \
  --branch feat/example \
  --sha '<approved-40-character-commit>' \
  --plan docs/specs/example/plan.json \
  --c2-approved
```

This uses the model, implements the plan and creates local commits. Without `--publish` (the workflow's checkbox) the job ends `prepared`: every gate passed and `ship` was not invoked. That is not a simulation or a published result. To publish, dispatch again from a new approved source commit and branch.

Each job writes `/var/lib/x12/state/<X12_JOB>/status.json` (status, reason, stage list, `reviewed_sha`, `pr_url`), the native review reports and the final-check logs; the Actions artifact carries those files. Raw stage stdout/stderr stay on the VM and may contain source and model output; inspect and redact before sharing.

The wrapper schema in `run.py` asks the agent to project the skill's result into `PASS`/`FAIL`/`BLOCKED`, revision, report paths, `pr_url` and `next_review`. This schema is **not an AndThen API**. The controller also reads the actual `plan.json`, checks clean Git state, parses the native reports' findings and `## Remediation Status` outside fenced examples, runs the configured checks itself and queries GitHub's PR metadata. Exit 0 or a reported URL alone cannot pass.

The confirmation review is a delta review: it covers the work since the fix round's revision and the findings still open, not the whole plan again.

The `ship` prompt says to keep the plan bundle and design folders, and the job stops if `plan.json` is gone afterwards. `ship --auto` may take its own recommendation to delete a ready plan's bundle (`v1.2.0` ship, step 5), so observe in the rehearsal whether the instruction holds.

## 5. Failure and retention

- GitHub concurrency serialises jobs per repository and branch without cancelling an active run. A repeat dispatch of a branch that already has a PR, or whose remote tip moved, stops before any agent call. The controller never force-pushes.
- A failed job leaves its `status.json` with `blocked` and the reason, its workspace and its logs. The kit does not resume partial agent work: fix the cause, then dispatch again from the approved SHA (a new workspace) or from a new approved commit.
- There is still a check/publish race because `ship` owns the push and PR creation. Fast-forward rejection protects divergent history, but the wrapper cannot give an atomic compare-and-publish. Rehearse what `ship` does when the branch advances during shipping. Keep one writer per branch.
- **Cancellation.** The workflow has no signal trap: a foreground `docker exec` blocks bash's traps and does not forward signals into the container. Cancelling the Actions job ends the step, and the `always()` stop step then runs `docker stop --time 10` for this job's container. That stop kills everything in the container, so the controller cannot write a final status and `status.json` stays `running`. The workload directory, Claude configuration volume, state and per-job host records remain. Cancelling a job differs from disconnecting an SSH client. Rehearse real cancellation during execution and during shipping.
- A failure during or after `ship` can leave a pushed branch or PR while the job reports `blocked`. Inspect GitHub before retrying. The controller marks `published` only after one open PR into the base at the final head SHA, a present `plan.json`, a clean tree and passing post-ship checks.
- Archive the owned work and proof before the operator removes that job's container, workspace and volumes. Remove only resources named in the job directory. Do not sweep the VM while another job is using it. X11's provider cleanup still applies.

## Activation checklist with v1.2.0

- [ ] You have your own runner on your own X11 VM, your own repo and your own `setup-token` token ([Whose runner](#whose-runner)).
- [ ] Install `v1.2.0` at `/opt/x12/andthen` as in section 2. Confirm `rev-parse HEAD` is `cee221357d7fce0468581eba6974d9559dab4dda`, read its `ship` skill and plugin README, and record the manifest and Claude Code versions.
- [ ] Re-run the offline suite. Validate the copied workflow with actionlint and ShellCheck, including the `x12` label. Pin reviewed action revisions per the organisation's policy.
- [ ] Rehearse the real VM service account, full devcontainer build, mounts, state UID, plugin `system/init` metadata, that auto mode is active and nothing is denied (`permission_denials` empty), `claude auth status` with only the subscription token set, the Git helper and every application check.
- [ ] Run one bounded plan with publish off. Compare each structured projection with its native reports. Confirm the loop ended on a hand-off, all three lenses ran and the report parser matches 1.2.0.
- [ ] On a disposable branch, tick publish. Confirm `ship --auto` opens the expected PR, note whether it kept or deleted the bundle, and check the PR reports real checks. The facilitator reads C4 on GitHub; merging stays human.
- [ ] Run a red check, a semantic `BLOCKED`, an unavailable lens or plugin, an exhausted loop, a CRITICAL/HIGH finding left `DEFERRED`, a duplicate dispatch and a remote advance. None may reach `ship`; inspect any partial publication.
- [ ] Disconnect the client during a live job: the runner finishes and keeps its result. A disconnected client differs from a stopped VM.
- [ ] Cancel a real Actions job during execution and during shipping. Confirm the container stops, its work and volume survive and nothing keeps publishing in the background.
- [ ] Verify the required PR checks run with the chosen token and organisation policy. Set evidence retention, quota ownership and cleanup responsibility, then offer X12.

## References

- [Claude Code headless](https://code.claude.com/docs/en/headless): `structured_output`, `system/init` plugin field, bare mode. [Authentication](https://code.claude.com/docs/en/authentication): precedence, `setup-token`. [GitHub Actions](https://code.claude.com/docs/en/github-actions) and [legal and compliance](https://code.claude.com/docs/en/legal-and-compliance#authentication-and-credential-use): token guidance.
- [CLI reference](https://code.claude.com/docs/en/cli-reference), [permission modes](https://code.claude.com/docs/en/permission-modes), [plugin name conflicts](https://code.claude.com/docs/en/plugins/loading#name-conflicts): `--plugin-dir`, `--json-schema`, `--max-budget-usd`, `auto`, managed plugin precedence.
- [Dev Container CLI](https://github.com/devcontainers/cli), [CLI source](https://github.com/devcontainers/cli/blob/main/src/spec-node/devContainersSpecCLI.ts), [configuration source](https://github.com/devcontainers/cli/blob/main/src/spec-node/configContainer.ts): `up`, `--override-config`, original config-path resolution. The CLI `--mount` takes no `readonly`; the template uses Docker `runArgs` mounts.
- [Manual workflow dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow), [self-hosted runner communication](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), [GitHub token behaviour](https://docs.github.com/en/actions/concepts/security/github_token).
- AndThen at `v1.2.0`: [plugin README](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/README.md), [plan schema](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/references/plan-schema.md), [review report template](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/skills/review/references/report-template.md), [COOKBOOK: review and fix until clean](https://github.com/IT-HUSET/andthen/blob/v1.2.0/COOKBOOK.md#review-and-fix-until-clean-from-a-coordinating-session). The 1.1.0 contracts informed the review parsing; the activation checks must still exercise 1.2.0.
