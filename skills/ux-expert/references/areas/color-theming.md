# Color and Theming (COL)

## Senior mindset

A senior designer treats color as a **signal system**, not decoration. In a well-designed product, color is mostly **neutral** (greys carry about 80–90% of the surface), and saturated color is **rare and meaningful**: it marks the primary action, status (success, warning, error, info), selection and links. When everything is colorful, color stops meaning anything.

They also know color is the **least reliable channel**: about 1 in 12 men and 1 in 200 women have a color-vision deficiency (most commonly red–green), screens vary, sunlight washes out contrast, and dark mode changes every relationship. So every color meaning must be **backed by a second channel** (icon, text, shape or position), and every contrast must be **computed**, not eyeballed.

## Scope

- **In:** palette and token structure (primitive → semantic → component), text and non-text contrast, semantic color roles, state colors (hover, active, focus, disabled, selected), color-only information, color-blind safety, dark mode, `forced-colors` / Windows high contrast, theming architecture, brand consistency, data-viz color (light; full charts → DATA).
- **Out:** typography size (→ TYP; jointly needed for the large-text contrast threshold).

## Procedure

### Step 1: Extract the palette
- Find tokens: CSS custom properties (`--color-*`), Tailwind `theme.colors` / `@theme`, theme objects (`palette`, `colors`), `Color(` in Flutter/Swift, `colors.xml`.
- Classify them into **primitive** (blue-500), **semantic** (`--color-text-muted`, `--color-danger`) and **component** (`--button-primary-bg`) tokens.
- Count hard-coded colors outside token files (`#[0-9a-fA-F]{3,8}`, `rgb(`, `hsl(`, Tailwind arbitrary `bg-[#…]`). These are **drift** (→ DS).

### Step 2: Compute contrast (measured evidence)
For every **foreground/background pair actually used** (body text, muted text, placeholder, link, button label on its fill, disabled text, error text, text on brand color, text on images), compute the WCAG contrast ratio:
- Relative luminance: L = 0.2126 R + 0.7152 G + 0.0722 B, with sRGB channels linearized (c ≤ 0.04045 ? c/12.92 : ((c+0.055)/1.055)^2.4).
- Ratio = (L_lighter + 0.05) / (L_darker + 0.05).

Thresholds (WCAG 2.2 AA): **4.5:1** normal text; **3:1** large text (≥ 24 px, or ≥ 18.66 px bold); **3:1** non-text UI (input borders that identify the control, focus rings, icons that carry meaning, chart marks). Disabled controls are exempt, but they should still be legible enough to understand.

Do this in **both light and dark themes**. A tiny script (Node or Python) is acceptable and preferred over estimation. Record the pairs in a table.

### Step 3: Semantic consistency
- One color per meaning: is red always "error/destructive", green always "success"? Is the brand color also used for errors, or are links the same color as non-interactive accents?
- Links are distinguishable from body text by more than color (an underline, or ≥ 3:1 contrast with surrounding text plus a non-color cue on hover/focus; WCAG 1.4.1).
- Status uses **icon + text + color**, never color alone (e.g. a red dot alone for "offline").
- State colors: hover, pressed, selected, focus and disabled are each distinct and consistent across components.

### Step 4: Color-vision deficiency
- Simulate protanopia, deuteranopia and tritanopia (Chrome DevTools "Emulate vision deficiencies", or a simulation library) on critical screens and charts.
- Check red/green pairs (success vs. error, up vs. down in finance, diff views) for a second channel.

### Step 5: Dark mode and themes
- Does dark mode exist? Should it (CTX: developers and long-session users usually expect it)? Is it respecting `prefers-color-scheme`, with a user override?
- Dark mode is **not inverted** light mode: surfaces use dark greys (not pure `#000` everywhere for large surfaces), elevation is shown with lighter surfaces, saturated colors are desaturated or lightened to keep contrast, shadows are replaced, and images/illustrations are adapted.
- Check for **un-themed islands**: hard-coded white backgrounds, images with white boxes, third-party widgets, emails, charts, code blocks, scrollbars (`color-scheme: dark`).
- **Flash of incorrect theme** on load (theme applied after hydration).

### Step 6: High contrast and forced colors
- `@media (forced-colors: active)`: borders and focus remain visible; icons that rely on `background-image` don't disappear; custom checkboxes remain perceivable.
- `prefers-contrast: more` support (nice to have).

## Criteria

<!-- BEGIN GENERATED criteria (color-theming) -->
<!-- Source: criteria/color-theming.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| COL-01 | Tokenized palette with semantic roles | Token structure | No semantic tokens; components use primitives or hex directly | S2 (→ DS) |
| COL-02 | Body text contrast | Computed ratio | < 4.5:1 | S3 (WCAG AA) |
| COL-03 | Secondary/muted/placeholder text contrast | Computed ratio | < 4.5:1 for meaningful muted text; placeholder carrying instructions < 4.5:1 | S2–S3 |
| COL-04 | Large text and headings contrast | Computed ratio | < 3:1 | S3 |
| COL-05 | Non-text contrast (inputs, focus, icons, chart marks) | Computed ratio | < 3:1 against adjacent colors | S2–S3 |
| COL-06 | Text on brand/colored fills | Button labels, badges, banners | < 4.5:1 (common with white on mid-brand colors such as orange or light green) | S2–S3 |
| COL-07 | No color-only meaning | Status, errors, required fields, links, charts | Meaning lost in greyscale | S3 (WCAG 1.4.1) |
| COL-08 | Consistent semantic colors | Usage mapping across components | The same color with conflicting meanings | S2 |
| COL-09 | Restraint (color as signal) | Share of saturated color on screens | Many competing saturated colors; primary action not the most salient | S2 |
| COL-10 | Distinct interaction states | Hover, active, focus, selected, disabled | Missing or indistinguishable states | S2 (→ INT) |
| COL-11 | Color-vision-deficiency safe | Simulation on critical screens and charts | Indistinguishable critical pairs | S2–S3 |
| COL-12 | Dark mode quality (if present or expected) | Contrast, elevation, un-themed islands | Pure inversion; white islands; failing contrast in dark | S2–S3 |
| COL-13 | Theme preference respected | `prefers-color-scheme`, persisted override, no flash | Theme flashes on load; preference ignored | S2 |
| COL-14 | Forced-colors / high-contrast support | `forced-colors` media query testing | Controls or focus disappear | S2–S3 |
| COL-15 | Text over images is legible | Scrim or overlay present | Contrast depends on image content | S2 |
| COL-16 | Brand applied consistently | Brand colors across product, emails, marketing | Several slightly different brand blues | S1 |
| COL-17 | Disabled vs. enabled distinguishable | Disabled styling | Disabled looks enabled (or vice versa) | S2 |
| COL-18 | Theming architecture scalable | Themes switch via tokens, not duplicated CSS | `dark:` overrides scattered per component with gaps | S1–S2 (→ DS) |
<!-- END GENERATED criteria -->

## Code probes

- Hard-coded colors outside tokens: `#[0-9a-fA-F]{3,8}\b`, `rgba?\(`, `hsla?\(`, `bg-\[#`, `text-\[#`, `Color\(0x`.
- Theme: `prefers-color-scheme`, `data-theme`, `class="dark"`, `useColorScheme`, `ThemeProvider`, `next-themes`, `color-scheme:`.
- Forced colors: `forced-colors`, `-ms-high-contrast`.
- Color-only status: components named `StatusDot`, `Indicator`, `Badge` with no text or `aria-label`.

## Contrast script (example)

```js
const hex = h => h.replace('#','').match(/.{2}/g).map(x => parseInt(x,16)/255);
const lin = c => c <= 0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
const L = h => { const [r,g,b] = hex(h).map(lin); return 0.2126*r + 0.7152*g + 0.0722*b; };
const ratio = (a,b) => { const [x,y] = [L(a),L(b)].sort((p,q)=>q-p); return ((x+0.05)/(y+0.05)).toFixed(2); };
console.log(ratio('#6B7280', '#FFFFFF')); // ≈ 4.83
```
(Expand 3-digit hex first; for alpha colors, composite over the actual background before computing.)

## Gotchas

- Compute contrast against the real background, including dark-mode surfaces and cards, not against white by default.
- Disabled controls are exempt from WCAG 1.4.3; placeholder text that carries instructions is not.
- "Large text" is 24 CSS px regular or 18.66 CSS px bold. A 16 px bold label is normal text (4.5:1).
- Brand colors are often fixed by marketing. Recommend an accessible darker variant for text and fills rather than changing the brand.

## Output

- A contrast table: pair · usage · light ratio · dark ratio · pass/fail (AA).
- A semantic color map: meaning → token → consistent?
- Findings in the standard format; the coverage table (COL-01 … COL-18).

## Done when

Every used text and UI color pair on critical screens has a computed ratio in each theme, color-only meanings are checked, and dark/forced-colors behavior is verified or marked Not verified.
