# ux-expert-mcp

MCP server for [ux-expert](https://github.com/youmssi/ux-expert): principal-level UX expertise for any MCP client. It turns stories into UX acceptance criteria, audits products and changes across 22 areas, plans safe refactors, and scores findings the same way every time.

- **Read-only and local:** no network access, no code execution, no writes. It serves the skill's files and computes from them.
- **Protocol:** MCP 2026-07-28 over stdio, with older revisions negotiated automatically (official TypeScript SDK v2).

## What it exposes

| Kind | Name | Use |
|---|---|---|
| Prompt | `ux-design` | Brief or stories → UX requirements and acceptance criteria tagged with criterion IDs |
| Prompt | `ux-audit` | Full audit, pre-launch gate, scoped audit, area deep-dive or change review |
| Prompt | `ux-refactor` | Audit findings → sequenced, guarded refactor plan |
| Tool | `list_criteria` | Criteria for a product type, phase (design/build) and areas |
| Tool | `get_criterion` | One criterion with its sources and area file |
| Tool | `read_area` | An area's procedure, criteria, code probes and gotchas |
| Tool | `find_patterns` | Proven patterns from GOV.UK, GitHub Primer, Shopify Polaris and IBM Carbon, by criterion or words |
| Tool | `score_finding` | Severity × reach × confidence → priority, quick win |
| Tool | `launch_gate` | Go / Conditional Go / No-Go from the audit counts |
| Tool | `contrast_ratio` | WCAG 2.2 contrast of two colors, pass/fail for text and UI |
| Resources | `skill://ux-expert/<path>` | Every file of the skill (`SKILL.md`, references, criteria, sources) |

## Install

Requires Node.js 20 or later. Every client runs the same command: `npx -y ux-expert-mcp`.

**Claude Code**

```sh
claude mcp add ux-expert -- npx -y ux-expert-mcp
```

**Claude Desktop, Cursor (`.cursor/mcp.json`), Gemini CLI (`settings.json`) and most JSON-configured clients**

```json
{
  "mcpServers": {
    "ux-expert": { "command": "npx", "args": ["-y", "ux-expert-mcp"] }
  }
}
```

**VS Code (`.vscode/mcp.json`)**

```json
{
  "servers": {
    "ux-expert": { "type": "stdio", "command": "npx", "args": ["-y", "ux-expert-mcp"] }
  }
}
```

**OpenAI Codex CLI (`~/.codex/config.toml`)**

```toml
[mcp_servers.ux-expert]
command = "npx"
args = ["-y", "ux-expert-mcp"]
```

Configuration formats change between client versions; check your client's MCP documentation if a key is not recognized.

Clients that only accept remote (HTTP) servers, such as the ChatGPT web app, cannot launch a local stdio server. Use the single-file bundles from the [GitHub releases](https://github.com/youmssi/ux-expert/releases) there instead.

## Use

Pick a prompt in your client (often a slash command or a prompt menu), or ask in plain words. The model then calls the tools, for example:

```text
Write the UX acceptance criteria for these stories: …
Audit the checkout flow in this repository.
Is #9CA3AF on white readable for body text?
```

## Development

The server reads the skill from the repository (`../skills/ux-expert`) during development; `npm run build` copies it into `skill/` for publishing.

```sh
npm ci
npm test        # builds, then runs unit, in-process protocol and stdio tests
npx @modelcontextprotocol/inspector node dist/index.js
```

## License

Code: MIT. Skill content: CC BY 4.0. See `LICENSE` and `LICENSE-CONTENT`.
