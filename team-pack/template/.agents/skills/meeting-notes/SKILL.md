---
name: meeting-notes
description: Brings a meeting transcript into the team repo, then runs an AI pass that extracts decisions, action items, open questions and knowledge updates, files tasks on the board and writes decision records. Use after any team or partner call, or when someone pastes or exports a transcript.
license: MIT
metadata:
  version: "1.0"
---

# Meeting notes

## Step 1: bring the transcript in

- Get the transcript from the recording tool (for example a Notion meeting notes export, a Google Meet transcript in Docs, or a pasted text file).
- Save it as `knowledge/meetings/YYYY-MM-DD-<slug>.md` with a header:

```markdown
---
type: Meeting
title: <Meeting title>
description: <one sentence: what the meeting was about>
tags: [meeting, <topic>]
date: YYYY-MM-DD
attendees: [<names>]
sources:
  - resource: <link to the recording tool page>
status: draft
---

# <Meeting title>
Transcript quality: <speaker labels yes/no, known gaps>

## Transcript
<raw text>
```

- Remove anything personal or off-topic that should not be in a shared repo (personal life, health, third parties' private details, secrets). When in doubt, ask the person who recorded it.
- Transcription is imperfect. Do not invent speaker names that are not in the source.

## Step 2: AI pass

Append these sections to the same file, above `## Transcript`:

```markdown
## Summary
<5 lines max>

## Decisions
- <decision> (who decided, quote or paraphrase with approximate position in transcript)

## Action items
- [ ] <action> - owner: <name> - due: <date or none> - task: <board id once filed>

## Open questions
- <question> - who should answer

## Knowledge updates
- <fact or learning> -> knowledge/<file>.md
```

Rules for the pass:

- Only record a decision if someone clearly agreed to it. Ideas and suggestions go under open questions or are left out.
- Every action item needs an owner. If none was named, mark `owner: unassigned` and add it to open questions.
- Quote short phrases as evidence so a human can check against the transcript.

## Step 3: file it

1. Create a board task for each action item (task-management skill) and write the task id back into the note.
2. For each real decision, create `knowledge/decisions/YYYY-MM-DD-<slug>.md` with frontmatter `type: Decision`, `title`, `description` and `tags`, and a body with what, why, who, date and a link to the meeting (`/meetings/YYYY-MM-DD-<slug>.md`).
3. Apply knowledge updates to the right `knowledge/` files.
4. Add an inbox entry for each attendee with action items (inbox-outbox skill).
5. Add the meeting and any decisions to the `index.md` of their folders and a line to `knowledge/log.md`.
6. When a human has checked the AI pass, set `status: stable` and add `verified: { by: human:<name>, at: <timestamp> }`.
7. Commit: `docs(meetings): add YYYY-MM-DD <slug>`.
