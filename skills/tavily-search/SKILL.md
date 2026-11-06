---
name: tavily-search
description: |
  Search, extract, crawl, map, and research the web using the official Tavily command-line tool (`tvly`).
  Use this skill whenever an agent needs web intelligence: searching current facts or news,
  extracting clean markdown from URLs, discovering site URL structures, bulk crawling docs,
  or running autonomous cited deep research. This is a command-line interface tool (CLI) run via Bash.
allowed-tools:
  - Bash(tvly *)
---

# Tavily CLI (`tvly`) Complete Reference

Tavily is a dedicated command-line interface tool (`tvly`). All operations are executed directly in the shell using `tvly <command> [flags]`. Running as a native CLI ensures universal, immediate portability across all AI coding agents (Claude Code, OpenAI Codex, Antigravity, OpenCode, Cursor, Pi, Kilo, Gemini CLI) with zero configuration overhead.

Verify authentication and version:
```bash
tvly --status
```

---

## Global Options & Behaviors

* `--status`: Print version and authentication status.
* `--version`: Print CLI version and exit.
* `--json`: Emit clean JSON to `stdout` (spinners/logs go to `stderr`).
* `--help`: Available for any command (`tvly search --help`, etc.).
* **Agent Shell Detection**: When stdout is not a TTY (in pipes or agent execution), `tvly` automatically disables ANSI colors and formats output cleanly (snippets for search, raw markdown for extract/crawl, plain URLs for map).
* **Stdin Support**: Use `-` as query argument to read from stdin:
  ```bash
  echo "python 3.13 free threaded gil" | tvly search -
  ```
* **Smart Output Flag (`-o`)**:
  - `-o <filepath>`: Saves full JSON response to specified file path (creates directories automatically).
  - `-o` (without value): Automatically saves full payload to `.tavily/<command>-<slug>-<hash>.json` and creates a local `.gitignore` so outputs stay out of git commits.

---

## Exit Codes

| Code | Meaning | Agent Action |
| :---: | :--- | :--- |
| **`0`** | Success | Parse output. |
| **`2`** | Invalid input or CLI usage error | Check argument names, types, or missing parameters. |
| **`3`** | Authentication failure | Run `tvly login` or check `TAVILY_API_KEY`. |
| **`4`** | API error (rate limits, network timeout) | Back off or retry with lower depth/limits. |

---

## Command Reference & Full Options

### 1. `tvly search [QUERIES]...`
Search the web with AI-optimized ranking and extraction.
- **Parallel Multi-Query:** Pass up to 5 queries simultaneously to execute them in parallel:
  ```bash
  tvly search "fastapi lifespan" "pydantic v2 migration" --depth advanced --json
  ```

| Option | Type / Choices | Default | Description |
| :--- | :--- | :---: | :--- |
| `--depth` | `ultra-fast` \| `fast` \| `basic` \| `advanced` | `basic` | Search depth (`advanced` gives highest quality reranked passages). |
| `--max-results` | integer (`0-20`) | `5` | Number of results to return. |
| `--topic` | `general` \| `news` \| `finance` | `general` | Optimizes ranking algorithm for topic domain. |
| `--time-range` | `day` \| `week` \| `month` \| `year` | — | Relative time filter. |
| `--start-date` / `--end-date` | `YYYY-MM-DD` | — | Explicit publication date boundaries. |
| `--include-domains` | comma-separated | — | Hard whitelist of domains (`docs.astral.sh,github.com`). |
| `--exclude-domains` | comma-separated | — | Blacklist of domains. |
| `--country` | country code (e.g. `us`, `gb`) | — | Boost results from specific country. |
| `--include-answer` | `basic` \| `advanced` | — | Include an AI summary answer. |
| `--include-raw-content` | `markdown` \| `text` | — | Embed full page markdown directly in search results. |
| `--include-images` | flag | `false` | Include image results. |
| `--include-image-descriptions`| flag | `false` | Include AI-generated image descriptions. |
| `--chunks-per-source` | integer | — | Chunks per source (requires `fast` or `advanced` depth). |
| `--max-chars` | integer | `600` | Snippet character limit printed to stdout (0 = whole). |
| `-o`, `--output` | filepath or flag | — | Save JSON output to file (or auto-save in `.tavily/`). |
| `--client-name` | string | — | Attribution client name. |
| `--json` | flag | `false` | Output structured JSON. |

---

### 2. `tvly extract URLS...`
Extract clean markdown or plain text from 1 to 20 URLs in a single invocation, handling client-side JS rendering.
```bash
tvly extract https://docs.python.org/3/whatsnew/3.13.html --extract-depth advanced --json
```

| Option | Type / Choices | Default | Description |
| :--- | :--- | :---: | :--- |
| `--query` | string | — | Reranks and extracts passages specifically answering this query. |
| `--chunks-per-source` | integer (`1-5`) | — | Number of targeted chunks to return (requires `--query`). |
| `--extract-depth` | `basic` \| `advanced` | `basic` | `advanced` renders full client JS and complex tables. |
| `--format` | `markdown` \| `text` | `markdown` | Output format. |
| `--include-images` | flag | `false` | Include image URLs found in article. |
| `--timeout` | float (`1-60`) | — | Timeout in seconds. |
| `-o`, `--output` | filepath or flag | — | Save output to file. |
| `--json` | flag | `false` | Output structured JSON. |

---

### 3. `tvly map URL`
Discover and enumerate all URLs across a website without downloading bodies.
```bash
tvly map https://docs.stripe.com/ --instructions "Payment Intents API and webhooks" --limit 20 --json
```

| Option | Type / Choices | Default | Description |
| :--- | :--- | :---: | :--- |
| `--limit` | integer | `50` | Maximum URLs to discover. |
| `--max-depth` | integer (`1-5`) | `1` | Traversal depth from root URL. |
| `--max-breadth` | integer | `20` | Maximum links followed per page. |
| `--instructions` | string | — | Natural language guidance to steer discovery. |
| `--select-paths` | regex | — | Comma-separated regex whitelist (`^/docs/.*`). |
| `--exclude-paths` | regex | — | Comma-separated regex blacklist. |
| `--select-domains` | regex | — | Comma-separated domain whitelist. |
| `--exclude-domains` | regex | — | Comma-separated domain blacklist. |
| `--allow-external` / `--no-external` | boolean | `false` | Traverse external domain links. |
| `--timeout` | float (`10-150`) | — | Timeout in seconds. |
| `-o`, `--output` | filepath or flag | — | Save discovered URL list to file. |
| `--json` | flag | `false` | Output JSON array. |

---

### 4. `tvly crawl URL`
Recursively crawls a website and extracts markdown content from every visited page.
```bash
tvly crawl https://docs.fastapi.tiangolo.com/tutorial/ --select-paths '^/tutorial/.*' --limit 15 --output-dir ./fastapi-docs
```

| Option | Type / Choices | Default | Description |
| :--- | :--- | :---: | :--- |
| `--limit` | integer | `50` | Total pages cap. Always define a limit. |
| `--max-depth` | integer (`1-5`) | `1` | Traversal depth. |
| `--max-breadth` | integer | `20` | Maximum links followed per page. |
| `--instructions` | string | — | Natural language focus guidance. |
| `--chunks-per-source` | integer (`1-5`) | — | Chunks per page (requires `--instructions`). |
| `--extract-depth` | `basic` \| `advanced` | `basic` | JS execution depth. |
| `--format` | `markdown` \| `text` | `markdown` | Extracted format. |
| `--output-dir` | directory path | — | **Saves each crawled page as a `.md` file in this directory.** |
| `--select-paths` / `--exclude-paths` | regex | — | Path inclusion/exclusion regex. |
| `--select-domains` / `--exclude-domains` | regex | — | Domain inclusion/exclusion regex. |
| `--allow-external` / `--no-external` | boolean | `false` | Follow external links. |
| `--include-images` | flag | `false` | Include images. |
| `--timeout` | float (`10-150`) | — | Timeout in seconds. |
| `-o`, `--output` | filepath or flag | — | Save full crawl JSON payload to file. |
| `--json` | flag | `false` | Output JSON. |

---

### 5. `tvly research` (Autonomous Deep Research)
Coordinates multi-source cited research briefs using Tavily's research agent backend.

#### Commands
* **Run research synchronously:**
  ```bash
  tvly research run "State of WebAssembly runtimes in 2025" --model auto --citation-format numbered -o report.json
  ```
* **Fire-and-forget (asynchronous):**
  ```bash
  tvly research run "Quantum computing commercial readiness" --no-wait --json
  # Returns: {"request_id": "req_abc123"}
  ```
* **Check status:**
  ```bash
  tvly research status req_abc123 --json
  ```
* **Poll until finished:**
  ```bash
  tvly research poll req_abc123 --poll-interval 10 --timeout 600 -o report.json
  ```

| Option | Choices | Default | Description |
| :--- | :--- | :---: | :--- |
| `--model` | `mini` \| `pro` \| `auto` | `auto` | `mini` (fast factual brief), `pro` (comprehensive), `auto` (adaptive). |
| `--no-wait` | flag | `false` | Returns `request_id` immediately. |
| `--stream` | flag | `false` | Streams progress in real time. |
| `--output-schema` | filepath | — | Path to JSON schema file to enforce structured output. |
| `--citation-format` | `numbered` \| `mla` \| `apa` \| `chicago` | — | Citation style for generated reports. |
| `--poll-interval` | seconds | `10` | Frequency of status checks when polling. |
| `--timeout` | seconds | `600` | Max duration before timing out. |
| `-o`, `--output` | filepath or flag | — | Save report and source data to file. |
| `--json` | flag | `false` | Output raw JSON. |

---

## System & Config Utilities

* `tvly auth`: Inspect authentication source and identity.
* `tvly login`: Interactive browser OAuth or `--api-key tvly-YOUR_KEY` (`--no-browser` for headless).
* `tvly logout`: Purge stored credentials.
* `tvly set-default [--claude|--codex] [--project]`: Configures Tavily CLI as the primary search engine for coding agents.
* `tvly unset-default`: Restores original agent search defaults.
* `tvly update [--check] [--json]`: Checks for or installs CLI binary updates.
* `tvly init [--all] [--yes] [--skip-auth] [--skip-skills]`: Automatic agent skills setup.
