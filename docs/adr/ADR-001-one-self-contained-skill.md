# ADR-001: One self-contained skill with area references

- **Status:** accepted
- **Date:** 2026-10-09
- **Story:** UXE-2

## Context

The first draft was 23 separate skills: an orchestrator (`ux-audit`) and 22
area skills (`ux-forms-input`, `ux-accessibility`…). Every area skill read shared
files from the orchestrator's folder (`../ux-audit/references/…`).

The Agent Skills specification (agentskills/agentskills, commit `69ef37e`)
requires:
- paths relative to the skill's own root, so a skill must not depend on files in
  another skill's folder;
- `SKILL.md` under 500 lines, with detail in `references/` loaded on demand.

Its authoring guidance warns that skills scoped too narrowly "force multiple
skills to load for a single task, risking overhead and conflicting
instructions".

In practice, an area is almost never used alone. A forms review still needs the
user context, the finding format and the scoring model.

## Options considered

1. **23 skills, shared files copied into each at build time.** Each area can
   trigger on its own. Cons: 22 copies of the shared references in the
   published output; 23 descriptions competing for activation; harder to
   install and to explain.
2. **One skill (`ux-expert`) whose areas are reference files.** `SKILL.md`
   routes by mode and scope, and loads `references/areas/<area>.md` only when
   needed. Pros: spec-compliant, one install, one description, no duplication,
   and the same tree feeds the MCP server and bundles. Cons: a single
   description has to cover every area so the skill triggers on narrow requests
   ("check our contrast").
3. **Do nothing.** The package fails `skills-ref validate` portability rules
   and breaks when one area skill is installed without the orchestrator.

## Decision

Option 2: one self-contained skill `skills/ux-expert/`, with the 22 areas as
`references/areas/<area>.md` and the shared material in `references/`.

## Consequences

- Install is one folder; the Claude plugin marketplace lists one plugin.
- `SKILL.md` must name the areas and their trigger words so narrow requests
  still activate the skill.
- If evals (UXE-10) show poor triggering for narrow requests, revisit by
  generating thin area skills from the same source (option 1, generated, never
  hand-copied).
