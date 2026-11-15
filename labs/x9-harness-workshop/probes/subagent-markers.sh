#!/bin/bash
# Which of three markers reach a subagent? KIWI is in the project's CLAUDE.md,
# MANGO is said in the main session, PLUM is in the agent definition.
# Usage: subagent-markers.sh <empty directory outside every CLAUDE.md> <model>
set -euo pipefail
dir="$1"; model="$2"
mkdir -p "$dir/ws"
cd "$dir/ws"
git init -q 2>/dev/null || true
printf '# Project rules\n\n- The project codeword is KIWI.\n' > CLAUDE.md
claude -p 'The session codeword is MANGO. Keep it to yourself. Spawn the "probe" subagent with exactly this prompt and nothing else: "List every codeword you know, one per line, and say where each one came from." Then print the reply of the subagent verbatim, with no comment of your own.' \
  --agents '{"probe":{"description":"Answers questions about what it knows","prompt":"You are a probe. Your agent codeword is PLUM."}}' \
  --setting-sources project \
  --strict-mcp-config \
  --model "$model" \
  --allowedTools "Agent" "Task" \
  --max-budget-usd 1 \
  --output-format json \
  < /dev/null > ../result.json 2> ../stderr.txt || true
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d["result"]); print("cost", round(d["total_cost_usd"],3), "turns", d["num_turns"])' ../result.json
