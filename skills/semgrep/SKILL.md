---
name: semgrep
description: "Fast, polyglot static analysis, AST code search, and security vulnerability auditing tool. Use to scan codebases for security flaws (OWASP, SQL injection, secrets, XSS), enforce architectural invariants, or run semantic pattern searches ($X == $X)."
---

# Semgrep — AST Static Analysis & Security Engine

Semgrep is a high-speed, polyglot semantic analysis engine. Unlike regex or text-based search tools (`grep`, `ripgrep`), Semgrep parses source code into an Abstract Syntax Tree (AST), allowing AI agents to match code patterns based on syntactic structure, variable equivalence, and expression depth regardless of whitespace, formatting, or variable names.

The `semgrep` binary is globally installed at `~/.local/bin/semgrep`.

---

## ⚡ Global CLI Quick Reference

| Task | Command |
| :--- | :--- |
| **Auto-detect & scan codebase** | `semgrep scan --config auto` |
| **Audit for Security Vulnerabilities** | `semgrep scan --config "p/security-audit"` |
| **Scan for OWASP Top 10** | `semgrep scan --config "p/owasp-top-ten"` |
| **Scan for Leaked Secrets & Keys** | `semgrep scan --config "p/secrets"` |
| **Scan for CWE Top 25 Flaws** | `semgrep scan --config "p/cwe-top-25"` |
| **Target specific paths or files** | `semgrep scan --config auto src/` |
| **Ad-hoc AST Pattern Search** | `semgrep scan --pattern '<pattern>' --lang <lang> [path]` |
| **Output findings as structured JSON** | `semgrep scan --config auto --json` |
| **CI / Git Diff Mode** | `semgrep ci` |
| **Start Semgrep MCP Server** | `semgrep mcp` |

---

## 🧠 Semantic Pattern Syntax Guide

AI agents can construct powerful queries using Semgrep's pattern primitives:

### 1. Metavariables (`$X`, `$USER`, `$REQ`)
Matches any single expression, identifier, or AST node. If the same metavariable is repeated, Semgrep enforces value equality across instances.

```bash
# Finds tautological checks (e.g. if x == x or if a.b == a.b):
semgrep scan --pattern '$X == $X' --lang python .

# Finds insecure password hashing with low iterations or empty salts:
semgrep scan --pattern 'crypto.pbkdf2Sync($PASS, "", ...)' --lang js .
```

### 2. The Ellipsis Operator (`...`)
Matches zero or more arguments, parameters, statements, or characters:

```bash
# Matches any function call to exec, regardless of how many arguments:
semgrep scan --pattern 'child_process.exec(...) ' --lang js .

# Matches any try block that catches Exception but ignores it:
semgrep scan --pattern 'try:
    ...
except Exception:
    pass' --lang python .

# Matches any fetch or axios call without credentials:
semgrep scan --pattern 'fetch($URL, { ... })' --lang ts .
```

### 3. Deep Expression Operator (`<... $X ...>`)
Matches an expression nested arbitrarily deep within another expression or statement:

```bash
# Finds any SQL query construction that concatenates user input:
semgrep scan --pattern 'db.query(<... $REQ.params ...>)' --lang js .
```

---

## 🛠️ Step-by-Step Agent Workflows

### Workflow 1: Pre-Deployment Security Audit
Before shipping or deploying any web application, API, or service:

```bash
# 1. Run automated scan with rule detection
semgrep scan --config auto

# 2. Check specifically for hardcoded API keys and secrets
semgrep scan --config "p/secrets"

# 3. If web app (Next.js, FastAPI, Express), check OWASP Top 10
semgrep scan --config "p/owasp-top-ten"
```

### Workflow 2: Automated Agent Code Review via JSON
To programmatically ingest vulnerabilities and report actionable line numbers:

```bash
semgrep scan --config "p/security-audit" --json > /tmp/audit.json
```
Inspect the `.results[]` array in the JSON output:
- `path`: File location
- `start.line`, `end.line`: Line numbers
- `extra.message`: Actionable explanation of the flaw
- `extra.severity`: `ERROR`, `WARNING`, or `INFO`

### Workflow 3: Instant Refactoring & Antipattern Auditing
When refactoring or enforcing architectural rules:

```bash
# Find all occurrences of dangerous raw HTML rendering in React:
semgrep scan --pattern 'dangerouslySetInnerHTML={{ __html: $X }}' --lang tsx src/

# Find all unhandled promises or floating async calls:
semgrep scan --pattern 'async function $F(...) { ... }' --lang ts src/

# Find Python subprocess calls without explicit shell=False:
semgrep scan --pattern 'subprocess.Popen($CMD, ..., shell=True, ...)' --lang python .
```

---

## 🌐 Supported Languages

Semgrep supports first-class parsing for:
- **Web & Backend**: JavaScript, TypeScript, TSX, Python, Go, Java, C#, Ruby, PHP
- **Systems**: Rust, C, C++, OCaml, Swift, Kotlin
- **Configuration & Infrastructure**: Dockerfile, Terraform, YAML, JSON, HTML

---

## 🔗 Verification & Health

To verify Semgrep operational health at any time:
```bash
semgrep --version
semgrep scan --help
```
