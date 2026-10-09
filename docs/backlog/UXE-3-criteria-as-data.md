### UXE-3 — Tools can query the criteria catalogue

**Type:** refactor  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-2  ·  **Size:** M

#### Why

Design mode, the MCP server and citation tracking all need to select criteria
by area, product type and phase. In Markdown tables, every consumer would have
to re-parse prose, and fields such as sources and phases have nowhere to live.

#### Decision

YAML catalogue as the source of truth, with tables generated
([ADR-004](../adr/ADR-004-criteria-as-data.md), accepted in this story).
Fields are added by the stories that read them: `applies_to` and `phases` in
UXE-4, `sources` in UXE-7.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `skills/ux-expert/criteria/<area>.yaml` | — | One file per area; each criterion has `id`, `name`, `check` (optional), `fail_signal`, `severity`, `severity_note` and `related` (optional), `status` |
| `skills/ux-expert/criteria/schema.json` | — | JSON Schema for the catalogue |
| `scripts/generate.py` | — | Renders criteria tables into `references/areas/<area>.md` between markers |
| CI | Validate only | Also fails when the generated tables differ from the YAML (`generate.py --check`) |

#### Acceptance criteria

- [ ] All 465 criteria are in YAML with unchanged IDs, and the generated tables match the current content (identical except severity cells reformatted with the same meaning)
- [ ] The schema rejects a missing field, an unknown severity, a malformed ID and a duplicate ID (tested)
- [ ] Editing a table by hand makes CI fail with a message naming the file
- [ ] Cross-references in severity cells ("→ TRUST-03") become `related` entries that must point to an existing area or criterion
- [ ] The YAML files sit inside the skill folder, so they are part of the installed skill and available to MCP

#### Out of scope

- `applies_to` and `phases` (UXE-4) and `sources` (UXE-7).
