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
scenario = json.loads((home / 'scenario.json').read_text())
if sys.argv[1:] == ['auth', 'status']:
    sys.exit(1 if scenario.get('auth_failure') else 0)
prompt = sys.argv[sys.argv.index('-p') + 1]
stage = re.search(r'X12_STAGE=(\S+)', prompt).group(1)
with (home / 'argv.jsonl').open('a') as stream:
    stream.write(json.dumps({'stage': stage, 'argv': sys.argv[1:]}) + '\n')
plan = pathlib.Path('docs/specs/example/plan.json')
if stage == 'execute':
    data = json.loads(plan.read_text())
    for story in data['stories']:
        story.update(status='done', verified={'at': '2026-11-15T12:00Z', 'summary': 'python3 proof.py -> exit=0, intent proven'})
        if scenario.get('unverified'): story['verified'] = None
    plan.write_text(json.dumps(data, indent=2) + '\n')
    git('add', '--', str(plan))
    git('commit', '-m', 'Implement story', '--', str(plan))
is_review = stage.startswith(('fix-', 'review-'))
number = int(stage.split('-')[1]) if is_review else 0
asks = stage.startswith('fix-') and number <= scenario.get('follow_up_rounds', 0)
signal = scenario.get('signal', 'all')
findings = []
if scenario.get('note_only'):
    findings.append(('LOW', 'SURFACED'))
if asks and signal in ('all', 'report'):
    findings.append(('HIGH', 'RESOLVED'))
if stage.startswith('fix-') and scenario.get('deferred_high'):
    findings.append(('HIGH', 'DEFERRED'))
if stage == 'fix-01' and scenario.get('partial_fix'):
    findings.append(('MEDIUM', 'PARTIALLY RESOLVED'))
if stage.startswith('review-') and scenario.get('confirm_high'):
    findings.append(('HIGH', None))
status = 'FAIL' if is_review and findings else 'PASS'
if stage == scenario.get('blocked_stage'):
    status = 'BLOCKED'
text = 'complete'
if asks and signal in ('all', 'text'):
    text = 'Next (fresh session): the `andthen:review` skill on the plan with `--fix`, as a follow-up to the report.'
reports = []
if is_review:
    report = pathlib.Path(re.search(r'--output-dir (\S+)', prompt).group(1)) / 'review.md'
    blocks = ''.join('#### Finding %d - %s - Example\n\n- **Finding**: example\n\n' % (i, sev) for i, (sev, _) in enumerate(findings, 1))
    content = ('# Mixed Review: example\n\n## Findings\n\n' + (blocks or 'No findings.\n') +
               '\n## Verdict\n\n**Overall readiness: ' + ('FAIL' if findings else 'PASS') + '**\n')
    if stage.startswith('fix-') and any(state for _, state in findings):
        content += '\n## Remediation Status\n\n' + ''.join('- **Finding %d - Example** - %s - evidence\n' % (i, state) for i, (_, state) in enumerate(findings, 1) if state)
    if scenario.get('fenced_example'):
        content = '```markdown\n#### Finding 9 - CRITICAL - Quoted example\n```\n' + content
    report.write_text(content)
    reports.append(str(report))
if stage.startswith('review-') and scenario.get('remote_advance'):
    git('push', 'origin', git('commit-tree', 'HEAD^{tree}', '-p', 'HEAD', input='Concurrent change\n') + ':refs/heads/feat/example')
url = None
if stage == 'ship' and not scenario.get('no_publication'):
    if scenario.get('ship_deletes_plan'):
        git('rm', '-q', '--', str(plan))
        git('commit', '-m', 'Ship')
    git('push', 'origin', 'HEAD:refs/heads/feat/example')
    url = 'https://github.com/course/example/pull/1'
    oid = 'f' * 40 if scenario.get('pr_wrong_head') else git('rev-parse', 'HEAD')
    (home / 'prs.json').write_text(json.dumps([{'url': url, 'state': 'OPEN', 'baseRefName': 'main', 'headRefOid': oid}]))
revision = 'abcdef0' if scenario.get('stale_revision') else git('rev-parse', 'HEAD')
value = {'status': status, 'summary': 'simulated stage ' + stage, 'revision': revision, 'report_paths': reports,
         'pr_url': url, 'next_review': bool(asks and signal in ('all', 'flag'))}
config = json.loads((home / 'config.json').read_text())
plugins = [] if scenario.get('no_plugin') else [{'name': 'andthen', 'path': config['plugin_dir']}]
result = {'type': 'result', 'subtype': 'success', 'is_error': False, 'result': text, 'structured_output': value}
if scenario.get('missing_output'):
    del result['structured_output']
if scenario.get('permission_denial'):
    result['permission_denials'] = [{'tool_name': 'Bash'}]
if scenario.get('hidden_blocked'):
    result['result'] = 'BLOCKED: decision needed'
print(json.dumps({'type': 'system', 'subtype': 'init', 'plugins': plugins}))
print(json.dumps(result))
'''
FAKE_GH = r'''#!/usr/bin/env python3
import os, pathlib, sys
if sys.argv[1:] == ['auth', 'status']:
    sys.exit(0)
print((pathlib.Path(os.environ['X12_TEST_DIR']) / 'prs.json').read_text())
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
        self.env.update(X12_TEST_DIR=str(self.home), X12_JOB="job-1", GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_GLOBAL=os.devnull, CLAUDE_CODE_OAUTH_TOKEN="test-subscription-token")
        self.env.pop("ANTHROPIC_API_KEY", None)
        self.env.pop("ANTHROPIC_AUTH_TOKEN", None)
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
        self.plan.write_text(json.dumps({"stories": [{"id": "S01", "status": "pending", "fis": "s01-example.md"}]}) + "\n")
        (plan_dir / "s01-example.md").write_text("# Example\n\nProve the approved intent.\n")
        committed = ["docs/specs/example/plan.json", "docs/specs/example/s01-example.md"]
        self.git("add", "--", *committed)
        self.git("commit", "-m", "Approve plan", "--", *committed)
        self.git("push", "origin", "feat/example")
        self.sha = self.git("rev-parse", "HEAD").strip()
        plugin = self.home / "plugin"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin/plugin.json").write_text('{"name":"andthen","version":"1.2.0"}')
        settings = self.home / "settings.json"
        settings.write_text("{}")
        self.config = {"repository": "course/example", "base": "main", "branch_prefix": "feat/",
                       "plugin_dir": str(plugin), "settings": str(settings), "state_dir": str(self.home / "state"),
                       "max_fix_rounds": 3, "stage_budget_usd": 1, "checks": [[sys.executable, "proof.py"]]}
        self.save_config()
        self.scenario = {}
        (self.home / "prs.json").write_text("[]")
        binaries = self.home / "bin"
        binaries.mkdir()
        for name, source in (("claude", FAKE_CLAUDE), ("gh", FAKE_GH)):
            (binaries / name).write_text(source)
            (binaries / name).chmod(0o755)
        self.env["PATH"] = str(binaries) + os.pathsep + self.env["PATH"]

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, env=self.env,
                                       text=True, stderr=subprocess.DEVNULL)

    def save_config(self):
        (self.home / "config.json").write_text(json.dumps(self.config))

    def run_pipeline(self, *, publish=True, approved=True, branch="feat/example", plan="docs/specs/example/plan.json"):
        (self.home / "scenario.json").write_text(json.dumps(self.scenario))
        args = [sys.executable, str(KIT / "run.py"), "--config", str(self.home / "config.json"),
                "--branch", branch, "--sha", self.sha, "--plan", plan]
        if publish:
            args.append("--publish")
        if approved:
            args.append("--c2-approved")
        return subprocess.run(args, cwd=self.repo, env=self.env, text=True, capture_output=True, timeout=30)

    def calls(self):
        path = self.home / "argv.jsonl"
        return [json.loads(line)["stage"] for line in path.read_text().splitlines()] if path.exists() else []

    def status(self):
        return json.loads((self.home / "state/job-1/status.json").read_text())

    def fresh(self, **scenario):
        fixture = PipelineTest(methodName="runTest")
        fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        fixture.scenario.update(scenario)
        return fixture

    def stops(self, message, calls):
        """The job fails with `message`, saves a blocked status and has made exactly these agent calls."""
        result = self.run_pipeline()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr)
        self.assertEqual(self.calls(), calls)
        self.assertEqual(self.status()["status"], "blocked")

    def test_success_needs_real_checks_and_a_verified_pr(self):
        result = self.run_pipeline()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), ["execute", "fix-01", "review-01", "ship"])
        status = self.status()
        self.assertEqual((status["status"], status["pr_url"]), ("published", "https://github.com/course/example/pull/1"))
        self.assertEqual(status["reviewed_sha"], self.git("rev-parse", "HEAD").strip())
        self.assertIn("intent proven", (self.home / "state/job-1/final-check-01.stdout").read_text())
        self.assertTrue(self.plan.is_file())

    def test_without_publish_every_gate_runs_but_ship_does_not(self):
        result = self.run_pipeline(publish=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.calls(), ["execute", "fix-01", "review-01"])
        self.assertEqual(self.status()["status"], "prepared")

    def test_loop_ends_on_the_hand_off_not_the_verdict(self):
        # A Note that no fix round may apply holds every verdict at FAIL; ship must still follow.
        self.scenario["note_only"] = True
        self.assertEqual(self.run_pipeline().returncode, 0)
        self.assertEqual(self.calls(), ["execute", "fix-01", "review-01", "ship"])
        self.assertEqual(self.status()["status"], "published")

    def test_follow_up_rounds_continue_while_the_next_line_asks(self):
        self.scenario["follow_up_rounds"] = 2
        self.assertEqual(self.run_pipeline().returncode, 0)
        self.assertEqual(self.calls(), ["execute", "fix-01", "fix-02", "fix-03", "review-03", "ship"])
        self.assertEqual(self.status()["fix_rounds"], 3)

    def test_each_next_signal_asks_for_a_follow_up(self):
        for signal in ("flag", "text", "report"):
            with self.subTest(signal=signal):
                fixture = self.fresh(follow_up_rounds=1, signal=signal)
                self.assertEqual(fixture.run_pipeline().returncode, 0)
                self.assertEqual(fixture.calls(), ["execute", "fix-01", "fix-02", "review-02", "ship"])
        fixture = self.fresh(partial_fix=True)
        self.assertEqual(fixture.run_pipeline().returncode, 0)
        self.assertEqual(fixture.calls(), ["execute", "fix-01", "fix-02", "review-02", "ship"])

    def test_round_limit_backstops_endless_follow_ups(self):
        self.scenario["follow_up_rounds"] = 99
        self.stops("limit", ["execute", "fix-01", "fix-02", "fix-03"])

    def test_deferred_high_finding_needs_a_decision(self):
        self.scenario["deferred_high"] = True
        self.stops("decision is needed", ["execute", "fix-01"])

    def test_confirmation_with_open_high_finding_blocks_ship(self):
        self.scenario["confirm_high"] = True
        self.stops("leaves CRITICAL/HIGH", ["execute", "fix-01", "review-01"])

    def test_fenced_examples_are_not_findings(self):
        self.scenario["fenced_example"] = True
        self.assertEqual(self.run_pipeline().returncode, 0)

    def test_blocked_stops_even_with_exit_zero(self):
        self.scenario["blocked_stage"] = "execute"
        self.stops("BLOCKED", ["execute"])

    def test_blocked_in_text_cannot_hide_behind_pass(self):
        self.scenario["hidden_blocked"] = True
        self.stops("BLOCKED", ["execute"])

    def test_unverified_story_stops_before_review(self):
        self.scenario["unverified"] = True
        self.stops("verified summary", ["execute"])

    def test_real_red_check_prevents_ship(self):
        self.config["checks"] = [[sys.executable, "-c", "print('intent violated'); raise SystemExit(3)"]]
        self.save_config()
        self.stops("final-check-01 exited 3", ["execute", "fix-01", "review-01"])

    def test_old_or_prerelease_plugin_makes_zero_agent_calls(self):
        manifest = Path(self.config["plugin_dir"]) / ".claude-plugin/plugin.json"
        for version in ("1.1.0", "1.2.0-rc.1"):
            with self.subTest(version=version):
                manifest.write_text(json.dumps({"name": "andthen", "version": version}))
                self.stops(">=1.2.0 required", [])

    def test_plugin_that_did_not_load_stops_the_first_stage(self):
        self.scenario["no_plugin"] = True
        self.stops("did not load", ["execute"])

    def test_permission_denial_stops(self):
        self.scenario["permission_denial"] = True
        self.stops("permission was denied", ["execute"])

    def test_missing_structured_output_or_stale_revision_is_not_success(self):
        for scenario in ("missing_output", "stale_revision"):
            with self.subTest(scenario=scenario):
                fixture = self.fresh(**{scenario: True})
                fixture.stops("structured stage summary", ["execute"])

    def test_stages_run_in_auto_mode_never_bypass(self):
        # Auto mode has a classifier review each action; bypass or dontAsk would change what a stage may do.
        self.assertEqual(self.run_pipeline().returncode, 0)
        calls = [json.loads(line) for line in (self.home / "argv.jsonl").read_text().splitlines()]
        self.assertEqual([c["stage"] for c in calls], ["execute", "fix-01", "review-01", "ship"])
        for call in calls:
            argv = call["argv"]
            self.assertEqual(argv[argv.index("--permission-mode") + 1], "auto", call["stage"])
            self.assertNotIn("--dangerously-skip-permissions", argv)
            self.assertEqual(argv[argv.index("--max-budget-usd") + 1], "1")
            settings = json.loads(argv[argv.index("--settings") + 1])
            self.assertNotIn("defaultMode", settings.get("permissions", {}))
            pushes = "Bash(git push *)" in settings.get("permissions", {}).get("deny", [])
            self.assertEqual(pushes, call["stage"] != "ship", f"{call['stage']}: only ship may push")

    def test_authentication_failure_makes_zero_agent_calls(self):
        self.scenario["auth_failure"] = True
        self.stops("claude-auth exited 1", [])

    def test_subscription_token_is_required_and_an_api_key_cannot_override_it(self):
        del self.env["CLAUDE_CODE_OAUTH_TOKEN"]
        self.stops("CLAUDE_CODE_OAUTH_TOKEN", [])
        self.env["CLAUDE_CODE_OAUTH_TOKEN"] = "test-subscription-token"
        self.env["ANTHROPIC_API_KEY"] = "test-key"
        self.stops("would override the subscription token", [])

    def test_existing_pr_stops_before_any_agent_call(self):
        (self.home / "prs.json").write_text('[{"url": "https://github.com/course/example/pull/1"}]')
        self.stops("already has a PR", [])

    def test_advanced_remote_tip_stops_before_any_agent_call(self):
        self.git("commit", "--allow-empty", "-m", "Concurrent change")
        self.git("push", "origin", "feat/example")
        self.git("reset", "-q", "--hard", self.sha)
        self.stops("advanced beyond", [])

    def test_remote_advance_during_the_job_prevents_ship(self):
        self.scenario["remote_advance"] = True
        self.stops("Remote branch advanced during", ["execute", "fix-01", "review-01"])

    def test_second_dispatch_after_publication_stops_before_any_agent_call(self):
        self.assertEqual(self.run_pipeline().returncode, 0)
        before = self.calls()
        self.assertNotEqual(self.run_pipeline().returncode, 0)
        self.assertEqual(self.calls(), before)

    def test_default_branch_unapproved_and_escaping_input_rejected(self):
        for kwargs, message in (({"branch": "main"}, "outside the configured prefix"),
                                ({"approved": False}, "C2 approval"),
                                ({"plan": "../plan.json"}, "Path escapes")):
            with self.subTest(**kwargs):
                result = self.run_pipeline(**kwargs)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(message, result.stderr)
                self.assertEqual(self.calls(), [])

    def test_ship_returning_without_pr_is_not_published(self):
        self.scenario["no_publication"] = True
        self.stops("ship did not leave", ["execute", "fix-01", "review-01", "ship"])

    def test_pr_for_another_revision_is_not_published(self):
        self.scenario["pr_wrong_head"] = True
        self.stops("exactly one open PR", ["execute", "fix-01", "review-01", "ship"])

    def test_ship_deleting_the_plan_bundle_is_not_published(self):
        self.scenario["ship_deletes_plan"] = True
        self.stops("deleted the plan bundle", ["execute", "fix-01", "review-01", "ship"])


if __name__ == "__main__":
    unittest.main()
