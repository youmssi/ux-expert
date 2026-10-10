# Stack packs

<!-- Generated from criteria/stacks/*.yaml by scripts/generate.py. Edit the YAML, then run the script. -->

What a framework, component library or test tool changes about UX findings: where the evidence is, defaults
that turn generic findings into false positives, common ways teams break built-in behaviour, and probes.
Read a pack only when recon detects its stack (`python3 scripts/probe.py <project root>` lists them).
Each pack records the version and commit it was verified against.

| Pack | Kind | Detected by | Verified against |
|---|---|---|---|
| [Next.js (App Router)](stacks/nextjs.md) | Frameworks | `next`, `next.config.js`, `next.config.mjs`, `next.config.ts` | 16.x, 2026-10-10 |
| [Radix Primitives](stacks/radix-ui.md) | Component libraries | `radix-ui`, `@radix-ui/react-dialog`, `@radix-ui/react-alert-dialog`, `@radix-ui/react-dropdown-menu`, `@radix-ui/react-popover`, `@radix-ui/react-select`, `@radix-ui/react-tooltip`, `@radix-ui/react-toast` | Primitives 1.x (radix-ui 1.4), releases to 2026-07-20, 2026-10-10 |
| [shadcn/ui](stacks/shadcn-ui.md) | Component libraries | `components.json` | new-york-v4 registry (Tailwind CSS 4, React 19), 2026-10-10 |
