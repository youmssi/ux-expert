# Accessibility (A11Y)

## Senior mindset

A senior treats accessibility as **usability for the full range of humans and situations**: permanent (blind, deaf, motor impairment), temporary (broken arm, eye surgery) and situational (bright sunlight, holding a baby, noisy train, slow connection). Microsoft's Inclusive Design toolkit calls this "solve for one, extend to many". Captions help everyone in a noisy room; keyboard shortcuts help power users.

They also know two hard facts:
1. **Automated tools catch only part of the problems.** The best tools found about 30–40 % of 142 known issues in a UK government audit [src:gds-automated-2017]; a vendor reports about 57 % by issue volume [src:deque-coverage-2021]. Manual keyboard and screen-reader testing is not optional.
2. **Accessibility is increasingly a legal launch requirement**: the European Accessibility Act (applicable since June 2025 for many consumer digital services in the EU), ADA lawsuits in the US, Section 508 for US federal work, and EN 301 549 in EU procurement. An inaccessible critical flow can be a launch blocker, not a nice-to-have.

The senior's rule: **use native semantic elements first** (`<button>`, `<a href>`, `<label>`, `<dialog>`, `<select>`). The first rule of ARIA is "don't use ARIA if a native element does the job". Most bugs come from `div`s pretending to be buttons.

## Scope

- **In:** WCAG 2.2 A and AA success criteria across Perceivable, Operable, Understandable and Robust; selected AAA items; keyboard and focus; screen-reader experience (names, roles, states, live regions, headings, landmarks); ARIA patterns (APG); forms accessibility; media (alt text, captions, transcripts, audio description); cognitive accessibility (plain language, consistent help, no time pressure); mobile (VoiceOver/TalkBack, accessibility labels and traits, Dynamic Type); documents (PDFs); legal obligations.
- **Out:** detailed contrast computations are done in COL (reuse its table), form UX in FORM (reuse it), and motion details in INT. This skill **owns the WCAG verdict**.

## Procedure

### Step 1: Determine the obligations
From CTX: jurisdiction, sector (public, finance, e-commerce, education), customers (enterprise procurement often requires a VPAT/ACR). Set the target: **WCAG 2.2 AA** by default.

### Step 2: Automated scan (if runtime is available)
- Run **axe-core** (e.g. `@axe-core/playwright`) on every critical-flow screen, in every relevant state (modal open, error shown, menu expanded). Also run Lighthouse accessibility.
- Record violations by rule, impact and count. Treat these as **measured** evidence. Remember they are only part of the picture.
- If no runtime: run static linters if configured (`eslint-plugin-jsx-a11y`, `vue-a11y`, `angular-eslint` template a11y) or use the code probes below.

### Step 3: Keyboard-only walkthrough (manual)
For each critical flow, without a mouse:
- **Tab order** follows the visual and logical order; no positive `tabindex`.
- **Every interactive element is reachable and operable** (Enter/Space on buttons, arrows inside composite widgets: menus, tabs, radios, grids, listboxes).
- **Focus is always visible** (`:focus-visible` style with ≥ 3:1 contrast; never `outline: none` without a replacement).
- **No keyboard traps** (except modals, which trap intentionally and release on Esc/close).
- **Skip link** to the main content on pages with repeated navigation.
- **Focus management:** when a modal opens, focus moves into it; on close, it returns to the trigger. After a route change in an SPA, focus moves to the new page heading (or the page title is announced). After deleting an item, focus moves somewhere sensible.
- **Focus not obscured** by sticky headers or footers (WCAG 2.4.11).

### Step 4: Screen-reader walkthrough (manual or reasoned from code)
Default pairing: NVDA with Chrome or Firefox on Windows, VoiceOver with Safari on macOS and iOS, TalkBack with Chrome on Android. Test the pairing your users have; without a screen reader, reason from the accessibility tree (Playwright `page.accessibility.snapshot()`, or the Chrome DevTools Accessibility pane) and mark the result Medium confidence.
- **Page title** unique and descriptive per page.
- **Landmarks:** `header`, `nav`, `main` (exactly one), `footer`, and labeled regions where there are several of the same kind.
- **Headings:** a logical outline (one H1, no skipped levels used for styling).
- **Accessible names:** every control has a meaningful name (icon buttons have `aria-label`; no "button", "click here" or duplicate "Edit" names without context, e.g. "Edit invoice #123").
- **Roles and states:** toggles expose `aria-pressed` or `aria-checked`; disclosure controls expose `aria-expanded`; current page uses `aria-current`; invalid fields `aria-invalid`.
- **Live regions:** async updates (toasts, form errors on submit, search result counts, chat streaming) are announced with `aria-live="polite"` (or `role="status"`), and critical alerts with `role="alert"`. Don't announce every streaming token: announce on completion or in batches.
- **Images:** informative images have meaningful `alt`; decorative ones have `alt=""`; complex images (charts) have a text alternative or data table.
- **Tables:** real `<table>` with `<th scope>` for data; not `div` grids without grid roles.
- **ARIA correctness:** valid roles, required children/parents (e.g. `role="tab"` inside `role="tablist"`), no `aria-hidden="true"` on focusable elements, and widget keyboard patterns as described in the WAI-ARIA Authoring Practices (APG).

### Step 5: Visual and adaptability checks
- Contrast (from COL): text 4.5:1 / 3:1; non-text 3:1.
- Zoom 200% (text) and **reflow at 320 CSS px** with no horizontal scrolling for content (except data tables, maps and code).
- Text spacing override (WCAG 1.4.12) doesn't clip content.
- Orientation not locked (WCAG 1.3.4).
- Target size ≥ 24×24 CSS px or adequately spaced (WCAG 2.5.8).
- Meaning not conveyed by color, shape, size or position alone ("click the green button on the right" ❌).
- Motion: `prefers-reduced-motion`; no auto-playing media with sound; pause controls for carousels and auto-updating content.

### Step 6: Forms (reuse FORM results; confirm the WCAG mapping)
Labels (1.3.1, 3.3.2), error identification (3.3.1), error suggestion (3.3.3), error prevention for legal/financial actions (3.3.4: reversible, checked or confirmed), autocomplete (1.3.5), redundant entry (3.3.7), accessible authentication (3.3.8).

### Step 7: Cognitive and consistency
- Plain language for critical instructions (→ CONT).
- **Consistent help** in the same relative place across pages (3.2.6).
- **Consistent navigation and identification** (3.2.3, 3.2.4).
- No unexpected context changes on focus or input (3.2.1, 3.2.2), e.g. a select that navigates on change.
- No time limits, or adjustable ones (2.2.1).

### Step 8: Media
Captions for prerecorded and live video audio (1.2.2, 1.2.4), transcripts for audio, audio description or a media alternative for video-only information (1.2.3, 1.2.5).

### Step 9: Mobile native (if applicable)
- iOS: `accessibilityLabel`, `accessibilityTraits`/roles, `accessibilityHint` used sparingly, Dynamic Type support, and grouping of elements (`accessibilityElement(children: .combine)`).
- Android: `contentDescription`, `importantForAccessibility`, touch targets 48 dp, `sp` units.
- React Native: `accessible`, `accessibilityLabel`, `accessibilityRole`, `accessibilityState`.
- Flutter: `Semantics` widgets, `excludeSemantics`, `MergeSemantics`.
- Find candidates with `python3 scripts/probe.py <project root>` (`references/native-probes.md`).

### Step 10: Produce the conformance view
Map the findings to WCAG success criteria. For pre-launch or enterprise mode, recommend producing an **Accessibility Conformance Report (VPAT)** and an **accessibility statement** page (required for EU public sector, and good practice elsewhere).

## Criteria

<!-- BEGIN GENERATED criteria (accessibility) -->
<!-- Source: criteria/accessibility.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| A11Y-01 | Automated scan clean on critical screens (axe) | Serious/critical violations | S2–S4 (by impact) |
| A11Y-02 | Keyboard operable everything (2.1.1) | Any critical control unreachable or inoperable by keyboard | S4 (on critical flow) |
| A11Y-03 | No keyboard trap (2.1.2) | Focus stuck | S4 |
| A11Y-04 | Visible focus (2.4.7; 2.4.11; 2.4.13 AAA) | `outline: none` without replacement; focus hidden by sticky UI | S3 |
| A11Y-05 | Logical focus order (2.4.3) | Positive tabindex; DOM order differs from visual order | S2–S3 |
| A11Y-06 | Focus management on dynamic UI | Modals don't move or return focus; SPA route change loses focus | S3 |
| A11Y-07 | Skip link / bypass blocks (2.4.1) | No way to bypass repeated navigation | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-08 | Page titles (2.4.2) | Missing, duplicate or generic titles | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-09 | Landmarks and headings (1.3.1, 2.4.6) | No `main`; heading levels used for styling | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-10 | Accessible names (4.1.2, 2.5.3 label-in-name) | Unlabeled icon buttons; visible label not contained in the accessible name | S3 |
| A11Y-11 | Roles and states exposed (4.1.2) | Custom widgets with no role or state | S3 |
| A11Y-12 | Valid ARIA usage | Invalid roles; `aria-hidden` on focusable elements; redundant or contradictory ARIA | S2–S3 |
| A11Y-13 | Status messages announced (4.1.3) | Toasts, async errors and results not announced | S2–S3 |
| A11Y-14 | Text alternatives (1.1.1) | Missing alt; meaningless alt ("image", file names) | S2–S3 |
| A11Y-15 | Contrast (1.4.3, 1.4.11), from COL | Below thresholds | S3 |
| A11Y-16 | Use of color (1.4.1) | Color-only meaning | S3 |
| A11Y-17 | Resize and reflow (1.4.4, 1.4.10) | Content lost or 2-D scrolling at 320 px or 200% | S3 |
| A11Y-18 | Text spacing (1.4.12) | Clipping | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-19 | Content on hover/focus (1.4.13) | Tooltips not dismissible or hoverable | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-20 | Target size (2.5.8) | < 24×24 CSS px without spacing | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-21 | Dragging alternatives (2.5.7), pointer gestures (2.5.1), pointer cancellation (2.5.2) | Drag-only or path-gesture-only operations | S3 |
| A11Y-22 | Motion and flashing (2.2.2, 2.3.1, 2.3.3) | Unstoppable motion; flashing; ignores reduced motion | S2–S4 |
| A11Y-23 | Timing adjustable (2.2.1) | Hard time limits with no extension | S3 |
| A11Y-24 | Forms: labels, errors, suggestions, prevention (1.3.1, 3.3.1–3.3.4, 1.3.5) | See FORM | S2–S4 |
| A11Y-25 | Redundant entry and accessible auth (3.3.7, 3.3.8) | Re-entry; cognitive test without alternative | S3 |
| A11Y-26 | Consistent navigation, identification and help (3.2.3, 3.2.4, 3.2.6) | Inconsistent | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-27 | No unexpected context change (3.2.1, 3.2.2) | Auto-navigation on select or focus | S2–S3 |
| A11Y-28 | Language of page and parts (3.1.1, 3.1.2) | Missing `lang`; wrong `lang` on translated pages | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-29 | Media alternatives (1.2.x) | Video without captions; audio without transcript | S3 |
| A11Y-30 | Orientation (1.3.4) | Locked orientation | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508) |
| A11Y-31 | Zoom not disabled | `user-scalable=no`, `maximum-scale=1` | S3 |
| A11Y-32 | Native mobile accessibility APIs | Missing labels, roles, Dynamic Type | S3 |
| A11Y-33 | Accessibility process | No a11y lint, test or statement; no VPAT where required | S1–S3 (by obligation) |
<!-- END GENERATED criteria -->

## Code probes

- `outline:\s*(none|0)` (then check for a `:focus-visible` replacement)
- `<div[^>]*onClick`, `<span[^>]*onClick`, `role="button"` (check `tabIndex` and key handlers)
- `tabIndex=\{?["']?[1-9]` (positive tabindex)
- `<img(?![^>]*\balt=)`, `alt=["'](image|img|photo|picture|icon)`
- Icon-only buttons: `<button[^>]*>\s*<(svg|Icon|\w+Icon)` with no `aria-label`
- `aria-hidden="true"` on elements containing `button|a href|input`
- `user-scalable=no|maximum-scale=1`
- `<html(?![^>]*\blang=)`
- `aria-live|role="(status|alert)"` (presence near toasts and async errors)
- `autoFocus` (check that it's justified)
- Linters: `eslint-plugin-jsx-a11y` in `package.json` / ESLint config; `jest-axe`, `@axe-core/*` in tests

## Gotchas

- A clean axe run is not a pass for keyboard and focus criteria (A11Y-02 to A11Y-06). Those need the keyboard walkthrough.
- `aria-label` on a `div` or `span` without a role is ignored by most screen readers.
- `sr-only` (visually hidden) text is fine; `display: none` and `visibility: hidden` remove content from the accessibility tree.
- WCAG 2.5.8 has exceptions: inline links in text, and targets with enough spacing. Measure spacing before flagging a small target.

## Output

- An axe results summary (if run): rule · impact · count · screens.
- A keyboard walkthrough log per critical flow (step, focus target, issue).
- A screen-reader findings log.
- A WCAG 2.2 AA conformance table: SC · Pass/Fail/Partial/N/A/Not verified · findings.
- Findings in the standard format; the coverage table (A11Y-01 … A11Y-33).

## Done when

Every critical flow has had a keyboard walkthrough (runtime) or is explicitly Not verified, automated scans have run where possible, and the WCAG conformance table is filled with no silent gaps.
