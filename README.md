# TradeHopper: Security and Team Playbooks

Two free packs for the TradeHopper team: a security pack for the web app, and a team orchestration pack for a shared knowledge base that every agent on the team can use.

Open the HTML docs in a browser for the full guide. They are single files and work on a phone.

## Package A: security pack

[`A-security-pack.html`](A-security-pack.html)

| Path | What it is |
|---|---|
| `.claude/skills/prelaunch-security-audit/SKILL.md` | 40-item pre-launch checklist as a Claude Code skill, based on the OWASP Top 10 2025 and OWASP ASVS 5.0 |
| `security-pack/audit-runbook.md` | Orchestrated audit in Claude Code (one subagent per item, fixes on branches with PRs), with the exact orchestrator prompt |
| `security-pack/templates/.github/workflows/security-ci.yml` | PR checks: lint, typecheck, tests, gitleaks, Semgrep, CodeQL, dependency audit and review, optional AI review |
| `security-pack/templates/.github/dependabot.yml` | Grouped weekly dependency and GitHub Actions updates, 7-day cooldown (set your package ecosystem) |
| `security-pack/templates/.github/workflows/sentry-to-pr.yml` | Error-to-PR loop: Claude reads new Sentry issues and opens draft fix PRs |
| `security-pack/templates/.github/workflows/cve-poller.yml` | CVE poller in GitHub Actions: OSV and Dependabot alerts, draft upgrade PRs |
| `security-pack/prompts/grok-bot-cve-poller.md` | Ready-to-paste CVE poller for the hosted Grok Bot |
| `security-pack/templates/.github/CODEOWNERS` | Code owners for security-critical paths |

Everything under `security-pack/templates/.github/` is meant for the app repo: copy it into the app repo's `.github/` folder. The templates do not assume a language or package manager: commands and toolchain setup are marked `ADAPT`, with Node/npm shown as one example. It does not run in this repo. All actions are pinned to commit SHAs and downloaded tools are checksum-verified.

This repo's own CI (`.github/workflows/ci.yml`) lints those templates with actionlint, checks that actions are SHA-pinned, checks the HTML docs (structure, anchors, referenced paths), validates every skill against the Agent Skills format and the knowledge bundle against OKF, and runs a banned-terms check. The scripts are in `scripts/`.

## Package B: team orchestration pack

[`B-team-orchestration-pack.html`](B-team-orchestration-pack.html)

`team-pack/template/` is a ready-to-copy team-brain repo:

- `AGENTS.md` (team protocol) and `CLAUDE.md` (imports `@AGENTS.md`)
- `knowledge/` in the Open Knowledge Format (OKF) v0.2
- `people/<name>/inbox.md` and `outbox.md`
- `tasks/` board mirror
- `.agents/skills/` with 7 shared skills in the Agent Skills format (`.claude/skills` symlinks to it): connected-services-interview, task-management, inbox-outbox, repo-sync, workspace-tidiness, meeting-notes, weekly-retro
- `grok-bot/` protocol and Custom Rules for the hosted Grok Bot
- `.github/workflows/` scheduled board sync and weekly retro

## Notes

- Nothing here is legal advice. See the business-risk section in the security pack.
- The checklist is a baseline, not a penetration test. Once you have paying users, get a professional review.
- Tool versions and config keys were checked against official docs in November 2026. Re-check before relying on them.

## License

MIT. See [LICENSE](LICENSE).

From Agent Architects
