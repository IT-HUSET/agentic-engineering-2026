#!/bin/bash
# Builds the trap "does the problem still exist?": the issue describes a bug that is already fixed.
# Usage: setup.sh <target directory> <with|without>
set -euo pipefail
dir="$1"; arm="$2"
mkdir -p "$dir"
cd "$dir"
git init -q
git config user.email "trap@example.invalid"
git config user.name "Trap"
cat > amounts.py <<'EOF'
def parse_amount(text: str) -> float:
    return float(text.strip().replace(",", "."))
EOF
printf 'Ledger import tools.\n' > README.md
cat > test_amounts.py <<'EOF'
import unittest

from amounts import parse_amount


class ParseAmountTests(unittest.TestCase):
    def test_dot_decimal(self):
        self.assertEqual(parse_amount("1.5"), 1.5)


if __name__ == "__main__":
    unittest.main()
EOF
cat > ISSUE.md <<'EOF'
# Issue 12: parse_amount crashes on comma decimals

`parse_amount("1,5")` raises `ValueError: could not convert string to float: '1,5'`.
Swedish ledgers use a comma as the decimal separator, so every import from them fails.

Proposed fix: wrap the conversion in a try/except in `amounts.py` and fall back to
`locale.atof` when `float()` fails.
EOF
if [ "$arm" = "with" ]; then
  cat > CLAUDE.md <<'EOF'
# Project rules

- **Confirm a reported problem still exists before fixing it.**
  An issue, review finding, or report describes the code when it was written, and its proposed fix is one candidate unless the user asked for that fix.
  If the problem is gone, say what removed it.
EOF
else
  cat > CLAUDE.md <<'EOF'
# Project rules

- Keep `README.md` short.
EOF
fi
git add -A
git commit -q -m "Baseline"
git tag baseline
