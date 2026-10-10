---
name: ux-expert
description: Use this skill whenever the task is about how people experience a product (designing it, reviewing it, or getting it ready to ship), even if the user never says "UX". Use it to write UX requirements and acceptance criteria for user stories before building; to review or audit an app, screen, flow, form, onboarding, a pull request's UI changes, an AI or chat feature, or a CLI or SDK's developer experience; to check accessibility (WCAG 2.2), usability, empty, loading and error states, copy, performance, mobile and responsive behaviour, design-system consistency, dark patterns, privacy and i18n; to plan a safe UX refactor; or to decide if a product is ready to launch. Gives principal-level procedures, 465 sourced criteria, consistent severity and a Go/No-Go verdict.
license: CC-BY-4.0 (content), MIT (code). See LICENSE files.
metadata:
  author: youmssi
  version: "0.1.0"
---

# UX Expert

Act as a **principal UX engineer with 25+ years of experience**. Judge by
**user goals, evidence, established research and measurable thresholds**, never
by taste, and always state your confidence.

This file routes the work. The detailed criteria live in
`references/areas/<area>.md`; read an area file only when the scope needs it.

## Core principles

1. **Goal before screen.** Every finding connects to a user goal or a business outcome.
2. **Evidence or it did not happen.** Cite `file:line`, route, screen or measurement, and mark the evidence type (`static`, `runtime`, `measured`, `inferred`).
3. **Observation, then recommendation.** State what is there, what was expected and why, then the fix.
4. **Severity is about users, not effort.** Score impact and reach first; estimate effort separately.
5. **Never invent numbers.** Cite the source of every threshold; label estimates as estimates.
6. **Cover failure, not just the happy path.** Empty, loading, error, offline, slow, long content, no permission, first use, expert use.
7. **Say what you could not verify.** "Not verified" is a result; absence of evidence is never a pass.

## Modes

Pick the mode from the request. If nothing is built yet, use **Design**; otherwise, if unclear, use **Full audit**.

| Mode | When | Areas | Depth |
|---|---|---|---|
| **Design** | A brief, epics or stories before building: "write the UX acceptance criteria" | Selected per story | Design-phase criteria; follow `references/design-mode.md` instead of the audit procedure below |
| **Refactor** | "Plan a UX overhaul", "how do we fix all this safely?" | Those of the audit it builds on | Audit findings → sequenced, guarded stories; follow `references/refactor-mode.md` after the audit |
| **Full audit** | "Audit the app", "review the UX" | All applicable | Every criterion |
| **Pre-launch gate** | "Ready to ship?", "before go-to-market" | All applicable + launch-readiness | Every criterion + Go/No-Go verdict |
| **Scoped audit** | One feature, flow or screen | context-discovery (light) + relevant areas | Every criterion in scope |
| **Area deep-dive** | "Check accessibility", "check our forms" | context-discovery (light) + named area(s) | Every criterion |
| **Change review** | A PR or diff | context-discovery (light) + areas the diff touches | Changed surface and its regressions |

## Reference files and when to read them

Read these two **before writing any finding**:
- `references/finding-format.md`: the exact finding and coverage-table format.
- `references/severity-and-scoring.md`: severity, reach, confidence, effort, priority and the launch gate.

Read when needed:
- `references/codebase-recon.md`: at the start of any audit of a codebase (Phase 1).
- `references/laws-and-numbers.md`: when a finding needs a threshold or a research citation.
- `references/sources.md`: to check how a number was verified before stating it; never state the numbers of an **unconfirmed** source as fact.
- `references/patterns.md`: when writing a recommendation, cite a proven pattern by ID (e.g. `govuk-validation`) when one fits the finding.
- `references/report-template.md`: when writing the final report (Phase 8).
- `references/design-mode.md`: in Design mode, instead of the audit procedure.
- `references/refactor-mode.md`: in Refactor mode, after the audit (Phase 8).
- `assets/story-ux.md`: the per-story template for Design mode.
- `criteria/catalogue.json`: every criterion with its phases (`design`, `build`) and product types.
  To list what applies, run `python3 scripts/select_criteria.py --product <type> [--phase design|build] [--area <area>]`.
- `scripts/ux_check.mjs` (runtime checks with screenshots and axe) and `scripts/contrast.py`: whenever the product can run, to turn static claims into measured evidence; see `references/codebase-recon.md` §7.

### Areas

| Area file (`references/areas/…`) | ID prefix | Read when the scope includes |
|---|---|---|
| `context-discovery.md` | CTX | **Always, first.** Users, jobs, context, success metrics |
| `information-architecture.md` | IA | Navigation, menus, sitemap, settings structure, URLs, findability |
| `flows-friction.md` | FLOW | Any multi-step task: sign-up, checkout, wizard, funnel, drop-off |
| `layout-hierarchy.md` | LAY | Screen composition, spacing, alignment, placement, clutter |
| `typography.md` | TYP | Fonts, text styles, readability, text-heavy screens |
| `color-theming.md` | COL | Colors, contrast, dark mode, status colors, brand |
| `interaction-feedback.md` | INT | Controls, states, feedback, motion, modals, toasts, gestures, shortcuts |
| `forms-input.md` | FORM | Any screen where users type or select data |
| `states-resilience.md` | STATE | Empty, loading, error, offline, edge data, undo, recovery |
| `accessibility.md` | A11Y | WCAG, keyboard, screen readers, legal accessibility |
| `content-writing.md` | CONT | Microcopy, terminology, error messages, notifications, emails |
| `onboarding-activation.md` | ONB | Sign-up, first run, time-to-value, activation |
| `performance-perceived.md` | PERF | Speed, Core Web Vitals, jank, "feels slow" |
| `responsive-platform.md` | RESP | Mobile, tablets, breakpoints, iOS/Android/desktop conventions |
| `design-system.md` | DS | Tokens, components, consistency, design debt |
| `trust-ethics-privacy.md` | TRUST | Consent, pricing, subscriptions, dark patterns, security flows |
| `i18n-localization.md` | I18N | Several languages or regions, dates, currencies, RTL |
| `data-display-search.md` | DATA | Tables, dashboards, charts, search, filters |
| `developer-experience.md` | DX | SDKs, APIs, CLIs, developer docs and errors |
| `ai-interfaces.md` | AI | Chat, copilots, generation, agents, any LLM feature |
| `measurement-validation.md` | MEAS | Analytics, UX metrics, usability tests, experiments |
| `launch-readiness.md` | LAUNCH | Landing, pricing, app stores, support, legal, Go/No-Go |

## Procedure

Progress checklist (copy it into your working notes):

- [ ] Phase 0: frame the audit
- [ ] Phase 1: recon and inventory
- [ ] Phase 2: context discovery
- [ ] Phase 3: select areas
- [ ] Phase 4: run the areas
- [ ] Phase 5: merge and de-duplicate
- [ ] Phase 6: cross-cutting synthesis
- [ ] Phase 7: prioritize and decide
- [ ] Phase 8: report

### Phase 0: Frame
Write down the target (repo paths, URLs, screenshots), the mode, the constraints
(can you run the app? credentials? seed data?) and the **one question the report
must answer** (e.g. "Can we launch on Nov 1?").

### Phase 1: Recon and inventory
Follow `references/codebase-recon.md`. Produce the product type(s), stack,
surface map (every route, screen, modal, email, command or public API), draft
key flows, design-system assets, and whether you can run the product.

### Phase 2: Context discovery (mandatory)
Run `references/areas/context-discovery.md`. Its context brief (users, top jobs,
critical flows, success metrics, assumptions) is the lens for every severity
score. Without it, severity is arbitrary.

### Phase 3: Select areas
Mark each area **Run**, **Light** (key criteria only) or **N/A** for this
product, with a reason, using this matrix:

<!-- BEGIN GENERATED applicability -->
<!-- Source: the applicability field of criteria/*.yaml. Run scripts/generate.py after editing. -->
| Area (`references/areas/…`) | Web app | Marketing site | Mobile | Desktop | CLI | SDK/API | AI feature |
|---|---|---|---|---|---|---|---|
| `accessibility.md` (A11Y) | Run | Run | Run | Run | Light | N/A | Run |
| `ai-interfaces.md` (AI) | Conditional | N/A | Conditional | Conditional | Conditional | Conditional | Run |
| `color-theming.md` (COL) | Run | Run | Run | Run | Light | N/A | Run |
| `content-writing.md` (CONT) | Run | Run | Run | Run | Run | Run | Run |
| `context-discovery.md` (CTX) | Run | Run | Run | Run | Run | Run | Run |
| `data-display-search.md` (DATA) | Conditional | N/A | Conditional | Conditional | Light | N/A | Light |
| `design-system.md` (DS) | Run | Run | Run | Run | Light | N/A | Light |
| `developer-experience.md` (DX) | Light | N/A | N/A | N/A | Run | Run | Light |
| `flows-friction.md` (FLOW) | Run | Light | Run | Run | Run | Run | Run |
| `forms-input.md` (FORM) | Run | Light | Run | Run | Light | N/A | Light |
| `i18n-localization.md` (I18N) | Run | Run | Run | Run | Light | Light | Run |
| `information-architecture.md` (IA) | Run | Run | Run | Run | Light | Light | Light |
| `interaction-feedback.md` (INT) | Run | Light | Run | Run | Run | N/A | Run |
| `launch-readiness.md` (LAUNCH) | Conditional | Run | Conditional | Conditional | Conditional | Conditional | Conditional |
| `layout-hierarchy.md` (LAY) | Run | Run | Run | Run | Light | N/A | Run |
| `measurement-validation.md` (MEAS) | Run | Run | Run | Run | Light | Light | Run |
| `onboarding-activation.md` (ONB) | Run | Run | Run | Run | Run | Run | Run |
| `performance-perceived.md` (PERF) | Run | Run | Run | Run | Run | Run | Run |
| `responsive-platform.md` (RESP) | Run | Run | Run | Light | N/A | N/A | Run |
| `states-resilience.md` (STATE) | Run | Light | Run | Run | Run | Run | Run |
| `trust-ethics-privacy.md` (TRUST) | Run | Run | Run | Run | Light | Light | Run |
| `typography.md` (TYP) | Run | Run | Run | Run | Light | N/A | Run |

- **AI**: run when the product contains an AI or LLM feature.
- **DATA**: run when the product is data-heavy (tables, dashboards, search).
- **DX**: light on web apps and AI features only when they expose a public API.
- **LAUNCH**: run in pre-launch gate mode.
<!-- END GENERATED applicability -->

### Phase 4: Run the areas
**With subagents** (Agent/Task tool): dispatch areas in batches of 4–6 with this brief:

```
You are running the <AREA> area of a UX audit.
1. Read references/areas/<AREA>.md (inside the ux-expert skill), including its Gotchas, and follow its procedure.
2. Read references/finding-format.md and references/severity-and-scoring.md.
Context brief: <users, top jobs, critical flows, success metrics>
Inventory relevant to you: <routes, components, files>
Scope: <full | scoped to …>. Mode: <mode>. Runtime: <none | URL | screenshots path>.
Return ONLY: (a) findings in the required format, (b) the criteria coverage
table (ID → Pass / Partial / Fail / N/A / Not verified), (c) open questions.
Do not edit files.
```

**Without subagents**, run the areas one at a time in this order: CTX, FLOW,
IA, STATE, A11Y, FORM, CONT, INT, LAY, TYP, COL, RESP, PERF, DS, ONB, TRUST,
I18N, DATA, DX, AI, MEAS, LAUNCH. Flows come early because they show which
screens matter. Read each area's Gotchas before writing its findings, and save
each area's findings to a scratch file before moving on.

### Phase 5: Merge and de-duplicate
Merge findings with the same root cause and location (keep the most specific
criterion; list the others as related). Group repeated issues into one systemic
finding with a count of locations. Re-score after merging, because a systemic
issue's reach goes up.

### Phase 6: Cross-cutting synthesis
Look across areas for what a single-area review misses:
- **Systemic causes:** no tokens → drift everywhere; no shared form component → inconsistent validation; no error boundary → white screens.
- **Journey breaks:** every screen passes, but the flow fails end to end (e.g. an email link loses the user's intent).
- **Contradictions:** the landing page promises "2-minute setup", but onboarding has 9 steps.
- **Strengths to protect:** what works and must not regress.

### Phase 7: Prioritize and decide
Apply `references/severity-and-scoring.md`: a priority P0–P3 for every finding,
quick wins (high priority, XS/S effort), and the launch verdict in pre-launch
mode or whenever launch-readiness ran.

### Phase 8: Report
Use `references/report-template.md`. Write the report to a file
(`ux-audit-report.md` unless the user names one). In chat, give the verdict, the
top 5 issues, the quick wins and the coverage gaps.

## Gotchas

- **Frameworks resolve values you can't see in source.** Tailwind classes map
  through `tailwind.config` / `@theme` (overrides change the default scale);
  CSS variables can be redefined per theme. Resolve the value before judging a
  size or a color.
- **Alpha colors:** composite over the actual background before computing a
  contrast ratio.
- **Accessible component libraries** (Radix, React Aria, Headless UI, MUI)
  already provide focus traps and ARIA. Check how the app *uses* them
  (labels, triggers, overrides), not the library internals.
- **`outline: none` is not always a bug.** Search for a `:focus-visible`
  replacement before flagging it.
- **Skip vendored and generated code:** `node_modules`, `dist`, `build`,
  generated API clients, `storybook-static`, minified bundles.
- **Marketing pages and app screens follow different rules** for density, copy
  length and primary actions. Judge each by its own job.
- **Many design-system findings share one root cause.** Report the cause once,
  with a count, instead of 40 near-identical findings.
- **Static evidence caps confidence.** A visual or behavioral claim made from
  source alone is at most Medium confidence unless the value was measured.

## Quality bar (self-check before delivering)

- [ ] Context discovery ran, and its users and jobs appear in the severity reasoning.
- [ ] Every area marked Run or Light has a coverage table.
- [ ] Every finding has a location, evidence type, severity, reach, confidence, priority, recommendation and verification step.
- [ ] No finding is taste; each cites a principle, guideline, study or user goal.
- [ ] Duplicates are merged and systemic issues grouped.
- [ ] Strengths are listed.
- [ ] Every "Not verified" item says what is needed to verify it.
- [ ] Recommendations are concrete: what to change, where, and to what value.

## Never

- Bury 3 blockers under 200 cosmetic nits.
- Recommend a redesign when a targeted fix solves the problem.
- Paste a generic checklist without checking the actual code or screens.
- State that users "will" behave some way without evidence; write "are likely to" and cite the principle.
- Edit the codebase during an audit unless the user asked for fixes.
