# Typography (TYP)

## Senior mindset

"95% of web design is typography" (Oliver Reichenstein) is an exaggeration with a true core: **most of what users do in a product is read**. A senior treats type as the main way to create hierarchy. **Size, weight and color**, used sparingly, can structure an entire screen without a single box or border.

They check typography in three layers:
1. **System:** is there a deliberate, small type scale (about 4–6 sizes), or 23 one-off sizes?
2. **Readability:** can the target user read it comfortably on the target device (size, contrast, line length, line height)?
3. **Behavior:** what happens with long text, translations, zoom at 200%, a missing font, or numbers in a table?

## Scope

- **In:** font families and fallbacks, type scale, sizes, weights, line height, line length, letter spacing, case usage, paragraph spacing, numerals (tabular/proportional), truncation and wrapping, font loading (FOIT/FOUT), text resize and spacing (WCAG 1.4.4, 1.4.12), hierarchy of headings.
- **Out:** text color contrast (→ COL; measure jointly), copy content (→ CONT), heading semantics for screen readers (→ A11Y).

## Procedure

### Step 1: Extract the type system
- Find tokens or theme: `fontSize`, `--font-size-*`, `text-xs…text-9xl` usage, `Typography` variants (`h1…body2`), `TextStyle`, `.font(`.
- Find every **actual** size used in code: `font-size:\s*[\d.]+(px|rem|em)`, Tailwind `text-(xs|sm|base|lg|xl|\d?xl|\[.*?\])`.
- Build a table: **style name · size · line height · weight · letter spacing · usage count**. Flag sizes that are not in the scale.

### Step 2: Evaluate the scale
- A healthy UI uses **4–6 sizes** in daily use (e.g. 12/14/16/20/24/32), ideally on a ratio (1.125–1.333) or a curated set.
- Adjacent hierarchy levels need **visible contrast**. Two sizes 1 px apart create ambiguity instead of hierarchy.
- Weights: typically 2–3 weights (regular, medium/semibold, bold). Using 5+ weights is noise.

### Step 3: Readability checks
- **Body size:** ≥ 16 px for general web products. Dense pro tools may use 13–14 px if contrast is strong and zoom works. Never < 12 px for any meaningful text.
- **Line height:** body 1.4–1.6; headings 1.1–1.3; UI labels around 1.2–1.4.
- **Line length:** 45–75 characters for paragraphs. The most reliable rule in code is a `max-width` in `ch` (e.g. `max-width: 65ch`). For pixel widths, a rough estimate is that an average character is about 0.5 em wide, so a 16 px body text column of 700 px holds about 85 characters.
- **Paragraph spacing:** visible, around 0.75–1.5× the font size.
- **Letter spacing:** positive tracking for ALL CAPS small labels (+0.05 em to +0.1 em); never tighten body text.
- **Case:** avoid ALL CAPS for long text (slower reading); sentence case for UI labels is more readable and friendlier (and avoids inconsistent title case).
- **Alignment:** left-aligned (start-aligned) body text; avoid justified text on the web (rivers); avoid multi-line centered text.

### Step 4: Behavior checks
- **Text resize (WCAG 1.4.4):** sizes in `rem`/`em` (or platform dynamic type), not fixed `px` everywhere. Does the layout survive 200% zoom?
- **Text spacing (WCAG 1.4.12):** containers don't clip when line-height is set to 1.5 and letter spacing to 0.12 em (no fixed `height` plus `overflow: hidden` on text).
- **Dynamic Type / font scaling** on mobile (iOS Dynamic Type, Android `sp` units). Check that `allowFontScaling={false}` and `maxFontSizeMultiplier` aren't abused.
- **Truncation:** ellipsis only where the full text is reachable (tooltip, expand, detail view). Never truncate critical information (amounts, names in confirmation dialogs).
- **Wrapping:** long words or URLs (`overflow-wrap: anywhere`), and long translations (→ I18N).
- **Numerals:** tabular figures (`font-variant-numeric: tabular-nums`) in tables, counters, prices and timers, so digits don't jitter.
- **Font loading:** `font-display: swap` or `optional`; preload critical fonts; fallback metrics matched (`size-adjust`) to avoid layout shift; a system font stack as fallback.

### Step 5: Hierarchy check per screen
- Exactly one H1-level visual heading per page.
- Heading levels visually distinct and in order.
- Labels vs. values distinguishable (e.g. muted label, strong value).

## Criteria

| ID | Criterion | Check | Threshold / fail signal | Default severity |
|---|---|---|---|---|
| TYP-01 | Defined type scale | Tokens/variants exist and are used | No scale; > 8 distinct sizes in use | S2 (systemic → DS) |
| TYP-02 | Off-scale sizes | Count sizes not in the scale | Any frequent off-scale size | S1–S2 |
| TYP-03 | Body text size | Computed body size | < 16 px for a general audience; < 12 px anywhere meaningful | S2–S3 |
| TYP-04 | Line height | Body and heading line heights | Body < 1.4 or > 1.8 | S2 |
| TYP-05 | Line length | Container width for paragraphs | > ~80–90 characters, or < ~35 for body text | S2 |
| TYP-06 | Distinct hierarchy levels | Size and weight steps between levels | Adjacent levels nearly identical; level order inverted | S2 |
| TYP-07 | Weight discipline | Weights in use | > 3–4 weights; bold used for emphasis everywhere | S1 |
| TYP-08 | Case usage | ALL CAPS and title-case patterns | Long uppercase text; inconsistent casing across UI | S1–S2 |
| TYP-09 | Alignment | `text-align: justify`, centered paragraphs | Justified or centered multi-line body text | S1–S2 |
| TYP-10 | Relative units / scalable text | rem/em/sp/Dynamic Type | Fixed px everywhere; font scaling disabled | S2–S3 |
| TYP-11 | Survives 200% zoom and text spacing | Runtime zoom; fixed-height text containers | Clipped or overlapping text | S3 (WCAG AA) |
| TYP-12 | Safe truncation | Ellipsis usage on critical data | Truncated values with no way to see them in full | S2–S3 |
| TYP-13 | Long-string wrapping | overflow-wrap on user content, URLs, emails | Horizontal overflow or broken layout | S2 |
| TYP-14 | Tabular numerals where numbers align or change | `tabular-nums` in tables, counters, prices | Jittering counters; misaligned numeric columns | S1–S2 |
| TYP-15 | Font loading strategy | `font-display`, preload, fallback stack | Invisible text during load; large layout shift from font swap | S2 |
| TYP-16 | Font family count | Families loaded | > 2 families (excluding monospace) without reason; heavy font payload | S1–S2 (→ PERF) |
| TYP-17 | Monospace for code and IDs | Code, keys, IDs in monospace | Code in a proportional font; ambiguous characters (0/O, 1/l/I) in IDs | S1–S2 |
| TYP-18 | Readable on all backgrounds | Text over images or gradients has a scrim or overlay | Text over busy imagery | S2 (→ COL) |

## Code probes

- Sizes: `font-size:`, `fontSize:`, `text-\[`, `TextStyle\(`, `.font\(.system\(size:`.
- Line height: `line-height:`, `leading-`.
- Units: count `px` vs `rem` in font sizes.
- Scaling disabled: `allowFontScaling={false}`, `maximum-scale=1`, `user-scalable=no`.
- Justify: `text-align:\s*justify`, `text-justify`.
- Fonts: `@font-face`, `font-display`, `next/font`, `<link[^>]*fonts.googleapis`.
- Numerals: `tabular-nums`, `font-variant-numeric`.

## Output

- A type system table (style · size · line height · weight · usage count · on-scale?).
- Findings in the standard format; the coverage table (TYP-01 … TYP-18).

## Done when

The full type inventory is extracted, the scale is evaluated, readability is checked on critical screens, and zoom/spacing behavior is verified at runtime or marked Not verified.
