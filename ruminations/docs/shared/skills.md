---
title: AndThen skills
andthen_version: 1.1.0
source: ~/.claude/plugins/marketplaces/andthen/plugin/skills/*/SKILL.md
used_by: [03-init, 04-skills, 06-core-loop]
---

# AndThen skills

The registry of every skill in AndThen 1.1.0. The number of skills shown on the page is counted from this file, never typed by hand.

## Groups

Order is the order on the skill map and in the overview table. Tint names refer to the tint tokens in the contract.

| Id | Label | Tint |
| - | - | - |
| start | Start & session | cream |
| share | Share & track | teal |
| design | Design & discovery | lav |
| core | Core Loop | rust |
| quality | Quality | green |
| fix | Fix path | red |

## Skills

Fields per skill: Group, Role (the short line on the map), Optional, Map (x, y, width, height on the 1280 × 605 map), Document (the artifact chip under a Core Loop box), Summary, When, Reads, Command, Works with, and Result (icon · title · text, plus Tag for the short label on the Core Loop rail).

### now-what

- Group: start
- Role: routes you
- Map: 215, 74, 140, 50
- Summary: The first-stop router. It inspects the project's state and tells you which skill to run next.
- When: Run it when you don't know where to start, or when you're stuck.
- Reads: The project as it is now
- Command: `/andthen:now-what`
- Works with: init, clarify, plan, implement-fix, triage
- Result: compass · Next step · Which skill to run next, based on the state of the project. Nothing is written to disk.

### init

- Group: start
- Role: sets up
- Map: 375, 74, 140, 50
- Summary: Sets up the AndThen workflow structure, in a new project, a partial setup or an existing codebase.
- When: Once per project, before the first real step.
- Reads: The project folder
- Command: `/andthen:init`
- Works with: now-what, describe
- Result: folder · Workflow structure · The AndThen folders and docs the other skills expect.

### handoff

- Group: start
- Role: resumes later
- Map: 535, 74, 140, 50
- Summary: Compacts the conversation into a handoff document that a fresh session can resume from.
- When: Before /clear, when the context is running low, or at the end of a working session.
- Reads: The current conversation
- Command: `/andthen:handoff`
- Works with: now-what
- Result: handoff · Handoff document · What a fresh session needs to pick up where you left off.

### visualize

- Group: share
- Role: draws artifacts
- Map: 740, 74, 150, 50
- Summary: Draws an AndThen artifact as one HTML page with SVG figures: a plan, a spec, a report, an ADR, the Domain Map or the glossary.
- When: When a document is easier to discuss as a picture.
- Reads: Any AndThen artifact
- Command: `/andthen:visualize <artifact>`
- Works with: plan, decide, domain, describe, review
- Result: image · HTML page · One self-contained page that draws the artifact with SVG figures.

### tracker

- Group: share
- Role: issues
- Map: 910, 74, 150, 50
- Summary: Works the issue tracker. publish turns a PRD and its plan into a parent issue with one child issue per story, triage labels and routes incoming items, setup writes the tracker document.
- When: When the work lives in issues. Its triage sorts tickets; the triage skill debugs failures.
- Reads: A PRD, a plan.json or incoming issues
- Command: `/andthen:tracker publish <plan.json>`
- Works with: clarify, plan
- Result: ticket · Tracker issues · A parent issue for the PRD and one child issue per story.

### describe

- Group: design
- Role: maps the code
- Map: 215, 194, 180, 50
- Summary: Documents what an existing project already is: architecture docs and the requirements it implies. --model adds a typed architecture model.
- When: On a brownfield codebase, before you change it.
- Reads: The existing codebase
- Command: `/andthen:describe`
- Works with: init, architecture, domain, visualize
- Result: map · Architecture docs · How the code is built today, plus the requirements it implies. --model adds a typed model.

### domain

- Group: design
- Role: names & contexts
- Map: 422, 194, 180, 50
- Summary: Models the domain: subdomains, bounded contexts, event storming, and the glossary that fixes one name per concept.
- When: When the same thing goes by several names, or when a product spans several contexts.
- Reads: PRD, code and conversations
- Command: `/andthen:domain --mode glossary`
- Works with: decide, plan, describe, visualize
- Result: book · Domain Map + glossary · Bounded contexts and how they connect, and one name per concept.

### architecture

- Group: design
- Role: structure advice
- Map: 629, 194, 180, 50
- Summary: Architecture advice and structural analysis: how to structure or split something, health reviews and fitness functions.
- When: When the question is "how should this be structured?" rather than "which option do we pick?".
- Reads: Code, docs and the question
- Command: `/andthen:architecture --mode advise`
- Works with: decide, describe, domain
- Result: layers · Architecture report · Advice on structure, a health review or fitness functions.

### spike

- Group: design
- Role: proves an idea
- Map: 836, 194, 180, 50
- Summary: Answers one named design question by building a throwaway, runnable spike, then reports a verdict. Evidence, not product.
- When: When you need to know whether an approach works before you specify it.
- Reads: One design question
- Command: `/andthen:spike "<question>"`
- Works with: decide, plan
- Result: flask · Verdict · An evidence-based answer to one design question. The spike code is thrown away.

### ui-ux-design

- Group: design
- Role: screens & flows
- Map: 1043, 194, 180, 50
- Summary: UI and UX design: research, design systems, wireframes and clickable mockups, one at a time or chained.
- When: When the feature has screens or flows worth sketching before they are specified.
- Reads: Requirements and existing UI
- Command: `/andthen:ui-ux-design`
- Works with: plan, visual-validation
- Result: wireframe · Wireframes · Screens and flows as wireframes, or as clickable mockups once a design system exists.

### clarify

- Group: core
- Role: requirements
- Optional: yes
- Map: 215, 318, 140, 64
- Document: prd.md
- Summary: Interviews you in rounds about gaps, edge cases, scope and alternatives until the understanding is shared, then writes the PRD. --brief stops at intent.md.
- When: Optional. Start here if you can't list three acceptance criteria.
- Reads: Your idea, a file or a tracker item
- Command: `/andthen:clarify "<idea>"`
- Works with: plan, decide, tracker, now-what
- Result: doc · prd.md · The Product Requirements Document. With --brief, a shorter intent.md.
- Tag: prd.md

### decide

- Group: core
- Role: records choices
- Optional: yes
- Map: 389, 318, 140, 64
- Document: ADRs
- Summary: Interviews you over the technical choices the solution needs, recommends each one, weighs a contested one in a trade-off, and writes ADRs.
- When: Optional. For a choice that binds beyond one story or is costly to reverse.
- Reads: The PRD or the open question
- Command: `/andthen:decide`
- Works with: clarify, plan, architecture, domain, spike
- Result: seal · ADR · An Architecture Decision Record for each settled choice, and the PRD rows it settles now cite it. domain adds a glossary.
- Tag: ADR

### plan

- Group: core
- Role: the spec
- Map: 563, 318, 140, 64
- Document: FIS + plan.json
- Summary: Writes the Feature Implementation Specification: what to build, the proof for each acceptance scenario, and when it's done. One story, or a plan.json with one FIS per story.
- When: Always. No code changes happen here.
- Reads: PRD, requirements file, tracker item or your request
- Command: `/andthen:plan <prd.md>`
- Works with: clarify, decide, exec-plan, domain, ui-ux-design, spike, tracker
- Result: stack · FIS + plan.json · One Feature Implementation Specification per story, with plan.json listing the stories.
- Tag: FIS + plan.json

### exec-plan

- Group: core
- Role: builds
- Map: 737, 318, 140, 64
- Document: code + tests
- Summary: Builds a FIS, or runs a plan directory with one fresh subagent per story. A story is done only on executed proof, and a fresh reviewer checks each one.
- When: Always. --worktree runs independent stories in parallel. Stories go test-first where the Testing Strategy or your request requires it. Don't hand-edit mid-run.
- Reads: A FIS or a plan directory
- Command: `/andthen:exec-plan <FIS | dir>`
- Works with: plan, review, testing, simplify-code, visual-validation
- Result: code · Code + tests · Working code, each story marked done on a check that actually ran.
- Tag: code + tests

### review

- Group: core
- Role: checks the whole
- Map: 911, 318, 140, 64
- Document: review report
- Summary: The only review skill. Lenses for code, gap (against the FIS), security and outcome (against the PRD), plus PR review. Routes findings into Fix or Note, and --fix applies them.
- When: Always, after exec-plan.
- Reads: The change, its FIS and its PRD
- Command: `/andthen:review --fix`
- Works with: exec-plan, ship, implement-fix, simplify-code, visual-validation
- Result: checklist · Review report · Findings sorted into Fix and Note, with a PASS or FAIL verdict. --fix applies and commits the Fix ones.
- Tag: review report

### ship

- Group: core
- Role: opens the PR
- Map: 1085, 318, 140, 64
- Document: pull request
- Summary: Keeps the implementation observations worth keeping and commits. Then, on one ask, it pushes, opens the pull request, and deletes or keeps the plan bundle.
- When: Last. Nothing is pushed until you say yes.
- Reads: The branch and its plan
- Command: `/andthen:ship`
- Works with: review, implement-fix
- Result: pr · Pull request · Learnings kept, and after your yes the PR opened and the plan files removed. prd.md stays, stamped Shipped.
- Tag: pull request

### testing

- Group: quality
- Role: tests & TDD
- Map: 215, 499, 180, 50
- Summary: Test strategy, coverage and test authoring at every level, test-first where required, and the Prove-It bugfix flow.
- When: When you want a test strategy, or a failing test before a fix.
- Reads: Code and FIS scenarios
- Command: `/andthen:testing --mode prove-it`
- Works with: exec-plan, triage
- Result: checksq · Tests · Tests at the right level, written test-first when you or the Testing Strategy require it, plus a strategy.

### visual-validation

- Group: quality
- Role: UI vs design
- Map: 410, 499, 190, 50
- Summary: Checks UI screenshots against mockups, wireframes or design specs and runs visual regression checks.
- When: When the change has a UI that must match a design.
- Reads: Screenshots, mockups and wireframes
- Command: `/andthen:visual-validation`
- Works with: ui-ux-design, exec-plan, review
- Result: eye · Validation report · Where the built UI differs from its feature's mockup or wireframe, or from the design system.

### simplify-code

- Group: quality
- Role: leaner code
- Map: 620, 499, 180, 50
- Summary: Simplifies code for clarity, reuse and leanness, and keeps the exact behavior.
- When: When working code has grown more complex than it needs to be.
- Reads: Code in scope
- Command: `/andthen:simplify-code`
- Works with: review, exec-plan
- Result: simplify · Simpler code · Less complexity, exactly the same behavior, committed once the checks are green.

### triage

- Group: fix
- Role: diagnoses
- Optional: yes
- Map: 860, 499, 160, 50
- Summary: Investigates, diagnoses and fixes build failures, configuration errors, runtime bugs, regressions and failing tests.
- When: Optional. When the cause is unknown or the build is broken. Describe symptoms, not fixes.
- Reads: Symptoms: errors, logs, failing tests
- Command: `/andthen:triage`
- Works with: implement-fix, testing, now-what
- Result: search · Diagnosis · The root cause, found before anything is changed, and the fix committed once green.
- Tag: diagnosis

### implement-fix

- Group: fix
- Role: small change
- Map: 1060, 499, 165, 50
- Summary: Implements a small feature or fix, or a review report's actionable findings, with minimal verified changes.
- When: When you can state the change in one sentence.
- Reads: Your request, a review report or a tracker item
- Command: `/andthen:implement-fix "<request>"`
- Works with: triage, review, ship
- Result: check · Verified fix · A minimal change, checked with the real build and tests, then committed.
- Tag: verified fix

