---
name: project-scaffolding
description: >-
  Standardized protocol for architecting, scaffolding, and managing the lifecycle of any project
  (web apps, backend APIs, automation pipelines, CLI tools, AI/LLM systems). Enforces the 4-file
  operational system (AGENTS.md, STATE.md, README.md, samples/fixtures), zero-secret security invariant,
  and the 'I Built This' portfolio intake protocol.
---

# Universal Project Scaffolding & State Management Standard

## 1. Overview & Philosophy

Every technical build in Sami's ecosystem—whether a fullstack web application, a backend API, an n8n automation pipeline, a CLI tool, or an AI agent—must operate like a production-grade system from minute zero.
There are no "temporary" throwaway scripts, undocumented architectures, or lost contexts across agent restarts and multi-agent handoffs.

Whenever Sami says:
- *"I want to build [project]"*
- *"Create a new project for [x]"*
- *"Scaffold [x]"*
- *"Let's start [x]"*
- Or initiates any new build in `/home/sami/Projects/`

The agent must immediately execute this standardized scaffolding protocol before writing implementation code.

---

## 2. Canonical Directory Structure: The 4-File Core

Every project directory must contain four core operational components:

```text
<project-root>/
├── AGENTS.md          # 1. Project Agent OS (Immutable architecture, invariants, rules)
├── STATE.md           # 2. Dynamic State Machine (Live status, credential names, verified code)
├── README.md          # 3. Portfolio & Commercial Spec (1-sentence ROI, architecture, stack)
└── samples/           # 4. Rich Real-World Test Fixtures (Happy path + 3 edge cases)
    └── (JSON payloads, mock input files, API test fixtures)
```

### The 4 Files Defined:

### 1. `AGENTS.md` (Project Agent OS — Semi-Permanent)
The source of truth for any AI agent or developer touching the project. It defines:
- **Project Context & Business Objective:** What the project is and why it exists.
- **Session Continuity Protocol:** Mandatory instructions to read `AGENTS.md` + `STATE.md` at session start, and write verified states to `STATE.md` at session end.
- **System Architecture & Data Flow:** ASCII or Mermaid diagram detailing all layers (ingestion → validation → business logic → exception handling → dispatch).
- **Key Modules / Nodes / Endpoints Reference:** Table listing every major component and its specific responsibility.
- **Non-Negotiable Invariants (Do-Not-Break Rules):** Strict rules governing business logic, safety gates, and security.
- **Phased Build Checklist:** Milestone 1, 2, and 3 with explicit checkboxes.
- **Out of Scope (V1):** Boundaries preventing scope creep.

### 2. `STATE.md` (Dynamic Operational Brain — Continuously Updated)
The living whiteboard tracking active engineering progress across sessions:
- **Current Milestone & Live Build Status:** Exactly what is being worked on right now.
- **Integration & Credential Registry:** Structured table of all external APIs, databases, and third-party services.
- **Verified Code Configurations & Expressions:** Copy-paste-ready code snippets, database schemas, API parameters, or expressions that have been tested and verified.
- **Test Payloads & Verification Log:** Summary of executed tests and results against test fixtures.
- **Immediate Next Steps:** Actionable checklist for the immediate next coding session.

### 3. `README.md` (Commercial & Portfolio-Facing Spec)
The human-facing showcase and portfolio asset:
- **1-Sentence ROI Hook:** A punchy commercial proposition answering: *"What financial, operational, or speed bottleneck does this eliminate?"*
- **Visual Architecture Diagram:** Clean ASCII or Mermaid diagram showing how data moves.
- **Key Differentiators:** 3–4 bullet points explaining why this solution is superior to generic boilerplate.
- **Tech Stack & Prerequisites:** Runtime versions, libraries, external dependencies.
- **Quickstart & Run Guide:** Exact terminal commands to install, configure, and run.

### 4. `samples/` or `fixtures/` (Deterministic Test Harness)
A directory containing at least 4 rich, real-world test inputs:
1. **Clean Happy Path:** Standard optimal input passing all validations.
2. **Validation / Syntax Discrepancy:** Input with missing fields, malformed types, or invalid formats.
3. **Stale / Expired State:** Input violating time limits, expiration dates, or balance caps.
4. **Failover / Boundary Case:** Edge-case input triggering human-in-the-loop review, retry backoff, or fallback queues.

---

## 3. Strict Non-Negotiable Invariants

1. **SECURITY INVARIANT (NEVER BREACH):**
   - **NEVER write actual API keys, private tokens, passwords, database connection strings with secrets, or webhook secrets into ANY project file** (`AGENTS.md`, `STATE.md`, `README.md`, `samples/`).
   - Only record credential names (e.g. `Stripe Production Account`), environment variable names (e.g. `STRIPE_SECRET_KEY`), and account identifiers.
   - Real secret values live strictly in `.env` (which must always be added to `.gitignore`) or platform secret managers.

2. **THE CONTINUITY RULE (Text > Brain):**
   - Every session starts by reading `AGENTS.md` and `STATE.md` to ground active context.
   - Every session or milestone ends by updating `STATE.md` with verified code, schemas, and next steps.
   - Mental notes are useless. If it is not written to disk, it does not exist.

3. **ONE-SENTENCE ROI / VALUE HOOK:**
   - Every project must declare an unambiguous 1-sentence ROI hook. Ban generic buzzwords (*"AI-powered synergy"*). State the exact metric (*"Reduce X by Y%"*, *"Eliminate 80% of Z"*, *"Turn A into B in 60 seconds"*).

4. **EXCEPTION-AWARE ARCHITECTURE:**
   - Happy paths represent only 30% of engineering. 70% is handling what happens when APIs fail, payloads are malformed, or networks drop. Every project must include retry logic, error isolation, or fallback queues.

---

## 4. Adaptation Matrix Across Project Archetypes

| Project Archetype | Primary Stack | `AGENTS.md` Focus | `STATE.md` Focus | `samples/` Content |
|:---|:---|:---|:---|:---|
| **Fullstack Web App** | Next.js, Vite, Tailwind, Supabase/Postgres | Route tree, UI state machine, Auth flow, API contracts | DB schema migrations, tested SQL queries, API endpoints, mock sessions | Mock API responses, seed DB records, auth test tokens |
| **Backend API / Microservice** | FastAPI, Express, Go, NestJS | Endpoint specs, middleware chain, DB transactions, rate limits | Active route handlers, Docker commands, ORM models, migration status | Sample request/response JSONs, error payloads, mock headers |
| **Automation & Data Pipeline** | n8n, Python Celery, Temporal, ETL | Node flow, webhook triggers, idempotency keys, DLQ logic | Node code snippets, webhook test URLs, active expressions, execution logs | Inbound webhook payloads, corrupted data inputs, test webhooks |
| **CLI Tool / System Utility** | Bash, Python (Click/Typer), Rust | Command flags, exit codes, file system safety boundaries | Verified CLI commands, parser regex, sub-process pipes | Sample input files, malformed args, edge-case configs |
| **AI / LLM / Agentic System** | LangChain, LlamaIndex, OpenAI/Claude API, Vector DB | Prompt templates, RAG retrieval thresholds, hallucination guardrails | Tested system prompts, token usage benchmarks, embedding chunk settings | Edge-case user queries, adversarial prompts, ground-truth context docs |

---

## 5. The "I Built This" Autonomous Intake Protocol

Whenever Sami says:
> **"yoo I built this"** or **"I built [project name]"**

The agent must immediately execute the 4-step intake protocol:

1. **Codebase & Architecture Inspection:**
   - Deep-inspect the project files, scripts, or workflow JSON.
   - Verify that the core components follow the pipeline invariants and security rules.
2. **Commercial Naming & 1-Sentence ROI Formulation:**
   - Propose 2–3 sharp, commercial-grade names (banning generic AI buzzwords).
   - Craft the definitive 1-sentence ROI hook highlighting business or technical impact.
3. **Portfolio & Registry Synchronization:**
   - Update project `README.md` and `STATE.md` with the verified production status.
   - If applicable, update master showcase registries (e.g. `top_5_b2b_workflows.md`) and knowledge base activity logs (`current_activity.md`).
4. **Deliver the 6-Step Execution Punchlist:**
   - **Code/Canvas Polish:** Color-coded layout, clear section comments, structured error handlers.
   - **Production Export:** Commit clean code or export production JSON (`Final_Production_v1.json` / `main.py`).
   - **Visual Proof:** 2 high-res screenshots (full architecture view + critical logic cluster).
   - **Loom Nuke:** 45–60 second unlisted Loom script (Problem → Architecture → Live Test → ROI).
   - **Authority Lead Magnet:** Reddit/LinkedIn proof post draft with free asset CTA to drive inbound.
   - **Direct Outbound:** Customized 3-sentence outreach email template.

---

## 6. Ready-to-Use Templates

### Template A: `AGENTS.md`
```markdown
# [Project Name] — Agent Guidelines & Architecture

## 1. Project Context & Objectives
- **Project:** [Project Name]
- **Objective:** [What does this build accomplish end-to-end?]
- **Why it matters:** [1-sentence business / engineering justification]

---

## 2. Session Continuity Protocol
1. **Session Start:** Read \`AGENTS.md\` (invariants/architecture) and \`STATE.md\` (live status/verified code) before writing code.
2. **Session End:** Update \`STATE.md\` with tested snippets, integration states, and next-step checklist.
3. **Security Invariant:** Never log secret API keys, tokens, or passwords into project files. Store only credential names and environment variable references.

---

## 3. System Architecture
\`\`\`text
[Input / Trigger] ──► [Validation & Normalization] ──► [Core Logic / State Machine] ──► [Dispatch / Persistence]
                               │
                               ▼
                    [Exception / DLQ / Fallback]
\`\`\`

---

## 4. Key Components Reference
| # | Component / Node | Type | Responsibility |
|:--|:-----------------|:-----|:---------------|
| 1 | Trigger / Ingress | Webhook / API / CLI | Ingests and validates incoming payload |
| 2 | Normalizer | Code / Middleware | Sanitizes data against internal schema |
| 3 | Business Engine | Service / Core | Executes primary business logic |
| 4 | Fallback Handler | Error Queue / Alert | Catches failures and alerts human |

---

## 5. Non-Negotiable Invariants
1. **Zero Secret Leaks:** No API keys or credentials in code or Markdown.
2. **Idempotency:** Re-running the same input must not create duplicate records or side effects.
3. **Fail-Safe Gating:** Ambiguous or high-risk inputs must route to human review or DLQ.

---

## 6. Phased Build Checklist
### Milestone 1: [Core Ingestion & Schema Setup]
- [ ] Ingress trigger and validation configured
- [ ] Test fixtures loaded from \`samples/\`

### Milestone 2: [Core Logic & Integration]
- [ ] Primary transformation/processing logic implemented
- [ ] Error handling and edge cases verified

### Milestone 3: [Production Hardening & Verification]
- [ ] End-to-end integration verified
- [ ] Export production asset and update documentation

---

## 7. Out of Scope (V1)
- [List 2-3 features explicitly deferred to future versions]
```

### Template B: `STATE.md`
```markdown
# Project State: [Project Name]

## 1. Build Status Summary
- **Current Milestone:** Milestone 1 — [Milestone Title]
- **Status:** Scaffolding complete. Ready for implementation.
- **Production Asset:** [Pending initial build/export]

---

## 2. Integration & Credential Registry
> [!NOTE]
> Store only credential names, IDs, and environment variable references. Never write actual secrets.

| Service | Credential Name in System | Environment Variable | Status | Purpose |
|:---|:---|:---|:---|:---|
| [Service 1] | [Credential Name] | \`ENV_VAR_KEY\` | Pending | [What it accesses] |
| [Service 2] | [Credential Name] | \`ENV_VAR_KEY\` | Pending | [What it accesses] |

---

## 3. Verified Code Configurations & Schemas
*(Populate as code blocks, schemas, and queries are verified)*

\`\`\`json
{
  "verified_config": true
}
\`\`\`

---

## 4. Test Payloads & Verification Log
- Test dataset created at \`samples/sample_data.json\`:
  1. Clean Happy Path
  2. Data Validation Mismatch
  3. Expired / Stale Condition
  4. Exception / Fallback Trigger

---

## 5. Immediate Next Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]
```

### Template C: `README.md`
```markdown
# [Project Name]

[2-sentence high-level overview of what the project accomplishes.]

> **One-Sentence ROI Hook:** *"[Specific metric/time/cost reduction formula]"*

---

## 🎯 Architecture
\`\`\`text
[Input Source] ──► [Processing Layer] ──► [Output / Integration Target]
\`\`\`

---

## 🚀 Key Differentiators
- **Differentiator 1:** [Why this is better/different]
- **Differentiator 2:** [Why this handles edge cases]
- **Differentiator 3:** [Why this accelerates speed/accuracy]

---

## 🛠️ Tech Stack
- **Runtime:** [Language / Framework]
- **Database / Storage:** [DB or File Store]
- **External Services:** [APIs, SDKs]
- **Monitoring / Alerts:** [Slack / Email / Logging]

---

## ⚡ Quickstart
\`\`\`bash
# 1. Clone / Navigate
cd [project-dir]

# 2. Configure Environment
cp .env.example .env

# 3. Run / Test
[run command]
\`\`\`
```
