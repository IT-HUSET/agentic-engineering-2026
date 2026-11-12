---
title: AndThen Skills
tab: Skills
token: skills
order: 4
depends_on: [shared/skills.md, shared/icons.md]
---

# AndThen Skills

Eyebrow: AndThen skills · {andthen_version}

## Overview of the {skill_count} skills of AndThen

Each box is a skill, grouped by the job it does. Click one to see what it reads, what it writes and which skills it works with.

Component: legend with five items: Skill (solid box) · Optional step (dashed box) · Artifact it writes (document chip) · Hand-off (arrow) · You (filled dot).

## Skill map

Interactive component: C4-style container map, 1280 × 605, inside a scrolling card. A person "You [developer]" stands outside the dashed AndThen boundary (labelled "ANDTHEN · CLAUDE CODE PLUGIN · {skill_count} SKILLS"). Each group is a tinted band with its label in capitals. Skills sit at their Map position from shared/skills.md; optional skills have a dashed border; Core Loop skills carry their Document chip beneath them on a dotted line. Clicking a skill selects it, highlights the skills in its Works with list and dims the rest; arrows touching it stay lit. Keyboard: Tab and Enter.

Hint below 960 px: Scroll sideways to see the whole map.

### Bands

| Group | x | y | Width | Height | Label |
| - | - | - | - | - | - |
| start | 195 | 40 | 505 | 100 | START & SESSION |
| share | 720 | 40 | 525 | 100 | SHARE & TRACK |
| design | 195 | 160 | 1050 | 100 | DESIGN & DISCOVERY · OPTIONAL, INFORMS PLAN |
| core | 195 | 290 | 1050 | 150 | CORE LOOP · EACH STEP WRITES WHAT THE NEXT ONE READS |
| quality | 195 | 465 | 625 | 100 | QUALITY · USED BY EXEC-PLAN AND REVIEW |
| fix | 840 | 465 | 405 | 100 | FIX PATH · A ONE-SENTENCE FIX |

### Arrows

From and To are skill ids, `you` for the person, or `group:<id>` for a whole band. Path is SVG path data on the map.

| From | To | Path | Label |
| - | - | - | - |
| you | now-what | `M142 99 H211` | asks (at 177, 91) |
| clarify | decide | `M357 350 H385` |  |
| decide | plan | `M531 350 H559` |  |
| plan | exec-plan | `M705 350 H733` |  |
| exec-plan | review | `M879 350 H907` |  |
| review | ship | `M1053 350 H1081` |  |
| group:design | plan | `M633 262 V314` | informs (at 662, 285) |
| triage | implement-fix | `M1022 524 H1056` |  |
| implement-fix | ship | `M1227 524 H1255 V350 H1229` |  |

## Selected skill

Component: detail card under the map, tinted by the skill’s group. Shows group (and "optional"), the skill name in mono, its Role, Summary and When, then a Result box with the icon, title and text, Reads, the Command with a copy button, and "Works with" as buttons that select that skill. Starts on plan. Each command box starts hidden behind a "Show command" button, as on the Setup tab.

## All {skill_count} skills and what they produce

Eyebrow: Overview

Component: table with one row per skill in map order: Skill (button that selects it on the map and scrolls up; "optional" under the name when it applies) · Group (dot in the group tint and the label) · Result (icon and title) · What you get (the Result text). The selected skill’s row is tinted.
