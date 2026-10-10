# ADR-007: Framework knowledge as versioned stack packs, read from upstream repositories

- **Status:** accepted
- **Date:** 2026-10-10
- **Story:** UXE-18

## Context

The criteria are framework-agnostic on purpose. Real projects are built on frameworks and component libraries
whose defaults change what a finding means: Radix already traps focus in a modal dialog, Next.js announces route
changes, shadcn/ui components are the team's own code. Without that knowledge an agent reports false positives
(a "missing" focus trap) and misses framework-specific defects (`error.tsx` not catching its own layout). Model
memory of these frameworks is often one or two major versions behind.

## Options considered

1. **Framework notes inside area files** — Pros: no new structure. Cons: every area grows for every framework; loaded even when unused; no version or source per note.
2. **Stack packs as data** — one YAML file per stack (`criteria/stacks/<id>.yaml`): detection, the version and upstream commit verified against, where evidence lives, gotchas each traced to a file in the upstream repository, probes, optional recipes. Generated pages are read only when the stack is detected. Pros: precise, versioned, loaded on demand, checked like the rest of the catalogue. Cons: packs age as frameworks release.
3. **Do nothing** — keep generic criteria. Cons: the false positives and misses above remain.

## Decision

Option 2. Packs are written by reading the framework's own repository at a recorded commit and summarizing in our
own words. Every gotcha links to its source file at that commit. A monthly workflow (`freshness.yml`) fails when a
pack is older than about six months, which triggers a re-read. Pack IDs and probe IDs are locked like criterion IDs.

## Consequences

- New stacks are added one per story, starting with web SaaS (Next.js, shadcn/ui, Radix) and test tooling (Playwright).
- Packs never restate generic UX rules; they cite criteria by ID and add only what the stack changes.
- A pack for a different major version than the project uses is a weaker source; the pack says so on its page.
- Revisit if packs grow past what one person can re-verify every six months; then drop the least used.
