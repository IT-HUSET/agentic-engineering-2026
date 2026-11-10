FROM mcr.microsoft.com/devcontainers/python:3.13

# tmux keeps `claude remote-control` alive after the terminal that started it closes.
RUN apt-get update \
    && apt-get install -y --no-install-recommends tmux \
    && rm -rf /var/lib/apt/lists/*

# A new named volume takes this directory's owner. Without it the sign-in volume is root-owned.
RUN install -d -o vscode -g vscode /home/vscode/.claude

# Codespaces loads GITHUB_TOKEN and secrets only in login shells. Commands sent over SSH, which the
# Claude app uses, run in other shells, where gh is signed out and git push fails.
# SHELL_LOGGED_IN skips that file's cd to the workspace. Does nothing outside Codespaces.
RUN sed -i '1i [ -n "$SSH_CONNECTION" ] \&\& [ -f /etc/profile.d/codespaces.sh ] \&\& export SHELL_LOGGED_IN=true \&\& . /etc/profile.d/codespaces.sh' /home/vscode/.bashrc
