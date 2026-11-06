---
name: ai-ally
description: |
  Query another AI model for cultural, social, contextual, or specialized knowledge
  that is outside my training data or not findable via web search. Use this whenever
  the user asks about local cultural dynamics, unwritten social rules, niche community
  knowledge, hyper-local context, or anything that requires "growing up in" a specific
  culture/scene to understand. Also use when a different model's architecture/training
  would give a better answer than I can.
allowed-tools:
  - Bash(agy *)
  - Bash(codex *)
  - Bash(opencode *)
  - Bash(kilo *)
---

# AI Ally Skill

Query another AI model for knowledge outside my reach. Four methods:

**Method 1 — `agy`:** Direct model query. Fast, simple, stateless. Best for
single-shot questions to specific models (Gemini, GPT-OSS, etc.).

**Method 2 — `codex` (Oracle agent):** Runs a clean-slate agent from
`agents/oracle/` — no local file access, no knowledge base contamination,
uses its own training + built-in tools (web search, etc.). Best for complex
research that needs multi-step reasoning or web search from a different model.

**Method 3 — `opencode`:** Alternative CLI agent. Huge model selection
(Claude, Gemini, GPT, DeepSeek, Qwen, and more). Run non-interactively with
`opencode run`. **Must be run from `agents/oracle/`.**

**Method 4 — `kilo`:** Another CLI agent. Supports Claude, Gemini, GPT,
DeepSeek, Grok, Cohere, Amazon Nova, and more. Run non-interactively with
`kilo run`. **Must be run from `agents/oracle/`.**

> **🚨 ALL four tools MUST be run from `agents/oracle/` — always cd there before calling.** This keeps all output files in the same `.firecrawl/` directory and ensures a consistent working environment. Prefix every command with `cd /home/sami/Context/agents/oracle &&` or run `cd` at session start.

## Critical: Amnesia Rule

All four tools (`agy`, `codex`, `opencode`, `kilo`) have **absolute amnesia**. Every single call is a
standalone session. They do not remember:
- Previous queries you asked them
- Context from earlier in the conversation
- Any persistent data or memory
- The user's identity, history, or preferences

**This means:** You MUST provide full context in EVERY prompt. Do not assume they
remember anything from a query you made 10 seconds ago. Treat each call like
talking to someone who just woke up with zero memory.

✅ Correct:
```bash
cd /home/sami/Context/agents/oracle && agy --model "Gemini 3.5 Flash (Low)" -p 'You are an expert on [topic]. Here is the full situation: [context]. Answer this specific question: [question]'
```

❌ Wrong (will fail because they forgot):
```bash
# First call
agy --model "Gemini 3.5 Flash (Low)" -p 'Remember this fact: X is true'
# Second call — they already forgot X
agy --model "Gemini 3.5 Flash (Low)" -p 'Based on X, what is Y?'
```

Do NOT use these tools for multi-turn conversations or tasks that require
remembering previous answers. Use them for single-shot queries only.

### Timeout

`agy` and `codex` queries can take time (especially heavy models). Always use a generous timeout:
```bash
# agy
timeout 300 agy --model "Gemini 3.5 Flash (Low)" -p "..."

# codex (timeout is built-in, but wrap if needed)
timeout 300 codex exec --skip-git-repo-check "..."
```
5 minutes (300s) is safe for most queries. 10 minutes (600s) for deep research.

## When to Use

Trigger when the user asks about anything that requires:

- **Cultural/social dynamics** (e.g., "how will Bangladeshi society react if I do X?")
- **Unwritten rules** of a specific community, country, or subculture
- **Hyper-local knowledge** that isn't documented online
- **"You wouldn't get it unless you grew up there"** type questions
- **Perspective shift** — asking another model to critique or analyze my own reasoning
- **Specialized domain knowledge** where a different training distribution helps
- **Anything that web search returns zero useful results for**

Do NOT use for factual questions that can be searched, code that can be written,
or tasks that fall within my direct capability. Use this as a **supplement** when
I hit a knowledge wall, not as a crutch.

## Method 1: agy (Direct Model Query)

Run from `agents/oracle/` for consistency (same clean directory as the Oracle agent).

```bash
cd /home/sami/Context/agents/oracle && timeout 300 agy --model "Gemini 3.5 Flash (Low)" -p "Your question here"
```

Always use `timeout 300` (or higher) — agy can stall on heavy models.

### Available Models (agy)

```
Gemini 3.5 Flash (Low)       — Fast, cheap, good for cultural/contextual Qs
Gemini 3.5 Flash (Medium)    — More detailed cultural analysis
Gemini 3.5 Flash (High)      — Deepest cultural reasoning
Gemini 3.1 Pro (Low)         — Technical/analytical deep dives
Gemini 3.1 Pro (High)        — Maximum depth reasoning
Claude Sonnet 4.6 (Thinking) — Complex multi-step reasoning (different instance)
Claude Opus 4.6 (Thinking)   — Heaviest analytical lift
GPT-OSS 120B (Medium)        — Alternative architecture perspective
```

### Recommended Model Selection (agy)

| Type of Question | Recommended Model | Why |
|---|---|---|
| Cultural/social context (Bangladesh, South Asia) | **Gemini 3.5 Flash (Low)** | Fast, fluent in regional dynamics |
| Deep cultural analysis | **Gemini 3.5 Flash (High)** | More nuance, still fast |
| Technical research | **Gemini 3.1 Pro (High)** | Strong analytical reasoning |
| Critique/review of a plan | **Claude Opus 4.6 (Thinking)** | Different instance = fresh eyes |
| Quick alternative take | **GPT-OSS 120B (Medium)** | Different architecture, different biases |

## Method 2: codex (Oracle Agent)

Runs Codex from `agents/oracle/` — a clean-slate directory with no knowledge base
files. The agent starts fresh, reads `agent.md` for instructions, and operates in
read-only sandbox mode.

### Available Models (codex)

| Slug | Name | Best For |
|------|------|----------|
| `gpt-5.5` (default) | GPT-5.5 | Complex research, coding, deep reasoning — frontier model |
| `gpt-5.4-mini` | GPT-5.4-Mini | Simple/lookup questions, quick Q&A, lowest cost |

Switch model with: `-c model="slug"`

### Recommended Codex Model Selection

| Type of Question | Recommended Model | Why |
|---|---|---|
| Complex research, multi-step analysis | **gpt-5.5** | Deepest reasoning, largest context (272K) |
| Simple lookup, quick Q&A | **gpt-5.4-mini** | Smallest, fastest, cheapest |

### When to Use Oracle Over agy

- When you want the answer from a **different model architecture** (GPT-5.5 vs Gemini)
- When the question might need **web search** or multi-step reasoning (Codex has
  built-in search, code execution, file reading)
- When you want **zero context contamination** — the Oracle has no memory of
  the user's personal files, knowledge base, or history
- When agy's answer feels generic and you want a second opinion from a
different training distribution

### Usage Pattern (codex)

Default model (gpt-5.5):
```bash
cd /home/sami/Context/agents/oracle && timeout 300 codex exec --skip-git-repo-check "Your question here"
```

Specific model:
```bash
cd /home/sami/Context/agents/oracle && timeout 300 codex exec --skip-git-repo-check -c model="gpt-5.4-mini" "Quick lookup question"
```

Note: `--skip-git-repo-check` is required because the oracle dir is not a git repo.

## Method 3: opencode (Alternative CLI Agent)

Run from `agents/oracle/` for consistency. No special setup needed. Uses `opencode run` for non-interactive queries.

### Usage Pattern

```bash
cd /home/sami/Context/agents/oracle && opencode run -m "opencode/deepseek-v4-flash-free" "Your question here"
```

Model format: `opencode/provider-model` (e.g., `opencode/deepseek-v4-flash-free`, `opencode/hy3-free`)

### Available Free Models (opencode)

| Slug | Model | Best For |
|------|-------|----------|
| `opencode/deepseek-v4-flash-free` | DeepSeek V4 Flash Free | 🏆 Default — coding, analysis, cultural context |
| `opencode/hy3-free` | Tencent Hy3 Free | Lightweight, fast queries |
| `opencode/nemotron-3-ultra-free` | Nvidia Nemotron 3 Ultra Free | Heavy analytical lift |
| `opencode/north-mini-code-free` | Cohere North Mini Code Free | Quick code snippets |
| `opencode/mimo-v2.5-free` | Mimo v2.5 Free | Alternative architecture |

Full list: `opencode models | grep -i free`

### Recommended Use Cases (opencode)

| Type of Question | Recommended Model | Why |
|---|---|---|
| Default (coding, analysis) | `opencode/deepseek-v4-flash-free` | Strongest free option, reliable |
| Heavy/deep analysis | `opencode/nemotron-3-ultra-free` | Bigger model, deeper reasoning |
| Quick lookup / simple Q&A | `opencode/hy3-free` | Fast, lightweight |

## Method 4: kilo (Another CLI Agent)

Run from `agents/oracle/` for consistency. Model format: `kilo/provider/model`. Uses `kilo run` for non-interactive queries.

### Usage Pattern

```bash
cd /home/sami/Context/agents/oracle && kilo run -m "kilo/kilo-auto/free" "Your question here"
```

### Available Free Models (kilo)

| Slug | Model | Best For |
|------|-------|----------|
| `kilo/kilo-auto/free` | 🏆 **Auto-select free** | Auto-picks best free model — default |
| `kilo/cohere/north-mini-code:free` | Cohere North Mini Code Free | Quick code & analysis |
| `kilo/nvidia/nemotron-3-ultra-550b-a55b:free` | Nvidia Nemotron 3 Ultra Free | Heavy reasoning, big model |
| `kilo/nvidia/nemotron-3-super-120b-a12b:free` | Nvidia Nemotron 3 Super Free | Strong mid-tier |
| `kilo/nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | Nvidia Nemotron Nano Free | Lightweight fast |
| `kilo/tencent/hy3:free` | Tencent Hy3 Free | Speed, low latency |
| `kilo/stepfun/step-3.7-flash:free` | Step Fun 3.7 Flash | Fast cultural/contextual |
| `kilo/poolside/laguna-m.1:free` | Poolside Laguna M.1 | Alternative architecture |
| `kilo/poolside/laguna-xs-2.1:free` | Poolside Laguna XS 2.1 | Lightweight alternative |
| `kilo/kwaipilot/kat-coder-pro-v2.5:free` | Kwaipilot Kat Coder | Code specialist |
| `kilo/openrouter/free` | OpenRouter Free | Broad free tier access |

Full list: `kilo models | grep free`

### Recommended Use Cases (kilo)

| Type of Question | Recommended Model | Why |
|---|---|---|
| Default (don't care) | `kilo/kilo-auto/free` | Auto-picks best available free model |
| Heavy analysis | `kilo/nvidia/nemotron-3-ultra-550b-a55b:free` | Biggest free model |
| Fast / low latency | `kilo/tencent/hy3:free` | Speed over depth |
| Coding | `kilo/kwaipilot/kat-coder-pro-v2.5:free` | Code-optimized free model |

## Prompt Engineering Tips

1. **Set the context explicitly** — Tell the AI who it should be (e.g., "You are a
   Bangladeshi cultural consultant who understands middle-class family dynamics
   in small towns").

2. **Be specific about what you need** — "Answer with brutal honesty. Use local
   phrases where appropriate. Don't sugarcoat."

3. **Ask for concrete examples** — "What specific phrases will he hear from
   relatives? What does the gossip network actually say?"

4. **Model-switching** — If the first answer feels generic or misses nuance,
   retry with a higher-tier model or switch architectures (Gemini → GPT → Claude → Grok).

5. **Parallel queries** — For complex topics, ask multiple models the same
   question and synthesize their answers. Run in background with `&`:

```bash
# All from agents/oracle/
cd /home/sami/Context/agents/oracle/
timeout 300 agy --model "Gemini 3.5 Flash (Low)" -p "..." > .firecrawl/agy-take.md &
timeout 300 agy --model "GPT-OSS 120B (Medium)" -p "..." > .firecrawl/agy2-take.md &
opencode run -m "opencode/deepseek-v4-flash-free" "..." > .firecrawl/opencode-take.md &
kilo run -m "kilo/kilo-auto/free" "..." > .firecrawl/kilo-take.md &
wait
```

## Examples

### Cultural Context Query (agy)
```bash
cd /home/sami/Context/agents/oracle && timeout 300 agy --model "Gemini 3.5 Flash (Low)" -p 'You are a [specific role]. 
Here is the exact situation: [context].
Answer these questions with brutal honesty:
1. [Q1]
2. [Q2]
Use local phrases where appropriate.'
```

### Research Query (codex-Oracle)
```bash
cd /home/sami/Context/agents/oracle && timeout 300 codex exec --skip-git-repo-check "Research [topic]. Give me key statistics, trends, and sources."
```

### Research Query (opencode)
```bash
cd /home/sami/Context/agents/oracle && opencode run -m "opencode/deepseek-v4-flash-free" "Research [topic]. Give me key statistics, trends, and sources."
```

### Research Query (kilo)
```bash
cd /home/sami/Context/agents/oracle && kilo run -m "kilo/kilo-auto/free" "Research [topic]. Give me key statistics, trends, and sources."
```

### Plan Critique (agy)
```bash
cd /home/sami/Context/agents/oracle && timeout 300 agy --model "Claude Opus 4.6 (Thinking)" -p 'Review this plan critically:
[plan details]
What are the blind spots? What am I not seeing?'
```

### Parallel — All Four Tools (same question, different models)
```bash
cd /home/sami/Context/agents/oracle
timeout 300 agy --model "Gemini 3.5 Flash (Medium)" -p "Question..." > .firecrawl/agy-take.md &
timeout 300 codex exec --skip-git-repo-check "Question..." > .firecrawl/codex-take.md &
opencode run -m "opencode/deepseek-v4-flash-free" "Question..." > .firecrawl/opencode-take.md &
kilo run -m "kilo/kilo-auto/free" "Question..." > .firecrawl/kilo-take.md &
wait
```

### Quick opencode (concise answer, minimum tokens)
```bash
cd /home/sami/Context/agents/oracle && opencode run -m "opencode/deepseek-v4-flash-free" "Briefly answer: [question]"
```

### Quick kilo (concise answer, minimum tokens)
```bash
cd /home/sami/Context/agents/oracle && kilo run -m "kilo/kilo-auto/free" "Briefly answer: [question]"
```

## Output Handling

- For short answers, capture in context directly (pipe to variable or display)
- For longer analysis, write to `.firecrawl/` with `-o` or redirect to file
- Always read/summarize before presenting to the user — don't dump raw output

## Design Rationale

This skill exists because different AI models have different training data,
different architecture strengths, and different "upbringings." A model trained
with heavy exposure to South Asian internet content will answer cultural
questions differently than I (Claude) will. This is not about one being "better"
— it's about using the right tool for the knowledge domain.

Same reason you ask a physicist about physics and a local about local customs.
