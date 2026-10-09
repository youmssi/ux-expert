# Onboarding and Activation (ONB)

## Senior mindset

A senior's onboarding definition is not "a product tour". It is **"the shortest path from first contact to the user's first real success"**: the **aha moment**, when the user gets the value they came for. Everything before that moment is cost; the job is to make it **short, safe and obviously worth it**.

Their principles:
1. **Show, don't tell.** Let users do the core action as early as possible, ideally before sign-up. ChatGPT lets you type immediately; Cal.com's first step is connecting a calendar and sharing your link.
2. **Teach in context.** Help appears at the moment it's needed (contextual tips, empty states), not in a 7-slide tour users skip.
3. **Defaults and templates beat configuration.** An empty canvas is intimidating; a pre-filled example is a starting point.
4. **Measure activation, not completion of onboarding.** Completing a tour is not success; doing the core job is.
5. **Personalize only if it changes the path.** Every "tell us about yourself" question must change what the user sees; otherwise remove it.

## Scope

- **In:** first contact to account (sign-up/sign-in options, SSO, passwordless), verification, setup steps, the first-run screen, empty-state onboarding, sample data and templates, product tours, tooltips, checklists, welcome emails and lifecycle messaging, the activation definition and instrumentation, team invites (collaborative activation), returning-user re-onboarding, onboarding for new features (feature discovery), mobile permission priming.
- **Out:** detailed form design (→ FORM), general flow step analysis (→ FLOW: ONB focuses on the first-run journey and learning), analytics implementation details (→ MEAS).

## Procedure

### Step 1: Define the aha moment and activation
- From CTX: what is the core job? What is the first meaningful outcome? (e.g. "first booking received", "first rule evaluated successfully", "first invoice sent", "first useful AI answer".)
- **Activation event** = the user action that best predicts retention (when analytics exist, the team should validate it statistically; otherwise propose one).
- Check whether the activation event is instrumented in code (`track('…')`).

### Step 2: Map the first-run journey
Walk from the entry points (landing CTA, app store, invite email, docs quick start) to the aha moment:

| # | Step | Required? | Time estimate | Value delivered so far | Drop-off risk | Notes |
|---|---|---|---|---|---|---|

Compute **time-to-value (TTV)**: steps and estimated minutes to the aha moment. Compare with the marketing promise ("set up in 2 minutes").

### Step 3: Sign-up friction
- Can users **try before signing up** (guest mode, demo, playground, sandbox)?
- Sign-up options: SSO (Google, Microsoft, Apple, GitHub for developers), passkeys, magic link, email+password. Offer the options that match the audience.
- Fields at sign-up: the absolute minimum (often email only, or SSO).
- Email verification: does it block usage? Prefer letting users in and verifying in the background, unless there are security or abuse reasons.
- Paywall timing: does the user see value before being asked to pay? Is a card required for a trial (a legitimate choice, but a known conversion trade-off; it must be clearly disclosed → TRUST)?

### Step 4: Setup and personalization
- Each setup question: does the answer change the experience? If not, remove it.
- Can setup be skipped and done later? Are there sensible defaults?
- Integrations or imports (connect calendar, import CSV, connect repo): are they **optional or required**, with a fallback path (sample data)?

### Step 5: First-run screen and empty states
- The first screen after sign-up has **one obvious next action** toward the aha moment.
- Empty states educate and invite (→ STATE-02).
- **Templates, examples and sample data** are available so users can explore without creating from scratch.

### Step 6: Education mechanisms
Evaluate each that exists:
- **Product tours:** ≤ 3–5 steps, skippable, triggered at a relevant moment, resumable, not blocking the UI they describe.
- **Tooltips/hotspots:** contextual, dismissible, never all at once.
- **Checklists:** 3–7 meaningful tasks tied to value (not "upload avatar"), progress shown, with the first item pre-completed (goal-gradient effect), and dismissible.
- **Videos/docs:** short, linked in context, with text alternatives.
- **Progressive disclosure:** advanced features revealed as users mature (not all at once).

### Step 7: Collaborative and lifecycle onboarding
- Invites: is inviting teammates part of activation for team products? Is it easy, can it be deferred, and does the invitee's journey preserve context ("Ana invited you to project X" → lands in project X)?
- Lifecycle messages: a welcome email with the single next step; nudges tied to incomplete activation (not generic drips); easy opt-out.
- Returning users after inactivity: "what's new" or "pick up where you left off".

### Step 8: Mobile specifics (if applicable)
- No sign-up wall before value where possible.
- **Permission priming:** explain the value before the OS permission prompt (notifications, location, camera), and ask at the moment of need, not on first launch. A denied OS prompt is hard to recover from.
- App Store screenshots and descriptions match the actual first-run experience (→ LAUNCH).

## Criteria

<!-- BEGIN GENERATED criteria (onboarding-activation) -->
<!-- Source: criteria/onboarding-activation.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| ONB-01 | Aha moment and activation event defined | No definition; onboarding ends at "profile complete" | S2 |
| ONB-02 | Activation instrumented | No event for activation | S2 (→ MEAS) |
| ONB-03 | Short time-to-value | Many steps or minutes before first value; exceeds the marketing promise | S3 |
| ONB-04 | Try before commit (where feasible) | Hard sign-up wall for a product that could demo value | S2 |
| ONB-05 | Minimal sign-up | > 3 fields at sign-up without justification; no SSO for the audience | S2–S3 |
| ONB-06 | Non-blocking verification | Email verification blocks first use without a security reason | S2 |
| ONB-07 | Setup questions change the experience | Questions that personalize nothing | S2 |
| ONB-08 | Skippable, deferrable setup | Forced integrations or imports with no fallback | S3 |
| ONB-09 | Clear first-run next action | First screen with no obvious next step, or many competing ones | S3 |
| ONB-10 | Templates, samples or examples | Blank-canvas start only | S2 |
| ONB-11 | Contextual education | Long upfront tours; help disconnected from the moment | S2 |
| ONB-12 | Tours well-behaved | > 5 steps; unskippable; covering the UI; restarting every visit | S2 |
| ONB-13 | Meaningful checklist (if any) | Vanity tasks; no progress; can't dismiss | S1–S2 |
| ONB-14 | Invite flow preserves context | Invitee lands on a generic page; must re-find the shared object | S2–S3 |
| ONB-15 | Lifecycle messages tied to progress | Generic drip emails; no opt-out | S2 |
| ONB-16 | Permission priming at moment of need | OS permission prompts on first launch without context | S2–S3 |
| ONB-17 | Returning-user re-onboarding | Users lose orientation after inactivity or major changes | S1–S2 |
| ONB-18 | New-feature discovery | New features invisible, or announced via disruptive modals | S1–S2 |
| ONB-19 | Promise–experience consistency | Landing or App Store promises not met in the first run | S2–S3 |
<!-- END GENERATED criteria -->

## Code probes

- Onboarding routes: `onboarding`, `welcome`, `setup`, `getting-started`, `first-run`, `wizard`.
- Tours: `react-joyride`, `shepherd`, `intro.js`, `driver.js`, `userflow`, `appcues`, `pendo`, `chameleon`.
- Checklists: `checklist`, `getting started`, `progress`.
- Flags for first-run: `hasOnboarded`, `isFirstVisit`, `onboardingCompleted`, `firstLogin`.
- Activation tracking: `track\(['"](activated|first_|aha|onboarding_)`.
- Permissions: `requestPermission`, `Notification.requestPermission`, `PermissionsAndroid.request`, `requestWhenInUseAuthorization`.
- Sign-up methods: `signIn\(['"](google|github|apple|azure)`, `passkey`, `webauthn`, `magic link`, `OTP`.

## Output

- The aha moment and activation definition (proposed or confirmed).
- The first-run journey table with a TTV estimate and drop-off risks.
- A proposed optimized onboarding: before/after steps and TTV.
- Findings in the standard format; the coverage table (ONB-01 … ONB-19).

## Done when

The aha moment is defined, the first-run journey is mapped end to end with TTV, each education mechanism is evaluated, and an optimized proposal with quantified deltas is written.
