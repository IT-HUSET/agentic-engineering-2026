#!/usr/bin/env bash
# Checks that the host's credentials did not follow you into the dev container. Run in the container before the first claude.
# Prints OK or WARNING per check and exits 1 on at least one warning. Never prints secrets.
warn=0
check() { echo "$1: $2"; case "$2" in OK*) ;; *) warn=1 ;; esac; }

[ -z "${SSH_AUTH_SOCK:-}" ] && check "SSH_AUTH_SOCK empty" OK || check "SSH_AUTH_SOCK empty" "WARNING set to $SSH_AUTH_SOCK"

ssh-add -l >/dev/null 2>&1; rc=$?   # 2 = no agent, 1 = agent without keys, 0 = keys listed
[ "$rc" -ne 0 ] && check "ssh-add -l lists no keys" OK || check "ssh-add -l lists no keys" "WARNING the agent has keys"

helpers=$(git config --get-all credential.helper 2>/dev/null)
[ -z "$helpers" ] && check "no credential.helper" OK || check "no credential.helper" "WARNING: $helpers"

if printf 'protocol=https\nhost=github.com\n\n' | GIT_TERMINAL_PROMPT=0 git credential fill >/dev/null 2>&1; then
  check "git credential fill returns nothing" "WARNING returned a credential for github.com"
else
  check "git credential fill returns nothing" OK
fi

if command -v gh >/dev/null && gh auth status >/dev/null 2>&1; then check "gh is logged out" "WARNING gh is logged in"; else check "gh is logged out" OK; fi

vars=$(env | cut -d= -f1 | grep -iE '^(GH|GITHUB)_|TOKEN|SECRET|API_KEY' | tr '\n' ' ')
[ -z "$vars" ] && check "no token variables" OK || check "no token variables" "WARNING review: $vars"

echo "Still open even when everything is OK: outbound network, and /workspaces being the host's directory."
exit $warn
