#!/bin/bash
# Builds a small demo repo with the examples installed: one subagent, one skill and three hooks.
# Fallback for the exercises when your own repo cannot be used.
# Usage: demo-repo.sh <target directory outside every CLAUDE.md>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dir="$1"
if [ -e "$dir" ]; then echo "Target directory already exists: $dir" >&2; exit 1; fi
mkdir -p "$dir"
cd "$dir"
git init -q
git config user.email "demo@example.invalid"
git config user.name "Demo"

cat > amounts.py <<'EOF'
def parse_amount(text: str) -> float:
    return float(text.strip().replace(",", "."))
EOF
cat > test_amounts.py <<'EOF'
import unittest

from amounts import parse_amount


class ParseAmountTests(unittest.TestCase):
    def test_dot_decimal(self):
        self.assertEqual(parse_amount("1.5"), 1.5)

    def test_comma_decimal(self):
        self.assertEqual(parse_amount("1,5"), 1.5)


if __name__ == "__main__":
    unittest.main()
EOF
printf '# Ledger tools\n\nParses amount cells from ledger exports.\n' > README.md
printf '# Changelog\n\n## Unreleased\n' > CHANGELOG.md
printf '# Project rules\n\n- Run the tests with `python3 -m unittest -q`.\n- The project codeword is KIWI.\n' > CLAUDE.md
printf '__pycache__/\n' > .gitignore

cp -R "$here/dot-claude" .claude
chmod +x .claude/hooks/*.py
git add .
git commit -q -m "Baseline"
git tag baseline
echo "Demo repo: $dir"
