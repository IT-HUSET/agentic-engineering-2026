#!/usr/bin/env bash
# Azure Run Command may invoke /bin/sh rather than honor the shebang.
if [ -z "${BASH_VERSION:-}" ]; then
  exec /bin/bash "$0" "$@"
fi
# Encode the salted hash for Azure's command transport so dollar signs cannot expand.
set -euo pipefail

if [[ $# -ne 1 || ! $1 =~ ^[A-Za-z0-9_-]+$ || ${#1} -gt 512 ]]; then
  printf 'Expected one encoded SHA-512 crypt hash.\n' >&2
  exit 2
fi
password_hash=$(python3 - "$1" <<'DECODE'
import base64
import sys
try:
    value = sys.argv[1]
    decoded = base64.b64decode(value + '=' * (-len(value) % 4), altchars=b'-_', validate=True).decode('ascii')
    if '\n' in decoded or '\r' in decoded:
        raise ValueError('a hash must be one line')
    print(decoded)
except (ValueError, UnicodeError):
    raise SystemExit('Invalid encoded password hash.')
DECODE
)
# Literal dollar signs are part of the crypt format.
# shellcheck disable=SC2016
hash_pattern='^\$6\$(rounds=[0-9]+\$)?[./A-Za-z0-9]{1,16}\$[./A-Za-z0-9]{86}$'
if [[ ! $password_hash =~ $hash_pattern ]]; then
  printf 'Expected one SHA-512 crypt hash.\n' >&2
  exit 2
fi
if [[ $EUID -ne 0 ]]; then
  printf 'Run as root through Azure Run Command.\n' >&2
  exit 1
fi
getent passwd course >/dev/null
config=/etc/ssh/sshd_config
[[ -f $config && ! -L $config ]]
backup=$(mktemp /etc/ssh/sshd_config.x11.XXXXXX)
cp -p "$config" "$backup"
changed=false
cleanup() {
  status=$?
  trap - EXIT
  if [[ $status -ne 0 && $changed == true ]]; then
    cp -p "$backup" "$config"
    if /usr/sbin/sshd -t; then systemctl reload ssh >/dev/null 2>&1 || true; fi
    printf 'Password access configuration failed; prior SSH configuration restored.\n' >&2
  fi
  rm -f "$backup"
  exit "$status"
}
trap cleanup EXIT
changed=true
python3 - "$config" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text()
start = '# BEGIN X11 PASSWORD ACCESS'
end = '# END X11 PASSWORD ACCESS'
if start in text or end in text:
    pattern = re.compile(r'(?m)^# BEGIN X11 PASSWORD ACCESS\n.*?^# END X11 PASSWORD ACCESS\n?\s*\Z', re.S)
    if text.count(start) != 1 or text.count(end) != 1 or not pattern.search(text):
        raise SystemExit('Existing X11 block is malformed or not final; leaving unrelated configuration alone.')
    text = pattern.sub('', text)
block = '''# BEGIN X11 PASSWORD ACCESS
Match User root
    PermitRootLogin no
    PasswordAuthentication no
Match User course
    PasswordAuthentication yes
    PubkeyAuthentication no
    AuthenticationMethods password
# END X11 PASSWORD ACCESS
'''
path.write_text(text.rstrip('\n') + '\n\n' + block)
PY
/usr/sbin/sshd -t
course_settings=$(/usr/sbin/sshd -T -C user=course,host=localhost,addr=127.0.0.1)
root_settings=$(/usr/sbin/sshd -T -C user=root,host=localhost,addr=127.0.0.1)
grep -qx 'passwordauthentication yes' <<< "$course_settings"
grep -qx 'pubkeyauthentication no' <<< "$course_settings"
grep -qx 'authenticationmethods password' <<< "$course_settings"
grep -Eq '^permitrootlogin (no|prohibit-password|without-password)$' <<< "$root_settings"
grep -qx 'passwordauthentication no' <<< "$root_settings"
printf 'course:%s\n' "$password_hash" | chpasswd -e
systemctl reload ssh
printf 'PASSWORD_ACCESS_READY\n'
