#!/usr/bin/env python3
"""Gate (Stop): blocks the stop once when the tests are red.

decision "block" keeps the turn alive, and reason becomes Claude's next instruction.
The gate lets the stop through in three cases:
- stop_hook_active is true: a Stop hook is already keeping the turn alive, so the
  gate blocks at most once per stop and never loops.
- background_tasks is not empty: a subagent or a background command is still
  working, and the tree is half-finished.
- the working tree is unchanged: the turn was a question, not a change.
"""
import json
import os
import subprocess
import sys

# Replace with the repo's own test command.
TEST_COMMAND = [sys.executable, "-m", "unittest", "-q"]

data = json.load(sys.stdin)
if data.get("stop_hook_active") or data.get("background_tasks"):
    sys.exit(0)

project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
changed = subprocess.run(
    ["git", "status", "--porcelain"], cwd=project, capture_output=True, text=True
)
if changed.returncode == 0 and not changed.stdout.strip():
    sys.exit(0)

result = subprocess.run(TEST_COMMAND, cwd=project, capture_output=True, text=True)
if result.returncode != 0:
    tail = (result.stdout + result.stderr).strip()[-1200:]
    print(json.dumps({
        "decision": "block",
        "reason": "The test suite fails. Fix it, or say exactly why it cannot pass.\n" + tail,
    }))
