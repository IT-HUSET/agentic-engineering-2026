---
description: Write or update the catalog entry catalog/<repo>.md for one of the team's repos. Use when a repo is added or its test command, owner or dependencies change.
argument-hint: "<repo-name>"
---

# Catalog entry for a repo

`$ARGUMENTS` is the repo's name in the "Other repos" table in `AGENTS.md`. The session runs in team-home.

1. Look up the path and remote in "Other repos". If the row is missing, ask before you create anything.
2. Read the repo, no more than needed: README, the build file, the CI configuration and `CODEOWNERS` if there is one.
3. Write `catalog/<repo>.md` with frontmatter (owner, stack, remote, path, test, depends_on) and a short body
   about what deviates from the standard: Docker requirements, environment variables, rules that the code does not show.
4. Write only what the agent cannot read for itself in a fresh session. Do not paste in the README.
5. `test:` must be a command that has been run and passed, not an assumed one. Run it in the repo.

A hook (`check-catalog.sh`) checks the frontmatter once the file is written. If it answers with missing fields: fill them in.
