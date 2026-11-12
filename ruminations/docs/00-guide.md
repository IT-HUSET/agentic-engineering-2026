---
title: AndThen Guide
version: 1.55
date: 2026-11-12
status: published
html: html/andthen-guide.html
artifact: https://claude.ai/artifact/HAVpWj74fHd8ZMU5xyUJyT
description: Course guide to AndThen: setup, what andthen:init does step by step, a clickable map of all 21 skills, the Core Loop from idea to pull request, the other paths and what each step leaves behind, the Foundation Lab step by step, where AndThen Studio helps along the way, where every part of AndThen lives, and, on a side tab, where Claude's memory lives and how to manage it.
icon: workflow
tabs: [01-start, 02-setup, 03-init, 04-skills, 05-anatomy, 06-core-loop, 07-paths, 08-foundation-lab, 09-studio, 10-memory]
depends_on: [shared/skills.md, shared/icons.md]
---

# AndThen Guide

The frame around the ten tabs. One HTML page, one tab per markdown file, in the order of `tabs` above. The last tab, Claude’s memory, is a side track about Claude Code rather than AndThen, so it sits after the AndThen tabs. The Swedish page has the same frame, from `docs/sv/00-guide.md`.

## Header

- Logo: IT-HUSET wordmark, black on light, white on dark.
- Meta text, right-aligned: Agentic Engineering 2026 · AndThen
- Language switch, right of the meta text: EN and SV as a two-part pill, the current language filled. EN opens `html/andthen-guide.html`, SV opens `html/andthen-guide.sv.html`, the same page in Swedish built from `docs/sv/`. The switch keeps the open tab (its token goes along in the link), and the browser remembers the choice (localStorage), so the next visit opens in that language. Ticks in the Foundation Lab checklist are shared by both languages.

## Tabs

Component: a tab bar under the header. Before the tabs, once for all of them, a small "AndThen" label in the display font and accent colour, set off by a thin divider; the tab labels leave the word out. Each tab's label is the `tab` field of its file, and its link token is the `token` field, so `#init` in the artifact link opens that tab. The first tab opens when there is no token. Left and right arrow keys move between tabs. The active tab has a rust underline. The last tab, Claude’s memory, is a side track about Claude Code, so a thin vertical line, the same colour as the divider after the label, sets it apart from the AndThen tabs. On a narrow screen the tab bar scrolls sideways in its own row, and the active tab is scrolled into view.

## Footer

Component: forest-green band with the white logo.

Built on [AndThen](https://github.com/IT-HUSET/andthen) · spec-driven agentic engineering
