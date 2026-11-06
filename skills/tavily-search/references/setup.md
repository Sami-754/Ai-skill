# Tavily CLI Setup & Authentication

Tavily is configured as a standalone command-line interface tool (`tvly`) available globally in the system `$PATH`. All AI agents interact with Tavily exclusively via shell commands (`Bash(tvly *)`).

## Verification
Check existing authentication status and version:
```bash
tvly --status
```
Example output:
```text
tavily v0.2.1
> Authenticated via OAuth (tvly login)
```

## First-Time Setup & Authentication

If `tvly` is not logged in:

### Method 1: Interactive Browser Login (OAuth)
```bash
tvly login
```

### Method 2: Headless API Key Login (Recommended for CI / Remote Agents)
```bash
tvly login --api-key tvly-YOUR_API_KEY
```

### Method 3: Environment Variable
You can export the API key in your shell profile:
```bash
export TAVILY_API_KEY="tvly-YOUR_API_KEY"
```

## CLI Installation (If installing on a new machine)
```bash
curl -fsSL https://cli.tavily.com/install.sh | bash
```

## Key Management & Status Commands
* `tvly auth`: Inspect authentication details and active account.
* `tvly logout`: Clear cached credentials.
* `tvly update`: Check for or install the latest CLI binary.
