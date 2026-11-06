# X1 – Decide and model

> **Skills:** `decide`, `domain --mode glossary`, `spike`
> **Pull this when:** your PRD or plan shows a design fork, or two names for one thing. You apply what the Day 1 talks covered; this exercise does not re-teach the theory.

## Trigger

Pull X1 when you can point at one of these in your own artifacts:

- `clarify` printed `decide` as its `Next (fresh session):` line, or the PRD's *Decisions Log*, *Constraints & Assumptions* or *Open Questions* hold a technical fork that binds beyond one story or is costly to reverse (a storage shape, a queue, a boundary).
- Two or more names for the same concept across the PRD, the FIS files and the code (`member`, `collaborator`, `recipient`), or one word used for two things.
- A plan story whose FIS has a *Preflight* item the skill recommended an ADR for.
- A question only running code can answer ("does this hold under load?", "does the library do what we need?").

No fork, no new vocabulary: skip this and go to `plan`.

## Input

Your team's `<feature-dir>/prd.md`, plus `docs/DECISIONS.md` and `docs/UBIQUITOUS_LANGUAGE.md` if they exist. If your case has no fork yet, your facilitator has the shared-lists PRD, ADR and glossary from the foundation to work on.

## Output

- One ADR per real decision in `docs/adrs/`, each with a row in `docs/DECISIONS.md`, or a one-line *Still Current* entry for a load-bearing choice with no real alternative.
- For a contested decision, trade-off artifacts under `docs/research/` (or `--output-dir`): `research.md`, `tradeoff-matrix.md`, `recommendation.md`.
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
   - Close options on a **two-way door** skip the analysis. That is the skill telling you the fork is not worth one.
   - A decision it labels **one-way** (costly to reverse) deserves the slowest read. Check the *Reversal* line says what reversing would take.
   - You choose `Accepted` or `Proposed` when it plays the settled set back. Choose `Proposed` when someone else must sign off.
3. **When running code is the only answer: spike.** If `decide` says a question needs measurement, or you hit one yourself:
   ```text
   /andthen:spike "does the SQLite query for 'lists shared with me' stay fast with 10k shares?"
   ```
   It confirms the question with you, builds throwaway code in its own worktree under `.agent_temp/spike/`, and reports a verdict: the answer, the evidence, and what the spike did **not** cover. The code stays on a `spike/<slug>` branch as evidence and is never merged or reused. Fold the verdict back into `decide` as evidence.
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
- [ ] Every decision you sorted as "binds beyond one story" has a record; every one you sorted "local to a story" does not have an ADR.
- [ ] A spike verdict, if you ran one, names what it did not cover.
- [ ] Glossary: one canonical term per concept, banned synonyms in **Avoid**, no rationale or mechanism in a cell, and the FIS files use the terms.

## Sizing check

*Did this fork earn an ADR, and did the vocabulary earn a glossary?* A real fork with different long-term consequences does. A choice that is cheap to undo either way does not: record it as a *Still Current* line or leave it to `plan`. Do not decide design the code has already settled, and do not compare five options when two are obviously dominated. When the "decision" is really a tangle of subdomains across many features, one ADR is the wrong tool: see X3.
