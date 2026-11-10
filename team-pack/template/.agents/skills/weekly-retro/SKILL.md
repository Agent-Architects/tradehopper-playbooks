---
name: weekly-retro
description: Runs the weekly team retro - reviews the past week's meetings, task board history, inbox and outbox traffic and agent corrections, finds friction and repeated mistakes, and proposes skill or protocol updates as pull requests for humans to approve. Use once a week, or when asked to run a retro or improve the team's skills.
license: MIT
metadata:
  version: "1.0"
---

# Weekly retro

Agents propose, humans merge. Nothing in this skill changes `AGENTS.md` or any skill without a reviewed PR.

## Inputs (last 7 days)

- `knowledge/meetings/` files from the week.
- Board history: tasks created, completed, bounced back, stuck in `blocked` or `review` for more than 2 days.
- `people/*/inbox.md` and `outbox.md` changes (`git log --since="7 days ago" -p -- people/`).
- Commits touching `knowledge/` and `.agents/skills/`.
- Any notes people left in `retro/notes.md` during the week ("the agent keeps doing X").

## Analysis

Produce `retro/YYYY-MM-DD.md`:

```markdown
# Retro YYYY-MM-DD

## Metrics
- Tasks done: <n>. Median time todo->done: <x days>.
- Handoffs: <n>; bounced for missing info: <n>.
- Tasks stuck in blocked/review > 2 days: <list>.
- Skills used this week (from commit messages and outboxes): <list>. Unused for 30 days: <list>.

## What went well
## What got stuck
## Repeated corrections (humans fixing the same agent mistake)
## Proposed changes
1. <change> - why (evidence links) - files touched
```

## Proposals as pull requests

For each proposed change:

1. Branch `retro/YYYY-MM-DD-<slug>`.
2. One change per PR: a new skill, an edit to one skill, an `AGENTS.md` rule, or a knowledge fix.
3. PR body: the problem, evidence (links to meeting lines, tasks or commits), the change, and how to tell next week whether it worked.
4. Request review from the person most affected. Do not merge.

## In the retro meeting (30 minutes)

- Walk through the metrics and the proposed PRs. Approve, change or reject each.
- Rejected proposals get a one-line reason recorded in the retro file so agents do not propose them again.
- Skills unused for 30 days are archived unless someone objects.
