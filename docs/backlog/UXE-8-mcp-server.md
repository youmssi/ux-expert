### UXE-8 — Any MCP client can use ux-expert with one command

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-7  ·  **Size:** L

#### Why

Many agents and IDEs speak MCP but do not read Agent Skills folders. Without a server, their users copy files by hand, and the copies drift from the source.

#### Decision

A read-only TypeScript MCP server on the official SDK v2 (MCP 2026-07-28), built from the skill ([ADR-005](../adr/ADR-005-mcp-server.md)). Scoring rules move into data so the server reuses them instead of duplicating prose.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `mcp/` | — | `ux-expert-mcp` package: prompts `ux-design`, `ux-audit`, `ux-refactor`; tools `list_criteria`, `get_criterion`, `read_area`, `score_finding`, `launch_gate`, `contrast_ratio`; every skill file as a `skill://ux-expert/<path>` resource |
| `criteria/scoring.yaml` | Matrix and gate as prose | Data with a schema; tables in `severity-and-scoring.md` and `catalogue.json` generated from it |
| CI | Python checks | + `mcp` job: build, tests, package contents |
| `.github/workflows/release.yml` | — | Publishes the package to npm with provenance on a `vX.Y.Z` tag |

#### Acceptance criteria

- [ ] The server negotiates MCP 2026-07-28 and still serves older clients
- [ ] Prompts, tools and resources are listed and work through a real client, in-process and over stdio (tested)
- [ ] Every tool is annotated read-only; invalid arguments are rejected before the tool runs (tested)
- [ ] Scoring results match the tables in `severity-and-scoring.md`, which are generated from the same data
- [ ] The packed tarball contains the skill, the build and both licenses (checked in CI)
- [ ] Install instructions cover Claude Code, JSON-configured clients, VS Code and Codex, and state the remote-only limitation

#### Out of scope

- A hosted HTTP endpoint (later, if remote-only clients need it).
- Publishing to npm (the maintainer adds `NPM_TOKEN` and tags a release).
