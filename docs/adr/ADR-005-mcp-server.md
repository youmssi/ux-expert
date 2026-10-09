# ADR-005: MCP server design

- **Status:** accepted
- **Date:** 2026-10-09
- **Story:** UXE-8

## Context

ADR-002 chose to ship an MCP server built from the skill, so MCP clients that do not read skill folders can use the package. Facts checked when starting the work:

- The current MCP specification is revision **2026-07-28** (stateless core). The official TypeScript SDK implements it only in **v2** (`@modelcontextprotocol/server` 2.3.1, `@modelcontextprotocol/client` 2.3.1). `@modelcontextprotocol/sdk` 1.x is in maintenance and stops at 2025-11-25 (SDK README, typescript-sdk@b022522).
- No official "Skills over MCP" extension or SDK support was found. Community servers expose skills as resources under `skill://` URIs.
- The scoring rules (priority matrix, launch gate) existed only as prose, so a server tool would have had to duplicate them.

## Options considered

1. **SDK v1 (`@modelcontextprotocol/sdk`).** Widely deployed, but frozen before the current spec; a new package would start on a maintenance line.
2. **SDK v2, standard primitives.** Prompts for the three modes (user-chosen), tools for queries and computations (model-chosen, read-only), resources for every skill file under `skill://ux-expert/<path>`.
3. **Wait for a Skills-over-MCP extension.** Nothing to build on today.

## Decision

Option 2. A TypeScript package `ux-expert-mcp` in `mcp/`, stdio transport, Node.js 20+, SDK v2. It is **read-only**: no network, no code execution, no writes; every tool carries `readOnlyHint: true`. The skill is the single source of truth: the build copies `skills/ux-expert/` into the package, and the server reads `criteria/catalogue.json`, which now also carries the scoring rules from the new `criteria/scoring.yaml` (also rendered into `references/severity-and-scoring.md`).

## Consequences

- MCP clients get prompts, tools and resources from one `npx -y ux-expert-mcp`.
- Criteria selection exists twice, in the Python selector (agents without MCP) and in TypeScript (the server). Both read the same catalogue, and a test pins them to the same count, so they cannot drift silently.
- Clients that accept only remote HTTP servers (e.g. the ChatGPT web app) are not served by a stdio package; they use the single-file bundles (UXE-9). A hosted HTTP endpoint is a later option.
- Publishing to npm needs an `NPM_TOKEN` secret (or npm trusted publishing) configured by the maintainer.
- Revisit when an official Skills-over-MCP extension ships in the SDK.
