# Performance and Perceived Speed (PERF)

## Senior mindset

To a senior UX engineer, **speed is a feature and the first impression of quality**. Users don't measure milliseconds. They feel **waiting, uncertainty and jank**. So the senior works on two levers:
1. **Actual speed:** fewer bytes, fewer round trips, less main-thread work, and smarter caching.
2. **Perceived speed:** acknowledge instantly, show progress honestly, show content progressively, never block on what isn't needed, and do work before the user asks (prefetch) or after they leave (background).

Their thresholds come from human perception (0.1 s / 1 s / 10 s; the Doherty threshold of 400 ms) and from Core Web Vitals measured at the **75th percentile of real users**, on **real devices**: a mid-range Android phone on a 4G connection, not the developer's MacBook on fiber.

## Scope

- **In:** Core Web Vitals (LCP, INP, CLS) plus TTFB/FCP, interaction latency for critical actions, JS/CSS/image/font weight, render strategy (SSR/SSG/streaming/CSR), data waterfalls, caching and revalidation, optimistic UI, skeletons, prefetching, list virtualization, heavy-page behavior, animation smoothness (60 fps), mobile app cold start and frame drops, CLI/API latency (light), and performance budgets in CI.
- **Out:** loading state design and content (→ STATE), animation design (→ INT), backend scaling (only as it surfaces to users).

## Procedure

### Step 1: Define budgets from context
Use CTX (devices, networks, frequency) to set budgets. Defaults:
- LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (p75, mobile).
- Critical interactions: visual acknowledgement ≤ 100 ms; result ≤ 1 s, or a progress indicator.
- JS shipped for the first route: aim ≲ 150–200 KB compressed for mobile-first consumer products (a commonly used budget, not a standard; adjust by audience).
- Mobile app cold start: ≲ 2 s to first meaningful screen on mid-range devices.

### Step 2: Measure (if runtime is available)
- Lighthouse (mobile profile) on critical routes; record LCP, CLS, TBT (lab proxy for INP), and the opportunities list.
- Playwright with CPU throttling (4×) and network throttling (Fast 3G / Slow 4G) to time critical interactions: click → visual response → completion.
- Field data if available: CrUX, `web-vitals` library reports, RUM tools (Vercel Analytics, Datadog RUM, SpeedCurve, Sentry performance).
- Bundle analysis: `next build` output, `webpack-bundle-analyzer`, `source-map-explorer`, `vite-bundle-visualizer`.

### Step 3: Static analysis (always)
- **Bundle:** large dependencies (moment, lodash full import, chart libraries, editors, icon packs imported wholesale), missing code splitting (`dynamic(`, `lazy(`, `import(`), and client components that could be server components.
- **Images:** modern formats (AVIF/WebP), responsive `srcset`/`sizes`, explicit dimensions, `loading="lazy"` below the fold, `fetchpriority="high"` / priority on the LCP image, and a CDN.
- **Fonts:** subset, preload critical fonts, `font-display`, and the number of families and weights (→ TYP).
- **Data fetching:** sequential `await`s that could be parallel (waterfalls); fetch in `useEffect` after render (client waterfall) vs. server or route loaders; N+1 requests in lists; missing caching (SWR/React Query `staleTime`, HTTP cache headers, CDN).
- **Rendering:** rendering huge lists without virtualization (`react-window`, `@tanstack/virtual`, `FlatList` misused); expensive re-renders (context providers re-rendering everything, missing memoization on hot paths); layout thrash.
- **Third-party scripts:** tag managers, chat widgets, A/B tools and analytics loading synchronously in `<head>`, blocking the main thread.
- **Layout stability:** see LAY-15; ads, embeds and banners injected above content.

### Step 4: Perceived-performance techniques (check presence and fit)
- **Instant acknowledgement** (pressed states, optimistic updates).
- **Skeletons** shaped like content for > 1 s loads; **no spinners for < ~300 ms** operations (a flash of spinner feels slower; delay showing it ~200–300 ms).
- **Progressive rendering / streaming** (SSR streaming, Suspense boundaries, streamed AI responses).
- **Prefetching** of likely next routes (link prefetch on hover/viewport) and data.
- **Background processing** with notification for long jobs; users are never stuck watching a progress bar for minutes.
- **Stale-while-revalidate** so returning views show cached content instantly.
- **Pagination / infinite scroll with stable placeholders.**

### Step 5: Map to user impact
For each performance issue, write the user consequence on a critical flow: "On mid-range Android, the dashboard LCP is ~5.8 s (measured, Lighthouse mobile), so the first impression after login is a blank screen for about 6 s."

## Criteria

| ID | Criterion | Threshold / fail signal | Default severity |
|---|---|---|---|
| PERF-01 | LCP on critical routes | > 2.5 s (p75 mobile) needs improvement; > 4 s poor | S2 (needs improvement) / S3 (poor) |
| PERF-02 | INP / interaction latency | > 200 ms needs improvement; > 500 ms poor | S2 / S3 |
| PERF-03 | CLS | > 0.1 / > 0.25 | S2 / S3 |
| PERF-04 | TTFB / server response | Consistently > ~800 ms | S2 |
| PERF-05 | Critical action feedback timing | No acknowledgement within 100 ms; no result or progress within 1 s | S2–S3 |
| PERF-06 | JavaScript weight | Far over budget; no code splitting; heavy libraries for small features | S2 |
| PERF-07 | Image optimization | Unoptimized formats or sizes; no lazy loading; LCP image lazy-loaded | S2 |
| PERF-08 | Font loading | Render-blocking fonts; many weights; no subsetting | S1–S2 |
| PERF-09 | Data waterfalls | Sequential independent requests; client-only fetch for initial content | S2 |
| PERF-10 | Caching and revalidation | Every navigation refetches everything; no cache headers | S2 |
| PERF-11 | Large lists virtualized/paginated | Rendering thousands of DOM nodes | S2–S3 |
| PERF-12 | Third-party script cost | Synchronous third parties blocking render or interaction | S2 |
| PERF-13 | Perceived-speed patterns present | No skeletons, no optimistic UI, spinner flashes | S2 |
| PERF-14 | Long tasks off the critical path | Users blocked during long processing; no background option | S2–S3 |
| PERF-15 | Prefetching likely next steps | Obvious next steps not prefetched (light) | S1 |
| PERF-16 | Smooth animation and scrolling | Jank; animating layout properties (`top`, `width`) instead of `transform`/`opacity` | S1–S2 |
| PERF-17 | Low-end device and slow-network behavior | Unusable on mid-range mobile or 3G | S3 (if audience includes them) |
| PERF-18 | Mobile app start and frame rate | Cold start > ~2–3 s; frequent dropped frames | S2–S3 |
| PERF-19 | Performance budgets enforced | No budgets or CI checks (Lighthouse CI, size-limit, bundlesize) | S1–S2 |
| PERF-20 | Real-user monitoring | No field data on vitals | S1–S2 (→ MEAS) |

## Code probes

- Code splitting: `dynamic\(`, `React.lazy`, `import\(`, `loadable`.
- Heavy imports: `from ['"]moment['"]`, `from ['"]lodash['"]` (full), `import \* as Icons`, `chart.js`, `monaco`, `@mui/icons-material['"]$`.
- Images: `<img(?![^>]*(loading|width))`, `next/image` with `priority`, `fetchpriority`.
- Fetch in effects: `useEffect\([^)]*fetch\(` / `useEffect` + `axios.`.
- Waterfalls: consecutive `await fetch` / `await db.` lines that don't depend on each other.
- Virtualization: `react-window`, `react-virtuoso`, `@tanstack/react-virtual`, `FlatList`, `RecyclerView`.
- Third parties: `<script src=` in `_document`/`layout`/`index.html` without `async`/`defer`; `next/script` `strategy`.
- Budgets: `size-limit`, `bundlesize`, `lighthouserc`, `@lhci`.
- RUM: `web-vitals`, `reportWebVitals`, `@vercel/speed-insights`, `datadogRum`.

## Output

- A metrics table per critical route (lab and field where available, with device/network profile).
- An interaction latency table for critical actions.
- A top opportunities list with estimated user impact.
- Findings in the standard format; the coverage table (PERF-01 … PERF-20).

## Done when

Critical routes have measured (or explicitly Not verified) vitals, static analysis covers bundle, images, fonts, data and third parties, and each issue is tied to a user consequence.
