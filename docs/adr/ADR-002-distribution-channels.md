# ADR-002: Distribution channels from a single source

- **Status:** accepted
- **Date:** 2026-10-09
- **Story:** UXE-1

## Context

The package must be easy to load into many agents: Claude Code, OpenAI Codex
and ChatGPT, Gemini CLI, Cursor, DeepSeek, Grok and others. They differ in what
they support:

- **Agent Skills** (`SKILL.md` folders) is an open format, published by
  Anthropic in December 2025 and listed as supported by Claude Code, Codex,
  Gemini CLI and many other clients (see `docs/clients.mdx` in
  agentskills/agentskills).
- **MCP** (Model Context Protocol, current spec revision 2026-07-28) is
  supported by many clients that do not read skill folders.
- Some chat apps support neither, and only accept pasted or uploaded files.

## Options considered

1. **Skills only.** Simplest, but excludes MCP-only and plain chat clients.
2. **MCP only.** Wide reach, but skills-capable agents lose progressive
   disclosure and the install becomes a running process.
3. **Skills as the source, with generated MCP server and bundles.** One
   content tree; each channel is a build output.
4. **Do nothing.** Users copy files by hand, and the copies drift from the
   source.

## Decision

Option 3. `skills/ux-expert/` is the source of truth. From it we ship:

| Channel | Artifact | Version |
|---|---|---|
| Agent Skills | `skills/ux-expert/` in the Git repo, tagged releases | v0.1 |
| Claude Code plugin marketplace | `.claude-plugin/marketplace.json` | v0.1 |
| MCP server | npm package, TypeScript, stdio + Streamable HTTP, read-only: prompts (modes), resources (skill files, criteria), tools (criteria queries, scoring, contrast, launch gate) | v0.3 |
| Single-file bundles | Markdown per mode, attached to GitHub releases | v0.3 |

## Consequences

- Content changes once and reaches every channel at the next release.
- The MCP server is read-only: no network access, no code execution and no
  writes, so it is safe to install anywhere.
- The MCP server targets the current spec revision. Before v0.3, evaluate the
  "Skills over MCP" extension described for the 2026-07-28 revision, and prefer
  it if clients support it.
- Each release has to check every install path (CONTRIBUTING §7).
