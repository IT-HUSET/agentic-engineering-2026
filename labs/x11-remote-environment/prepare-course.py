#!/usr/bin/env python3
"""Keep X11 IPs and temporary SSH keys in one local, owner-only JSON file."""

import argparse
import csv
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMP_ROOT = REPO_ROOT / '.agent_temp'
DEFAULT_FILE = TEMP_ROOT / 'x11-access.json'


def owner_only(path, directory=False):
    path.chmod(0o700 if directory else 0o600)
    if os.name == 'nt':
        identity = subprocess.run(
            ['whoami', '/user', '/fo', 'csv', '/nh'],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        sid = next(csv.reader([identity]))[1]
        grant = f'*{sid}:(OI)(CI)F' if directory else f'*{sid}:F'
        subprocess.run(
            ['icacls', str(path), '/inheritance:r', '/grant:r', grant],
            check=True, stdout=subprocess.DEVNULL,
        )


def local_file(path):
    if TEMP_ROOT.is_symlink() or not TEMP_ROOT.resolve().is_relative_to(REPO_ROOT):
        raise ValueError('the repo .agent_temp must not be a symlink or escape the repository')
    path = path.absolute()
    if not path.resolve().is_relative_to(TEMP_ROOT.resolve()) or path == TEMP_ROOT:
        raise ValueError('the access file must be inside this repo\'s .agent_temp')
    for candidate in (path, *path.parents):
        if candidate == TEMP_ROOT.parent:
            break
        if candidate.is_symlink():
            raise ValueError('the access path must not contain symbolic links')
    return path


def write_new(path, content):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        owner_only(path)
        with os.fdopen(descriptor, 'w', encoding='utf-8') as handle:
            descriptor = None
            handle.write(content)
    except BaseException:
        if descriptor is not None:
            os.close(descriptor)
        path.unlink()
        raise


def read_access(path):
    data = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(data, dict) or not data:
        raise ValueError('the access file must map participant IDs to ip/privateKey records')
    for participant, record in data.items():
        if not re.fullmatch(r'p[0-9]{2}', participant) or not isinstance(record, dict) or set(record) != {'ip', 'privateKey'}:
            raise ValueError('the access file must contain only pNN records with ip and privateKey')
        if record['ip'] is not None:
            ipaddress.IPv4Address(record['ip'])
        if not isinstance(record['privateKey'], str) or not record['privateKey'].startswith('-----BEGIN OPENSSH PRIVATE KEY-----'):
            raise ValueError(f'{participant} does not contain an OpenSSH private key')
    return data


def public_key(private_key):
    with tempfile.TemporaryDirectory(prefix='x11-key-', dir=TEMP_ROOT) as staging:
        folder = Path(staging)
        owner_only(folder, directory=True)
        key = folder / 'key'
        write_new(key, private_key)
        return subprocess.run(
            ['ssh-keygen', '-y', '-f', str(key)],
            check=True, capture_output=True, text=True,
        ).stdout.strip()


def participant_id(value):
    if not re.fullmatch(r'p[0-9]{2}', value) or value == 'p00':
        raise argparse.ArgumentTypeError('use a participant ID from p01 to p99')
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    create = commands.add_parser('create', help='create one new access file; no cloud operations')
    create.add_argument('--count', type=int, default=4)
    create.add_argument('--output-file', type=Path, default=DEFAULT_FILE)
    for name in ('export', 'public-key', 'set-ip'):
        command = commands.add_parser(name)
        command.add_argument('participant', type=participant_id)
        command.add_argument('--input-file', type=Path, default=DEFAULT_FILE)
        if name == 'set-ip':
            command.add_argument('ip', type=ipaddress.IPv4Address)
    args = parser.parse_args()
    if shutil.which('ssh-keygen') is None:
        parser.error('OpenSSH ssh-keygen is required')
    path = local_file(args.output_file if args.command == 'create' else args.input_file)
    TEMP_ROOT.mkdir(exist_ok=True)
    if args.command == 'create':
        if not 1 <= args.count <= 99:
            parser.error('--count must be between 1 and 99')
        if path.exists():
            parser.error('the output file already exists; nothing overwritten')
        if not path.parent.is_dir():
            parser.error('the output parent directory must already exist')
        data = {}
        with tempfile.TemporaryDirectory(prefix='x11-keys-', dir=TEMP_ROOT) as staging:
            folder = Path(staging)
            owner_only(folder, directory=True)
            for number in range(1, args.count + 1):
                participant = f'p{number:02d}'
                key = folder / participant
                subprocess.run(
                    ['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-f', str(key), '-C', f'agentic-engineering-2026-{participant}'],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
                )
                data[participant] = {'ip': None, 'privateKey': key.read_text(encoding='utf-8')}
            write_new(path, json.dumps(data, indent=2) + '\n')
        print(f'Prepared {args.count} distinct keys in {path}. No cloud resources created; private keys were not printed.')
        return
    data = read_access(path)
    if args.participant not in data:
        parser.error('the selected participant is absent from this access file')
    if args.command == 'export':
        directory = Path.home() / '.ssh'
        if directory.is_symlink():
            parser.error('the local .ssh directory must not be a symbolic link')
        directory.mkdir(mode=0o700, exist_ok=True)
        destination = directory / f'agentic-engineering-2026-{args.participant}'
        if destination.exists() or destination.is_symlink():
            parser.error('the selected key path already exists; nothing overwritten')
        write_new(destination, data[args.participant]['privateKey'])
        print(f'Exported only {args.participant} to {destination}. Keep it private and hand it only to that participant.')
    elif args.command == 'public-key':
        print(public_key(data[args.participant]['privateKey']))
    else:
        data[args.participant]['ip'] = str(args.ip)
        descriptor, temporary = tempfile.mkstemp(prefix='x11-access-', dir=TEMP_ROOT)
        os.close(descriptor)
        temporary = Path(temporary)
        try:
            owner_only(temporary)
            temporary.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
        print(f'Updated {args.participant} IP in {path}; no other persistent file created.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Preparation stopped: {error}', file=sys.stderr)
        sys.exit(1)
