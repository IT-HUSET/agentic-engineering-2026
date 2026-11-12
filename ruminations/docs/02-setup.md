---
title: Setup
tab: Setup
token: setup
order: 2
depends_on: []
---

# Setup

Eyebrow: Setup

## Install AndThen as a Claude Code plugin

Component: "AndThen" in the title is set in the accent colour.

Tell us about your setup, and the steps below show exactly the commands you need. Run them in order.

## Your setup

Interactive component: a muted box titled "Your setup" with two checkboxes. The second is enabled only when the first is ticked. The steps below rebuild whenever one changes.

- Checkbox: AndThen is already installed
- Checkbox: I added it from a tag or `@develop`

## Steps

Component: numbered white cards (01, 02, …), each with title, text and the command in a dark box with a copy button. The command box starts hidden: a small outlined "Show command" button with a terminal icon reveals it, and then reads "Hide command". A revealed box stays open when the steps rebuild. A conditional step has a dashed border and its condition as a tag. Numbers follow the steps actually shown.

1. **Create your own repo.** On GitHub, open the course repo and choose Use this template, then Create a new repository. Pick your account and tick Include all branches. Clone it and work there: your changes are saved, and your pull request opens in your own repo.
   Command: `gh repo clone <your-account>/<your-repo>`
2. **Remove the old marketplace** – only if already installed and added from a tag or `@develop`. A marketplace stays on the ref it was added with, so a tag or @develop has to go before you add the latest release.
   Command: `/plugin marketplace remove andthen`
3. **Update the marketplace** – only if already installed, not from a tag. Fetches the latest AndThen release.
   Command: `/plugin marketplace update andthen`
4. **Update the plugin** – only if already installed, not from a tag. Updates AndThen from the marketplace. Restart Claude Code afterwards.
   Command: `/plugin update andthen@andthen`
5. **Add the AndThen marketplace** – unless you just updated. Tells Claude Code where to find AndThen. It follows the latest release. The course is based on AndThen 1.0.0 and rechecked against 1.1.0, so a later release may differ in details.
   Command: `/plugin marketplace add IT-HUSET/andthen`
6. **Install the plugin** – unless you just updated. Installs the plugin from the marketplace you just added. The name reads plugin@marketplace:
   Component: annotated name, `andthen` labelled "plugin", `@`, `andthen` labelled "marketplace".
   Command: `/plugin install andthen@andthen`
7. **Check your setup.** In a terminal, from the repo root. It checks git, gh, Claude Code with AndThen, and the todo-app tests, and ends on GREEN or RED. Fix every FAIL before Day 1.
   Command: `uv run check.py`
8. **Ask where to start.** When you are unsure where to start, run now-what. It inspects the project and routes you to the right skill.
   Command: `/andthen:now-what`

## Where to type this

Commands that start with `/` are slash commands: type them at the Claude Code prompt in a terminal session started with `claude`, one at a time. The others, such as `uv run check.py`, run in an ordinary terminal from the repo root.

## Troubleshooting

Component: a collapsed details box.

Summary: Adding the marketplace fails with “its source doesn’t match its extraKnownMarketplaces entry”

Your user settings already list a marketplace named `andthen`, pointing at a different source. Open `~/.claude/settings.json` and make that entry match the line you are adding. For the latest release, leave out `ref`:

```json
"extraKnownMarketplaces": {
  "andthen": {
    "source": { "source": "github", "repo": "IT-HUSET/andthen" }
  }
}
```

Then run the steps again from the top.

## AndThen Studio

Eyebrow: Also install

Component: lavender card with a top stripe.

Studio is a visual companion to AndThen. It shows the files AndThen writes as boards you can look through, so specs, plans and decisions are easier to review together. It is one binary that runs on your machine only.

Note (with a lock icon): The repository is private. Ask your facilitator for access if the link gives you a 404.

Install it with the GitHub CLI, signed in (`gh auth login`) with access to the repository. Run the command in a terminal, not in Claude Code. Pick your system:

Interactive component: two small toggle buttons, "macOS / Linux" and "Windows (PowerShell)", selecting which command shows. Default: Windows when the browser reports Windows, otherwise macOS / Linux. The command box starts hidden behind the same "Show command" button as the steps above.

- macOS / Linux: Installs to `~/.local/bin`. If that folder is not on your `PATH`, the script prints the line to add to your shell profile.
  Command: `gh release download -R IT-HUSET/andthen-studio -p install.sh -O - | sh`
- Windows (PowerShell): Installs to `%LOCALAPPDATA%\Programs\andthen-studio` and adds it to your user `PATH`. Open a new terminal afterwards.
  Command: `gh release download -R IT-HUSET/andthen-studio -p install.ps1 -O - | Out-String | Invoke-Expression`

Check it: `andthen_studio --version` prints the installed release.

Button: How to use it in the course → (studio)
Button: [Open AndThen Studio on GitHub →](https://github.com/IT-HUSET/andthen-studio)

## Next

Component: a row of buttons that switch tabs, in tab order. The first is filled, the others are outlined.

- See what andthen:init does → (init)
- Explore the skills → (skills)
- See where AndThen lives → (anatomy)
- Walk the Core Loop → (loop)
- See the other paths → (paths)
- Do the Foundation Lab → (lab)
- Use AndThen Studio → (studio)
