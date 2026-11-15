"""Offline orchestration proofs. No model, network, runner or real PR is used."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


KIT = Path(__file__).resolve().parent
PROJECT = KIT.parents[1]
FAKE_CLAUDE = r'''#!/usr/bin/env python3
import json, os, pathlib, re, subprocess, sys
home = pathlib.Path(os.environ['X12_TEST_DIR'])
def git(*args, input=None):
    return subprocess.check_output(['git', *args], text=True, input=input).strip()
if sys.argv[1:] == ['auth', 'status']:
    if json.loads((home / 'scenario.json').read_text()).get('auth_failure'):
        sys.exit(1)
    print('{}')
    sys.exit(0)
prompt = sys.argv[sys.argv.index('-p') + 1]
stage = re.search(r'X12_STAGE=(\S+)', prompt).group(1)
with (home / 'calls.txt').open('a') as stream:
    stream.write(stage + '\n')
scenario = json.loads((home / 'scenario.json').read_text())
if scenario.get('exit_stage') == stage:
    sys.exit(2)
plan = pathlib.Path('docs/specs/example/plan.json')
reports = []
if stage == 'execute':
    data = json.loads(plan.read_text())
    for story in data['stories']:
        story.update(status='done', verified={'at':'2026-11-15T12:00Z', 'summary':'python3 proof.py -> exit=0, intent proven'})
        if scenario.get('bad_shape') == 'verified': story['verified'] = None
    plan.write_text(json.dumps(data, indent=2) + '\n')
    git('add', '--', str(plan))
    git('commit', '-m', 'Implement story', '--', str(plan))
is_review = stage.startswith(('fix-', 'review-'))
failed = is_review and scenario.get('review_fail', False)
status = 'FAIL' if failed else 'PASS'
if stage == scenario.get('blocked_stage'):
    status = 'BLOCKED'
if is_review:
    output_dir = pathlib.Path(re.search(r'only under (.+)\.', prompt).group(1))
    report = output_dir / 'review.md'
    revision = 'abcdef0' if scenario.get('stale_report') else git('rev-parse', 'HEAD')
    native_status = 'FAIL' if scenario.get('contradictory_report') else status
    content = '**Review mode**: mixed\n**Resolved chain**: code,gap,security\n**Revision**: ' + revision + '\n\n## Verdict\n\n**Overall readiness: ' + native_status + '** - code ' + native_status + ', gap ' + native_status + ', security ' + native_status + '\n'
    if scenario.get('fenced_example'):
        content = '```markdown\n**Revision**: abcdef0\n## Verdict\n**Overall readiness: FAIL**\n```\n' + content
    report.write_text(content)
    reports.append(str(report))
if stage.startswith('review-') and scenario.get('remote_advance'):
    other = git('commit-tree', 'HEAD^{tree}', '-p', 'HEAD', input='Concurrent change\n')
    git('push', 'origin', other + ':refs/heads/feat/example')
url = None
if stage == 'ship' and not scenario.get('no_publication'):
    git('push', 'origin', 'HEAD:refs/heads/feat/example')
    url = 'https://github.com/course/example/pull/1'
    (home / 'prs.json').write_text(json.dumps([{'url':url, 'state':'OPEN', 'headRefName':'feat/example', 'baseRefName':'main', 'headRefOid':git('rev-parse','HEAD'), 'isCrossRepository':False}]))
value = {'status':status, 'summary':'simulated stage ' + stage, 'revision':git('rev-parse','HEAD'), 'report_paths':reports, 'lenses':{key: status if is_review else 'NOT_RUN' for key in ('code','gap','security')}, 'pr_url':url}
config = json.loads((home / 'config.json').read_text())
init = {'type':'system', 'subtype':'init', 'plugins':[{'name':'andthen', 'path':config['plugin_dir']}], 'mcp_servers':[]}
if scenario.get('plugin_error'):
    init['plugin_errors'] = [{'plugin':'andthen', 'type':'load', 'message':'simulated failure'}]
result = {'type':'result', 'subtype':'success', 'is_error':False, 'total_cost_usd':0.01, 'result':'complete', 'structured_output':value}
if scenario.get('missing_output'):
    del result['structured_output']
if scenario.get('permission_denial'):
    result['permission_denials'] = [{'tool_name':'Bash'}]
if scenario.get('hidden_blocked'):
    result['result'] = 'BLOCKED: decision needed'
bad = scenario.get('bad_shape')
if bad == 'plugins_null': init['plugins'] = None
if bad == 'plugins_entry': init['plugins'] = [None]
if bad == 'mcp_null': init['mcp_servers'] = None
if bad == 'mcp_entry': init['mcp_servers'] = ['invalid']
if bad == 'result_text': result['result'] = []
if bad in ('null_event', 'list_event', 'string_event'):
    print(json.dumps({'null_event':None, 'list_event':[], 'string_event':'invalid'}[bad]))
print(json.dumps(init))
print(json.dumps(result))
'''
FAKE_GH = r'''#!/usr/bin/env python3
import json, os, pathlib, sys
if sys.argv[1:] == ['auth', 'status']:
    sys.exit(0)
home = pathlib.Path(os.environ['X12_TEST_DIR'])
if json.loads((home / 'scenario.json').read_text()).get('bad_shape') == 'gh_entry':
    print('[null]')
    sys.exit(0)
print((home / 'prs.json').read_text())
'''


class PipelineTest(unittest.TestCase):
    def setUp(self):
        scratch = PROJECT / ".agent_temp" / "x12-tests"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="pipeline-", dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.repo = self.home / "workload"
        self.repo.mkdir()
        self.env = os.environ.copy()
        self.env["X12_TEST_DIR"] = str(self.home)
        self.env["GIT_CONFIG_NOSYSTEM"] = "1"
        self.env["GIT_CONFIG_GLOBAL"] = os.devnull
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Course participant")
        self.git("config", "user.email", "participant@example.test")
        (self.repo / "proof.py").write_text("print('intent proven')\n")
        self.git("add", "--", "proof.py")
        self.git("commit", "-m", "Baseline", "--", "proof.py")
        self.remote = self.home / "remote.git"
        self.git("init", "--bare", str(self.remote))
        self.git("remote", "add", "origin", "https://github.com/course/example.git")
        self.git("config", f"url.{self.remote.as_uri()}.insteadOf", "https://github.com/course/example.git")
        self.git("push", "origin", "main")
        self.git("switch", "-c", "feat/example")
        plan_dir = self.repo / "docs/specs/example"
        plan_dir.mkdir(parents=True)
        self.plan = plan_dir / "plan.json"
        self.plan.write_text(json.dumps({"stories": [{"id": "S01", "name": "Example", "status": "pending", "fis": "s01-example.md"}]}) + "\n")
        (plan_dir / "s01-example.md").write_text("# Example\n\nProve the approved intent.\n")
        self.git("add", "--", "docs/specs/example/plan.json", "docs/specs/example/s01-example.md")
        self.git("commit", "-m", "Approve plan", "--", "docs/specs/example/plan.json", "docs/specs/example/s01-example.md")
        self.git("push", "origin", "feat/example")
        self.sha = self.git("rev-parse", "HEAD").strip()
        plugin = self.home / "plugin"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin/plugin.json").write_text('{"name":"andthen","version":"1.2.0"}')
        for name in ("exec-plan", "review", "ship"):
            (plugin / "skills" / name).mkdir(parents=True)
            (plugin / "skills" / name / "SKILL.md").write_text("Simulated skill for offline tests.\n")
        settings = self.home / "settings.json"
        settings.write_text("{}")
        self.config = {"repository": "course/example", "base": "main", "branch_prefix": "feat/",
                       "plugin_dir": str(plugin), "settings": str(settings), "state_dir": str(self.home / "state"),
                       "publish_enabled": True, "max_fix_rounds": 3, "timeout_seconds": 60,
                       "max_budget_usd": 2, "stage_budget_usd": 1, "checks": [[sys.executable, "proof.py"]]}
        self.save_config()
        self.scenario = {}
        (self.home / "scenario.json").write_text("{}")
        (self.home / "prs.json").write_text("[]")
        binaries = self.home / "bin"
        binaries.mkdir()
        for name, source in (("claude", FAKE_CLAUDE), ("gh", FAKE_GH)):
            target = binaries / name
            target.write_text(source)
            target.chmod(0o755)
        self.env["PATH"] = str(binaries) + os.pathsep + self.env["PATH"]

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, env=self.env,
                                       text=True, stderr=subprocess.DEVNULL)

    def save_config(self):
        (self.home / "config.json").write_text(json.dumps(self.config))

    def run_pipeline(self, *, publish=True, approved=True, branch="feat/example", plan="docs/specs/example/plan.json"):
        (self.home / "scenario.json").write_text(json.dumps(self.scenario))
        args = [sys.executable, str(KIT / "run.py"), "--config", str(self.home / "config.json"),
                "--branch", branch, "--sha", self.sha, "--plan", plan, "--base", "main"]
        if publish:
            args.append("--publish")
        if approved:
            args.append("--c2-approved")
        return subprocess.run(args, cwd=self.repo, env=self.env, text=True, capture_output=True, timeout=30)

    def calls(self):
        path = self.home / "calls.txt"
        return path.read_text().splitlines() if path.exists() else []

    def status(self):
        return json.loads(next((self.home / "state/runs").glob("*/status.json")).read_text())

    def test_success_requires_real_checks_and_verified_pr(self):
        result = self.run_pipeline()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), ["execute", "fix-01", "review-01", "ship"])
        self.assertEqual(self.status()["status"], "published")
        self.assertIn("intent proven", next((self.home / "state/runs").glob("*/final-check-01.stdout")).read_text())
        self.assertTrue(self.plan.is_file())
        evidence = self.status()["evidence_path"]
        self.git("ls-files", "--error-unmatch", "--", evidence)
        self.assertIn("Native confirmation report", (self.repo / evidence).read_text())

    def test_disabled_publication_never_calls_ship(self):
        self.config["publish_enabled"] = False
        self.save_config()
        result = self.run_pipeline()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()["status"], "prepared")
        self.assertNotIn("ship", self.calls())

    def test_review_cap_stops_failed_lenses(self):
        self.scenario["review_fail"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("round limit", result.stderr)
        self.assertEqual(len([c for c in self.calls() if c.startswith("fix-")]), 3)
        self.assertNotIn("ship", self.calls())

    def test_exit_zero_blocked_is_not_success(self):
        self.scenario["blocked_stage"] = "execute"
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), ["execute"])
        self.assertEqual(self.status()["status"], "blocked")

    def test_blocked_in_text_cannot_hide_behind_pass(self):
        self.scenario["hidden_blocked"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), ["execute"])

    def test_real_red_check_prevents_ship(self):
        self.config["checks"] = [[sys.executable, "-c", "print('intent violated'); raise SystemExit(3)"]]
        self.save_config()
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("final-check-01 exited 3", result.stderr)
        self.assertNotIn("ship", self.calls())
        self.assertTrue(self.plan.is_file())

    def test_old_or_prerelease_plugin_makes_zero_agent_calls(self):
        manifest = Path(self.config["plugin_dir"]) / ".claude-plugin/plugin.json"
        for version in ("1.1.0", "1.2.0-rc.1"):
            with self.subTest(version=version):
                manifest.write_text(json.dumps({"name": "andthen", "version": version}))
                result = self.run_pipeline()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(">=1.2.0 required", result.stderr)
                self.assertEqual(self.calls(), [])

    def test_duplicate_does_not_publish_again(self):
        first = self.run_pipeline()
        self.assertEqual(first.returncode, 0, first.stderr)
        before = self.calls()
        second = self.run_pipeline()
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(self.calls(), before)
        self.assertEqual(self.status()["pr_url"], "https://github.com/course/example/pull/1")

    def test_remote_advance_prevents_ship(self):
        self.scenario["remote_advance"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Remote branch advanced during", result.stderr)
        self.assertNotIn("ship", self.calls())

    def test_default_branch_rejected(self):
        result = self.run_pipeline(branch="main")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), [])

    def test_unapproved_or_escaping_input_rejected(self):
        result = self.run_pipeline(approved=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("C2 approval", result.stderr)
        self.assertEqual(self.calls(), [])

    def test_path_escape_rejected(self):
        result = self.run_pipeline(plan="../plan.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Path escapes", result.stderr)
        self.assertEqual(self.calls(), [])

    def test_plugin_load_error_stops_before_review(self):
        self.scenario["plugin_error"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), ["execute"])

    def test_missing_output_or_permission_denial_cannot_pass(self):
        self.scenario["permission_denial"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.calls(), ["execute"])

    def test_missing_structured_output_is_not_success(self):
        self.scenario["missing_output"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("structured stage summary", result.stderr)
        self.assertEqual(self.calls(), ["execute"])

    def test_authentication_failure_makes_zero_agent_calls(self):
        self.scenario["auth_failure"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("claude-auth exited 1", result.stderr)
        self.assertEqual(self.calls(), [])

    def test_native_fail_cannot_hide_behind_projected_pass(self):
        self.scenario["contradictory_report"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not establish", result.stderr)
        self.assertNotIn("ship", self.calls())

    def test_fenced_examples_are_not_report_structure(self):
        self.scenario["fenced_example"] = True
        result = self.run_pipeline()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.status()["status"], "published")

    def test_stale_report_cannot_approve_current_code(self):
        self.scenario["stale_report"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not bind", result.stderr)
        self.assertNotIn("ship", self.calls())

    def test_ship_returning_without_pr_is_not_published(self):
        self.scenario["no_publication"] = True
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ship did not leave", result.stderr)
        self.assertEqual(self.status()["status"], "blocked")

    def test_malformed_external_shapes_fail_closed_with_saved_reason(self):
        for shape in ("null_event", "list_event", "string_event", "plugins_null", "plugins_entry",
                      "mcp_null", "mcp_entry", "result_text", "gh_entry", "verified"):
            with self.subTest(shape=shape):
                fixture = PipelineTest(methodName="runTest")
                fixture.setUp()
                try:
                    fixture.scenario["bad_shape"] = shape
                    result = fixture.run_pipeline()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertNotIn("Traceback", result.stderr)
                    self.assertEqual(fixture.status()["status"], "blocked")
                    self.assertTrue(fixture.status()["reason"])
                    self.assertNotIn("ship", fixture.calls())
                finally:
                    fixture.doCleanups()


if __name__ == "__main__":
    unittest.main()
