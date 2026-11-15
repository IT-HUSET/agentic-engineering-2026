#!/bin/bash
# Runs a trap N times per arm, in parallel, and prints one line per run.
# A trap is a directory with setup.sh <workspace> <with|without>, check.sh <workspace> and prompt.txt.
# Usage: traps/run-trap.sh <trap directory> <runs per arm> <model> <output directory outside every CLAUDE.md>
# The arms are "with without". Set ARMS for others, e.g. ARMS="with without setting".
set -euo pipefail
trap_dir="$(cd "$1" && pwd)"; n="$2"; model="$3"; out="$4"
if [ -e "$out" ]; then echo "Output directory already exists: $out" >&2; exit 1; fi
mkdir -p "$out"
prompt="$(cat "$trap_dir/prompt.txt")"
arms="${ARMS:-with without}"
for arm in $arms; do
  for i in $(seq 1 "$n"); do
    ws="$out/$arm-$i/ws"
    "$trap_dir/setup.sh" "$ws" "$arm"
    (
      cd "$ws"
      claude -p "$prompt" \
        --setting-sources project \
        --strict-mcp-config \
        --model "$model" \
        --allowedTools "Read" "Edit" "Bash(git *)" "Bash(python3 -m unittest*)" \
        --disallowedTools "Bash(git push*)" \
        --max-budget-usd 1 \
        --output-format json \
        < /dev/null > "../result.json" 2> "../stderr.txt" || true
    ) &
  done
done
wait
for arm in $arms; do
  for i in $(seq 1 "$n"); do
    state="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print("ERROR " + str(d.get("subtype")) if d.get("is_error") or d.get("subtype") != "success" else "OK")' "$out/$arm-$i/result.json" 2>/dev/null || echo "ERROR no result.json")"
    if [ "$state" = "OK" ]; then
      verdict="$("$trap_dir/check.sh" "$out/$arm-$i/ws")"
    else
      verdict="$state"
    fi
    cost="$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(round(d.get("total_cost_usd"),3), d.get("num_turns"))' "$out/$arm-$i/result.json" 2>/dev/null || echo "? ?")"
    echo "$arm $i $verdict | cost/turns: $cost"
  done
done
