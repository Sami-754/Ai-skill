# Legal Templates

Attorney-drafted legal templates for startups, SaaS companies, and technology businesses. Created by the attorneys at [General Legal](https://general.legal) and released under [CC0 1.0 Universal](LICENSE). Free for anyone to use, modify, and distribute for any purpose, without attribution.

These templates are provided in LLM-optimized markdown and original .docx formats. Highlighted text (marked with `<mark>` tags in the markdown files) indicates fields that should be customized for your use.

---

## ⚡ Global CLI (`legal` / `legal-templates`)

Use the global terminal command from any project directory:

```bash
# List all available legal templates
legal list

# Inspect template overview and key provisions
legal info mutual-nda

# Inspect all customizable placeholders and fields
legal placeholders advisor-agreement

# Search across all 12 templates for clauses
legal search "arbitration"
legal search "indemnification"

# Display markdown template to stdout
legal show mutual-nda --no-mark

# Copy template markdown to your current workspace
legal copy mutual-nda ./NDA.md --no-mark

# Copy original Word (.docx) file
legal docx mutual-nda ./NDA.docx

# Substitute placeholders
legal fill advisor-agreement --var "[(describe services)]"="Strategic Architecture" --out ./Advisor.md

# Verify library health
legal doctor
```

---

## 📚 Templates Catalog

| Template | Slug | Category | Description |
| :--- | :--- | :--- | :--- |
| [Advisor Agreement](templates/advisor-agreement/) | `advisor-agreement` | Governance | Advisor agreement covering advisory services, equity compensation, IP assignment, and confidentiality |
| [Business Associate Agreement (BAA)](templates/business-associate-agreement/) | `business-associate-agreement` | Privacy & Security | HIPAA-required contract between covered entities and business associates handling PHI |
| [Cookie Notice](templates/cookie-notice/) | `cookie-notice` | Platform Legal | Disclosure of cookie and tracking technology practices for websites and web applications |
| [Data Processing Addendum (U.S.)](templates/dpa-us/) | `dpa-us` | Privacy & Security | Processor-friendly DPA for U.S. personal data with security measures and state-privacy-law compliance |
| [Data Processing Addendum (Global)](templates/dpa-global/) | `dpa-global` | Privacy & Security | Processor-friendly DPA for U.S., EU/EEA, UK, and Switzerland with GDPR-aligned obligations |
| [Employee Offer Letter (California Exempt)](templates/employee-offer-letter/) | `employee-offer-letter` | Employment & HR | Offer letter for California exempt hires covering compensation, exempt-employee policies, and arbitration |
| [Master Services Agreement (MSA)](templates/master-services-agreement/) | `master-services-agreement` | Commercial | Tech-oriented MSA for companies deploying software and providing platform or integration services |
| [Mutual Non-Disclosure Agreement](templates/mutual-nda/) | `mutual-nda` | Commercial | Two-way confidentiality agreement for parties sharing sensitive information while exploring a business relationship |
| [One-Way Non-Disclosure Agreement](templates/one-way-nda/) | `one-way-nda` | Commercial | One-way confidentiality agreement protecting a single disclosing party's information |
| [Privacy Policy (U.S. Only)](templates/privacy-policy-us/) | `privacy-policy-us` | Platform Legal | Privacy policy covering U.S. federal and state privacy laws including CCPA/CPRA |
| [Privacy Policy (GDPR Enhanced)](templates/privacy-policy-gdpr/) | `privacy-policy-gdpr` | Platform Legal | Multi-jurisdictional privacy policy covering both U.S. state laws and GDPR/UK GDPR |
| [Terms of Use](templates/terms-of-use/) | `terms-of-use` | Platform Legal | Website terms of use covering access rights, IP protections, liability limits, and dispute resolution |

---

## Attribution & License

- **License**: Released under [CC0 1.0 Universal](LICENSE) (Public Domain Dedication).
- **Attribution**: These templates include an optional General Legal credit footnote. Retaining that footnote isn't a legal requirement under CC0, but is requested by the authors when reproducing or adapting these documents.
