# Bulk Web Crawling with `tvly crawl`

`tvly crawl` starts from an entry URL, recursively follows internal links, and extracts full markdown content from every visited page.

## When to Use `tvly crawl`
- You need to download entire documentation sections into local markdown files.
- You are building local reference indices or offline context for a complex API.
- You need archival or bulk content extraction across a specific path.

## CLI Patterns

### 1. Crawl to Local Markdown Files (`--output-dir`)
Saves every discovered page as an individual `.md` file inside the target directory:
```bash
tvly crawl https://docs.astral.sh/uv/concepts/ --select-paths '^/concepts/.*' --limit 15 --output-dir ./uv-concepts-docs
```

### 2. Guided Crawl with Instructions
Provide natural language guidance to prioritize specific content:
```bash
tvly crawl https://supabase.com/docs --instructions "Row Level Security and Postgres functions" --limit 10 -o ./supabase-rls.json
```

### 3. Depth & Breadth Limits
Always enforce bounds to prevent unintentional infinite loops on large sites:
```bash
tvly crawl https://example.com/blog --max-depth 2 --max-breadth 10 --limit 25 --json
```

### Best Practices for Agents
1. **Always Set `--limit`:** Default is 50. Explicitly set a limit (e.g. 10–25) to avoid excessive processing time and credits.
2. **Use `--select-paths`:** Restrict crawling to relevant subpaths (e.g. `^/docs/.*`) rather than crawling the home page or navigation footer links.
3. **Save to Disk:** Avoid dumping large crawl payloads directly into stdout. Use `--output-dir <path>` or `-o <file.json>`.
