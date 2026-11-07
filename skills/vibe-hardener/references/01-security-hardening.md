# 01. Security & Backend Hardening Guide

Vibe-coded prototypes frequently fall victim to automated vulnerability scanners within hours of going live. Use these patterns and checklists to ensure zero leaks, bulletproof database access, and secure authentication.

---

## 1. Secrets & Git Hygiene

### The Rule
- **NEVER** commit `.env`, `.env.local`, `.env.production`, or private key files (`*.pem`, `*.key`) to version control.
- Ensure your root `.gitignore` contains:
```gitignore
# Environment files
.env
.env*.local
.env.development
.env.test
.env.production
*.pem
*.key
```

### Git History Remediation
If an API key or `.env` file was accidentally committed in a past git commit:
```bash
# 1. Immediately revoke and regenerate the compromised key in your provider dashboard
# 2. Remove the file from git tracking without deleting it locally:
git rm --cached .env
git commit -m "chore: stop tracking .env"
```

---

## 2. Supabase & PostgreSQL Row Level Security (RLS)

### Critical Vibe-Code Flaw:
Vibe coders create tables in Supabase and forget to enable RLS. Anyone with the public `anon` key can read, modify, or truncate the entire database!

### Remediation:
Always enable RLS on every table:
```sql
-- 1. Enable RLS on every table
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;

-- 2. Strict User Isolation Policy (Users can only read/write their own records)
CREATE POLICY "Users can view own profile"
ON profiles FOR SELECT
USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
ON profiles FOR UPDATE
USING (auth.uid() = id);

-- 3. Document Policy with Ownership Check
CREATE POLICY "Users can manage their own documents"
ON documents FOR ALL
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

---

## 3. Frontend Trust vs Backend Verification

### Critical Vibe-Code Flaw:
Accepting `userId` directly from client request bodies (e.g., `POST /api/delete-item` with `{ userId: "123", itemId: "456" }`). Any malicious user can pass another user's ID!

### Remediation:
Derive identity **strictly** from the verified session / auth token on the server:
```typescript
// Next.js Route Handler / Express
import { createServerClient } from '@supabase/ssr' // or Clerk/Auth.js

export async function POST(req: Request) {
  const supabase = createClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 })
  }

  // Use user.id strictly from the verified session, NOT req.json()
  const { itemId } = await req.json()
  await db.items.delete({ where: { id: itemId, userId: user.id } })
}
```

---

## 4. Input Validation with Zod

Every API route accepting user input must validate schema before processing:
```typescript
import { z } from "zod";

export const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(2).max(100).trim(),
  age: z.number().int().min(13).max(120).optional(),
});

// In API Route:
const result = CreateUserSchema.safeParse(await req.json());
if (!result.success) {
  return new Response(JSON.stringify({ errors: result.error.flatten() }), { status: 400 });
}
```

---

## 5. Rate Limiting (Upstash / Arcjet / Memory)

Prevent brute force, API abuse, and runaway LLM billing:
```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(20, "1 m"), // 20 requests per minute
});

export async function rateLimitCheck(identifier: string) {
  const { success, limit, remaining, reset } = await ratelimit.limit(identifier);
  if (!success) {
    throw new Error("Too many requests. Please slow down.");
  }
}
```

---

## 6. Webhook Signature Verification

Never process webhooks without cryptographic signature verification (Stripe, Clerk, LemonSqueezy):
```typescript
// Stripe Webhook Example
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: Request) {
  const body = await req.text();
  const sig = req.headers.get("stripe-signature");

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(body, sig!, process.env.STRIPE_WEBHOOK_SECRET!);
  } catch (err: any) {
    return new Response(`Webhook Error: ${err.message}`, { status: 400 });
  }

  // Safely handle event
}
```

---

## 7. Security Headers & CORS

Ensure strict headers in `next.config.js` or server middleware:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
- Never set CORS origin to `*` for authenticated or state-altering API routes.
