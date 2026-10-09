# Forms and Input (FORM)

## Senior mindset

Forms are where **business needs meet user effort**, and where most conversion is lost. A senior asks of every field: **"Who needs this, when, and what happens if we don't ask?"** Every field has a cost: time, error risk, privacy anxiety and abandonment. Baymard Institute's checkout research repeatedly finds that typical checkouts ask for far more fields than needed, and that cutting fields measurably improves completion.

Their second principle is **be generous in what you accept** (Postel's law): accept "+1 (555) 123-4567", "5551234567" and "555 123 4567" alike. Reformat for the user; never reject them for formatting.

Their third principle is **errors are the system's fault until proven otherwise**. The form should prevent errors through constraints and good defaults, catch them early (inline, at the right moment), explain them in human words next to the field, and never discard what the user typed.

## Scope

- **In:** field inventory and necessity, labels and help text, layout (single column, grouping), input types and mobile keyboards, `autocomplete` tokens, defaults and smart prefill, input masks and format tolerance, validation (timing, placement, wording), required/optional indication, error summary, submission (button state, double submit, success), multi-step forms, file upload, authentication fields (password, OTP, passkeys), search fields, long forms (save drafts).
- **Out:** flow-level necessity of the whole form (→ FLOW), visual spacing (→ LAY), screen-reader details (→ A11Y, but label association is checked here too), copy tone (→ CONT).

## Procedure

### Step 1: Inventory each form
For every form on critical flows:

| Field | Input type | Required? | Why needed (business reason) | When needed (now/later) | Could be inferred/defaulted? | autocomplete | Validation rules | Error message(s) |
|---|---|---|---|---|---|---|---|---|

Find forms through: `<form`, `useForm`, `Formik`, `react-hook-form`, `zod`/`yup` schemas, `<input`, `TextField`, `TextInput`, `FormField`.

### Step 2: Necessity and order
- Remove or defer every field that is not needed **now** (e.g. "Company size" at sign-up, "Phone" when email is enough).
- Mark what could be **inferred** (city from postal code, card type from number, country from locale/IP, name from SSO).
- Order fields logically, the way users think (name → email → password; address in the local convention).
- Group related fields with visible section headings (`fieldset`/`legend`).

### Step 3: Labels and help
- Every field has a **visible, persistent label** (placeholder is not a label: it disappears on input, often has low contrast, and screen readers may skip it).
- Labels are **top-aligned** for fastest completion (Penzo 2006); left-aligned labels are acceptable for dense settings forms on wide screens.
- Help text (format, why we ask, privacy reassurance) sits **below the label, before** input, and is programmatically linked (`aria-describedby`).
- Mark **optional** fields ("(optional)") when most are required, or mark required ones when most are optional. Do it consistently, and don't rely on a red asterisk alone without an explanation.

### Step 4: Input efficiency
- Correct `type` and `inputmode` for mobile keyboards: `email`, `tel`, `url`, `number` (only for real quantities, not for IDs, card numbers or postal codes; use `inputmode="numeric"` with `type="text"` instead), `search`, `date` (or a well-built picker).
- Correct `autocomplete` tokens (`name`, `given-name`, `email`, `tel`, `street-address`, `postal-code`, `country`, `cc-number`, `cc-exp`, `cc-csc`, `username`, `current-password`, `new-password`, `one-time-code`). This is also WCAG 1.3.5 (AA).
- Turn off `autocorrect`/`autocapitalize` on emails, usernames and codes; `spellcheck="false"` for codes.
- **Defaults:** sensible, safe and in the user's interest (country from locale; never pre-checked marketing consent).
- **Masks:** forgiving. Allow paste; don't block typing separators; format as you type only if the caret behaves well.
- Choice fields: radios for ≤ 5 options, a select or searchable combobox for many, and country and state lists searchable.
- Field width hints the expected length (postal code short, address long).

### Step 5: Validation
- **Timing:** validate on **blur** (after the user leaves the field) or on submit, not on every keystroke for format rules (it yells at users mid-typing). Exceptions: positive confirmation such as password strength or username availability, which can be live.
- Once a field is in an error state, **re-validate as the user types**, so the error disappears as soon as it's fixed.
- **Placement:** the error appears next to the field (below it, usually), with an icon and text (not color alone), and is linked via `aria-describedby`. `aria-invalid="true"` is set.
- **On submit with errors:** focus moves to the first error field, or to an **error summary** at the top that lists links to each invalid field (for long forms).
- **Messages:** say what's wrong and how to fix it, in the user's terms: "Enter a date in the future, like 12/31/2026" ✅ vs. "Invalid input" ❌.
- **Server errors** map back to fields where possible; never wipe the form.
- Client and server validation rules match (no "the client accepted it, the server rejects it" surprises).

### Step 6: Submission
- The submit button label states the outcome ("Create account", "Pay $49"), not "Submit".
- Submitting shows a loading state on the button, prevents double submission, and keeps the inputs.
- Success leads to a clear next state (→ FLOW-20).
- **Enter key** submits single-line forms; multi-line text areas don't submit on Enter unless that is the convention (chat inputs: Enter sends, Shift+Enter adds a new line; make it discoverable).

### Step 7: Special inputs
- **Passwords:** show/hide toggle; the rules shown **before** typing; paste allowed; password managers work (`autocomplete="new-password"`/`current-password`, a correct `name` and `id`, and a username field present, even hidden, for managers to pair). No arbitrary maximum length below 64. Follow NIST SP 800-63B: length over complexity rules, check against breached lists, no forced periodic rotation.
- **OTP codes:** a single input or segmented boxes that accept paste of the full code; `autocomplete="one-time-code"`; resend with a cooldown timer; don't force users to memorize or transcribe across devices without an alternative (WCAG 3.3.8).
- **Passkeys / SSO:** offered where possible to remove password friction.
- **File upload:** drag & drop **and** a button; accepted types and size limits stated up front; progress per file; errors per file; preview; remove/replace; large files resumable.
- **Dates:** a picker with typed entry fallback; locale format shown; a range picker for ranges; no impossible dates; time zone stated when relevant.
- **Long forms:** autosave drafts, progress, sections, and "save and continue later".
- **CAPTCHA:** avoid it where possible (use invisible or risk-based checks); if present, an accessible alternative is required.

## Criteria

<!-- BEGIN GENERATED criteria (forms-input) -->
<!-- Source: criteria/forms-input.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| FORM-01 | Only necessary fields, asked when needed | Necessity table | Removable or deferrable fields on critical forms | S2–S3 |
| FORM-02 | Visible persistent labels | Every input has a label | Placeholder-only labels | S3 (→ A11Y) |
| FORM-03 | Label/help association | `for`/`id`, `aria-describedby` | Unassociated labels or help | S2–S3 |
| FORM-04 | Single-column logical layout | Layout of critical forms | Multi-column forms causing skipped fields (exception: short related pairs such as city/postal) | S2 |
| FORM-05 | Correct input types and keyboards | `type`, `inputmode` | Wrong keyboards on mobile; `type=number` for codes | S2 |
| FORM-06 | Autocomplete tokens | `autocomplete` attributes | Missing on personal, address, payment or credential fields | S2 (WCAG 1.3.5) |
| FORM-07 | Format tolerance | Accept spaces, dashes, parentheses; trim whitespace; case-insensitive emails | Rejects valid input over formatting | S2–S3 |
| FORM-08 | Smart, safe defaults | Defaults present and in the user's interest | No defaults; or defaults against the user (pre-checked consent) | S2 (S3+ if it is a dark pattern; → TRUST) |
| FORM-09 | Validation timing | On blur/submit; live re-validation after an error | Errors on first keystroke; validation only server-side after a round trip | S2 |
| FORM-10 | Error placement and clarity | Inline, specific, with fix guidance | Generic "Invalid" or "Error"; errors only at the top | S2–S3 |
| FORM-11 | Error focus management | Focus to first error or summary on submit | Errors appear off-screen with no focus change | S2–S3 |
| FORM-12 | Input preserved on error | Data retained after server or validation errors | Form cleared | S3 |
| FORM-13 | Required/optional clear | Consistent marking with a legend | Ambiguous or color-only asterisk | S2 |
| FORM-14 | Submit labeled by outcome | Button copy | "Submit", "OK", "Continue" where the outcome matters (payments) | S1–S2 |
| FORM-15 | Double-submit prevention | Loading/disabled during submit; idempotency | Multiple records or charges | S3–S4 |
| FORM-16 | Password field usability | Show/hide, rules upfront, paste, manager support, sane max length | Paste blocked; rules revealed only after failure | S2–S3 |
| FORM-17 | OTP/verification usability | Paste whole code, `one-time-code`, resend with timer | Six boxes that break paste; no resend | S2–S3 |
| FORM-18 | Accessible authentication | No cognitive tests without alternatives; CAPTCHA alternatives | Inaccessible CAPTCHA blocks sign-up | S3–S4 (WCAG 3.3.8) |
| FORM-19 | File upload clarity | Limits upfront, progress, per-file errors, alternatives to drag | Silent failures on large or invalid files | S2–S3 |
| FORM-20 | Date/time input usability | Typed + picker; locale; time zone | Picker-only with tedious year navigation; ambiguous formats (03/04) | S2 |
| FORM-21 | Long-form resilience | Autosave and resume | Long form lost on timeout or navigation | S3 |
| FORM-22 | No redundant entry | Previously given info isn't asked again; billing = shipping option | Re-asking known data | S2 (WCAG 3.3.7) |
| FORM-23 | Client/server rule parity | Shared schema or matching rules | Client passes, server rejects with a different message | S2 |
| FORM-24 | Enter-key behavior | Submits single-line forms; documented in chat or multi-line inputs | Enter does nothing, or unexpectedly submits a multi-line field | S1–S2 |
<!-- END GENERATED criteria -->

## Code probes

- Placeholder-as-label: `<input[^>]*placeholder=` in an element with no `<label`, `aria-label` or `aria-labelledby` nearby.
- Missing autocomplete: `<input[^>]*type="(email|tel|password)"(?![^>]*autocomplete)`.
- Wrong numeric type: `type="number"` on `zip|postal|card|cvc|otp|code|phone`.
- Paste blocking: `onPaste.*preventDefault`, `onpaste="return false"`.
- Validation mode: `mode: 'onChange'` (react-hook-form) on format-heavy forms; `reValidateMode`.
- Error props: `aria-invalid`, `aria-describedby`, `errors\.`.
- Submit handling: `isSubmitting`, `disabled={`, `Idempotency-Key`.

## Gotchas

- react-hook-form defaults to `mode: 'onSubmit'` with `reValidateMode: 'onChange'`: errors appear only on submit. FORM-09 needs `mode: 'onBlur'` or `'onTouched'`.
- `type="number"` drops leading zeros and accepts `e`. For codes, card numbers and postal codes use `type="text"` with `inputmode="numeric"`.
- Password managers need a username or email field in the same form, even a hidden one, to save the credentials.
- Native validation bubbles are inconsistent across browsers. A form with `noValidate` and custom inline errors is the intended pattern, not a bug.

## Output

- A field inventory table per form, with proposed removals, inferences and deferrals.
- A validation behavior summary per form.
- Findings in the standard format; the coverage table (FORM-01 … FORM-24).

## Done when

All forms on critical flows are inventoried, every field has a necessity verdict, and validation, submission and special inputs are checked (runtime when possible).
