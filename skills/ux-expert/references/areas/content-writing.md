# Content and UX Writing (CONT)

## Senior mindset

A senior knows **the interface is mostly words**. Strip the text from most products and they become unusable; strip the styling and they mostly still work. Content is design.

Their tests for every string:
1. **Is it clear to this user right now?** Plain words, no jargon, no internal names.
2. **Is it useful?** Does it help the user decide or act? Remove anything that doesn't.
3. **Is it consistent?** One word per concept, one pattern per situation, everywhere.
4. **Is it human?** The tone fits the moment: calm in errors, celebratory only for real milestones, never blaming or cute when users are stressed.

They read the whole string catalog **as one document**, because drift (Sign in / Log in / Login; Workspace / Team / Organization) only becomes visible when you see everything together.

## Scope

- **In:** labels and buttons, headings and titles, helper and instructional text, placeholders, empty-state copy, error messages, success and confirmation messages, destructive confirmations, tooltips, onboarding copy, notification text (in-app, push, email, SMS), email templates (transactional), legal/consent microcopy (clarity only; ethics → TRUST), inclusive language, readability level, capitalization and punctuation style, number/date presentation in text (locale → I18N).
- **Out:** marketing site persuasion copy (→ LAUNCH for the GTM surface), developer error messages (→ DX), localization mechanics (→ I18N).

## Procedure

### Step 1: Build the string inventory
- If i18n catalogs exist (`locales/*.json`, `messages/*.po`, `*.arb`, `Localizable.strings`, `strings.xml`): export all keys and values for the default language.
- Otherwise extract the literals from templates/JSX (see the code probes), plus `aria-label`, `title`, `placeholder` and `alt` values, toast and dialog content, and email templates.
- Categorize each string: label · button · heading · help · empty · error · success · confirm · notification · email · legal.

### Step 2: Terminology audit
- Build a **glossary**: each concept → the term used → variants found → count. Cross-check with CTX's vocabulary map and the data model.
- Flag synonyms for one concept, and one term used for two concepts.
- Flag internal jargon or engineering terms leaking to users ("entity", "payload", "null", "sync failed (code 0x80…)", "tenant", "instance", "invalid state", "deprecated").
- Recommend a **canonical glossary** (term, definition, do/don't use).

### Step 3: Actions and buttons
- Buttons say what they do: **verb + object** ("Create project", "Send invite"), typically 1–3 words.
- The confirmation dialog's buttons repeat the action ("Delete project" / "Cancel"), never "Yes" / "No" or "OK" / "Cancel" for destructive actions.
- Link text makes sense out of context (no "click here", "learn more" repeated 10 times without context; WCAG 2.4.4).
- The same action has the same label everywhere (no Save / Update / Apply / Confirm for the same operation).

### Step 4: Error messages
Each error message must have:
1. **What happened** in user terms ("We couldn't save your changes").
2. **Why**, if known and useful ("because you're offline").
3. **What to do** ("They're stored on this device and will sync when you're back online" / "Try again" / "Contact your admin to get access").

Plus: no blame ("You entered an invalid…" → "Enter a date after today"), no technical codes as the main message (codes can be secondary, for support), no ALL CAPS, no exclamation marks, no jokes in errors, and the exact field or object named.

### Step 5: Empty, success and confirmation copy
- **Empty:** what this space is for, the value, and the action ("No invoices yet. Create your first invoice to get paid faster.").
- **Success:** confirm what happened, with specifics ("Invite sent to ana@acme.com"), and the next step where useful.
- **Destructive confirmations:** name the object, state the consequence and reversibility ("Delete 'Q3 Budget'? This deletes 14 sheets and can't be undone.").

### Step 6: Help and instructional text
- Front-load key words; one idea per sentence; ≤ 2 lines for inline help.
- Explain **why** you ask for sensitive data ("We use your phone only for login codes").
- Avoid redundant help that repeats the label.

### Step 7: Tone, voice and style consistency
- Identify (or infer) the voice: e.g. "clear, calm, confident, friendly". Check it is applied consistently, and that tone adapts to context (neutral in errors, warm in onboarding, precise in billing).
- Mechanics: capitalization (sentence case recommended for UI), punctuation (no periods on short labels, periods on full sentences), numerals vs. words, Oxford comma, date/time formats in text, abbreviations, "you" vs. "we" usage.
- Person: avoid mixing "my account" and "your account" in the same UI.

### Step 8: Readability and inclusivity
- Target **plain language**: roughly grade 7–9 reading level for general consumer products (estimate with Flesch–Kincaid on longer text). Simpler for critical instructions.
- Avoid idioms and culture-specific metaphors (they translate badly → I18N).
- Inclusive language: gender-neutral ("they"), no ableist metaphors ("blind spot", "crippled", "sanity check" are commonly flagged), no unnecessary gendered defaults, and respectful naming of people (allow single names, don't assume first/last).

### Step 9: Notifications and emails
- Each notification: a clear trigger, the value to the user, the action, and how to control or unsubscribe.
- Subject lines specific ("Your invoice #1043 from Acme is due Friday" vs. "Notification").
- The email sender name is recognizable; plain-text versions exist; links go to the exact object; the footer explains why the user got it.
- Frequency and batching: no notification spam (digest options).

## Criteria

<!-- BEGIN GENERATED criteria (content-writing) -->
<!-- Source: criteria/content-writing.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| CONT-01 | One term per concept | Synonyms or overloaded terms across the UI | S2 |
| CONT-02 | No internal jargon | Engineering or internal words visible to users | S2 |
| CONT-03 | Buttons are verb + object, specific | "Submit", "OK", "Yes/No", vague labels | S2 |
| CONT-04 | Same action, same label | Save/Update/Apply inconsistency | S1–S2 |
| CONT-05 | Descriptive link text | "Click here", ambiguous "Learn more" | S2 (WCAG 2.4.4) |
| CONT-06 | Errors: what + why + what to do | "Something went wrong", raw codes, stack traces | S2–S3 |
| CONT-07 | No blame, no humor in errors | "You failed to…", "Oops! 🙈" on serious failures | S1–S2 |
| CONT-08 | Empty states explain value and action | "No data" | S2 |
| CONT-09 | Success messages specific | Generic "Success!" | S1 |
| CONT-10 | Destructive confirmations specific | No object name, consequence or reversibility | S2–S3 |
| CONT-11 | Help text concise and purposeful | Long paragraphs; repeating labels; missing "why we ask" | S1–S2 |
| CONT-12 | Consistent style mechanics | Mixed casing, punctuation, date formats in text | S1 |
| CONT-13 | Tone fits context | Cheerful tone in failures or billing; robotic in onboarding | S1–S2 |
| CONT-14 | Plain-language readability | Complex sentences in critical instructions | S2 |
| CONT-15 | Inclusive language | Gendered defaults; ableist terms; name-format assumptions | S2 |
| CONT-16 | Scannable copy | Front-loaded words; headings; bullets for lists | S1–S2 |
| CONT-17 | Notification content useful and controllable | Vague notifications; no settings or unsubscribe | S2 (for consent; → TRUST) |
| CONT-18 | Transactional emails clear | Generic subjects; broken deep links; no plain text | S2 |
| CONT-19 | Placeholder text not carrying critical info | Instructions only in the placeholder | S2 (→ FORM) |
| CONT-20 | Numbers, units and currency explicit | "Price: 49" without currency; ambiguous units | S2–S3 |
| CONT-21 | Glossary/style guide exists | No source of truth for terms and voice | S1 |
<!-- END GENERATED criteria -->

## Code probes

- Generic copy: `Something went wrong|An error occurred|Oops|Invalid input|Error!|Success!|Click here|Submit\b|>OK<`.
- JSX literals (when no i18n): `>\s*[A-Z][^<>{}]{3,}\s*<`, `(title|placeholder|aria-label|alt)=["'][^"']+["']`.
- Toasts/dialogs: `toast\((['"\`])`, `confirm\(`, `alert\(`, `<Dialog.Title>`.
- Emails: `emails/`, `templates/`, `subject:`.
- Jargon scan: `\b(entity|payload|null|undefined|NaN|tenant|instance|config|param|invalid state|exception)\b` inside user-facing strings.

## Gotchas

- Message catalogs often contain unused keys. Check that a string is used before reviewing its wording.
- Error text shown in the UI often comes straight from the API response. Trace where a message comes from before rewriting it.
- Sentence case versus title case is a style choice. Flag inconsistency (CONT-12), not the choice.
- Product names and legal wording are usually fixed. Flag clarity problems, and mark them as needing a product or legal decision.

## Output

- A terminology glossary table (concept · canonical term · variants found · locations).
- Rewrite suggestions: a before → after table for the worst strings (at least all errors on critical flows).
- Findings in the standard format; the coverage table (CONT-01 … CONT-21).

## Done when

The full string inventory has been reviewed, the glossary has been produced, every error message on critical flows has been checked against the what/why/what-to-do formula, and rewrites have been proposed for every failing string on critical flows.
