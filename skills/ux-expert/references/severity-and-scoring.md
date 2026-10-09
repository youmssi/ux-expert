# Severity, scoring, prioritization and launch gate

Based on Nielsen's severity model (frequency × impact × persistence), adapted so it can be computed consistently by different agents.

## 1. Severity (impact on one affected user)

| Level | Name | Definition | Typical examples |
|---|---|---|---|
| **S4** | Blocker | The user **cannot complete** a core job, **loses data or money**, is **exposed to harm** (security, privacy, legal), or a **legal accessibility barrier** blocks them | Submit button unreachable by keyboard; payment silently fails; account deleted with no confirmation or undo; consent pre-ticked in the EU |
| **S3** | Major | The user completes the job only with **significant difficulty**, errors, or outside help, **or** large numbers abandon the task | 9-step sign-up; error message "Something went wrong" with no next step; contrast 2.5:1 on body text |
| **S2** | Moderate | Noticeable friction, confusion or slowdown; the user recovers on their own | Inconsistent button labels; validation only on submit; no loading indicator for a 3s action |
| **S1** | Minor | Cosmetic or polish issue with small effect on task success or perception | Misaligned icon; inconsistent spacing between two cards |
| **S0** | Note | Not a problem now; an observation, risk or improvement idea | "Consider keyboard shortcuts for power users" |

**Escalation rules:**
- Anything that violates **law or regulation** (WCAG AA where legally required, GDPR consent, consumer-protection rules on cancellation) is at least **S3**, and S4 if it blocks.
- **Data loss** or **irreversible action without confirmation or undo** is always **S4**.
- A **trust-breaking** issue (looks like a scam, misleading pricing) on a payment or sign-up path is at least **S3**.

## 2. Reach (how many users and how often)

| Level | Definition |
|---|---|
| **R3** | On a **critical path** (sign-up, onboarding, core job, payment), or affects **most users** in most sessions, or is systemic (everywhere) |
| **R2** | Common secondary path, or affects a significant segment (e.g. all mobile users, all screen-reader users, all non-English locales) |
| **R1** | Edge case, rare path, or a small segment |

Note: "screen-reader users" is a small share of users but they are **fully blocked**. Reach stays R2, and severity carries the weight.

## 3. Confidence

| Level | Meaning |
|---|---|
| **High** | Measured or observed at runtime, or unambiguous in code |
| **Medium** | Static evidence of a visual or behavioral result, or strong principle-based reasoning |
| **Low** | Inference; needs validation (user test, analytics, runtime check) |

Low-confidence findings are **never** P0. Mark them "validate first" and describe the validation in **Verification**.

## 4. Effort (for planning only; it never lowers severity)

| Size | Rough meaning |
|---|---|
| XS | Copy or token change; < 1 hour |
| S | One component or screen; < 1 day |
| M | Several screens or a shared component; 1–3 days |
| L | A flow redesign or new system piece; 1–2 weeks |
| XL | Architectural or cross-team; > 2 weeks |

## 5. Priority matrix

<!-- BEGIN GENERATED priority-matrix -->
<!-- Source: criteria/scoring.yaml. Run scripts/generate.py after editing. -->
|  | **R3** | **R2** | **R1** |
|---|---|---|---|
| **S4** | P0 | P0 | P1 |
| **S3** | P0 | P1 | P2 |
| **S2** | P1 | P2 | P3 |
| **S1** | P2 | P3 | P3 |
| **S0** | P3 | P3 | P3 |
<!-- END GENERATED priority-matrix -->

Then apply confidence: **Low** confidence drops one level (P0 → P1, …), with a "validate first" flag.

- **P0:** must fix before launch or release.
- **P1:** fix in the current cycle; can launch only with an owner and a date.
- **P2:** next cycles; backlog with a planned slot.
- **P3:** opportunistic, or bundle with related work.

**Quick win** = P0–P2 with effort XS or S. List quick wins separately; they build momentum.

## 6. Area scorecard (0–5 maturity per area)

| Score | Meaning |
|---|---|
| 5 | Exemplary; no P0–P2; systemic practices in place (tokens, tests, guidelines) |
| 4 | Solid; no P0/P1; a few P2 |
| 3 | Adequate; no P0; a handful of P1 |
| 2 | Weak; one P0 or many P1 |
| 1 | Poor; several P0; no system |
| 0 | Not addressed at all, although it applies |

Also report the **criteria pass rate** per area: Pass / (Pass + Partial + Fail). Exclude N/A, and report Not verified separately.

## 7. Launch gate

<!-- BEGIN GENERATED launch-gate -->
<!-- Source: criteria/scoring.yaml (checked in this order). Run scripts/generate.py after editing. -->
| Verdict | Rule |
|---|---|
| **No-Go** | Any P0 open, or a critical flow was never verified end to end |
| **Conditional Go** | 0 P0, but P1s are unowned or some critical criteria (FLOW, STATE, A11Y, TRUST on critical flows) are Not verified; list the exact conditions |
| **Go** | 0 P0, every P1 has an owner and a date, and critical-flow coverage has no Not verified rows for FLOW, STATE, A11Y or TRUST |
<!-- END GENERATED launch-gate -->

State the verdict with the list of P0s and conditions. Never give a Go with unverified critical flows.
