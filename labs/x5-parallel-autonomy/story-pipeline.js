export const meta = {
  name: 'story-pipeline',
  description: 'Run a plan.json story by story in dependency order, one agent per story, test gate after each wave, stop on red',
  phases: [
    { title: 'Plan', detail: 'read plan.json, compute waves' },
    { title: 'Stories', detail: 'one agent per story, ready stories in parallel up to MAX_PARALLEL' },
    { title: 'Merge', detail: 'merge the parallel branches, stop on conflict' },
    { title: 'Gate', detail: 'test suite and plan.json rows after each wave' },
  ],
}

// ANSWER KEY AND FALLBACK. You ask Claude to write your own workflow (the lab, form B) and compare it with this one.
// Use this script only if Claude does not deliver a runnable one. Tried against a stand-in, never against the real runtime.
// Constants. Pass { planDir, maxParallel, stopAfter } as args to override. stopAfter is a story id: the run ends after the wave that holds it.
const PLAN_DIR = (args && args.planDir) || 'docs/specs/let-people-share-their-lists'
const MAX_PARALLEL = (args && args.maxParallel) || 2
const STOP_AFTER = args && args.stopAfter
const TEST_CMD = 'uv run pytest -q'
const COMPILE_CMD = 'uv run python -m compileall -q src tests'

const S = { type: 'string' }
const obj = (required, properties) => ({ type: 'object', required, properties })
const list = items => ({ type: 'array', items })

const PLAN_SCHEMA = obj(['stories'], {
  stories: list(obj(['id', 'fis', 'dependsOn', 'status'], { id: S, fis: S, dependsOn: list(S), status: S })),
})
const STORY_SCHEMA = obj(['id', 'outcome', 'summary', 'branch', 'root'], {
  id: S, outcome: { type: 'string', enum: ['done', 'failed'] }, summary: S, branch: S, root: S,
})
const MERGE_SCHEMA = obj(['merged', 'conflict'], {
  merged: list(S),
  conflict: obj(['story', 'files'], { story: S, files: list(S) }),
})
const GATE_SCHEMA = obj(['testExit', 'testLine', 'compileExit', 'rows'], {
  testExit: { type: 'number' }, testLine: S, compileExit: { type: 'number' },
  rows: list(obj(['id', 'status', 'summary'], { id: S, status: S, summary: S })),
})

function storyPrompt(story, isolated) {
  return [
    'You execute exactly one story of an implementation plan.',
    `Invoke the andthen:exec-plan skill with --auto on ${PLAN_DIR}/${story.fis} and do nothing else.`,
    isolated
      ? 'You run in your own git worktree. Commit there, never touch the main checkout.'
      : 'You run in the main checkout. Commit there.',
    'Never ask a question: an open choice is recorded by the skill as an ASSUMPTION line.',
    'When the skill has finished, report: id (the story id), outcome (done only if the skill wrote the row done with a verified summary, otherwise failed),',
    "summary (the row's verified.summary, or the failure reason), branch (git rev-parse --abbrev-ref HEAD) and root (git rev-parse --show-toplevel).",
  ].join('\n')
}

function gatePrompt(ids) {
  return [
    'Run these two commands from the project root, in this order, change nothing and fix nothing:',
    `1. ${TEST_CMD}`,
    `2. ${COMPILE_CMD}`,
    "Report each command's exit code, and for the first the runner's last output line verbatim.",
    `Then read ${PLAN_DIR}/plan.json and report id, status and verified.summary (empty string if absent) of the stories ${ids.join(', ')}.`,
  ].join('\n')
}

function gateIsGreen(gate, ids) {
  const testsOk = gate.testExit === 0 && /\d+ passed/.test(gate.testLine) && !/failed|error/i.test(gate.testLine)
  const rowsOk = ids.every(id => gate.rows.some(r => r.id === id && r.status === 'done' && r.summary.length > 0))
  return gate.compileExit === 0 && testsOk && rowsOk
}

// Plan: read plan.json once, compute everything else in code.
const plan = await agent(
  `Read ${PLAN_DIR}/plan.json and return every story with its id, fis file name, dependsOn and status. Change nothing.`,
  { phase: 'Plan', schema: PLAN_SCHEMA, effort: 'low', label: 'read plan.json' },
)
if (!plan) return { stopped: 'plan.json could not be read' }

const done = new Set(plan.stories.filter(s => s.status === 'done').map(s => s.id))
let pending = plan.stories.filter(s => s.status !== 'done' && s.status !== 'skipped')
const completed = []
let wave = 0

while (pending.length) {
  const ready = pending.filter(s => s.dependsOn.every(d => done.has(d)))
  if (!ready.length) {
    log(`STOP: no story is ready. Left: ${pending.map(s => s.id).join(', ')}`)
    return { stopped: 'dependency cycle or an edge nothing satisfies', left: pending.map(s => s.id), completed }
  }
  wave++
  log(`Wave ${wave}: ${ready.map(s => s.id).join(', ')}`)

  const parallelWave = ready.length > 1
  const results = []
  for (let i = 0; i < ready.length; i += MAX_PARALLEL) {
    const batch = ready.slice(i, i + MAX_PARALLEL)
    const out = await parallel(
      batch.map(story => () => {
        const opts = { phase: 'Stories', schema: STORY_SCHEMA, label: story.id }
        if (parallelWave) opts.isolation = 'worktree'
        return agent(storyPrompt(story, parallelWave), opts)
      }),
    )
    results.push(...out)
  }

  const failed = ready.filter((s, i) => !results[i] || results[i].outcome !== 'done')
  if (failed.length) {
    log(`STOP: story failed: ${failed.map(s => s.id).join(', ')}. Dependents are not started.`)
    return { stopped: 'story failed', failed: failed.map(s => s.id), results: results.filter(Boolean), completed }
  }

  if (parallelWave) {
    const merge = await agent(
      [
        'You are in the main checkout. Merge these story branches into the current branch, in this order, one at a time:',
        ...ready.map((s, i) => `${s.id}: branch ${results[i].branch}, worktree ${results[i].root}`),
        'For each: git merge --no-ff <branch>. After a successful merge, remove the worktree (git worktree remove <path>) and delete the branch (git branch -d <branch>).',
        'On a conflict: record the story id and the conflicting files (git diff --name-only --diff-filter=U), run git merge --abort, keep that worktree and branch, and stop. Resolve nothing.',
        'Report the ids merged, and conflict as { story: "", files: [] } when there was none.',
      ].join('\n'),
      { phase: 'Merge', schema: MERGE_SCHEMA, effort: 'low', label: 'merge wave ' + wave },
    )
    if (!merge || merge.conflict.files.length > 0) {
      log(`STOP: merge conflict in ${merge ? merge.conflict.story : '?'}: ${merge ? merge.conflict.files.join(', ') : ''}`)
      return { stopped: 'merge conflict', conflict: merge && merge.conflict, merged: merge && merge.merged, completed }
    }
  }

  const ids = ready.map(s => s.id)
  const gate = await agent(gatePrompt(ids), { phase: 'Gate', schema: GATE_SCHEMA, effort: 'low', label: 'gate wave ' + wave })
  if (!gate || !gateIsGreen(gate, ids)) {
    log(`STOP: gate red after wave ${wave}`)
    return { stopped: 'gate red', wave: ids, gate, completed }
  }

  ids.forEach(id => { done.add(id); completed.push({ id, summary: results[ready.findIndex(s => s.id === id)].summary }) })
  pending = pending.filter(s => !done.has(s.id))
  if (STOP_AFTER && ids.includes(STOP_AFTER)) {
    log(`Stopped as asked after ${STOP_AFTER}. Left: ${pending.map(s => s.id).join(', ')}`)
    return { stopped: 'stopAfter', left: pending.map(s => s.id), completed }
  }
}

return { stopped: null, waves: wave, completed }
