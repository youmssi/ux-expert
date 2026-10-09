# ADR-004: Criteria as structured data

- **Status:** proposed
- **Date:** 2026-10-09
- **Story:** UXE-3

## Context

The 465 criteria currently live in Markdown tables inside each area file.
Agents read Markdown well, but tools cannot reliably query it. Upcoming work
needs to query the criteria:

- **Design mode** (UXE-4) selects criteria by phase (design, build, audit) and
  by product type.
- **The MCP server** (UXE-8) serves `get_criteria(area, product_type, phase)`.
- **Citation verification** (UXE-7) tracks a source and a `verified_on` date
  for each criterion.

## Options considered

1. **YAML catalogue as the source; Markdown tables generated.** One file per
   area (`criteria/<area>.yaml`) with a JSON Schema. A script renders the tables
   into the area files, and CI fails if they differ.
2. **Markdown as the source; a parser extracts data.** No new format, but
   fragile parsing and no place for structured fields (sources, phases).
3. **Do nothing.** Design mode and the MCP server re-implement criteria
   selection by reading prose.

## Decision

Option 1, to be confirmed when UXE-3 starts. Fields per criterion: `id`,
`name`, `check`, `fail_signal`, `severity` (default and range), `applies_to`
(product types), `phases`, `sources` (each with a `verified_on` date),
`status` (active | retired).

## Consequences

- Area files keep their prose; only the criteria tables are generated.
- A new criterion is added in YAML, never in the Markdown table.
- The schema becomes part of the public interface from v0.3 (MCP), so it
  follows semantic versioning.
