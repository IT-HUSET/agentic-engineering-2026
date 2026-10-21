# X4 – Show and publish the plan

> **Skills:** `visualize`, `tracker publish`
> **Pull this when:** someone outside your session has to read the plan, or the plan has to land in a tracker.

## Trigger

Pull X4 when you can say one of these about your plan:

- A reviewer, product owner or teammate will approve the plan at C2 without having been in your session, and `plan.json` plus a stack of FIS files is a poor thing to hand them.
- Your team tracks work in GitHub issues (or another tracker) and wants the stories there.
- `docs/ISSUE-TRACKER.md` exists, or your team's convention says requirements live in the tracker (`Record: tracker`).

A single-story plan that only you read needs neither.

## Input

Your team's `<feature-dir>/plan.json` and `prd.md` from C2. If your plan is not ready, your facilitator has a several-story `plan.json` to use.

For `tracker`, GitHub through `gh` is the supported path, so `gh auth status` must show you signed in, and the repo needs a GitHub remote. Your facilitator tells you which repo is safe to write to.

## Output

- `.agent_temp/visualize/plan.html`: a self-contained page with story dependencies and status. It is a derived copy, not committed by default.
- A **dry-run preview** of what `tracker publish` would write, and, only if your facilitator agrees, the issues themselves.

## Steps

1. **Read your plan like a stranger.** Open `plan.json`. Note, for each story, its `name`, `dependsOn` and `status`. Which stories could start together? Which single story, if it slips, blocks the most? Write the answers in `.agent_temp/x4-notes.md`. The picture should bring out exactly these.
2. **Draw it.** In a fresh session:
   ```text
   /andthen:visualize <feature-dir>/plan.json "story dependencies and status"
   ```
   The page lands at `.agent_temp/visualize/plan.html`. Before it hands the page over, the skill renders it in a browser and fixes overlaps, clipped labels and unreadable arrows. With no browser reachable it says the page is **unchecked**; open it yourself and look. It works for any other AndThen artifact too (the Domain Map, a FIS, an ADR, a review report).
3. **Compare the picture with your notes.** Does the diagram bring out your answers from step 1? If a reader has to dig for the blocking story, ask for a different emphasis and re-run.
4. **Set up the tracker, once.** `tracker publish` offers `setup` whenever `docs/ISSUE-TRACKER.md` is missing, even on GitHub, because creating the document is part of the first publish. Accept it when offered, or run it first:
   ```text
   /andthen:tracker setup
   ```
   Choose GitHub as the backend, and choose your `Record:` line. It asks which backend you use and whether requirements live in the repo (`Record: repo`, the default: `prd.md` stays after the merge) or the tracker (`Record: tracker`: the PRD lives in its issue and child issues keep each story's record).
5. **Preview before you write.** Always dry-run first:
   ```text
   /andthen:tracker publish <feature-dir>/plan.json --dry-run
   ```
   It shows what each issue would gain or lose and writes nothing. Check: one parent issue carrying the PRD and a story checklist, and a child issue per story titled `S03 - <name>` with its scope, intent, expected outcomes, acceptance scenarios and dependencies. **No issue names a file or a commit**, because both are gone after the merge.
6. **Publish only on a yes from your facilitator.**
   ```text
   /andthen:tracker publish <feature-dir>/plan.json
   ```
   It shows the preview again and asks once. Re-running updates the same issues, found through the parent's checklist. Flow is one way, plan to tracker, with no sync back, so an edit you make in the tracker is shown to you before it is replaced. A closed issue is a shipped record and is never edited.
7. **Know what `ship` will do.** Under `Record: tracker`, `ship` offers to publish before the push, and the pull request closes each finished story's issue. With the plan unfinished it keeps the bundle and closes only the finished stories' issues.

## Verify

- [ ] The page shows every story in `plan.json` and every `dependsOn` edge, and a stranger can tell what blocks what without opening a FIS.
- [ ] The page's status per story matches `plan.json` (re-draw it after a story moves; it goes stale).
- [ ] The dry-run preview lists one issue per story plus the parent, and none of them mentions a file path or commit.
- [ ] Nothing was written to the tracker unless you and your facilitator agreed. If you published, re-run `--dry-run` and confirm it targets the issues that exist instead of proposing new ones.
- [ ] You know where your requirements live after the merge (`Record:` line) and what that means for `prd.md`.

## Dial check

*Does anyone else need this plan in a form other than the files?* A solo developer on a one-story plan does not. A team that approves plans in review, or a stakeholder who reads in the tracker, does. Publishing to a tracker is also a commitment to keep two views aligned: it is one way (plan to tracker), so decide which one is the truth before you start.
