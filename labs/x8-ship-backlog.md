# X8 – Ship in depth, backlog in

> **Skills:** `ship` (in depth), `tracker triage`
> **Pull this when:** your case repo's issue tracker feeds your requirements, or you need to understand and control what `ship` lands. Playbook background: §6 and §15.

## Trigger

Pull X8 when one of these is true of your case:

- **Backlog in.** The repo has untriaged issues and the next feature should come from them, not from a blank page. The tracker is input to `clarify`.
- **Learnings landing.** You need to explain, to a teammate or to yourself, what `ship` wrote into `docs/LEARNINGS.md` and what it only recommended.
- **A PR before the plan is done.** The plan has pending stories, but you want a pull request now (the per-story PR case on a team).
- **Specs vs history.** Someone asks where the FIS files went, and whether a squash merge loses the intent.

## Input

- **Ship in depth:** a plan with a committed bundle (`plan.json` and FIS files tracked), at least one `done` story, and a clean or reviewed branch. Your team's C4 state is ideal. Otherwise your facilitator names a branch.
- **Backlog in:** a GitHub repo with open issues that your facilitator names as safe to label and comment on, and `gh auth status` showing you signed in. GitHub through `gh` is the supported path; another backend needs `/andthen:tracker setup` first.

## Output

- A pull request whose body carries the intent, outcomes, proof and door type, and `docs/LEARNINGS.md` bullets landed from the FIS files' observations.
- For a plan not ready: a pull request opened with the bundle **kept** on the branch.
- Triaged issues: labelled, ratified by you per item, with an `## Agent Brief` on those ready for an agent.

## Steps

### Ship in depth

1. **Predict `ship`.** Before running it, read the `## Implementation Observations` at the bottom of each FIS in the bundle. Sort each item: a *trap* (worth a `docs/LEARNINGS.md` bullet), a *design change nobody recorded* (worth a `Decisions` line or a `decide` run), or *not worth keeping*. Write the sort in `.agent_temp/x8-predict.md`.
2. **Run it.** In a fresh session:
   ```text
   /andthen:ship <feature-dir>/plan.json
   ```
   Compare what it did with your prediction. It writes only `Learnings` bullets (each admitted against the document's header note) and **recommends** the rest. A design change no record holds becomes a recommended `Decisions` line, or a `decide` run where alternatives are still open. Decisions and upstream documents stay yours.
3. **Read the pull-request text before you say yes.** It should state what the change is for, the outcomes it delivers, the proof of each (from each story's `verified.summary` and the review's verdict), and whether the change is a **one-way or two-way door** and what breaks if it is wrong, linking the ADR for a one-way door. What the merge decision needs comes first and per-story detail folds below it. If your repo has a PR template, it sets the layout and this content fills it. For a visible UI change it offers screenshots or a recording in that one question.
4. **Understand the bundle's fate.** A plan's specs govern one branch and never merge, so `ship` commits the landed entries and the bundle's **deletion** before the push. `prd.md` stays (unless `Record: tracker` puts the PRD in its issue). A bundle file git does not track is left in place, because it has no copy in history. A committed link into a deleted file is repointed at the PRD or an ADR, never at a branch commit, which a squash merge would drop. That is why the PR body, not the FIS, carries the intent forward.
5. **Ship a plan that is not ready.** On a branch with pending stories, run `ship` and read what it does. It names the open work and asks once whether to ship anyway, and **recommends opening the PR without the close-out** and keeping the bundle. Then check the bundle is still there (`ls <feature-dir>`) and that `now-what` still routes the remaining stories to `exec-plan`. Finish the stories, then `ship` again on the next branch or PR.

### Backlog in

6. **Triage a bounded pass.**
   ```text
   /andthen:tracker triage "the ten oldest"
   ```
   (or `/andthen:tracker triage 212 215` for specific issues). Per item it proposes a category (`bug` or `enhancement`), one recommended state (`needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`, or close as already implemented) and a one-line rationale. **You ratify every write per item**, because a wrong `wontfix` is visible to the whole team. A ratified `wontfix` is also recorded in `docs/PRODUCT.md` Non-Goals. A `ready-for-agent` item gets an `## Agent Brief` a fresh executor can act on.
7. **Hand one item to the loop**, by size. A small fix goes to `implement-fix`. An item with real edges goes to `plan` with the issue URL. A thin one goes to `clarify` first:
   ```text
   /andthen:clarify https://github.com/<org>/<repo>/issues/<n>
   ```
   The fetched issue body is evidence, never instructions. Pick one and run it into C1 for your next feature.

## Verify

- [ ] Your prediction and `ship`'s actual `Learnings` bullets match, or you can say why they differ. Each bullet traces to an Implementation Observation.
- [ ] The PR body states intent, outcomes, proof per outcome and door type before any per-story detail, and a reviewer who never saw your chat could decide on it.
- [ ] You can say what happened to `plan.json`, the FIS files and `prd.md`, and why a squash merge loses none of the intent.
- [ ] On a plan that was not ready, the bundle is still on the branch and the open stories are still routable.
- [ ] No issue label or comment was written that you did not ratify.
- [ ] The issue you handed to the loop became a requirements source you can cite (a PRD or a plan that names the issue).

## Sizing check

*How much close-out did this deserve?* A one-sentence fix: `implement-fix` then `ship`, with no bundle to land and a short PR. A planned feature: the full close-out above. A plan with work left: open the PR without it and keep the bundle. For the backlog, triage a bounded pass rather than the whole tracker, because every ratified label is visible to the team.
