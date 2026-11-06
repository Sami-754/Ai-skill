# Hook: discord-nav (CONDITIONAL)

**Scope:** Project-local — ` /home/sami/Context/.agents/` (NOT universal)
**Plugin:** `.opencode/plugin/discord-hook.ts`
**Type:** Conditional — fires ONLY when task mentions Discord

## When it fires
- Keywords: `discord`, `server`, `channel`, `guild`
- Otherwise quiet

## What it does
- Loads `discord-nav/SKILL.md`
- Handles server/channel navigation, message reading, etc.
- Still uses browser-control for browser detection (Kimi vs MCP)

## Depends on
- **browser-control hook**

## Skill
- `/home/sami/Context/.agents/skills/discord-nav/SKILL.md`
