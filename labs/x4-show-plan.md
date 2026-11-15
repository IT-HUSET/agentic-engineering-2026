# X4 – Show and publish the plan

**What you do:** turn your plan into something a person outside your session can read, a one-page drawing of the stories and how they depend on each other. If your team uses a tracker, you also publish the stories there as issues.

**Why it matters:** `plan.json` and a stack of FIS files are written for agents, not for reviewers. An approval at C2 from someone who could not read the plan is a rubber stamp.

**What you have at the end:** `plan.html` with the stories' dependencies and status, a dry-run preview of what would be published, and then the issues in your case repo.

> **Skills:** `visualize`, `tracker publish`

## When to pull it

Pull X4 when one of these is true for your plan:

- **Someone who was not in your session approves it** at C2: a reviewer, a product owner or a teammate.
- **Your team tracks work in GitHub issues** (or another tracker) and wants the stories there.
- **Your convention puts requirements in the tracker.** *Check:* `Record: tracker` in your conventions, or a `docs/ISSUE-TRACKER.md`.

**Skip it** for a single-story plan that only you read.

## Input

Your team's `<feature-dir>/plan.json` and `prd.md` from C2. If your plan is not ready, your facilitator has a several-story `plan.json` to use.

For `tracker`, GitHub through `gh` is the supported path, so `gh auth status` must show you signed in, and the repo needs a GitHub remote. Publish to your team's case repo, nowhere else.

## Output

- `.agent_temp/visualize/plan.html`: a self-contained page with story dependencies and status. It is a derived copy, not committed by default.
- A **dry-run preview** of what `tracker publish` would write, then the issues themselves in your team's case repo.

## Steps

1. **Read your plan like a stranger.** Open `plan.json`. Note, for each story, its `name`, `dependsOn` and `status`. Which stories could start together? Which single story, if it slips, blocks the most? Write the answers in `.agent_temp/x4-notes.md`. The picture should bring out exactly these.
2. **Draw it.** In a fresh session:
   ```text
   /andthen:visualize <feature-dir>/plan.json "story dependencies and status"
   ```
   The page lands at `.agent_temp/visualize/plan.html`. Before it hands the page over, the skill renders it in a browser and fixes overlaps, clipped labels and unreadable arrows. With no browser reachable it says the page is **unchecked**; open it yourself and look. It works for any other AndThen artifact too (the Domain Map, a FIS, an ADR, a review report).
3. **Compare the picture with your notes.** Does the diagram bring out your answers from step 1? If a reader has to dig for the blocking story, ask for a different emphasis and re-run.
4. **Decide whether you need `setup` at all.** On a GitHub remote you do not: with no `docs/ISSUE-TRACKER.md`, `publish` takes the built-in `gh` path and `Record:` defaults to `repo`, so `prd.md` stays in the repo after the merge. Run `setup` only to put the record in the tracker instead, or for a tracker that is not GitHub:
   ```text
   /andthen:tracker setup
   ```
   It asks which backend you use, for anything but GitHub the command per operation, and whether requirements live in the repo (`Record: repo`) or the tracker (`Record: tracker`: the PRD lives in its issue and child issues keep each story's record).
5. **Preview before you write.** Always dry-run first:
   ```text
   /andthen:tracker publish <feature-dir>/plan.json --dry-run
   ```
   It shows what each issue would gain or lose and writes nothing. Check: one parent issue carrying the PRD and a story checklist, and a child issue per story titled `S03 - <name>` with its scope, intent, expected outcomes, acceptance scenarios and dependencies. **No issue names a file or a commit**, because both are gone after the merge.
6. **Publish to your team's case repo.**
   ```text
   /andthen:tracker publish <feature-dir>/plan.json
   ```
   It shows the preview again and asks once. Re-running updates the same issues, found through the parent's checklist. Flow is one way, plan to tracker, with no sync back, so an edit you make in the tracker is shown to you before it is replaced. A closed issue is a shipped record and is never edited.
7. **Know what `ship` will do.** Under `Record: tracker`, `ship` offers to publish before the push, and the pull request closes each finished story's issue. With the plan unfinished it asks whether to keep the bundle (recommending keep) and closes only the finished stories' issues, leaving the parent open.

## Verify

- [ ] The page shows every story in `plan.json` and every `dependsOn` edge, and a stranger can tell what blocks what without opening a FIS.
- [ ] The page's status per story matches `plan.json` (re-draw it after a story moves; it goes stale).
- [ ] The dry-run preview lists one issue per story plus the parent, and none of them mentions a file path or commit.
- [ ] Issues were written only to your team's case repo. Re-run `--dry-run` and confirm it targets the issues that exist instead of proposing new ones.
- [ ] You know where your requirements live after the merge (`Record:` line) and what that means for `prd.md`.

## Sizing check

*Does anyone else need this plan in a form other than the files?* A solo developer on a one-story plan does not. A team that approves plans in review, or a stakeholder who reads in the tracker, does. Publishing to a tracker is also a commitment to keep two views aligned: it is one way (plan to tracker), so decide which one is the truth before you start.
