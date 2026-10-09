# Launch Readiness (LAUNCH)

## Senior mindset

A senior knows that **users experience the product long before they log in, and long after they leave a screen**. The ad, the search result, the landing page, the pricing table, the app store screenshots, the welcome email, the help article and the support reply are all part of the UX. A great app behind a confusing landing page doesn't get adopted, and a great onboarding undone by a broken password-reset email loses users.

At launch, the senior's job changes from "make it better" to **"make sure nothing critical fails, and that we'll know immediately if it does"**. They separate **must-fix** from **nice-to-have** with discipline, and they never let unverified critical flows go out.

## Scope

- **External (around the product):** landing/home page, value proposition and positioning, pricing page, sign-up conversion path from marketing pages, SEO basics and social previews, app store listings (if mobile), docs and help center, support channels and SLAs, status page, legal pages (terms, privacy, cookies, accessibility statement, imprint where required), transactional emails and deliverability, brand consistency across touchpoints, community/social presence, and comparison/migration content.
- **Internal (operational readiness):** critical flow end-to-end verification in production-like conditions, analytics live, error monitoring and alerting, performance on production infrastructure, feature flags and rollback plan, data backups, support team briefed (known issues, macros), and launch-day runbook.
- **Gate:** consolidating every area's P0/P1 and Not-verified items into the verdict (using `severity-and-scoring.md` §7).

## Procedure

### Step 1: Landing page and value clarity
- **5-second test (reasoned or with users):** after 5 seconds, can a visitor say **what it is, who it's for, and what to do next**? The headline states the outcome for the target user (not a slogan); the subheadline explains how; the primary CTA is single and specific ("Start free", "Book a demo") (→ CTX-01).
- Above the fold: headline, subheadline, primary CTA, and a product visual that shows the real product.
- Social proof is real and specific (logos with permission, attributed quotes, numbers with sources) (→ TRUST-06).
- Objection handling: security, pricing, integrations, migration, FAQ.
- Performance of the landing page (→ PERF; LCP matters for both SEO and bounce).
- Mobile landing experience (→ RESP).

### Step 2: Pricing page
- Plans are easy to compare (≤ 3–4 plans; a recommended plan highlighted); the differences are in user terms (outcomes, limits), not internal feature codes.
- Clear prices: currency, tax, billing period, per-seat math, annual vs. monthly toggle with the real totals (→ TRUST-07).
- Free trial / free plan terms clear; "Contact sales" only where it's truly needed.
- FAQ about billing, cancellation and refunds.
- The CTA on each plan leads to the right sign-up path with the plan preselected (intent preserved → FLOW-11).

### Step 3: Conversion path
Trace: ad/search → landing → pricing → sign-up → verification → first value. Check message consistency (the promise on the ad = the headline = the onboarding), the number of steps, and that tracking exists at each step (→ MEAS-02).

### Step 4: Discoverability and sharing
- Unique `<title>` and meta descriptions; canonical URLs; `robots.txt` and `sitemap.xml`; no accidental `noindex` in production; structured data where relevant.
- Open Graph/Twitter cards: title, description and a 1200×630 image for key pages; links shared in Slack, LinkedIn or X look right.
- Favicon and app icons in all required sizes.
- `hreflang` for multi-locale sites (→ I18N-20).

### Step 5: App store listings (if mobile)
- Screenshots that show the real first-run value (→ ONB-19), a clear first line of the description, a privacy nutrition label/data safety section that matches reality, age rating, support URL, and in-app account deletion (app store requirement where account creation exists → TRUST-10).

### Step 6: Help, support and status
- Help center/docs covering the top tasks and top expected problems (from the audit's P1/P2 list and FLOW break points).
- In-app help entry point placed consistently (WCAG 3.2.6 → A11Y-26).
- Support channels and expected response times are stated; the support team is briefed with known issues and macros.
- A status page linked from the app, the footer and error states (→ STATE-22).

### Step 7: Legal and compliance pages
Terms of service, privacy policy, cookie policy (with the consent tool working → TRUST-03), accessibility statement (→ A11Y-33), imprint/legal notice where required (e.g. Germany/Austria), refund policy, DPA/subprocessor list for B2B, and age restrictions. Flag them for legal review; don't judge legal sufficiency.

### Step 8: Transactional emails and notifications
- All lifecycle emails exist and render correctly (welcome, verification, password reset, invite, receipt/invoice, trial ending, payment failed, cancellation confirmation, data export ready, security alerts).
- Deliverability: a sending domain with SPF, DKIM and DMARC; a recognizable sender; plain-text versions; links to the production domain; tested in major clients (Gmail, Outlook, Apple Mail) and in dark mode.
- Content quality → CONT-18.

### Step 9: Operational readiness
- Every **critical flow verified end to end in a production-like environment** (real payment provider in test mode, real email delivery, real SSO), on the device/browser matrix (→ RESP-01).
- Analytics events firing in production (→ MEAS); error monitoring and alerts set (→ STATE-23).
- Load expectations: performance under launch traffic (rate limits produce friendly messages → STATE-21).
- Feature flags for risky features; a **rollback plan**; backups verified.
- A launch-day runbook: owners, monitoring dashboards, a communication plan, and an escalation path.

### Step 10: Consolidate the gate
1. Gather all P0 and P1 findings from every area, and all **Not verified** rows on critical criteria (FLOW, STATE, A11Y, TRUST, FORM on critical flows).
2. Apply the launch gate rules from `severity-and-scoring.md` §7.
3. Produce the verdict with:
   - **Blockers (P0):** each with an owner and estimated effort.
   - **Conditions** (for Conditional Go): P1s with owner and date, and verifications to complete.
   - **Accepted risks:** P2/P3 knowingly deferred.
   - **Launch-week monitoring:** the metrics and thresholds that would trigger a rollback or hotfix.

## Criteria

<!-- BEGIN GENERATED criteria (launch-readiness) -->
<!-- Source: criteria/launch-readiness.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| LAUNCH-01 | Value proposition clear in 5 seconds | Visitor can't tell what, who or next step | S3 |
| LAUNCH-02 | Single, specific primary CTA | Competing CTAs; vague "Learn more" as the primary | S2 |
| LAUNCH-03 | Real product shown | Only abstract illustrations; misleading visuals | S2 |
| LAUNCH-04 | Credible, real social proof | Unattributed or fabricated proof | S2–S3 |
| LAUNCH-05 | Pricing clear and comparable | Hidden totals; confusing plan differences | S3 |
| LAUNCH-06 | Plan intent preserved into sign-up | Plan selection lost | S2 |
| LAUNCH-07 | Message consistency across the funnel | Promise mismatch between ad, landing and onboarding | S2 |
| LAUNCH-08 | SEO and indexing basics | `noindex` in production; missing titles, sitemap or canonical | S2–S3 |
| LAUNCH-09 | Social previews | Missing or broken OG images and titles | S1–S2 |
| LAUNCH-10 | App store listing accurate and compliant | Misleading screenshots; data labels inconsistent; no in-app deletion | S2–S3 |
| LAUNCH-11 | Help content for top tasks and problems | No help, or help that doesn't cover critical flows | S2 |
| LAUNCH-12 | Support channels and expectations | No visible contact or response expectations | S2 |
| LAUNCH-13 | Status page | None linked | S1–S2 |
| LAUNCH-14 | Legal pages present and linked | Missing terms, privacy, cookies or imprint where required | S3 (legal review) |
| LAUNCH-15 | Transactional emails complete and deliverable | Missing lifecycle emails; SPF/DKIM/DMARC not set; broken rendering | S3 |
| LAUNCH-16 | Brand consistency across touchpoints | Different names, logos or tone across site, app and emails | S1–S2 |
| LAUNCH-17 | Critical flows verified in a production-like environment | Not verified end to end | S4 (gate) |
| LAUNCH-18 | Analytics and monitoring live | Not firing in production; no alerts | S2–S3 |
| LAUNCH-19 | Rollback and feature-flag plan | No rollback path | S2–S3 |
| LAUNCH-20 | Launch-day runbook and owners | No owners or monitoring plan | S2 |
| LAUNCH-21 | Gate verdict produced with conditions | No explicit Go/No-Go with reasons | S2 |
<!-- END GENERATED criteria -->

## Code probes

- SEO: `<meta name="robots"`, `noindex`, `robots.txt`, `sitemap`, `metadata = {`, `generateMetadata`, `og:image`, `twitter:card`, `canonical`.
- Legal routes: `terms`, `privacy`, `cookies`, `imprint`, `impressum`, `legal`, `accessibility`.
- Emails: `emails/`, `react-email`, `mjml`, `sendgrid|postmark|resend|ses|mailgun`, template names.
- Status: `status.` links, `statuspage`, `instatus`, `betteruptime`.
- Flags: see MEAS.

## Output

- An external-surface audit table (touchpoint · status · issues).
- An email inventory (email · exists · renders · deliverability).
- An operational readiness checklist.
- **The launch gate decision**: verdict, blockers, conditions, accepted risks, and the launch-week monitoring plan.
- Findings in the standard format; the coverage table (LAUNCH-01 … LAUNCH-21).

## Done when

Every external touchpoint is reviewed, operational readiness is checked, all area P0/P1 and Not-verified critical items are consolidated, and an explicit verdict with conditions is written.
