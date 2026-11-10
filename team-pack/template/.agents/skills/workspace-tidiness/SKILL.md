---
name: workspace-tidiness
description: Keeps the team repo organized - where each kind of file goes, file and folder naming rules, and archiving instead of deleting. Use when creating, moving or renaming files in the team repo, and when a folder looks messy or has loose files.
license: MIT
metadata:
  version: "1.0"
---

# Workspace tidiness

## Where things go

| Kind of file | Folder |
|---|---|
| Team protocol and agent rules | `AGENTS.md` (root) |
| Durable knowledge (product, brand, offers, playbooks, audience, metrics definitions) | `knowledge/<topic>/` |
| Decisions | `knowledge/decisions/YYYY-MM-DD-<slug>.md` |
| Meeting transcripts and notes | `knowledge/meetings/YYYY-MM-DD-<slug>.md` |
| Task board mirror | `tasks/` |
| Per-person inbox and outbox | `people/<name>/` |
| Connected services registry | `knowledge/services/` |
| Sanitized exports from services | `knowledge/references/<service>/` |
| Shared skills | `.agents/skills/<skill-name>/SKILL.md` |
| Hosted Grok Bot protocol text | `grok-bot/` |
| Weekly retro outputs and notes | `retro/` |
| Anything stale or uncertain | `archive/YYYY-MM/` |

If a file does not fit any row, ask before creating a new top-level folder. New top-level folders change the protocol and need a PR.

## Naming

- Lowercase, hyphen-separated: `ad-learnings-q4.md`, not `Ad Learnings Q4 FINAL v2.md`.
- Dated files start with `YYYY-MM-DD-`.
- One topic per file. Update it in place instead of creating `-v2` or `-new` copies. Git keeps history.
- Every `.md` file under `knowledge/` follows the Open Knowledge Format (OKF) v0.2: YAML frontmatter with a non-empty `type`, plus `title`, `description` (one sentence) and `tags`. Add `status` (`draft`, `stable`, `deprecated`) and `verified: { by: human:<name>, at: <ISO 8601 timestamp> }` once a person has checked it. Agent-written files add `generated: { by: <tool>/<model>, at: <timestamp> }`.
- `index.md` and `log.md` are reserved names in every `knowledge/` folder. Never use them for concept files.

## Archive, do not delete

- Move stale or superseded files to `archive/YYYY-MM/` with `git mv`, and leave a one-line pointer in the old location's index if other files link to it.
- Only a human deletes files, and only after checking nothing links to them.

## Index and log files (OKF)

- Each folder in `knowledge/` has an `index.md` with no frontmatter (the root one may carry `okf_version: "0.2"`), made of headed sections of bullet links: `* [Title](file.md) - <the file's description>`. Update it when you add, move or archive a file. Agents read indexes first and open files only as needed.
- `knowledge/log.md` records changes newest first under `## YYYY-MM-DD` headings, for example `* **Update**: Added [Ad learnings Q4](/growth/ad-learnings-q4.md).`
- Link between knowledge files with bundle-absolute links that start with `/` (the `knowledge/` folder is the root), for example `[Pricing](/product/pricing.md)`.

## Tidy pass (on request or weekly)

1. Find loose files in the root and misplaced files by the table above.
2. Find files with bad names, duplicates and `-v2` copies.
3. Propose moves as a list, then apply them with `git mv` in one commit: `chore(tidy): reorganize <area>`.
