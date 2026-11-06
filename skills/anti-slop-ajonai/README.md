# Anti-Slop (AJONAI)

A universal skill and CLI for building web interfaces that don't read as machine-generated.

## Setup & CLI

The skill is installed in `~/.agents/skills/anti-slop-ajonai/` and provides a global executable `anti-slop` in `~/.local/bin/anti-slop` (on `$PATH`).

Any agent (Antigravity, Codex, Claude Code, Cursor) or human can invoke `anti-slop` directly.

## The checker

Runs on plain Node, no dependencies, no install step:

```bash
anti-slop src/
anti-slop src/ --json
anti-slop src/ --only=color,states
anti-slop src/ --strict     # advisories fail too
anti-slop --list-rules
```

Exit code 1 on any `error`, or on anything at all under `--strict`. Suitable for a pre-commit hook
or CI step.

Suppress a finding you've checked and accepted:

```jsx
{/* deliberate-ignore contrast-500-white */}
<div className="bg-indigo-500 text-white">…</div>
```

A suppression is a recorded decision, which is the entire point of the skill.

## What's here

```
SKILL.md                        the always-loaded core: the thesis and the process
references/
  00-decision-sheet.md          fill this before writing markup — highest-leverage file
  01-color.md                   palette construction, OKLCH ramps, contrast, dark mode
  02-type.md                    pairing, scale, tracking, leading, measure
  03-space-surface.md           spacing registers, elevation, radius, separators
  04-states.md                  the states nobody ships — read by default
  05-motion.md                  easing, duration, springs, interruptibility
  06-assets.md                  icons, imagery, charts, placeholder data
  07-audit.md                   reviewing existing UI, with calibration
  08-dated-defaults.md          the current monoculture — has a date, will go stale
scripts/check.mjs               35 static rules, dependency-free
```

## Why it's built this way

Most anti-slop rulesets are ban lists. Ban lists work once and then become the thing they were
meant to prevent — cream backgrounds, italic serif heroes, and tracked eyebrows were all
recommended escapes one generation ago and are detector rules now. Advice followed uniformly
produces uniformity.

So the core of this skill is a **process that derives choices from a specific brief**, and the
ban lists are quarantined in one file with a date on it.

Three things it does differently:

- **Interaction states are weighted above appearance.** When candidate tells were adversarially
  audited, motion and states had the highest survival rate and hero composition the lowest. A
  screenshot of a generated page is usually fine; the giveaway is that it's inert.
- **It reports co-occurrence, not items.** Under three independent judging lenses, fewer than 10%
  of candidate tells were unanimously high-signal. One rounded card proves nothing. Fourteen
  unchosen defaults together prove a lot.
- **It corrects known bugs in published rulesets.** No blanket typeface bans, no total em-dash ban
  (which prescribes typographically wrong marks to fool a classifier), the correct WCAG large-text
  threshold of 24px rather than the 18px several skills state, and no scoring of human tells —
  magic numbers, a double space, a stray inconsistency — as evidence of machine authorship.

## Source

Built from a multi-agent research project that mined four independent anti-slop rule corpora
(`pbakaus/impeccable`, `leonxlnx/taste-skill`, `emilkowalski/skill`, `h3nryprod01/design-taste`),
professional design systems (Material 3, IBM Carbon, Apple HIG via the WWDC design talks, Vercel's
Web Interface Guidelines), Tailwind and shadcn source, and the LLM mode-collapse literature — with
adversarial verification on every claim. 118 of 153 candidate visual defects did not survive audit;
13 of 25 research claims were refuted. What's here is what was left.
