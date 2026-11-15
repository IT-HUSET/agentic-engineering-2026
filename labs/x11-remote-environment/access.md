# Your X11 remote environment

Each participant has their own VM, container, SSH key and model/git sign-ins. The facilitator prepares everything except your personal sign-ins. You need no Azure account, Azure CLI or Entra invitation. Never use another participant's key or VM.

There is no automatic daily shutdown. The facilitator starts the VMs before the course and leaves them running while jobs need them. Manual deallocation happens only after you have saved your work and confirmed that no jobs are active. Files survive a stop; running tmux/agent jobs do not. All course resources are removed after everyone has saved their work.

## Connection table

Verified through Azure management on 2026-11-15. The facilitator rechecks this table after any VM replacement. Public IPs, SSH host fingerprints and public host keys may be recorded here; **private keys and tokens never belong here**.

| Your ID | VM | Public IP | Trusted ED25519 host fingerprint |
|---|---|---|---|
| p01 | x11-p01 | `135.225.54.185` | `SHA256:QEZhegV4E7PG4lOkdMFC3aJTm5c+tnimtYh7fyWeL2c` |
| p02 | x11-p02 | `135.116.85.42` | `SHA256:Mxltd08Jd9ZC96+HYzPwsv42zR3SEXyVvEHf6rbJRM0` |
| p03 | x11-p03 | `135.225.54.218` | `SHA256:MR3N7acY+weXW2X77TfBsEAJqcOFoU4OhWJ17aEgYEs` |
| p04 | x11-p04 | `57.174.209.89` | `SHA256:oXluzXb8jp/ku3BI/juNQys0GaG9tNdpcU4mQorTSpQ` |

- Linux username: `course` on your own VM.
- Prepared repo path: `/home/course/course-repo`.
- SSH key filename: `agentic-engineering-2026-p01` for p01, and correspondingly for the other IDs.
- Prepared source URL/commit: see the [public preparation record](README.md#public-preparation-record).

## 1. Receive and store only your key

The facilitator sends your individual temporary private key through the approved personal channel. Do not send it to the group, commit it, put it on the VM or paste it into an agent prompt. Keep it in your own computer's `.ssh` directory under the filename above. These temporary keys initially have no passphrase; you may add one locally with `ssh-keygen -p -f <your-key-path>`.

On macOS/Linux/WSL, restrict the received key to your account:

```bash
chmod 600 ~/.ssh/agentic-engineering-2026-p01
```

On Windows, store it in your own user-only `$HOME\.ssh` directory. If OpenSSH reports that key permissions are too open, ask the facilitator to check its Windows file ACL. Do not work around the error by using someone else's key.

The facilitator keeps only one owner-only local access JSON. The [preparation helper](README.md#1-prepare-the-one-local-access-file) can export one selected key to a new `.ssh` file for personal handoff; participants do not need that JSON or any temp manifest/config/card files.

## 2. Connect from your own computer

Replace p01 and the IP with **your own row**. Compare the first SSH prompt's ED25519 fingerprint with the trusted table before accepting it. Do not disable host-key checks or enable agent forwarding.

macOS/Linux/WSL:

```bash
x11_private_key="$HOME/.ssh/agentic-engineering-2026-p01"
x11_ip='<your-public-ip>'
ssh -i "$x11_private_key" -o ForwardAgent=no "course@$x11_ip"
```

Windows PowerShell:

```powershell
$x11_private_key = "$HOME\.ssh\agentic-engineering-2026-p01"
$x11_ip = '<your-public-ip>'
ssh -i $x11_private_key -o ForwardAgent=no "course@$x11_ip"
```

You are now on the **VM host**. Check the prepared repo and running container, then enter it:

```bash
cd /home/course/course-repo
git rev-parse HEAD
docker ps
devcontainer exec --workspace-folder "$PWD" bash
```

Do not clone over the prepared repo or recreate its container blindly. Use [troubleshooting](#troubleshooting) if the container is stopped.

## 3. Sign in inside your own container

The prompt now belongs to the **container**, where agent and git commands run. Configure your real git identity locally in this repo:

```bash
git config user.name 'Your Name'
git config user.email 'your-approved-email@example.com'
git remote -v
gh auth login
gh auth status
claude auth login
claude auth status
uv run check.py
```

Use your own approved account and project-scoped git access. `check.py` must end `GREEN` with at least one ready agent. If you use another supported agent, follow its sign-in instructions in the course README instead of the Claude commands. No personal sign-ins are baked into the image.

Before pushing, ensure `origin` is a repo you own or have course-authorised write access to. The prepared snapshot may have no `origin`; if it has one, it may point at the read-only source. Create your own repo from the course template and add or replace the destination explicitly:

```bash
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin https://github.com/<your-account>/<your-course-repo>.git
else
  git remote add origin https://github.com/<your-account>/<your-course-repo>.git
fi
git switch -c x11-work
```

If a work branch already exists, inspect it and continue there instead of rerunning branch creation. Multiple sessions on your own VM are allowed; coordinate their files or use worktrees for concurrent work. Continue with the [X11 lab](../x11-remote-environment.md).

## Troubleshooting

| Symptom | Action |
|---|---|
| SSH times out | Ask the facilitator to check VM power state and the venue's current public source IP against the NSG. There is no automatic daily stop. Do not widen access to the whole internet. |
| `Permission denied (publickey)` | Check your assigned ID, key path, VM IP and username `course`. Do not use another person's key. |
| Host fingerprint differs | Stop and ask the facilitator to verify through Azure management. A changed machine needs a new trusted fingerprint; never just suppress the warning. |
| Container is stopped after VM start | On the VM host run `docker ps -a`, identify your repo's container and run `docker start <container-id>`. Then retry `devcontainer exec`. The facilitator configures `unless-stopped`; a container explicitly stopped by a person needs an explicit start. |
| Container is missing or repo commit differs | Ask the facilitator to check the prepared environment. Do not recreate it until any existing work is saved. |
| `check.py` is RED | Read each FAIL, check personal model/git sign-ins and missing tools. Container startup alone is not proof setup succeeded. |
| A job disappeared after shutdown | VM shutdown/reboot ends processes. tmux survives a client disconnect, not a VM stop. Resume from saved code and logs. |
| Cannot push | Check `gh auth status`, repo permissions, `git remote -v` and your local git identity inside the container. |

Save code and proof outside the VM before final cleanup. Remove the temporary local course key when it is no longer needed.
