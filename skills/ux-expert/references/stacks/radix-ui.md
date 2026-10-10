# Radix Primitives

<!-- Generated from criteria/stacks/radix-ui.yaml by scripts/generate.py. Edit the YAML, then run the script. -->

Read when the project imports Radix Primitives (`radix-ui` or `@radix-ui/react-*`), directly or through shadcn/ui. Radix already implements focus management and keyboard support for its widgets, so many generic findings are false positives; the real defects come from labels the team must supply and defaults it overrides.

Verified against Radix Primitives Primitives 1.x (radix-ui 1.4), releases to 2026-07-20 on 2026-10-10, reading https://github.com/radix-ui/website@`402e749`. Detected by dependency `radix-ui`, `@radix-ui/react-dialog`, `@radix-ui/react-alert-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-popover`, `@radix-ui/react-select`, `@radix-ui/react-tooltip`, `@radix-ui/react-toast`. If the project uses another major version, check the gotchas against its docs.

## Where the evidence is

| What | Where |
|---|---|
| Overlays and menus | `Dialog`, `AlertDialog`, `Popover`, `DropdownMenu`, `Select`, `Tooltip` imports from `radix-ui` or `@radix-ui/react-*`, often wrapped in `components/ui/*.tsx` |
| Overridden defaults | Handlers that call `event.preventDefault()`: `onOpenAutoFocus`, `onCloseAutoFocus`, `onEscapeKeyDown`, `onPointerDownOutside`, `onInteractOutside`; `modal={false}` |
| Composition | `asChild` on triggers and items; the child element must be focusable, spread props and forward its ref |
| Labels | `Dialog.Title`, `Dialog.Description`, `VisuallyHidden`, `AccessibleIcon`, `Label`, `aria-label` on `Tooltip.Content` |

## Gotchas

- A modal `Dialog` traps focus, closes on Escape, returns focus to the trigger on close and hides outside content from screen readers. Do not report a missing focus trap or focus return unless the code prevents the default in `onOpenAutoFocus`, `onCloseAutoFocus` or `onEscapeKeyDown`, or sets `modal={false}`. (INT-11, A11Y-06) Source: [data/primitives/docs/components/dialog.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/dialog.mdx).
- Radix leaves accessible names to you. A dialog without a rendered `Dialog.Title` has no name; hide the title with `VisuallyHidden` rather than omitting it. Remove the description with `aria-describedby={undefined}` on `Dialog.Content`, not by deleting it. (A11Y-10) Source: [data/primitives/docs/components/dialog.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/dialog.mdx).
- `AlertDialog` does not close on an outside click, by design. On open, focus goes to Cancel (accessibility overview) while the component page says the destructive action; check the rendered behaviour. The action should look clearly different from Cancel. (CONT-10, LAY-04) Source: [data/primitives/docs/overview/accessibility.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/overview/accessibility.mdx).
- `asChild` passes behaviour to the child element. If the child is a `div` or a component that does not spread props and forward its ref, the trigger loses keyboard access and ARIA wiring. (A11Y-02, A11Y-11) Source: [data/primitives/docs/guides/composition.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/guides/composition.mdx).
- `DropdownMenu` is modal by default (outside content is inert while it is open); `Popover` is not. Typeahead and full keyboard navigation are built in; a menu `Label` is not focusable with arrow keys. (INT-11, A11Y-02) Source: [data/primitives/docs/components/dropdown-menu.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/dropdown-menu.mdx).
- `Tooltip` opens on hover or focus and closes on activation or Escape. It is a description, not a label: an icon button still needs its own `aria-label`. Setting `disableHoverableContent` (content closes when the pointer leaves the trigger) has accessibility consequences, as the docs warn. (INT-13, A11Y-10) Source: [data/primitives/docs/components/tooltip.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/tooltip.mdx).
- `Toast` pauses its timer on hover, focus and window blur, and the viewport is reachable with F8 by default. The hotkey is invisible unless the product mentions it. Foreground toasts (the default) are announced at once and may clear queued announcements, so stacked toasts get lost; background tasks should use `type="background"`. (INT-14, A11Y-13) Source: [data/primitives/docs/components/toast.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/toast.mdx).
- `Select` follows the select-only combobox pattern with typeahead; grouping with `Select.Group` and `Select.Label` gives options their group name automatically. (A11Y-11, FORM-02) Source: [data/primitives/docs/components/select.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/components/select.mdx).
- Radix ships behaviour, not styles. Focus indicators, contrast and target size are the project's CSS; check them on the rendered component. (A11Y-04, A11Y-20) Source: [data/primitives/docs/overview/introduction.mdx](https://github.com/radix-ui/website/blob/402e749613ab2e7ab7139c65b0029842b0360f07/data/primitives/docs/overview/introduction.mdx).

## Probes

Files: `.tsx`, `.jsx`. Run with `python3 scripts/probe.py <project root>`; a hit is a place to look, not a finding.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `radix-prevented-focus-default` | review | `on(Open\|Close)AutoFocus=\{[^}]*preventDefault` | Overridden focus placement on open or close; check focus lands somewhere sensible and returns to the trigger. | A11Y-06, INT-11 |
| `radix-escape-prevented` | smell | `onEscapeKeyDown=\{[^}]*preventDefault` | Escape no longer closes the overlay; acceptable only with unsaved-changes protection that says so. | INT-11, A11Y-03 |
| `radix-as-child` | review | `\basChild\b` | Composition; the child must be a focusable element or a component that spreads props and forwards its ref. | A11Y-02, A11Y-11 |
| `radix-non-modal` | review | `modal=\{false\}` | Non-modal overlay; outside content stays interactive and focus is not trapped. | INT-11 |
