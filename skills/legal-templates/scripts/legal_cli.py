#!/usr/bin/env python3
"""
Legal Templates CLI - Universal Terminal Tool for Legal Documents
Attorney-drafted CC0 1.0 templates for startups, SaaS, and technology companies.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Base repository directory: check env var, then default to ~/.agents/skills/legal-templates
DEFAULT_REPO_DIR = Path(os.path.expanduser("~/.agents/skills/legal-templates"))
REPO_DIR = Path(os.environ.get("LEGAL_TEMPLATES_DIR", str(DEFAULT_REPO_DIR)))

TEMPLATE_METADATA = {
    "advisor-agreement": {
        "title": "Advisor Agreement",
        "category": "Agreements & Governance",
        "docx_stem": "advisor-agreement",
        "description": "Advisor agreement covering advisory services, equity compensation, IP assignment, and confidentiality.",
    },
    "business-associate-agreement": {
        "title": "Business Associate Agreement (BAA)",
        "category": "Privacy, Security & Compliance",
        "docx_stem": "business-associate-agreement-baa",
        "description": "HIPAA-required contract between covered entities and business associates handling protected health information.",
    },
    "cookie-notice": {
        "title": "Cookie Notice",
        "category": "Website & Platform Legal",
        "docx_stem": "cookie-notice",
        "description": "Disclosure of cookie and tracking technology practices for websites and apps.",
    },
    "dpa-us": {
        "title": "Data Processing Addendum (U.S.)",
        "category": "Privacy, Security & Compliance",
        "docx_stem": "data-processing-addendum-dpa",
        "description": "Processor-friendly DPA for U.S. personal data with security measures and state privacy law compliance (CCPA/CPRA).",
    },
    "dpa-global": {
        "title": "Data Processing Addendum (Global)",
        "category": "Privacy, Security & Compliance",
        "docx_stem": "data-processing-addendum-dpa-u-s-and-european-personal-data",
        "description": "Processor-friendly DPA for US, EU/EEA, UK, and Switzerland with GDPR Article 28 and EU SCCs.",
    },
    "employee-offer-letter": {
        "title": "Employee Offer Letter (California Exempt)",
        "category": "Employment & HR",
        "docx_stem": "employee-offer-letter",
        "description": "Offer letter for California exempt hires covering compensation, flexible vacation, IP assignment, and arbitration.",
    },
    "master-services-agreement": {
        "title": "Master Services Agreement (MSA)",
        "category": "Agreements & Governance",
        "docx_stem": "master-services-agreement-msa",
        "description": "Tech-oriented MSA for companies deploying SaaS software, AI platforms, or technical professional services.",
    },
    "mutual-nda": {
        "title": "Mutual Non-Disclosure Agreement",
        "category": "Agreements & Governance",
        "docx_stem": "mutual-non-disclosure-agreement-nda",
        "description": "Two-way confidentiality agreement for parties sharing sensitive information while evaluating a business relationship.",
    },
    "one-way-nda": {
        "title": "One-Way Non-Disclosure Agreement",
        "category": "Agreements & Governance",
        "docx_stem": "one-way-non-disclosure-agreement-nda",
        "description": "One-way confidentiality agreement protecting a single disclosing party's proprietary information.",
    },
    "privacy-policy-us": {
        "title": "Privacy Policy (U.S. Only)",
        "category": "Website & Platform Legal",
        "docx_stem": "privacy-policy-u-s-only",
        "description": "Privacy policy covering U.S. federal and state privacy laws including CCPA/CPRA.",
    },
    "privacy-policy-gdpr": {
        "title": "Privacy Policy (GDPR Enhanced)",
        "category": "Website & Platform Legal",
        "docx_stem": "privacy-policy-gdpr-enhanced",
        "description": "Multi-jurisdictional privacy policy covering both U.S. state laws and EU/UK GDPR and Swiss FADP.",
    },
    "terms-of-use": {
        "title": "Terms of Use",
        "category": "Website & Platform Legal",
        "docx_stem": "terms-of-use",
        "description": "Website terms of use covering access rights, IP protections, liability limits, and dispute resolution.",
    },
}

ALIAS_MAP = {
    "nda": "mutual-nda",
    "mnda": "mutual-nda",
    "mutual": "mutual-nda",
    "1way-nda": "one-way-nda",
    "one-way": "one-way-nda",
    "msa": "master-services-agreement",
    "baa": "business-associate-agreement",
    "offer-letter": "employee-offer-letter",
    "offer": "employee-offer-letter",
    "advisor": "advisor-agreement",
    "terms": "terms-of-use",
    "tou": "terms-of-use",
    "cookie": "cookie-notice",
    "cookies": "cookie-notice",
    "privacy": "privacy-policy-us",
    "privacy-us": "privacy-policy-us",
    "privacy-gdpr": "privacy-policy-gdpr",
    "gdpr": "privacy-policy-gdpr",
    "dpa": "dpa-us",
}


def resolve_slug(query: str) -> str:
    """Resolve a user slug or alias to an canonical template slug."""
    clean = query.strip().lower()
    if clean in TEMPLATE_METADATA:
        return clean
    if clean in ALIAS_MAP:
        return ALIAS_MAP[clean]
    # Check partial match
    matches = [k for k in TEMPLATE_METADATA if clean in k]
    if len(matches) == 1:
        return matches[0]
    return clean


def get_template_path(slug: str) -> Path:
    return REPO_DIR / "templates" / slug / "template.md"


def get_readme_path(slug: str) -> Path:
    return REPO_DIR / "templates" / slug / "README.md"


def get_docx_path(slug: str) -> Path:
    meta = TEMPLATE_METADATA.get(slug, {})
    stem = meta.get("docx_stem", slug)
    return REPO_DIR / "docx-originals" / f"{stem}.docx"


# --- Subcommand handlers ---


def cmd_list(args):
    """List available templates."""
    if args.json:
        data = []
        for slug, meta in TEMPLATE_METADATA.items():
            t_path = get_template_path(slug)
            d_path = get_docx_path(slug)
            data.append({
                "slug": slug,
                "title": meta["title"],
                "category": meta["category"],
                "description": meta["description"],
                "template_md_exists": t_path.exists(),
                "docx_exists": d_path.exists(),
            })
        print(json.dumps(data, indent=2))
        return 0

    print(f"\n\033[1;36m🏛️  General Legal Templates Library (CC0 1.0 Universal)\033[0m")
    print(f"\033[90mRepository: {REPO_DIR}\033[0m\n")

    current_cat = None
    for slug, meta in TEMPLATE_METADATA.items():
        if meta["category"] != current_cat:
            current_cat = meta["category"]
            print(f"\033[1;33m[{current_cat.upper()}]\033[0m")

        t_exists = "✓" if get_template_path(slug).exists() else "✗"
        d_exists = "✓" if get_docx_path(slug).exists() else "✗"
        formats = f"md:{t_exists} docx:{d_exists}"

        print(f"  \033[1m{slug:<28}\033[0m \033[32m{meta['title']}\033[0m")
        print(f"    \033[90m{meta['description']}\033[0m")
        print(f"    \033[34mFormats: {formats}\033[0m\n")

    print("\033[90mUse 'legal show <slug>' to read, 'legal info <slug>' for overview, or 'legal copy <slug>' to export.\033[0m\n")
    return 0


def cmd_show(args):
    """Output template markdown to stdout."""
    slug = resolve_slug(args.slug)
    t_path = get_template_path(slug)
    if not t_path.exists():
        print(f"Error: Template '{args.slug}' not found at {t_path}", file=sys.stderr)
        return 1

    content = t_path.read_text(encoding="utf-8")
    if args.no_mark:
        content = re.sub(r"</?mark>", "", content)

    if args.color and sys.stdout.isatty():
        # Highlight <mark> contents with bright yellow
        content = re.sub(r"<mark>(.*?)</mark>", r"\033[1;33;44m\1\033[0m", content)

    sys.stdout.write(content)
    if not content.endswith("\n"):
        sys.stdout.write("\n")
    return 0


def cmd_info(args):
    """Show detailed metadata and overview of a template."""
    slug = resolve_slug(args.slug)
    meta = TEMPLATE_METADATA.get(slug)
    if not meta:
        print(f"Error: Unknown template '{args.slug}'. Run 'legal list' for valid slugs.", file=sys.stderr)
        return 1

    readme_path = get_readme_path(slug)
    t_path = get_template_path(slug)
    d_path = get_docx_path(slug)

    print(f"\n\033[1;36m📋 Template: {meta['title']} ({slug})\033[0m")
    print(f"\033[1mCategory:\033[0m {meta['category']}")
    print(f"\033[1mDescription:\033[0m {meta['description']}")
    print(f"\033[1mMarkdown:\033[0m {t_path} ({'Exists' if t_path.exists() else 'Missing'})")
    print(f"\033[1mDOCX Source:\033[0m {d_path} ({'Exists' if d_path.exists() else 'Missing'})\n")

    if readme_path.exists():
        print("\033[1;32m=== OVERVIEW & KEY PROVISIONS ===\033[0m")
        print(readme_path.read_text(encoding="utf-8"))

    if t_path.exists():
        content = t_path.read_text(encoding="utf-8")
        marks = re.findall(r"<mark>(.*?)</mark>", content, re.DOTALL)
        clean_marks = [m.strip() for m in marks if m.strip()]
        print(f"\033[1;33mCustomizable Placeholders:\033[0m {len(clean_marks)} total (<mark> tags)")
        print(f"\033[90mRun 'legal placeholders {slug}' to inspect all placeholder fields.\033[0m\n")

    return 0


def cmd_placeholders(args):
    """Extract and list all customizable fields in a template."""
    slug = resolve_slug(args.slug)
    t_path = get_template_path(slug)
    if not t_path.exists():
        print(f"Error: Template '{args.slug}' not found.", file=sys.stderr)
        return 1

    content = t_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    results = []
    for line_idx, line in enumerate(lines, 1):
        for match in re.finditer(r"<mark>(.*?)</mark>", line):
            val = match.group(1).strip()
            if not val:
                continue
            # Context window
            start = max(0, match.start() - 30)
            end = min(len(line), match.end() + 30)
            context = line[start:end].strip()
            results.append({
                "line": line_idx,
                "field": val,
                "context": f"...{context}..." if start > 0 or end < len(line) else context,
            })

    if args.json:
        print(json.dumps({"template": slug, "count": len(results), "placeholders": results}, indent=2))
        return 0

    print(f"\n\033[1;36m📝 Customizable Placeholders for {slug} ({len(results)} found)\033[0m\n")
    for i, r in enumerate(results, 1):
        print(f"  \033[1;33m{i:2d}. Line {r['line']:4d}:\033[0m \033[1;37m{r['field']}\033[0m")
        print(f"      \033[90mContext: {r['context']}\033[0m")

    # Distinct placeholder suggestions
    distinct = sorted({r["field"] for r in results if not r["field"].startswith("_") and not r["field"] in ("[__]", "[_]")})
    if distinct:
        print(f"\n\033[1;32mKey Fields to Provide:\033[0m")
        for d in distinct:
            print(f"  • {d}")

    print()
    return 0


def cmd_search(args):
    """Search across all templates and documentation for a keyword or clause."""
    query = args.query.strip().lower()
    if not query:
        print("Error: Search query cannot be empty.", file=sys.stderr)
        return 1

    print(f"\n\033[1;36m🔍 Searching Legal Templates for: '{args.query}'\033[0m\n")
    matches = []

    for slug in TEMPLATE_METADATA:
        t_path = get_template_path(slug)
        if not t_path.exists():
            continue
        lines = t_path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, 1):
            if query in line.lower():
                matches.append({
                    "slug": slug,
                    "line": idx,
                    "text": line.strip(),
                })

    if not matches:
        print("No matching clauses found across the library.\n")
        return 0

    print(f"Found {len(matches)} match{'es' if len(matches) != 1 else ''}:\n")
    current_slug = None
    for m in matches:
        if m["slug"] != current_slug:
            current_slug = m["slug"]
            title = TEMPLATE_METADATA[current_slug]["title"]
            print(f"\033[1;33m📄 {title} ({current_slug}):\033[0m")

        # Highlight match
        text = m["text"]
        highlighted = re.sub(f"({re.escape(args.query)})", r"\033[1;31;47m\1\033[0m", text, flags=re.IGNORECASE)
        if len(highlighted) > 200:
            highlighted = highlighted[:200] + "..."
        print(f"  \033[90mLine {m['line']:4d}:\033[0m {highlighted}")
        print()

    return 0


def cmd_copy(args):
    """Copy template markdown to a target destination."""
    slug = resolve_slug(args.slug)
    t_path = get_template_path(slug)
    if not t_path.exists():
        print(f"Error: Template '{args.slug}' not found.", file=sys.stderr)
        return 1

    dest = Path(args.dest) if args.dest else Path(f"./{slug}.md")
    if dest.is_dir():
        dest = dest / f"{slug}.md"

    dest.parent.mkdir(parents=True, exist_ok=True)
    content = t_path.read_text(encoding="utf-8")
    if args.no_mark:
        content = re.sub(r"</?mark>", "", content)

    dest.write_text(content, encoding="utf-8")
    print(f"✓ Copied {slug} template to: {dest} ({len(content):,} bytes)")
    return 0


def cmd_docx(args):
    """Copy original .docx template to a target destination."""
    slug = resolve_slug(args.slug)
    d_path = get_docx_path(slug)
    if not d_path.exists():
        print(f"Error: Original .docx for '{args.slug}' not found at {d_path}.", file=sys.stderr)
        return 1

    dest = Path(args.dest) if args.dest else Path(f"./{slug}.docx")
    if dest.is_dir():
        dest = dest / f"{slug}.docx"

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(d_path, dest)
    print(f"✓ Copied original DOCX to: {dest} ({dest.stat().st_size:,} bytes)")
    return 0


def cmd_fill(args):
    """Fill placeholder variables in a template."""
    slug = resolve_slug(args.slug)
    t_path = get_template_path(slug)
    if not t_path.exists():
        print(f"Error: Template '{args.slug}' not found.", file=sys.stderr)
        return 1

    content = t_path.read_text(encoding="utf-8")

    # Parse --var KEY=VALUE arguments
    substitutions = {}
    for item in args.vars or []:
        if "=" in item:
            k, v = item.split("=", 1)
            substitutions[k.strip()] = v.strip()

    # Apply substitutions
    # Also remove marks around replaced values
    for k, v in substitutions.items():
        # Match <mark>[k]</mark> or <mark>k</mark> or [k]
        pattern = rf"(<mark>\s*\[?{re.escape(k)}\]?\s*</mark>|\[{re.escape(k)}\])"
        content = re.sub(pattern, v, content, flags=re.IGNORECASE)

    if args.strip_remaining_marks:
        content = re.sub(r"</?mark>", "", content)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(content, encoding="utf-8")
        print(f"✓ Filled template written to: {out_path}")
    else:
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")

    return 0


def cmd_doctor(args):
    """Verify health and integrity of legal templates installation."""
    print(f"\n\033[1;36m🏥 Legal Templates Doctor\033[0m")
    print(f"Checking environment at: {REPO_DIR}\n")

    all_ok = True

    # 1. Check REPO_DIR
    if REPO_DIR.exists():
        print(f"  \033[32m✓\033[0m Repository directory found ({REPO_DIR})")
    else:
        print(f"  \033[31m✗\033[0m Repository directory missing ({REPO_DIR})")
        all_ok = False

    # 2. Check templates count
    md_count = sum(1 for s in TEMPLATE_METADATA if get_template_path(s).exists())
    readme_count = sum(1 for s in TEMPLATE_METADATA if get_readme_path(s).exists())
    expected = len(TEMPLATE_METADATA)

    if md_count == expected:
        print(f"  \033[32m✓\033[0m All {expected}/{expected} template.md files verified")
    else:
        print(f"  \033[31m✗\033[0m Only {md_count}/{expected} template.md files found")
        all_ok = False

    if readme_count == expected:
        print(f"  \033[32m✓\033[0m All {expected}/{expected} template README.md guides verified")
    else:
        print(f"  \033[33m!\033[0m {readme_count}/{expected} template README.md guides found")

    # 3. Check docx originals
    docx_count = sum(1 for s in TEMPLATE_METADATA if get_docx_path(s).exists())
    if docx_count == expected:
        print(f"  \033[32m✓\033[0m All {expected}/{expected} original .docx files verified")
    else:
        print(f"  \033[31m✗\033[0m Only {docx_count}/{expected} .docx originals found")
        all_ok = False

    # 4. Check Python 3 and uv availability
    uv_path = shutil.which("uv")
    if uv_path:
        print(f"  \033[32m✓\033[0m uv found: {uv_path}")
    else:
        print(f"  \033[33m!\033[0m uv not found in PATH")

    # 5. Check SKILL.md
    skill_file = REPO_DIR / "SKILL.md"
    if skill_file.exists():
        print(f"  \033[32m✓\033[0m SKILL.md found ({skill_file})")
    else:
        print(f"  \033[31m✗\033[0m SKILL.md missing ({skill_file})")
        all_ok = False

    print()
    if all_ok:
        print("\033[1;32m🎉 All checks passed! Legal Templates is fully operational.\033[0m\n")
        return 0
    else:
        print("\033[1;31m⚠️  Some checks failed. Please inspect logs above.\033[0m\n")
        return 1


def cmd_convert(args):
    """Run python-docx converter script using uv."""
    script_path = REPO_DIR / "scripts" / "convert_docx.py"
    if not script_path.exists():
        print(f"Error: Conversion script not found at {script_path}", file=sys.stderr)
        return 1

    print(f"Running conversion via uv run --with python-docx...")
    cmd = ["uv", "run", "--with", "python-docx", "python3", str(script_path)]
    return subprocess.run(cmd, cwd=str(REPO_DIR)).returncode


def cmd_fetch(args):
    """Fetch/refresh docx originals from upstream general.legal."""
    script_path = REPO_DIR / "scripts" / "fetch_templates.py"
    if not script_path.exists():
        print(f"Error: Fetch script not found at {script_path}", file=sys.stderr)
        return 1

    print(f"Fetching latest templates from https://general.legal/resources/library...")
    return subprocess.run([sys.executable, str(script_path)], cwd=str(REPO_DIR)).returncode


def main():
    parser = argparse.ArgumentParser(
        prog="legal",
        description="Legal Templates CLI - Attorney-drafted CC0 legal documents for tech startups and companies.",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # list
    p_list = subparsers.add_parser("list", aliases=["ls"], help="List all available legal templates")
    p_list.add_argument("--json", action="store_true", help="Output template list as JSON")
    p_list.set_defaults(func=cmd_list)

    # show
    p_show = subparsers.add_parser("show", aliases=["cat"], help="Print template markdown to stdout")
    p_show.add_argument("slug", help="Template slug or alias (e.g. mutual-nda, msa, terms)")
    p_show.add_argument("--no-mark", action="store_true", help="Strip <mark> tags from output")
    p_show.add_argument("--color", action="store_true", default=True, help="Colorize highlight tags in terminal")
    p_show.set_defaults(func=cmd_show)

    # info
    p_info = subparsers.add_parser("info", help="Show overview, when to use, and key provisions")
    p_info.add_argument("slug", help="Template slug or alias")
    p_info.set_defaults(func=cmd_info)

    # placeholders
    p_fields = subparsers.add_parser("placeholders", aliases=["fields"], help="Inspect customizable fields and placeholders")
    p_fields.add_argument("slug", help="Template slug or alias")
    p_fields.add_argument("--json", action="store_true", help="Output placeholders as JSON")
    p_fields.set_defaults(func=cmd_placeholders)

    # search
    p_search = subparsers.add_parser("search", aliases=["find"], help="Search across all templates for terms/clauses")
    p_search.add_argument("query", help="Keyword or search phrase")
    p_search.set_defaults(func=cmd_search)

    # copy
    p_copy = subparsers.add_parser("copy", aliases=["cp"], help="Copy template markdown to target file or directory")
    p_copy.add_argument("slug", help="Template slug or alias")
    p_copy.add_argument("dest", nargs="?", default="", help="Destination path (defaults to ./<slug>.md)")
    p_copy.add_argument("--no-mark", action="store_true", help="Strip <mark> tags when copying")
    p_copy.set_defaults(func=cmd_copy)

    # docx
    p_docx = subparsers.add_parser("docx", help="Copy original .docx template to target file or directory")
    p_docx.add_argument("slug", help="Template slug or alias")
    p_docx.add_argument("dest", nargs="?", default="", help="Destination path (defaults to ./<slug>.docx)")
    p_docx.set_defaults(func=cmd_docx)

    # fill
    p_fill = subparsers.add_parser("fill", help="Substitute placeholder variables in template")
    p_fill.add_argument("slug", help="Template slug or alias")
    p_fill.add_argument("--var", "-v", action="append", dest="vars", help="Set variable e.g. --var Company='Acme Inc'")
    p_fill.add_argument("--out", "-o", help="Output path (defaults to stdout)")
    p_fill.add_argument("--strip-remaining-marks", action="store_true", help="Strip any unfilled <mark> tags")
    p_fill.set_defaults(func=cmd_fill)

    # doctor
    p_doc = subparsers.add_parser("doctor", help="Check installation health and file integrity")
    p_doc.set_defaults(func=cmd_doctor)

    # convert
    p_conv = subparsers.add_parser("convert", help="Re-convert docx files to markdown via python-docx")
    p_conv.set_defaults(func=cmd_convert)

    # fetch
    p_fetch = subparsers.add_parser("fetch", help="Fetch/refresh docx originals from upstream general.legal")
    p_fetch.set_defaults(func=cmd_fetch)

    args = parser.parse_args()
    if not args.subcommand:
        parser.print_help()
        return 0

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
