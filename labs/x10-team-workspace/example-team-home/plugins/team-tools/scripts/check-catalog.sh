#!/usr/bin/env bash
# PostToolUse sensor: checks catalog entries right after the agent has written them.
# Exit 2 shows stderr to the agent. The file is already written, so the hook cannot block.
set -u
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  */catalog/*.md) ;;
  *) exit 0 ;;
esac
case "$(basename "$file")" in _*) exit 0 ;; esac
[ -f "$file" ] || exit 0

front=$(awk 'NR==1 && $0!="---" {exit} NR>1 && $0=="---" {exit} NR>1 {print}' "$file")
missing=""
for key in owner stack remote path test; do
  printf '%s\n' "$front" | grep -Eq "^${key}:[[:space:]]*[^[:space:]]" || missing="$missing $key"
done

if [ -n "$missing" ]; then
  {
    echo "The catalog entry $file is missing frontmatter fields:$missing."
    echo "A fresh session needs owner, stack, remote, path and test to find the repo and run its tests without guessing."
    echo "Fill in the fields from the repo (README, build file, CI configuration). Leave none empty."
  } >&2
  exit 2
fi
exit 0
