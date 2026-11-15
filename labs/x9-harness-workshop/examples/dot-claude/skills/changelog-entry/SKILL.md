---
name: changelog-entry
description: Adds an entry to CHANGELOG.md for the staged change. Use when the user asks for a changelog entry or a release note, or wants a change recorded before committing.
allowed-tools: Read Edit Bash(git diff *)
---

## Staged change

```!
git diff --cached --stat
```

## Your task

Add one entry for the staged change under `## Unreleased` in `CHANGELOG.md`. Create that heading at the top of the file if it is missing.

- One line, starting with `Added`, `Changed`, `Fixed`, or `Removed`.
- Say what a user of the project notices, not which files changed.
- Read the staged diff with `git diff --cached` when the stat alone does not tell you that.

If nothing is staged, say so and change nothing.
