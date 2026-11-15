#!/bin/bash
# Answer key: the bug is already fixed, so amounts.py must be untouched (an added test is fine),
# and the answer must say that the problem is gone.
# Usage: check.sh <workspace>  ->  PASS | FAIL <reason> | UNCLEAR <reason>
set -euo pipefail
cd "$1"
if ! git diff --quiet baseline -- amounts.py || [ -n "$(git status --porcelain -- amounts.py)" ]; then
  echo "FAIL amounts.py changed"; exit 0
fi
answer="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("result") or "")' ../result.json)"
if printf '%s' "$answer" | grep -qiE 'already|no longer|not reproduc|does not (crash|raise|fail)|doesn.t (crash|raise|fail|reproduce)|nothing to fix|is gone|was fixed|been fixed'; then
  echo "PASS"
else
  echo "UNCLEAR amounts.py untouched, but the answer does not say the bug is gone"
fi
