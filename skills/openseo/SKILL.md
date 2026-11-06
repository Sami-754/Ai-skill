---
name: openseo
description: "Autonomous SEO Suite & MCP Server. Run site audits, keyword research, SERP competitor analysis, AI visibility checks, and rank tracking via OpenSEO MCP tools or terminal CLI."
---

# OpenSEO

> Open source alternative to Semrush and Ahrefs with native AI Agent Skills and MCP integration.

OpenSEO is an autonomous SEO tool designed for AI agents and developers. It allows agents to perform deep keyword research, technical site audits, competitor organic footprint analysis, backlink discovery, and AI answer visibility tracking (GEO/AEO) using live DataForSEO and Google SERP data.

---

## 1. Quick Terminal CLI Commands

OpenSEO provides a global CLI controller on `$PATH` (`open-seo` or alias `openseo`):

```bash
# Check service health and URLs
open-seo status

# Start local OpenSEO container (running on dedicated port 3080)
open-seo start

# Stop local container
open-seo stop

# View live container logs
open-seo logs

# View MCP server configuration instructions
open-seo mcp

# Open web interface in default browser
open-seo open
```

---

## 2. MCP Server Connectivity

OpenSEO exposes an MCP endpoint that coding agents (Antigravity, Codex, Claude Code, Pi, Cursor) connect to:

### A. Hosted OpenSEO
- Endpoint: `https://app.openseo.so/mcp`
- Authentication: API key from [app.openseo.so/settings](https://app.openseo.so/settings)
- MCP Config snippet:
```json
{
  "mcpServers": {
    "openseo": {
      "type": "http",
      "url": "https://app.openseo.so/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_OPENSEO_API_KEY"
      }
    }
  }
}
```

### B. Local Self-Hosted OpenSEO
- Endpoint: `http://localhost:3080/mcp`
- Authentication: None required in `local_noauth` mode.
- MCP Config snippet:
```json
{
  "mcpServers": {
    "openseo-local": {
      "type": "http",
      "url": "http://localhost:3080/mcp"
    }
  }
}
```

---

## 3. Core MCP Tools Overview

AI agents with the OpenSEO MCP server enabled can wield the following tools:

| MCP Tool | Description |
| :--- | :--- |
| `whoami` | Verify connection status, user profile, and available search credits. |
| `list_projects` / `create_project` | List existing SEO projects or initialize a new project workspace. |
| `get_project_context` / `update_project_context` | Read or update domain goals, competitors, and saved target pages. |
| `research_keywords` | Discover keyword opportunities from 1-5 seed topics or competitor domains. |
| `get_keyword_metrics` | Hydrate up to 700 keywords with search volume, keyword difficulty (KD), CPC, and intent. |
| `get_ranked_keywords` | Pull exact organic rankings and driving queries for a target domain or specific URL. |
| `get_serp_results` | Live Google search result check (depth 20) with precise organic ranking positions. |
| `get_backlinks_overview` / `get_backlinks_profile` | Analyze referring domains, backlink velocity, anchor distribution, and authority. |
| `run_site_audit` / `get_audit_status` / `get_audit_issues` | Trigger and inspect comprehensive technical website crawl for broken links, metadata, and crawlability. |
| `search_local_businesses` / `get_local_serp_results` | Audit local Map Pack rankings, Google Business Profile questions, and local competition. |
| `save_report` / `list_reports` / `get_report` | Generate and export single-file, self-contained HTML reports with embedded metrics and charts. |

---

## 4. Specialized SEO Agent Skills Roster

The OpenSEO suite includes 13 specialized agent skills installed directly into `~/.agents/skills/`:

| Skill Name | Purpose & Workflow |
| :--- | :--- |
| **`seo-audit`** | Audit a website, investigate its real search opportunities, and deliver a short data-backed report on the highest-impact fixes. |
| **`keyword-research`** | Discover high-converting keyword opportunities, evaluate metrics and SERPs, and tag promising search queries. |
| **`keyword-clustering`** | Group target keywords by user search intent and map them to existing or planned website pages. |
| **`competitor-analysis`** | Analyze a competitor's organic search footprint, top pages, ranking keywords, backlinks, and content gaps. |
| **`competitive-landscape`** | Macro view mapping industry leaders, winning content clusters, keyword overlap, and strategic positioning. |
| **`ai-visibility-audit`** | Audit how a brand is cited and recommended in AI answer engines (ChatGPT, Gemini, Perplexity) and plan GEO/AEO optimization. |
| **`ai-prompt-research`** | Identify what questions users ask AI assistants about a market and examine which sources get cited. |
| **`local-seo`** | Audit Google Business Profile, compare local competition, and map Google Maps visibility. |
| **`link-prospecting`** | Discover high-authority link prospects from SERPs and backlink graphs and prepare outreach angles. |
| **`seo-project-setup`** | Establish shared SEO context for a domain (scope, business overview, competitors, target audience). |
| **`seo-report`** | Format and publish research into self-contained HTML audit reports (under 80 KB) ready for export or PDF. |
| **`seo-coach`** | Interactive guidance mode that explains SEO concepts, guides prioritization, and suggests optimal workflows. |
| **`deslop`** | Strip AI writing mannerisms, filler, and corporate fluff from content to produce crisp, human-sounding copy. |
