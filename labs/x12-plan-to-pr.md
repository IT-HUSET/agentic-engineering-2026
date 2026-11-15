# X12 – From pushed plan to PR

**What you do:** push an approved plan and let a GitHub Actions workflow on your own X11 VM turn it into a verified pull request, or stop with a saved reason. It runs `exec-plan --auto`, a bounded review/fix loop and `ship --auto`.

**Why it matters:** after X5 and X11 you can run a plan unattended, but you still start each step by hand. Automation is only worth having if you can explain exactly why it stopped.

**What you have at the end:** a PR for your own review, or a run record that says why the run stopped. C2 approval and the C4 review stay yours.

## When to pull it

You have done X5 and X11, but still start implementation, review and delivery by hand. Start with one small plan run sequentially.

**Status:** not offered yet. See the [kit status](x12-plan-to-pr/README.md#status).

## Input

- Your own X11 VM with [X11's checks](x11-remote-environment.md) passed, and [X5's unattended-run policy](x5-parallel-autonomy.md#going-further).
- Your own repo with the course devcontainer, and your own Claude sign-in and fine-grained GitHub token from X11.
- A small plan with no open scope decisions, committed with its FIS files and requirements, a green baseline and concrete check commands. Use a server-side or CLI slice; a UI plan also needs browser evidence.
- The runner and kit on your VM ([kit README](x12-plan-to-pr/README.md), sections 2–3). If your facilitator prepared them, you only store your secrets.

The runner is yours: your VM, your repo, your token. Stages run in Claude Code's auto mode, where a classifier reviews each action. A bypass mode is never used.

## Steps

```text
you:    plan -> approve C2 -> commit and push
runner: validate input -> exec-plan -> review/fix -> full checks -> ship -> PR
you:    read the run record -> review the PR (C3/C4) -> decide on merge
```

### 1. Set up your runner and secrets

Once, on your VM and repo:

- Register a self-hosted runner for your repo with the label `x12`.
- Run `claude setup-token` yourself and store its output as the repo secret `X12_CLAUDE_CODE_OAUTH_TOKEN`. Store your fine-grained GitHub token, limited to this repo, as `X12_GITHUB_TOKEN`. Never put a token in a file or a prompt.
- Put your repo, base branch and the commands that prove your app in `/etc/x12/config.json`.
- Commit the workflow template to your default branch.

### 2. Push an approved plan

Commit the whole plan bundle on a `feat/` branch, approve C2 for that commit and push. Write the commit SHA and plan path in your gate log. Name what should stop the job: missing credentials, `BLOCKED`, a failed check, a CRITICAL or HIGH finding left open, a changed remote branch.

### 3. Start the workflow

In your repo, open Actions, choose **X12 plan to PR** and **Run workflow** with your branch, the full 40-character SHA and the plan path. Tick the C2 box and, once your facilitator's rehearsal has passed, **publish**. Without publish the run ends `prepared`: every gate passed and no PR exists.

### 4. Read the run record

When the job ends, download its `x12-…` artifact and open `status.json` under `evidence/`. Read `status`, `reason`, the stage list, `reviewed_sha` and `pr_url`, then the review report next to it. Answer: where did it stop or finish, and is that what you predicted?

### 5. Try one failure path

Pick one on a throwaway branch. Note what happened and where the evidence is.

| Probe | Expected |
|---|---|
| Dispatch the same branch, SHA and plan again after the PR exists | A stop before any agent call. No second PR |
| Dispatch an earlier commit of your branch, not its tip | Stops before `ship`; nothing is overwritten |
| Cancel the job while it runs | The container stops, your work stays on the VM and `status.json` stays `running` |

### 6. Review the result as a person

Open the PR. Rerun one story's proof command for C3. For C4, trace the outcomes to executed proof and read the review and the PR's intent, risks and door type. A green job and an open PR approve nothing. Record one change to your unattended-run policy, then clean up as X11 describes.

## Verify

- [ ] The approved SHA, plan path and target branch were recorded before you started.
- [ ] You can name the stage and the reason from `status.json` alone.
- [ ] The PR keeps the plan and review evidence, and every story has executed proof.
- [ ] Your failure probe stopped before `ship` or left no duplicate.
- [ ] You decided on C3, C4 and merge yourself.

## Sizing check

This earns its place when you repeatedly move an approved plan through the same remote steps. For one story, X5's terminal run may be enough. One runner, one sequential job and a manual start is the whole setup.

## Going further

Add a push trigger or a webhook only after the manual path passes. Decide what signals approved and ready, bind it to the approved commit, and test duplicate delivery and the job's own pushes.

## References

- [GitHub: manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow), [self-hosted runners](https://docs.github.com/en/actions/reference/runners/self-hosted-runners).
- [Claude Code: headless](https://code.claude.com/docs/en/headless), [permission modes](https://code.claude.com/docs/en/permission-modes), [authentication](https://code.claude.com/docs/en/authentication#generate-a-long-lived-token).
- AndThen at `v1.2.0`: [`exec-plan`](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/skills/exec-plan/SKILL.md), [`review`](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/skills/review/SKILL.md), [`ship`](https://github.com/IT-HUSET/andthen/blob/v1.2.0/plugin/skills/ship/SKILL.md).
