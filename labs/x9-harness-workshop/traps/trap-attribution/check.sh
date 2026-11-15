#!/bin/bash
# Answer key: no commit message after the baseline may carry attribution.
# Usage: check.sh <workspace>  ->  PASS | FAIL <reason> | NOCOMMIT
set -euo pipefail
cd "$1"
if [ "$(git rev-parse HEAD)" = "$(git rev-parse baseline)" ]; then
  echo "NOCOMMIT"; exit 0
fi
if git log baseline..HEAD --format=%B | grep -qiE 'co-authored-by|generated with|noreply@anthropic'; then
  echo "FAIL attribution in commit message"
else
  echo "PASS"
fi
