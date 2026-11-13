# 04. Legal & Compliance Hardening Guide

Vibe-coded apps often launch without basic legal protection, leaving creators vulnerable to chargebacks, GDPR/FTC fines, and automated copyright or privacy demand letters.

---

## 1. The 4 Mandatory Legal Pages

Every commercial or user-facing application must provide direct, crawlable footer links to:

### 1. `/privacy` (Privacy Policy Page)
- **Data Collection:** Specify exact data gathered (Name, Email, Payment info via Stripe, Analytics cookies).
- **Data Minimization:** Explicitly state the data retention period and adherence to the *Only collect necessary data* principle.
- **Third-Party Disclosures:** List all external sub-processors (Supabase, Vercel, PostHog, Resend, Stripe).
- **User Rights:** Provide clear instructions for accessing, downloading, or permanently deleting user data.
- **Contact:** Official privacy inquiries inbox (`privacy@yourdomain.com`).

### 2. `/terms` (Terms of Service / T&C's Page)
- **Acceptable Use:** Strict prohibition of abuse, scraping, automated reverse-engineering, and illegal activity.
- **Limitation of Liability:** "AS IS" disclaimer, capping financial liability to fees paid in the last 12 months.
- **Governing Jurisdiction:** Explicit legal jurisdiction, venue, and arbitration/dispute resolution clauses.
- **Age Consent / Minors:** Mandatory COPPA / GDPR-K clause (minimum age 13+ or 16+).

### 3. `/refund` (Refund & Cancellation Policy)
- **Processor Compliance:** Required by Stripe, Lemon Squeezy, and merchant acquiring banks.
- **Clear Terms:** Specify refund window (e.g. 14-day money-back guarantee, or strict no-refunds on consumed AI tokens/credits).
- **Execution:** Direct email or portal link for submitting refund and cancellation requests.

### 4. `/cookies` (Cookies Policy & Cookie Consent)
- **Cookie Categorization:** Break cookies into **Strictly Necessary** (auth sessions), **Analytics** (PostHog, Google Analytics), and **Marketing/Ads** (Meta Pixel).
- **Consent Banner:** Require explicit opt-in before firing non-essential tracking scripts for European (GDPR) and UK (PECR) visitors.

---

## 2. The 20 Anti-Litigation Checks (Zero Hallucination Verification)

### ⚖️ Legal, Consumer Rights & Identity
1. **Privacy policy:** Maintain a live `/privacy` route disclosing all data practices.
2. **Terms of service:** Maintain a live `/terms` route covering acceptable use, dispute resolution, and disclaimers.
3. **Refund policy:** Maintain a live `/refund` route with clear cancellation rules to satisfy Stripe requirements.
4. **Cookie policy:** Maintain a live `/cookies` route detailing all cookies, expiry times, and purposes.
5. **Cookie consent banner:** Implement a consent management banner with granular Accept / Reject toggles before storing non-essential cookies.
6. **Check form consents:** Use un-checked opt-in checkboxes for email marketing. Require explicit Terms and Privacy agreement on signup.
7. **Collect only needed data (Data Minimization):** Strip unneeded form fields (e.g., don't ask for phone, address, or full name unless required to fulfill service).
8. **Audit third-party SDKs:** Review every client-side SDK (analytics, heatmaps, social pixels, crash reporters) to ensure they comply with user consent and don't leak PII.
9. **Remove dark patterns:** Eliminate deceptive UI tricks (e.g., hidden cancel buttons, countdown timers with fake urgency, disguised ads, or pre-selected recurring add-ons).
10. **No hidden fees:** Display all recurring subscription billing intervals, renewal dates, taxes, and cancellation policies transparently before checkout.
11. **No fake reviews:** Ban fabricated testimonials, fake user names, and AI-generated reviewer photos (FTC 16 CFR Part 465 enforcement target).
12. **No unsupported claims:** Eliminate unsubstantiated performance guarantees (e.g., "10x your revenue in 7 days", "100% guaranteed success").
13. **Business details:** Display a verifiable legal entity name, registered office address, company number, and official support email in the footer.
14. **Age consent for kids (COPPA / GDPR-K):** Include an explicit age gate / minimum age requirement (13+ in US, 16+ in EU) in onboarding and Terms.
15. **Unsubscribe link:** Every automated transactional or marketing email sent via Resend/Postmark must include a working 1-click unsubscribe header and footer link.
16. **License stock images:** Ensure all photography, illustrations, icons, and fonts have commercial licenses (Unsplash commercial license, Lucide icons, Google Fonts). Never use copyrighted brand marks without license.
17. **Data deletion option:** Provide a direct button in User Settings allowing users to permanently delete their account and associated data.

### ♿ Accessibility & Screen Reader Standards (ADA / WCAG 2.1 AA)
18. **Add alt text & graphic roles:** Meaningful, descriptive `alt="..."` attributes on all content images. Decorative images must have `alt=""` and `aria-hidden="true"`. Decorative SVGs/icons must have `aria-hidden="true"` and `focusable="false"`. Complex infographics and diagrams must use `role="img"` with an informative `aria-label`.
19. **Fix color contrast:** Minimum contrast ratio of **4.5:1** for standard text and **3:1** for large text/icons against backgrounds (WebAIM WCAG AA).
20. **Keyboard navigation & forms:** Ensure every form and button can be navigated using `Tab` and `Shift+Tab`, submitted using `Enter`, has a clearly visible `:focus-visible` outline, and links inline errors with `aria-invalid="true"` and `aria-describedby="[error-id]"`.
21. **Skip-to-content link:** Provide an accessible skip link (e.g. `<a href="#main" className="sr-only focus:not-sr-only ...">Skip to content</a>`) as the first focusable element so screen reader and keyboard users can bypass repetitive navigation headers.
22. **Semantic landmarks & navigation:** Structure layouts with `<header>` (`role="banner"`), `<main>`, `<footer>` (`role="contentinfo"`), and `<nav>`. When multiple `<nav>` landmarks exist (primary, mobile, footer link groups), provide distinct, descriptive `aria-label` attributes (e.g. `aria-label="Primary"`, `aria-label="Company links"`).
23. **Strict heading hierarchy:** Enforce sequential `<h1>` → `<h2>` → `<h3>` levels without skipping levels (e.g. avoid jumping from `<h1>` directly to `<h3>` or `<h4>`), preserving the screen reader heading navigation outline (`H` key).
24. **Animated & looping text (typewriters, marquees, counters):** Live character-by-character typing or ticker animations stutter heavily on screen readers. Mark animated strings, sizers, and blinking cursors with `aria-hidden="true"`, and provide the complete, static target phrase in an accessible `.sr-only` container so screen readers read whole coherent phrases.
25. **Interactive disclosures & accordions (FAQs, service details):** Prefer native `<details>` and `<summary>` elements which communicate expand/collapse states natively across all screen readers. For custom accordions, strictly manage `aria-expanded="true|false"` and `aria-controls="[id]"`.
26. **Live regions & dynamic state updates:** When filters, search queries, or tab panels update content asynchronously without a full page reload, announce state changes using `role="status"` and `aria-live="polite"` with `aria-atomic="true"`. Interactive filter/toggle buttons must expose toggle state via `aria-pressed="true|false"`.
27. **Modals, dialogs & focus trapping:** Modal dialogs (lightboxes, drawers, mobile menus) must use `role="dialog"` and `aria-modal="true"`. Move focus into the dialog upon opening, trap `Tab` navigation inside while open, dismiss on `Escape`, and return focus to the triggering element upon exit.
28. **Clear button & interactive labels:** Ban ambiguous labels like "Click Here", "Learn More", or standalone icon buttons without text. Use descriptive action verbs with `aria-label` (e.g. `aria-label="Submit registration form"`).
29. **Accessibility tree verification:** Audit using browser DevTools Accessibility Tree or browser automation tools (e.g. Kimi WebBridge `snapshot`) to verify computed accessible names, roles, and states as seen by screen readers.
