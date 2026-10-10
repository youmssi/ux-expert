# Design mode: UX requirements before the backlog

Use when a product, epic or set of stories is being designed and **nothing is
built yet** (or a new feature is being added). The output is UX requirements and
testable acceptance criteria that drop into the team's stories, each tagged with
criterion IDs, so the same IDs can be checked at audit time.

## Inputs

- A brief, PRD, epics, or draft stories, in any format.
- Product type(s): `web-app`, `marketing-site`, `mobile`, `desktop`, `cli`,
  `sdk-api`, `ai-feature` (a product can have several).
- Known constraints: platforms, languages and regions, legal context
  (accessibility law, GDPR, payments), brand or design system.

If the product type, primary users or the core job are missing, ask up to 5
questions. Otherwise state assumptions and continue.

## Procedure

Progress checklist:

- [ ] 1. Frame the product
- [ ] 2. Context (light)
- [ ] 3. Design the critical flows
- [ ] 4. Select the design-phase criteria
- [ ] 5. Route each story to its areas
- [ ] 6. Write the UX acceptance criteria per story
- [ ] 7. List open product decisions
- [ ] 8. Write the UX Definition of Done
- [ ] 9. Self-check

### 1. Frame
Write the one-liner from `references/areas/context-discovery.md` (Step 1), the
product type(s), the platforms, the locales and the constraints.

### 2. Context (light)
From the brief, write the context brief of
`references/areas/context-discovery.md`: segments, ranked jobs, critical flows,
success metrics, assumptions. Keep it to one screen.

### 3. Design the critical flows
For each critical flow, write the **proposed** step table from
`references/areas/flows-friction.md` (Step 2), then apply its optimization
order: Remove → Merge → Reorder → Infer → Default → Defer. Record targets: steps,
fields, decisions, seams and time-to-value. Stories that the flow needs but the
backlog lacks (e.g. "password reset", "cancel subscription") go to step 7 as
missing stories.

### 4. Select the design-phase criteria
Run, from the skill directory:

```bash
python3 scripts/select_criteria.py --product <type> --phase design
python3 scripts/select_criteria.py --product <type> --phase design --area forms-input --area states-resilience
```

If you cannot run scripts, read `criteria/catalogue.json` and keep criteria
whose `phases` contain `design` and whose `applies_to` contains the product
type. For areas marked Light or Conditional for this product, keep only what the
stories need.

### 5. Route each story to its areas
Every story with UI gets the **baseline**: STATE, A11Y, CONT, INT. Then add areas by
what the story contains:

| The story contains | Add |
|---|---|
| A form, sign-up, sign-in, settings | FORM, TRUST (if personal data, consent or credentials) |
| A multi-step task, wizard, checkout | FLOW |
| A list, table, dashboard, search, filters | DATA, PERF |
| Navigation, a new section or page | IA, LAY |
| First-run, empty product, invitations | ONB |
| Payment, pricing, subscription, deletion | TRUST, FLOW |
| Notifications, emails | CONT, TRUST |
| Several languages or regions, dates, money | I18N |
| An AI or LLM feature | AI, TRUST |
| A public API, SDK or CLI | DX |
| Mobile or responsive screens | RESP |
| New visual components or styles | DS, COL, TYP |
| Metrics or experiments | MEAS |

### 6. Write the UX acceptance criteria
For each story, fill `assets/story-ux.md`. Rules:

- **Specific to the story.** Write the behaviour, not the criterion's name.
  ✅ "The sign-up form asks only for email and password; name and company are
  asked after the first project exists [FORM-01, FLOW-04]."
  ❌ "Only necessary fields [FORM-01]."
- **Observable and testable.** Someone else could check it with a test, a
  screenshot or a measurement. Use the thresholds from the criteria and
  `references/laws-and-numbers.md` (e.g. "contrast ≥ 4.5:1", "targets ≥ 24×24 CSS px").
- **Tagged.** Every criterion ends with its IDs in brackets.
- **Edges, not just the happy path.** Each story with UI covers, where they apply:
  empty, loading, error (with recovery), no permission, long or extreme content,
  keyboard-only, screen reader, small screen, another language.
- **5 to 15 criteria per story.** More means the story should be split; fewer
  usually means edges were skipped.
- **No implementation prescription** unless it is a UX requirement (say "the
  error names the field and how to fix it", not "use react-hook-form").

### 7. Open product decisions
A choice that belongs to the product owner (pricing model, whether guests can try
before sign-up, data retention) is never guessed. Write it as:

```
[INTERACTIVE STEP] <question>
- Option A — <trade-off, with the UX consequence and criterion IDs>
- Option B — <trade-off>
Recommendation: <A/B> because <reason tied to the user's job>.
```

Also list missing stories found in step 3.

### 8. UX Definition of Done
Run `python3 scripts/select_criteria.py --product <type> --phase build` and turn
the result into a product-level checklist that every story's PR must meet
(focus visible, labels associated, errors caught and shown, tokens used, strings
externalized…). Group by area, keep the IDs, and keep it to one page: one line per
group of related criteria, not one per criterion.

### 9. Self-check
- [ ] Every story with UI has the baseline areas covered.
- [ ] Every acceptance criterion is observable, specific and tagged.
- [ ] Every critical flow has a proposed step table with target metrics.
- [ ] Product decisions are `[INTERACTIVE STEP]`s, not assumptions.
- [ ] The Definition of Done fits on one page.

## Output

Write `ux-design-requirements.md` (or the file the user names):

```markdown
# UX requirements: <product>
## 1. Frame and context brief
## 2. Critical flows (proposed step tables and targets)
## 3. Stories
<one block per story, from assets/story-ux.md>
## 4. Open product decisions and missing stories
## 5. UX Definition of Done
## 6. Traceability (criterion ID → stories)
```

## Gotchas

- Pasting the full criteria list into each story makes the backlog unusable. Select
  for the story, then write the behaviour.
- The selector lists criteria that *can* apply. Keep only those the story actually
  touches.
- Design mode does not audit. If code already exists for a story, mention it
  and suggest an area deep-dive or refactor mode for that part.
