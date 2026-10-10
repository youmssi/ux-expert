<h1 align="center">ux-expert</h1>

<p align="center">
    Principal-level UX expertise for AI agents
</p>

<p align="center">
    <a href="https://github.com/youmssi/ux-expert/actions/workflows/ci.yml?query=branch%3Adevelop"><img src="https://img.shields.io/github/actions/workflow/status/youmssi/ux-expert/ci.yml?branch=develop&label=ci" alt="CI status"/></a>
    <a href="https://agentskills.io"><img src="https://img.shields.io/badge/Agent%20Skills-compatible-6f42c1" alt="Agent Skills compatible"/></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-blue" alt="Code license: MIT"/></a>
    <a href="LICENSE-CONTENT"><img src="https://img.shields.io/badge/content-CC%20BY%204.0-blue" alt="Content license: CC BY 4.0"/></a>
    <a href="https://github.com/youmssi/ux-expert/issues"><img src="https://img.shields.io/github/issues/youmssi/ux-expert" alt="Issues"/></a>
</p>

## Introduction

`ux-expert` gives any AI agent the working method of a principal UX engineer. It reviews products and changes across 28 areas of UX, backs every finding with evidence and a source, scores severity the same way every time, and ends with a launch verdict: Go, Conditional Go or No-Go.

It is not a generic checklist. Every judgement starts from the user's goal, cites `file:line`, a route or a measurement, and says how confident it is. The 565 criteria have permanent IDs (such as `FORM-09`), so a rule can be traced from design through to the launch report.

It works with Claude, ChatGPT, Gemini, Codex, Cursor, DeepSeek, Grok and any agent that supports [Agent Skills](https://agentskills.io) or MCP.

## Features

- **Design mode**: turn a brief or user stories into UX acceptance criteria, open product decisions and a UX Definition of Done before anything is built ([example](docs/examples/design-mode-team-tasks.md))
- **Refactor mode**: turn audit findings into a safe, sequenced plan of stories, each shippable alone and protected by a regression guard ([example](docs/examples/refactor-mode-plan.md))
- **Full audits**: review a whole product, or one flow, screen or area, and get a prioritized report
- **Launch gate**: an explicit Go / Conditional Go / No-Go decision, listing blockers and conditions
- **Change review**: check a pull request's UI changes and the regressions they could cause
- **28 areas, 565 criteria**: flows, information architecture, layout, typography, color, interaction, forms, states, accessibility (WCAG 2.2 AA), content, onboarding, performance, responsive and platform conventions, design system, trust and privacy, i18n, data display and search, developer experience, AI interfaces, measurement, launch readiness, collaboration, enterprise administration, notification systems, commerce and payments, in-product help, aesthetics and delight
- **Evidence-first findings**: every finding has a location, evidence type, severity, reach, confidence, priority, fix and verification step
- **Proven patterns**: 17 patterns from the public design systems of GOV.UK, GitHub (Primer), Shopify (Polaris) and IBM (Carbon), linked to the criteria they satisfy and cited in recommendations
- **Consistent scoring**: one model for every agent: severity S0–S4 × reach R1–R3 → priority P0–P3, with an explicit launch gate
- **Built for codebases**: search patterns for React, Vue, Svelte, Angular, CLIs and SDKs, plus 45 native probes for SwiftUI, Jetpack Compose, Flutter and React Native (`scripts/probe.py`), locate evidence in real code
- **Measured, not guessed**: `scripts/ux_check.mjs` takes screenshots and runs axe, target-size, focus and reflow checks on the running product
- **Stack packs**: versioned knowledge of Next.js, shadcn/ui and Radix, read from their own repositories at recorded commits: where the evidence is, defaults that make generic findings false positives, and probes ([list](skills/ux-expert/references/stacks.md))
- **Stable IDs**: criterion, pattern and probe IDs never change meaning or disappear within a major version ([stability policy](docs/stability.md))
- **Queryable catalogue**: criteria are validated YAML with a JSON Schema, ready for tools and the MCP server

## How it works

| Piece | Path | Role |
|---|---|---|
| Orchestrator | [`skills/ux-expert/SKILL.md`](skills/ux-expert/SKILL.md) | Picks the mode, selects the areas, runs the 8-phase procedure |
| Areas | [`skills/ux-expert/references/areas/`](skills/ux-expert/references/areas/) | One file per area: the expert mindset, procedure, criteria and code probes |
| Shared references | [`skills/ux-expert/references/`](skills/ux-expert/references/) | Finding format, severity and scoring, codebase recon, laws and thresholds, report template |
| Criteria catalogue | [`skills/ux-expert/criteria/`](skills/ux-expert/criteria/) | 565 criteria as YAML, with phases and product types; the area tables, the `SKILL.md` matrix and `catalogue.json` are generated from it |
| Refactor mode | [`references/refactor-mode.md`](skills/ux-expert/references/refactor-mode.md) | From audit findings to a sequenced, guarded plan |
| Design mode | [`references/design-mode.md`](skills/ux-expert/references/design-mode.md), [`assets/story-ux.md`](skills/ux-expert/assets/story-ux.md) | From brief to UX acceptance criteria per story |
| MCP server | [`mcp/`](mcp/) | Prompts, read-only tools and resources for any MCP client |
| Selector | [`scripts/select_criteria.py`](skills/ux-expert/scripts/select_criteria.py) | Lists the criteria for a product type and phase |

Agents load only what a task needs: the skill's description at startup, `SKILL.md` when the skill activates, and an area file only when the scope includes that area.

## Install

| Agent | How | Available |
|---|---|---|
| Claude Code | `/plugin marketplace add youmssi/ux-expert`, then `/plugin install ux-expert@ux-expert` | v0.1 |
| Any Agent Skills client (Codex, Gemini CLI, Cursor…) | Copy `skills/ux-expert/` into the client's skills directory | now |
| MCP clients (Claude Code, Cursor, VS Code, Codex, Gemini CLI…) | `npx -y ux-expert-mcp` — see [`mcp/README.md`](mcp/README.md) for each client | after the first npm release |
| Chat apps without skills or MCP (ChatGPT web, DeepSeek, Grok…) | Upload a single-file bundle from the GitHub release | from the first release |

Step-by-step instructions for each tool: [`docs/install.md`](docs/install.md). To wire ux-expert into your team's workflow (stories, PRs, releases): [`docs/use-in-your-project.md`](docs/use-in-your-project.md).

## Usage

Ask in plain words. The skill picks the mode:

```text
Write the UX acceptance criteria for these stories: <paste stories>.
Run a full UX audit of this app.
Plan how to fix these audit findings safely.
Are we ready to launch on November 1?
Audit the checkout flow.
Check accessibility only.
Review the UX of this pull request.
Review the developer experience of our SDK.
```

The audit writes `ux-audit-report.md` and summarizes the verdict, top issues, quick wins and coverage gaps in chat.

## Roadmap

| Version | Focus |
|---|---|
| v0.1 | One spec-compliant skill, validated in CI, criteria as data |
| v0.2 | **Design mode** (user story → UX acceptance criteria) and **refactor mode** (gap analysis → safe plan) |
| v0.3 | MCP server and single-file bundles for every agent |
| v0.4 | Evals on real products; calibrated severity |
| v0.5 | Best-in-class pattern library, runtime checks (contrast, axe, screenshots), native platforms |
| v0.6 | Collaboration, enterprise admin, notifications, commerce, in-product help, aesthetics |
| v1.0 | Stable criterion IDs and schema, documentation site |

The full backlog and the known limitations are in [`docs/backlog/`](docs/backlog/README.md). What stays stable across releases is in the [stability policy](docs/stability.md).

## Contributing

Contributions are welcome. Read [AGENTS.md](AGENTS.md) and [CONTRIBUTING.md](CONTRIBUTING.md): one story per branch, squash-merged into `develop`, with the checks green.

<a href="https://github.com/youmssi/ux-expert/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=youmssi/ux-expert" alt="Contributors" />
</a>

## License

Code is under the [MIT License](LICENSE); content (skill text, criteria, references) is under [CC BY 4.0](LICENSE-CONTENT). See [ADR-003](docs/adr/ADR-003-licensing.md) for details.
