### UXE-3 — Tools can query the criteria catalogue

**Type:** refactor  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-2  ·  **Size:** M

#### Why

Design mode, the MCP server and citation tracking all need to select criteria
by area, product type and phase. In Markdown tables, every consumer would have
to re-parse prose, and fields such as sources and phases have nowhere to live.

#### Decision

YAML catalogue as the source of truth, with tables generated
([ADR-004](../adr/ADR-004-criteria-as-data.md), moved to `accepted` in this
story).

#### Behaviour

| Where | Before | After |
|---|---|---|
| `skills/ux-expert/criteria/<area>.yaml` | — | One file per area; each criterion has `id`, `name`, `check`, `fail_signal`, `severity`, `applies_to`, `phases`, `sources`, `status` |
| `skills/ux-expert/criteria/schema.json` | — | JSON Schema for the catalogue |
| `scripts/generate.py` | — | Renders criteria tables into `references/areas/<area>.md` between markers |
| CI | Validate only | Also fails when the generated tables differ from the YAML (`generate.py --check`) |

#### Acceptance criteria

- [ ] All 465 criteria are in YAML with unchanged IDs, and the generated tables match the current content
- [ ] The schema rejects a missing field, an unknown severity, a malformed ID and a duplicate ID (tested)
- [ ] Editing a table by hand makes CI fail with a message naming the file
- [ ] `applies_to` and `phases` are filled for every criterion (reviewed per area)
- [ ] The YAML files sit inside the skill folder, so they are part of the installed skill and available to MCP

#### Out of scope

- Verifying each source (UXE-7); this story only adds the field, with what the
  text already cites.
