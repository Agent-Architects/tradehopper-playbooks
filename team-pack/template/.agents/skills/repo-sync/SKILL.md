---
name: repo-sync
description: Push and pull etiquette for the shared team repo - pull with rebase before work, small focused commits with Conventional Commit messages, push promptly, resolve conflicts safely, and never commit secrets or personal data. Use whenever reading from or writing to the team repo, before starting work, and before ending a session.
license: MIT
metadata:
  version: "1.0"
---

# Repo sync

Several people and agents write to this repo. These rules keep it conflict-light and safe.

## Start of session

```bash
git status            # must be clean, or commit or stash your own work first
git pull --rebase
```

## While working

- **Small commits.** One logical change per commit: one skill update, one meeting note, one task sync.
- **Conventional Commits:** `docs(knowledge): add ad learnings for Nov`, `chore(tasks): sync board`, `feat(skills): add meeting-notes skill`, `fix(skills): correct board status map`.
- **Stage files by name.** Never `git add .` or `git add -A`; that is how `.env` files and exports with personal data leak.
- **Check before committing:** `git diff --staged` and look for tokens, keys, passwords, emails, phone numbers and customer data. If CI has secret scanning, it is a backstop, not the plan.

## Pushing

```bash
git pull --rebase
git push
```

- Content changes (knowledge, meetings, tasks mirror, inbox and outbox) can go straight to `main` if the team allows it.
- Changes to `AGENTS.md`, `CLAUDE.md`, `.agents/skills/`, `.claude/`, `.github/` and `grok-bot/` go through a pull request reviewed by a human. These files change how every agent behaves.

## Conflicts

1. Never force-push to `main`. Never `git reset --hard` or delete someone else's work to make a conflict go away.
2. For append-only files (inbox, outbox, meeting notes), keep both sides in date order.
3. For `tasks/` mirror files, take the latest board state and regenerate.
4. For anything else, stop and ask the person who wrote the other side.

## Never commit

- Secrets of any kind, `.env` files, `CLAUDE.local.md`, `.claude/settings.local.json`.
- Raw exports containing customer personal data or payment details.
- Large media (video, raw footage, design files). Link to Drive or the asset store instead.

## End of session

Commit and push what you changed. If you leave work unfinished, say so in your outbox and on the board.
