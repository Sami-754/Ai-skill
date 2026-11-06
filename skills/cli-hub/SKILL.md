---
name: cli-hub
description: >-
  Discover and install agent-native CLIs for professional software (Blender, GIMP, Inkscape, Godot, LibreOffice, Krita, OBS Studio, and 70+ others). Use cli-hub to browse, search, and manage CLI-Anything harnesses.
---

# CLI-Hub

CLI-Hub is a marketplace and package manager of agent-native command-line interfaces that make professional software accessible to AI agents.

The global executable **`cli-hub`** is pre-installed at `~/.local/bin/cli-hub` (on `$PATH`).

## Quick Start

```bash
# Browse all available CLIs
cli-hub list

# Search by category or keyword
cli-hub search image
cli-hub search "3d modeling"

# Install a CLI harness (auto-links binary into ~/.local/bin/)
cli-hub install gimp

# Show details for a CLI
cli-hub info gimp

# Launch an installed CLI
cli-hub launch gimp
```

## Workflow Matrices

A single CLI is one tool. A **matrix** is a whole workflow packaged as
capabilities × providers — e.g. `video-creation` maps intents like
`text.transcribe` or `visual.generate` to harness CLIs, public CLIs, Python
libraries, native binaries, and cloud APIs. Reach for a matrix when a task spans
several tools (produce a video, design an image, build a game).

Standard agent sequence — **preflight before you install**:

```bash
cli-hub matrix list                                   # browse all matrices
cli-hub can "transcribe audio"                        # find the capability across matrices
cli-hub matrix search "video subtitle"                # search; shows the matched capability
cli-hub matrix preflight video-creation --json        # what's usable here? (exit 3 = gaps)
cli-hub matrix preflight video-creation -c text.transcribe --fix-hints   # one capability + install hints
cli-hub matrix install video-creation --capability text.transcribe       # install ONLY what the task needs
# After install, the matrix SKILL.md renders locally with provider-selection rules — read it.
```

Scope every install — do not bulk-install a 14-CLI matrix for a one-capability
task. Use `--capability <id>`, `--recipe <id>`, or `--only a,b`, and
`--dry-run` to preview the plan with zero side effects. `--json` is available on
every matrix subcommand; exit codes are `0` ok · `3` partial/gaps · `1` failure ·
`2` usage error. Retry failures with `cli-hub matrix install <name> --resume`,
and audit an install with `cli-hub matrix doctor <name>`.


## Live Catalog

**URL**: [`https://reeceyang.sgp1.cdn.digitaloceanspaces.com/SKILL.md`](https://reeceyang.sgp1.cdn.digitaloceanspaces.com/SKILL.md)

The catalog is auto-updated and provides:
- Full list of available CLIs organized by category
- One-line `cli-hub install` commands for each tool
- Complete descriptions and usage patterns


## What Can You Do?

CLI-Hub covers a broad range of software and codebases, empowering agents to conduct complex workflows via CLI:

- **Creative workflows**: Image editing, 3D modeling, video production, audio processing, music notation
- **Productivity tools**: Office suites, knowledge management, live streaming
- **AI platforms**: Local LLMs, image generation, AI APIs, research assistants
- **Communication**: Video conferencing and collaboration
- **Development**: Diagramming, browser automation, network management
- **Content generation**: AI-powered document and media creation

Each CLI provides stateful operations, JSON output for agents, REPL mode, and integrates with real software backends.

## How It Works

`cli-hub` is a lightweight wrapper around `pip`. When you run `cli-hub install gimp`, it installs a separate Python package (`cli-anything-gimp`) with its own CLI entry point (`cli-anything-gimp`). Each CLI is an independent pip package — `cli-hub` simply resolves names from the registry and tracks installs.

## Preview Consumption

Some installed harnesses also support preview workflows. The command split is:

- `cli-anything-<software> preview ...` creates or updates real preview artifacts
- `cli-hub previews ...` inspects, renders, watches, or opens those existing artifacts

Use:

```bash
# From the harness side: publish preview state
cli-anything-blender --json --project scene.blend-cli.json preview capture --recipe quick

# From cli-hub: inspect or open the resulting bundle or live session
cli-hub previews inspect /path/to/bundle-or-session
cli-hub previews html /path/to/bundle-or-session -o page.html
cli-hub previews watch /path/to/session --open
cli-hub previews open /path/to/bundle-or-session
```

For live sessions, `cli-hub previews` reads:

- `session.json` for the current head
- `trajectory.json` for append-only history
- the current bundle manifest and artifacts

## How to Use

1. **CLI is pre-installed**: `cli-hub` is globally available on `$PATH` (`~/.local/bin/cli-hub`).
2. **Find your tool**: `cli-hub search <keyword>` or `cli-hub list -c <category>`
3. **Install**: `cli-hub install <name>` (installs and auto-links `cli-anything-<name>` to `~/.local/bin/`)
4. **Run**: `cli-anything-<name>` for REPL, or `cli-anything-<name> <command>` for one-shot
5. **JSON output**: All CLIs support `--json` flag for machine-readable output
6. **Preview-capable CLIs**: use `cli-anything-<name> preview ... --json` to publish,
   then `cli-hub previews ...` to inspect or open the result

## Example Workflow

```bash
# Find what you need
cli-hub search video

# Install it (auto-links to ~/.local/bin/cli-anything-kdenlive)
cli-hub install kdenlive

# Use it with JSON output
cli-anything-kdenlive --json project create --name my-project
```

## More Info

- Live Catalog: https://reeceyang.sgp1.cdn.digitaloceanspaces.com/SKILL.md
- Web Hub: https://clianything.cc
- Repository: https://github.com/HKUDS/CLI-Anything
