# In-Product Help and Support (HELP)

## Senior mindset

Help is part of the product, not a website next to it. The best help appears **where the difficulty is**, answers the question in the user's words, and, when it can't, hands the user to a person **without making them start over**. A senior reads support tickets as a list of design defects: each frequent ticket is a missing affordance, label or self-serve path.

Principles:
1. **Same place, every page.** Users should not hunt for help; WCAG 2.2 requires consistent placement of help mechanisms [src:wcag22].
2. **Context in, context out.** Help knows where the user is; support receives what the user was doing.
3. **Self-serve first, human always reachable** for people who pay.
4. **Help stays true.** Articles that name old buttons are worse than none.

## Scope

- **In:** help entry points, contextual help, in-product search of help content, help deep links, tooltips as help, help in empty and error states, contact and chat, support handoff, error references, what's new, shortcut help, AI help assistants, help analytics, incident notices.
- **Out:** onboarding tours and checklists (→ ONB), microcopy of labels and errors (→ CONT), the public help center and status page as launch assets (→ LAUNCH-11, LAUNCH-13), AI chat design in general (→ AI).

## Procedure

### Step 1: Find the entry points
On every critical route, note where help, contact or chat appears (header, footer, floating widget, menu). Different places or missing on some routes is HELP-01. Search for widget scripts (`intercom`, `zendesk`, `crisp`, `helpscout`, `drift`, `plain`, `chatwoot`) and where they are mounted or excluded.

### Step 2: Ask the top questions
Take the 5 most likely questions from CTX (or from support tags if available). For each: can the user find the answer inside the product, how many steps, and does the answer match the current interface (HELP-02, HELP-03, HELP-12)?

### Step 3: Dead ends
Trigger an error and open an empty state: is there a help link or next step (HELP-06)? Does the error show a reference the user can quote (HELP-09)?

### Step 4: Reach a person
From the product, contact support: is the path visible, is the response time stated, and does the ticket include the page, account and error without the user retyping them (HELP-07, HELP-08)?

### Step 5: AI help (if present)
Ask a question the docs answer, one they don't, and one about a feature that doesn't exist. The assistant cites sources, says when it doesn't know, does not invent features, and offers a person (HELP-13).

### Step 6: Change and incidents
Is there a what's-new entry for recent interface changes (HELP-10)? During an incident, does the product show a notice linking the status page (HELP-15)?

## Criteria

<!-- BEGIN GENERATED criteria (in-product-help) -->
<!-- Source: criteria/in-product-help.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| HELP-01 | Help in a consistent place (3.2.6) | Help, contact or chat in different places across pages, or missing on some | S2–S3 (S3 where accessibility law applies; → A11Y-26) |
| HELP-02 | Help at the point of difficulty | Users must leave the task to understand a complex field or step | S2 |
| HELP-03 | Help searchable in the product | Only a link to the documentation home page | S2 |
| HELP-04 | Help links land on the right answer | Links open a generic help center instead of the relevant article | S1–S2 |
| HELP-05 | Essential instructions not hidden in tooltips | Information needed to complete the task only in a tooltip | S2 (→ INT-13) |
| HELP-06 | Error and empty states link to help | Dead-end states with no help or next step | S2 (→ STATE-08, STATE-02) |
| HELP-07 | Human support reachable | Paying users cannot find a contact path or expected response time | S2–S3 (→ LAUNCH-12) |
| HELP-08 | Support handoff carries context | Users must repeat the page, account and error to support | S2 |
| HELP-09 | Errors carry a reference users can quote | Errors with no ID that support can trace | S2 |
| HELP-10 | Changes announced in the product | Interface changes with no what's-new note or changelog | S1–S2 (→ ONB-18) |
| HELP-11 | Shortcuts and commands discoverable | Shortcuts exist but are listed nowhere in the product | S1 (→ INT-16) |
| HELP-12 | Help matches the current interface | Articles name buttons, menus or screens that no longer exist | S2 |
| HELP-13 | AI help grounded and escalates | Assistant answers without sources, invents features or cannot hand over to a person | S2–S3 (→ AI) |
| HELP-14 | Help usage measured | No data on help searches without results or the most used articles | S1–S2 (→ MEAS) |
| HELP-15 | Incidents surfaced in the product | During an outage the product shows nothing; users learn from errors | S2 (→ LAUNCH-13) |
| HELP-16 | Self-serve paths for top support reasons | The most common support requests have no self-serve path | S2 |
<!-- END GENERATED criteria -->

## Gotchas

- Support widgets are often excluded from checkout, onboarding or settings routes to "reduce distraction", which breaks consistent help (HELP-01) exactly where users struggle. Check the exclusion list in the widget config.
- Floating chat launchers sit bottom-right and cover primary actions and cookie banners on mobile; check overlap at 375 px (→ LAY-16).
- A help center on another domain usually loses the user's route and account; the "help" link then opens the help home page (HELP-04). Check whether the link passes context.
- Tooltips are not available on touch devices without a tap and are often skipped by screen readers when they are attached to non-focusable elements; essential guidance there is HELP-05.

## Output

- The help entry-point table per critical route.
- The top-questions table: question, where answered, steps, accurate (y/n).
- Findings in the standard format; the coverage table (HELP-01 … HELP-16).

## Done when

Entry points are checked on every critical route, the top questions are answered or marked unanswerable in the product, and the path to a person is walked end to end.
