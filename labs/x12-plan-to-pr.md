# X12 – From pushed plan to PR

**What you do:** let a pushed, approved plan become a verified pull request without anyone carrying it between sessions. A GitHub Actions workflow on your X11 environment runs `exec-plan --auto`, a bounded review/fix loop and `ship --auto`, and stops with a clear reason when something fails.

**Why it matters:** after X5 and X11 you can run a plan unattended, but someone still starts each step by hand. Automation is only worth having if you can explain exactly why it stopped.

**What you have at the end:** a version-controlled workflow with your team's limits and checks, a run record that ties the input commit and plan to each stage's result, and either a PR to the expected base or preserved logs that say why the run stopped. C2 approval and the C4 review stay human.

## When to pull it

Pull X12 when this is true for your team:

- **You have done X5 and X11,** but still start the implementation, review and delivery steps by hand.

Start with one small plan run sequentially. Independent stories and parallel worktrees are not needed here.

**Status, 2026-11-15: AndThen 1.2.0 is available on `develop`.** Its installed `ship` skill confirms that `--auto` authorises branch push and PR creation. Pin the source revision and verify the remote installation, then complete the live rehearsal before this lab is offered. Offline tests exercise the orchestrator with fake tools; they do not prove that a model, the container wiring or GitHub publishing works. Publishing is disabled in the example configuration.

## Input

- [X5's unattended-run boundary and policy](x5-parallel-autonomy.md#going-further), plus an [X11 remote environment](x11-remote-environment.md) that has passed its own checks. Azure is the main path; Hetzner uses the same job contract.
- A trusted course repo and a pushed feature branch. Commit the complete plan bundle, its FIS files and referenced requirements. **A human approves C2 before the job starts.** Record the approved commit SHA and plan path in the team's gate log. The job cannot verify that a checkbox represents a real conversation.
- A green baseline and concrete full-check commands. Use a small case plan with no unresolved scope decisions, initially a server-side or CLI slice. A UI plan also needs actual browser evidence. The facilitator may supply X5's prepared workload, copied to the course repo and reviewed for C2; X5's local clones without a remote are not ready for this lab.
- A runner restricted to the course repo, model access, project-scoped GitHub access, git identity and a pinned AndThen plugin directory. Live execution requires AndThen of at least 1.2.0 at a recorded source revision; 1.2.0 from `develop` is available for rehearsal. Do not edit a version string to bypass the check.
- The [preparation kit](x12-plan-to-pr/README.md), with a workflow template, configuration, permission settings, orchestrator and offline tests.

## Output

- A version-controlled workflow and the team's chosen limits, checks and publishing policy. Credentials stay in the approved secret store.
- A run record tying the input repo, branch, SHA and plan to stage results, actual check output and the final PR or stop reason.
- On success: a PR to the expected base, with the plan bundle and review evidence retained for the course's artifact review.
- On failure: preserved logs and owned work, with no automatic publication from the failed pre-ship gates. If publication itself partially succeeds, investigate GitHub before retrying.

## Steps

### 1. Draw the handoff and the stop conditions

Draw your outer loop and inner loop before editing the template:

```text
human: clarify/design -> plan -> approve C2 -> commit and push
remote: validate input -> exec-plan -> review/fix -> full checks -> ship -> PR
human: inspect evidence -> approve C3/C4 -> decide whether to merge
```

Write down the exact source commit, target base and plan path. List the conditions that must stop the job: missing tools or credentials, `BLOCKED`, incomplete story proof, a failed final check, a failing final review, an exhausted limit or a changed remote branch. Name who receives the stopped run and where its work remains.

<details>
<summary>Reference boundary</summary>

The runner is a service on the VM host, outside the agent container. It starts a separate workspace/container per job using the repo's devcontainer configuration. The agent receives the workload and the credentials deliberately assigned to it; it receives no host Docker socket, SSH agent or Azure management login. A container is not an approval of arbitrary fork code: the main exercise accepts only the team's trusted repo and branch.

The orchestrator and its configuration come from the trusted control revision, not from the branch the agent is implementing. A reviewed start SHA pins the input. A final remote-tip check detects intervening pushes, but does not make `ship`'s subsequent push atomic. Test the pinned version's behaviour for a concurrent push and never permit force-push as a workaround.

</details>

### 2. Prove the orchestration offline

From the participant repo root:

```bash
python3 -m unittest discover -s labs/x12-plan-to-pr -p 'test_*.py' -v
```

Read the tests as examples of the job contract. Find the case where the agent exits successfully but reports `BLOCKED`, and the case where a real check exits non-zero. Predict whether either can reach `ship` before running them.

Keep the output in your run log, labelled **offline, fake tools**. These tests need neither a model account nor an external GitHub repo.

### 3. Prepare the remote job without publishing

Follow the [kit setup and activation checklist](x12-plan-to-pr/README.md). Configure the actual repo, plugin path, branch policy, full-check commands, limits and artifact storage. Keep publishing disabled while you inspect the wiring.

Install the workflow template on the course repo's default branch. Use `workflow_dispatch` first, with explicit branch, source SHA and plan inputs. Check that the workflow selects the intended self-hosted runner and that the code checkout matches the approved SHA. The workflow must use a fresh writable feature branch, rather than a detached checkout or the developer's interactive X11 workspace.

Inspect actual container mounts and exercise the headless permission rules. Implementation and review need their own allowed operations; publishing also needs GitHub network access and write permissions. X5's network-disabled configuration cannot publish unchanged. Do not solve denied tools by enabling unrestricted access to the host.

### 4. Run the bounded inner loop

The orchestrator starts a fresh agent invocation for each stage. The skill sequence is:

```text
/andthen:exec-plan --auto <plan-directory>
/andthen:review --mode code,gap,security --fix --auto <plan-path>
/andthen:review --mode code,gap,security --auto <plan-path>
```

The separate review without `--fix` confirms the result of the fixes. Repeat only within the chosen limit, initially at most three fix rounds. Run the configured full checks against the final tree independently of the agent's prose summary. A wrapper's structured stage result is not a new native AndThen artifact format; compare it with the actual plan and review reports.

With 1.2.0 available on `develop`, the facilitator verifies the pinned source and remote installation and completes the live rehearsal. Only then enable publication in the trusted configuration and trigger a publishing run. The last skill call uses the same plan:

```text
/andthen:ship --auto <plan-path> Keep the plan bundle and design folders. Retain the committed review evidence. Target the configured base branch. Open a PR; do not merge it or force-push.
```

The kit passes this mandate to `ship`; it does not replace it with a separate PR publisher. Check the actual PR's repo, head, base and revision after the call. A reported success without that PR is a failed publication-contract check.

### 5. Try the failure paths

Use a throwaway course branch and the kit's offline fixtures first. Then repeat the relevant checks with real tools during rehearsal:

| Probe | Required observation |
|---|---|
| Old or prerelease AndThen | No agent stages or publication; the version failure is explicit |
| Agent exits 0 but returns `BLOCKED`, or unusable stage output | Stop before `ship`; the reason and log remain |
| Final check fails | No `ship`; the failing command and output are recorded |
| Review remains failing at the limit | No `ship`; reports and changes remain available |
| Same approved input is dispatched twice | No repeated publication or duplicate PR |
| Someone advances the remote feature branch | Stop before `ship`; preserve both people's work, without force-push |
| Client disconnects | The runner continues; inspect its status and result after reconnecting |
| Actions job is cancelled | Its agent process stops with its job container; work remains available for inspection |

Do not call a VM shutdown a disconnect test. Disconnecting the SSH client should leave the job running; cancelling the Actions job should stop it. After a cancelled or partially published run, inspect both the saved workspace and GitHub before deciding how to resume. A stopped run does not authorise changing the plan or merging its result.

### 6. Review the result as a person

Open the PR and its evidence with your facilitator. Run a story's proof command again for C3. For C4, trace the outcomes to executed proof, inspect the plan-level review and read the PR's intent, risks and door type. A green Actions job and an open PR do not approve either gate.

Record one change to the team's unattended-run policy based on the failure probes. Clean up per-job containers/workspaces only after code and evidence are saved, then remove temporary runner access and follow X11's resource cleanup procedure.

## Verify

- [ ] The approved source SHA, plan path, checks and target branch are recorded before execution.
- [ ] Offline orchestration tests pass and are labelled separately from live results.
- [ ] Live execution uses the pinned plugin and the intended remote container, with measured tool versions and access checks.
- [ ] Every required story has executed proof; the final review passes and configured full checks are green.
- [ ] Duplicate and changed-branch probes prevent a second or stale publication.
- [ ] The successful PR retains the plan and review evidence and points to the expected base and source result.
- [ ] Stopped runs preserve their reason, reports and owned work for inspection.
- [ ] The facilitator approves C3/C4; merge remains a human decision.

## Sizing check

This setup earns its place when the team repeatedly moves an approved plan through the same remote steps. For a single story, X5's terminal invocation may be enough. Start with one runner, one sequential job and a manual dispatch. Do not add a queue service, dashboard, Kubernetes cluster or custom image pipeline to this lab.

## Going further

After the manual-dispatch path passes, add an intentional push trigger or a webhook. Define what signals **approved and ready**, bind that signal to the approved commit and carry the same input contract into the job. Test duplicate delivery, cancellation and the job's own pushes. Explain why an ordinary edit to the plan does not unexpectedly start another implementation.

## References

- [GitHub: manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow), [self-hosted runner requirements](https://docs.github.com/en/actions/reference/runners/self-hosted-runners), [workflow concurrency](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency).
- [Claude Code: headless execution](https://code.claude.com/docs/en/headless), [permissions](https://code.claude.com/docs/en/permissions).
- AndThen: [`exec-plan`](https://github.com/IT-HUSET/andthen/blob/develop/plugin/skills/exec-plan/SKILL.md), [`review`](https://github.com/IT-HUSET/andthen/blob/develop/plugin/skills/review/SKILL.md), [`ship`](https://github.com/IT-HUSET/andthen/blob/develop/plugin/skills/ship/SKILL.md). Verify the pinned 1.2.0 source and remote installation before activation; `develop` may move.
