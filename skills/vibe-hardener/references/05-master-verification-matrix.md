# 05. Master Verification Matrix

This matrix provides 100% verified, cross-referenced proof that every single point from your checklists is implemented and audited.

---

## Proof Table 1: "Your vibe coded app is fake. It's missing 19 things that make it real" (19/19)

| # | Item from Image 1 | Exact Skill File Location | Implementation & Verification Proof |
|:---:|---|---|---|
| **1** | **Real login and logout** | [`02-ux-completeness.md`](./02-ux-completeness.md#6-real-authentication-lifecycle) (Line 73) | Session invalidation and cookie clearing on logout using Supabase/Clerk/Auth.js. |
| **2** | **Password reset** | [`02-ux-completeness.md`](./02-ux-completeness.md#6-real-authentication-lifecycle) (Line 74) | Dedicated `/forgot-password` and `/reset-password` routes with secure token exchange. |
| **3** | **Email verification** | [`02-ux-completeness.md`](./02-ux-completeness.md#6-real-authentication-lifecycle) (Line 75) | Enforce email confirmation before dashboard access. |
| **4** | **Loading states** | [`02-ux-completeness.md`](./02-ux-completeness.md#2-skeleton-loaders--loading-states) (Line 44), [`scripts/audit.py`](../scripts/audit.py) (Line 229) | `loading.tsx` and animated skeleton placeholders matching component geometry. |
| **5** | **Empty states** | [`02-ux-completeness.md`](./02-ux-completeness.md#3-empty-states-0-items-found) (Line 64) | Dedicated empty state components with illustrations, friendly text, and primary CTA. |
| **6** | **Clear error messages** | [`02-ux-completeness.md`](./02-ux-completeness.md#4-form-validation--error-states) (Line 76) | Inline field errors with high contrast and accessible `aria-invalid` markup. |
| **7** | **Form validation** | [`01-security-hardening.md`](./01-security-hardening.md#4-input-validation-with-zod) (Line 60), [`02-ux-completeness.md`](./02-ux-completeness.md#4-form-validation--error-states) | Server and client validation with Zod schemas. |
| **8** | **Rate limiting** | [`01-security-hardening.md`](./01-security-hardening.md#5-rate-limiting-upstash--arcjet--memory) (Line 78), [`scripts/audit.py`](../scripts/audit.py) (Line 307) | Slotted window rate limiting via `@upstash/ratelimit` or Arcjet. |
| **9** | **Database backups** | [`02-ux-completeness.md`](./02-ux-completeness.md#8-database-backups--recovery-plan) (Line 85) | Automated daily backups with tested restore procedure and Point-In-Time Recovery. |
| **10** | **Row level security** | [`01-security-hardening.md`](./01-security-hardening.md#2-supabase--postgresql-row-level-security-rls) (Line 28), [`scripts/audit.py`](../scripts/audit.py) (Line 126) | `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;` + ownership policies. |
| **11** | **API keys off the frontend** | [`01-security-hardening.md`](./01-security-hardening.md#1-secrets--git-hygiene) (Line 1), [`scripts/audit.py`](../scripts/audit.py) (Line 96) | Scan and strip secrets from client bundles (`NEXT_PUBLIC_` / `VITE_`). |
| **12** | **Mobile layout** | [`02-ux-completeness.md`](./02-ux-completeness.md#5-mobile-layout--sticky-cta) (Line 85) | Viewport meta, 48px touch targets, and sticky mobile CTA. |
| **13** | **Custom 404 page** | [`02-ux-completeness.md`](./02-ux-completeness.md#1-custom-404-not-found-experience) (Line 14), [`scripts/audit.py`](../scripts/audit.py) (Line 219) | Dedicated `not-found.tsx` / `404.tsx` with home & support navigation. |
| **14** | **Analytics installed** | [`scripts/audit.py`](../scripts/audit.py) (Line 299), [`SKILL.md`](../SKILL.md) | Audit for PostHog, Plausible, or Umami analytics dependencies. |
| **15** | **Error tracking** | [`scripts/audit.py`](../scripts/audit.py) (Line 291), [`SKILL.md`](../SKILL.md) | Audit for `@sentry/nextjs` or Bugsnag crash monitoring. |
| **16** | **Privacy policy page** | [`04-legal-compliance.md`](./04-legal-compliance.md#1-privacy-privacy-policy-page) (Line 10), [`scripts/audit.py`](../scripts/audit.py) (Line 257) | Live `/privacy` page with disclosures, retention periods, and contact email. |
| **17** | **Terms page** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-terms-terms-of-service--tcs-page) (Line 18), [`scripts/audit.py`](../scripts/audit.py) (Line 263) | Live `/terms` page covering acceptable use, dispute resolution, and liability limits. |
| **18** | **Delete account button** | [`02-ux-completeness.md`](./02-ux-completeness.md#9-account-deletion--data-export-gdpr--apple-app-store-mandatory) (Line 91), [`scripts/audit.py`](../scripts/audit.py) (Line 241) | Two-step "Danger Zone" account deletion and data export button. |
| **19** | **Onboarding flow** | [`02-ux-completeness.md`](./02-ux-completeness.md#7-first-run-onboarding-flow) (Line 79) | 3-step setup guide directing user to their first action. |

---

## Proof Table 2: "20 things to have Claude do so your app doesn't get sued" (20/20)

| # | Item from Image 2 | Exact Skill File Location | Implementation & Verification Proof |
|:---:|---|---|---|
| **1** | **Privacy policy** | [`04-legal-compliance.md`](./04-legal-compliance.md#1-privacy-privacy-policy-page) (Line 10), [`scripts/audit.py`](../scripts/audit.py) (Line 257) | Live `/privacy` route detailing all personal data collection. |
| **2** | **Terms of service** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-terms-terms-of-service--tcs-page) (Line 18), [`scripts/audit.py`](../scripts/audit.py) (Line 263) | Live `/terms` route covering disclaimers and limitation of liability. |
| **3** | **Refund policy** | [`04-legal-compliance.md`](./04-legal-compliance.md#3-refund-refund--cancellation-policy) (Line 26), [`scripts/audit.py`](../scripts/audit.py) (Line 269) | Live `/refund` route satisfying payment processor requirements. |
| **4** | **Cookie policy** | [`04-legal-compliance.md`](./04-legal-compliance.md#4-cookies-cookies-policy--cookie-consent) (Line 32), [`scripts/audit.py`](../scripts/audit.py) (Line 276) | Live `/cookies` route categorizing strictly necessary vs analytics vs ads. |
| **5** | **Cookie consent banner** | [`04-legal-compliance.md`](./04-legal-compliance.md#4-cookies-cookies-policy--cookie-consent) (Line 34), [`scripts/audit.py`](../scripts/audit.py) (Line 276) | Granular Accept/Reject banner prior to storing cookies. |
| **6** | **Check form consents** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 44) | Explicit un-checked opt-in marketing boxes + Terms acceptance statement. |
| **7** | **Collect only needed data** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 45) | Data Minimization (GDPR Art. 5): Strip excessive personal fields. |
| **8** | **Audit third-party SDKs** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 46) | Audit analytics/pixels to ensure consent compliance and no PII leakage. |
| **9** | **Remove dark patterns** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 47) | Eliminate hidden cancel buttons, fake countdowns, and pre-selected add-ons. |
| **10** | **No hidden fees** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 48) | Clear recurring billing terms, renewal dates, and taxes before checkout. |
| **11** | **No fake reviews** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 49) | FTC 16 CFR Part 465 ban on fabricated testimonials and AI personas. |
| **12** | **No unsupported claims** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 50) | Strip unverified promises ("10x ROI", "100% cure") without substantiation. |
| **13** | **Add alt text** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 57), [`scripts/audit.py`](../scripts/audit.py) (Line 198) | Meaningful descriptive `alt` attributes on all images. |
| **14** | **Fix color contrast** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 58) | WCAG AA minimum contrast ratio (4.5:1 text, 3:1 large icons). |
| **15** | **Keyboard navigation** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 59) | Full Tab order, Enter key form submission, and `:focus-visible` styling. |
| **16** | **Business details** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 51) | Legal company entity, registered office address, and support email in footer. |
| **17** | **Age consent for kids** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 52) | Explicit COPPA (13+) / GDPR-K (16+) age gate and terms clause. |
| **18** | **Unsubscribe link** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 53) | Mandatory 1-click unsubscribe header & footer in all outbound emails. |
| **19** | **License stock images** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 54) | Commercial licensing verification for all photos, icons, and fonts. |
| **20** | **Data deletion option** | [`04-legal-compliance.md`](./04-legal-compliance.md#2-the-20-anti-litigation-checks-zero-hallucination-verification) (Line 55), [`02-ux-completeness.md`](./02-ux-completeness.md#9-account-deletion--data-export-gdpr--apple-app-store-mandatory) | Direct self-service account deletion and data export in User Settings. |
