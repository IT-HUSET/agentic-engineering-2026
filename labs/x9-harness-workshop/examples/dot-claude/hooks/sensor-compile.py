#!/usr/bin/env python3
"""Sensor (PostToolUse, matcher Edit|Write): quick check of the file that was just changed.

The tool has already run. Exit 2 shows stderr to Claude, which then fixes it in the same turn.
Replace py_compile with your team's linter or type checker.
"""
import json
import subprocess
import sys

path = json.load(sys.stdin).get("tool_input", {}).get("file_path", "")
if not path.endswith(".py"):
    sys.exit(0)

result = subprocess.run(
    [sys.executable, "-m", "py_compile", path], capture_output=True, text=True
)
if result.returncode != 0:
    print(f"Sensor: {path} does not compile.\n{result.stderr.strip()[-800:]}", file=sys.stderr)
    sys.exit(2)
