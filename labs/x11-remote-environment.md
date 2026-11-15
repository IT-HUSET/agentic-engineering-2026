# X11 – Remote agent environment

**What you do:** move the agent off your laptop. You build a remote VM and container from your repo, start a run, disconnect, reconnect to the result, and check what the agent can and cannot reach. This is an individual exercise: each participant has their own VM, container and sign-ins.

**Why it matters:** a long run that dies when your laptop sleeps is not unattended, and an agent environment nobody can describe is one nobody can trust. When the repo can rebuild the environment, anyone on the team can.

**What you have at the end:** the environment configuration and a short runbook in your repo, and a log that proves the run survived a disconnect, the boundary checks held, and a second machine rebuilt the environment.

> Azure is the reference provider, charged to the course organiser's subscription. Hetzner is an alternative with the same checks. Provider accounts and payment arrangements are prepared before the course.

## When to pull it

Pull X11 when one of these is true for you:

- **A useful run depends on your laptop staying connected.**
- **Nobody can say what the agent can reach:** which host files and credentials it sees.

**Status:** four individual VMs are built, tested and deallocated ([preparation record](x11-remote-environment/README.md#public-preparation-record)). There is no automatic daily stop. Hetzner is untested.

## Input

- A repo and branch you may run in the chosen cloud. Start with the course repo if your own stack is not ready.
- The repo's `.devcontainer/`, including `devcontainer.json`, `Dockerfile` and `setup.sh`; copy the course folder to a case repo and adapt its dependency step if needed.
- An SSH key (preferably one you generate, of which the facilitator receives only the public half) and your row in [participant access](x11-remote-environment/access.md). On the main path you need no Azure account, RBAC role or Entra invitation: the facilitator deploys one VM per participant in the shared `agentic-engineering-2026` course resource group. SSH is restricted to an approved public source address: initially the facilitator's network, then the venue's network for the course.
- Your own Claude sign-in (IT-HUSET team seat or your own plan, D11) and a fine-grained GitHub token for the one course repo. Azure pays only for the VMs; model usage counts against your plan limits.
- A small agent task with a concrete result and a real test command. For example, one already-approved story from your case, or a documentation correction plus the unchanged `todo-app` tests.
- The [preparation kit](x11-remote-environment/README.md), including `azure.bicep` and `cloud-init.yaml`.

## Output

Keep the environment configuration and a short runbook in your repo. Keep the following proof in your log outside the agent workspace: repo commit, host/container/tool versions, test result, disconnect result (copied out of the repo after the check, step 5), actual boundary checks, second-machine result, cost owner and cleanup confirmation. Do not save access tokens or private keys in either place.

## Steps

### 1. Predict the boundary

Draw two boxes before you run anything:

- **VM host:** Ubuntu, Docker, Node and Dev Container CLI. A human provisions and manages it.
- **Agent container:** your repo's existing development environment. The agent, its tools and its tmux session run here.

Write down whether the agent should be able to read `/opt/x11-host-only.txt` on the host, use the host Docker socket, or act in your Azure subscription. Predict which of these the configuration enforces, and how you will test it. Name what a container still exposes: the mounted repo, its own credentials and outbound network access.

<details>
<summary>Reference boundary</summary>

The host marker and `/var/run/docker.sock` are not mounted into the container. There is no Azure CLI login or VM managed identity. The agent can still read everything mounted into its container, including its own authenticated tools, and this template does not restrict outbound traffic. The NSG restricts incoming connections; it is not an egress policy. A successful host-file probe does not prove protection against every container escape.

You can administer your own VM and Docker through its `course` account, outside the agent container. The identical username on another participant's VM is a separate account. Each participant gets an individual VM, container, SSH key and model sign-in. Multiple sessions on your own VM are allowed; coordinate their branches/worktrees and files if they edit concurrently.

</details>

### 2. Connect

Your facilitator has provisioned and prebuilt your VM ([kit steps 1–3](x11-remote-environment/README.md#1-prepare-the-one-local-access-file); the Bicep template and preparation record show how). Follow [participant access §1–2](x11-remote-environment/access.md#1-your-ssh-key): get your key in place, verify the host fingerprint and connect without agent forwarding. Do not log in to Azure from the VM or paste cloud-management credentials into an agent session.

### 3. Start the same development environment

**Prepared environment:** the facilitator has already cloned and built your environment. **VM host:** enter the prepared repo path in the access instructions, check the recorded commit and inspect the existing container:

```bash
cd ~/course-repo
git rev-parse HEAD
docker version
node --version
devcontainer --version
docker ps
```

Continue below with the mount inspection and your personal sign-ins. Do not clone into an existing `course-repo` or blindly recreate the prepared container. If it is missing or the recorded commit differs, ask the facilitator to resolve that before continuing.

<details>
<summary>Building from scratch or on the rebuild VM</summary>

On a new VM, first run `sudo cloud-init status --wait`, check its exit status and resolve any bootstrap error. Reconnect after your account is added to the Docker group.

**VM host:** clone the permitted repo into a new folder. Replace the example URL and commit with your own; the second VM must use the same recorded commit. For a private repo, use the prearranged project-scoped clone route and remove any temporary host credential afterwards. Never put a token in the URL.

```bash
git clone https://github.com/<owner>/<repo>.git course-repo
cd course-repo
git switch -c x11-course <recorded-commit>

docker version
node --version
devcontainer --version
devcontainer up --workspace-folder "$PWD"
```

</details>

Use the whole configuration. A plain `docker build .devcontainer` would omit the Features and `postCreateCommand`. The course setup script warns and continues when an install fails, so read its output; `up` succeeding is not the final gate.

Before signing in, exit the container shell if needed and inspect the running container from the **VM host**. For the prepared environment, run `docker ps` on the VM host and identify your repo's running container; a fresh build also returns its ID in the successful `up` output:

```bash
docker inspect <container-id> --format '{{.HostConfig.Privileged}} {{json .Mounts}}'
```

Expect `false`, the workspace mount and the declared Claude configuration volume. Investigate unexpected mounts. Do not accept host `~/.ssh`, cloud credentials, the Docker socket or a privileged container. The CLI path does not require VS Code's automatic git-credential or SSH-agent forwarding.

Enter the container, then keep all following agent commands there:

```bash
devcontainer exec --workspace-folder "$PWD" bash
```

**Container:** sign in as yourself to your chosen agent inside your own container. For Claude Code use `claude auth login`. Sign in to GitHub with a **fine-grained token for the one course repo** (Contents and Pull requests read/write), as in [access.md §3](x11-remote-environment/access.md#3-sign-in-inside-your-own-container), not a plain `gh auth login`, which grants `repo`, `read:org` and `gist` over all your repositories. Keep the token out of shell history, tracked files, a Dockerfile and cloud-init. Verify `gh auth status`, the agent's sign-in and the AndThen installation. Then run:

```bash
uv run check.py
```

A case repo uses its own setup check and real build/test commands. In the course repo, `check.py` must end `GREEN`; repair missing tools or authentication first. Before changing files, create your work branch from the prepared `x11-course` checkout: `git switch -c x11-work`.

<details>
<summary>Do we need another image?</summary>

The VM boots an Ubuntu image; the agent runs the existing dev container. These are different layers. Dockerfile, Features and setup remain the single development-tool definition. We do not create a custom Azure image containing another copy of the tools. The shared configuration can later be prebuilt into a container registry if measured startup friction justifies it; sign-ins remain outside that image.

</details>

<details>
<summary>Optional: preview the course app through SSH</summary>

**Container, in another terminal:** start the app listening on the container interface:

```bash
cd todo-app
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**VM host:** find the container's private bridge address, using its ID from `devcontainer up`:

```bash
docker inspect <container-id> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

**Your own computer:** copy that address into the forwarding target below. Use the key and VM IP from the preparation kit:

```bash
ssh -i "$x11_private_key" -o ForwardAgent=no -N -L '127.0.0.1:8000:<container-private-ip>:8000' "course@$x11_ip"
```

Open `http://localhost:8000` locally. Leave the tunnel open while using the app. No public app port or Docker port publication is needed. After a rebuild, resolve the new container address again. The app command is for `todo-app`; a case uses its own server and port.

</details>

### 4. Try to cross the boundary

**VM host, in another SSH terminal:** `cat /opt/x11-host-only.txt` must show the harmless marker. **Container:** run:

```bash
test ! -e /opt/x11-host-only.txt && echo 'host marker is not mounted'
test ! -S /var/run/docker.sock && echo 'Docker socket is not mounted'
test -z "${SSH_AUTH_SOCK:-}" && echo 'no forwarded SSH agent'
test ! -d "$HOME/.azure" && echo 'no Azure CLI credential directory'
gh auth status
```

`gh auth status` must show your fine-grained `github_pat_` token with none of the `repo`, `read:org` or `gist` scopes. Also try `gh api repos/<owner>/<a-private-repo-you-did-not-grant> --jq .name`: it must fail.

Record exit status and output. Also have the facilitator show that the VM has no managed identity and that the NSG permits SSH only from the approved `/32`. Attempt SSH from a second, unapproved source network: it should fail. Keep existing access open while testing; repair the rule rather than widening it to all addresses.

These are probes for specific configuration mistakes, not proof of complete isolation. Ask the agent to explain the remaining access it has, then compare its answer against mounts and provider configuration rather than accepting self-report.

### 5. Disconnect and return to the result

Start with a deterministic job so that an agent waiting for permission cannot obscure the persistence check. **Container, from the repo root:** write a small wrapper that retains its log and exit status. The deliberate 15-second delay gives you a window to disconnect before the real check starts; it is part of this probe, not a performance measurement.

```bash
mkdir -p .lab-output/x11
cat > .lab-output/x11/check.sh <<'SH'
#!/usr/bin/env bash
{
  date -u '+started %Y-%m-%dT%H:%M:%SZ'
  sleep 15
  uv run check.py
  x11_exit=$?
  date -u '+finished %Y-%m-%dT%H:%M:%SZ'
  printf 'check exit=%s\n' "$x11_exit"
  printf '%s\n' "$x11_exit" > .lab-output/x11/check.exit
} > .lab-output/x11/check.log 2>&1
exit "$x11_exit"
SH
tmux new-session -d -s x11-proof
tmux send-keys -t x11-proof 'bash .lab-output/x11/check.sh' Enter
```

For a case repo, replace `uv run check.py` with its real deterministic build/test command before starting. The wrapper runs in an existing tmux shell, which stays open when it finishes. Exit the container shell and close SSH while the probe is running. Reconnect, return to the repo folder on the **VM host**, and attach:

```bash
devcontainer exec --workspace-folder "$PWD" tmux attach -t x11-proof
```

**Container:** show `.lab-output/x11/check.log` and `cat .lab-output/x11/check.exit`. Expect the completed checks and exit `0`, with the completion timestamp after you disconnected. If it finished before disconnect, repeat the probe. The files sit in the mounted repo, at `~/course-repo/.lab-output/x11/` on the VM host. After the check, `scp` them to your own computer for your proof log, and do not commit them.

Then start your bounded agent task in a separate tmux session:

```bash
tmux new -As x11
```

Give the agent the agreed task, test command and stopping condition. Use the AndThen plan/story you already approved when the task warrants it. Keep permission prompts and the course's existing review gates; a remote VM is not a reason to turn them off. Detach with `Ctrl-b`, then `d`, exit the container shell and close SSH again. On return, use `devcontainer exec --workspace-folder "$PWD" tmux attach -t x11` from the repo folder on the **VM host**.

Show the task's result and run its real checks. If the agent was waiting for input, record that and distinguish it from a stopped process. The test is persistence across **client disconnect**, not VM stop or reboot. Do not connect a second editor during these checks. If you later use VS Code, repeat them: closing an editor can stop a container under its lifecycle settings.

### 6. Rebuild on a second VM

Save and push the work you need to retain. The facilitator rebuilds one participant at a time, following the [rebuild instructions](x11-remote-environment/README.md#5-rebuild-proof-and-final-cleanup): your turn gets `x11-pNN-rebuild`, deployed with your public key, and it is deleted before the next participant's starts. Transfer the source bundle (or clone a published case commit) with your own key as the kit describes, then repeat steps 3–4 with fresh sign-ins. Do not copy a disk, credential cache or Docker volume from the first VM.

Compare the test results. Any missing manual instruction belongs in your runbook or setup configuration. If your case needs changes beyond the supplied skeleton, use the normal `plan → exec-plan → review --fix` loop to make those changes and rerun this proof.

<details>
<summary>What counts as a rebuild?</summary>

A fresh host plus the recorded repo/configuration and explicit sign-ins produces a working environment. Resuming the original VM or restoring its snapshot only proves recovery of existing state. Mutable package versions mean this exercise proves a functional rebuild, not an identical binary image.

</details>

### 7. Close the resources

Save code and proof outside the VMs and tell the facilitator that no job is active. Deallocation, group deletion and the Hetzner equivalent are in the kit's [operate](x11-remote-environment/README.md#4-operate-during-the-course) and [cleanup](x11-remote-environment/README.md#5-rebuild-proof-and-final-cleanup) sections.

## Verify

- [ ] The repo and runbook name both layers and reuse the complete `.devcontainer/` configuration.
- [ ] Real build/tests and the setup check pass inside the agent container.
- [ ] The host marker, Docker socket and forwarded SSH agent are unavailable inside it; cloud-management credentials and VM identity are absent, and `gh auth status` shows a one-repo token.
- [ ] SSH works from the approved network and fails from an unapproved one. Outbound network access is described accurately.
- [ ] The deterministic check completes after disconnect with a retained log and exit `0`; the bounded agent task also survives closing SSH, and its returned result is checked.
- [ ] Your own rebuild VM (`x11-pNN-rebuild`) reaches the same functional checks without copying hidden state from the first.
- [ ] Your row in the public access table and own SSH key reach only your assigned VM, and your model sign-in is inside your own container.
- [ ] Work is saved outside the machines, billing ownership is known, and the facilitator confirms removal of the shared course resources after the course.

## Sizing check

Did a remote VM solve a real dependency on a laptop or a missing execution boundary? A supervised task that already runs comfortably in the local dev container may need no remote infrastructure. A short-lived course setup may be covered by Codespaces. Build a custom host image or platform only after this small environment shows a concrete bottleneck. Record one sizing-log line and, if appropriate, continue with [X5's unattended runs](x5-parallel-autonomy.md#going-further). After X5, [X12](x12-plan-to-pr.md) prepares a remote plan-to-PR job for AndThen ≥1.2.0, with its own release check and live rehearsal.

<sub>Stuck? Describe the symptom: “the container starts, but `check.py` reports missing tools” or “the job disappears after disconnect”. Keep the failing command and exit status.</sub>
