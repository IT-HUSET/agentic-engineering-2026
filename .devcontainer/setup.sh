#!/usr/bin/env bash
# Each step warns instead of failing, so one network hiccup doesn't lose the whole container.
set -u

echo "Claude Code: $(claude --version 2>/dev/null || echo 'not found')"

echo "Installing AndThen (latest release)..."
claude plugin marketplace add IT-HUSET/andthen \
  || echo "Note: already added or failed. Retry: claude plugin marketplace add IT-HUSET/andthen"
claude plugin install andthen@andthen \
  || echo "Note: install failed. Retry: claude plugin install andthen@andthen"

# The course supports three agents, each with its own sign-in.
echo "Installing Codex CLI and Copilot CLI..."
npm install -g @openai/codex @github/copilot >/dev/null 2>&1 \
  || echo "Note: install failed. Retry: npm install -g @openai/codex @github/copilot"

# /usr/local/bin, because shells that skip /etc/bash.bashrc (SSH commands, login shells) lack ~/.local/bin.
# pipefail, so a failed download is not hidden by sh running an empty script.
echo "Installing AndThen Studio (latest release)..."
studio_install=https://github.com/IT-HUSET/andthen-studio-releases/releases/latest/download/install.sh
(set -o pipefail; curl -fsSL "$studio_install" | sudo ANDTHEN_STUDIO_INSTALL_DIR=/usr/local/bin sh) \
  || echo "Note: install failed. Retry: curl -fsSL $studio_install | sudo ANDTHEN_STUDIO_INSTALL_DIR=/usr/local/bin sh"

if [ -f todo-app/pyproject.toml ]; then
  echo "Installing todo-app dependencies..."
  (cd todo-app && uv sync) || echo "Note: uv sync failed. Retry: cd todo-app && uv sync"
fi

echo "Done. Run 'claude' to sign in."
