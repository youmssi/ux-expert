# Flows and Friction (FLOW)

## Senior mindset

Junior designers review **screens**. Seniors review **transitions**: what the user knows, wants and holds in their head **between** screens. Almost every severe UX failure happens at a seam: after a redirect, after an email link, after an error, after a timeout, after switching devices.

A senior reads a flow like an engineer reads a hot code path: **count the operations, find the slowest one, and remove anything that isn't necessary**. Their order of operations is always:
1. **Remove** steps (the best step is no step: infer, default, defer, automate).
2. **Merge** steps (ask for related things together).
3. **Reorder** (value before effort; easy before hard; commitment escalates gradually).
4. Only then **redesign** the remaining steps.

Cal.com's booking flow is a good model. The guest never creates an account, the time zone is detected rather than asked, and the date and time are chosen on one screen. The flow is **defined by what was removed**.

## Scope

- **In:** every critical flow from CTX (sign-up, onboarding, core job, payment, sharing, recovery, cancellation/deletion), step and decision counts, input burden, seams (emails, redirects, OAuth, payment providers, device switches), interruption and resumption, drop-off risks, redundant work, flow-level error recovery.
- **Out:** detailed field-level form design (→ FORM), state visuals (→ STATE), copy wording (→ CONT). Reference them; don't re-audit them.

## Procedure

### Step 1: Get the flow list
Take the critical flows from the CTX context brief. If CTX did not run, derive them from routes plus the standard list: sign-up/install, first value, core job, payment/upgrade, invite/share, password reset, cancel/delete/export.

### Step 2: Trace each flow from code and/or runtime
For each flow, build a **step table**:

| # | Screen / route / file | User intent | User action(s) | Inputs required | Decisions | System response & latency | Feedback shown | Possible failures | Exit/back |
|---|---|---|---|---|---|---|---|---|---|

- Follow the actual code path: route → component → submit handler → API → redirect target. Note **every redirect** (`redirect(`, `router.push`, `navigate(`, `window.location`) and every **external hop** (email, OAuth, Stripe, 3-D Secure, SMS).
- If runtime is available, actually perform the flow (Playwright or browser), and record screenshots and timings.

### Step 3: Compute flow metrics
- **Steps:** the number of distinct screens or states the user must pass.
- **Interactions:** clicks, taps and keystrokes on the happy path (a rough KLM-style count: each field ≈ 1 click + typing; each choice ≈ 1 click).
- **Decisions:** the number of points where the user must choose. Weight decisions with more than 5 options as heavier (Hick's law).
- **Inputs:** the number of fields, and how many could be inferred, defaulted or deferred.
- **Memory load:** any information the user must carry from one step to another (codes, names, earlier choices).
- **Seams:** context switches (another app, email, another device, another tab).
- **Time to value:** steps before the user receives the first benefit.

### Step 4: Find friction, using this checklist on each step
1. **Necessity:** what would break if this step disappeared? If "nothing for the user", remove or defer it.
2. **Inference:** could the system know this already? (Locale, time zone, country from IP, company from email domain, card type from number, city from postal code.)
3. **Default:** is there a safe default most users would accept?
4. **Deferral:** can this be asked later, when it is needed? (Profile details, team invites, preferences.)
5. **Order:** does the user get value before being asked for effort? (Let users try before signing up when feasible.)
6. **Commitment escalation:** small commitments first; big ones (payment, permissions) only after value is felt.
7. **Decision quality:** does the user have enough information **at this moment** to decide? If not, they stall or guess.
8. **Feedback:** after each action, does the user know it worked and what comes next?
9. **Reversibility:** can they go back without losing work?
10. **Interruption:** if they leave mid-flow (close tab, phone call, email verification), can they resume where they were?

### Step 5: Stress-test the seams (where flows break)
For each seam, test or reason through:
- **Email verification / magic link:** opened on another device or browser? Link expired? Already used? Does it return the user to where they were, with their intent preserved?
- **OAuth / SSO:** user denies permission; account exists with another method; returns to the right page with state.
- **Payment:** card declined; 3-D Secure challenge; network drop after charge; double-submit; return URL; receipts.
- **Session expiry mid-flow:** is data preserved and re-auth seamless?
- **Back / refresh / duplicate tab** inside a wizard.
- **Concurrency:** two users editing; stale data.
- **Permissions:** user lacks access halfway through. Does the flow say who can grant it?

### Step 6: Identify break points and drop-off risk
Rank steps by **drop-off risk**, using:
- Effort spike (many fields, uploads, verification)
- Uncertainty spike (unclear pricing, unclear consequences)
- Trust spike (payment, permissions, personal data)
- Waiting (verification emails, processing)
- Context switch (leaving the app)

If analytics exist, compare with real funnel data (→ MEAS). Otherwise label risk as **inferred**.

### Step 7: Propose the optimized flow
For each flow, write the **proposed step table** next to the current one, and quantify the change: "From 9 steps / 14 fields / 3 seams to 5 steps / 6 fields / 1 seam". Classify each change as **Remove / Merge / Reorder / Infer / Default / Defer / Redesign**.

## Criteria

<!-- BEGIN GENERATED criteria (flows-friction) -->
<!-- Source: criteria/flows-friction.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| FLOW-01 | Every critical flow is completable | Trace end to end | Any break, dead end or missing step | S4 |
| FLOW-02 | Minimal steps | Each step passes the necessity test | ≥ 1 removable step on a critical flow | S2–S3 |
| FLOW-03 | Minimal input | Fields that could be inferred, defaulted or deferred | Asking for known or unnecessary data | S2 |
| FLOW-04 | Value before effort | Time-to-value step count; sign-up or payment placement | Heavy commitment before any value | S2–S3 |
| FLOW-05 | Decisions are informed and few | Decision points have the needed info and sensible defaults | Choices the user cannot evaluate yet; more than ~7 equal options | S2 |
| FLOW-06 | No memory burden across steps | The user needn't remember data between screens | Copying codes or IDs between screens; re-entering earlier data (WCAG 3.3.7) | S2–S3 |
| FLOW-07 | Clear progress and orientation | Multi-step flows show step X of Y or a progress indicator | Unknown length; surprise extra steps | S2 |
| FLOW-08 | Feedback after every action | Each action produces a visible result within 1 s | Silent success; silent failure | S3 (S4 if silent failure) |
| FLOW-09 | Back and edit without data loss | Back or edit within the flow preserves inputs | Inputs cleared; must restart | S3 |
| FLOW-10 | Interruption-safe | Drafts are saved; resumable after leaving or a session timeout | Progress lost on tab close or timeout | S3 |
| FLOW-11 | Seams preserve intent | After email, OAuth or payment redirects, the user lands at their goal with context | Lands on a generic dashboard; intent lost | S3 |
| FLOW-12 | Edge seams handled | Expired or used links, declined cards, denied OAuth, double submit | Raw errors, or the user is stuck | S3–S4 |
| FLOW-13 | Idempotent critical actions | Double click or retry doesn't double-charge or double-create | Duplicates | S3–S4 (S4 for payments) |
| FLOW-14 | Exit flows are as easy as entry flows | Cancel, downgrade, delete and export are reachable and proportional | Cancellation harder than sign-up (also legal risk, → TRUST) | S3 |
| FLOW-15 | Error recovery inside the flow | Errors are recoverable in place, with inputs kept | Error page that discards progress | S3 |
| FLOW-16 | Expert efficiency | Repeated flows have shortcuts: bulk actions, templates, duplicate, keyboard | Experts forced through the novice wizard every time | S2 |
| FLOW-17 | Permission and role dead ends | Users without permission see why and how to get access | Blank screen or a generic 403 | S2–S3 |
| FLOW-18 | Consistent flow patterns | Similar tasks (create X, create Y) follow the same pattern | Each creation flow behaves differently | S2 |
| FLOW-19 | Confirmation proportional to risk | Low-risk: no confirmation (use undo); high-risk: explicit confirmation | Confirm dialogs everywhere (users stop reading them) or nowhere | S2–S4 |
| FLOW-20 | Completion is clear | The end state confirms success and suggests the next step | Flow ends on an ambiguous screen | S2 |
<!-- END GENERATED criteria -->

## Code probes

- Redirects: `redirect(`, `router.push(`, `router.replace(`, `navigate(`, `window.location`, `Response.redirect`.
- Multi-step wizards: `step`, `currentStep`, `setStep`, `Stepper`, `wizard`.
- Draft persistence: `localStorage`, `sessionStorage`, `autosave`, `draft`, `persist`.
- Double-submit protection: `disabled={isSubmitting}`, `idempotency`, `Idempotency-Key`, debounce on submit.
- Token and link expiry handling: `expired`, `invalid token`, `TokenExpiredError`.

## Output

- For each critical flow: the current step table, metrics, ranked break points, the proposed step table, and the delta metrics.
- Findings in the standard format (flow-level issues; reference other areas for screen-level issues).
- The coverage table (FLOW-01 … FLOW-20).

## Done when

Every critical flow has been traced end to end (runtime or code), every seam has been tested or marked Not verified, and every flow has a proposed optimized version with quantified deltas.
