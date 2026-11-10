# Dev container

An alternative to installing everything on your own machine, and the way to run on Windows without WSL2. It has Claude Code, Codex CLI, GitHub Copilot CLI, AndThen, `gh`, `uv`, Node and `tmux`, and it installs the `todo-app` dependencies.

Use it in one of three ways: run your agent in the container's terminal (VS Code, or the codespace in your browser) after signing in there, for example `claude auth login`; connect the Claude app to a codespace over SSH; or follow a session with Remote Control.

Your case team can use it too: copy `.devcontainer/` to the root of your team's repo, and change the `uv sync` step in `setup.sh` if your stack needs something else.

## Let Claude set it up

The quickest way to a codespace with the Claude app connected. Open a session in the Claude app's Code tab on your own machine, in any folder, and paste this with your GitHub account filled in. Claude runs the commands and stops when you need to sign in or click something in the app.

> Set up a GitHub codespace for my repo `<your-account>/agentic-engineering-2026` and connect this Claude app to it over SSH. Install the GitHub CLI (`gh`) if it's missing and sign me in with the `codespace` scope. Then read `.devcontainer/README.md` in my repo with `gh` and follow its Codespaces steps. Run the commands yourself, and stop when I need to sign in or click in the app.

Prefer to do it by hand? Follow the steps below.

## Start it

**Codespaces:** you need the GitHub CLI, `gh`, on your own machine, signed in. It creates the codespace and carries every SSH connection to it, the Claude app's included. Install it if you don't have it: `winget install --id GitHub.cli` on Windows (then open a new PowerShell window so it finds `gh`), `brew install gh` on macOS, or see [cli.github.com](https://cli.github.com).

```bash
gh auth login -h github.com -p https -w -s codespace
```

Already signed in to `gh`? Add the scope instead:

```bash
gh auth refresh -h github.com -s codespace
```

```bash
gh codespace create -R <your-account>/agentic-engineering-2026 -b main --machine basicLinux32gb --idle-timeout 240m
```

**Docker on your own machine:** open the repo in VS Code and run **Dev Containers: Reopen in Container**. The Claude app connection below works only with Codespaces, because this container does not publish its SSH port to your machine.

## Connect the Claude app (Codespaces)

The Claude Code tab in the desktop app can run its sessions inside your codespace over SSH. You don't sign in to Claude in the container for this, because the app passes its own sign-in to each session.

On Windows you need the Claude app from Claude's download page, not the Microsoft Store. Run the commands below in PowerShell. `ssh -V` should show OpenSSH 9.4 or later. With an older version the app uses a built-in SSH client with fewer features.

1. Give the codespace a fixed SSH name. Replace `<codespace>` with the name from `gh codespace list`. Run this again if you create a new codespace.

   macOS and Linux:
   ```bash
   gh codespace ssh -c <codespace> --config | sed -E 's/^Host .*/Host course-codespace/' > ~/.ssh/course-codespace.conf
   ```
   Windows (PowerShell):
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.ssh" | Out-Null
   gh codespace ssh -c <codespace> --config | ForEach-Object { $_ -replace '^Host .*', 'Host course-codespace' } | Set-Content -Encoding ascii "$HOME\.ssh\course-codespace.conf"
   ```
2. Include that file in your SSH config. Do this once.

   macOS and Linux:
   ```bash
   printf '\nMatch all\nInclude ~/.ssh/course-codespace.conf\n' >> ~/.ssh/config
   ```
   Windows (PowerShell):
   ```powershell
   Add-Content -Encoding ascii "$HOME\.ssh\config" "`nMatch all`nInclude ~/.ssh/course-codespace.conf"
   ```
3. Check that it connects. This prints `ok`, and starts the codespace if it was stopped:
   ```bash
   ssh course-codespace echo ok
   ```
4. In the app, open the environment selector and choose **New environment**, **SSH**, **Add SSH connection**. Enter `course-codespace` as **SSH host** and leave port and key empty.
5. Choose `/workspaces/<repo-name>` as the folder.

Tested from macOS and from Windows 11 (PowerShell 5.1, OpenSSH 9.5).

### What differs from a local session

| | Over SSH |
|---|---|
| Browser pane | Not available, so Claude can't open your app or check the UI there |
| See your running app | Forward the port yourself: `ssh -N -L 8000:localhost:8000 course-codespace`, then open `http://localhost:8000` |
| File pane | View only. Ask Claude to make the edit |
| `claude` in the terminal tab | Not signed in. Run `claude auth login` if you want it |

## Follow a session with Remote Control

Remote Control lets you steer a session in the container from your phone or [claude.ai/code](https://claude.ai/code). It needs a Claude subscription, not an API key, and on a Team or Enterprise plan an Owner must have turned it on.

1. Sign in to Claude in the container, in the app's terminal tab or any other terminal there. The sign-in stays in the container until you run `claude auth logout`.
   ```bash
   claude auth login
   ```
2. Start it in `tmux`, so it keeps running when you close the terminal:
   ```bash
   tmux new -As rc claude remote-control
   ```
3. Open the URL it prints, or press space for a QR code.
4. Leave `tmux` with `Ctrl-b` and then `d`. Run `tmux attach -t rc` to get back.

## Stopped codespaces, and ones that won't stop

A codespace stops after its idle timeout, which is why the command above sets the maximum, 240 minutes. Your files survive a stop, and the next SSH connection starts the codespace again, but a running job ends.

- **Silence stops it.** With a 5-minute timeout, a silent SSH connection and a `tmux` process with nobody connected both stopped it within about 6 minutes. Don't count on Remote Control alone to keep a codespace running during a long unattended run.
- **Output keeps it running.** Output over an open SSH connection kept it running for the 9 minutes we measured.
- **The Claude app keeps it running.** With the app connected, a codespace with a 30-minute timeout was still running after 45 minutes, even with the session archived and nobody working. That uses up your Codespaces quota, so stop it yourself when you're done:
  ```bash
  gh codespace stop -c <codespace>
  ```
