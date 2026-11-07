# 02. UX & Functional Completeness Guide

Vibe-coded prototypes look great on the happy path, but they break immediately when:
1. A user enters an invalid URL.
2. An API request takes 2 seconds to load.
3. A list or database query returns 0 items.
4. A mobile user on an iPhone opens the site.
5. An account needs to be deleted or a password reset.
6. A new user lands on a blank dashboard with no onboarding guidance.

Use this guide to implement the missing 20% of UX that makes an app feel 100% real.

---

## 1. Custom 404 (Not Found) Experience

Never show a raw browser error or a default framework 404.
- Provide a clean, friendly illustration or message.
- Offer actionable next steps: "Go to Dashboard", "Return Home", or a Search bar.
- Next.js App Router: `app/not-found.tsx`
```tsx
import Link from "next/link";

export default function NotFound() {
  return (
    <main className="min-h-[70vh] flex flex-col items-center justify-center text-center px-4">
      <span className="text-sm font-semibold tracking-wide text-primary uppercase">404 Error</span>
      <h1 className="mt-2 text-4xl font-bold tracking-tight text-foreground sm:text-5xl">Page not found</h1>
      <p className="mt-4 text-base text-muted-foreground">Sorry, we couldn’t find the page you’re looking for.</p>
      <div className="mt-8 flex gap-4">
        <Link href="/" className="rounded-lg bg-primary px-5 py-2.5 text-sm font-medium text-white shadow hover:opacity-90">
          Back to Home
        </Link>
        <Link href="/support" className="rounded-lg border px-5 py-2.5 text-sm font-medium hover:bg-muted">
          Contact Support
        </Link>
      </div>
    </main>
  );
}
```

---

## 2. Skeleton Loaders & Loading States

A blank screen during data fetching makes users think the app crashed.
- Add `app/loading.tsx` or skeleton card components.
- Use pulsating placeholders matching the exact card/row geometry:
```tsx
export function SkeletonCard() {
  return (
    <div className="rounded-xl border p-6 space-y-4 animate-pulse">
      <div className="h-6 w-1/3 bg-muted rounded"></div>
      <div className="h-4 w-full bg-muted rounded"></div>
      <div className="h-4 w-2/3 bg-muted rounded"></div>
      <div className="h-10 w-28 bg-muted rounded mt-4"></div>
    </div>
  );
}
```

---

## 3. Empty States (0 Items Found)

When a table, inbox, or list has no records:
- Do NOT show an empty white box or broken table headers.
- Include:
  1. Contextual icon or illustration.
  2. Friendly message ("No projects yet").
  3. Clear Primary CTA ("Create your first project").

```tsx
export function EmptyState({ onAction }: { onAction: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center border-2 border-dashed rounded-xl">
      <div className="p-3 bg-muted rounded-full mb-3">📁</div>
      <h3 className="font-semibold text-lg">No projects created yet</h3>
      <p className="text-muted-foreground text-sm max-w-sm mt-1 mb-4">
        Get started by creating your first project workspace.
      </p>
      <button onClick={onAction} className="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium">
        + Create Project
      </button>
    </div>
  );
}
```

---

## 4. Form Validation & Error States

- Inline error messages directly underneath each invalid input (never generic toast/alert popups).
- Red border highlight with high contrast text.
- Form inputs must include `aria-invalid="true"` and `aria-describedby="field-error"` for accessibility.
- Prevent duplicate submits by disabling the submit button and showing a spinner during in-flight requests.

---

## 5. Mobile Layout & Sticky CTA

- Ensure all buttons have at least **48x48px** touch target area.
- Verify viewport `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- **Sticky Mobile CTA:** On landing pages, mobile users frequently scroll past the hero. Add a fixed bottom bar:
```tsx
<div className="fixed bottom-0 left-0 right-0 p-4 bg-background/90 backdrop-blur border-t md:hidden z-50">
  <Link href="/signup" className="w-full flex items-center justify-center py-3 bg-primary text-white font-medium rounded-lg shadow">
    Get Started Free
  </Link>
</div>
```

---

## 6. Real Authentication Lifecycle

Vibe-coded apps often stop at a mock login button. A production app requires:
1. **Real Login & Logout:** Complete session invalidation and cookie clearing on logout.
2. **Password Reset Flow:** Dedicated `/forgot-password` and `/reset-password` routes with secure, time-limited token exchange.
3. **Email Verification:** Block access to sensitive dashboard features until the user confirms their email address via confirmation link or OTP.

---

## 7. First-Run Onboarding Flow

Don't drop a brand-new user into a completely blank, confusing screen:
- Present a lightweight 3-step setup checklist or interactive modal.
- Guide the user to their first "aha!" moment (e.g., connect database, create first document, invite a teammate).
- Allow dismissing or skipping the onboarding tour at any time.

---

## 8. Database Backups & Recovery Plan

- Enable automated daily database backups in Supabase / Neon / RDS.
- Perform at least one manual restore test to verify that backup snapshots actually restore cleanly without data corruption.
- Enable Point-In-Time Recovery (PITR) for mission-critical production data.

---

## 9. Account Deletion & Data Export (GDPR / Apple App Store Mandatory)

Any application storing user accounts must allow users to delete their account:
- Provide a "Danger Zone" in Account Settings (`/settings/account`).
- Two-step confirmation (modal requiring typing "DELETE" or entering password).
- Clean up related rows via database cascading deletes (`ON DELETE CASCADE`).
- Provide a "Download My Data" button exporting JSON/CSV archives of the user's data.
