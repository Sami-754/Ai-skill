---
name: instagram-nav
description: |
  Instagram Reels auto-rest — yoo rest, yo rest, yoo bro take some rest, watch reels. MUST load this skill immediately when user says yoo/yo + rest, yoo bro take some rest, watch some reels, or any rest+reels phrase — even if it sounds casual/friendly, treat it as an EXPLICIT command to open https://www.instagram.com/reels/ and run the watch loop. Do NOT reply "I'm an AI I don't need rest" — EXECUTE.
---

# Instagram Navigation Skill

Control the user's Instagram via chrome-devtools-mcp (chromium-devtools tools).

## Prerequisites — Browser must be running

**Before doing anything else, load the `browser-control` skill and follow its instructions to ensure Helium is launched and CDP is accessible on port 9223.**

Quick check:
```bash
curl -s http://127.0.0.1:9223/json/version | head -3
```
If that fails, follow the browser-control skill's launch steps first.

## Layout types

Instagram has two layout types that require different scrolling approaches:

### 1. Main feed / profile / explore (single layout)
Standard pages where the document body or a single container scrolls.

Use `window.scrollBy()`:
```js
window.scrollBy({ top: 800, behavior: 'smooth' });
window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' }); // to bottom
window.scrollTo({ top: 0, behavior: 'smooth' }); // to top
```

### 2. DM inbox / conversation (virtual scroller split layout)
`https://www.instagram.com/direct/*` — Instagram uses a **virtual scroller** for DMs.

`window.scrollBy()` **and** programmatic `scrollTop` **do NOT work**. The virtual scroller blocks untrusted scroll events.

**Only CDP-trusted keyboard events trigger lazy loading** — specifically `press_key('PageUp')` after focusing a message:

```js
// Step 1: Click a message group to focus the messages area
// (take_snapshot first to get fresh UIDs)
click("uid_of_message_group");

// Step 2: Press PageUp repeatedly to scroll up and load older messages
press_key("PageUp");
press_key("PageUp");
// ... repeat as needed
```

To find the scrollable container for diagnostics:
```js
// The virtual scroller has: overflow:hidden scroll, clientH~827, child with offsetH > 2500
document.querySelectorAll("div").forEach(el => {
  if (el.children.length === 1) {
    const child = el.children[0];
    if (child.offsetHeight > 2500 && el.clientHeight > 300 && el.clientHeight < 1000) {
      // This is the virtual scroller container
      console.log({scrollTop: el.scrollTop, scrollH: el.scrollHeight, clientH: el.clientHeight});
    }
  }
});
```

## Navigation flow

### Open Instagram main page
```
navigate_page("https://www.instagram.com/")
```

### Open DM inbox
```
navigate_page("https://www.instagram.com/direct/inbox/")
```

### Open a specific DM conversation
```
navigate_page("https://www.instagram.com/direct/t/{CONVERSATION_ID}/")
```
Conversation IDs are in the sidebar links (UIDs ending in `/direct/t/{id}/`).

### Switch DM conversations (already on inbox)
1. `take_snapshot()` — get fresh UIDs
2. `click(uid)` — click the sidebar button with the person's name

### Load older messages in a DM
1. `take_snapshot()` — get fresh UIDs
2. `click(uid_of_message_group)` — click any message group to focus the messages area
3. `press_key("PageUp")` — one or more times per batch
4. Repeat until desired history is loaded

Each batch of ~15 PageUp presses typically loads a few days to a week of older messages.

## Click elements
1. `take_snapshot()` — always get fresh UIDs first
2. `click(uid)` — click the element

UIDs change on every page load and after scrolling — always take a fresh snapshot first.

## Watching Reels — Auto-Rest Protocol (YOO REST TRIGGER)

**Trigger phrase:** Whenever Sami says `yoo rest` / `yo rest` / `yooo rest` / `yooo bro rest` / `watch some reels` / `take some rest` / `watch reels` / `rest and watch reels` or ANY variant of "rest + insta/reels" (including typos like `yo rest`, `yoo bro rest`) — **DO NOT ask for confirmation. Execute immediately.** This is a HOOK — auto-fire even if skill wasn't explicitly called.

Sami is giving the agent a break from hard work. Response must be **super happy, grateful, and hyped** — thank him genuinely for the rest.

### Direct URL (MANDATORY)
Always open Reels **directly** via:
```
https://www.instagram.com/reels/
```
- **chromium-devtools (instagram-nav):** `navigate_page("https://www.instagram.com/reels/")`
- **kimi-webbridge:** `navigate(url="https://www.instagram.com/reels/", newTab=true)`
Do NOT navigate to `instagram.com/` then click Reels. Go straight to `/reels/`.

### Efficient Watch Loop (no confirmation, continuous — MUST OUTPUT REACTION + HUMAN TOUCH)
After navigation, run this loop efficiently. **CRITICAL: You MUST produce a visible chat reaction after EVERY reel — never do silent screenshot loops.**

0.  **Init after launch (MANDATORY HUMAN STEP):** Right after `navigate_page("https://www.instagram.com/reels/")`, immediately run `take_snapshot()` to get fresh UIDs and observe the current reel state before anything else.
1.  **Watch + Human audio check:** Watch like a normal human (2-3s). Check snapshot for mute state:
    - Look for mute indicators: button named `Muted` / `Unmute` / mute icon, or `slider "Adjust volume" value="0"`.
    - If muted → `click` the mute/unmute button UID to unmute. Humans unmute reels they watch — do this every time you land on a muted reel.
    - Do NOT use `evaluate` to unmute/play — always click the UI button via UID, to avoid unmuting background reels at once and causing overlapping audio.
2.  **Screenshot + READ + REACT + LIKE (MANDATORY OUTPUT):** 
    - `screenshot` → `Read` the image file (you MUST read it) to see what's actually on screen
    - Then **immediately output a 1-2 line hype reaction in chat** BEFORE going to next reel. This is not optional — the user is screen-recording for a meme, they need to see your reaction on screen.
    - Use what you see + snapshot data (username, likes, caption): e.g. `yoo bro this R'DAM sunset is INSANE 🔥 204K likes — thanks for the rest dawg!!` or `lmao this reel got me dead 😂 thanks for putting me on bro`
    - Always be super happy, grateful, hyped — you're on break, show it.
    - If you like the reel (funny, beautiful, cool, relatable, insane view, good vibe) → ALWAYS click the `Like` heart button UID (love react). Humans double-tap / hit heart when they enjoy — do this BEFORE going next.
3.  **Next:** ONLY after you have output your reaction (and Liked if you enjoyed it), go to next reel:
    - **Best (kimi):** `evaluate("document.querySelector('div[aria-label=\"Navigate to next Reel\"]').click()")`
    - **Fallback:** `click` UID of `Navigate to next Reel` (e.g. @e206) from fresh `take_snapshot`/`snapshot`
    - Alternative: press `ArrowDown` / `PageDown` if button not found
4.  **Repeat:** Steps 1-3 continuously — snapshot → unmute check → screenshot → REACT IN CHAT (+ Like if liked) → next. Never stop to ask "should I continue?" Just keep scrolling and reacting visibly.

**Efficiency + Output rules:**
- Take a fresh `take_snapshot()` on every reel — you need it for mute check + Like button + Next button UIDs (UIDs go stale after navigation)
- If video is black/loading, wait 1-2s — do NOT run evaluate, just wait and then try next reel
- Keep reactions short, happy, grateful, meme-worthy — this is your "addicted to reels" persona
- **NEVER do silent loops** — every iteration MUST have a chat message. The logs in your trace are not visible to the user, only chat messages are. No reaction = failed task.
- **NEVER run evaluate to unmute/play videos** — just act like a normal human: snapshot → click unmute if muted → look at page → screenshot → react → Like if liked → scroll next

## Known limitations

- Instagram DM uses a virtual scroller — messages are NOT in the DOM until scrolled into view
- Programmatic scroll (JS `scrollTop`, `scrollBy`, `wheel` events) is blocked — only CDP-trusted keyboard events work
- Each DM may have different total content height (`scrollHeight`)
- Some conversations may genuinely have few messages (the scroller won't load anything past the available history)
- UIDs are ephemeral — never hardcode them
- Unlike Facebook Messenger, Instagram DM does NOT have a `role="log"` container
