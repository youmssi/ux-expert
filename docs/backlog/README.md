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
| [UXE-5](UXE-5-refactor-mode.md) | Refactor mode: gap analysis → sequenced, regression-safe improvement plan | M | in progress |
| UXE-6 | Content tightening: cut what agents already know, add gotchas, clear defaults, token budgets per file | M | to refine |
| UXE-7 | Citation verification: every number checked against its primary source, with a `verified_on` date | M | to refine |

## v0.3: every agent can load it

| Story | Title | Size | Status |
|---|---|---|---|
| UXE-8 | MCP server (TypeScript, read-only): prompts per mode, resources, criteria and scoring tools | L | to refine |
| UXE-9 | Single-file bundles per mode for chat apps; install guide per agent | S | to refine |

## v0.4: proven quality

| Story | Title | Size | Status |
|---|---|---|---|
| UXE-10 | Evals: test prompts and seeded-defect sample apps (web SaaS, AI chat), with and without the skill | L | to refine |
| UXE-11 | Severity calibration and description tuning from eval results | M | to refine |

## v0.5: depth

| Story | Title | Size | Status |
|---|---|---|---|
| UXE-12 | Best-in-class pattern library: dated, sourced patterns from widely praised products | M | to refine |
| UXE-13 | Runtime scripts: contrast calculator, axe scan, screenshot matrix, visual review | L | to refine |
| UXE-14 | Native platform probes: SwiftUI, Jetpack Compose, Flutter, React Native | M | to refine |

## v0.6: breadth

| Story | Title | Size | Status |
|---|---|---|---|
| UXE-15 | New areas: collaboration, enterprise admin, notification systems, commerce, in-product help, aesthetics and delight | L | to refine |

## v1.0: stable

| Story | Title | Size | Status |
|---|---|---|---|
| UXE-16 | Stability guarantees (criterion ID and schema policy), docs site, 1.0 release | M | to refine |

## Known limitations (tracked by the stories above)

- Never evaluated on real products yet: precision and recall unknown (UXE-10).
- Some research figures were written from memory and await primary-source checks
  (UXE-7).
- Code search patterns favour web and React (UXE-14).
- Pixel-level visual review needs runtime screenshots and design files, not
  code alone (UXE-13).
- Severity defaults are uncalibrated (UXE-11).
