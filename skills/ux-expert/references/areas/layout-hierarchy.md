# Layout and Visual Hierarchy (LAY)

## Senior mindset

A senior designer looking at a screen does a **squint test** first: blur the screen (or literally squint) and ask, **"What do I see first, second and third? Is that the right order for the user's job?"** Hierarchy is not decoration. It is the **order of attention**, and it should match the **order of importance for the task**.

They then check the **invisible structure**: every element sits on a grid, every space comes from a scale, and every group is separated more from its neighbors than its members are from each other. When those three rules hold, a screen feels "calm" without anyone knowing why. When they break, it feels "off" even to people who can't say what's wrong.

Placement is **not arbitrary**. It comes from:
- **Reading patterns:** F-pattern for text-heavy screens, Z-pattern for sparse ones; in left-to-right languages the top-left gets the most attention (mirrored in RTL).
- **Fitts's law:** frequent, important actions are big and close to the user's attention or thumb.
- **Conventions (Jakob's law):** logo top-left, account top-right, primary action bottom-right in dialogs on the web (platform conventions vary; see RESP).
- **Proximity to the thing it acts on:** an action sits next to its object, not in a distant toolbar.

ChatGPT's layout shows this: one narrow centered reading column (~700 px) for readable line length, the input pinned at the bottom near where the eye ends after reading, and secondary features (history, settings) in a collapsible side panel.

## Scope

- **In:** grids and columns, spacing scale and rhythm, alignment, grouping and proximity, hierarchy (size, weight, color, position, whitespace), primary/secondary/tertiary action emphasis, placement of key elements, density, whitespace, scanning paths, above-the-fold content, sticky elements, z-order and overlays, layout stability.
- **Out:** font scale details (→ TYP), color values and contrast (→ COL), breakpoint behavior (→ RESP), component consistency (→ DS).

## Procedure

### Step 1: Pick the screens
Audit **every critical-flow screen** (from FLOW) plus the main templates (list, detail, form, dashboard, settings, empty state, modal). Capture screenshots at 1440, 1024, 768 and 375 px if runtime is available.

### Step 2: Squint test and attention order (per screen)
1. Write the **intended** attention order: what the user needs first, second, third for their job on this screen.
2. Write the **actual** attention order (from screenshots, or by reasoning from size, weight, color and position in code).
3. Any mismatch is a hierarchy finding. Typical case: a decorative banner or a secondary filter bar dominates the primary content.

### Step 3: Primary action analysis
- **Exactly one primary action per view** (filled or high-contrast button). Count elements styled as primary (`variant="primary"`, `btn-primary`, solid fills).
- Secondary actions use an outline/ghost style; tertiary actions are links.
- **Placement:** the primary action sits at the end of the reading path of the content it commits (bottom of a form, bottom-right of a dialog on web/desktop; full-width or bottom-anchored on mobile).
- **Destructive actions** are not styled as primary unless destruction *is* the purpose of the dialog. They are separated from frequent actions by distance.

### Step 4: Spacing system audit
- Extract every spacing value used: `margin`, `padding`, `gap`, `space-*`, Tailwind spacing classes, `EdgeInsets`, etc.
- Build a **histogram** of values. A healthy product uses a small set from a **4/8 pt scale**. Flag off-scale values (e.g. 13 px, 17 px, 22 px) and an excessive variety (> ~10 distinct values).
- **Proximity rule:** for each group (card, form section, list item), internal spacing must be smaller than external spacing. A common healthy ratio is 1:2 (e.g. 8 inside, 16 between; 16 inside, 32 between sections).

### Step 5: Grid and alignment
- Is there a column grid (12-column on desktop, 4–8 on mobile) or a consistent layout primitive (`Container`, `Stack`, `Grid`)?
- Check the **alignment edges**: count the distinct left edges on a screen. Fewer is calmer. Labels, inputs and buttons should share edges.
- Check numeric alignment: right-align numbers in tables, align decimal places (→ DATA).
- Check that the max content width is set for reading (~600–760 px for text) and that wide screens don't stretch forms to 1400 px.

### Step 6: Density and whitespace
- Match density to the user (CTX): experts in data tools want density (with good alignment); occasional users need more whitespace and fewer elements.
- Count the **elements competing for attention** above the fold. More than ~5–7 visually strong elements equals clutter.
- Whitespace is used to **group and separate**, not just added uniformly.

### Step 7: Placement and reachability (Fitts)
- Size of frequent targets: desktop buttons ≥ 32–40 px tall for primary actions; touch ≥ 44 pt (iOS) / 48 dp (Android). WCAG 2.5.8 minimum 24×24 CSS px.
- **Distance:** the action is near its object (row actions on hover or at the row's end; a "Save" bar near the edited content or sticky).
- **Mobile thumb zone:** primary actions in the lower half; destructive actions not in the easiest-to-hit zone.
- **Edge targets:** on desktop, toolbar items at screen edges are easier to hit.

### Step 8: Stability and overlays
- **Layout shift:** content jumping when images, ads, fonts or async data load (CLS; → PERF). Check that images have width/height or aspect-ratio, and that skeletons match final sizes.
- **Sticky elements:** sticky headers and bars stealing too much viewport (> ~20–25% on mobile) or hiding focused elements (WCAG 2.4.11).
- **Z-order:** a z-index system rather than `9999` wars; modals, toasts and dropdowns layer predictably.

## Criteria

<!-- BEGIN GENERATED criteria (layout-hierarchy) -->
<!-- Source: criteria/layout-hierarchy.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| LAY-01 | Attention order matches task priority | Squint test vs. intended order | The most visually dominant element is not the most important | S2–S3 |
| LAY-02 | Single clear primary action | Count primary-styled actions per view | 0 or ≥ 2 equally dominant primaries | S2–S3 |
| LAY-03 | Action hierarchy (primary/secondary/tertiary) | Button variants used consistently | Cancel styled like Submit; all buttons the same | S2 |
| LAY-04 | Destructive actions separated | Distance and style of delete/remove | Delete adjacent to Save in the same style | S3 |
| LAY-05 | Spacing from a scale | Spacing histogram | Off-scale values; > ~10 distinct values | S1–S2 (systemic; → DS) |
| LAY-06 | Proximity grouping | Internal vs. external spacing | Equal or inverted spacing makes groups ambiguous | S2 |
| LAY-07 | Consistent grid and alignment | Count distinct alignment edges; layout primitives | Ragged edges; no grid | S1–S2 |
| LAY-08 | Readable content width | max-width on text and forms | Text lines > ~90 characters; full-width forms on desktop | S2 |
| LAY-09 | Appropriate density | Elements competing above the fold; whitespace use | Clutter, or excessive sparseness for expert tools | S2 |
| LAY-10 | Placement follows conventions | Logo, nav, account, search, primary-action positions | Unconventional placement without a benefit | S2 |
| LAY-11 | Actions near their objects | Distance between an action and its target | Global toolbar actions for item-level operations without selection feedback | S2 |
| LAY-12 | Adequate target sizes | Computed sizes of interactive elements | < 24×24 CSS px (WCAG AA fail); < 44 pt / 48 dp on touch | S2–S3 |
| LAY-13 | Thumb-zone-aware mobile placement | Primary actions in the reachable zone | Key actions only at the top corners on mobile | S2 |
| LAY-14 | Above-the-fold priority | What is visible without scrolling at common viewports | Primary task or value hidden below the fold | S2–S3 |
| LAY-15 | Layout stability | Image dimensions, skeleton sizes, font loading | Visible content jumps; CLS > 0.1 | S2 |
| LAY-16 | Sticky elements sized and non-obscuring | Height of sticky bars; focus visibility | > ~25% of mobile viewport; focused element hidden | S2 |
| LAY-17 | Predictable layering (z-index) | z-index values and overlay system | Arbitrary huge z-index; overlays covering each other | S1–S2 |
| LAY-18 | Consistent page templates | Same structure for same page types | Each list or detail page laid out differently | S2 (→ DS) |
| LAY-19 | Visual balance and symmetry purpose | Weight distribution; intentional asymmetry | One side overloaded; random empty regions | S1 |
| LAY-20 | Scannability | Headings, sections, chunking of long pages | Walls of content without structure | S2 |
<!-- END GENERATED criteria -->

## Code probes

- Spacing values: `(margin|padding|gap)(-\w+)?:\s*\d+px`, Tailwind `\b(p|m|gap|space-[xy])-?[trblxy]?-(\d+|\[.*?\])`, `EdgeInsets\.`, `padding\(`.
- Arbitrary values: `-\[\d+px\]`.
- Primary buttons: `variant=["']primary`, `btn-primary`, `color="primary"`, `type="submit"`.
- Width constraints: `max-w-`, `max-width`, `Container`.
- Z-index: `z-index:\s*\d+`, `z-\[?\d+`.
- Images without dimensions: `<img(?![^>]*(width|height))`, `next/image` without `fill` or sizes.

## Anti-patterns

- Everything bold, so nothing stands out.
- Two primary buttons side by side ("Save" and "Publish", both solid).
- Card soup: every piece of content boxed, borders everywhere instead of whitespace grouping.
- Centered body text over multiple lines (it's hard to find the next line start).
- Full-width text on large monitors.
- Floating action button and sticky footer and sticky header and chat bubble together on mobile.

## Output

- Per screen: the intended vs. actual attention order, primary-action analysis, and a spacing/alignment summary.
- A product-wide spacing histogram and target-size violations list.
- Findings in the standard format; the coverage table (LAY-01 … LAY-20).

## Done when

Every critical-flow screen has passed the squint test and primary-action analysis, the spacing histogram is computed, and target sizes are checked (measured or static).
