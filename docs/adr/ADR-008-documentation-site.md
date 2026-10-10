# ADR-008: Documentation site on Next.js and Fumadocs with shadcn/ui, generated from the repository

- **Status:** accepted (supersedes the Python site builder from UXE-16)
- **Date:** 2026-10-10
- **Story:** UXE-20

## Context

The first site (`scripts/build_site.py`) rendered the Markdown with a small stylesheet. It was correct and
accessible, but had no search, no navigation sidebar, a basic home page and no way to explore the criteria
beyond one long table. The product owner asked for a site with the best UI and UX, suggesting shadcn/ui,
Tailark and React Bits.

## Options considered

1. **Fumadocs (Next.js 16, Tailwind 4) with shadcn/ui** — static export to GitHub Pages; local search (Orama),
   sidebar, table of contents, dark mode, `llms.txt` for agents; shadcn tokens shared by docs and landing.
   Pros: full docs product, dogfoods our own Next.js, shadcn/ui and Playwright packs. Cons: a Node build.
2. **Restyle the Python builder** — cheapest, no search, basic home page.
3. **Astro Starlight** — good docs defaults, but not shadcn-based.

React Bits was set aside: its licence (MIT + Commons Clause) forbids redistributing the components, which a
public MIT repository would do. Tailark (MIT) blocks were not needed once the landing used shadcn primitives.

## Decision

Option 1, in `website/`. Every docs page is generated at build time from the repository's Markdown and
catalogue (`scripts/sync-content.mjs`); nothing is hand-copied. The landing page and the criteria explorer read
`catalogue.json`, so numbers never go stale. The site must pass the skill's own `ux_check.mjs` in CI.

## Consequences

- `scripts/build_site.py`, its tests and `docs/site/style.css` are removed; Python-Markdown leaves the requirements.
- CI gains a `website` job (type-check, build, link check); the runtime job audits the built site.
- Fumadocs and Next.js upgrades follow their release notes; the Next.js stack pack documents the version we know.
- Revisit if the site needs content that is not in the repository (blog, case studies).
