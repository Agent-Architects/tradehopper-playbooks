---
name: task-management
description: Pulls tasks from the team's task board before work, updates status after work, hands tasks off to another person's agent, and keeps the tasks/ mirror in the repo in sync with the board. Starts with a one-time interview to configure which board is the source of truth (Notion, Linear, GitHub Projects or another). Use before starting any work session, when finishing a task, when handing work to a teammate, or when asked to sync tasks.
license: MIT
metadata:
  version: "1.0"
---

# Task management

The board is the source of truth. The `tasks/` folder is a read-friendly mirror so every agent, including ones without board access, can see what is happening. The mechanics below are the same whatever board you use.

## One-time setup: board interview

If `tasks/BOARD.md` does not exist, interview the person and create it:

1. Which board is the source of truth? (Notion database, Linear team, GitHub Project, other.) Exactly one.
2. How do agents connect? (Official MCP server, CLI such as `gh`, or API.) Record the connection, never the token.
3. Map the board's fields to the standard fields below. Which status values exist? Map each to `todo`, `doing`, `review`, `blocked`, `done`.
4. Who are the assignees, and what is each person's agent called on the board, if it has its own user?
5. Which labels exist? Recommend at least: `needs-human`, `high-risk`, `from-growth`, `bug`, `content`.

`tasks/BOARD.md` format:

```markdown
# Board
Source of truth: <Notion database "Tasks" | Linear team "TH" | GitHub Project "TradeHopper">
Link: <url>
Connection: <official MCP | gh CLI | API>
Status map: todo=<board value>; doing=<...>; review=<...>; blocked=<...>; done=<...>
Fields: id=<field>; title=<field>; owner=<field>; due=<field>; labels=<field>
People: matt, rhyes, jameson (+ their agents)
```

## Standard task fields

`id`, `title`, `status`, `owner`, `due`, `labels`, `links` (artifacts, PRs, docs), `updated`.

## Before work (every session)

1. Run the inbox-outbox skill: read `people/<you>/inbox.md` first.
2. `git pull --rebase` (repo-sync skill).
3. Pull tasks assigned to your person from the board. If the board is unreachable, read `tasks/open.md` and say the data may be stale.
4. Pick the task to work on, or ask the person which one. Set it to `doing` on the board.

## After work

1. Update the task on the board: status, a one-line progress comment, and links to artifacts or PRs.
2. Append one line to `people/<you>/outbox.md`: date, task id, what changed, link.
3. If the work is done, set `review` (when a human must check it) or `done`.
4. If blocked, set `blocked`, label `needs-human` if a person must act, and say exactly what is needed.

## Handoff to another person's agent

1. On the board: assign the task to the other person, set status, and comment with what is done, what is next, links and any deadline.
2. Append a handoff entry to `people/<them>/inbox.md` (inbox-outbox skill format) with the task id.
3. Commit and push. The receiving agent sees it on its next inbox check.
4. A handoff is not complete until both the board and the inbox entry exist.

## Sync: board to tasks/ mirror

Run on a schedule (see the team pack for options) or on request.

1. Read all non-archived tasks from the board.
2. Write `tasks/open.md` (todo, doing, review, blocked) and `tasks/done-<YYYY-MM>.md` (done this month), one row per task: `| id | title | status | owner | due | labels | updated |`.
3. Do not copy private comments, customer data or secrets into the mirror.
4. The mirror is one-way by default: board to repo. If someone edits `tasks/open.md` by hand, treat it as a request: create or update the task on the board, then regenerate the mirror.
5. Commit with `chore(tasks): sync board <timestamp>` only if something changed.

## Rules

- If it is not on the board, it did not happen.
- Do not create tasks for tiny work (under about 15 minutes). Do create one for anything multi-step, shared or handed off.
- Never close a task someone else owns without their agreement.
- Anything touching money, ad spend, trading, production deploys or publishing gets `needs-human` and waits for a person.
