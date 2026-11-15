#!/usr/bin/env python3
"""Gate (Stop): blocks the stop once when the tests are red.

decision "block" keeps the turn alive, and reason becomes Claude's next instruction.
The gate lets the stop through in these cases:
- stop_hook_active is true: a Stop hook is already keeping the turn alive, so the
  gate blocks at most once per stop and never loops.
- background_tasks is not empty: a subagent or a background command is still
  working, and the tree is half-finished.
- the working tree is unchanged: the turn was a question, not a change.
- no test command is defined: the gate has nothing to run.

The test command comes from the environment variable TEAM_TEST_CMD (a shell command,
for example "python3 -m unittest -q" or "make test"). Set it per repo in the `env`
block of .claude/settings.json. Without it the gate does nothing, so it is safe to
ship to repos in any language.
"""
import json
import os
import subprocess
import sys

test_command = os.environ.get("TEAM_TEST_CMD", "").strip()

data = json.load(sys.stdin)
if not test_command or data.get("stop_hook_active") or data.get("background_tasks"):
    sys.exit(0)

project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
changed = subprocess.run(
    ["git", "status", "--porcelain"], cwd=project, capture_output=True, text=True
)
if changed.returncode == 0 and not changed.stdout.strip():
    sys.exit(0)

result = subprocess.run(
    test_command, shell=True, cwd=project, capture_output=True, text=True
)
if result.returncode != 0:
    tail = (result.stdout + result.stderr).strip()[-1200:]
    print(json.dumps({
        "decision": "block",
        "reason": "The test suite fails. Fix it, or say exactly why it cannot pass.\n" + tail,
    }))
