# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): a breaking change to
the skill layout, criterion schema or MCP interface is a major version.

## [Unreleased]

## [1.0.0] - 2026-10-10

First stable release. Criterion, pattern, probe and stack pack IDs, the skill
layout, `catalogue.json` and the MCP interface are now covered by the
[stability policy](docs/stability.md).

### Added

- Stack packs (`criteria/stacks/*.yaml`, generated `references/stacks.md` and
  `references/stacks/<id>.md`, ADR-007): Next.js 16 (App Router), shadcn/ui,
  Radix Primitives and Playwright Test 1.64 (with eight regression-guard recipes,
  type-checked in CI), each verified against the project's repository at a recorded
  commit, with gotchas traced to source files and probes. `scripts/probe.py`
  detects the stacks and runs their probes; `scripts/check_freshness.py` and a
  monthly workflow flag packs older than six months.

- Stability policy (`docs/stability.md`, ADR-006): criterion, pattern and probe
  IDs, the skill layout, `catalogue.json` (now with `schema_version`) and the
  MCP interface are public and stable within a major version. Enforced by
  `criteria/ids.lock.json` (published IDs cannot be removed, only retired) and
  `mcp/interface.json` (a snapshot of tools and prompts).
- Documentation site built from the repository (`scripts/build_site.py`):
  areas, a searchable criteria catalogue, patterns, probes, sources and guides;
  published to GitHub Pages from `main`. CI audits it with `ux_check.mjs`.

- Six areas (100 criteria; 28 areas and 565 criteria in total): collaboration
  (COLLAB), enterprise administration (ADMIN), notification systems (NOTIF),
  commerce and payments (COMM), in-product help (HELP), aesthetics and delight
  (AES), with sources for notification permissions, one-click unsubscribe and
  EU price-reduction rules.
- Native mobile probes (`criteria/probes.yaml`, generated
  `references/native-probes.md`): 45 code search probes for iOS (SwiftUI,
  UIKit), Android (Compose, Views), Flutter and React Native, with platform
  notes checked against each platform's source; `scripts/probe.py` detects the
  platforms in a project and runs them.
- Runtime checks: `scripts/ux_check.mjs` (Playwright + axe) saves screenshots
  per width and color scheme and reports axe violations, small targets, missing
  focus indicators, reflow overflow and blocked zoom, mapped to criterion IDs;
  `scripts/contrast.py` computes WCAG contrast with the standard library.
- Proven patterns (`criteria/patterns.yaml`, generated `references/patterns.md`):
  17 patterns from GOV.UK, GitHub Primer, Shopify Polaris and IBM Carbon, read
  from their repositories at recorded commits and linked to criteria; the MCP
  server's `find_patterns` tool returns them by criterion or words.
- Trigger evals: 20 realistic queries (10 should trigger, 10 near-misses) and
  `evals/run_triggers.py` to measure the description's trigger rate.
- Calibration tests that keep every criterion's severity consistent with the
  escalation rules.
- Evals (`evals/`): audit evals on two seeded-defect apps (34 defects, 4
  decoys) and a design-mode eval, answer keys, a grader producing Agent Skills
  `grading.json` and `benchmark.json`, and a runner comparing runs with and
  without the skill in clean workspaces.
- Release assets built by `scripts/bundle.py`: single-file bundles per mode
  (design, audit, refactor, full) for chat assistants, and the skill as a zip;
  the release workflow attaches them to the GitHub release.
- `docs/install.md` (every tool) and `docs/use-in-your-project.md` (wiring
  ux-expert into stories, pull requests and releases).
- **MCP server** `ux-expert-mcp` (`mcp/`): MCP 2026-07-28 over stdio on the
  official TypeScript SDK v2; prompts `ux-design`, `ux-audit`, `ux-refactor`;
  read-only tools `list_criteria`, `get_criterion`, `read_area`,
  `score_finding`, `launch_gate`, `contrast_ratio`; every skill file as a
  `skill://ux-expert/<path>` resource.
- Scoring rules as data (`criteria/scoring.yaml`); the priority matrix and
  launch-gate tables are generated from it.
- Sources catalogue (`criteria/sources.yaml`) and generated bibliography
  (`references/sources.md`): every source with its verification status and
  date; 73 criteria list their sources; text cites them as `[src:<id>]`.
- A Gotchas section in every area (77 concrete corrections, e.g. react-hook-form
  validation defaults, `rem` with a 62.5 % root, iOS Safari viewport limits,
  consent tools that block scripts with `type="text/plain"`).
- An estimated token budget per skill file, enforced by `validate.py`.
- **Refactor mode**: turns audit findings into a sequenced plan of shippable,
  guarded stories (safety → guards → foundations → migrations → flows →
  polish), with a dependency graph and measures
  (`references/refactor-mode.md`, worked example in `docs/examples/`).
- **Design mode**: turns a brief or user stories into UX requirements and
  testable acceptance criteria tagged with criterion IDs, open product decisions
  and a UX Definition of Done (`references/design-mode.md`,
  `assets/story-ux.md`, worked example in `docs/examples/`).
- Every criterion now has `phases` (design, build) and product types; each area
  has an applicability per product type. The `SKILL.md` matrix and
  `criteria/catalogue.json` are generated from them.
- `scripts/select_criteria.py` inside the skill lists the criteria for a
  product type and phase (standard library only).
- The generator fails when a skill file or example cites an unknown or retired
  criterion ID.
- Project README with status badges, features, how it works, install per
  agent, usage, roadmap and contributing.

- Criteria catalogue as data: `skills/ux-expert/criteria/<area>.yaml` with a
  JSON Schema; area tables are generated by `scripts/generate.py`, and CI fails
  when a table drifts from its YAML. Cross-references between criteria
  (`related`) are now structured.
- The `ux-expert` Agent Skill: one self-contained skill with 22 UX areas
  (465 criteria) as references, an orchestrating `SKILL.md` with five audit
  modes and a gotchas list, validated against the Agent Skills spec.
- Claude Code plugin marketplace manifest (`.claude-plugin/marketplace.json`).
- `scripts/validate.py` (criterion IDs, links, line budget) and CI.
- Repository foundation: contribution workflow, engineering and content rules,
  story and ADR templates, roadmap, and licensing (MIT for code, CC BY 4.0 for
  content).

### Fixed

- `ux_check.mjs` no longer reports inline links in table cells as small
  targets; WCAG 2.5.8 exempts inline targets in text.
- `generate.py` checks citations after writing the regenerated tables, so
  retiring a criterion needs one run, not two.
- Severity calibration: 17 WCAG-sourced criteria now reach S3 where
  accessibility law applies; 4 lost-work criteria reach S4; 4 legal-information
  criteria reach S3 where the law requires them.
- The skill description now says when to use the skill in the user's terms
  ("Use this skill whenever…"), including requests that never say "UX".
- FORM-09: validate on submit by default (GOV.UK and CMS design systems), not
  when the user leaves a field.
- Unconfirmed research figures (first click 87/46 %, inline validation +22 %,
  top-aligned labels fastest) are no longer stated as fact.
- Text expansion per the W3C table; password minimum 15 characters per NIST
  SP 800-63B-4 in the design-mode example.
