# shadcn/ui

<!-- Generated from criteria/stacks/shadcn-ui.yaml by scripts/generate.py. Edit the YAML, then run the script. -->

Read when the project has a `components.json` at its root. shadcn/ui components are copied into the project, so audit them as the team's own code, starting from what the upstream versions already get right.

Verified against shadcn/ui new-york-v4 registry (Tailwind CSS 4, React 19) on 2026-10-10, reading https://github.com/shadcn-ui/ui@`2d3f1cd`. Detected by file `components.json`. If the project uses another major version, check the gotchas against its docs.

## Where the evidence is

| What | Where |
|---|---|
| The components actually in use | `components/ui/*.tsx` (path set by the `ui` alias in `components.json`); each file may differ from upstream |
| Underlying primitives | Imports in `components/ui/*.tsx`: `radix-ui` or `@radix-ui/react-*` (Radix), `@base-ui/react` (Base UI), `react-aria-components` (React Aria) |
| Theme tokens and dark mode | The global CSS file named in `components.json`: tokens under `:root` and `.dark`, exposed with `@theme inline`; colors in OKLCH |
| Toasts, forms, sidebar | `components/ui/sonner.tsx` (toasts), `field.tsx` or `form.tsx` (form fields), `sidebar.tsx` (navigation shell) |

## Gotchas

- shadcn/ui is not a dependency but code copied into the project, open for modification. Compare a suspicious component with the upstream file before attributing a defect to shadcn/ui, and report it against the project's file. (DS-06, DS-10) Source: [apps/v4/content/docs/(root)/index.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/(root)/index.mdx).
- New projects default to Base UI primitives; Radix and React Aria are still supported. Check the imports in `components/ui` before applying Radix behaviour (the Radix pack) to a project. (DS-10) Source: [apps/v4/content/docs/changelog/2026-07-base-ui-default.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/changelog/2026-07-base-ui-default.mdx).
- Buttons, inputs, selects, checkboxes and tabs replace the outline with a 3 px `focus-visible` ring, so `outline-none` in these files is not an A11Y-04 defect. Menu and select items show focus only as a background change (`focus:bg-accent`); check its contrast against the menu background. (A11Y-04, COL-10) Source: [apps/v4/registry/new-york-v4/ui/button.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/button.tsx).
- Default button and icon-button sizes are 36 px (`h-9`, `size-9`) and the smallest sizes 24 px, which meets WCAG 2.5.8. The checkbox is 16 px (`size-4`) and the switch about 18 px high; check spacing or a clickable label before reporting a target-size failure. (A11Y-20, RESP-07) Source: [apps/v4/registry/new-york-v4/ui/button.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/button.tsx).
- Inputs style `aria-invalid`, but only if the code sets it. The current form docs wire `aria-invalid` and `data-invalid` by hand on each `Field`; a missing attribute leaves errors invisible to screen readers. (FORM-10, A11Y-24) Source: [apps/v4/content/docs/forms/react-hook-form.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/forms/react-hook-form.mdx).
- The older `Form` component wires `aria-invalid` and `aria-describedby` (description plus message) automatically through `FormControl`. A custom field that skips `FormControl` loses both. (FORM-03, A11Y-24) Source: [apps/v4/registry/new-york-v4/ui/form.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/form.tsx).
- Upstream icon controls carry `sr-only` text or `aria-label` (dialog close, carousel, pagination). Icon-only `Button`s written by the team do not get one automatically; each needs a label. (A11Y-10) Source: [apps/v4/registry/new-york-v4/ui/dialog.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/dialog.tsx).
- `TooltipProvider` defaults to `delayDuration = 0`, so tooltips open instantly on hover. Information only in a tooltip is still hover- or focus-only (INT-13). (INT-13) Source: [apps/v4/registry/new-york-v4/ui/tooltip.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/tooltip.tsx).
- The `toast` component is deprecated in favour of Sonner (`sonner.tsx`), which follows the theme from `next-themes`. Check toasts for INT-14 in the Sonner usage, not in a leftover `toast.tsx`. (INT-14) Source: [apps/v4/content/docs/(root)/tailwind-v4.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/(root)/tailwind-v4.mdx).
- The sidebar toggles with Ctrl/Cmd+B, persists its state in a cookie and becomes a sheet on mobile with a visually hidden header. Check the shortcut does not clash with text editing in the app (B for bold). (INT-16) Source: [apps/v4/registry/new-york-v4/ui/sidebar.tsx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/registry/new-york-v4/ui/sidebar.tsx).
- Projects on Tailwind 3 keep receiving Tailwind 3 and React 18 versions of components until they upgrade, and files added before an upgrade keep their old styles. Mixed focus rings or radii between files are often this, not design drift. (AES-01, DS-04) Source: [apps/v4/content/docs/(root)/tailwind-v4.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/(root)/tailwind-v4.mdx).
- The CLI can rewrite physical positioning classes to logical ones for right-to-left layouts. Components added before RTL was enabled keep `left`/`right` classes. (I18N-09) Source: [apps/v4/content/docs/rtl/index.mdx](https://github.com/shadcn-ui/ui/blob/2d3f1cd436b18ea12f24130de4df781355925b08/apps/v4/content/docs/rtl/index.mdx).

## Probes

Files: `.tsx`, `.jsx`. Run with `python3 scripts/probe.py <project root>`; a hit is a place to look, not a finding.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `shadcn-icon-button-unlabeled` | review | `size="icon(-xs\|-sm\|-lg)?"` | Icon-only buttons; each needs `aria-label` or `sr-only` text. | A11Y-10 |
| `shadcn-aria-invalid` | inventory | `aria-invalid=\|data-invalid` | Fields that expose their error state. Compare with the number of validated fields. | FORM-10, A11Y-24 |
| `shadcn-dialog-without-title` | review | `<DialogContent\|<SheetContent\|<AlertDialogContent` | Each dialog or sheet needs a `DialogTitle` (visually hidden if needed) so it has an accessible name. | A11Y-10, INT-11 |
| `shadcn-hardcoded-color-class` | smell | `\b(bg\|text\|border\|ring)-(red\|blue\|green\|gray\|slate\|zinc\|neutral\|yellow\|orange\|purple)-\d{2,3}\b` | Palette classes that bypass the theme tokens (`bg-primary`, `text-muted-foreground`) and dark mode. | DS-03, COL-12 |
