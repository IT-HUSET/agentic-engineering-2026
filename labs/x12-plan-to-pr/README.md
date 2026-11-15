# X12 preparation kit: plan to PR

**Status, 2026-11-15:** **AndThen 1.2.0 is available on `develop` and, according to the owner, is installed in both Claude Code and Codex on the instructor's workstation.** Its installed `ship` skill confirms that `--auto` authorises pushing the branch and opening the PR; incomplete publication ends with `BLOCKED:`. This is a source check, not a live publication test or evidence of a release tag on `main`. Pin the source commit used for rehearsal and verify the remote container's installation separately. Versions below 1.2.0 and prereleases remain rejected. No model, GitHub PR, Actions runner or remote container has been exercised by this kit's offline tests. Complete the activation checklist before offering the exercise.

The controller runs inside the disposable devcontainer from [X11](../x11-remote-environment.md). GitHub's self-hosted runner runs **outside** that container on the VM. The controller starts a fresh headless Claude Code session for each stage:

```text
approved pushed plan
  → exec-plan --auto
  → review --fix --auto + separate read-only review (code, gap, security)
  → commit a snapshot of the passing native review
  → run the configured real final checks
  → ship --auto
  → verify the actual remote head, PR metadata, retained plan and post-ship checks
```

The review/fix pair runs at most three times. A failed check, missing lens, denial, `BLOCKED`, malformed result, changed remote tip or exhausted limit stops the job. The controller never substitutes its own PR publisher for `ship`.

## Files and local proof

| File | Purpose |
|---|---|
| `run.py` | Sequential controller, native-review and real-check gates, branch lock and attempt ledger |
| `test_run.py` | Offline tests with stand-in Claude/GitHub CLIs and real local Git repositories |
| `config.example.json` | One trusted repository, branch prefix, base, limits and actual check argv |
| `settings.example.json` | Explicit noninteractive tool policy for this disposable course container |
| `workflow.example.yml` | Inactive `workflow_dispatch` template for the X11 VM |

From the participant repository root:

```bash
python3 -B -m unittest discover -s labs/x12-plan-to-pr -p 'test_*.py' -v
```

The suite writes its fixtures under `.agent_temp/x12-tests/`, cleans only its own fixtures and uses neither model credentials nor the network. Its simulated 1.2.0 manifest is a test fixture, not a claim that the release was tested. It proves the controller's branching, not an agent's ability to implement or review a real feature.

## 1. Prepare the trusted course repository

- Use a dedicated team case repo, with the existing course `.devcontainer/` at its root. Adjust its dependency step and the final checks for that application. AndThen's project root and the Git root must be the same directory for this kit.
- Commit the controller kit, the reviewed devcontainer configuration and the workflow on the **default branch** before dispatch. Put the template at `.github/workflows/x12-plan-to-pr.yml`; keep it as a template until the activation checks pass.
- Start with a single-container configuration in ordinary JSON, as in the course repo. The workflow's Python override builder intentionally does not parse JSONC or orchestrate Docker Compose. Adapt and rehearse another configuration separately.
- Use `init` to install the approved role agents into the **project** before preparing the plan. Do not rely on a runner account's unrelated personal plugins, agents, hooks or credentials.
- Finish the outer loop, commit every FIS and `plan.json`, approve C2 for that exact commit, then push a non-default branch under the configured prefix. A missing FIS, untracked bundle, dirty tree or incomplete plan is rejected.
- The workflow takes the branch, full lowercase 40-character source SHA and repo-relative `plan.json` path as data. Selecting the C2 checkbox attests to approval of that SHA. Workflow execution is restricted to the configured trusted repository and people allowed to dispatch it.

Do not enable fork/issue/comment events or run arbitrary contributor code on this VM. The supplied policy grants shell access inside a container that holds the course workload's model and GitHub credentials. It is a course team trust boundary, not a hostile-code service.

## 2. Prepare the VM and controlled configuration

Follow X11 first. The runner service account needs Docker access, Dev Container CLI and Python 3.10 or later. Docker-group access gives that account control of the VM. Keep its Azure login and host credentials elsewhere. Do not forward SSH agents or mount `/var/run/docker.sock` into the agent container.

Register a repository-scoped Linux x64 GitHub Actions runner with the additional label `x12`. Configure its service to remain running after SSH disconnects. The runner connects out to GitHub; it does not need a public webhook endpoint. Name its operator and cleanup owner.

On the VM, create these host paths for the actual runner service account. Substitute that account, rather than assuming it is your SSH account:

```bash
x12_runner_user='<runner-service-account>'
sudo install -d -o "$x12_runner_user" -g "$x12_runner_user" /var/lib/x12/state /var/lib/x12/host-jobs /opt/x12
sudo install -d -m 0755 /etc/x12
```

Install a reviewed, pinned AndThen 1.2.0 checkout from `develop` at `/opt/x12/andthen`, with its plugin at `/opt/x12/andthen/plugin`. Record the resolved commit and manifest version, and the tag when using a tagged release. The instructor's local installations do not provision or update this VM. Do not edit that checkout from a workload run. The container receives it read-only at `/opt/andthen`; `--plugin-dir` selects it explicitly. Each stage verifies that exactly one AndThen plugin loaded from that path and rejects plugin/MCP startup errors. CLI-local plugins replace same-name marketplace plugins, but managed `enabledPlugins` policy can prevent an override; check the actual startup metadata in the pilot.

Copy `config.example.json` to `/etc/x12/config.json` and edit the **host** copy:

- `repository`: the one permitted `owner/repo`, matching `X12_REPOSITORY` below.
- `base` and `branch_prefix`: the intended target and allowed source prefix. The template passes `--base main`; change that literal if the configured base differs.
- `plugin_dir`, `settings` and `state_dir`: keep the container paths shown in the example.
- `checks`: replace the example with the application's real build/test/lint/type-check commands as argv arrays, run from its root. Commands do not pass through a shell. Configure every gate needed by the approved work, including browser checks when required. No UI check is implied by `pytest`.
- `timeout_seconds`, `stage_budget_usd`, `max_budget_usd` and `max_fix_rounds`: explicit operational limits. The model CLI receives the lesser of its stage allowance and the remaining total. Startup, local checks and GitHub calls share the controller's runtime limit.
- Leave **`publish_enabled: false`** until source/version verification and the live rehearsal checks pass.

Configuration and control code are mounted read-only. Shared state is writable and outside the workload repo. Ensure the container's actual `remoteUser` UID can write `/var/lib/x12/state` through that mount; Dev Container CLI normally adjusts it to the host user, but the pilot must demonstrate this.

The workflow copies the full trusted devcontainer configuration into a per-job override and adds explicit mounts. It reuses the Dockerfile, Features and lifecycle setup; it does not build a second tool image. Relative build paths still resolve against the workload's original `.devcontainer/devcontainer.json`. Its mount probe rejects privileged containers, unexpected host bind mounts and writable controller/plugin/configuration mounts. Inspect the actual Docker result in the pilot, including named volumes, capabilities and environment.

## 3. Credentials and repository settings

Create these repository **variables**:

| Variable | Value |
|---|---|
| `X12_REPOSITORY` | The trusted `owner/repo` |
| `X12_GIT_NAME` | The course Git author name |
| `X12_GIT_EMAIL` | The course Git author email |

Create these repository **secrets** through the organisation's approved route:

| Secret | Scope |
|---|---|
| `X12_ANTHROPIC_API_KEY` | Approved model account and budget for this workload |
| `X12_GITHUB_TOKEN` | Only this case repo, contents read/write and pull requests read/write; add issues access only if the plan's agreed tracker mode requires it |

A course GitHub App installation token is preferable where the organisation already supplies one; its acquisition/refresh step depends on that organisation. The template expects a valid token in the named secret and does not implement token minting. Rehearse token lifetime, branch policy and required CI checks. Actions' default token is read-only in this template; it is not the publication token. `GITHUB_TOKEN` event behaviour and organisation approvals can affect follow-on checks, so verify the actual required checks on the pilot PR instead of assuming they ran.

`actions/checkout` uses `persist-credentials: false`. The trusted launch adds the repository-local HTTPS helper `!gh auth git-credential`; `GH_TOKEN` alone would authenticate `gh` but would not configure Git push. The helper contains no token. Credentials are passed only to `docker exec` through its inherited environment, after container setup and the mount check, rather than as literal argument values or Docker build inputs. Both `claude auth status` and `gh auth status` must succeed before execution.

The policy uses `dontAsk` and an explicit tool list. The controller adds push/PR/API deny patterns before the ship stage. These patterns help catch mistakes; they do not contain arbitrary shell scripts or prevent a process from reading credentials it has. X11's dedicated VM/container and trusted workload remain the boundary. Never use the kit in a container with unrelated personal or cloud credentials.

## 4. Dispatch and inspect

The workflow's required inputs are `branch`, `source_sha`, `plan` and the C2 checkbox. Leave **publish off** for the first real model pilot after verifying the remote container's pinned 1.2.0 installation. From an already prepared container, the equivalent invocation is:

```bash
python3 /opt/x12-control/labs/x12-plan-to-pr/run.py \
  --config /opt/x12-config/config.json \
  --branch feat/example \
  --sha '<approved-40-character-commit>' \
  --plan docs/specs/example/plan.json \
  --base main --c2-approved
```

This still uses the model, implements the plan and creates local commits. **`prepared` means all local gates passed and `ship` was not invoked. It is not a simulation or a published result.** Publishing requires both the host configuration switch and `--publish` (the workflow's publish checkbox). A prepared attempt is retained and cannot be silently replayed: inspect it, then prepare a new approved source commit/branch for the publication pilot.

The wrapper-specific schema in `run.py` asks the agent to project the skill's result into `PASS`, `FAIL` or `BLOCKED`, revision, lens verdicts and report paths. This schema is **not an AndThen API**. The controller also reads the actual plan, checks clean Git state and ancestry, parses the native confirmation report's revision/chain/verdict outside fenced examples, runs the configured checks itself and queries GitHub's PR metadata. CLI exit 0 or a reported URL alone cannot pass.

The final read-only review binds a clean code SHA. The controller copies its native report into `<plan-dir>/x12-review-evidence/<reviewed-sha>.md` and commits only that new file. Real final checks run after this evidence-only commit. The PR must disclose the reviewed SHA, that subsequent documentation commit and any `ship` metadata commits, link the snapshot and state the actual check results. Keep the plan bundle and design folders; `ship` receives those instructions explicitly.

## 5. Failure, retention and duplicate handling

- GitHub concurrency serialises jobs for a repository/branch without cancelling an active run. The shared state mount adds a local branch lock across containers on this VM.
- Each source SHA/branch/plan has a durable attempt record under `/var/lib/x12/state/runs/<key>/status.json`. A completed published duplicate returns its existing result without invoking another agent. A failed, interrupted or prepared attempt blocks a silent rerun; inspect its retained workspace and make a new approved source commit before starting another attempt. This kit does not automatically resume partial agent work.
- A pre-existing PR for the source branch is a stop condition. Before `ship`, the remote source tip must still equal the approved start SHA and no PR may have appeared. The controller never force-pushes.
- There is still a check/publish race because `ship` owns the push and PR creation. Normal Git fast-forward rejection protects divergent remote history, but the wrapper cannot supply an atomic compare-and-publish guarantee without support from `ship`. Rehearse its behaviour when the branch advances during shipping. Keep one writer per branch.
- The workflow stops and retains this job's container after normal completion or a trapped cancellation. An `always()` stop step is a second backstop. Its workload directory, Claude configuration volume, state and per-job host records remain. Cancelling the Actions job is intentionally different from disconnecting an SSH client; a canceled job must not leave an agent shipping in the background. Rehearse real Docker cancellation propagation, including the Actions termination grace period. Host loss or forced termination can prevent a final status write; an existing `running`/`shipping` record then blocks a replay for human inspection.
- Raw agent stdout/stderr stay on the VM for the operator. They may contain source and model output; inspect/redact before sharing. The uploaded artifact contains only this unique `X12_JOB` ID's status, native Markdown review reports and final-check logs, plus its container setup/inspection records. Selection does not rely on `workspaceFolder`, which a repo can fix to the same path across jobs. Check selected reports too for sensitive content.
- A failure during or after `ship` can leave a pushed branch or PR even though the job reports `blocked`. Inspect GitHub and the local ledger before retrying. The controller marks `published` only after checking one open PR in the expected repository with the expected base, branch and final head SHA, the retained plan, clean tree and post-ship checks.
- Archive the owned work and proof before the operator removes that job's container, unique workspace and volumes. Remove only resources identified in its saved Docker inspection and job directory. Do not sweep the VM while another team/job is using it. X11's provider cleanup still applies.

## Activation checklist with 1.2.0 from develop

- [ ] Pin the `develop` commit and read its `ship` skill and plugin documentation. Confirm the remote installation matches that source. Record commit, manifest version and Claude Code version, plus a tag when using a tagged release. The installed local skill already confirms the publication mandate; actual publishing, keep instructions and failure handling still need the live pilot.
- [ ] Run the offline suite again and validate the copied workflow with actionlint/ShellCheck, including the custom `x12` label. Pin reviewed action revisions according to the organisation's policy before activation.
- [ ] Rehearse the real VM service account, full devcontainer build, mounts, UID/state writes, plugin `system/init` metadata, authentication, Git helper and all application checks. This kit's offline suite does not prove those integrations.
- [ ] Run one bounded plan with publication disabled. Compare every structured projection with its native reports. Confirm all three lenses ran, the native report parser matches 1.2.0 and the committed evidence contains the reviewed SHA.
- [ ] In a disposable pilot branch, enable host publication and the dispatch checkbox. Confirm `ship --auto` creates the actual expected PR, keeps the plan/design folders and reports real checks. Have the facilitator read C4 on GitHub; merging remains human.
- [ ] Run a red check, a semantic `BLOCKED`, an unavailable lens/plugin, an exhausted review loop, a duplicate dispatch and a remote-advance case. None may trigger `ship` before its gates; inspect any partially published shipping failure explicitly.
- [ ] Disconnect the client during a live job and show that the runner finishes and preserves its result. A disconnected client is different from a stopped/deallocated VM.
- [ ] Cancel a real Actions job during execution and during shipping. Confirm only its container stops, its work/volume survive, no background process continues publishing and another team's container is unaffected.
- [ ] Verify required PR checks actually run with the chosen token and organisation policy. Set evidence retention, quota ownership and cleanup responsibility, then offer X12.

## References

Updated 2026-11-15: 1.2.0 is available on `develop` and installed locally in Claude Code and Codex, as reported by the owner. Its publication mandate is source-checked; live publication and the complete remote chain remain untested.

- [Claude Code headless execution](https://code.claude.com/docs/en/headless): structured output in `structured_output`, `system/init` plugin/error fields and noninteractive execution.
- [Claude Code CLI reference](https://code.claude.com/docs/en/cli-reference), [permission modes](https://code.claude.com/docs/en/permission-modes), [plugin name conflicts](https://code.claude.com/docs/en/plugins/loading#name-conflicts): `--plugin-dir`, `--json-schema`, `--max-budget-usd`, `dontAsk` and managed plugin precedence.
- [Dev Container CLI](https://github.com/devcontainers/cli), [CLI source](https://github.com/devcontainers/cli/blob/main/src/spec-node/devContainersSpecCLI.ts), [configuration source](https://github.com/devcontainers/cli/blob/main/src/spec-node/configContainer.ts): `up`, `--override-config` and original config-path resolution. CLI `--mount` does not accept `readonly`; the template uses Docker `runArgs` mounts instead.
- [Manual workflow dispatch](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow), [self-hosted runner communication](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), [GitHub token behaviour](https://docs.github.com/en/actions/concepts/security/github_token).
- [AndThen plugin contracts](https://github.com/IT-HUSET/andthen/blob/develop/plugin/README.md), [plan schema](https://github.com/IT-HUSET/andthen/blob/develop/plugin/references/plan-schema.md), [native review report template](https://github.com/IT-HUSET/andthen/blob/develop/plugin/skills/review/references/report-template.md). The original 1.1.0 contracts informed execution/review parsing. The installed 1.2.0 `ship` skill confirms the publication change; the activation checks must still exercise it and check the parsers against the pinned revision.
