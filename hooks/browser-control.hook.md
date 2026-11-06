# Hook: browser-control (ALWAYS)

**Scope:** Project-local — ` /home/sami/Context/.agents/` (NOT universal `~/.config/opencode/`)
**Plugin:** `.opencode/plugin/browser-control-hook.ts`
**Type:** Universal hook — fires on ANY browser activity

## When it fires
- Any message containing: `browser`, `chrome`, `helium`, `brave`, `zen`, `firefox`, `navigate`, `click`, `snapshot`, `screenshot`, `evaluate`, `tab`, `page`, `url`, `open`, `kimi`, `cdp`, `marionette`, `instagram`, `discord`, `reels`
- Basically: if the task touches a browser at all, this hook runs

## What it does
1. Detects intent via keywords
2. Checks for Kimi triggers: `i'm on`, `im on`, `i opened`, `you can see my screen`, `check this page`, `use kimi`, `watch some reels`, `yoo rest`
   - If found → **Browser IS ON → use Kimi WebBridge (curl 127.0.0.1:10086) with newTab:true**
3. If no Kimi trigger but browser intent → assume YOU must launch via MCP (port 9223/2828)
4. If NOT SURE → probe all once:
   ```bash
   curl -s http://127.0.0.1:9223/json/version
   curl -s http://127.0.0.1:10086/command -d '{"action":"list_tabs"}'
   curl -s http://127.0.0.1:2829/json/version
   ```

## Depends on
- Nothing — this is the base hook. Instagram/Discord hooks depend on THIS.

## Skill
- `/home/sami/Context/.agents/skills/browser-control/SKILL.md`
