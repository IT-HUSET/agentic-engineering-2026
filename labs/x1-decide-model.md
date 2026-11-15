# X1 – Decide and model

**What you do:** settle a technical choice that will be hard to undo, record it as an ADR, and agree on one name for each concept in your case. When only running code can answer the question, you run a short spike instead.

**Why it matters:** a choice made silently inside one story binds every story after it. Two names for one thing make the agent build two things.

**What you have at the end:** one ADR per real decision, a glossary that the PRD, the FIS files and the code agree with, and a spike verdict for any question only code could answer.

> **Skills:** `decide`, `domain --mode glossary`, `spike` · You apply what F3 and the Day 1 architect-role talk covered. This exercise does not re-teach the theory.

## When to pull it

Pull X1 when one of these is true for your case:

- **You face a choice that is costly to reverse,** such as a storage shape, a queue or a boundary between modules. *Check:* `clarify` printed `decide` as its `Next (fresh session):` line, or the PRD's *Decisions Log*, *Constraints & Assumptions* or *Open Questions* name the fork. A FIS *Preflight* item that recommends an ADR counts too.
- **The same thing has two names,** or one word means two things (`member`, `collaborator`, `recipient`). *Check:* search the PRD, the FIS files and the code for the terms.
- **Only running code can answer.** "Does this hold under load?" "Does the library do what we need?"

**Skip it** when there is no fork and no new vocabulary. Go straight to `plan`.

## Input

Your team's `<feature-dir>/prd.md`, plus `docs/DECISIONS.md` and `docs/UBIQUITOUS_LANGUAGE.md` if they exist. If your case has no fork yet, your facilitator has the shared-lists PRD, ADR and glossary from the foundation to work on.

## Output

- One ADR per real decision in `docs/adrs/`, each with a row in `docs/DECISIONS.md`, or a one-line *Still Current* entry for a load-bearing choice with no real alternative.
- For a contested decision, trade-off artifacts under `docs/research/<topic>/` (or `<--output-dir>/<topic>/`): `research.md`, `tradeoff-matrix.md`, `recommendation.md`.
- A curated `docs/UBIQUITOUS_LANGUAGE.md`.
- For an empirical question, a **Spike Verdict** in chat and throwaway code on a `spike/<slug>` branch.

## Steps

1. **List the forks yourself first.** In `.agent_temp/x1-forks.md`, write each design decision your PRD leaves open and sort it: *already settled* (by code or an ADR), *a requirement* (the PRD should say), *binds beyond one story or costly to reverse* (decide now), *local to one story* (leave to `plan`). Then run the skill and compare.
2. **Decide.** In a fresh session:
   ```text
   /andthen:decide <feature-dir>
   ```
   It opens with its own sorted list; add, drop or move points. It asks one decision per question, recommendation first.
   - A **contested** decision (no option stands out, or the evidence is missing) runs a weighted trade-off. Confirm the options, criteria and weights **before** it researches: wrong weights waste the research. Name a count if you want fewer than five ("compare three options").
   - Close options on a **two-way door** are not contested and skip the weighted trade-off. A decision with real alternatives still gets an ADR. A load-bearing choice with no real alternative ("SQLite stays the store") gets a *Still Current* line, and a choice local to one story is left to `plan`.
   - A decision it labels **one-way** (costly to reverse) deserves the slowest read. Check the *Reversal* line says what reversing would take.
   - You choose `Accepted` or `Proposed` when it plays the settled set back. Choose `Proposed` when someone else must sign off.
3. **When running code is the only answer: spike.** `decide` normally hands such a question to `spike` itself and folds the verdict back in as evidence. Outside `decide`, or when you hit the question yourself, run:
   ```text
   /andthen:spike "does the SQLite query for 'lists shared with me' stay fast with 10k shares?"
   ```
   Then run `/andthen:decide <feature-dir>` again with the Spike Verdict. Invoked directly, `spike` confirms the question with you. It builds throwaway code in its own worktree under `.agent_temp/spike/` and reports a verdict: the answer, the evidence, and what the spike did **not** cover. The code stays on a `spike/<slug>` branch as evidence and is never merged or reused.
4. **Curate the glossary.** The foundation produced a first glossary. Here you tend it on your case:
   ```text
   /andthen:domain --mode glossary <focus area>
   ```
   It merges into the existing document (new rows marked `(new)`, changes `(updated)`) and does not regenerate curated terms. Then read the **Avoid** column and the **Overloaded Terms** table with your PRD open: does a banned synonym still appear in the PRD or FIS files? If a term needs a bounded-context qualifier, you have found a boundary. That is a signal for X3.
5. **Carry it forward.** If a plan already exists, `decide` closes on `plan` for the stories the decision changes: `/andthen:plan "story S02 of <feature-dir>/plan.json – <what the ADR now says>; revise its FIS"`. `plan` has no revise mode, so the prompt carries the change.

## Verify

- [ ] Each ADR states one decision plainly, names the criteria that decided it, and includes the floor option (do nothing, or extend what exists) among the alternatives.
- [ ] Each ADR's **Reversal** line says one-way or two-way and what reversing takes.
- [ ] `docs/DECISIONS.md` has a row per ADR with the status you chose.
- [ ] Every decision you sorted as "binds beyond one story" has a record (an ADR, or a *Still Current* line when there is no real alternative). None you sorted "local to a story" has an ADR.
- [ ] A spike verdict, if you ran one, names what it did not cover.
- [ ] Glossary: one canonical term per concept, banned synonyms in **Avoid**, no rationale or mechanism in a cell, and the FIS files use the terms.

## Sizing check

*Did this fork earn an ADR, and did the vocabulary earn a glossary?* A real fork with different long-term consequences does, and a close call on a two-way door still gets its ADR, just without the weighted trade-off. A load-bearing choice with no real alternative is a *Still Current* line, and a choice local to one story is left to `plan`. Do not decide design the code has already settled, and do not compare five options when two are obviously dominated. When the "decision" is really a tangle of subdomains across many features, one ADR is the wrong tool: see X3.
