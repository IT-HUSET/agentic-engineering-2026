# /// script
# requires-python = ">=3.9"
# ///
"""Setup check for the course. Run from the repo root: uv run check.py

Green means: git, gh signed in, one host (Claude Code, Codex CLI or
GitHub Copilot CLI) installed and signed in with AndThen 1.x, and the
todo-app tests pass. Works on macOS, Linux, WSL and in the dev container.
"""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
failures = 0


def ok(msg):
    print(f"  ok    {msg}")


def info(msg):
    print(f"  --    {msg}")


def fail(msg):
    global failures
    failures += 1
    print(f"  FAIL  {msg}")


# `uv run check.py` sets VIRTUAL_ENV; drop it so todo-app uses its own .venv.
ENV = {k: val for k, val in os.environ.items() if k != "VIRTUAL_ENV"}


def run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180, cwd=cwd, env=ENV)
        return r.returncode, (r.stdout + r.stderr).strip()
    except (OSError, subprocess.TimeoutExpired) as e:
        return 1, str(e)


def first_line(text):
    return text.splitlines()[0] if text else ""


def version_token(text):
    for token in first_line(text).split():
        if token[:1].isdigit() and "." in token:
            return token.rstrip(".")
    return "version unknown"


def andthen_version(entries, id_key):
    for e in entries:
        if e.get(id_key) == "andthen@andthen" and e.get("enabled", True):
            return e.get("version")
    return None


def andthen_claude(exe):
    code, out = run([exe, "plugin", "list", "--json"])
    if code != 0:
        return None
    try:
        return andthen_version(json.loads(out), "id")
    except (ValueError, AttributeError):
        return None


def andthen_codex(exe):
    code, out = run([exe, "plugin", "list", "--json"])
    if code != 0:
        return None
    try:
        return andthen_version(json.loads(out).get("installed", []), "pluginId")
    except (ValueError, AttributeError):
        return None


def andthen_copilot(exe):
    code, out = run([exe, "plugin", "list"])
    if code != 0:
        return None
    for line in out.splitlines():
        if "andthen@andthen" in line:
            m = re.search(r"v?(\d+\.\d+\.\d+)", line)
            return m.group(1) if m else "installed"
    return None


# name, executable, sign-in command (None = cannot be checked), AndThen lookup, install hint
HOSTS = [
    ("Claude Code", "claude", ["auth", "status"], andthen_claude,
     "run 'claude' and follow the browser login"),
    ("Codex CLI", "codex", ["login", "status"], andthen_codex,
     "run 'codex login'"),
    ("Copilot CLI", "copilot", None, andthen_copilot,
     "start 'copilot' and run /login if it asks"),
]


def check_host(name, exe_name, auth_args, andthen_lookup, login_hint):
    exe = shutil.which(exe_name)
    if not exe:
        return None
    code, out = run([exe, "--version"])
    version = version_token(out) if code == 0 else "version unknown"
    signed_in = True
    if auth_args:
        code, _ = run([exe, *auth_args])
        signed_in = code == 0
    plugin = andthen_lookup(exe)

    problems = []
    if not signed_in:
        problems.append(f"not signed in: {login_hint}")
    if not plugin:
        problems.append("AndThen not installed: see the README, step 2")
    elif plugin[:1] == "0":
        problems.append(f"AndThen {plugin} is a 0.x release: update to the latest release")

    label = f"{name} {version}, AndThen {plugin or 'missing'}"
    if not auth_args:
        label += " (sign-in not checked)"
    return label, problems


print("Agentic Software Engineering 2026: setup check")

v = sys.version_info
ok(f"Python {v.major}.{v.minor}.{v.micro}")

if shutil.which("git"):
    ok(first_line(run(["git", "--version"])[1]))
else:
    fail("git not on PATH")

if not shutil.which("gh"):
    fail("gh (GitHub CLI) not on PATH: https://cli.github.com, then 'gh auth login'")
elif run(["gh", "auth", "status"])[0] == 0:
    ok("gh signed in")
else:
    fail("gh not signed in: run 'gh auth login'")

ready = []
for host in HOSTS:
    result = check_host(*host)
    if result is None:
        info(f"{host[0]} not installed (one host is enough)")
        continue
    label, problems = result
    if problems:
        info(f"{label}: " + "; ".join(problems))
    else:
        ok(label)
        ready.append(label)
if not ready:
    fail("no host is ready: install Claude Code, Codex CLI or Copilot CLI, sign in and install AndThen")

tests = "not run"
app = ROOT / "todo-app"
if not shutil.which("uv"):
    fail("uv not on PATH: https://docs.astral.sh/uv/getting-started/installation/")
elif not app.is_dir():
    fail("todo-app/ not found: run this from the root of your repo")
else:
    code, out = run(["uv", "run", "pytest", "-q"], cwd=app)
    lines = [ln for ln in out.splitlines() if " passed" in ln or " failed" in ln or " error" in ln]
    tests = lines[-1].strip() if lines else first_line(out)
    if code == 0:
        ok(f"todo-app tests pass ({tests})")
    else:
        fail("todo-app tests fail: run 'uv run pytest -q' in todo-app/ to see why")

print()
if failures == 0:
    print("GREEN: ready for Day 1.")
    print("Next: start your host in todo-app/ and ask 'What does this app do? Answer in three lines.'")
else:
    print(f"RED: {failures} thing(s) to fix above. Stuck? Use the dev container (see README).")
sys.exit(1 if failures else 0)
