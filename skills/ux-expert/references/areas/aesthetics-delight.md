# Aesthetics and Delight (AES)

## Senior mindset

People judge quality by what they see before they judge it by what works, and they forgive more in a product that looks cared for (the aesthetic–usability effect, a qualitative finding [src:classic-laws]). But polish is not decoration. A senior audits aesthetics as **craft and consistency**, things another reviewer would see the same way, and treats delight as a **reward that never costs the user time**.

Principles:
1. **Consistency is the first aesthetic.** The same kind of element looks the same everywhere.
2. **Every state is designed,** not just the happy path in the screenshot.
3. **Expression where it helps.** Personality in onboarding, empty states and milestones; quiet on dense work surfaces and in bad news.
4. **Delight is optional and fast.** It never blocks, never repeats on routine actions, and respects reduced motion.

## Scope

- **In:** visual craft details (radii, shadows, borders, icon styles), pixel polish, imagery and illustration, brand expression and where it appears, celebratory moments and decorative motion, tone of personality, placeholder content, quality of edge states, favicons and app icons and email templates, sound and haptics, easter eggs, perceived quality.
- **Out:** spacing scale and hierarchy (→ LAY), type scale (→ TYP), palette and contrast (→ COL), tokens and components (→ DS), motion timing and reduced motion as accessibility (→ INT-08, INT-09, A11Y-22). AES judges the result as a whole; the other areas own the rules.

## Procedure

### Step 1: Capture the real screens
Use rendered screens, not design files: run `scripts/ux_check.mjs` for screenshots at real widths in light and dark mode, with realistic data (long names, empty lists, many items). Without a runtime, mark visual findings as reduced confidence.

### Step 2: Consistency sweep
Lay out screenshots side by side by element type: buttons, cards, inputs, icons, avatars, illustrations. Note each variant of radius, shadow, border, icon style and image style (AES-01, AES-03).

### Step 3: Polish on critical screens
For each critical-flow screen: alignment, clipped or overflowing text, uneven gaps, broken or stretched images, placeholder content (AES-02, AES-08).

### Step 4: Edge states and details
Empty, loading, error and offline screens next to the happy path: same care or raw (AES-09)? Favicon, app icon, splash, social image, email templates (AES-10).

### Step 5: Delight inventory
List each delight moment: celebrations, playful copy, decorative animations, sounds, haptics, easter eggs. For each: trigger, frequency, duration, whether it blocks input, reduced-motion behaviour, off switch (AES-05, AES-06, AES-11, AES-12). Check tone in errors, billing and security screens (AES-07).

## Criteria

<!-- BEGIN GENERATED criteria (aesthetics-delight) -->
<!-- Source: criteria/aesthetics-delight.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| AES-01 | Craft details consistent | Mixed corner radii, shadows, borders or icon styles for the same kind of element | S1–S2 (→ DS-04, DS-12) |
| AES-02 | Pixel polish on key screens | Misalignments, clipped text or uneven gaps on critical screens at supported widths | S1–S2 (→ LAY-07) |
| AES-03 | Imagery coherent | Mixed illustration styles; blurry, stretched or off-brand images; no dark-mode variants | S1–S2 |
| AES-04 | Expression placed where it helps | Decoration competes with task content on dense work screens | S2 (→ LAY-01, COL-09) |
| AES-05 | Delightful motion never delays the task | A celebratory or decorative animation blocks the next action or ignores reduced motion | S2 (→ INT-08, INT-09) |
| AES-06 | Celebrations proportional | Confetti on routine actions; real milestones pass unnoticed | S0–S1 |
| AES-07 | Personality fits the moment | Jokes or playful tone in errors, billing, security or bad news | S2 (→ CONT-07, CONT-13) |
| AES-08 | No placeholder content in production | Lorem ipsum, broken images, default avatars or test data visible to users | S2–S3 (→ LAUNCH-03) |
| AES-09 | Edge states designed with the same care | Polished happy path; raw, unstyled empty, error or loading screens | S2 (→ STATE-01) |
| AES-10 | Brand details complete | Default framework favicon, app icon, splash or social image; unstyled emails | S1–S2 (→ LAUNCH-09, LAUNCH-16) |
| AES-11 | Sound and haptics optional and meaningful | Sounds or vibrations by default with no setting to turn them off | S1–S2 |
| AES-12 | Easter eggs harmless | Hidden features that obstruct tasks, trap focus or break assistive technology | S1 |
| AES-13 | Perceived quality checked with users | Brand-led or consumer product with no evidence of how users perceive its look | S0–S1 (→ MEAS) |
<!-- END GENERATED criteria -->

## Gotchas

- Design files show ideal data. Long names, missing avatars, 0 and 10,000 items break polish that looks perfect in a mockup; audit with realistic data.
- Lottie and Rive animations play regardless of `prefers-reduced-motion` unless the code checks it; search for the check before clearing AES-05.
- Frameworks ship default favicons and social images (`public/favicon.ico`, `app/favicon.ico`, `opengraph-image`); check they were replaced (AES-10).
- "Looks dated" or "not modern" is not a finding. Name the observable inconsistency or defect, or record it as an S0 note.

## Output

- The consistency sweep table: element type, variants found, screens.
- The delight inventory with trigger, frequency, blocking and reduced-motion behaviour.
- Findings in the standard format; the coverage table (AES-01 … AES-13).

## Done when

Critical screens are reviewed as rendered, every element type has its variants counted, edge states are compared with the happy path, and every delight moment is inventoried.
