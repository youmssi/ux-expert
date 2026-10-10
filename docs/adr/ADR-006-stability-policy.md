# ADR-006: Publish a stability policy enforced by an ID lock and an interface snapshot

- **Status:** accepted
- **Date:** 2026-10-10
- **Story:** UXE-16

## Context

Teams cite criterion IDs in stories, tickets and reports (`FORM-09`), and MCP clients call tools by name.
A rename or removal silently breaks those references. Until now permanence was a written rule
(AGENTS.md §3.4) that a careless edit could break without any check failing. A 1.0 release needs a
promise users can rely on, and the promise needs to be enforced by CI, not by memory.

## Options considered

1. **Policy text only** — document what is stable. Pros: no tooling. Cons: nothing stops a removed ID from shipping.
2. **Policy plus checks** — an append-only `criteria/ids.lock.json` maintained by `generate.py` (new IDs are added, removed IDs fail the check), a `schema_version` in `catalogue.json`, and a snapshot of the MCP interface compared in tests. Pros: breaking changes fail CI and need a deliberate edit. Cons: one more generated file; interface changes need a snapshot update.
3. **Do nothing** — keep 0.x semantics, where anything can change. Cons: teams cannot depend on the IDs.

## Decision

Option 2. The policy is in `docs/stability.md`. The lock and snapshot turn each promise into a failing check,
and the only way past them is a visible change in review.

## Consequences

- Removing a published ID now fails `generate.py --check`; retiring it is the supported path.
- Adding a tool, prompt or optional input means updating `mcp/interface.json` (`UPDATE_INTERFACE=1 npm test`) in the same PR.
- A breaking change needs a major version and a migration note; ADR-001's layout and ADR-004's catalogue become public contracts.
- Revisit when a second consumer format (e.g. a JSON Schema for findings) becomes public.
