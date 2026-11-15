#!/usr/bin/env python3
"""Run X12 inside a disposable, trusted course devcontainer: an approved plan in, a verified PR out."""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


class Stopped(Exception):
    pass


# The wrapper's projection of a skill's result. Not an AndThen interface.
SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "FAIL", "BLOCKED"]},
        "summary": {"type": "string"},
        "revision": {"type": "string"},
        "report_paths": {"type": "array", "items": {"type": "string"}},
        "pr_url": {"type": ["string", "null"]},
        "next_review": {"type": "boolean"},
    },
    "required": ["status", "summary", "revision", "report_paths", "pr_url", "next_review"],
}
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[`~]*[ \t]*$", re.M | re.S)


def read_json(path):
    return json.loads(Path(path).read_text())


def report_findings(text):
    """Severity of each finding and the status `implement-fix` recorded for it, outside code fences."""
    body, _, remediation = FENCE.sub("", text).partition("\n## Remediation Status\n")
    severity = {int(n): sev for n, sev in
                re.findall(r"^#{3,4} Finding (\d+) - (CRITICAL|HIGH|MEDIUM|LOW) - ", body, re.M)}
    status = {int(n): value for n, value in
              re.findall(r"^- \*\*Finding (\d+) - .*?\*\* - (PARTIALLY RESOLVED|RESOLVED|UNRESOLVED|DEFERRED|SURFACED)\b",
                         remediation, re.M)}
    return severity, status


class Pipeline:
    def __init__(self, args):
        self.args = args
        self.root = Path.cwd().resolve()
        self.config = read_json(args.config)
        job = os.environ.get("X12_JOB", f"local-{os.getpid()}")
        self.run_dir = Path(self.config["state_dir"]) / job
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.state = {"status": "running", "job_id": job, "source_sha": args.sha, "branch": args.branch,
                      "plan": args.plan, "stages": []}
        self.save()

    def save(self):
        (self.run_dir / "status.json").write_text(json.dumps(self.state, indent=2) + "\n")

    def finish(self, status, **fields):
        self.state.update(status=status, **fields)
        self.save()
        print(json.dumps(self.state))

    def command(self, argv, name=None):
        env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
        proc = subprocess.run(argv, cwd=self.root, env=env, text=True, capture_output=True)
        if name:
            (self.run_dir / f"{name}.stdout").write_text(proc.stdout)
            (self.run_dir / f"{name}.stderr").write_text(proc.stderr)
        if proc.returncode:
            raise Stopped(f"{name or argv[0]} exited {proc.returncode}; inspect retained logs")
        return proc.stdout.strip()

    def git(self, *args):
        return self.command(["git", *args])

    def clean(self):
        if self.git("status", "--porcelain", "--untracked-files=all"):
            raise Stopped("Workload tree is dirty; owned work is retained, not discarded")
        if self.git("branch", "--show-current") != self.args.branch:
            raise Stopped("The workload changed branches")
        self.git("merge-base", "--is-ancestor", self.args.sha, "HEAD")

    def remote_tip(self):
        return self.git("ls-remote", "--exit-code", "origin", f"refs/heads/{self.args.branch}").split()[0]

    def prs(self):
        return json.loads(self.command(
            ["gh", "pr", "list", "--repo", self.config["repository"], "--head", self.args.branch,
             "--state", "all", "--json", "url,state,baseRefName,headRefOid"]))

    def preflight(self):
        a, c = self.args, self.config
        if not a.c2_approved:
            raise Stopped("C2 approval for this source SHA is required")
        if a.branch == c["base"] or not a.branch.startswith(c["branch_prefix"]):
            raise Stopped("Source branch is the base or outside the configured prefix")
        plan = PurePosixPath(a.plan)
        if plan.name != "plan.json" or plan.is_absolute() or ".." in plan.parts:
            raise Stopped("Path escapes the repository or is not a plan.json")
        self.git("ls-files", "--error-unmatch", "--", a.plan)
        if self.git("rev-parse", "HEAD") != a.sha:
            raise Stopped("Checkout must be at the approved source SHA")
        self.clean()
        if self.git("config", "--get", "remote.origin.url").removesuffix(".git") not in (
                f"https://github.com/{c['repository']}", f"git@github.com:{c['repository']}"):
            raise Stopped("origin is not the configured trusted GitHub repository")
        if self.remote_tip() != a.sha:
            raise Stopped("Remote branch has advanced beyond the approved source SHA")
        if self.prs():
            raise Stopped("This source branch already has a PR; inspect it instead of creating another")
        version = read_json(Path(c["plugin_dir"]) / ".claude-plugin/plugin.json").get("version", "")
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:\+[\w.-]+)?", version)
        if not match or tuple(map(int, match.groups())) < (1, 2, 0):
            raise Stopped(f"AndThen release >=1.2.0 required; found {version!r}")
        env = os.environ
        if not env.get("CLAUDE_CODE_OAUTH_TOKEN"):
            raise Stopped("CLAUDE_CODE_OAUTH_TOKEN (from `claude setup-token`) is required")
        if env.get("ANTHROPIC_API_KEY") or env.get("ANTHROPIC_AUTH_TOKEN"):
            raise Stopped("ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN would override the subscription token in -p mode; "
                          "remove it from the job")
        self.command(["claude", "auth", "status"], "claude-auth")
        self.command(["gh", "auth", "status"], "github-auth")

    def check_plan(self):
        for story in read_json(self.root / self.args.plan)["stories"]:
            done = story["status"] == "done" and (story.get("verified") or {}).get("summary")
            if not (done or story["status"] == "skipped"):
                raise Stopped(f"Story {story['id']} is neither skipped nor done with a verified summary")

    def agent(self, stage, instruction, review=False):
        (self.run_dir / stage).mkdir(exist_ok=True)
        prompt = (
            f"X12_STAGE={stage}\n{instruction}\n"
            "Do not push, open a PR or change remote state except in the ship stage. Never force-push. "
            "Commit only this run's own changes, by path. Do not leave background jobs running.\n"
            "The requested JSON schema is this wrapper's projection of the skill's actual result. "
            "status: PASS only when all requested work is complete, FAIL for unresolved findings, BLOCKED for missing "
            "input, a permission denial, quota, an unavailable review lens or a decision needed. "
            "revision: the full HEAD SHA. report_paths: absolute native report paths. pr_url: null outside ship. "
            "next_review: true only when the skill printed a 'Next (fresh session):' line asking for another andthen:review run."
        )
        settings = read_json(self.config["settings"])
        if stage != "ship":
            settings.setdefault("permissions", {}).setdefault("deny", []).extend(
                ["Bash(git push *)", "Bash(gh pr create *)", "Bash(gh api *)"])
        # One runaway cap per stage (list-price estimate, not a bill); timeout-minutes bounds the job.
        output = self.command(
            ["claude", "-p", prompt, "--plugin-dir", self.config["plugin_dir"], "--settings", json.dumps(settings),
             "--permission-mode", "auto", "--output-format", "stream-json", "--verbose",
             "--json-schema", json.dumps(SCHEMA), "--max-budget-usd", str(self.config["stage_budget_usd"])], stage)
        events = [json.loads(line) for line in output.splitlines() if line.strip()]
        init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
        plugin_dir = Path(self.config["plugin_dir"]).resolve()
        if not init or not any(p.get("name") == "andthen" and Path(p["path"]).resolve() == plugin_dir
                               for p in init.get("plugins", [])):
            raise Stopped(f"{stage}: the pinned AndThen plugin did not load")
        result = next((e for e in events if e.get("type") == "result"), None)
        if not result or result.get("is_error") or result.get("subtype") != "success":
            raise Stopped(f"{stage}: agent did not finish successfully")
        if result.get("permission_denials"):
            raise Stopped(f"{stage}: a tool permission was denied")
        value = result.get("structured_output") or {}
        if not value.get("status") or value.get("revision") != self.git("rev-parse", "HEAD"):
            raise Stopped(f"{stage}: missing structured stage summary or revision")
        self.state["stages"].append({"name": stage, **value})
        self.save()
        if value["status"] == "BLOCKED" or re.search(r"(?:^|\n)\s*BLOCKED:", result["result"] + "\n" + value["summary"]):
            raise Stopped(f"{stage}: BLOCKED; inspect the stage report")
        if review and not value["report_paths"]:
            raise Stopped(f"{stage}: a native review report is required")
        return {**value, "text": result["result"]}

    def assess(self, value):
        """Read a fix round's native reports: does it ask for a follow-up review, and what stays open?"""
        follow_up = bool(value["next_review"] or re.search(
            r"^[\s*_>-]*Next \(fresh session\):.*review", value["text"], re.M))
        stuck = []
        for report in value["report_paths"]:
            severity, status = report_findings(Path(report).read_text())
            # The Next line's own condition: a CRITICAL/HIGH fixed, or a Fix left partial.
            follow_up = follow_up or "PARTIALLY RESOLVED" in status.values() or any(
                severity.get(n) in ("CRITICAL", "HIGH") and state == "RESOLVED" for n, state in status.items())
            stuck += [str(n) for n in sorted(severity)
                      if severity[n] in ("CRITICAL", "HIGH") and status.get(n) != "RESOLVED"]
        return follow_up, stuck

    def checks(self, label):
        for index, argv in enumerate(self.config["checks"], 1):
            self.command(argv, f"{label}-{index:02d}")
        self.clean()

    def run(self):
        a = self.args
        self.preflight()
        if self.agent("execute", f"Invoke /andthen:exec-plan --auto {a.plan}.")["status"] != "PASS":
            raise Stopped("Plan execution did not pass")
        self.check_plan()
        self.clean()
        # The loop ends on the hand-off, never on the verdict: a Note no fix round may apply can hold it at FAIL.
        previous = ""
        for number in range(1, self.config["max_fix_rounds"] + 1):
            stage = f"fix-{number:02d}"
            follow = f" Follow up the previous report(s): {previous}." if previous else ""
            fixed = self.agent(stage, f"Invoke /andthen:review --mode code,gap,security --fix --auto "
                               f"--output-dir {self.run_dir / stage} {a.plan}.{follow}", review=True)
            self.clean()
            follow_up, stuck = self.assess(fixed)
            if follow_up:
                previous = ", ".join(fixed["report_paths"])
                continue
            if stuck:
                raise Stopped(f"{stage}: CRITICAL/HIGH finding(s) {', '.join(stuck)} stay open "
                              "(DEFERRED, UNRESOLVED or Note); a decision is needed")
            break
        else:
            raise Stopped("Fix-round limit reached while the last round still asked for a follow-up review")
        before = self.git("rev-parse", "HEAD")
        stage = f"review-{number:02d}"
        checked = self.agent(stage, f"Invoke /andthen:review --mode code,gap,security --auto "
                             f"--output-dir {self.run_dir / stage} {a.plan}. "
                             f"Follow up these reports: {', '.join(fixed['report_paths'])}; "
                             "review the work since their revision and the findings still open. "
                             "This confirmation is read-only for the workload tree.", review=True)
        self.clean()
        if self.git("rev-parse", "HEAD") != before:
            raise Stopped("Read-only confirmation changed the workload revision")
        # plan-schema Shipping: no CRITICAL or HIGH finding open (DEFERRED counts as open) and every story
        # done or skipped. The review verdict itself does not gate.
        open_findings = self.assess(checked)[1]
        if open_findings:
            raise Stopped(f"Confirmation review leaves CRITICAL/HIGH finding(s) {', '.join(open_findings)} open; "
                          "no ship until a person decides")
        self.check_plan()
        self.state.update(reviewed_sha=before, fix_rounds=number)
        self.checks("final-check")
        if self.remote_tip() != a.sha:
            raise Stopped("Remote branch advanced during this job; do not force-push")
        if self.prs():
            raise Stopped("A PR appeared during this job; stop instead of duplicating it")
        if not a.publish:
            return self.finish("prepared", reason="All gates passed; ship was not invoked because publish is off")
        shipped = self.agent("ship", f"Invoke /andthen:ship --auto {a.plan}. "
                             f"Explicit authorization: push only this branch {a.branch} to origin "
                             f"and open its PR into {self.config['base']} in {self.config['repository']}. "
                             "Keep the plan bundle and design folders; delete nothing. "
                             "Do not edit implementation or tests. Do not merge. Do not force-push. "
                             "Name the Actions run URL (GITHUB_SERVER_URL/GITHUB_REPOSITORY/GITHUB_RUN_ID) in the PR.")
        self.clean()
        if not (self.root / a.plan).is_file():
            raise Stopped("ship deleted the plan bundle despite the keep instruction")
        self.checks("post-ship-check")
        head = self.git("rev-parse", "HEAD")
        if shipped["status"] != "PASS" or self.remote_tip() != head:
            raise Stopped("ship did not leave the final local revision on the remote branch")
        matching = [pr for pr in self.prs()
                    if pr["state"] == "OPEN" and pr["baseRefName"] == self.config["base"] and pr["headRefOid"] == head]
        if len(matching) != 1 or shipped["pr_url"] != matching[0]["url"]:
            raise Stopped("ship did not produce exactly one open PR into the base at the final revision")
        self.finish("published", pr_url=matching[0]["url"], final_sha=head)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--c2-approved", action="store_true")
    parser.add_argument("--publish", action="store_true")
    pipeline = None
    try:
        pipeline = Pipeline(parser.parse_args(argv))
        pipeline.run()
        return 0
    except Exception as error:  # any failure stops the job with a saved reason
        reason = str(error) if isinstance(error, Stopped) else repr(error)
        if pipeline:
            pipeline.state.update(status="blocked", reason=reason)
            pipeline.save()
        print(f"BLOCKED: {reason}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
