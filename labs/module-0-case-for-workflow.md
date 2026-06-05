# Module 0 - The case for workflow

> **The point of today:** the differentiator in AI-assisted development isn't the model or the tool - it's the **workflow you run it through.**
> **This module:** meet the tool, meet the one idea (the Structure Dial), and get your environment working - so the rest of the day is hands-on.

You don't need to be sold on AI coding to be here. You probably already use it and have hit the ceiling: it's great on small things and drifts on real ones. That gap is the whole course. The fix is a repeatable loop and the judgment to right-size it.

## The one idea (1 minute)

**AI amplifies whatever engineering culture you already have.** Disciplined teams get faster; undisciplined teams get faster at producing mess. So the discipline comes first - and "discipline" here is a concrete, repeatable workflow, not vibes.

## Step 1 - Set up

Install AndThen (you'll use it all day):

```bash
/plugin marketplace add IT-HUSET/andthen
/plugin install andthen
```

The lab's codebase is `todo-app/` - a small but real FastAPI + HTMX app. It's the brownfield base you'll work on across the course.

## Step 2 - First, run the tests

The session-opening ritual for *every* agentic work session: know the ground is solid before you change anything.

```bash
cd todo-app
uv run pytest
```

They should pass. This is not a formality - a healthy test suite is what lets you trust an agent's changes later. (When you ask an agent to start work, "first run the tests" is a great first instruction.)

## Step 3 - Meet the tool

Ask your agent for one small, safe change - for example: *"Add a short module docstring to `src/app/utils.py` explaining what it's for."* Watch what it does, and notice the loop:

> **gather context -> act -> observe the result -> repeat**

Then re-run the tests. Still green? Good - you just closed the loop.

## Step 4 - Decide and explain (the important bit)

Look at what the agent produced and answer, out loud or in a note:
- What did it get right?
- Is there anything you'd have done differently - and *why*?

> 💡 This is the habit the whole course is built on: you own every line, so you form a view rather than rubber-stamping. The agent is senior at understanding the codebase, junior at judgment - that's your job.

## Step 5 - The front door

When you're not sure where to start on a piece of work:

```bash
/andthen:now-what
```

It inspects the project and routes you to the right step. Notice the message underneath it: **structure is a dial, not a mandate.** A one-line fix doesn't need a spec; a payments flow does. Choosing *how much structure* a task deserves is the core skill you'll practice today.

## The Structure Dial

| Work size | What you reach for |
|-----------|--------------------|
| One-sentence fix | `quick-implement` - just verify |
| One real feature | `spec -> exec-spec` |
| Multi-feature / MVP | `prd -> plan` |
| Same, automated | `exec-plan` |

Keep this in your head all day. Every exercise ends by asking: *was that the right amount of structure?*

## Done when

Your environment works, the tests pass, you've watched the agent complete one loop, and you can state the one idea in your own words. Next up: **Module 1 - Frame & Clarify**, where we take a fuzzy idea ("shared lists") and turn it into real requirements.

---

<sub>Curious about the evidence behind "discipline beats tool"? The IT-HUSET Agentic Engineering Playbook collects the studies, surveys, and production case studies. Ask your facilitator for the link.</sub>
