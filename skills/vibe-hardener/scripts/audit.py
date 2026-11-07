#!/usr/bin/env python3
"""
vibe-hardener audit script
Comprehensive automated scanner for vibe-coded applications.
Audits codebases across:
  1. Security & Secrets (RLS, API keys, CORS, localStorage auth, SQL injection, webhooks)
  2. UX & Functional Completeness (404, loading, skeletons, empty states, mobile, delete account)
  3. SEO & AI Discoverability (robots.txt, llms.txt, sitemaps, OpenGraph, JSON-LD, headings)
  4. Legal & Compliance (Privacy, Terms, Cookies, Refund, business identity, data deletion)
  5. Ops & Observability (Analytics, Error tracking, rate limiting, source maps)
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path

# ANSI colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

class VibeAuditor:
    def __init__(self, root_dir: str):
        self.root = Path(root_dir).resolve()
        self.issues = []
        self.warnings = []
        self.passes = []
        self.ignore_dirs = {
            "node_modules", ".git", ".next", ".nuxt", "dist", "build",
            ".turbo", ".cache", "venv", ".venv", "__pycache__", ".agents"
        }
        self.code_exts = {".ts", ".tsx", ".js", ".jsx", ".html", ".vue", ".svelte", ".py"}
        self.pkg_data = self._load_package_json()

    def _load_package_json(self):
        pkg_file = self.root / "package.json"
        if pkg_file.exists():
            try:
                return json.loads(pkg_file.read_text(errors="ignore"))
            except Exception:
                return {}
        return {}

    def log_issue(self, category: str, title: str, details: str, fix: str):
        self.issues.append({"category": category, "title": title, "details": details, "fix": fix})

    def log_warning(self, category: str, title: str, details: str, fix: str):
        self.warnings.append({"category": category, "title": title, "details": details, "fix": fix})

    def log_pass(self, category: str, title: str):
        self.passes.append({"category": category, "title": title})

    def run_all(self):
        print(f"\n{BOLD}{CYAN}🔍 Auditing vibe-coded project at: {self.root}{RESET}\n")
        self.check_env_and_git()
        self.check_frontend_secret_leaks()
        self.check_database_and_backend_security()
        self.check_code_level_vulnerabilities()
        self.check_public_assets_and_metadata()
        self.check_html_and_accessibility()
        self.check_error_and_loading_pages()
        self.check_account_and_user_flows()
        self.check_seo_and_ai_discovery()
        self.check_legal_and_compliance()
        self.check_ops_and_observability()
        self.print_report()

    # ---------------------------------------------------------
    # 1. Security & Secrets
    # ---------------------------------------------------------
    def check_env_and_git(self):
        cat = "Security: Git & Secrets"
        gitignore_path = self.root / ".gitignore"
        env_files = [f for f in self.root.glob("**/.env*") if not any(part in self.ignore_dirs for part in f.parts)]

        if not gitignore_path.exists():
            self.log_issue(cat, "Missing .gitignore", "No .gitignore found at root.", "Create a .gitignore file and ignore .env*, node_modules/, etc.")
        else:
            content = gitignore_path.read_text(errors="ignore")
            if ".env" not in content:
                self.log_issue(cat, ".env not in .gitignore", ".gitignore does not ignore .env files.", "Add '.env*' to .gitignore immediately.")
            else:
                self.log_pass(cat, ".env is properly ignored in .gitignore")

        committed_env = [ef for ef in env_files if ef.name in [".env", ".env.local", ".env.production"]]
        if committed_env:
            self.log_warning(cat, f"Local env files detected ({len(committed_env)})",
                             f"Files: {', '.join(f.name for f in committed_env)}. Ensure these are never committed.",
                             "Run `git status` to verify these files are untracked.")

    def check_frontend_secret_leaks(self):
        cat = "Security: Secret Exposure"
        suspicious_vars = []
        secret_patterns = [
            re.compile(r'(?:NEXT_PUBLIC_|VITE_|REACT_APP_)[A-Z0-9_]*(?:SECRET|PRIVATE|PASSWORD|SERVICE_ROLE)', re.IGNORECASE),
            re.compile(r'service_role', re.IGNORECASE),
            re.compile(r'sk_live_[a-zA-Z0-9]{20,}', re.IGNORECASE),
            re.compile(r'ghp_[a-zA-Z0-9]{20,}', re.IGNORECASE),
        ]

        for p in self.root.rglob("*"):
            if p.is_file() and p.suffix in self.code_exts and not any(part in self.ignore_dirs for part in p.parts):
                try:
                    text = p.read_text(errors="ignore")
                    for pat in secret_patterns:
                        matches = pat.findall(text)
                        if matches:
                            suspicious_vars.append((str(p.relative_to(self.root)), matches[0]))
                except Exception:
                    pass

        if suspicious_vars:
            unique = set(suspicious_vars[:5])
            details = "; ".join([f"{f[0]} contains '{f[1]}'" for f in unique])
            self.log_issue(cat, "Exposed Secret / Service Role in Frontend Code", details,
                           "Move private secrets to server-side routes or environment variables without NEXT_PUBLIC_/VITE_ prefixes.")
        else:
            self.log_pass(cat, "No private secrets or service_role found in client code")

    def check_database_and_backend_security(self):
        cat = "Security: Database & API"
        # Check Supabase / PostgreSQL RLS
        sql_files = [f for f in self.root.glob("**/*.sql") if not any(part in self.ignore_dirs for part in f.parts)]
        if sql_files:
            has_rls = False
            for sf in sql_files:
                text = sf.read_text(errors="ignore").upper()
                if "ENABLE ROW LEVEL SECURITY" in text:
                    has_rls = True
                    break
            if not has_rls:
                self.log_issue(cat, "Missing Database Row Level Security (RLS)",
                               "SQL migrations exist but lack `ENABLE ROW LEVEL SECURITY;`.",
                               "Run `ALTER TABLE <table_name> ENABLE ROW LEVEL SECURITY;` and add user isolation policies.")
            else:
                self.log_pass(cat, "Row Level Security (RLS) enabled in SQL files")

        # Check CORS Wildcard
        cors_wildcard = []
        for p in self.root.rglob("*"):
            if p.is_file() and p.suffix in {".ts", ".js"} and ("api" in str(p) or "server" in str(p)):
                if not any(part in self.ignore_dirs for part in p.parts):
                    try:
                        text = p.read_text(errors="ignore")
                        if 'Access-Control-Allow-Origin", "*"' in text or "Access-Control-Allow-Origin': '*'" in text or 'cors({ origin: "*" })' in text:
                            cors_wildcard.append(str(p.relative_to(self.root)))
                    except Exception:
                        pass
        if cors_wildcard:
            self.log_issue(cat, "Permissive CORS Wildcard (*)", f"Wildcard CORS found in: {', '.join(cors_wildcard[:3])}",
                           "Lock CORS to explicit production and preview domains.")
        else:
            self.log_pass(cat, "No wildcard CORS (*) found in API routes")

    def check_code_level_vulnerabilities(self):
        cat = "Security: Code Vulnerabilities"
        localstorage_tokens = []
        raw_html_xss = []
        sql_concat = []

        for p in self.root.rglob("*"):
            if p.is_file() and p.suffix in self.code_exts and not any(part in self.ignore_dirs for part in p.parts):
                try:
                    text = p.read_text(errors="ignore")
                    # Check localStorage auth token storage
                    if re.search(r'localStorage\.setItem\([\'"][^\'"]*(?:token|auth|session|jwt)[\'"]', text, re.I):
                        localstorage_tokens.append(str(p.relative_to(self.root)))
                    # Check raw HTML injection (XSS)
                    if "dangerouslySetInnerHTML" in text or "v-html" in text:
                        raw_html_xss.append(str(p.relative_to(self.root)))
                    # Check SQL string concatenation
                    if re.search(r'(?:SELECT|INSERT|UPDATE|DELETE)\s+.*?\+\s*[a-zA-Z_]', text, re.I) or \
                       re.search(r'`(?:SELECT|INSERT|UPDATE|DELETE)\s+.*?\$\{', text, re.I):
                        sql_concat.append(str(p.relative_to(self.root)))
                except Exception:
                    pass

        if localstorage_tokens:
            self.log_warning(cat, "Auth Tokens in localStorage",
                             f"Found localStorage token storage in: {', '.join(localstorage_tokens[:3])}",
                             "Store auth tokens in HttpOnly, Secure, SameSite cookies to protect against XSS token theft.")
        else:
            self.log_pass(cat, "No plain auth tokens stored in localStorage")

        if raw_html_xss:
            self.log_warning(cat, "Raw HTML Rendering (XSS Risk)",
                             f"Found dangerouslySetInnerHTML or v-html in: {', '.join(raw_html_xss[:3])}",
                             "Sanitize user-provided HTML with DOMPurify before rendering.")
        else:
            self.log_pass(cat, "No raw HTML rendering without sanitization found")

        if sql_concat:
            self.log_issue(cat, "Potential SQL String Concatenation",
                           f"Found string interpolation in SQL queries in: {', '.join(sql_concat[:3])}",
                           "Use parameterized queries or ORM queries (Prisma/Drizzle/Supabase) to prevent SQL injection.")
        else:
            self.log_pass(cat, "No raw SQL string concatenation detected")

    # ---------------------------------------------------------
    # 2. UX & Identity Completeness
    # ---------------------------------------------------------
    def check_public_assets_and_metadata(self):
        cat = "UX & Brand Identity"
        favicons = [f for f in self.root.glob("**/favicon*") if not any(part in self.ignore_dirs for part in f.parts)] + \
                   [f for f in self.root.glob("**/icon.*") if not any(part in self.ignore_dirs for part in f.parts)]
        
        has_vite_favicon = any("vite.svg" in f.name for f in favicons)
        if has_vite_favicon:
            self.log_issue(cat, "Default Vite Favicon Detected", "Using default vite.svg icon.", "Replace with custom branded favicon (SVG/PNG/ICO).")
        elif not favicons:
            self.log_warning(cat, "Missing Favicon Set", "No favicon.ico or icon.png found.", "Add a branded favicon and apple-touch-icon.")
        else:
            self.log_pass(cat, "Custom branded favicon present")

        # OpenGraph Image
        og_images = [f for f in self.root.glob("**/opengraph-image*") if not any(part in self.ignore_dirs for part in f.parts)] + \
                    [f for f in self.root.glob("**/og-image*") if not any(part in self.ignore_dirs for part in f.parts)] + \
                    [f for f in self.root.glob("**/og.*") if not any(part in self.ignore_dirs for part in f.parts)]
        if not og_images:
            self.log_warning(cat, "Missing Open Graph Image (og:image)", "No 1200x630px social card preview found.",
                             "Add opengraph-image.png so links look professional on Twitter, LinkedIn, and Discord.")
        else:
            self.log_pass(cat, "Open Graph social preview image present")

        # Default Titles
        for p in self.root.rglob("*"):
            if p.is_file() and p.name in ["index.html", "layout.tsx", "App.tsx"] and not any(part in self.ignore_dirs for part in p.parts):
                try:
                    text = p.read_text(errors="ignore")
                    if "Vite + React" in text or "Create Next App" in text:
                        self.log_issue(cat, "Default Framework Title Detected",
                                       f"File {p.relative_to(self.root)} contains default title ('Vite + React' or 'Create Next App').",
                                       "Replace with your product's actual name and value proposition.")
                except Exception:
                    pass

    def check_html_and_accessibility(self):
        cat = "HTML & Accessibility"
        missing_alt = 0
        missing_lang = False

        html_files = [f for f in self.root.glob("**/*.html") if not any(part in self.ignore_dirs for part in f.parts)]
        for hf in html_files:
            try:
                text = hf.read_text(errors="ignore")
                if "<html" in text and 'lang=' not in text:
                    missing_lang = True
            except Exception:
                pass

        if missing_lang:
            self.log_warning(cat, "Missing HTML `lang` Attribute", "<html lang=\"en\"> is missing.",
                             "Add `lang=\"en\"` to the root <html> tag for screen readers and SEO.")
        else:
            self.log_pass(cat, "HTML lang attribute is present")

        # Check img alt tags in JSX/HTML
        for p in self.root.rglob("*"):
            if p.is_file() and p.suffix in {".tsx", ".jsx", ".html"} and not any(part in self.ignore_dirs for part in p.parts):
                try:
                    text = p.read_text(errors="ignore")
                    # Match <img ... without alt=
                    imgs = re.findall(r'<img\s+[^>]*>', text)
                    for img in imgs:
                        if 'alt=' not in img:
                            missing_alt += 1
                except Exception:
                    pass

        if missing_alt > 0:
            self.log_warning(cat, f"Missing `alt` Attributes ({missing_alt} images)",
                             f"Found {missing_alt} <img> tags missing an alt description.",
                             "Add meaningful alt text to images for accessibility and SEO.")
        else:
            self.log_pass(cat, "Image alt attributes present")

    def check_error_and_loading_pages(self):
        cat = "UX & App Resilience"
        not_found_pages = [f for f in self.root.glob("**/not-found.*") if not any(part in self.ignore_dirs for part in f.parts)] + \
                          [f for f in self.root.glob("**/404.*") if not any(part in self.ignore_dirs for part in f.parts)]
        if not not_found_pages:
            self.log_issue(cat, "Missing Custom 404 Page", "No not-found.tsx, 404.tsx, or 404.html found.",
                           "Create a custom 404 page with navigation to Home and Support.")
        else:
            self.log_pass(cat, "Custom 404 page present")

        loading_files = [f for f in self.root.glob("**/loading.*") if not any(part in self.ignore_dirs for part in f.parts)]
        error_files = [f for f in self.root.glob("**/error.*") if not any(part in self.ignore_dirs for part in f.parts)]

        if not loading_files:
            self.log_warning(cat, "Missing Loading / Skeleton States", "No loading.tsx or skeleton loaders found.",
                             "Add skeleton placeholders or loading spinners to prevent blank screen freezes.")
        else:
            self.log_pass(cat, "Loading / skeleton states present")

        if not error_files:
            self.log_warning(cat, "Missing Error Boundary", "No error.tsx or custom ErrorBoundary found.",
                             "Add error boundaries to capture client exceptions gracefully.")
        else:
            self.log_pass(cat, "Error boundary present")

    def check_account_and_user_flows(self):
        cat = "User Lifecycle & Trust"
        all_text = ""
        for p in self.root.rglob("*"):
            if p.is_file() and p.suffix in self.code_exts and not any(part in self.ignore_dirs for part in p.parts):
                try:
                    all_text += " " + p.read_text(errors="ignore")
                except Exception:
                    pass

        has_delete_account = bool(re.search(r'delete\s*account|remove\s*account|danger\s*zone', all_text, re.I))
        if not has_delete_account:
            self.log_warning(cat, "Missing Account Deletion Option",
                             "No 'Delete Account' button or flow detected.",
                             "Add an account deletion option (mandatory for Apple App Store, Google Play, and GDPR).")
        else:
            self.log_pass(cat, "Account deletion flow detected")

    # ---------------------------------------------------------
    # 3. SEO & AI Discoverability
    # ---------------------------------------------------------
    def check_seo_and_ai_discovery(self):
        cat = "SEO & AI Discoverability"
        robots_paths = [f for f in self.root.glob("**/robots.txt") if not any(part in self.ignore_dirs for part in f.parts)] + \
                       [f for f in self.root.glob("**/robots.ts") if not any(part in self.ignore_dirs for part in f.parts)]
        if not robots_paths:
            self.log_issue(cat, "Missing robots.txt", "No robots.txt found.", "Create public/robots.txt allowing AI search engines and web crawlers.")
        else:
            try:
                content = robots_paths[0].read_text(errors="ignore")
                if "GPTBot" in content or "ClaudeBot" in content or "PerplexityBot" in content:
                    self.log_pass(cat, "robots.txt explicitly configures AI crawlers (GPTBot, ClaudeBot, PerplexityBot)")
                else:
                    self.log_warning(cat, "robots.txt Lacks Explicit AI Crawler Directives",
                                     "robots.txt does not explicitly mention GPTBot, ClaudeBot, or PerplexityBot.",
                                     "Allow AI search crawlers so your app appears in AI Overviews and answer engines.")
            except Exception:
                self.log_pass(cat, "robots.txt present")

        # Sitemap
        sitemaps = [f for f in self.root.glob("**/sitemap.*") if not any(part in self.ignore_dirs for part in f.parts)]
        if not sitemaps:
            self.log_issue(cat, "Missing sitemap.xml", "No sitemap.xml or sitemap.ts found.", "Add a dynamic sitemap for search engine indexing.")
        else:
            self.log_pass(cat, "sitemap.xml present")

        # llms.txt
        llms_paths = [f for f in self.root.glob("**/llms.txt") if not any(part in self.ignore_dirs for part in f.parts)]
        if not llms_paths:
            self.log_warning(cat, "Missing llms.txt", "No llms.txt found in public/ directory.",
                             "Create public/llms.txt so LLM agents can understand your product structure and APIs.")
        else:
            self.log_pass(cat, "llms.txt present for AI agents")

    # ---------------------------------------------------------
    # 4. Legal & Compliance
    # ---------------------------------------------------------
    def check_legal_and_compliance(self):
        cat = "Legal & Compliance"
        files_lower = [str(p).lower() for p in self.root.rglob("*") if p.is_file() and not any(part in self.ignore_dirs for part in p.parts)]

        has_privacy = any("privacy" in f for f in files_lower)
        has_terms = any("terms" in f for f in files_lower)
        has_refund = any("refund" in f for f in files_lower)
        has_cookie = any("cookie" in f for f in files_lower)

        if not has_privacy:
            self.log_issue(cat, "Missing Privacy Policy (/privacy)", "No privacy policy route or page found.",
                           "Add /privacy page covering data collection, third-party trackers, and user rights.")
        else:
            self.log_pass(cat, "Privacy Policy page detected")

        if not has_terms:
            self.log_issue(cat, "Missing Terms of Service (/terms)", "No terms of service route or page found.",
                           "Add /terms page covering acceptable use, liability limits, and billing terms.")
        else:
            self.log_pass(cat, "Terms of Service page detected")

        if not has_refund:
            self.log_warning(cat, "Missing Refund / Cancellation Policy (/refund)", "No refund policy page found.",
                             "Add /refund or cancellation terms (mandatory for Stripe/LemonSqueezy merchant approval).")
        else:
            self.log_pass(cat, "Refund / cancellation policy detected")

        if not has_cookie:
            self.log_warning(cat, "Missing Cookie Consent / Policy", "No cookie policy or banner component found.",
                             "Add a cookie banner if using analytics or third-party cookies.")
        else:
            self.log_pass(cat, "Cookie policy or component detected")

    # ---------------------------------------------------------
    # 5. Ops & Observability
    # ---------------------------------------------------------
    def check_ops_and_observability(self):
        cat = "Ops & Observability"
        deps = {}
        if self.pkg_data:
            deps.update(self.pkg_data.get("dependencies", {}))
            deps.update(self.pkg_data.get("devDependencies", {}))

        # Check Error Tracking (Sentry, etc.)
        has_error_tracker = any(k in deps for k in ["@sentry/nextjs", "@sentry/react", "@sentry/browser", "bugsnag-js", "@highlight-run/next"])
        if not has_error_tracker:
            self.log_warning(cat, "No Production Error Tracking (Sentry / Bugsnag)",
                             "No error tracking dependency found in package.json.",
                             "Install Sentry (`@sentry/nextjs`) to catch production errors before users report them.")
        else:
            self.log_pass(cat, "Production error tracking installed")

        # Check Analytics
        has_analytics = any(k in deps for k in ["posthog-js", "posthog-node", "@vercel/analytics", "mixpanel-browser", "plausible-tracker"])
        if not has_analytics:
            self.log_warning(cat, "No Analytics Installed", "No analytics library found in package.json.",
                             "Install PostHog, Plausible, or Umami to track user conversion and retention.")
        else:
            self.log_pass(cat, "Analytics library installed")

        # Check Rate Limiting
        has_ratelimit = any(k in deps for k in ["@upstash/ratelimit", "express-rate-limit", "@arcjet/next"])
        if not has_ratelimit:
            self.log_warning(cat, "No API Rate Limiting Library", "No rate limiting package found in package.json.",
                             "Install @upstash/ratelimit or Arcjet to protect APIs from abuse and runaway costs.")
        else:
            self.log_pass(cat, "Rate limiting library installed")

    # ---------------------------------------------------------
    # Report Presentation
    # ---------------------------------------------------------
    def print_report(self):
        print(f"{BOLD}{'=' * 70}{RESET}")
        print(f"{BOLD}             VIBE-HARDENER PRODUCTION AUDIT REPORT{RESET}")
        print(f"{BOLD}{'=' * 70}{RESET}\n")

        if self.passes:
            print(f"{BOLD}{GREEN}✅ PASSED CHECKS ({len(self.passes)}):{RESET}")
            for p in self.passes:
                print(f"  {GREEN}✔{RESET} [{p['category']}] {p['title']}")
            print()

        if self.warnings:
            print(f"{BOLD}{YELLOW}⚠️  WARNINGS & GAPS ({len(self.warnings)}):{RESET}")
            for w in self.warnings:
                print(f"  {YELLOW}▲{RESET} [{w['category']}] {BOLD}{w['title']}{RESET}")
                print(f"     Details: {w['details']}")
                print(f"     Fix:     {CYAN}{w['fix']}{RESET}")
            print()

        if self.issues:
            print(f"{BOLD}{RED}🚨 CRITICAL ISSUES / VIBE-CODE GIVEAWAYS ({len(self.issues)}):{RESET}")
            for i in self.issues:
                print(f"  {RED}✖{RESET} [{i['category']}] {BOLD}{i['title']}{RESET}")
                print(f"     Details: {i['details']}")
                print(f"     Fix:     {CYAN}{i['fix']}{RESET}")
            print()
        else:
            print(f"{BOLD}{GREEN}🎉 Zero critical vibe-code flaws found!{RESET}\n")

        score = max(0, 100 - (len(self.issues) * 12) - (len(self.warnings) * 4))
        score_color = GREEN if score >= 85 else (YELLOW if score >= 60 else RED)
        print(f"{BOLD}Production Readiness Score: {score_color}{score}/100{RESET}\n")


def main():
    parser = argparse.ArgumentParser(description="Audit a vibe-coded web application for production readiness.")
    parser.add_argument("path", nargs="?", default=".", help="Root directory of the project to audit (default: .)")
    args = parser.parse_args()

    auditor = VibeAuditor(args.path)
    auditor.run_all()

if __name__ == "__main__":
    main()
