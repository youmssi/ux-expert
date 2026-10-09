# Changelog

All notable changes to this package are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow
[Semantic Versioning](https://semver.org/spec/v2.0.0.html): a breaking change to
the skill layout, criterion schema or MCP interface is a major version.

## [Unreleased]

### Added

- The `ux-expert` Agent Skill: one self-contained skill with 22 UX areas
  (465 criteria) as references, an orchestrating `SKILL.md` with five audit
  modes and a gotchas list, validated against the Agent Skills spec.
- Claude Code plugin marketplace manifest (`.claude-plugin/marketplace.json`).
- `scripts/validate.py` (criterion IDs, links, line budget) and CI.
- Repository foundation: contribution workflow, engineering and content rules,
  story and ADR templates, roadmap, and licensing (MIT for code, CC BY 4.0 for
  content).
