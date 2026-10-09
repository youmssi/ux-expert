# Example: refactor mode on a sample audit

A worked example of `references/refactor-mode.md`. It is also the reference
output for the refactor-mode evals (UXE-10).

**Input:** an audit of an existing web app ("Teamly v1": React, Tailwind, no
design tokens, no i18n). Team of 3 front-end engineers, releases weekly, feature
flags available, Playwright already used for 2 smoke tests.

**Audit findings (summary):**

| Finding | Criterion | Priority | Location |
|---|---|---|---|
| F-001 Deleting a project has no confirmation or undo | STATE-17 | P0 | `ProjectMenu.tsx:88` |
| F-002 Sign-up submit unreachable by keyboard (`div` with onClick) | A11Y-02 | P0 | `SignupForm.tsx:142` |
| F-003 187 hard-coded hex colors, 6 near-identical blues | DS-03, COL-08 | P1 | 43 files |
| F-004 Muted text `#9CA3AF` on white: 2.5:1 | COL-03 | P1 | `globals.css:12` |
| F-005 Each of 7 forms validates differently; errors only on submit | FORM-09, FORM-10 | P1 | 7 forms |
| F-006 Placeholder-only labels on 4 forms | FORM-02 | P1 | 4 forms |
| F-007 "Something went wrong" for every API error; input cleared | CONT-06, FORM-12 | P1 | `api.ts:31` |
| F-008 No error boundary: a widget crash blanks the page | STATE-10 | P1 | `App.tsx` |
| F-009 Onboarding: 9 steps before the first task | FLOW-02, ONB-03 | P1 | `/onboarding/*` |
| F-010 Spacing values: 23 distinct, 9 off-scale | LAY-05 | P2 | 60+ files |
| F-011 All strings hard-coded; French launch planned | I18N-01 | P2 | whole app |
| F-012 No funnel events for onboarding | MEAS-02 | P2 | — |

**Strengths to protect:** the task board's keyboard shortcuts (INT-16) and the
fast board load (LCP 1.6 s, PERF-01).

---

# UX refactor plan: Teamly v1

## 1. Summary

12 findings (2 P0, 7 P1, 3 P2) come from 5 root causes. The plan has 13
stories over about 6 weekly releases: safety first, guards next, then 3
foundations, the migrations onto them, the onboarding redesign, and polish.
Expected outcome: both P0 and all 7 P1 findings closed, onboarding cut from 9 to
4 steps, measured from a baseline taken in story R-3.

## 2. Root causes and workstreams

| Root cause | Findings | Class |
|---|---|---|
| Interactive elements built from `div`s; no destructive-action pattern | F-001, F-002 | Safety |
| No design tokens | F-003, F-004, F-010 | Foundation → migration |
| No shared form field component or validation rule | F-005, F-006 | Foundation → migration |
| No error-handling pattern | F-007, F-008 | Foundation → migration |
| Onboarding designed around the data model | F-009, F-012 | Flow redesign |
| No i18n layer | F-011 | Foundation → migration (after the others) |

## 3. Dependency graph

```
R-4 tokens            → R-7 contrast fix, R-8 screen migration (color, spacing)
R-5 form field        → R-9 form migration
R-6 error pattern     → R-10 API error migration
R-3 onboarding events → R-11 onboarding redesign (baseline first)
R-5, R-6, R-9, R-10   → R-11 onboarding redesign (its forms and errors use them)
R-8, R-9, R-10        → R-12 i18n layer (extract strings once, from final components)
```

## 4. Sequence

| # | Story | Class | Closes | Depends on | Guard | Size |
|---|---|---|---|---|---|---|
| 1 | R-1 Undo for project deletion | Safety | F-001 | — | E2E: delete → undo restores the project | S |
| 2 | R-2 Keyboard-operable sign-up submit | Safety | F-002 | — | axe + E2E keyboard-only sign-up | XS |
| 3 | R-3 Onboarding funnel events (baseline) | Guard | F-012 | — | Event contract test | S |
| 4 | R-13 Guards for strengths to protect | Guard | — | — | E2E board shortcuts; LCP budget in CI | S |
| 5 | R-4 Semantic tokens (color, spacing, type) | Foundation | — | — | Visual snapshots of 5 key screens | M |
| 6 | R-5 Form field component with label, help, error and validation on blur | Foundation | — | — | Unit + axe on the component | M |
| 7 | R-6 Error pattern: boundary, typed API errors, message catalog | Foundation | F-008 | — | Unit: each error type renders its message | M |
| 8 | R-7 Muted-text contrast via token | Migration | F-004 | R-4 | Contrast unit test on tokens | XS |
| 9 | R-8 Migrate screens to tokens, critical flows first | Migration | F-003, F-010 | R-4 | Visual snapshots | L (3 PRs) |
| 10 | R-9 Migrate the 7 forms to the field component | Migration | F-005, F-006 | R-5 | axe + E2E per form | M (7 PRs) |
| 11 | R-10 Migrate API calls to the error pattern | Migration | F-007 | R-6 | Unit per error type | M |
| 12 | R-11 Onboarding in 4 steps, behind a flag | Flow | F-009 | R-3, R-5, R-6, R-9, R-10 | E2E sign-up → first task | L |
| 13 | R-12 i18n layer and string extraction | Foundation + migration | F-011 | R-8, R-9, R-10 | Pseudo-locale snapshot | L |

Quick wins that ride along: R-2 and R-7 (XS each).

## 5. Stories (two of thirteen shown)

### R-5 — Every form field behaves the same way
**Class:** foundation · **Depends on:** — · **Size:** M
**Closes:** prepares F-005, F-006 (FORM-02, FORM-03, FORM-09, FORM-10, FORM-11, A11Y-10)
**Why:** 7 forms validate 7 different ways, and 4 have placeholder-only labels, so users can't predict errors and screen-reader users can't identify fields.
**Change:** a `FormField` component with a visible label, help text and an error linked by `aria-describedby`, validation on blur and re-validation while typing after an error; documented in Storybook. Old inputs stay until R-9 (expand → migrate → contract).
**Guard:** unit tests for label association and validation timing; axe on all Storybook states.
**Verify:** FORM-02, FORM-03, FORM-09 and FORM-10 checks pass on the Storybook stories.
**Rollback:** not needed (no screen uses it yet).

### R-11 — New teams reach their first task in 4 steps
**Class:** flow · **Depends on:** R-3, R-5, R-6, R-9, R-10 · **Size:** L
**Closes:** F-009 (FLOW-02, ONB-03, ONB-07, ONB-08)
**Why:** 9 steps before the first task; the R-3 baseline shows where users drop.
**Change:** sign-up → project (prefilled name, templates) → first tasks → optional invite; company, role and avatar questions deferred or removed.
**Guard:** E2E sign-up → first task in ≤ 4 steps; the R-13 guards stay green.
**Verify:** steps counted from the route graph; the funnel compared with the R-3 baseline after 2 weeks.
**Rollback:** `onboarding_v2` flag, defaulting to the old flow until the funnel is checked.

## 6. Measures

| Workstream | Baseline (measured in) | Target |
|---|---|---|
| Onboarding | Sign-up → first task completion (R-3) | +20 % relative, within 4 weeks of R-11 |
| Accessibility | axe serious/critical violations on critical flows (R-2 run) | 0 |
| Consistency | Token adoption rate for color (R-4 count) | ≥ 95 % (DS-03) |
| Errors | Share of API errors shown as the generic message (R-6 logs) | 0 |

## 7. Deferred findings

None. F-011 (i18n) is scheduled last because extracting strings before the
component migrations would mean extracting them twice.
