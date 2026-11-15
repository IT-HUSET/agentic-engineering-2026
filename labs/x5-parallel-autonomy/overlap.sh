#!/usr/bin/env bash
# File overlap between two stories. Load with: source overlap.sh
#   areas <fis>                    files a story plans to touch (backtick paths under ### Work Areas)
#   overlap <clone> <range>        files that both S03 and S04 have committed (stories are recognised by Story-ID:)
# dependsOn shows order only, never files. Example:
#   comm -12 <(areas s03-invitations.md) <(areas s04-todo-assignment.md)
#   overlap x5-a1 x5-start..HEAD        (after an aborted merge: x5-start..story/S04)

areas() { sed -n '/^### Work Areas/,/^### What We/p' "$1" | grep -oE '`[^`]*(/|\.py|\.md|\.html)[^`]*`' | tr -d '`' | sort -u; }

story_files() { git -C "$1" log --no-merges --grep="^Story-ID: $2\$" --name-only --format= "$3" | sort -u; }

overlap() { comm -12 <(story_files "$1" S03 "$2") <(story_files "$1" S04 "$2"); }
