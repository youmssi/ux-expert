# Roadmap and backlog

The source of truth for scope. Stories are taken **in order**, one at a time:
each one is squash-merged into `develop` before the next one starts. A story
that is only a line here gets its story file (from `docs/templates/story.md`)
as the first commit of its own PR.

Priorities: web SaaS and AI products first, then mobile. Content is in English.

## v0.1: a correct, installable package

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-1](UXE-1-repository-foundation.md) | Repository foundation: workflow, rules, templates, ADRs, licenses | S | done |
| [UXE-2](UXE-2-spec-compliant-skill.md) | One spec-compliant `ux-expert` skill, validated in CI, installable as a Claude plugin | M | done |
| [UXE-3](UXE-3-criteria-as-data.md) | Criteria as a YAML catalogue with schema; tables generated and drift-checked | M | done |
| [UXE-17](UXE-17-project-readme.md) | Project README in the structure of established open-source projects | S | done |

## v0.2: design and refactor, not only audit

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-4](UXE-4-design-mode.md) | Design mode: user story → UX requirements, acceptance criteria and Definition of Done | M | done |
| [UXE-5](UXE-5-refactor-mode.md) | Refactor mode: gap analysis → sequenced, regression-safe improvement plan | M | done |
| [UXE-6](UXE-6-content-tightening.md) | Content tightening: gotchas in every area, clear defaults, token budgets per file | M | done |
| [UXE-7](UXE-7-citation-verification.md) | Citation verification: every number traced to a checked source, with status and date | M | done |

## v0.3: every agent can load it

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-8](UXE-8-mcp-server.md) | MCP server (TypeScript, read-only, MCP 2026-07-28): prompts per mode, resources, criteria and scoring tools | L | done |
| [UXE-9](UXE-9-bundles-and-install-guide.md) | Single-file bundles per mode for chat apps; install guide per agent; using it in a project | S | done |

## v0.4: proven quality

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-10](UXE-10-evals.md) | Evals: test prompts and seeded-defect sample apps (web SaaS, AI chat), with and without the skill | L | done |
| [UXE-11](UXE-11-calibration-and-description.md) | Severity calibration against the escalation rules; description rewritten and a trigger eval set | M | done |

## v0.5: depth

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-12](UXE-12-pattern-library.md) | Best-in-class pattern library: dated, sourced patterns from the public design systems of widely used products | M | done |
| [UXE-13](UXE-13-runtime-checks.md) | Runtime scripts: contrast calculator, axe scan, screenshot matrix, visual review | L | done |
| [UXE-14](UXE-14-native-probes.md) | Native platform probes: SwiftUI, Jetpack Compose, Flutter, React Native | M | done |

## v0.6: breadth

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-15](UXE-15-new-areas.md) | New areas: collaboration, enterprise admin, notification systems, commerce, in-product help, aesthetics and delight | L | done |

## v1.0: stable

| Story | Title | Size | Status |
|---|---|---|---|
| [UXE-16](UXE-16-stability-and-docs-site.md) | Stability guarantees (criterion ID and schema policy), docs site, 1.0 release | M | done |
| [UXE-18](UXE-18-stack-packs.md) | Stack packs: versioned framework knowledge read from upstream repositories (Next.js, shadcn/ui, Radix) | M | done |
| [UXE-19](UXE-19-playwright-pack.md) | Playwright pack: turn criteria into regression guards (ARIA snapshots, axe, emulation, screenshots) | S | done |

## Known limitations (tracked by the stories above)

- The eval harness exists (UXE-10), but no clean-context benchmark has been
  recorded yet: recall and false-positive rates are still unmeasured.
- Research figures are traced to sources (UXE-7); 3 remain unconfirmed and are
  not stated as fact. Sources need re-checking when standards change.
- Native mobile evidence comes from code probes (UXE-14); there are no runtime
  checks on devices or simulators.
- Visual review relies on runtime screenshots (UXE-13); comparison with design
  files (Figma) is not covered.
- Severity defaults are calibrated against the escalation rules (UXE-11), not
  yet against reviewed eval runs.
