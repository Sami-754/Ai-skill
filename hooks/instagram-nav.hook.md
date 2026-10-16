# Hook: instagram-nav (CONDITIONAL)

**Scope:** Project-local — ` /home/sami/Context/.agents/` (NOT universal)
**Plugin:** `.opencode/plugin/instagram-hook.ts`
**Type:** Conditional — fires ONLY when task mentions Instagram

## When it fires
- Keywords: `instagram`, `insta`, `reels`, `direct`, `dm`, `inbox`, `yoo rest`, `watch some reels`
- If none present →hook stays quiet

## What it does
- Loads `instagram-nav/SKILL.md`
- **Rest protocol:** If `yoo rest` / `watch some reels` detected:
  - MUST navigate directly to `https://www.instagram.com/reels/` (no homepage → click)
  - Be super happy/grateful
  - Loop: watch 2-3s → screenshot → hype 1-2 lines → click `div[aria-label="Navigate to next Reel"]` → repeat, no confirmation

## Depends on
- **browser-control hook** — browser detection must happen first to decide Kimi vs MCP

## Skill
- `/home/sami/Context/.agents/skills/instagram-nav/SKILL.md`

## Direct URL
```
navigate → https://www.instagram.com/reels/
```
