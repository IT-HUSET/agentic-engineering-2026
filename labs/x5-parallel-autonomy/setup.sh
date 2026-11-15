#!/usr/bin/env bash
# Prepares the workload for the two "Going further" deepenings of X5. Run it in the dev container.
#   SOL=<workload folder> ./setup.sh work   builds $X5/work as its own repo with the plan committed
#   ./setup.sh tag                          checks that S01 and S02 are done and tags x5-start
#   ./setup.sh clones                       makes three clones of the tag: x5-a1, x5-b1, x5-c1
# Between work and tag, S01 and S02 are run in $X5/work (see the lab, "Who holds the plan?").
# The unattended-pipeline deepening needs only work. To do both, build a second workload: X5=$HOME/x5-pipeline SOL=... ./setup.sh work
set -euo pipefail
X5=${X5:-$HOME/x5}
D=docs/specs/let-people-share-their-lists

work() {
  : "${SOL:?SOL must point to the workload folder your facilitator hands out}"
  mkdir -p "$X5/results" "$X5/work"
  # empty project root: todo-app/ becomes its own repo, so the docs/ paths in the plan resolve
  git -C "${REPO:-/workspaces/agentic-engineering-2026}" archive HEAD todo-app | tar -x -C "$X5/work" --strip-components=1
  cd "$X5/work"
  git init -q -b main && git add -A && git commit -q -m "todo-app baseline"
  git switch -q -c feat/shared-lists

  # the bundle: PRD, ADR, glossary, the plan with five FIS. Everything is committed: exec-plan --worktree stops otherwise.
  mkdir -p "$D" docs/adrs .claude
  cp "$SOL/f2-shared-lists-prd.md" "$D/prd.md"
  cp "$SOL/f3-shared-lists-adr.md" docs/adrs/ADR-001-per-list-access-grant.md
  cp "$SOL/f3-shared-lists-glossary.md" docs/UBIQUITOUS_LANGUAGE.md
  cp "$SOL"/f4-shared-lists-whole-prd/* "$D/"
  # every docs/ path the plan and the FIS files mention must exist: no output means ok
  for f in $(grep -rhoE 'docs/[A-Za-z0-9_./-]+\.(md|json)' "$D" | sort -u); do [ -f "$f" ] || echo "MISSING $f"; done

  # worktrees branch from HEAD, not from the remote's default branch
  printf '{\n  "worktree": { "baseRef": "head" }\n}\n' > .claude/settings.json
  jq empty .claude/settings.json
  printf '.claude/worktrees/\n' >> .gitignore
  git add -A && git commit -q -m "X5 workload: PRD, ADR, glossary, plan"
  echo "work is ready in $X5/work on feat/shared-lists. Run S01 and S02 there, then: ./setup.sh tag"
}

tag() {
  cd "$X5/work"
  for s in S01 S02; do
    [ "$(jq -r --arg s "$s" '.stories[] | select(.id == $s) | .status' "$D/plan.json")" = done ] || { echo "$s is not done in plan.json" >&2; exit 1; }
  done
  [ -z "$(git status --porcelain --untracked-files=no)" ] || { echo "tracked files are modified: commit them first" >&2; exit 1; }
  uv run pytest -q | tail -1
  git tag -f x5-start
  echo "x5-start = $(git rev-parse --short x5-start). Next: ./setup.sh clones"
}

clones() {
  cd "$X5"
  for f in a b c; do
    git clone -q work "x5-${f}1"
    (cd "x5-${f}1" && git switch -q -c "x5/${f}1" x5-start && git remote remove origin && uv sync -q)
  done
  for f in a b c; do git -C "x5-${f}1" rev-parse --short HEAD; done   # three equal SHAs
  git -C x5-a1 remote | wc -l                                          # 0
}

case "${1:-}" in
  work) work ;;
  tag) tag ;;
  clones) clones ;;
  *) echo "Usage: SOL=<workload folder> $0 work | $0 tag | $0 clones" >&2; exit 1 ;;
esac
