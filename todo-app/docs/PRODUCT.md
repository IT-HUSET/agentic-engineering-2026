# Product Vision: Todo App

> **Source**: course seed for the Agentic Software Engineering 2026 foundation labs

## Vision
A personal todo app for one person's own lists: capture a task in a second, find it again by name, and see what is due today or overdue at a glance.

## Problem Statement
People keep tasks in several places (notes, mail, paper) and lose track of what is due. Heavy project tools are too much for personal lists, and a plain notes file shows no due dates or priorities.

## Target Users & Personas
- **Individual planner** – keeps a few lists (work, personal) for their own tasks, adds items quickly during the day, checks due dates in the morning.

## Value Propositions
- Adding a todo takes one field and Enter.
- Overdue and due-today items stand out without opening them.
- Lists stay private to their owner.

## Product Principles
- Personal before collaborative: every feature works for one person on their own lists.
- Fast capture over rich structure: the quick-add path stays one field.

## Non-Goals
- **Multi-user sharing of lists.** Lists belong to one owner, and no other user can see or change them. Sharing, invitations and roles are out of scope for this product.
- Team or project management features (assignment, workflows, reporting).
- Native mobile apps; the responsive web UI is the mobile experience.

## Success Metrics
### North Star
- Todos completed per active user per week.
### Leading Indicators
- Share of todos created through quick-add.
- Share of todos with a due date.

## Strategic Constraints
- **Business**: none recorded.
- **Regulatory**: none recorded.
- **Technical**: none recorded.

## Roadmap Themes
- **Personal productivity** – search, due dates and priorities that help one person plan their day.

## Open Questions
- Area to revisit: reminders – whether due-date alerts belong in the app at all.

## Decisions Log
| Decision | Rationale | Date |
|----------|-----------|------|
| Lists are private to their owner | Keeps the product personal and the data model simple | 2026-11-09 |
