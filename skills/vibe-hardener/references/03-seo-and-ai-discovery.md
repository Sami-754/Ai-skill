# 03. SEO & AI Discoverability Guide

To be indexed by Google and cited by AI engines (ChatGPT, Claude, Perplexity, Gemini AI Overviews), your web app must provide structured metadata, clear crawl policies, and semantic markup.

---

## 1. `robots.txt` Optimized for AI & Search Engines

Create `public/robots.txt` (or `app/robots.ts` in Next.js).
**Critical:** Explicitly welcome AI web scrapers and search bots:

```txt
User-agent: *
Allow: /
Disallow: /api/
Disallow: /admin/
Disallow: /dashboard/
Disallow: /settings/

# Permit AI Search & Overview Crawlers
User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: https://yourdomain.com/sitemap.xml
```

---

## 2. `llms.txt` Standard for LLM Ingestion

The `llms.txt` standard provides LLMs with a clean Markdown directory of your product's capabilities, documentation, and pricing without requiring complex DOM parsing.

Create `public/llms.txt`:
```markdown
# Product Name

> One sentence describing what your product solves.

## Core Features
- Feature A: Description of key workflow
- Feature B: Description of key integration
- Feature C: Description of automation or performance

## Documentation & Links
- [Getting Started](https://yourdomain.com/docs/intro)
- [API Reference](https://yourdomain.com/docs/api)
- [Pricing](https://yourdomain.com/pricing)
- [Privacy Policy](https://yourdomain.com/privacy)
- [Terms of Service](https://yourdomain.com/terms)
```

---

## 3. Dynamic `sitemap.xml`

Next.js App Router (`app/sitemap.ts`):
```typescript
import { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const baseUrl = 'https://yourdomain.com';
  return [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/pricing`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/privacy`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 0.3,
    },
  ];
}
```

---

## 4. Open Graph & Social Sharing Card

Social platforms (Twitter, LinkedIn, Facebook, Slack, iMessage) need a high-res image preview (1200x630 px).

Next.js Metadata (`app/layout.tsx` or per-page):
```typescript
export const metadata = {
  metadataBase: new URL('https://yourdomain.com'),
  title: {
    default: 'BrandName - The Hardened Vibe Platform',
    template: '%s | BrandName',
  },
  description: 'Turn your vibe-coded prototypes into battle-tested SaaS applications.',
  openGraph: {
    title: 'BrandName',
    description: 'Turn your vibe-coded prototypes into battle-tested SaaS applications.',
    url: 'https://yourdomain.com',
    siteName: 'BrandName',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'BrandName Preview',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'BrandName',
    description: 'Turn your vibe-coded prototypes into battle-tested SaaS applications.',
    images: ['/og-image.png'],
    creator: '@yourhandle',
  },
};
```

---

## 5. Schema.org JSON-LD Structured Data

Inject structured data into your landing page `<head>` or root component so search engines understand your entity:
```tsx
export function JsonLd() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "BrandName",
    "operatingSystem": "All",
    "applicationCategory": "BusinessApplication",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "description": "Clear 1-sentence description of the software."
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
```

---

## 6. HTML & Heading Invariants
- Exactly **one `<h1>`** per page (typically the hero headline).
- Use hierarchical `<h2>`, `<h3>` tags without skipping levels.
- Every `<img>` tag **must** have an informative `alt` tag (never empty unless decorative with `aria-hidden="true"`).
- Root `<html>` must declare language attribute (e.g., `<html lang="en">`).
