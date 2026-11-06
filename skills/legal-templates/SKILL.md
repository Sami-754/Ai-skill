---
name: legal-templates
description: "Attorney-drafted CC0 legal templates and contracts for startups, SaaS, tech companies, and agencies. Use to draft, review, customize, or inspect NDAs, Terms of Use, Privacy Policies, DPAs, Offer Letters, Advisory Agreements, and MSAs."
---

# Legal Templates & Contracts Skill

This skill equips any AI agent and human developer with attorney-drafted, battle-tested legal documents released under the **CC0 1.0 Universal License** by [General Legal](https://general.legal). Every document is maintained in both **LLM-optimized Markdown** and original **Microsoft Word (.DOCX)** formats.

---

## ⚡ Global CLI Quick Reference

The `legal` (and `legal-templates`) command is globally installed in `~/.local/bin/legal`.

| Task | Command |
| :--- | :--- |
| **List all templates** | `legal list` *(or `legal list --json`)* |
| **Inspect template overview & key clauses** | `legal info <slug>` |
| **Inspect customizable placeholders** | `legal placeholders <slug>` *(or `legal placeholders <slug> --json`)* |
| **Search across all templates & clauses** | `legal search "<keyword or clause>"` |
| **Display markdown template to stdout** | `legal show <slug>` *(or `legal show <slug> --no-mark`)* |
| **Copy template markdown to project** | `legal copy <slug> [destination_path]` |
| **Copy original .docx source** | `legal docx <slug> [destination_path]` |
| **Substitute placeholders** | `legal fill <slug> --var Key="Value" --out path.md` |
| **Verify system health** | `legal doctor` |
| **Regenerate markdown from docx** | `legal convert` |
| **Sync upstream from general.legal** | `legal fetch` |

---

## 📚 Complete Template Catalog

The library contains 12 core attorney-drafted documents across four domains:

### 1. Commercial Agreements & Corporate Governance

| Slug | Aliases | Title | Use Cases & Description |
| :--- | :--- | :--- | :--- |
| `mutual-nda` | `nda`, `mnda` | **Mutual Non-Disclosure Agreement** | Two-way confidentiality agreement when two companies or founders explore partnerships, investments, technical integrations, or M&A. |
| `one-way-nda` | `1way-nda`, `one-way` | **One-Way Non-Disclosure Agreement** | Unilateral non-disclosure agreement protecting a single disclosing party when sharing proprietary info with contractors, vendors, or evaluators. |
| `advisor-agreement` | `advisor` | **Advisor Agreement** | Engages startup mentors and strategic advisors with stock option vesting, comprehensive IP assignment, and institutional conflict rules. |
| `master-services-agreement` | `msa` | **Master Services Agreement (MSA)** | Enterprise SaaS platform deployment and professional services contract. Covers platform licensing, customer data vs AI inputs/outputs, SLAs, warranties, IP indemnity, and liability caps. |

### 2. Website & Platform Legal

| Slug | Aliases | Title | Use Cases & Description |
| :--- | :--- | :--- | :--- |
| `terms-of-use` | `terms`, `tou` | **Terms of Use** | Public website and SaaS application terms of use. Covers user accounts, acceptable use, IP ownership, liability limits, and dispute resolution. |
| `cookie-notice` | `cookie`, `cookies` | **Cookie Notice** | Public disclosure of tracking cookies, session identifiers, analytics, and third-party advertising tags for websites and web apps. |
| `privacy-policy-us` | `privacy`, `privacy-us` | **Privacy Policy (U.S. Only)** | Privacy policy compliant with U.S. federal and state privacy statutes (including California CCPA/CPRA, Virginia VCDPA, Colorado CPA, etc.). |
| `privacy-policy-gdpr` | `privacy-gdpr`, `gdpr` | **Privacy Policy (GDPR Enhanced)** | Multi-jurisdictional privacy policy covering U.S. state laws plus European Union GDPR, UK GDPR, and Swiss FADP requirements. |

### 3. Privacy, Data Protection & Security

| Slug | Aliases | Title | Use Cases & Description |
| :--- | :--- | :--- | :--- |
| `dpa-us` | `dpa` | **Data Processing Addendum (U.S.)** | Processor-friendly addendum to customer MSAs for processing U.S. personal data under CCPA/CPRA and state privacy regulations. |
| `dpa-global` | `dpa-global` | **Data Processing Addendum (Global)** | Comprehensive international DPA fulfilling EU/UK GDPR Article 28, incorporating 2021 EU Standard Contractual Clauses (SCCs Modules 2 & 3), and UK IDTA. |
| `business-associate-agreement` | `baa` | **Business Associate Agreement (BAA)** | Mandatory HIPAA contract between covered entities (hospitals, healthtech, payers) and business associates handling Protected Health Information (PHI). |

### 4. Employment & Human Resources

| Slug | Aliases | Title | Use Cases & Description |
| :--- | :--- | :--- | :--- |
| `employee-offer-letter` | `offer`, `offer-letter` | **Employee Offer Letter (California Exempt)** | Offer letter for salaried exempt employees in California. Covers base salary, flexible non-accruing vacation, CIIAA integration, and binding arbitration. |

---

## 🔍 How Custom Placeholders Work

In the markdown templates, text that must be customized is wrapped in HTML `<mark>` tags:
```markdown
This Agreement is entered into between <mark>[Company]</mark>, a Delaware corporation ("Company")
and <mark>[Customer]</mark> ("Customer") as of <mark>[Effective Date]</mark>.
```

### Agent Best Practices When Drafting:
1. **Never leave raw `<mark>` tags in final deliverables** provided to the user.
2. Before generating a final contract, run `legal placeholders <slug>` to see all fields that need customization.
3. Replace placeholders with the actual legal names, entities, dates, addresses, and compensation amounts provided by the user.
4. If the user has not provided specific terms, prompt the user for the missing details, or insert standard startup terms while explicitly noting them for user review.

---

## 🛠️ Step-by-Step Autonomous Workflows for Agents

### Workflow 1: Draft an NDA for Two Parties
When the user says: *"Draft an NDA between Acme Corp (Delaware) and Nova AI Inc (California) for exploring a technical partnership"*:

1. Inspect the template overview and placeholders:
   ```bash
   legal info mutual-nda
   legal placeholders mutual-nda
   ```
2. Copy or read the clean markdown template:
   ```bash
   legal show mutual-nda --no-mark
   ```
3. Customize the text:
   - Disclosing / Receiving Parties: "Acme Corp" and "Nova AI Inc"
   - Governing law: Delaware
   - Term: 5 years (standard)
   - Survival: 7 years / perpetual for trade secrets
4. Present the complete, customized contract to the user.

### Workflow 2: Launch Website Terms of Service & Privacy Policy
When the user is building a web app and asks: *"Generate a Terms of Service and Privacy Policy for my new SaaS project called TaskPilot"*:

1. Check requirements (Does TaskPilot serve EU users? If yes, use `privacy-policy-gdpr`; if US only, use `privacy-policy-us`):
   ```bash
   legal info terms-of-use
   legal info privacy-policy-gdpr
   ```
2. Inspect required fields:
   ```bash
   legal placeholders terms-of-use
   legal placeholders privacy-policy-gdpr
   ```
3. Export and customize:
   ```bash
   legal copy terms-of-use ./docs/TERMS.md --no-mark
   legal copy privacy-policy-gdpr ./docs/PRIVACY.md --no-mark
   ```
4. Fill in company contact email, effective date, governing jurisdiction, and specific features.

### Workflow 3: Onboard a Startup Advisor
When the user asks: *"I need an advisor agreement for Jane Doe giving her 0.5% options vesting over 2 years"*:

1. Inspect the template:
   ```bash
   legal info advisor-agreement
   legal placeholders advisor-agreement
   ```
2. Read the template:
   ```bash
   legal show advisor-agreement --no-mark
   ```
3. Tailor Section 1 (Services scope) and Section 2 (Grant: 0.5% options, 2-year monthly vesting).
4. Deliver the completed agreement.

---

## ⚖️ Legal Status & Disclaimer

- **License**: CC0 1.0 Universal (Public Domain Dedication). Free to use, adapt, reproduce, and redistribute for commercial and private purposes without restriction.
- **Credit Footnote**: All templates include an optional General Legal footnote. Retaining it is not a legal obligation under CC0, but is requested by the original authors.
- **Disclaimer**: These templates are provided for general informational and reference purposes only and do not constitute formal legal advice. AI agents and users should advise clients to consult qualified legal counsel for transaction-specific nuances.
