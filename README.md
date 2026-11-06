# Agent Skills & Tools Collection

> A comprehensive, production-tested collection of **100+ AI agent skills**, rules, and hooks designed for coding assistants (Antigravity, Claude Code, OpenAI Codex, OpenCode, Cursor, Pi, Kilo, Gemini CLI).

Built with a **CLI-first philosophy**: all tools run natively via standalone command-line utilities (`tvly`, `firecrawl`, `strix`, `semgrep`, `brag`, `harvey`, `reticle`, `awwwards`), giving universal compatibility across all AI agents with zero MCP setup overhead.

---

## Repository Structure

```text
~/.agents/
├── skills/             # 100+ modular, task-specific agent skills
├── hooks/              # Agent execution lifecycle hooks
├── rules/              # Agent rules and operational guidelines
├── .skill-lock.json    # Skill version and lockfile
├── .gitignore          # Ignores runtime caches and virtual environments
└── README.md
```

---

## Core Tooling & Skill Highlights

### 1. Web Extraction & Search (CLI-Native)
* **Tavily CLI (`tvly`)**: Multi-query parallel web search, full markdown extraction, domain mapping, site crawling, and autonomous deep research briefs.
* **Firecrawl CLI (`firecrawl`)**: Scraping SPAs, recursive crawling, structured extraction, and arXiv research paper exploration.
* **Exa CLI (`exa-cli`)**: Semantic, neural web searching.

### 2. Application Security & Code Auditing
* **Strix Pentesting (`strix`)**: Autonomous web app penetration testing, OWASP Top 10 exploits, API security testing, and vulnerability remediation.
* **Semgrep SAST (`semgrep`)**: AST-based code analysis, secret discovery, and vulnerability hunting.

### 3. Media & Creative Engineering
* **Hyperframes & Brag (`brag`, `hyperframes`)**: Programmatic launch video generation from source code.
* **Awwwards Jury Standards (`awwwards`)**: Agency-grade design scoring, animation audits, and checklist validation.

### 4. GTM & Account Intelligence
* **Harvey Sales Engine (`harvey`)**: Outbound sales daemon, multi-stakeholder account navigation, cold email crafting, and signal tracking.

### 5. In-Browser Verification & QA
* **Reticle (`reticle`)**: Autonomous in-browser assertions and DOM verification.
* **CDP & Social Automation**: Direct browser control for Chromium and Firefox.

### 6. Frontend Craft & Architecture
* **Design Systems & Anti-Slop**: `impeccable`, `anti-slop-ajonai`, `gpt-taste`, `design-taste-frontend`, `industrial-brutalist-ui`, `minimalist-ui`.
* **The Ponytail Senior Dev Engine**: `ponytail`, `ponytail-audit`, `ponytail-review`, `ponytail-debt`.
* **Editorial & Technical Writing**: `anti-slop-writing`, `unslop`, `deslop`, `writing-guidelines`.

---

## Installation & Setup

Clone directly into your local agent configuration directory:

```bash
git clone https://github.com/Sami-754/Ai-skill.git ~/.agents
```

Or sync into an existing setup:
```bash
cp -r skills hooks rules ~/.agents/
cp .skill-lock.json ~/.agents/
```
