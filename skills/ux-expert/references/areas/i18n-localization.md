# Internationalization and Localization (I18N)

## Senior mindset

A senior knows that **i18n is architecture and l10n is content**. If the architecture is wrong (concatenated strings, hard-coded formats, physical left/right CSS), every new language becomes a rewrite. So even for an English-only launch, they check whether the product is **i18n-ready**, because retrofitting costs far more later.

They also know that localization is not translation. It is **meeting local expectations**: date order (03/04 is March 4 in the US and April 3 in most of Europe), decimal separators (1,234.56 vs. 1.234,56 vs. 1 234,56), name order, address formats, phone formats, currencies, week start days, payment methods, imagery and color meanings, and legal requirements.

Text expansion is the most common visible breakage: German and Finnish run long, short English labels can double or triple in some languages, and Chinese/Japanese can shrink but need different line-breaking rules and larger font sizes for readability.

## Scope

- **In:** externalized strings, message format (ICU) for plurals/select/gender, no concatenation, context for translators, text expansion and truncation resilience, RTL (Arabic, Hebrew, Persian, Urdu) mirroring and bidirectional text, `lang`/`dir` attributes, locale-aware formatting (`Intl` APIs or equivalents) for dates, times, relative times, numbers, percentages, currencies, units and lists, time-zone handling, names/addresses/phones, sorting and search collation, fonts and script coverage (CJK, Devanagari, Arabic), locale detection, switching and persistence, localized URLs and SEO (`hreflang`), localized emails and notifications, local payment methods, and cultural review of icons, imagery and color.
- **Out:** copy quality in the source language (→ CONT), general layout (→ LAY).

## Procedure

### Step 1: Determine the target
From CTX: current and planned locales and regions. If English-only with no plans, run **Light** (readiness check plus formatting correctness for international users of the English UI: currencies, time zones and dates still matter).

### Step 2: String externalization
- Is there an i18n library and catalogs? What percentage of user-facing strings go through it? (Count literals in JSX/templates vs. `t(`/`<Trans>`/`intl.formatMessage` calls.)
- Strings in **non-UI places**: emails, push notifications, server error messages, PDF exports, `<title>`/meta tags, `alt`/`aria-label`, validation schemas (zod/yup messages), toasts, and enum labels mapped from the backend.

### Step 3: Message construction
- **Concatenation** breaks grammar in other languages: `"You have " + n + " items"`, `t('hello') + name`. Use full messages with placeholders.
- **Plurals:** ICU plural rules (`{count, plural, one {# item} other {# items}}`). Languages have 1–6 plural forms (e.g. Arabic has 6); `n === 1 ? 'item' : 'items'` is wrong for many.
- **Gender/select** where grammar requires it.
- **Context/descriptions** for translators (the same English word "Open" can be a verb or an adjective).
- **No text in images**; no layout-dependent sentence fragments (e.g. a sentence split across a link and plain text in a way that can't be reordered).

### Step 4: Text expansion and layout resilience
- Pseudo-localize if possible (e.g. accented and ~30–40% expanded strings, like `[Ŝéţţîñĝš ~~~~]`) and screenshot critical screens. Otherwise inspect fixed widths on buttons, tabs, nav items, table headers and badges.
- Buttons and labels grow, wrap gracefully, or truncate with access to the full text (→ TYP-12).
- Avoid fixed-height containers for text.

### Step 5: RTL support (if RTL locales are targeted or planned)
- `dir="rtl"` on `<html>` (or the container) is set per locale.
- **Logical CSS properties:** `margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`, and Tailwind `ms-/me-/ps-/pe-/start-/end-` instead of `ml-/mr-/left-/right-`.
- Directional icons mirror (back/forward arrows, progress direction); non-directional ones do not (play button, checkmarks, clocks, logos).
- Bidirectional text: user-generated content mixing scripts is isolated (`<bdi>`, `unicode-bidi: isolate`, `dir="auto"` on inputs).
- Charts and timelines: decide whether the direction mirrors.

### Step 6: Locale-aware formatting
- Dates and times: `Intl.DateTimeFormat`/`toLocaleDateString` with options, or libraries (date-fns with locales, Luxon, Day.js plugins). There should be no hard-coded `MM/DD/YYYY`. Show unambiguous formats in critical contexts ("Mar 4, 2026" or ISO for technical users).
- **Time zones:** store in UTC, display in the user's zone (or the event's zone, labeled); scheduling products show zone names explicitly; DST transitions handled.
- Numbers, percentages and currencies: `Intl.NumberFormat` with `style: 'currency'` and the correct currency code; no `'$' + amount.toFixed(2)`. Currency is not derived from language alone (an English UI can serve EUR customers).
- Relative time (`Intl.RelativeTimeFormat`), lists (`Intl.ListFormat`), units (`Intl.NumberFormat` `style: 'unit'`), and measurement systems (metric/imperial).
- Week start (Sunday vs. Monday), calendar systems if relevant.
- Sorting/search: `Intl.Collator` or locale-aware collation for user-visible sorted lists; accent-insensitive search.

### Step 7: Personal data formats
- **Names:** a single "Full name" field, or flexible fields; no forced first/last split; support for long names, single names, non-Latin characters and apostrophes/hyphens.
- **Addresses:** country-first, then country-specific fields (postal code optional where not used; state/province lists per country). Libraries such as Google's address metadata (libaddressinput) help.
- **Phone numbers:** a country code selector plus a forgiving input; store in E.164 (libphonenumber).

### Step 8: Locale selection and persistence
- Detection from `Accept-Language`/device settings, with an **explicit, easy override** (a language switcher showing language names in their own language: "Deutsch", not "German"; don't use flags for languages).
- Persistence across sessions, devices and emails.
- Fallback chain (e.g. `pt-BR` → `pt` → `en`) without showing raw keys.
- Localized URLs and `hreflang` for marketing/SEO surfaces (→ LAUNCH).

### Step 9: Fonts, scripts and cultural review
- Fonts include the glyphs required (or a fallback stack per script); line height suits scripts with tall glyphs (Thai, Devanagari, Arabic).
- CJK: no letter spacing; appropriate line-breaking (`word-break: keep-all` for Korean where appropriate); avoid italics.
- Cultural review: icons (mailbox, piggy bank), hand gestures, colors (red can mean prosperity or danger), imagery, examples (names, currencies, holidays), and humor.

## Criteria

<!-- BEGIN GENERATED criteria (i18n-localization) -->
<!-- Source: criteria/i18n-localization.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| I18N-01 | Strings externalized | Hard-coded UI strings (in multi-locale products) | S2–S3 |
| I18N-02 | Non-UI strings localized | Emails, notifications, server errors, meta, alt text only in English | S2 |
| I18N-03 | No concatenation | Sentences built from fragments | S2 |
| I18N-04 | Correct plural/gender handling | Binary `n === 1` logic; no ICU | S2 |
| I18N-05 | Translator context | Ambiguous keys without descriptions | S1 |
| I18N-06 | No text in images | Text baked into images | S2 |
| I18N-07 | Expansion-resilient layout | Fixed-width labels clip under pseudo-localization | S2 |
| I18N-08 | `lang` and `dir` set correctly | Missing or not updated per locale | S2–S3 (S3 where accessibility law applies, e.g. EU EAA, ADA, Section 508; → A11Y-28) |
| I18N-09 | Logical CSS properties (RTL) | Physical left/right properties throughout | S2–S3 (if RTL targeted) |
| I18N-10 | Icon mirroring rules | Arrows not mirrored, or logos mirrored | S1–S2 |
| I18N-11 | Bidi isolation for user content | Garbled mixed-direction text | S2 |
| I18N-12 | Locale-aware dates and times | Hard-coded formats; ambiguous numeric dates | S2–S3 |
| I18N-13 | Time zones correct and explicit | Wrong times; zone not shown in scheduling | S3 |
| I18N-14 | Locale-aware numbers and currencies | Hard-coded symbols or separators; currency inferred from language | S2–S3 |
| I18N-15 | Units and measurement systems | Imperial/metric not adapted where it matters | S1–S2 |
| I18N-16 | Locale-aware sorting and search | ASCII sort for names; accent-sensitive search | S1–S2 |
| I18N-17 | Flexible names, addresses, phones | Forced first/last; US-only address form; rigid phone format | S2–S3 |
| I18N-18 | Locale switching and persistence | No override; flags for languages; preference lost | S2 |
| I18N-19 | Graceful fallback | Raw keys (`checkout.title`) shown | S2 |
| I18N-20 | Localized URLs and hreflang (marketing) | Missing for multi-locale sites | S1–S2 |
| I18N-21 | Script/font coverage | Tofu boxes (□); poor rendering for target scripts | S2–S3 |
| I18N-22 | Cultural appropriateness | Culturally confusing or offensive imagery, icons or examples | S1–S3 |
| I18N-23 | Local payment and legal norms (commerce) | Only card payments where local methods dominate; missing local legal info | S2–S3 (S3 where local legal information is required) |
<!-- END GENERATED criteria -->

## Code probes

- Literals vs. i18n calls: count `t\(['"]`, `<Trans`, `formatMessage`, `\$t\(`, `i18n\.` vs. JSX literals (see the CONT probes).
- Concatenation: `t\([^)]*\)\s*\+`, `\+\s*t\(`, template literals mixing `t(` and words.
- Binary plurals: `=== 1 \? ['"]`, `count > 1 \?`.
- Hard-coded formats: `MM/DD/YYYY|DD/MM/YYYY|toLocaleDateString\(\)` (no locale argument), `format\(['"][^'"]*(MM|dd)`, `'\$'\s*\+`, `toFixed\(2\)` near currency.
- Physical CSS: `\b(ml|mr|pl|pr|left|right)-\d`, `margin-left|margin-right|padding-left|padding-right|text-align:\s*(left|right)|float:\s*(left|right)`.
- `dir=`, `lang=`, `<bdi`, `dir="auto"`.
- Phone/name: `firstName.*lastName` required; `libphonenumber`.
- Time zones: `new Date\(` string parsing; `getTimezoneOffset`; `Intl.DateTimeFormat\(\)\.resolvedOptions\(\)\.timeZone`; `date-fns-tz`, `luxon`.

## Gotchas

- `toLocaleDateString()` without a locale uses the runtime's locale. On a server that is often `en-US`, which causes wrong formats and hydration mismatches.
- Pass the locale and time zone explicitly to `Intl` APIs in server-rendered code.
- English-only products still need correct currencies, time zones and date formats for international users (I18N-12 to I18N-14).

## Output

- An i18n readiness summary: externalization percentage, message-format quality, RTL readiness, formatting correctness.
- A formatting audit table (data type · current implementation · correct? · locations).
- Pseudo-localization results (if run).
- Findings in the standard format; the coverage table (I18N-01 … I18N-23).

## Done when

The externalization rate is measured, message construction is reviewed, all date/number/currency/time-zone formatting on critical flows is checked, and RTL/expansion readiness is assessed (with runtime pseudo-localization if possible).
