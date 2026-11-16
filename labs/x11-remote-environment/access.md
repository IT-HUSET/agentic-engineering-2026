# Your X11 remote environment

Each participant has their own VM, container and Claude/GitHub sign-ins. The facilitator prepares the environment. You need only Windows PowerShell or macOS Terminal with SSH; no Azure account, Azure CLI or Entra invitation is needed.

There is no automatic daily shutdown. The facilitator leaves VMs running while jobs need them and manually deallocates only after work is saved and no jobs are active. Files survive a stop; tmux/agent jobs do not. All course resources are removed after everyone has saved their work.

## Connection table

Verified through Azure management on 2026-11-15. The facilitator rechecks this table after any VM replacement. Public IPs, SSH host fingerprints and public host keys may be recorded here; **passwords and tokens never belong here**.

| Your ID | VM | Public IP | Trusted ED25519 host fingerprint |
|---|---|---|---|
| p01 | x11-p01 | `135.225.54.185` | `SHA256:QEZhegV4E7PG4lOkdMFC3aJTm5c+tnimtYh7fyWeL2c` |
| p02 | x11-p02 | `135.116.85.42` | `SHA256:Mxltd08Jd9ZC96+HYzPwsv42zR3SEXyVvEHf6rbJRM0` |
| p03 | x11-p03 | `135.225.54.218` | `SHA256:MR3N7acY+weXW2X77TfBsEAJqcOFoU4OhWJ17aEgYEs` |
| p04 | x11-p04 | `57.174.209.89` | `SHA256:oXluzXb8jp/ku3BI/juNQys0GaG9tNdpcU4mQorTSpQ` |

- Linux username: `course` on your own VM.
- Prepared repo path: `/home/course/course-repo`.
- Prepared checkout: branch `x11-course`. Work on your own branch, `x11-work`.
- Prepared source URL/commit: see the [public preparation record](README.md#public-preparation-record).

## 1. Open PowerShell or Terminal

The four temporary VMs use the same course password. Password hint: **The teacher's favorite country**. Ask the teacher if you need it. Enter it only at the SSH password prompt; nothing appears while you type. Do not put the password in a command or an agent prompt.

## 2. Paste your connection command

Copy **your own row** into Windows PowerShell or macOS Terminal. It opens your prepared container directly and asks for the course password:

| Your ID | Command |
|---|---|
| p01 | `ssh -t -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@135.225.54.185 devcontainer exec --workspace-folder /home/course/course-repo bash` |
| p02 | `ssh -t -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@135.116.85.42 devcontainer exec --workspace-folder /home/course/course-repo bash` |
| p03 | `ssh -t -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@135.225.54.218 devcontainer exec --workspace-folder /home/course/course-repo bash` |
| p04 | `ssh -t -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@57.174.209.89 devcontainer exec --workspace-folder /home/course/course-repo bash` |

You arrive **inside your own container**. Continue with personal sign-ins below. Type `exit` to disconnect; reconnect with the same command. Do not clone over the prepared repo or recreate its container blindly. `accept-new` accepts a new host, but stops if a previously known host changes. Ask the facilitator about any changed-host warning.

<details>
<summary>Open the VM host for host checks or troubleshooting</summary>

For p01, omit the trailing container command. Use your own VM IP:

```bash
ssh -o StrictHostKeyChecking=accept-new -o ForwardAgent=no course@135.225.54.185
```

Enter the course password, then inspect the prepared workspace and enter its container when needed:

```bash
cd /home/course/course-repo
git rev-parse HEAD
docker ps
devcontainer exec --workspace-folder /home/course/course-repo bash
```

</details>

## 3. Sign in inside your own container

The prompt now belongs to the **container**, where agent and git commands run. Set your git identity in this repo, then sign in to Claude:

```bash
git config user.name 'Your Name'
git config user.email 'your-approved-email@example.com'
claude auth login
claude auth status
```

**GitHub: a token for the one course repo.** A plain `gh auth login` grants `repo`, `read:org` and `gist` over all your repositories, and the agent in this container can use whatever the container holds. Create a fine-grained personal access token on github.com instead: repository access **only the one course repo**, permissions **Contents** and **Pull requests** read and write, a short expiry. Paste it into a file in the container home, outside the repo, use it once, and delete the file:

```bash
(umask 077; cat > "$HOME/.x11-gh-token")   # paste the token, then press Ctrl-D
gh auth login --with-token < "$HOME/.x11-gh-token"
rm -f "$HOME/.x11-gh-token"
gh auth status
uv run check.py
```

`gh auth status` should show a `github_pat_` token and no `repo`, `read:org` or `gist` scopes. `check.py` must end `GREEN` with at least one ready agent. If you use another supported agent, follow its sign-in instructions in the course README instead of the Claude commands. No personal sign-ins are baked into the image.

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
| Password rejected or `Permission denied` | Check your own VM IP and username `course`, then ask the teacher to confirm the temporary course password. |
| Host fingerprint differs | Stop and ask the facilitator to verify through Azure management. A changed machine needs a new trusted fingerprint; never just suppress the warning. |
| Container is stopped after VM start | On the VM host run `docker ps -a`, identify your repo's container and run `docker start <container-id>`. Then retry `devcontainer exec`. The facilitator configures `unless-stopped`; a container explicitly stopped by a person needs an explicit start. |
| Container is missing or repo commit differs | Ask the facilitator to check the prepared environment. Do not recreate it until any existing work is saved. |
| `check.py` is RED | Read each FAIL, check personal model/git sign-ins and missing tools. Container startup alone is not proof setup succeeded. |
| A job disappeared after shutdown | VM shutdown/reboot ends processes. tmux survives a client disconnect, not a VM stop. Resume from saved code and logs. |
| Cannot push | Check `gh auth status`, that the token covers this repo with Contents write, `git remote -v` and your git identity inside the container. |

Save code and proof outside the VM before final cleanup.
