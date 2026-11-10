---
name: connected-services-interview
description: Interviews a team member about every service they use for the business (Notion, Google Docs and Sheets, Discord, ad platforms, Stripe, analytics, GitHub), connects each one to the agent through MCP or a CLI with least-privilege access, and stores sanitized exports and summaries in the team repo. Use when onboarding a person or agent, when someone adds a new tool, or when asked to "connect my services".
license: MIT
metadata:
  version: "1.0"
---

# Connected-services interview

Goal: every service the business depends on is listed in `knowledge/services/`, connected to the agents that need it with the narrowest access possible, and summarized into the repo so every agent shares the same context.

## Rules

- **Never ask for or store a secret in chat, in the repo or in a summary.** Tokens go in the person's own environment (shell env, OS keychain, `.claude/settings.local.json` `env`, or the tool's own login). The repo only records the variable name.
- **One login per person and per agent.** No shared accounts. Agent actions must be attributable and revocable.
- **Read-only by default.** Ask before enabling any write scope. Money, ad spend, publishing and deletions always stay behind a human approval.
- **Sanitize before committing.** Remove personal data about customers, emails, phone numbers, payment details, account numbers and anything in a "private" area.

## Step 1: interview

Ask one question at a time and record answers in `knowledge/services/<service>.md` as you go:

1. Which tools do you use for this business? Prompt with: task board, docs (Notion, Google Docs), spreadsheets (Google Sheets), chat (Discord), code (GitHub), payments (Stripe), product analytics (PostHog), errors (Sentry), ad platforms, video and design tools, AI agents and bots.
2. For each tool: what do you use it for, which workspace, folder, database, channel or account matters, and who owns it?
3. What should an agent be able to **read** there? What should it be able to **write**? What must it never touch?
4. Is this the source of truth for anything (tasks, content plan, metrics, decisions)?
5. How fresh does the repo copy need to be (live via MCP only, daily export, weekly summary)?

## Step 2: connect

For each service, prefer in this order: the vendor's official MCP server, the vendor's official CLI, the vendor's REST API with a scoped token, then a manual export.

- Check the vendor's current docs for the MCP server URL and auth method before configuring it. Do not install unofficial servers without the person's explicit approval and a quick review of the source.
- Claude Code: `claude mcp add --transport http <name> <url>` then authenticate with `/mcp`. Use `--scope project` only for servers with no secrets in the config (the team shares `.mcp.json`); use the default local scope otherwise.
- Codex and Grok CLIs: add the same server in that tool's MCP config.
- Hosted Grok Bot: add the service under **Connect apps**, or use **Add a custom connector** (type Remote HTTPS) for an MCP server. Apps are account-wide and use the member's own sign-in.
- Stripe: use a restricted key, or for the Stripe MCP server an agent API key or OAuth (Stripe MCP stops accepting full-access secret keys after 2026-11-30). Start in a sandbox or test mode.
- Test with one harmless read (list one page, one row, one channel) and record the result.

## Step 3: record

Write `knowledge/services/<service>.md`:

```markdown
---
type: Service
title: <Service>
description: <one sentence: what the team uses it for>
resource: <workspace or app URL, no secrets>
tags: [service, <area>]
---

# <Service>
Owner: <person>
Used for: <one line>
Source of truth for: <tasks | content plan | metrics | none>
Connection: <official MCP | CLI | API | manual export>, set up by <person> on <date>
Agent access: read <what>; write <what or none>; never <what>
Token: env var <NAME> in each person's own environment (never committed)
Repo copy: knowledge/references/<service>/ refreshed <how often>, summary in knowledge/<topic>.md
Last verified: <date>
```

Add the service to `knowledge/services/index.md` (`* [<Service>](<service>.md) - <description>`) and a line to `knowledge/log.md`.

## Step 4: export and summarize

- Export only what the team needs as Markdown (with OKF frontmatter, `type: Export` and `sources` pointing at the original) or CSV into `knowledge/references/<service>/<YYYY-MM-DD>-<slug>.md`.
- Strip personal data and secrets before writing. If unsure whether something is sensitive, leave it out and ask.
- Write or update a short summary in the right `knowledge/<topic>/` folder (OKF frontmatter, for example `type: Playbook` or `type: Metric`) that links to the export. Summaries are what agents read first; exports are evidence.
- Commit with `docs(services): connect <service>` following the repo-sync skill.

## Done when

Every tool from the interview has a `knowledge/services/<service>.md`, a tested connection or a documented reason it is manual, and any needed export plus summary is committed.
