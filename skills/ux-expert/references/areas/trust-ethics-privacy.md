# Trust, Ethics and Privacy (TRUST)

## Senior mindset

A senior knows that **trust is the hidden conversion metric**. Users who feel tricked leave, churn, complain and tell others. Regulators increasingly fine manipulative design: the EU DSA bans dark patterns on online platforms, GDPR requires freely given and unambiguous consent, and US regulators (e.g. the FTC) have acted against hard-to-cancel subscriptions and deceptive design.

Their test for every persuasive element: **"Would the user still agree with this design if they fully understood what it was doing?"** If not, it is a dark pattern, no matter how well it converts.

They also treat **security as UX**: account recovery, MFA, session handling and suspicious-activity notices are flows people meet at stressful moments. Bad security UX pushes users to unsafe workarounds (reused passwords, disabled MFA). Good security UX is **strong and calm**: passkeys, clear recovery, and readable alerts.

## Scope

- **In:** dark patterns (per the Brignull/deceptive.design taxonomy and regulators' lists), consent (cookies, marketing, data processing, AI training use), privacy settings, data access/export/deletion, pricing and fees transparency, trials and auto-renewal disclosure, cancellation and downgrade, destructive actions, permission requests (OS and in-app), security UX (sign-in, MFA, passkeys, password reset, account recovery, session management, device lists, suspicious-login alerts), transparency of automated decisions and AI, credibility signals (company info, contact, policies, status), children's data (if relevant), notifications ethics (frequency, opt-out), and social-proof honesty.
- **Out:** legal advice. Flag **risks** and recommend legal review; don't declare legal compliance.

## Procedure

### Step 1: Map trust-critical moments
From FLOW/ONB: sign-up, consent, pricing pages, checkout, trials, upgrades, cancellation, data deletion, account recovery, permission prompts, sharing/visibility settings, AI features that use user data.

### Step 2: Dark-pattern sweep
Check each trust-critical screen for these patterns:

| Pattern | What it looks like | Probe |
|---|---|---|
| **Pre-selection** | Pre-ticked marketing, add-ons or data sharing | `defaultChecked`, `checked={true}` on consent/opt-in |
| **Confirmshaming** | "No thanks, I don't like saving money" | Decline-link copy |
| **Roach motel / hard to cancel** | Sign-up in 1 click, cancellation requires phone/chat/many steps | Compare the sign-up and cancel flows (→ FLOW-14) |
| **Hidden costs / drip pricing** | Fees revealed only at the last step | Price shown on product vs. checkout total |
| **Sneak into basket** | Items or insurance added automatically | Cart defaults |
| **Disguised ads** | Ads styled as content or navigation | Sponsored labels |
| **False urgency/scarcity** | Fake countdowns, "only 2 left" not based on data | Timers reset on reload; hard-coded stock messages |
| **Fake social proof** | Invented testimonials or activity notifications | Hard-coded "Ana just bought…" |
| **Nagging** | Repeated prompts with no "never" option | Modal frequency logic |
| **Obstruction / asymmetric choice** | "Accept all" prominent, "Reject" hidden in a second layer | Cookie banner button styling and layers |
| **Trick wording** | Double negatives in opt-outs | Consent copy |
| **Forced continuity** | Trial converts to paid without a clear reminder | Trial-end reminder emails |
| **Privacy zuckering** | Defaults that over-share | Default visibility settings |
| **Interface interference** | Decline action styled as disabled or tiny | Button variants on consent and upsell screens |

### Step 3: Consent and privacy
- **Cookie/tracking consent (EU/UK audiences):** non-essential tracking does **not load before consent** (check script loading order); "Reject all" is as easy and prominent as "Accept all" (first layer); granular choices; consent is withdrawable as easily as given (a persistent link); consent state is recorded.
- **Marketing consent:** separate, unticked, and not bundled with the Terms of Service.
- **Data processing transparency:** a privacy policy in plain language, linked at collection points ("why we ask", → CONT); a just-in-time notice for sensitive data.
- **User data rights:** a self-serve **export** and **account deletion** (deletion should be reachable in-app; app stores also require in-app account deletion for apps that support account creation); retention explained.
- **AI/data use:** is user content used to train models? Is that disclosed, and is there an opt-out where required or expected (→ AI)?
- **Children:** if the audience may include minors, age-appropriate design obligations (e.g. COPPA, UK Age Appropriate Design Code) need checking.

### Step 4: Pricing, billing and subscriptions
- Prices include or clearly state taxes and fees; currency is explicit; billing period is explicit ("$12 per user/month, billed annually: $144/year").
- Trial terms: length, what happens at the end, whether a card is charged, and a reminder before charging.
- Upgrades/downgrades: proration explained; immediate vs. end-of-period effects explained.
- **Cancellation:** online, in a similar number of steps to sign-up, with clear confirmation (email); retention offers allowed but **skippable** and not repeated.
- Invoices and receipts accessible; failed-payment (dunning) flows are clear and non-threatening, with grace periods.

### Step 5: Destructive and high-stakes actions
- Irreversible actions are clearly labeled, confirmed proportionally, and offer undo or a grace period where possible (→ STATE-17/18).
- Bulk and organization-wide actions show their scope and require stronger confirmation (type the name).
- Sharing and visibility changes show **who will be able to see what** before applying ("Anyone with the link can view").
- Sending money or making legal commitments: a review step with the full summary (WCAG 3.3.4).

### Step 6: Security UX
- **Sign-in:** password managers supported; passkeys offered where possible; clear error messages that don't leak account existence where that matters (balance this with usability; e.g. a generic "Email or password is incorrect", while sign-up can say "already registered" with a recovery link).
- **MFA:** available (required for admin roles in B2B); TOTP/passkeys/security keys; SMS as a fallback only; recovery codes given with a clear explanation; remember-device option.
- **Password reset/account recovery:** secure, time-limited links; works across devices; notifies the user of the change; no security questions.
- **Sessions:** a list of active sessions/devices with sign-out; notifications on new device sign-in and on security changes.
- **Sensitive data display:** masking (card numbers, API keys) with reveal and copy; re-authentication for very sensitive actions (change email, delete account, view secrets).
- **Phishing resistance:** consistent sender domains; emails never ask for passwords; links point to the real domain.

### Step 7: Transparency and credibility
- The system explains **why** it did something (why a payment failed, why access is denied, why this recommendation).
- Company identity: about page, contact method, physical address/legal entity where required, status page, support hours.
- Policies: Terms, Privacy, Cookies, Accessibility statement (→ A11Y), refund policy, with real links in the footer, sign-up and checkout.
- Visual credibility: professional, consistent UI (→ DS), no broken pages, valid HTTPS, no mixed-content warnings.
- Reviews and testimonials real and attributable.

## Criteria

<!-- BEGIN GENERATED criteria (trust-ethics-privacy) -->
<!-- Source: criteria/trust-ethics-privacy.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| TRUST-01 | No pre-selected consent or add-ons | Pre-ticked marketing, sharing or paid add-ons | S3–S4 |
| TRUST-02 | Symmetric consent choices | Reject harder than accept; hidden second layer | S3 (EU legal risk) |
| TRUST-03 | No tracking before consent (where required) | Analytics/ads scripts load before consent | S3–S4 |
| TRUST-04 | Withdrawable consent | No persistent way to change consent | S2–S3 |
| TRUST-05 | No confirmshaming, trick wording, nagging | Present | S2–S3 |
| TRUST-06 | No false urgency, scarcity or social proof | Fabricated timers, stock or activity | S3 |
| TRUST-07 | Transparent total price | Fees revealed late; tax or period unclear | S3 |
| TRUST-08 | Clear trial and renewal terms | No reminder; unclear charge timing | S3 |
| TRUST-09 | Cancellation as easy as sign-up | Phone-only, multi-step or hidden cancellation | S3–S4 |
| TRUST-10 | Self-serve data export and deletion | No in-app deletion or export | S3 |
| TRUST-11 | Privacy notices at collection | Sensitive data collected without explanation | S2 |
| TRUST-12 | AI and data-use disclosure | User data used for training or analysis without disclosure or opt-out | S3 |
| TRUST-13 | Visibility and sharing clarity | Users can't tell who sees their content | S3 |
| TRUST-14 | High-stakes review step | Money or legal actions without a summary review | S3 |
| TRUST-15 | Strong, usable authentication | No password-manager support; no MFA for admin; no passkeys (light) | S2–S3 |
| TRUST-16 | Safe account recovery | Insecure or broken recovery; security questions | S3 |
| TRUST-17 | Session and device visibility | No session list or security alerts | S2 |
| TRUST-18 | Sensitive data handled visibly | Secrets shown unmasked; no re-auth for critical changes | S2–S3 |
| TRUST-19 | System transparency | Unexplained denials, failures or automated decisions | S2 |
| TRUST-20 | Credibility basics | Missing contact, legal entity, policies or status page | S2 (→ LAUNCH) |
| TRUST-21 | Ethical notifications | No opt-out; manipulative re-engagement | S2 |
| TRUST-22 | Minors and sensitive categories handled (if applicable) | No age-appropriate safeguards | S3 |
<!-- END GENERATED criteria -->

## Code probes

- Pre-selection: `defaultChecked`, `checked=\{?true`, `useState\(true\)` near `marketing|newsletter|consent|share|optIn`.
- Tracking before consent: analytics initialization (`gtag\(`, `fbq\(`, `posthog.init`, `analytics.load`) not wrapped in a consent check; `<Script` analytics in the root layout.
- Consent tools: `cookiebot`, `onetrust`, `klaro`, `cookieconsent`, `@consent-manager`.
- Urgency: `countdown`, `setInterval` on timers in pricing/checkout; hard-coded `only \d+ left`.
- Cancellation: routes `cancel`, `subscription`, `billing`; Stripe `customer_portal`/`billingPortal` usage.
- Deletion/export: `deleteAccount`, `export`, `download my data`, `gdpr`.
- Auth: `passkey|webauthn`, `totp|mfa|2fa`, `recovery codes`, `sessions`, `revoke`.

## Gotchas

- This is not legal advice. Flag legal risk and recommend review; never state that a product is compliant.
- Consent tools often block scripts with `type="text/plain"` until consent. That is correct blocking, not tracking before consent.
- Payment providers' hosted portals (for example Stripe's customer portal) can handle cancellation. Check that one is linked and enabled before flagging TRUST-09.

## Output

- A dark-pattern sweep table (screen · pattern · evidence · severity).
- A consent flow analysis (script loading order, choice symmetry).
- A subscription lifecycle table (trial → renewal → upgrade → cancel → delete).
- A security UX table.
- Findings in the standard format; the coverage table (TRUST-01 … TRUST-22).
- A **Legal review recommended** list. Clearly state that this is not legal advice.

## Done when

All trust-critical moments are swept for dark patterns, consent and tracking load order is verified, the subscription lifecycle and security flows are evaluated, and legal-risk items are listed for human review.
