# States and Resilience (STATE)

## Senior mindset

Designers present the **ideal state**: perfect data, fast network, the right permissions, short names. Real users live in the other states most of the time. A senior's reflex for every screen is the **state matrix**: "Show me this screen with **nothing**, with **one** item, with **10,000** items, while **loading**, when it **fails**, when **offline**, when the user **may not** see it, and when someone else **changed it**."

They know that **trust is built or destroyed in failure states**. A product that fails gracefully (clear message, data kept, a path forward) is perceived as more reliable than one that fails rarely but catastrophically. This is the peak–end rule: people remember the worst moment.

They also treat **empty states as onboarding real estate**. ChatGPT's empty conversation isn't blank: it shows suggested prompts. An empty project list in a good product explains the value and offers a single "Create your first …" action, plus a template or sample data.

## Scope

- **In:** per-screen state matrix (ideal, empty-first-use, empty-cleared, empty-no-results, loading-initial, loading-incremental, partial, error, offline, slow, timeout, permission-denied, not-found, rate-limited, conflict, stale), extreme content (long, zero, huge counts, special characters), error boundaries, crash prevention, data-loss prevention, autosave, undo/soft delete, retry, recovery paths, session expiry, maintenance/degraded mode.
- **Out:** wording of messages (→ CONT, but missing content is a STATE issue), visual design of spinners (→ INT), performance numbers (→ PERF).

## Procedure

### Step 1: Build the state matrix
For each critical-flow screen and each data-driven component:

| Screen/component | Ideal | Empty (first use) | Empty (no results/cleared) | Loading (initial) | Loading (refresh/paginate) | Partial | Error | Offline | Permission denied | Not found | Conflict/stale |
|---|---|---|---|---|---|---|---|---|---|---|---|

Mark each cell: ✅ designed and implemented · ⚠️ generic or weak · ❌ missing (blank, crash, infinite spinner, raw error) · N/A.

Trace in code how each data fetch handles its outcomes: `isLoading`/`isError`/`data?.length === 0` branches, `Suspense` fallbacks, `ErrorBoundary`, `error.tsx`, `try/catch` around fetches. **An unhandled branch usually means a blank area or a crash.**

### Step 2: Empty states
Three different empties need different content:
- **First use:** explain the value, provide one primary action, and offer a template, sample data or import.
- **No results (search/filter):** echo the query and filters, offer to clear filters, suggest corrections, and show near matches.
- **Cleared (user finished everything, e.g. inbox zero):** positive confirmation; no call to action needed.

### Step 3: Loading states
- **Initial load:** a skeleton matching the final layout for content areas (reduces perceived wait and layout shift); a spinner only for small, unknown-shape areas.
- **Incremental:** keep existing content visible while refreshing (stale-while-revalidate); show inline progress; never blank the screen to refetch.
- **Button-level:** a loading state on the triggering control.
- **Long tasks:** progress and the ability to leave and come back (background jobs, with a notification on completion).
- **No infinite spinners:** every loading state has a timeout path to an error with retry.

### Step 4: Error states
For every fetch and mutation, check:
- Is the error **caught**? (Look for unhandled promise rejections, empty `catch {}`, and `console.error` only.)
- Is it **shown** where the user is looking (inline or near the action), not only as a console log or an easily-missed toast?
- Does it say **what happened, why (if known), and what to do**? Is there a **Retry** action?
- Is the user's **input preserved**?
- Are errors **differentiated**? Network vs. validation vs. permission vs. not found vs. server vs. rate limit (429 with a "try again in X" message) vs. payment (decline reason).
- Is there an **error boundary** so one component's crash doesn't produce a white screen for the whole app? Is there a global fallback with a reload and support link?
- Are errors **logged/monitored** (Sentry, etc.) so the team learns about them? (→ MEAS)

### Step 5: Network and session resilience
- **Offline:** detection (`navigator.onLine`, failed requests), a non-blocking banner, queued writes or a clear "not saved" state, and auto-recovery when back online.
- **Slow network:** test with throttling (Slow 3G or Fast 3G). Do timeouts and skeletons behave? Do double submissions happen?
- **Session expiry:** before expiry, warn (if there's a timeout) and allow extension (WCAG 2.2.1). After expiry, re-authenticate **in place**, preserving unsaved work and returning to the same place.
- **Concurrency:** two tabs or two users editing. Detect conflicts (version/ETag), show who changed what, and offer merge or overwrite choices; never silently lose either edit.
- **Stale data:** a "last updated" indicator for real-time-critical data; auto-refresh or a refresh affordance.

### Step 6: Extreme content (break-the-layout tests)
Test or reason through, with real component code:
- Very long names, titles and emails (60+ characters, no spaces), long translations (→ I18N).
- Zero, one, many (1,000+ items: does it paginate or virtualize? → DATA/PERF).
- Huge numbers (1,234,567,890.12), negative numbers, zero values, null/undefined fields ("undefined" or "NaN" shown to users).
- Special characters, emoji, RTL text in user content, HTML-like input (should be escaped, never rendered).
- Missing images or avatars (fallback initials or placeholder), broken external embeds.
- Time edge cases: time zones, DST transitions, "0 minutes ago", dates far in the past or future.

### Step 7: Data-loss prevention and recovery
- **Autosave** for content creation (docs, long forms, editors) with a visible saved status ("Saved", "Saving…", "Offline: changes saved locally").
- **Unsaved-changes guard** on navigation away (`beforeunload` / router guard) when autosave doesn't exist.
- **Undo** over confirmation for reversible actions; **soft delete with a trash/restore period** for important objects.
- **Destructive bulk actions:** state the scope clearly ("Delete 248 items"), and type-to-confirm for irreversible high-impact actions (deleting a workspace).
- **Export / backup** paths for user data.

### Step 8: Degraded and maintenance modes
- A planned maintenance message, read-only mode, a status page link, and feature-flag fallbacks when third-party services fail (payment provider down, AI provider down → AI).

## Criteria

<!-- BEGIN GENERATED criteria (states-resilience) -->
<!-- Source: criteria/states-resilience.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| STATE-01 | State matrix complete for critical screens | Matrix | Any ❌ on a critical screen | S2–S4 (by state) |
| STATE-02 | First-use empty states guide action | Content of first-use empties | Blank area or "No data" only | S2–S3 |
| STATE-03 | No-results states help recovery | Search/filter empties | No query echo, no clear-filters option | S2 |
| STATE-04 | Loading is shown and shaped | Skeletons, spinners, button loading | Blank screens; layout jumps | S2 |
| STATE-05 | No infinite loading | Timeouts lead to an error | Spinner forever on failure | S3 |
| STATE-06 | Refresh keeps content | Stale-while-revalidate | Content blanks on refetch | S2 |
| STATE-07 | All errors caught and shown | Fetch/mutation error branches | Empty catch; console-only errors; silent failure | S3–S4 |
| STATE-08 | Errors actionable | Message + reason + action + retry | Generic messages, no retry | S2–S3 |
| STATE-09 | Errors differentiated | Network/permission/validation/server/rate-limit | One generic message for all | S2 |
| STATE-10 | Error boundaries | Component and route-level boundaries | White screen on a component crash | S3–S4 |
| STATE-11 | Offline handling | Detection, banner, queued or flagged writes | Silent failure offline; data lost | S2–S3 (S3+ for mobile/field apps) |
| STATE-12 | Session expiry is graceful | Re-auth in place, work preserved, warnings | Redirect to login and lose work | S3 |
| STATE-13 | Concurrency conflicts handled | Versioning, conflict UI | Last write silently wins over another user's work | S3 |
| STATE-14 | Extreme content safe | Long, zero, huge, null, special characters, missing media | Broken layout; "undefined"/"NaN"/"null" shown | S2 |
| STATE-15 | Large data sets scale | Pagination, virtualization, limits | Freezes or crashes with large data | S3 (→ PERF, DATA) |
| STATE-16 | Autosave / unsaved-changes guard | Autosave or a navigation guard | Work lost on navigation | S3 |
| STATE-17 | Undo / soft delete | Undo for reversible actions; trash for important objects | Irreversible delete with no confirmation | S4 |
| STATE-18 | Destructive scope clarity | Counts and names in confirmations; type-to-confirm for critical | "Are you sure?" with no specifics | S2–S3 |
| STATE-19 | Permission-denied states | Explain why and how to get access | Blank, or a raw 403 | S2 |
| STATE-20 | Not-found states | Helpful 404 for objects and routes | Crash or blank on a missing object | S2 |
| STATE-21 | Rate limit / quota states | Clear limit, reset time, upgrade or wait path | Raw 429 or generic error | S2 |
| STATE-22 | Third-party failure fallbacks | Payment, auth, maps, AI provider failures handled | Whole page fails when a third party fails | S2–S3 |
| STATE-23 | Error monitoring exists | Sentry/Datadog/etc. wired to front-end errors | Errors invisible to the team | S2 (→ MEAS) |
<!-- END GENERATED criteria -->

## Code probes

- Empty catch: `catch\s*(\(\s*\w*\s*\))?\s*\{\s*\}`; `.catch\(\(\)\s*=>\s*\{\s*\}\)`; `.catch\(console\.error\)`.
- Fetch states: `isLoading|isPending|isFetching|isError|error\b|status ===`.
- Boundaries: `ErrorBoundary`, `componentDidCatch`, `error.tsx`, `errorElement`, `onError`.
- Empty: `length === 0`, `!data`, `EmptyState`, `No results`, `No data`.
- Offline: `navigator.onLine`, `addEventListener\(['"]online`, `NetInfo`.
- Unsaved guard: `beforeunload`, `useBlocker`, `usePrompt`, `onBeforeRouteLeave`.
- User-visible nulls: template interpolation of possibly-undefined values, e.g. `{user.name}` with no fallback, `toFixed` on undefined.
- Monitoring: `Sentry.init`, `@sentry/`, `datadog`, `bugsnag`, `rollbar`, `logrocket`.

## Gotchas

- TanStack Query v5 keeps previous data only with `placeholderData: keepPreviousData`. Check the options before flagging STATE-06.
- Next.js `error.tsx` catches render errors in its segment, not errors thrown in event handlers or async callbacks.
- A `catch` that only reports to Sentry is visible to the team but silent for the user. Report it against STATE-07.
- Suspense fallbacks may never render when data is prefetched. Confirm loading states at runtime when you can.

## Output

- A state matrix per critical screen.
- An error-handling coverage summary (fetches/mutations: handled vs. unhandled).
- Extreme-content test results.
- Findings in the standard format; the coverage table (STATE-01 … STATE-23).

## Done when

Every critical screen has a state matrix, every data fetch/mutation on critical flows has a verified error path, and the extreme-content, offline and session tests are done or marked Not verified.
