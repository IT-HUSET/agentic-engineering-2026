---
description: Write a session note and open a PR against team-home. Run it yourself at the end of a session.
argument-hint: "[short topic]"
disable-model-invocation: true
---

# Session note

`$ARGUMENTS` is a short topic in kebab-case, for example `orders-retry-policy`. Without a topic: propose one.

1. Go through the session and keep only what passes the entry test: something that deviated from what a fresh session could read in the code or the git history, a decision with its reason, or a trap that cost time. If it happened once and the cause is fixed: do not write it.
2. Write the note with this template. Leave out code excerpts, logs, tokens, personal ID numbers and customer data.

   ```markdown
   # <topic>

   Date: <YYYY-MM-DD>. Repos: <names from the catalog>.

   ## Deviated from what could be read
   - <point>

   ## Decisions and reasons
   - <decision>, because <reason>

   ## Traps
   - <trap> and how to avoid it
   ```

3. If nothing passes the test: say so and stop without writing a note.
4. Otherwise run the script, with the note on stdin and a quoted heredoc so the shell interprets nothing:

   ```bash
   "${CLAUDE_PLUGIN_ROOT}/scripts/propose-note.sh" <topic> <<'NOTE'
   <the note>
   NOTE
   ```

   The script runs gitleaks, puts the note on its own branch in a temporary worktree of team-home, pushes and opens a PR. It never touches team-home's working tree.
5. Print the PR link. Do not merge the PR: a human approves it.
