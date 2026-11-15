#!/usr/bin/env python3
"""Guard (PreToolUse, matcher Bash): denies git commands that stage everything.

Exit 2 stops the call, and stderr goes back to Claude as the reason.

An example, not a watertight guard. The pattern misses `git -C dir add -A` and
`git commit -m x -a`, and it does not stop a plain `git commit` from taking along
what another agent has already staged. A hook matches commands, not intent.
"""
import json
import re
import sys

command = json.load(sys.stdin).get("tool_input", {}).get("command", "")

STAGES_EVERYTHING = re.compile(
    r"\bgit\s+(add\s+(-A|--all|-u|--update|\.)(\s|$)|commit\s+(-[a-zA-Z]*a[a-zA-Z]*|--all)\b)"
)

if STAGES_EVERYTHING.search(command):
    print(
        "Blocked: this stages everything in the tree. Stage by path (git add <file>) "
        "and commit by path (git commit -m ... -- <file>), because another agent may "
        "have work staged here.",
        file=sys.stderr,
    )
    sys.exit(2)
