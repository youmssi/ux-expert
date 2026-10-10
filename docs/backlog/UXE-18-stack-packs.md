### UXE-18 — Audits know what Next.js, shadcn/ui and Radix already do, and where they leave gaps

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-16  ·  **Size:** M

#### Why

Generic criteria do not know framework defaults. An agent reports a missing focus trap in a Radix dialog (Radix
traps focus), trusts `error.tsx` to catch a layout error (it does not), or blames shadcn/ui for an edit the team
made to its copy. Memory of these frameworks lags their releases: Next.js 16 deprecated `image.priority` and added
`retry` to error boundaries; shadcn/ui now defaults to Base UI.

#### Decision

Stack packs as data (ADR-007): one YAML per stack with detection, the version and upstream commit verified
against, where evidence lives, gotchas each linked to its source file at that commit, probes and optional
recipes. Content is read from each project's repository (cloned) and summarized in our own words. `probe.py`
detects packs; a monthly workflow flags packs older than six months. First packs: Next.js (App Router),
shadcn/ui, Radix Primitives.

#### Behaviour

| Where | Before | After |
|---|---|---|
| Recon on a Next.js + shadcn/ui project | Generic web probes only | `probe.py` names the packs to read and runs 15 stack probes |
| A Radix dialog without custom focus code | Possible "no focus trap" finding | Pack says it is built in; only overridden defaults are findings |
| `references/stacks/*.md` | — | Generated pages with sources at the verified commit; on the docs site too |
| Stale knowledge | Unnoticed | `freshness.yml` fails monthly for packs older than 183 days |

#### Acceptance criteria

- [ ] Every gotcha links to a file in the verified repository at the recorded commit
- [ ] Every probe matches its example and misses its counter-example; probe and pack IDs are locked (tested)
- [ ] `probe.py` detects packs from dependencies and root files, and `--stack` limits the run (tested)
- [ ] Pack pages pass the site audit (tested)

#### Out of scope

- Other frameworks (Remix/React Router, Nuxt, SvelteKit, Angular, MUI, Chakra): one story each, by demand.
- Playwright: UXE-19.
