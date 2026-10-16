---
name: facebook-nav
description: |
  Navigate and interact with Facebook — scroll feed, open Messenger, read chats, click posts. Use this skill whenever the user mentions Facebook, Messenger, scrolling Facebook, checking messages, or interacting with Facebook in any way.
---

# Facebook Navigation Skill

Control the user's Facebook via chrome-devtools-mcp (chromium-devtools tools).

## Prerequisites — Browser must be running

**Before doing anything else, load the `browser-control` skill and follow its instructions to ensure Helium is launched and CDP is accessible on port 9223.**

Quick check:
```bash
curl -s http://127.0.0.1:9223/json/version | head -3
```
If that fails, follow the browser-control skill's launch steps first.

## Layout types

Facebook has two layout types that require different scrolling approaches:

### 1. Main feed (single layout)
`https://www.facebook.com/` — the document body itself scrolls.

Use `window.scrollBy()`:

```js
window.scrollBy({ top: 800, behavior: 'smooth' });
window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }); // to bottom
window.scrollTo({ top: 0, behavior: 'smooth' }); // to top
```

### 2. Messenger (split layout)
`https://www.facebook.com/messages/*` — independent left sidebar + right messages panel.

`window.scrollBy()` does nothing. Find the scrollable divs:

```js
// Find all scrollable containers
const divs = [];
document.querySelectorAll("div").forEach(el => {
  const s = window.getComputedStyle(el);
  if ((s.overflowY === "auto" || s.overflowY === "scroll") && el.scrollHeight > el.clientHeight + 200) {
    divs.push(el);
  }
});
// divs[0] = left sidebar (thread list)
// divs[1] = right messages panel
divs[0].scrollBy({ top: 300, behavior: 'smooth' }); // scroll sidebar
divs[1].scrollBy({ top: 300, behavior: 'smooth' }); // scroll messages
divs[1].scrollTo({ top: 0, behavior: 'smooth' });   // scroll messages to top (load older)
```

## Navigation flow

### Open Facebook main page
```
navigate_page("https://www.facebook.com/")
```

### Open Messenger
Click the Messenger button in the top bar, or navigate directly:
```
navigate_page("https://www.facebook.com/messages/t/")
```

### Open a specific chat
```
navigate_page("https://www.facebook.com/messages/t/{CONVERSATION_ID}/")
```
Find conversation IDs from the sidebar links (they end in `/messages/t/{id}/` or `/messages/e2ee/t/{id}/`).

### Click elements
1. `take_snapshot()` — get current UIDs
2. `click(uid)` — click the element

UIDs change on every page load — always take a fresh snapshot first.

## Known limitations

- Messenger lazy-loads older messages when you scroll up; **trigger by scrolling `divs[1]` to `scrollTop = 0`** multiple times
- Smooth scroll (`behavior: "smooth"`) may not trigger Facebook's lazy load; use instant `scrollTop = 0` instead
- UIDs are ephemeral — never hardcode them
