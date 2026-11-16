#!/usr/bin/env python3
"""Set the temporary course password through Azure management, without local secret files."""

import argparse
import base64
import getpass
import json
from pathlib import Path
import re
import subprocess
import sys

SCRIPT = Path(__file__).with_name('password-access.sh')
HASH_PATTERN = re.compile(r'\$6\$(?:rounds=[0-9]+\$)?[./A-Za-z0-9]{1,16}\$[./A-Za-z0-9]{86}')


def verification_error(values):
    messages = '\n'.join(value.get('message', '') for value in values)
    failures = (
        ('Syntax error', 'remote shell syntax error'),
        ('Illegal option', 'remote shell rejected a script option'),
        ('Expected one encoded SHA-512 crypt hash.', 'Run Command did not supply the encoded hash argument'),
        ('Invalid encoded password hash.', 'Run Command supplied an invalid encoded hash'),
        ('Expected one SHA-512 crypt hash.', 'Run Command did not supply the expected hash argument'),
        ('Run as root through Azure Run Command.', 'remote script was not elevated'),
        ('Existing X11 block is malformed', 'existing X11 SSH block is malformed or not final'),
        ('prior SSH configuration restored', 'SSH configuration validation or reload failed; prior configuration restored'),
    )
    for marker, explanation in failures:
        if marker in messages:
            return explanation
    if any(value.get('code', '').lower().endswith('/failed') for value in values):
        return 'Azure extension reported failure'
    if not re.search(r'(?m)^PASSWORD_ACCESS_READY\s*$', messages):
        return 'remote script did not confirm password access'
    return None


def set_password(subscription, resource_group, vms, openssl='openssl'):
    password = getpass.getpass('Temporary course password: ')
    if not password or '\n' in password or '\r' in password:
        print('ERROR: enter one nonempty password line.', file=sys.stderr)
        return 1
    try:
        hashed = subprocess.run(
            [openssl, 'passwd', '-6', '-stdin'], input=password + '\n',
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        print('ERROR: OpenSSL SHA-512 password hashing failed; use OpenSSL with passwd -6.', file=sys.stderr)
        return 1
    del password
    if not HASH_PATTERN.fullmatch(hashed):
        print('ERROR: OpenSSL did not return a SHA-512 crypt hash.', file=sys.stderr)
        return 1
    encoded_hash = base64.urlsafe_b64encode(hashed.encode('ascii')).decode('ascii').rstrip('=')
    failed = False
    for vm in vms:
        command = [
            'az', 'vm', 'run-command', 'invoke', '--subscription', subscription,
            '--resource-group', resource_group, '--name', vm,
            '--command-id', 'RunShellScript', '--scripts', '@' + str(SCRIPT.resolve()),
            '--parameters', 'passwordHashEncoded=' + encoded_hash, '--output', 'json',
        ]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            values = json.loads(result.stdout).get('value', [])
            error = verification_error(values)
        except subprocess.CalledProcessError as failure:
            error = f'Azure CLI returned exit {failure.returncode}; check Azure authentication and VM agent state'
        except OSError:
            error = 'Azure CLI could not start'
        except (ValueError, TypeError, AttributeError):
            error = 'Azure CLI returned an unexpected response'
        print(f'{vm}: ' + ('PASSWORD_ACCESS_READY' if error is None else 'ERROR: ' + error))
        failed = failed or error is not None
    return int(failed)


def vm_name(value):
    if not re.fullmatch(r'x11-p[0-9]{2}(?:-rebuild)?', value):
        raise argparse.ArgumentTypeError('use a course VM name such as x11-p01 or x11-p01-rebuild')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    password = commands.add_parser('set-password', help='prompt once and configure password-only course SSH')
    password.add_argument('--subscription', required=True)
    password.add_argument('--resource-group', default='agentic-engineering-2026')
    password.add_argument('--vms', nargs='+', type=vm_name, default=[f'x11-p{number:02d}' for number in range(1, 5)])
    password.add_argument('--openssl', default='openssl', help='OpenSSL executable supporting passwd -6')
    args = parser.parse_args()
    if not SCRIPT.is_file():
        parser.error('the versioned password-access.sh script is missing')
    return set_password(args.subscription, args.resource_group, args.vms, args.openssl)


if __name__ == '__main__':
    sys.exit(main())
