---
name: harvey
description: "Autonomous AI sales agent daemon, pipeline controller, and local web dashboard. Controls outbound prospecting, cold email drafting, reply classification, and web UI using the global harvey CLI."
---

# Harvey — Autonomous AI Sales Agent

Harvey is an autonomous outbound sales agent (SDR) that runs locally on your machine. It finds target businesses, crawls their websites to spot real pain points, drafts tailored cold emails based on 11 sales frameworks, and manages an outbox with a human-in-the-loop web dashboard.

Harvey uses the subscription-backed Claude Code CLI or Codex CLI (`--safe-mode`), requiring **zero per-token model API billing**.

---

## Quick Reference — Global Terminal CLI

Any agent or human can invoke Harvey directly using the global `harvey` executable:

| Command | Purpose |
| :--- | :--- |
| `harvey status` | Check pipeline status (prospects, draft campaigns, active campaigns, brain status) |
| `harvey dashboard start` | Start the local web dashboard daemon in the background on port `5555` |
| `harvey dashboard stop` | Stop the running background dashboard daemon |
| `harvey dashboard status` | Check if the web dashboard is running and print its unlock URL |
| `harvey dashboard open` *(or `harvey open`)* | Ensure dashboard is running and open the web UI in default browser |
| `harvey dashboard url` *(or `harvey url`)* | Print the private token unlock URL (`http://127.0.0.1:5555/#token=...`) |
| `harvey run` | Start the 15-minute heartbeat loop (finds leads, drafts emails, checks replies) |
| `harvey outbox` | Review queued emails waiting for human approval |
| `harvey companies` | View registered companies and targeting rationale |
| `harvey train <url>` | Crawl a website to train Harvey on a product/service |
| `harvey discover` | Manually trigger lead discovery matching your configured ICP |
| `harvey profile` | Crawl discovered company websites to extract pain points (free, zero model cost) |
| `harvey signals` | Review and confirm which hiring/growth signals to prospect against |
| `harvey warmup` | Check domain email warmup status and deliverability health |
| `harvey usage` | Inspect daily model quota and call counts |

---

## Web Dashboard UI (`Command Deck`)

Harvey includes a full-featured local web dashboard served at `http://127.0.0.1:5555`.

### Launching the Dashboard:
```bash
# Launch in background and get the unlock URL:
harvey dashboard start

# Or automatically launch and open in browser:
harvey dashboard open
```

### Dashboard Features:
1. **Today Screen**: High-level activity feed, lead metrics, active campaigns, and daily call counts.
2. **Outbox Review**: Read every drafted cold email before it sends. Edit copy directly or approve with one click.
3. **Signals & Cohorts**: Confirm identified hiring signals, tech stack changes, or funding rounds to build prospect batches.
4. **Conversation Handoff**: When a prospect replies asking for a meeting, quote, or contract, Harvey flags it for human takeover.
5. **Dark Mode & Responsive UI**: Clean interface running with zero external font/CSS tracking.

---

## Pipeline Architecture & Deterministic Decisions

Harvey's heartbeat runs on a deterministic cycle every 15 minutes:

```
Wake → Check Quiet Hours → Check Model Budget → Decide → Act → Log → Sleep
```

Priority order for cycle decisions:
1. **Handle Replies** (highest priority: classify prospect replies, draft responses, flag handoffs)
2. **Send Approved Campaigns** (dispatch approved outbox emails within configured daily caps)
3. **Write Campaigns** (draft tailored sequences for new qualified prospects)
4. **Prospect / Discover** (find new accounts matching ICP criteria)
5. **Idle Analysis** (learn patterns, calculate conversion metrics)

---

## Configuration

Harvey is configured in `/home/sami/Tools/harvey/harvey.yaml`:
- `persona`: Name, company, role, tone, email signature.
- `product`: Value proposition, pricing, benefits, objection responses.
- `icp`: Target industries, company sizes, titles, geographies, hiring signals.
- `channels`: Email provider (`gmail`, `microsoft`, `smtp`, `instantly`), daily caps, warmup config.
- `brain`: Provider (`claude` or `codex`), model, daily quota limits.
- `compliance`: CAN-SPAM postal address, opt-out line, do-not-contact domains list.

---

## Sales Playbooks & Knowledge Library

Harvey loads specialized sales playbooks depending on the task. All playbooks are accessible in the `references/` folder:

- [Cold Email Copywriting](references/email_frameworks.md) — 2026 reply-rate data, banned AI patterns, 5 copywriting frameworks.
- [Objection Handling](references/objection_handling.md) — LAARC framework, battle cards for price, competitor, and timing.
- [Lead Qualification](references/lead_qualification.md) — ICP scoring, BANT & MEDDIC screening, disqualification rules.
- [Offer Strategy](references/offer_strategy.md) — Low-friction front-end offers, teardowns, audits, risk-reversal mechanics.
- [LinkedIn Outreach](references/linkedin_outreach.md) — Connection sequences, non-cringe notes, social selling cadence.
- [Sales Methodology](references/sales_methodology.md) — Consultative discovery, conversation flow, ABC loop.
- [Selling to Startups](references/selling_to_startups.md) — Founder psychology, accelerator timing (YC/Techstars), fast-moving deals.
- [Signal Playbook](references/signal_playbook.md) — Turning job postings, tech migrations, and funding rounds into hooks.
- [Account Navigation](references/account_navigation.md) — Multi-threading, gatekeeper navigation, finding economic buyers.
- [Prospecting Tactics](references/prospecting_tactics.md) — Google search dorking, website scraping, referral mining.
