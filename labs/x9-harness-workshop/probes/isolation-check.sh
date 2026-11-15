#!/bin/bash
# Measures what an empty headless run loads, with and without the user's settings.
# Usage: isolation-check.sh <empty directory outside every CLAUDE.md> <model>
set -euo pipefail
dir="$1"; model="$2"
mkdir -p "$dir/default" "$dir/project-only" "$dir/no-claudemd"
q='Answer in one line, no tools: do the instructions you were given mention "en dashes"? Reply YES or NO.'
( cd "$dir/default" && claude -p "$q" --model "$model" --max-budget-usd 1 --output-format json < /dev/null > ../default.json 2> ../default.err || true ) &
( cd "$dir/project-only" && claude -p "$q" --model "$model" --setting-sources project --strict-mcp-config --max-budget-usd 1 --output-format json < /dev/null > ../project-only.json 2> ../project-only.err || true ) &
( cd "$dir/no-claudemd" && CLAUDE_CODE_DISABLE_CLAUDE_MDS=1 claude -p "$q" --model "$model" --setting-sources project --strict-mcp-config --max-budget-usd 1 --output-format json < /dev/null > ../no-claudemd.json 2> ../no-claudemd.err || true ) &
wait
for f in default project-only no-claudemd; do
  python3 - "$dir/$f.json" "$f" <<'EOF'
import json, sys
try:
    d = json.load(open(sys.argv[1]))
except Exception as e:
    print(sys.argv[2], "ERROR", e); sys.exit(0)
u = d.get("usage", {})
loaded = u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
print(f'{sys.argv[2]:13} answer={str(d.get("result"))[:40]!r} context_in={loaded} cost={d.get("total_cost_usd")} turns={d.get("num_turns")} keys={sorted(d.keys())}')
EOF
done
