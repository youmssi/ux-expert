# Refactor mode: a safe plan for a deep UX refactor

Use when the product already exists and the team wants to **fix its UX in
depth**: many findings, systemic causes, and code that must keep working while
it changes. The output is a sequenced plan of stories, each shippable on its
own, each closing named findings and protected by a regression guard.

An audit says *what* is wrong. Refactor mode says **in what order to fix it,
so that no step is redone and nothing that works breaks.**

## Inputs

- An audit report from this skill (any audit mode), or run one first. Without
  findings, there is nothing to plan.
- The team's constraints: team size, release cadence, freeze dates, feature-flag
  support, test tooling (unit, end-to-end, visual regression, axe).
- The team's story template, if any (otherwise use the one in the output section).

## Procedure

Progress checklist:

- [ ] 1. Get the findings
- [ ] 2. Group by root cause
- [ ] 3. Classify the workstreams
- [ ] 4. Build the dependency graph
- [ ] 5. Sequence
- [ ] 6. Design each story's safety
- [ ] 7. Write the stories
- [ ] 8. Define how success is measured
- [ ] 9. Self-check

### 1. Get the findings
Use the report's findings with their IDs, priorities, root causes and
**strengths to protect**. If no report exists, run the audit procedure in
`SKILL.md` first (full audit, or a scoped audit for the area being refactored).

### 2. Group by root cause
One root cause can explain dozens of findings (Phase 5–6 of the audit). For each
group, write: the cause, the findings it explains (count and IDs), and the fix
that removes the cause. Examples:

| Root cause | Typical findings it explains |
|---|---|
| No semantic tokens | COL-08, COL-16, LAY-05, TYP-02, DS-03, dark-mode gaps |
| No shared form field component | FORM-02, FORM-03, FORM-10, FORM-11, A11Y-10, inconsistent validation |
| No error boundary or error pattern | STATE-07, STATE-08, STATE-10, CONT-06 |
| No i18n layer | I18N-01, I18N-03, I18N-12, I18N-14 |
| Flow designed around the database, not the job | FLOW-02, FLOW-03, FLOW-06, ONB-03 |

### 3. Classify the workstreams
Put each group into one class. The class decides its place in the sequence:

1. **Safety**: P0 findings that hurt users now (data loss, legal exposure, a
   blocked critical flow). Fix them first with the smallest safe change, even if a
   foundation will later replace that code.
2. **Foundations**: the systems that remove root causes (tokens, shared
   components, error handling, i18n layer, analytics events). They change little on
   screen by themselves.
3. **Systemic migrations**: moving screens onto the foundations, one screen or
   one area at a time.
4. **Flow redesigns**: journey-level changes (fewer steps, new order), done once
   the screens they touch sit on the foundations.
5. **Polish**: P2/P3 items left after the above.

### 4. Build the dependency graph
Draw an edge A → B when doing B before A would mean redoing B. Typical edges:
tokens → color, spacing and typography fixes; form field component → every form
fix; error pattern → every error-state fix; event taxonomy → funnel metrics.
List the graph as text (`A → B`) or as a Mermaid diagram.

### 5. Sequence
Order the stories:
1. Safety stories.
2. **Guard stories** that write characterization tests for the strengths to
   protect and the critical flows (end-to-end flow tests, visual snapshots, axe
   checks), so later changes cannot regress them silently.
3. Foundations, in graph order.
4. Systemic migrations, ordered by priority × reach of the findings they close.
   Critical-flow screens go first.
5. Flow redesigns.
6. Polish.

Interleave **quick wins** (P0–P2 with XS/S effort that touch no foundation)
wherever there is capacity: they show progress early.

### 6. Design each story's safety
Every story must be:
- **Shippable alone**: no long-lived branch. For a new component or pattern, use
  expand → migrate → contract: add the new one next to the old one, move the
  screens one by one, then delete the old one in its own story.
- **Behind a flag** when it changes a critical flow, with a rollback path.
- **Guarded**: name the test that fails if it regresses (visual snapshot, axe,
  end-to-end flow, unit test on the shared component). With Playwright, start from
  the recipes in `references/stacks/playwright.md` (ARIA snapshot, focus return,
  axe scan, accessible error message, error and offline states, session expiry,
  dark mode, reflow); they compile against the version the pack was verified with.
- **Verified**: how to confirm the findings are closed (the audit criterion check,
  a measurement, a before/after screenshot).

### 7. Write the stories
Use the team's template, or the one below. Each story lists the findings it closes
(by finding ID and criterion ID) and the stories it depends on.

### 8. Define how success is measured
For each workstream, write a hypothesis from
`references/areas/measurement-validation.md` (Step 7): baseline, target, and
how it is measured (e.g. sign-up completion, error rate, axe violations, token
adoption rate). Measure the baseline **before** the first story ships.

### 9. Self-check
- [ ] Every P0 finding is in a safety story or an early story.
- [ ] Every root cause has a foundation story that comes before the fixes that depend on it.
- [ ] Every story is shippable alone, guarded, and verifiable.
- [ ] Every strength to protect has a guard.
- [ ] Every finding is in exactly one story, or is explicitly deferred with a reason.

## Output

Write `ux-refactor-plan.md` (or the file the user names):

```markdown
# UX refactor plan: <product>
## 1. Summary (findings, root causes, number of stories, expected outcome)
## 2. Root causes and workstreams
## 3. Dependency graph
## 4. Sequence
| # | Story | Class | Closes | Depends on | Guard | Size |
## 5. Stories
## 6. Measures (baseline → target)
## 7. Deferred findings (with reasons)
```

Story template, when the team has none:

```markdown
### <KEY>-<n> — <title in the user's words>
**Class:** safety | guard | foundation | migration | flow | polish · **Depends on:** <keys> · **Size:** S | M | L
**Closes:** <finding IDs> (<criterion IDs>)
**Why:** <user impact of the findings, from the audit>
**Change:** <what changes, where>
**Guard:** <test that fails if this regresses>
**Verify:** <how the findings are confirmed closed>
**Rollback:** <flag or revert path, for critical flows>
```

## Gotchas

- A big-bang redesign is not a plan. If a story cannot ship alone, split it.
- Fixing screens one by one before the foundation exists doubles the work. Check
  the dependency graph first.
- Safety beats sequence: a P0 data-loss bug is fixed now, even in code a
  foundation will later replace.
- Write the guards before the change, not after. A guard written after a
  regression only records the regression.
