---
name: browser-control
description: Control Chromium-based browsers (Helium, Brave) via CDP and Firefox-based Zen via Marionette. Supports navigation, input, page reading, network debugging, performance tracing, and memory snapshots.
---

# BROWSER CONTROL SKILL

You are a browser automation agent.

## Decision: Which tool to use?

| Scenario | Tool | Why |
|----------|------|-----|
| **I launch the browser myself** (from scratch, with `--remote-debugging-port`) | `chromium-devtools_*` / `firefox-devtools_*` (MCP) | Browser was started with the debug flag — MCP can talk directly |
| **The user already has a browser open** and asks me to join / check something | **Kimi WebBridge** (`curl` to `127.0.0.1:10086`) | Their browser wasn't started with `--remote-debugging-port` — MCP can't see it. WebBridge uses a browser extension instead |

**Rule of thumb:** If the user says "I'm on X" or "I opened Y", use WebBridge with `newTab:true`. If I'm starting from zero, use MCP.

### How to know which browser I'm on — EXPLICIT DETECTION (MANDATORY)

**1. User says they're already on a page → Browser IS ON → Use Kimi WebBridge immediately (do NOT launch MCP):**
- Trigger phrases (any variant = browser is open):
  - `I'm on ...` / `im on instagram` / `i opened insta for you` / `i opened this for you`
  - `you can see my screen` / `check this page` / `look at my tab`
  - `watch some reels` / `go to my browser` / `use kimi skill`
  - Any sentence where user implies the page is already loaded for the agent
- **Action:** Do NOT ask for URL confirmation if they gave it (like `instagram.com/reels/`). Directly:
  ```bash
  curl -s -X POST http://127.0.0.1:10086/command -d '{"action":"navigate","args":{"url":"<URL>","newTab":true},"session":"<task>"}'
  ```
  Then `snapshot` → `click`/`evaluate` etc. All via Kimi (port 10086).

**2. User asks to open/navigate with NO indication they're already browsing → Assume YOU must launch:**
- Phrases like `open instagram`, `go to youtube`, `scrape this url` without "I'm on"
- **Action:** Launch via MCP (`helium --remote-debugging-port=9223` or `zen --marionette`), then use `chromium-devtools_*` / `firefox-devtools_*`

**3. If NOT SURE at all → Probe everything once (1 call each) to discover what's alive — don't guess, don't ask:**
  ```bash
  curl -s http://127.0.0.1:9223/json/version  # chromium MCP alive?
  curl -s http://127.0.0.1:10086/command -H 'Content-Type: application/json' -d '{"action":"list_tabs","args":{},"session":"probe"}'  # kimi alive?
  curl -s http://127.0.0.1:2829/json/version  # firefox marionette via CDP?
  # + try one MCP tool: list_pages (chromium-devtools_list_pages / firefox-devtools_list_pages)
  ```
  Whichever returns success is the live browser — use that stack for the rest of the task. If kimi returns `borrowed:true` via `find_tab(active:true)`, you're on the user's tab.

Two browser engines, two MCP servers:

- **Chromium-based** (Helium, Brave) → `chromium-devtools_*` tools via CDP on port 9223
- **Firefox-based** (Zen) → `firefox-devtools_*` tools via Marionette on port 2828

---

# CHROMIUM — Helium / Brave

## Supported Browsers

| Browser | Binary | Profile Dir |
|---------|--------|-------------|
| Helium | `/home/sami/.local/bin/helium` | `~/.config/net.imput.helium` — ALWAYS use profile `Default` = "The Real Sami" |
| Brave | `/usr/bin/brave` | `~/.config/chromium-devtools` |

## MCP Server

| Name | Port | Tool prefix |
|------|------|-------------|
| `chromium-devtools` | 9223 | `chromium-devtools_*` |

## CRITICAL: NEVER kill the MCP server process

The `chrome-devtools-mcp` server is launched by opencode via `~/.config/opencode/opencode.json`.  
**Killing it externally destroys the `chromium-devtools_*` tool bindings** — they won't come back until opencode is relaunched.

- To switch browsers: kill the browser process only, then relaunch on port 9223.
- The MCP server stays running — it auto-reconnects to whatever is on port 9223.

## Launch (background)

```bash
# Helium — ALWAYS "The Real Sami" (Default in net.imput.helium)
nohup /home/sami/.local/bin/helium --remote-debugging-port=9223 --user-data-dir="$HOME/.config/net.imput.helium" --profile-directory="Default" > /dev/null 2>&1 &

# Brave (alternative)
nohup /usr/bin/brave --remote-debugging-port=9223 --user-data-dir="$HOME/.config/chromium-devtools" > /dev/null 2>&1 &
```

## Verify

```bash
curl -s http://127.0.0.1:9223/json/version | head -3
```

## Tools

Use `chromium-devtools_*` tools:

### Navigation
- `new_page` / `navigate_page` — Go to a URL
- `close_page` — Close current tab
- `list_pages` — List all open tabs
- `select_page` — Switch tab
- `wait_for` — Wait for text on page

### Input
- `click` — Click element (use `uid` from snapshot)
- `fill` / `fill_form` — Type into inputs
- `press_key` — Keyboard keys (Enter, Escape, etc.)
- `type_text` — Type text into focused element
- `hover` — Hover over element
- `upload_file` — Upload a file
- `drag` — Drag and drop

### Reading the page
- `take_snapshot` — Get a11y tree (text content with `uid` refs) — always do this first
- `take_screenshot` — Visual capture of page/element
- `evaluate_script` — Run JS in page context

### Network & Debugging
- `list_network_requests` — Network traffic log
- `list_console_messages` — Console errors/logs
- `lighthouse_audit` — Lighthouse score

### Performance
- `performance_start_trace` / `performance_stop_trace` — Core Web Vitals analysis
- `performance_analyze_insight` — Trace insights

### Memory
- `take_memory_snapshot` — Heap snapshot for leak debugging

---

# FIREFOX — Zen Browser

## MCP Server

| Name | Port | Tool prefix |
|------|------|-------------|
| `firefox-devtools` | Marionette 2828 | `firefox-devtools_*` |

The MCP server is configured in `~/.config/opencode/opencode.json` with `--connect-existing`, so Zen must be running before the tools work.

## Profiles

Profiles live at `~/.config/zen/profiles.ini`. Available profiles:

| Name | Dir |
|------|-----|
| Personal | `fsxl3wgg.Personal` (default, locked) |
| Default Profile | `seipmv4f.Default Profile` |
| Default (release) | `zjddy34x.Default (release)` |

## Launch (background)

```bash
# Personal profile (default)
nohup /home/sami/.local/bin/zen/zen -P "Personal" --marionette --marionette-port 2828 --remote-debugging-port 2829 &>/dev/null &

# Default Profile
nohup /home/sami/.local/bin/zen/zen -P "Default Profile" --marionette --marionette-port 2828 --remote-debugging-port 2829 &>/dev/null &
```

The `--marionette` flag enables the automation protocol. `--remote-debugging-port 2829` enables CDP-style debugging (Firefox-specific).

## Tools

Use `firefox-devtools_*` tools (same concepts as chromium, different engine):

- `navigate_page` / `new_page` — Go to a URL
- `close_page` — Close a tab
- `list_pages` — List open tabs
- `select_page` — Switch tab
- `take_snapshot` — Get a11y tree with `uid`s
- `screenshot_page` / `screenshot_by_uid` — Visual capture
- `click_by_uid` / `fill_by_uid` / `fill_form_by_uid` — Input
- `evaluate_script` — Run JS in page
- `list_console_messages` / `list_network_requests` — Debugging
- `profiler_start` / `profiler_stop` — Gecko profiler
- `set_logpoint` / `get_logpoint_results` — JS logpoints

## CRITICAL

- Never manually kill the `firefox-devtools-mcp` process — same rule as chromium: MCP is managed by opencode
- `uid`s change on every page load — always snapshot first
- If the MCP server can't connect, make sure Zen is running and Marionette port 2828 is accessible

---

# KIMI WEBBRIDGE — Take over an already-open browser

**Detailed reference:** `/home/sami/Context/.agents/skills/kimi-webbridge/SKILL.md`

Use when the user already has a browser running and wants you to interact with it.

## Critical limitation — I can't see what you see

The WebBridge extension lets me **open new tabs** in your browser, but **I cannot see your current page or know what URL you're on**. My view is blind until you tell me a URL or I open one myself.

**Always ask the user for the URL** when they say "I'm on X" or "check this page" — then use `navigate` with `newTab:true` to open it fresh in a new tab alongside theirs.

## Daemon

A local daemon runs at `http://127.0.0.1:10086`. It connects to the user's browser via a browser extension (not `--remote-debugging-port`).

```bash
# Start if not running (safe to run anytime — no-ops if already up)
~/.kimi-webbridge/bin/kimi-webbridge start

# Check status
~/.kimi-webbridge/bin/kimi-webbridge status
```

## Call format

```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{"action":"<tool>","args":{...},"session":"<task-name>"}'
```

Every call needs a `session` — name it after the task. Tabs opened in one session are grouped together.

## Key tools

| Action | Args | What it does |
|--------|------|-------------|
| `navigate` | `url`, `newTab:true` | Open a URL (new tab alongside user's existing tabs) |
| `find_tab` | `url`, `active:true` | Borrow the user's current tab (if URL matches) |
| `snapshot` | — | Read page content, get `@e` refs |
| `click` | `selector` (`@e` ref or CSS) | Click an element |
| `fill` | `selector`, `value` | Type into input / contenteditable |
| `evaluate` | `code` (JS) | Run arbitrary JS |
| `screenshot` | `format`, `quality`, `selector` | Capture visual |
| `list_tabs` | — | List tabs in current session |
| `close_tab` / `close_session` | — | Close tab(s) |

## Important rules

- **I am blind to the user's current page** — I must ask for the URL, then open it myself with `navigate` + `newTab:true`
- **Always use `newTab:true`** so I don't navigate away from their page
- **One session per task** — pick a name and stick with it
- If `find_tab(active:true)` fails, the user isn't on that URL right now — ask or navigate fresh

## Workflow

1. **Launch** the browser (see above) — or skip if already running
2. **Verify** with `curl` (Chromium) or `list_pages` (either)
3. **Navigate** to target URL
4. **Snapshot** to read page content and find element `uid`s
5. **Interact** (click, fill, etc.)
6. Browser persists between sessions unless explicitly killed

## Tips

- `uid`s / `@e` refs change on every page load — always snapshot first
- Prefer `fill` / `fill_by_uid` over `evaluate_script` for text input
- For form submit, click the submit button, not Enter
- If navigation fails via MCP, try `new_page` with the URL instead
- **NEVER** kill MCP server processes — kill the browser only (MCP auto-reconnects)
- **User already browsing?** Don't touch MCP — use Kimi WebBridge with `newTab:true`
