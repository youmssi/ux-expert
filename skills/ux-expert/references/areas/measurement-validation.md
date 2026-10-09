# Measurement and Validation (MEAS)

## Senior mindset

A senior UX engineer's opinion is a **hypothesis**. Their experience tells them where to look and what probably matters, but the market decides. So they always ask: **"How will we know?"** How will we know the problem is real, that the fix worked, and that we didn't break something else?

They measure at three levels:
1. **Behavior (what users do):** funnels, task completion, time on task, errors, retention.
2. **Attitude (what users feel):** SUS, SEQ, CSAT, qualitative feedback. NPS is used cautiously (it is popular but a weak diagnostic for UX).
3. **Observation (why):** usability tests, session recordings (with privacy safeguards), interviews.

And they distrust vanity metrics (page views, total sign-ups) in favor of **metrics tied to user goals**: activation, task success, time to value, and retention of the core job.

The famous number they keep in mind: **5 users per round** reveal most usability problems for one user group (Nielsen & Landauer). Small, frequent tests beat one large, late study.

## Scope

- **In:** UX metric framework (HEART: Happiness, Engagement, Adoption, Retention, Task success, with goals → signals → metrics), the funnel definition for critical flows, event instrumentation audit (naming, properties, coverage, identity), activation/retention definitions, front-end error and performance monitoring (→ STATE-23, PERF-20), feedback channels (in-app feedback, support tagging), session replay (with masking), usability test plan (tasks, participants, success criteria, script), surveys (SUS, SEQ, UMUX-Lite), experimentation readiness (feature flags, A/B framework, guardrail metrics, sample size), dashboards for UX health, privacy compliance of analytics (→ TRUST-03), and validating the audit's Low-confidence findings.
- **Out:** building dashboards in specific tools; data warehousing.

## Procedure

### Step 1: Define UX goals and metrics (HEART)
For each critical flow/job from CTX, fill:

| Dimension | Goal | Signal | Metric | Current instrumentation |
|---|---|---|---|---|
| Task success | Users schedule their first meeting | `booking_created` after `link_shared` | % of new hosts with a booking within 7 days | ✅/⚠️/❌ |
| Adoption | … | … | … | … |
| Retention | … | … | … | … |
| Engagement | … | … | … | … |
| Happiness | … | … | SEQ after the core task; SUS quarterly | … |

Choose only the dimensions that matter for this product (HEART is a menu, not a requirement).

### Step 2: Instrumentation audit
- Find analytics calls: `track(`, `capture(`, `logEvent(`, `analytics.`, `gtag('event'`, `posthog.`, `mixpanel.`, `amplitude.`.
- Build an **event catalog**: event name · trigger location · properties · user/workspace identity attached.
- Check **coverage of each critical flow**: every step has an event (start, each step, completion, error, abandonment), so funnels can be built.
- Check **quality:** consistent naming convention (e.g. `object_action` in snake_case: `invoice_created`), no PII in event properties (emails, names) unless deliberate and compliant, properties that enable segmentation (plan, platform, locale, role), client vs. server events (server for reliability of critical conversions), and identity stitching (anonymous → identified).
- Check **error events**: are UX errors (validation failures, failed submissions, empty search results) tracked? These are the friction signals.

### Step 3: Monitoring
- Front-end error monitoring (Sentry etc.) with release tagging and source maps.
- Real-user performance monitoring (web-vitals).
- Alerting on critical-flow error spikes (sign-up, payment).

### Step 4: Qualitative channels
- In-app feedback widget (contextual: "Was this helpful?" on key screens or after tasks).
- Support ticket tagging by UX area.
- Session replay, if used, with **input masking** and consent compliance.
- A recurring user-interview cadence (recommendation).

### Step 5: Usability test plan (always produce one)
Using the audit's top risks (P0/P1 and Low-confidence findings), write:
- **Objectives:** the questions to answer.
- **Participants:** 5 per key segment per round (from CTX); screener criteria.
- **Method:** moderated remote (think-aloud) for discovery; unmoderated for scale; first-click tests for navigation (IA); tree tests for IA; 5-second tests for landing/value clarity.
- **Tasks:** realistic scenarios, not instructions ("You need to meet Ana next week. Use the link she sent you to book a time"), each with a **success criterion** and the related findings.
- **Metrics per task:** success (binary or graded), time on task, errors, SEQ (1–7) after each task; SUS at the end.
- **Script outline:** intro and consent, warm-up questions, tasks, debrief.
- **Analysis plan:** severity rating of observed issues and mapping back to audit findings (confirm/refute).

### Step 6: Experimentation readiness
- Feature flags (`launchdarkly`, `growthbook`, `unleash`, `statsig`, `posthog` flags, homemade).
- A/B testing capability; a defined **primary metric**, **guardrail metrics** (e.g. error rate, support contacts, refunds) and **minimum detectable effect**; awareness of required sample sizes (low-traffic products should prefer qualitative validation and before/after comparisons over underpowered A/B tests).
- Pre-registration discipline: hypothesis, metric and duration decided before starting; no peeking-driven stopping.

### Step 7: Convert audit findings into hypotheses
For each P0/P1 finding, write: **"We believe that <change> for <users> will result in <outcome>. We'll know when <metric> moves from <baseline> to <target>, measured by <method>."** Low-confidence findings get a **validation method** instead of a fix.

## Criteria

<!-- BEGIN GENERATED criteria (measurement-validation) -->
<!-- Source: criteria/measurement-validation.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| MEAS-01 | UX goals and metrics defined | No defined success metrics for critical jobs | S2 |
| MEAS-02 | Critical-flow funnel instrumented | Missing step, completion or error events | S2–S3 |
| MEAS-03 | Activation and retention measurable | No activation event; no cohort capability | S2 |
| MEAS-04 | Event naming and property consistency | Inconsistent names; missing segmentation properties | S1–S2 |
| MEAS-05 | No PII leakage in analytics | Emails/names in event properties or URLs sent to analytics | S3 (→ TRUST) |
| MEAS-06 | Friction signals tracked | Validation errors, failed submits, zero-results not tracked | S2 |
| MEAS-07 | Error monitoring with releases | No front-end error monitoring | S2 |
| MEAS-08 | Real-user performance monitoring | No field vitals | S1–S2 |
| MEAS-09 | Qualitative feedback channels | No in-app feedback; no support tagging | S2 |
| MEAS-10 | Session replay privacy-safe (if used) | Unmasked inputs; no consent | S3 |
| MEAS-11 | Usability testing practice | No testing before launch on critical flows | S2–S3 (pre-launch) |
| MEAS-12 | Attitudinal benchmark | No SUS/SEQ/CSAT baseline | S1 |
| MEAS-13 | Experimentation readiness | No flags; no way to roll out safely | S1–S2 |
| MEAS-14 | Guardrail metrics | Experiments or launches without guardrails | S2 |
| MEAS-15 | Analytics consent compliance | Tracking without required consent | S3 (→ TRUST-03) |
| MEAS-16 | UX health dashboard | No shared view of UX metrics | S1 |
| MEAS-17 | Findings converted to testable hypotheses | Fixes shipped without success criteria | S1–S2 |
<!-- END GENERATED criteria -->

## Output

- The HEART (or chosen framework) table.
- The event catalog, with a coverage map per critical flow (step → event → ✅/❌).
- The proposed tracking plan for missing events (name, trigger, properties).
- The usability test plan (ready to run).
- A hypothesis list for P0/P1 findings.
- Findings in the standard format; the coverage table (MEAS-01 … MEAS-17).

## Done when

Every critical flow has a funnel coverage map, a tracking plan exists for gaps, a usability test plan is ready, and every P0/P1 finding from the audit has a measurable hypothesis or a validation method.
