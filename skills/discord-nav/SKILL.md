---
name: discord-nav
description: |
  Navigate and interact with Discord — read channels, DMs, scroll chat history, switch servers. Use this skill whenever the user mentions Discord, Discord DMs, Discord servers, reading Discord messages, or interacting with Discord in any way.
---

# Discord Navigation Skill

Control the user's Discord via chrome-devtools-mcp (chromium-devtools tools).

## Prerequisites — Browser must be running

**Before doing anything else, load the `browser-control` skill and follow its instructions to ensure Helium is launched and CDP is accessible on port 9223.**

Quick check:
```bash
curl -s http://127.0.0.1:9223/json/version | head -3
```
If that fails, follow the browser-control skill's launch steps first.

## Layout types

Discord has three layout areas that require different scrolling approaches:

### 1. Servers sidebar (leftmost column)
The server list (`navigation "Servers sidebar"`) is a tree element. Scroll by clicking different server/folder treeitems to navigate.

### 2. DM list / channel list (middle column)
`https://discord.com/channels/@me` — the DM list (`navigation "Private channels"`) is a scrollable container that uses `overflow-y: auto`. Same applies inside a server — the channel list is also the first scrollable div.

Use `evaluate_script` to scroll it:

```js
// Find all scrollable containers
const divs = [];
document.querySelectorAll("div").forEach(el => {
  const s = window.getComputedStyle(el);
  if ((s.overflowY === "auto" || s.overflowY === "scroll") && el.scrollHeight > el.clientHeight + 50) {
    divs.push(el);
  }
});
// divs[0] = left sidebar (DM list OR server channel list)
// divs[1] = right messages panel
divs[0].scrollBy({ top: 300, behavior: 'smooth' }); // scroll channel list down
divs[0].scrollBy({ top: -300, behavior: 'smooth' }); // scroll channel list up
```

### 3. Messages panel (right panel — both DMs and servers)
The messages area uses Discord's virtual scroller. **1 PageUp or PageDown press** is enough per scroll batch. Works the same in DMs and server text channels.

```js
// Step 1: Click a message to focus the messages area
// (take_snapshot first to get fresh UIDs)
click("uid_of_message");

// Step 2: Press PageUp or PageDown
press_key("PageUp");   // load older messages
press_key("PageDown"); // scroll back to recent
```

To jump directly to the latest messages, click the "Jump To Present" button (appears when viewing old messages).

## Navigation flow

### Open Discord main page
```
navigate_page("https://discord.com/channels/@me")
```

### Open DM inbox
Discord loads DMs at `https://discord.com/channels/@me`. The DM list is on the left sidebar.

### Open a specific DM conversation
```
navigate_page("https://discord.com/channels/@me/{CONVERSATION_ID}/")
```
Conversation IDs are in the sidebar links (URLs ending in `/channels/@me/{id}/`).

### Switch DM conversations (already on inbox)
1. `take_snapshot()` — get fresh UIDs
2. `click(uid)` — click the person's name in the DM list

### Open a server channel
1. In the servers sidebar, click the server icon (treeitem)
2. Then click a text/voice channel from the channel list

### Load older messages
1. `take_snapshot()` — get fresh UIDs
2. `click(uid_of_message)` — click any message to focus the messages area
3. `press_key("PageUp")` — one press loads more

## Click elements
1. `take_snapshot()` — always get fresh UIDs first
2. `click(uid)` — click the element

UIDs change on every page load and after scrolling — always take a fresh snapshot first.

## Known limitations

- Discord uses a virtual scroller for messages — old messages may not be in the DOM
- The server sidebar uses a tree structure — click treeitems to expand folders and select servers
- UIDs are ephemeral — never hardcode them
- Discord has a `role="log"` container for messages (live region) — unlike Instagram
