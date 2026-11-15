#!/usr/bin/env python3
"""Coordinate X12 inside a disposable, trusted course devcontainer."""

import argparse
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import signal
import subprocess
import sys
import time


class Stopped(Exception):
    pass


SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "status": {"type": "string", "enum": ["PASS", "FAIL", "BLOCKED"]},
        "summary": {"type": "string"},
        "revision": {"type": "string"},
        "report_paths": {"type": "array", "items": {"type": "string"}},
        "lenses": {
            "type": "object",
            "additionalProperties": False,
            "properties": {name: {"type": "string", "enum": ["PASS", "FAIL", "NOT_RUN"]}
                           for name in ("code", "gap", "security")},
            "required": ["code", "gap", "security"],
        },
        "pr_url": {"type": ["string", "null"]},
    },
    "required": ["status", "summary", "revision", "report_paths", "lenses", "pr_url"],
}


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError) as error:
        raise Stopped(f"Cannot read JSON {path}: {error}") from error


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def report_structure(text):
    lines = []
    fence = None
    for line in text.splitlines():
        if fence:
            if re.fullmatch(r" {0,3}" + re.escape(fence[0]) + "{" + str(fence[1]) + r",}\s*", line):
                fence = None
            continue
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if marker:
            fence = (marker.group(1)[0], len(marker.group(1)))
        else:
            lines.append(line)
    return "\n".join(lines) + "\n"


def relative_file(root, value):
    if not isinstance(value, str) or not value or "\\" in value:
        raise Stopped("A repository-relative POSIX file path is required")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in (".", "..") for part in value.split("/")):
        raise Stopped("Path escapes or dot components are not accepted")
    target = root.joinpath(*path.parts)
    if not target.is_file() or target.is_symlink() or not target.resolve().is_relative_to(root):
        raise Stopped(f"Not a contained regular file: {value}")
    return target


class Pipeline:
    def __init__(self, args):
        self.args = args
        self.root = Path.cwd().resolve()
        self.config = read_json(args.config)
        self.started = time.monotonic()
        self.cost = 0.0
        self.run_dir = None
        self.lock = None
        self.owns_attempt = False
        self.state = {"status": "blocked", "source_sha": args.sha, "branch": args.branch,
                      "plan": args.plan, "workspace": str(self.root),
                      "job_id": os.environ.get("X12_JOB", f"local-{os.getpid()}"), "stages": []}

    def remaining(self):
        seconds = self.config["timeout_seconds"] - (time.monotonic() - self.started)
        if seconds <= 0:
            raise Stopped("Overall runtime limit reached")
        return seconds

    def command(self, argv, *, name=None, check=True):
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"
        # A timed-out agent may have started its own subprocesses.
        proc = subprocess.Popen(argv, cwd=self.root, env=env, text=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                start_new_session=True)
        try:
            out, err = proc.communicate(timeout=self.remaining())
        except (subprocess.TimeoutExpired, Stopped) as error:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                out, err = proc.communicate(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                out, err = proc.communicate()
            if name and self.run_dir:
                (self.run_dir / f"{name}.stdout").write_text(out)
                (self.run_dir / f"{name}.stderr").write_text(err)
            message = f"Runtime limit reached during {name or argv[0]}" if isinstance(error, subprocess.TimeoutExpired) else str(error)
            raise Stopped(message) from error
        if name and self.run_dir:
            (self.run_dir / f"{name}.stdout").write_text(out)
            (self.run_dir / f"{name}.stderr").write_text(err)
        if check and proc.returncode:
            raise Stopped(f"{name or argv[0]} exited {proc.returncode}; inspect retained logs")
        return proc.returncode, out, err

    def git(self, *args):
        return self.command(["git", *args])[1].strip()

    def save(self):
        if self.run_dir:
            self.state["cost_usd"] = self.cost
            write_json(self.run_dir / "status.json", self.state)

    def validate_config(self):
        c = self.config
        if not isinstance(c, dict) or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", c.get("repository", "")):
            raise Stopped("Configure the single trusted repository")
        for field in ("base", "branch_prefix", "plugin_dir", "settings", "state_dir"):
            if not isinstance(c.get(field), str) or not c[field]:
                raise Stopped(f"Missing configuration: {field}")
        for field in ("timeout_seconds", "max_budget_usd", "stage_budget_usd"):
            number = c.get(field)
            if isinstance(number, bool) or not isinstance(number, (int, float)) or not math.isfinite(number) or number <= 0:
                raise Stopped(f"{field} must be a positive number")
        rounds = c.get("max_fix_rounds")
        if type(rounds) is not int or not 1 <= rounds <= 3:
            raise Stopped("max_fix_rounds must be between 1 and 3")
        checks = c.get("checks")
        if not isinstance(checks, list) or not checks or any(
            not isinstance(cmd, list) or not cmd or any(not isinstance(arg, str) or not arg for arg in cmd)
            for cmd in checks
        ):
            raise Stopped("Configure nonempty argv arrays for the real final checks")
        if type(c.get("publish_enabled")) is not bool:
            raise Stopped("publish_enabled must be a boolean")
        for field in ("plugin_dir", "settings", "state_dir"):
            if not Path(c[field]).is_absolute() or Path(c[field]).resolve().is_relative_to(self.root):
                raise Stopped(f"{field} must be an absolute path outside the workload repo")
        if not Path(c["settings"]).is_file():
            raise Stopped("The controlled permission-settings file is missing")
        manifest = read_json(Path(c["plugin_dir"]) / ".claude-plugin/plugin.json")
        if not isinstance(manifest, dict):
            raise Stopped("Plugin manifest must be an object")
        version = manifest.get("version", "")
        match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:\+[A-Za-z0-9.-]+)?", version)
        if manifest.get("name") != "andthen" or not match or tuple(map(int, match.groups())) < (1, 2, 0):
            raise Stopped(f"AndThen release >=1.2.0 required; found {version!r}")
        for skill in ("exec-plan", "review", "ship"):
            if not (Path(c["plugin_dir"]) / "skills" / skill / "SKILL.md").is_file():
                raise Stopped(f"Missing AndThen skill: {skill}")
        self.state["andthen_version"] = version

    def acquire(self):
        state_dir = Path(self.config["state_dir"])
        state_dir.mkdir(parents=True, exist_ok=True)
        branch_key = hashlib.sha256(f"{self.config['repository']}:{self.args.branch}".encode()).hexdigest()[:20]
        self.lock = (state_dir / f"{branch_key}.lock").open("a+")
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise Stopped("Another job holds this repository/branch lock") from error
        run_key = hashlib.sha256(f"{branch_key}:{self.args.sha}:{self.args.plan}".encode()).hexdigest()[:20]
        self.run_dir = state_dir / "runs" / run_key
        if self.run_dir.exists():
            previous = read_json(self.run_dir / "status.json")
            if not isinstance(previous, dict):
                raise Stopped("Existing attempt status is malformed; inspect it")
            if previous.get("status") == "published":
                self.state = previous
                print(json.dumps(previous))
                return False
            raise Stopped(f"Existing attempt preserved at {self.run_dir}; inspect it before a new source commit")
        self.run_dir.mkdir(parents=True)
        self.owns_attempt = True
        self.save()
        return True

    def remote_tip(self, branch):
        output = self.git("ls-remote", "--exit-code", "origin", f"refs/heads/{branch}")
        lines = output.splitlines()
        if len(lines) != 1 or not re.fullmatch(r"[0-9a-f]{40}\s+refs/heads/" + re.escape(branch), lines[0]):
            raise Stopped(f"Cannot resolve one remote tip for {branch}")
        return lines[0].split()[0]

    def prs(self):
        output = self.command(["gh", "pr", "list", "--repo", self.config["repository"],
                               "--head", self.args.branch, "--state", "all", "--limit", "100",
                               "--json", "url,state,headRefName,baseRefName,headRefOid,isCrossRepository"])[1]
        try:
            value = json.loads(output)
        except ValueError as error:
            raise Stopped("Invalid GitHub PR metadata") from error
        if not isinstance(value, list) or any(not isinstance(pr, dict) for pr in value):
            raise Stopped("Invalid GitHub PR metadata")
        return value

    def validate_input(self):
        a, c = self.args, self.config
        if not a.c2_approved:
            raise Stopped("C2 approval for this source SHA is required")
        if not re.fullmatch(r"[0-9a-f]{40}", a.sha):
            raise Stopped("A full lowercase 40-character source SHA is required")
        self.git("check-ref-format", "--branch", a.branch)
        if a.branch == c["base"] or not a.branch.startswith(c["branch_prefix"]) or a.base != c["base"]:
            raise Stopped("Source branch or PR base is outside the configured course scope")
        if self.git("rev-parse", "--show-toplevel") != str(self.root):
            raise Stopped("Run from the workload repository root")
        if self.git("branch", "--show-current") != a.branch or self.git("rev-parse", "HEAD") != a.sha:
            raise Stopped("Checkout must be on the requested source branch at the pinned SHA")
        self.clean()
        origin = self.git("config", "--get", "remote.origin.url")
        allowed = {f"https://github.com/{c['repository']}.git", f"https://github.com/{c['repository']}",
                   f"git@github.com:{c['repository']}.git"}
        if origin not in allowed:
            raise Stopped("origin is not the configured trusted GitHub repository")
        if self.remote_tip(a.branch) != a.sha:
            raise Stopped("Remote branch has advanced beyond the approved source SHA")
        self.git("ls-remote", "--exit-code", "origin", f"refs/heads/{a.base}")
        if self.prs():
            raise Stopped("This source branch already has a PR; inspect it instead of creating another")
        self.initial_plan = self.plan(complete=False)
        if self.initial_plan.get("shipped"):
            raise Stopped("Plan is already marked shipped; inspect the prior attempt")

    def clean(self):
        if self.git("status", "--porcelain", "--untracked-files=all"):
            raise Stopped("Workload tree is dirty; owned work is retained, not discarded")
        if self.git("branch", "--show-current") != self.args.branch:
            raise Stopped("The workload changed branches")
        self.git("merge-base", "--is-ancestor", self.args.sha, "HEAD")

    def plan(self, complete):
        path = relative_file(self.root, self.args.plan)
        if path.name != "plan.json":
            raise Stopped("The plan input must name plan.json")
        self.git("ls-files", "--error-unmatch", "--", self.args.plan)
        value = read_json(path)
        stories = value.get("stories") if isinstance(value, dict) else None
        if not isinstance(stories, list) or not stories:
            raise Stopped("Plan must contain stories")
        ids = set()
        for story in stories:
            if not isinstance(story, dict) or not isinstance(story.get("id"), str) or story["id"] in ids:
                raise Stopped("Plan story IDs must be present and unique")
            ids.add(story["id"])
            fis = story.get("fis")
            if not isinstance(fis, str) or not re.fullmatch(r"s\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md", fis):
                raise Stopped("Every story needs a canonical FIS basename before handoff")
            relative = str(PurePosixPath(self.args.plan).parent / fis)
            relative_file(self.root, relative)
            self.git("ls-files", "--error-unmatch", "--", relative)
            status = story.get("status")
            if status not in ("pending", "in-progress", "done", "skipped"):
                raise Stopped("Unsupported plan story status")
            verified = story.get("verified")
            if complete and (status not in ("done", "skipped") or
                             status == "done" and (not isinstance(verified, dict) or not isinstance(verified.get("summary"), str) or not verified["summary"])):
                raise Stopped("Plan has unfinished or unattested stories")
        if complete:
            old = {s["id"]: s for s in self.initial_plan["stories"]}
            if ids != set(old) or any(s["status"] == "skipped" and old[s["id"]]["status"] != "skipped" for s in stories):
                raise Stopped("Run changed the approved story set or cut a story from scope")
        return value

    def agent(self, stage, instruction, *, review=False):
        budget = min(self.config["stage_budget_usd"], self.config["max_budget_usd"] - self.cost)
        if budget <= 0:
            raise Stopped("Total model budget reached")
        output_dir = self.run_dir / stage
        output_dir.mkdir()
        prompt = (
            f"X12_STAGE={stage}\n{instruction}\n"
            f"Write native review reports, when requested, only under {output_dir}.\n"
            "Do not push, open a PR or modify remote state except in the ship stage. Never force-push. "
            "Do not alter the approved story set or mark pending stories skipped. "
            "Commit only this run's owned changes by path. Do not modify runtime/control/config/state files. "
            "Do not leave background jobs running.\n"
            "The requested JSON schema is this lab wrapper's projection, not an AndThen interface. "
            "After the skill returns, project its actual report: status PASS only when all requested work is complete, "
            "FAIL for unresolved findings, BLOCKED for missing input, permission denial, quota or decision needed. "
            "Never claim PASS when a required lens/check is unavailable. "
            "revision is the full current HEAD SHA; report_paths are absolute native report paths; "
            "lenses contains code/gap/security verdicts, NOT_RUN outside review; pr_url is null outside ship. "
            "Preserve ASSUMPTION, Note and DEFERRED details in the native reports and summary."
        )
        settings = read_json(self.config["settings"])
        if not isinstance(settings, dict) or not isinstance(settings.get("permissions", {}), dict):
            raise Stopped("Controlled permission settings must be an object")
        denies = settings.get("permissions", {}).get("deny", [])
        if not isinstance(denies, list) or any(not isinstance(rule, str) for rule in denies):
            raise Stopped("Controlled permission deny rules must be strings")
        if stage != "ship":
            settings.setdefault("permissions", {}).setdefault("deny", []).extend([
                "Bash(git push *)", "Bash(gh pr create *)", "Bash(gh api *)",
            ])
        argv = ["claude", "-p", prompt, "--plugin-dir", self.config["plugin_dir"],
                "--settings", json.dumps(settings), "--permission-mode", "dontAsk",
                "--output-format", "stream-json", "--verbose", "--json-schema", json.dumps(SCHEMA),
                "--max-budget-usd", str(budget)]
        _, output, _ = self.command(argv, name=stage)
        try:
            events = [json.loads(line) for line in output.splitlines() if line.strip()]
        except ValueError as error:
            raise Stopped(f"{stage}: malformed Claude event output") from error
        if any(not isinstance(event, dict) for event in events):
            raise Stopped(f"{stage}: Claude events must be objects")
        init = next((e for e in events if e.get("type") == "system" and e.get("subtype") == "init"), None)
        if not init or any(init.get(field) for field in ("plugin_errors", "mcp_server_errors")):
            raise Stopped(f"{stage}: missing init metadata or plugin/MCP startup error")
        loaded = init.get("plugins", [])
        if not isinstance(loaded, list) or any(not isinstance(plugin, dict) or
            not isinstance(plugin.get("name"), str) or not isinstance(plugin.get("path"), str) for plugin in loaded):
            raise Stopped(f"{stage}: malformed plugin metadata")
        andthen = [p for p in loaded if p.get("name") == "andthen"]
        if len(andthen) != 1 or Path(andthen[0].get("path", "")).resolve() != Path(self.config["plugin_dir"]).resolve():
            raise Stopped(f"{stage}: the pinned AndThen plugin did not load")
        servers = init.get("mcp_servers", [])
        if not isinstance(servers, list) or any(not isinstance(server, dict) for server in servers):
            raise Stopped(f"{stage}: malformed MCP metadata")
        if any(server.get("status") not in ("connected", "disabled") for server in servers):
            raise Stopped(f"{stage}: an MCP server was unavailable")
        results = [e for e in events if e.get("type") == "result"]
        if len(results) != 1 or results[0].get("is_error") or results[0].get("subtype") != "success":
            raise Stopped(f"{stage}: agent did not finish successfully")
        result = results[0]
        if not isinstance(result.get("result"), str):
            raise Stopped(f"{stage}: malformed result text")
        if result.get("permission_denials"):
            raise Stopped(f"{stage}: a tool permission was denied")
        cost = result.get("total_cost_usd")
        if isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost < 0:
            raise Stopped(f"{stage}: missing model-cost metadata")
        self.cost += cost
        value = result.get("structured_output")
        if not isinstance(value, dict) or set(value) != set(SCHEMA["required"]):
            raise Stopped(f"{stage}: missing or malformed structured stage summary")
        if (value["status"] not in ("PASS", "FAIL", "BLOCKED") or
            not isinstance(value["summary"], str) or not value["summary"] or
            value["revision"] != self.git("rev-parse", "HEAD") or
            not isinstance(value["report_paths"], list) or any(not isinstance(p, str) for p in value["report_paths"]) or
            not isinstance(value["lenses"], dict) or set(value["lenses"]) != {"code", "gap", "security"} or
            any(v not in ("PASS", "FAIL", "NOT_RUN") for v in value["lenses"].values())):
            raise Stopped(f"{stage}: invalid stage summary or revision")
        if value["pr_url"] is not None and not isinstance(value["pr_url"], str):
            raise Stopped(f"{stage}: invalid PR URL")
        self.state["stages"].append({"name": stage, **value})
        self.save()
        if value["status"] == "BLOCKED" or re.search(r"(?:^|\n)\s*BLOCKED:", result.get("result", "") + "\n" + value["summary"]):
            raise Stopped(f"{stage}: BLOCKED; inspect the stage report")
        if review:
            if not value["report_paths"] or any(v == "NOT_RUN" for v in value["lenses"].values()):
                raise Stopped(f"{stage}: all three review lenses and a native report are required")
            for report in value["report_paths"]:
                path = Path(report)
                if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(output_dir):
                    raise Stopped(f"{stage}: native report missing or outside its output directory")
        return value

    def checks(self, label):
        for index, argv in enumerate(self.config["checks"], 1):
            self.command(argv, name=f"{label}-{index:02d}")
        self.clean()

    def snapshot_review(self, summary):
        revision = self.state["reviewed_sha"]
        parent = relative_file(self.root, self.args.plan).parent / "x12-review-evidence"
        if parent.is_symlink() or not parent.resolve().is_relative_to(self.root):
            raise Stopped("Review evidence directory escapes the workload")
        parent.mkdir(exist_ok=True)
        target = parent / f"{revision}.md"
        if target.exists():
            raise Stopped("Review evidence snapshot already exists; do not overwrite it")
        run_id = os.environ.get("GITHUB_RUN_ID", "")
        run_url = (f"https://github.com/{self.config['repository']}/actions/runs/{run_id}"
                   if run_id.isdigit() else "Not running in GitHub Actions")
        text = ["# X12 review evidence", "", f"**Reviewed revision**: {revision}",
                f"**Approved source**: {self.args.sha}", f"**Run**: {run_url}", "",
                "This snapshot is the only post-review change before the final checks. "
                "The native reports below bind the reviewed code revision. "
                "ship may subsequently commit its documented metadata changes.", "",
                "## Required final checks", "",
                "The wrapper runs these argv commands after committing this snapshot. "
                "Actual stdout, stderr and stage status are retained with the Actions run.", ""]
        text.extend(f"- `{json.dumps(cmd)}`" for cmd in self.config["checks"])
        for index, report in enumerate(summary["report_paths"], 1):
            text.extend(["", f"## Native confirmation report {index}", "", Path(report).read_text()])
        target.write_text("\n".join(text) + "\n")
        relative = str(target.relative_to(self.root))
        self.git("add", "--", relative)
        self.git("commit", "-m", "Record review evidence", "--", relative)
        changed = self.git("diff", "--name-only", revision, "HEAD").splitlines()
        if changed != [relative]:
            raise Stopped("Evidence commit changed more than its one owned snapshot")
        self.state["evidence_path"] = relative
        self.state["evidence_sha"] = self.git("rev-parse", "HEAD")
        self.save()

    def run(self):
        self.validate_config()
        if not self.acquire():
            return 0
        self.validate_input()
        self.command(["claude", "auth", "status"], name="claude-auth")
        self.command(["gh", "auth", "status"], name="github-auth")
        self.state["status"] = "running"
        self.save()
        value = self.agent("execute", f"Invoke /andthen:exec-plan --auto {self.args.plan}.")
        if value["status"] != "PASS":
            raise Stopped("Plan execution did not pass")
        self.plan(complete=True)
        self.clean()
        previous = ""
        for number in range(1, self.config["max_fix_rounds"] + 1):
            follow = f" Follow up the previous report(s): {previous}." if previous else ""
            fixed = self.agent(f"fix-{number:02d}",
                               f"Invoke /andthen:review --mode code,gap,security --fix --auto "
                               f"--output-dir {self.run_dir / f'fix-{number:02d}'} {self.args.plan}.{follow}", review=True)
            self.clean()
            before = self.git("rev-parse", "HEAD")
            checked = self.agent(f"review-{number:02d}",
                                 f"Invoke /andthen:review --mode code,gap,security --auto "
                                 f"--output-dir {self.run_dir / f'review-{number:02d}'} {self.args.plan}. "
                                 f"Follow up these reports: {', '.join(fixed['report_paths'])}. "
                                 "This confirmation is read-only for the workload tree.", review=True)
            self.clean()
            if self.git("rev-parse", "HEAD") != before:
                raise Stopped("Read-only confirmation changed the workload revision")
            for report in checked["report_paths"]:
                content = report_structure(Path(report).read_text())
                revision = re.search(r"^\*\*Revision\*\*:\s*([0-9a-f]{7,40})(-dirty)?\s*$", content, re.M)
                if not revision or revision.group(2) or not before.startswith(revision.group(1)):
                    raise Stopped("Confirmation report does not bind the current clean revision")
                if checked["status"] == "PASS":
                    chain = re.search(r"^\*\*Resolved chain\*\*:\s*(.+)$", content, re.M)
                    verdict = content.split("\n## Verdict\n", 1)
                    verdict_text = verdict[1].split("\n## ", 1)[0] if len(verdict) == 2 else ""
                    if (not chain or set(re.findall(r"code|gap|security|outcome", chain.group(1))) != {"code", "gap", "security"}
                        or not re.search(r"\*\*Overall readiness: PASS\*\*", verdict_text)
                        or re.search(r"\bFAIL\b", verdict_text)):
                        raise Stopped("Native confirmation report does not establish the three-lens PASS")
            if checked["status"] == "PASS" and all(v == "PASS" for v in checked["lenses"].values()):
                self.state["reviewed_sha"] = before
                break
            previous = ", ".join(checked["report_paths"])
        else:
            raise Stopped("Review/fix round limit reached without three passing lenses")
        self.plan(complete=True)
        self.snapshot_review(checked)
        self.checks("final-check")
        if self.remote_tip(self.args.branch) != self.args.sha:
            raise Stopped("Remote branch advanced during this job; do not force-push")
        if self.prs():
            raise Stopped("A PR appeared during this job; stop instead of duplicating it")
        if not self.args.publish or not self.config["publish_enabled"]:
            self.state["status"] = "prepared"
            self.state["reason"] = "All local gates passed; ship was not invoked because publishing is disabled"
            self.save()
            print(json.dumps(self.state))
            return 0
        self.state["status"] = "shipping"
        self.save()
        shipped = self.agent("ship", f"Invoke /andthen:ship --auto {self.args.plan}. "
                             f"Explicit authorization: push only this branch {self.args.branch} to origin "
                             f"and open its PR into {self.args.base} in {self.config['repository']}. "
                             "Keep the entire plan bundle and all design folders. Do not delete them. "
                             "Keep existing review evidence. Do not edit implementation or tests. "
                             "Do not merge. Do not force-push. "
                             f"The approved review read {self.state['reviewed_sha']}; report paths and actual checks "
                             f"are retained in {self.run_dir}. The committed native review snapshot is "
                             f"{self.state['evidence_path']}; commit {self.state['evidence_sha']} only adds that "
                             "post-review documentation, and final checks ran afterwards. Link the snapshot, "
                             "quote actual final-check output, and disclose any later changes. "
                             "Include these facts and the Actions run URL, "
                             "when available in GITHUB_SERVER_URL/GITHUB_REPOSITORY/GITHUB_RUN_ID, in the PR. "
                             "If origin advanced since the source SHA, stop; do not overwrite it.")
        self.plan(complete=True)
        self.clean()
        self.checks("post-ship-check")
        head = self.git("rev-parse", "HEAD")
        if shipped["status"] != "PASS" or self.remote_tip(self.args.branch) != head:
            raise Stopped("ship did not leave the final local revision on the remote branch")
        prs = self.prs()
        expected_url = f"https://github.com/{self.config['repository']}/pull/"
        matching = [pr for pr in prs if pr.get("state") == "OPEN" and pr.get("headRefName") == self.args.branch
                    and pr.get("baseRefName") == self.args.base and pr.get("headRefOid") == head
                    and pr.get("isCrossRepository") is False
                    and isinstance(pr.get("url"), str) and re.fullmatch(re.escape(expected_url) + r"\d+", pr["url"])]
        if len(matching) != 1 or shipped["pr_url"] != matching[0]["url"]:
            raise Stopped("ship did not produce one verified PR with the expected repository, base, head and revision")
        self.state.update(status="published", pr_url=matching[0]["url"], final_sha=head)
        self.save()
        print(json.dumps(self.state))
        return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--plan", required=True)
    parser.add_argument("--base", required=True)
    parser.add_argument("--c2-approved", action="store_true")
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args(argv)
    def canceled(_signum, _frame):
        raise Stopped("Controller canceled; owned work and evidence retained")
    signal.signal(signal.SIGTERM, canceled)
    signal.signal(signal.SIGINT, canceled)
    pipeline = None
    try:
        pipeline = Pipeline(args)
        return pipeline.run()
    except (Stopped, OSError, ValueError, TypeError, KeyError) as error:
        if pipeline and pipeline.owns_attempt:
            pipeline.state.update(status="blocked", reason=str(error))
            pipeline.save()
        print(f"BLOCKED: {error}", file=sys.stderr)
        return 1
    finally:
        if pipeline and pipeline.lock:
            pipeline.lock.close()


if __name__ == "__main__":
    sys.exit(main())
