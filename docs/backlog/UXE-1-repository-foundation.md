### UXE-1 — Contributors know how to work on the package

**Type:** chore  ·  **Repos:** ux-expert  ·  **Dependencies:** none  ·  **Size:** S

#### Why

The package moves out of an unrelated repository into its own. Before any
content lands, contributors and coding agents need one agreed workflow, the
rules for code and content, and the decisions that shape the package
(layout, distribution, license) written down.

#### Decision

- Workflow: `main` / `develop` / `uxe-<n>-<slug>`, squash-merge stories, merge
  commits for releases (`CONTRIBUTING.md`).
- Distribution from a single source: [ADR-002](../adr/ADR-002-distribution-channels.md).
- Licensing: MIT for code, CC BY 4.0 for content: [ADR-003](../adr/ADR-003-licensing.md).
- Skill layout ([ADR-001](../adr/ADR-001-one-self-contained-skill.md)) and
  criteria as data ([ADR-004](../adr/ADR-004-criteria-as-data.md)) are recorded
  here and implemented in UXE-2 and UXE-3.

#### Behaviour

| Where | Before | After |
|---|---|---|
| Repository root | `README.md` with a title only | README, `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`, `LICENSE-CONTENT` |
| `docs/` | — | Engineering principles, content rules, templates, ADR-001 to ADR-004, roadmap and stories UXE-1 to UXE-5 |
| `.github/` | — | Pull request template |

#### Acceptance criteria

- [ ] `AGENTS.md` is the single entry point; `CLAUDE.md` only imports it
- [ ] `CONTRIBUTING.md` describes branches, story flow, checks, commits, review, release and the Definition of Done for this repository
- [ ] `docs/engineering/content.md` states the rules for skill content (progressive disclosure, permanent criterion IDs, sources for numbers)
- [ ] The roadmap lists every story to v1.0 and the known limitations
- [ ] Both license files are present and the README explains which applies to what
- [ ] No file mentions an AI tool as author of the work

#### Out of scope

- The skill content itself (UXE-2).
- CI checks (UXE-2 adds `scripts/validate.py` and the workflow).
