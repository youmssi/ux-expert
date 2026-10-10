### UXE-20 — A documentation site with the UI and UX the package asks of others

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-16  ·  **Size:** L

#### Why

A UX package is judged by its own site. The first site had no search, a basic landing page and one long criteria
table. People evaluating the package (and agents reading it) need to find an area, a criterion or an install
step in seconds.

#### Decision

[ADR-008](../adr/ADR-008-documentation-site.md): Next.js 16 + Fumadocs + Tailwind 4 + shadcn/ui, statically
exported to GitHub Pages. Product-owner choices: this stack, and a calm and precise visual direction (neutral
palette, one accent, real product content instead of illustrations, motion only where it helps).

#### Behaviour

| Where | Before | After |
|---|---|---|
| Home | README rendered as a page | Landing: value proposition, an example finding with measured values, counts from the catalogue, six modes, how an audit works with a verdict, install tabs, stack packs |
| Docs | Flat pages | Sidebar, search, table of contents, dark mode, copy-as-Markdown, edit links to the real source file, `llms.txt` |
| Criteria | One long table | Explorer with filters (words, area, product type, phase, severity) kept in the URL; `/criteria#FORM-09` highlights the criterion |
| Quality | Audited by `ux_check` | Still audited on every PR: no axe violations, small targets, hidden focus or overflow on 7 representative pages |

#### Acceptance criteria

- [ ] Every page is generated from the repository; counts come from `catalogue.json` (tested)
- [ ] Every internal link resolves (tested)
- [ ] The audited pages pass `ux_check.mjs` at 320, 375 and 1280 px in light and dark (tested)
- [ ] Focus indicators reach 3:1 (shadcn's default gray ring replaced by the accent)

#### Out of scope

- A custom domain; analytics.
