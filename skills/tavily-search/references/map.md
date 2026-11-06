# Site Mapping with `tvly map`

`tvly map` discovers and lists URLs on a target domain without extracting page bodies. It is fast, lightweight, and uses minimal credits.

## When to Use `tvly map`
- You know the target domain (e.g. `docs.stripe.com`), but need to find the specific URL for an endpoint or guide.
- You want to inspect the site hierarchy before executing a bulk crawl.
- You need to generate a targeted URL list for selective extraction.

## CLI Patterns

### 1. Map Site Structure
```bash
tvly map https://docs.github.com --limit 30 --json
```

### 2. Guided Mapping with Intent
Steer the mapper using natural language `--instructions`:
```bash
tvly map https://nextjs.org/docs --instructions "Server Actions and App Router mutation patterns" --limit 15 --json
```

### 3. Filter Paths by Regular Expression
Restrict URL discovery to documentation subpaths only:
```bash
tvly map https://docs.fastapi.tiangolo.com --select-paths '^/tutorial/.*' --limit 20 --json
```

### 4. Two-Step Mapping & Extraction Pattern
1. Run `tvly map` to find exact URLs matching the topic:
   ```bash
   tvly map https://docs.modal.com --instructions "GPU scheduling and cold start optimization" --limit 10 --json
   ```
2. Pick the top 1–2 target URLs and extract full markdown:
   ```bash
   tvly extract <url1> <url2> --json
   ```
