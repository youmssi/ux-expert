# Design System and Consistency (DS)

## Senior mindset

When a senior sees 14 slightly different buttons, they don't file 14 bugs. They ask **"why was it possible to create 14 buttons?"** The design system is the **production line** of the UX. Most consistency defects are **systemic**: missing tokens, a component that doesn't support a needed variant (so people fork it), no documentation, or no review gate.

Consistency matters because it **lowers learning cost** (users learn a pattern once and reuse it), **builds trust** (polish signals reliability, per the aesthetic-usability effect), and **speeds up teams**. But a senior also knows the system should be **as small as possible**: a few well-designed components with clear variants beat a sprawling library nobody understands.

This area is the **root-cause engine** for many LAY, TYP, COL and INT findings. Its output feeds the cross-cutting synthesis in the orchestrator.

## Scope

- **In:** token architecture (color, spacing, typography, radius, shadow/elevation, motion, z-index, breakpoints), token adoption vs. hard-coded values, component inventory and coverage, duplicate/forked components, variant explosion, component API consistency (prop names, sizes, states), accessibility baked into components, iconography consistency, illustration/imagery style, documentation (Storybook, usage guidelines, do/don't), visual regression tests, theming support, versioning and governance, design–code parity (Figma vs. code, if available).
- **Out:** judging individual screen layouts (→ LAY), individual contrast values (→ COL). DS judges the **system** that produces them.

## Procedure

### Step 1: Locate the system
- Token sources: CSS variables in `:root`, `tailwind.config.*`/`@theme`, `tokens.json`, Style Dictionary, theme objects (MUI/Chakra/Mantine), `ThemeData` (Flutter), `Color`/`Font` extensions (Swift), `colors.xml`/`dimens.xml`/Compose theme.
- Component sources: `components/ui`, `packages/ui`, `design-system/`, `@company/ui`, shadcn (`components/ui/*.tsx`), third-party libraries.
- Docs: `.storybook/`, `*.stories.*`, `docs/design`, `zeroheight`, `README` in the UI package.

### Step 2: Token audit
For each token category, report: **defined?** · **semantic layer?** · **adoption rate**.
- **Adoption rate** = token usages / (token usages + hard-coded values) for that category. Compute with grep counts (see the code probes). Report e.g. "Color: 412 token uses vs. 187 hex literals, so 69% adoption".
- Look for **near-duplicates**: `#3B82F6` vs. `#3B81F6`, `15px` vs. `16px`, `border-radius: 6px/7px/8px`.

### Step 3: Component inventory
Build a table of UI primitives and patterns:

| Component | Canonical implementation | Duplicates/forks found | Usage count | Variants | States complete? | A11y built in? | Documented? |
|---|---|---|---|---|---|---|---|

Core list to check: Button, IconButton, Link, Input, Textarea, Select/Combobox, Checkbox, Radio, Switch, Slider, DatePicker, Form field wrapper (label/help/error), Modal/Dialog, Drawer/Sheet, Popover, Tooltip, Toast, Alert/Banner, Tabs, Accordion, Menu/Dropdown, Table/DataGrid, Pagination, Card, Avatar, Badge/Tag, Skeleton, Spinner/Progress, EmptyState, Breadcrumb, Navigation (sidebar/topbar/tabbar), Icon.

- **Forks:** search for components re-implementing a primitive (e.g. raw `<button className=…>` styled locally while a `Button` exists; several `Modal` implementations).
- **Variant explosion:** a component with many boolean style props (`isBig`, `isRed`, `noPadding`, `special`) instead of a small variant/size API.
- **API consistency:** the same concept named the same way across components (`size="sm|md|lg"` everywhere, not `small`/`compact`/`dense` mixed; `variant` vs. `type` vs. `kind`).

### Step 4: Pattern consistency across screens
Sample 3–5 instances of each repeated pattern (list page, detail page, create flow, settings form, confirmation dialog, empty state, error state) and compare structure, placement and behavior. Inconsistent patterns become a finding with a recommendation to create a pattern or template component.

### Step 5: Iconography and imagery
- One icon set (or consistent style: stroke width, corner radius, fill vs. outline); consistent sizes on a grid (16/20/24).
- The same icon means the same thing everywhere (no gear for both "settings" and "integrations"; no trash icon for "archive").
- Icons paired with labels where meaning isn't universal.
- Illustrations and photography in a consistent style.

### Step 6: Quality infrastructure
- Storybook (or equivalent) with stories for states and variants; usage guidelines.
- Visual regression testing (Chromatic, Percy, Playwright screenshots).
- A11y tests on components (`jest-axe`, Storybook a11y addon).
- Lint rules preventing drift (e.g. `stylelint-declaration-strict-value`, Tailwind `no-arbitrary-value` rules, ESLint `no-restricted-imports` for deprecated components).
- Versioning and changelog for the UI package; a deprecation path.

## Criteria

<!-- BEGIN GENERATED criteria (design-system) -->
<!-- Source: criteria/design-system.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| DS-01 | Tokens exist for all core categories | Missing color/spacing/type/radius/shadow/motion/z-index tokens | S2 |
| DS-02 | Semantic token layer | Components use primitives (`blue-500`) instead of roles (`--color-action-primary`) | S2 |
| DS-03 | Token adoption | < ~90% adoption in a category; many hard-coded values | S2 (systemic) |
| DS-04 | No near-duplicate values | Many near-identical colors, sizes and radii | S1–S2 |
| DS-05 | Canonical components for core primitives | Missing core components; each team builds its own | S2 |
| DS-06 | No forks/duplicates | ≥ 2 implementations of the same primitive | S2 |
| DS-07 | Controlled variants | Variant explosion; boolean style props | S1–S2 |
| DS-08 | Consistent component APIs | Inconsistent prop names and size scales | S1 |
| DS-09 | Complete states in components | Components missing focus/disabled/loading/error states | S2–S3 (→ INT) |
| DS-10 | Accessibility built into components | Primitives without keyboard/ARIA support, so every usage is broken | S3 (→ A11Y) |
| DS-11 | Consistent patterns across screens | Same pattern implemented differently | S2 |
| DS-12 | Iconography consistent | Mixed sets, styles, sizes; inconsistent meanings | S1–S2 |
| DS-13 | Documentation | No Storybook or usage docs | S1–S2 |
| DS-14 | Visual regression and a11y tests | None | S1–S2 |
| DS-15 | Drift prevention lint | No rules preventing hard-coded values or deprecated components | S1 |
| DS-16 | Theming via tokens | Themes require per-component overrides | S1–S2 (→ COL) |
| DS-17 | Governance and versioning | No owner, changelog or deprecation path | S1 |
| DS-18 | Design–code parity (if design files available) | Figma components differ from code; naming mismatch | S1–S2 |
<!-- END GENERATED criteria -->

## Code probes (counting drift)

```bash
# Hard-coded colors outside token/theme files
rg -n --glob '!**/{tokens,theme,themes}/**' --glob '!*.{svg,md}' '#[0-9a-fA-F]{3,8}\b' src | wc -l
# Tailwind arbitrary values
rg -n '\b[a-z-]+-\[[^\]]+\]' src | wc -l
# Inline styles
rg -n 'style=\{\{' src | wc -l
# Raw buttons where a Button component exists
rg -n '<button\b' src --glob '!**/components/ui/**' | wc -l
# Multiple modal implementations
rg -ln '(Modal|Dialog)\b.*(function|const|class)' src
# Off-scale font sizes and spacing
rg -n 'font-size:\s*\d+px' src | wc -l
rg -n '(margin|padding|gap)[^:]*:\s*\d+px' src | wc -l
```
Adjust the paths and globs to the project. Report the counts as **measured** evidence.

## Output

- A token adoption table per category with counts.
- The component inventory table (with forks highlighted).
- A pattern consistency comparison table.
- **Systemic root-cause statements** for the orchestrator, e.g. "No semantic color tokens + 187 hex literals explains COL-08, COL-16 and LAY inconsistency findings".
- Findings in the standard format; the coverage table (DS-01 … DS-18).

## Done when

Token adoption is measured for each category, core components are inventoried with forks identified, repeated patterns are compared, and systemic root causes are written for use in cross-cutting synthesis.
