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

Tell us about your setup, and the steps below show exactly the commands you need. Copy each one into Claude Code in order.

## Your setup

Interactive component: a muted box titled "Your setup" with two controls. The steps below rebuild whenever one changes.

- Checkbox: I have an older AndThen (0.x) installed
- Text field: Release tag from your facilitator, shown as `v1.0.0-rc.` followed by a short field for N (digits only, placeholder N). Empty means the course branch `develop`.

## Steps

Component: numbered white cards (01, 02, …), each with title, text and the command in a dark box with a copy button. The command box starts hidden: a small outlined "Show command" button with a terminal icon reveals it, and then reads "Hide command". A revealed box stays open when the steps rebuild. A conditional step has a dashed border and the tag "only if you have 0.x". Numbers follow the steps actually shown.

1. **Remove the old version** — only when the 0.x checkbox is ticked. AndThen 0.x and 1.0 share the marketplace name andthen, so the old marketplace has to go first.
   Command: `/plugin marketplace remove andthen`
2. **Add the AndThen marketplace.**
   - With no tag: Tells Claude Code where to find AndThen. @develop follows the course branch. If your facilitator gives you a release tag, enter it above.
     Command: `/plugin marketplace add IT-HUSET/andthen@develop`
   - With tag N: Tells Claude Code where to find AndThen, pinned to the release your facilitator gave you.
     Command: `/plugin marketplace add IT-HUSET/andthen@v1.0.0-rc.N`
3. **Install the plugin.** Installs the plugin from the marketplace you just added. The name reads plugin@marketplace:
   Component: annotated name, `andthen` labelled "plugin", `@`, `andthen` labelled "marketplace".
   Command: `/plugin install andthen@andthen`
4. **Ask where to start.** When you are unsure where to start, run now-what. It inspects the project and routes you to the right skill.
   Command: `/andthen:now-what`

## Where to type this

These are slash commands. Type them at the Claude Code prompt in a terminal session started with `claude`, one at a time.

## Troubleshooting

Component: a collapsed details box.

Summary: Adding the marketplace fails with “its source doesn’t match its extraKnownMarketplaces entry”

Your user settings already list a marketplace named `andthen`, pointing at a different source. Open `~/.claude/settings.json` and make that entry match the line you are adding. For the course branch, add `"ref": "develop"`:

```json
"extraKnownMarketplaces": {
  "andthen": {
    "source": { "source": "github", "repo": "IT-HUSET/andthen", "ref": "develop" }
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
