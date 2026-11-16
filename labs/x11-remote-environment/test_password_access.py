"""Local password-access checks. No Azure calls, real passwords or host SSH changes."""

import argparse
import base64
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.dont_write_bytecode = True
FOLDER = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prepare_course', FOLDER / 'prepare-course.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
HASH = '$6$testfixture$' + 'a' * 86
PASSWORD = 'unrelated test fixture'


class PasswordAccessTests(unittest.TestCase):
    def invoke(self, responses):
        calls = []

        def tools(command, **kwargs):
            calls.append((command, kwargs))
            if command[0] == 'test-openssl':
                return subprocess.CompletedProcess(command, 0, HASH + '\n', '')
            response = responses.pop(0)
            if isinstance(response, Exception):
                raise response
            return subprocess.CompletedProcess(command, 0, json.dumps(response), '')

        output = io.StringIO()
        with mock.patch.object(helper.getpass, 'getpass', return_value=PASSWORD) as prompt, mock.patch.object(helper.subprocess, 'run', side_effect=tools), contextlib.redirect_stdout(output):
            result = helper.set_password('course-subscription', 'course-group', ['x11-p01', 'x11-p02'], 'test-openssl')
        prompt.assert_called_once()
        return result, calls, output.getvalue()

    def test_plaintext_goes_only_to_local_hash_stdin_and_success_requires_script_marker(self):
        success = {'value': [{'code': 'ProvisioningState/succeeded', 'message': '[stdout]\nPASSWORD_ACCESS_READY\n[stderr]\n'}]}
        result, calls, output = self.invoke([success, success])
        self.assertEqual(result, 0)
        self.assertEqual(calls[0][0], ['test-openssl', 'passwd', '-6', '-stdin'])
        self.assertEqual(calls[0][1]['input'], PASSWORD + '\n')
        for command, kwargs in calls[1:]:
            self.assertNotIn(PASSWORD, ' '.join(command))
            self.assertNotIn('input', kwargs)
            encoded = next(value.split('=', 1)[1] for value in command if value.startswith('passwordHashEncoded='))
            self.assertNotIn('$', encoded)
            self.assertNotIn(HASH, ' '.join(command))
            self.assertEqual(base64.urlsafe_b64decode(encoded + '=' * (-len(encoded) % 4)).decode(), HASH)
            self.assertIn('@' + str((FOLDER / 'password-access.sh').resolve()), command)
            self.assertIn('course-subscription', command)
        self.assertEqual(output.count('PASSWORD_ACCESS_READY'), 2)
        self.assertNotIn(HASH, output)
        self.assertNotIn(PASSWORD, output)

    def test_extension_success_without_password_verification_is_reported_as_failure(self):
        unverified = {'value': [{'code': 'ProvisioningState/succeeded', 'message': 'Enable succeeded'}]}
        success = {'value': [{'message': 'PASSWORD_ACCESS_READY\n'}]}
        result, calls, output = self.invoke([unverified, success])
        self.assertEqual(result, 1)
        self.assertIn('x11-p01: ERROR', output)
        self.assertIn('x11-p02: PASSWORD_ACCESS_READY', output)
        self.assertEqual(len(calls), 3)

    def test_azure_error_does_not_leak_raw_command_or_hash_and_other_vm_is_still_attempted(self):
        failure = subprocess.CalledProcessError(1, ['az', HASH], stderr=PASSWORD)
        result, calls, output = self.invoke([failure, {'value': [{'message': 'PASSWORD_ACCESS_READY\n'}]}])
        self.assertEqual(result, 1)
        self.assertEqual(len(calls), 3)
        self.assertNotIn(HASH, output)
        self.assertNotIn(PASSWORD, output)

    def test_shell_failure_diagnostics_do_not_print_the_raw_response(self):
        error = helper.verification_error([{'message': 'Syntax error at line 5: ' + HASH + PASSWORD}])
        self.assertEqual(error, 'remote shell syntax error')
        self.assertNotIn(HASH, error)
        self.assertNotIn(PASSWORD, error)

    def test_azure_shell_transport_preserves_dollar_signs_after_decode(self):
        encoded = base64.urlsafe_b64encode(HASH.encode()).decode().rstrip('=')
        # Azure's command executor expands raw $6$...; this ASCII-only argument survives /bin/sh.
        transported = subprocess.run(['sh', '-c', 'printf "%s" ' + encoded], capture_output=True, text=True, check=True).stdout
        script = (FOLDER / 'password-access.sh').read_text()
        decoder = script.split("<<'DECODE'\n", 1)[1].split('\nDECODE\n', 1)[0]
        decoded = subprocess.run([sys.executable, '-', transported], input=decoder, capture_output=True, text=True, check=True).stdout.rstrip('\n')
        self.assertEqual(decoded, HASH)
        with_newline = base64.urlsafe_b64encode((HASH + '\n').encode()).decode().rstrip('=')
        rejected = subprocess.run([sys.executable, '-', with_newline], input=decoder, capture_output=True, text=True)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertNotIn(HASH, rejected.stdout + rejected.stderr)

    def test_shell_entry_rejects_bad_input_before_touching_ssh(self):
        result = subprocess.run(['sh', str(FOLDER / 'password-access.sh'), 'not-a-hash'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue('Invalid encoded password hash.' in result.stderr or 'Expected one' in result.stderr)

    def test_invalid_hash_never_reaches_azure(self):
        with mock.patch.object(helper.getpass, 'getpass', return_value=PASSWORD), mock.patch.object(helper.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, '$1$not-sha512', '')) as tools, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(helper.set_password('subscription', 'group', ['x11-p01']), 1)
        tools.assert_called_once()

    def test_only_course_vm_names_are_accepted(self):
        self.assertEqual(helper.vm_name('x11-p01-rebuild'), 'x11-p01-rebuild')
        with self.assertRaises(argparse.ArgumentTypeError):
            helper.vm_name('production-vm')

    def transform_config(self, config):
        script = (FOLDER / 'password-access.sh').read_text()
        transform = script.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
        return subprocess.run([sys.executable, '-', str(config)], input=transform, capture_output=True, text=True)

    def test_ssh_update_preserves_other_rules_and_reapplying_is_idempotent(self):
        temporary_root = FOLDER.parents[1] / '.agent_temp'
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='password-config-test-', dir=temporary_root) as temporary:
            config = Path(temporary) / 'sshd_config'
            original = 'Include /etc/ssh/sshd_config.d/*.conf\n# keep our policy\nMatch User build\n    PasswordAuthentication no\n'
            config.write_text(original)
            self.assertEqual(self.transform_config(config).returncode, 0)
            updated = config.read_text()
            self.assertTrue(updated.startswith(original))
            self.assertEqual(self.transform_config(config).returncode, 0)
            self.assertEqual(config.read_text(), updated)

    def test_nonfinal_owned_block_is_rejected_without_dropping_later_policy(self):
        temporary_root = FOLDER.parents[1] / '.agent_temp'
        temporary_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='password-config-test-', dir=temporary_root) as temporary:
            config = Path(temporary) / 'sshd_config'
            original = '# BEGIN X11 PASSWORD ACCESS\nMatch User course\n# END X11 PASSWORD ACCESS\nMatch User other\n    PasswordAuthentication no\n'
            config.write_text(original)
            self.assertNotEqual(self.transform_config(config).returncode, 0)
            self.assertEqual(config.read_text(), original)


if __name__ == '__main__':
    unittest.main()
