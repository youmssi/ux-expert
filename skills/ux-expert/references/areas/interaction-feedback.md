# Interaction and Feedback (INT)

## Senior mindset

Don Norman's model is the senior's lens: every interaction has a **gulf of execution** ("how do I do what I want?") and a **gulf of evaluation** ("did it work? what state is it in now?"). Good interaction design makes both gulfs small:
- **Affordances and signifiers** make the possible actions **visible** (a button looks pressable; a draggable row has a handle).
- **Feedback** makes the result **immediate and unambiguous** (pressed state within 100 ms, result or progress within 1 s).
- **Mapping and constraints** make errors **unlikely** (disabled options that can't apply, sliders for ranges, a date picker that blocks impossible dates).

Seniors also believe that **every interaction has five states**, not one: default, hover, focus, active/pressed, disabled, and often loading, selected and error as well. Most "the UI feels cheap" complaints come from missing states and badly timed motion.

ChatGPT's feel comes partly from this: the send button changes to a stop button while generating, text streams in (continuous feedback for a long operation), and every message has hover actions (copy, edit, regenerate) that appear only where they are relevant.

## Scope

- **In:** affordances and signifiers, choice of control (button vs. link vs. toggle vs. checkbox), component states, immediate feedback, microinteractions, motion (duration, easing, purpose, reduced motion), overlays (modal, drawer, popover, tooltip, toast, dropdown), keyboard shortcuts and command palettes, gestures and drag & drop, hover-dependent UI, undo/redo, selection models, optimistic UI behavior (latency → PERF).
- **Out:** loading/empty/error state content (→ STATE), screen-reader semantics (→ A11Y; but keyboard operability of custom widgets is checked here and there), form-specific behavior (→ FORM).

## Procedure

### Step 1: Component behavior inventory
List the interactive components (buttons, links, inputs, toggles, tabs, menus, dialogs, tooltips, toasts, accordions, carousels, drag areas, editors). For each, check the **state matrix**:

| Component | Default | Hover | Focus-visible | Active | Disabled | Loading | Selected | Error |
|---|---|---|---|---|---|---|---|---|

Mark each state ✅ (exists and distinct) / ⚠️ (exists but weak) / ❌ (missing). Derive this from component code and CSS (`:hover`, `:focus-visible`, `:active`, `[disabled]`, `aria-pressed`, `data-state`).

### Step 2: Control semantics (the right control for the job)
- **Button vs. link:** buttons do things; links go places. A `<a>` used for actions, or a `<button>` used for navigation, breaks expectations (middle-click, open in new tab, keyboard behavior).
- **Toggle switch vs. checkbox:** a switch applies **immediately**; a checkbox is part of a form that is submitted. A switch that requires "Save" is a mismatch.
- **Radio vs. dropdown:** radios for 2–5 visible options (faster, comparable); a select for many options; a segmented control for 2–4 view modes.
- **Disabled buttons:** a disabled submit with no explanation hides *why*. Prefer an enabled button plus validation messages, or an explanation near the disabled control.

### Step 3: Feedback timing
For each action on critical flows:
- **≤ 100 ms:** a visual response (pressed state, ripple, checkbox tick).
- **≤ 1 s:** the result, or an indication that work is in progress (spinner on the button, inline progress).
- **> 1 s:** a skeleton or progress indicator; **> 10 s:** a progress bar with an estimate and cancel/background options.
- **Completion:** a confirmation proportional to importance (inline change for small actions; a toast for background results; a success screen for major milestones).
- **Optimistic updates** for low-risk, high-confidence actions (like, rename, reorder), with rollback and an error message on failure.

### Step 4: Motion audit
- Find animations: CSS `transition`/`animation`, `framer-motion`/`motion`, `react-spring`, `Animated`, `withTiming`, Lottie.
- **Purpose:** each animation should explain something (where an element came from, what changed, the spatial relationship) or give feedback. Decorative-only motion on frequent actions is friction.
- **Duration:** micro 100–200 ms; panels 200–300 ms; big transitions ≤ 500 ms. Flag > 500 ms on frequent interactions.
- **Easing:** ease-out (decelerate) for entering, ease-in for exiting; avoid linear for UI movement.
- **Reduced motion:** `@media (prefers-reduced-motion: reduce)` or `useReducedMotion` disables or reduces non-essential motion, parallax and auto-playing animation (WCAG 2.3.3 AAA; 2.2.2 for auto-moving content > 5 s at level A needs pause/stop/hide).
- **No flashing** more than 3 times per second (WCAG 2.3.1).

### Step 5: Overlays
- **Modals:** used for focused, blocking tasks only. They trap focus, close on Esc, return focus to the trigger, prevent background scroll, have a visible close control, and are not stacked more than one deep. On mobile, prefer full-screen sheets.
- **Popovers/dropdowns:** close on outside click and Esc, position within the viewport (flip/shift), and are keyboard navigable.
- **Tooltips:** supplementary only (never essential information, which is inaccessible on touch); appear on hover **and** focus; dismissible (Esc) and hoverable (WCAG 1.4.13); short delay (~300–500 ms) to avoid flicker.
- **Toasts:** non-critical, polite announcements; errors and anything with an action shouldn't auto-dismiss (or should last long enough; WCAG 2.2.1); not covering primary controls; stacking behavior defined.

### Step 6: Power interactions
- **Keyboard shortcuts:** discoverable (tooltips show them, a `?` cheat sheet), don't conflict with browser or screen-reader keys, single-key shortcuts can be turned off or remapped (WCAG 2.1.4), and a command palette (⌘K / Ctrl+K) for large products.
- **Drag and drop:** visible handles, drop-zone feedback, auto-scroll, and a **non-drag alternative** (WCAG 2.5.7 Dragging Movements, AA).
- **Gestures:** swipe actions have visible alternatives; there's no reliance on multi-finger or path gestures without single-pointer alternatives (WCAG 2.5.1).
- **Hover-only UI:** row actions revealed on hover must also appear on focus and be available on touch.
- **Selection:** multi-select with Shift/Ctrl (Cmd) where users expect it (lists, tables, files); a "select all" with a clear scope.
- **Undo:** reversible actions offer undo (toast with Undo for ~5–10 s) instead of confirmations; ⌘Z where editors are involved.

## Criteria

<!-- BEGIN GENERATED criteria (interaction-feedback) -->
<!-- Source: criteria/interaction-feedback.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| INT-01 | Clear affordances/signifiers | Interactive elements look interactive; non-interactive ones don't | Clickable text without styling; styled non-clickables ("dead clicks") | S2 |
| INT-02 | Complete state matrix | Default/hover/focus/active/disabled/loading/selected | Missing focus or loading states on core components | S2–S3 |
| INT-03 | Correct control semantics | Button vs. link; switch vs. checkbox; radio vs. select | Mismatched control behavior | S2 |
| INT-04 | Immediate acknowledgement | Visual response ≤ 100 ms | No pressed state; clicks feel ignored, causing double clicks | S2 |
| INT-05 | Progress for longer operations | Indicators at 1 s and 10 s | No feedback during multi-second actions | S3 |
| INT-06 | Clear completion feedback | Success is confirmed proportionally | Silent success; or modal confirmations for trivial actions | S2 |
| INT-07 | Optimistic UI with rollback | Low-risk actions are instant with error rollback | Waiting spinners for trivial actions; or optimistic updates with no rollback | S2 |
| INT-08 | Motion purposeful and well-timed | Durations and easing | > 500 ms on frequent actions; linear easing; gratuitous motion | S1–S2 |
| INT-09 | Reduced motion respected | `prefers-reduced-motion` handling | Large/parallax/auto motion with no reduction | S2–S3 |
| INT-10 | No harmful flashing | Flash frequency | > 3 flashes/second | S4 (WCAG 2.3.1) |
| INT-11 | Modal behavior correct | Focus trap, Esc, focus return, scroll lock, close button | Any missing | S2–S3 |
| INT-12 | Modals used appropriately | Modals only for focused, blocking tasks | Modal for long forms, stacked modals, modal on page load | S2 |
| INT-13 | Tooltips supplementary and accessible | Hover + focus, dismissible, not essential | Essential info only in a tooltip; hover-only | S2 |
| INT-14 | Toasts well behaved | Duration, placement, error persistence, actions reachable | Errors auto-dismiss; toasts cover controls | S2–S3 |
| INT-15 | Disabled states explained | Reason visible for disabled primary actions | Disabled submit with no reason | S2 |
| INT-16 | Keyboard shortcuts discoverable and safe | Cheat sheet, tooltips, no conflicts, single-key can be disabled | Hidden or conflicting shortcuts | S1–S2 |
| INT-17 | Drag and drop has alternatives | Non-drag path exists | Reorder/move only by drag | S2–S3 (WCAG 2.5.7) |
| INT-18 | Hover-only actions reachable | Focus and touch alternatives | Actions invisible on touch or keyboard | S2–S3 |
| INT-19 | Undo for reversible actions | Undo or soft-delete | Destructive action without undo or confirmation | S3–S4 |
| INT-20 | Consistent interaction patterns | Same gesture or click → same result across the product | Double-click opens in one list but selects in another | S2 |
| INT-21 | Prevention of accidental activation | Down-event vs. up-event activation, safe spacing | Actions fire on mousedown/touchstart; accidental taps on adjacent destructive actions | S2 (WCAG 2.5.2) |
| INT-22 | Scroll behavior sane | No scroll-jacking, no nested-scroll traps, restore scroll position on back | Hijacked scroll; lost position after back | S2 |
<!-- END GENERATED criteria -->

## Code probes

- States: `:hover`, `:focus-visible`, `:focus`, `:active`, `disabled`, `aria-disabled`, `data-state=`, `aria-pressed`, `aria-selected`, `aria-expanded`.
- Wrong semantics: `<a[^>]*onClick` with no `href`; `<div[^>]*onClick`; `href="#"`; `<button` with `router.push` in onClick to navigate.
- Motion: `transition:`, `animation:`, `duration-`, `motion\.`, `animate=`, `useReducedMotion`, `prefers-reduced-motion`.
- Overlays: `Dialog`, `Modal`, `Popover`, `Tooltip`, `toast\(`, `duration:`, `autoClose`.
- Shortcuts: `useHotkeys`, `keydown`, `Mousetrap`, `cmdk`, `kbar`.
- Drag: `react-dnd`, `dnd-kit`, `draggable`, `onDragStart`, `Sortable`.

## Output

- A state matrix per core component.
- A feedback-timing table for critical actions.
- A motion inventory (duration, easing, purpose, reduced-motion handling).
- Findings in the standard format; the coverage table (INT-01 … INT-22).

## Done when

All core components have a state matrix, critical actions have feedback timing evaluated, overlays and motion are audited, and power interactions are checked for alternatives.
