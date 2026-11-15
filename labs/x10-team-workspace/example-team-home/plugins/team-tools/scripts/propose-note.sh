#!/usr/bin/env bash
# Reads a session note on stdin, runs gitleaks, pushes it on its own branch and opens a PR.
# Requires TEAM_HOME (path to team-home), gitleaks, git and gh.
set -euo pipefail

slug=${1:?Give a kebab-case topic as the first argument}
: "${TEAM_HOME:?Set TEAM_HOME to the path of team-home}"
command -v gitleaks >/dev/null || { echo "gitleaks is missing." >&2; exit 1; }

note=$(cat)
[ -n "$note" ] || { echo "Empty note." >&2; exit 1; }

if ! printf '%s\n' "$note" | gitleaks stdin --redact --no-banner; then
  echo "gitleaks found a suspected secret. Remove it from the note and run again." >&2
  exit 1
fi

day=$(date +%Y-%m-%d)
branch="session/$day-$slug"
file="sessions/$day-$slug.md"
wt=$(mktemp -d)
cleanup() { git -C "$TEAM_HOME" worktree remove --force "$wt" 2>/dev/null || true; git -C "$TEAM_HOME" branch -D "$branch" >/dev/null 2>&1 || true; }
trap cleanup EXIT

git -C "$TEAM_HOME" fetch origin main --quiet
git -C "$TEAM_HOME" worktree add -b "$branch" "$wt" origin/main --quiet
mkdir -p "$wt/sessions"
printf '%s\n' "$note" > "$wt/$file"
git -C "$wt" add -- "$file"
git -C "$wt" commit --quiet -m "Session note: $slug"
git -C "$wt" push --quiet -u origin "$branch"
(cd "$wt" && gh pr create --base main --head "$branch" \
  --title "Session note: $slug" \
  --body "Session note. Review against the entry test in AGENTS.md before merging.")
