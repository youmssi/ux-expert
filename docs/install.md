# Install ux-expert in your agent

Pick the row for your tool. Every channel ships the same content, built from `skills/ux-expert/`.

| Your tool | Channel | Effort |
|---|---|---|
| Claude Code | Plugin marketplace, or copy the skill folder | 1 minute |
| Claude apps (claude.ai, desktop) | Upload the skill zip | 1 minute |
| Other Agent Skills clients: OpenAI Codex, Gemini CLI, Cursor, VS Code and GitHub Copilot, Kiro, Junie, OpenCode, Goose, Roo Code… | Copy the skill folder | 1 minute |
| MCP clients | `npx -y ux-expert-mcp` | 1 minute |
| ChatGPT (web and Projects), DeepSeek, Grok, Gemini web, any chat assistant | Upload a single-file bundle | 1 minute |

Release assets (bundles and the skill zip) are attached to each [GitHub release](https://github.com/youmssi/ux-expert/releases).

## Claude Code

Plugin (gets updates with each release):

```text
/plugin marketplace add youmssi/ux-expert
/plugin install ux-expert@ux-expert
```

Or copy the folder: into `.claude/skills/ux-expert/` in a repository (shared with the team through git), or into `~/.claude/skills/ux-expert/` for all your projects.

```sh
git clone --depth 1 https://github.com/youmssi/ux-expert /tmp/ux-expert
cp -r /tmp/ux-expert/skills/ux-expert .claude/skills/
```

## Claude apps

Download `ux-expert-skill.zip` from the latest release and upload it as a custom skill; see Anthropic's [Agent Skills documentation](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview).

## Other Agent Skills clients

Copy `skills/ux-expert/` into the skills directory your client reads. Each client documents its location:

| Client | Skills documentation |
|---|---|
| OpenAI Codex (ChatGPT & Codex) | <https://developers.openai.com/codex/skills/> |
| Gemini CLI | <https://geminicli.com/docs/cli/skills/> |
| Cursor | <https://cursor.com/docs/context/skills> |
| VS Code | <https://code.visualstudio.com/docs/copilot/customization/agent-skills> |
| GitHub Copilot | <https://docs.github.com/en/copilot/concepts/agents/about-agent-skills> |
| Kiro | <https://kiro.dev/docs/skills/> |
| JetBrains Junie | <https://junie.jetbrains.com/docs/agent-skills.html> |
| OpenCode | <https://opencode.ai/docs/skills/> |
| Goose | <https://block.github.io/goose/docs/guides/context-engineering/using-skills/> |
| Roo Code | <https://docs.roocode.com/features/skills> |

The full list of compatible clients is on [agentskills.io](https://agentskills.io).

## MCP clients

See [`mcp/README.md`](../mcp/README.md) for the setup of Claude Code, Claude Desktop, Cursor, VS Code, Gemini CLI and Codex. The server runs locally over stdio and is read-only.

## Chat assistants without skills or MCP

1. Download the bundle for the job from the latest release:

   | Bundle | For | Size (≈ tokens) |
   |---|---|---|
   | `ux-expert-design.md` | UX acceptance criteria before building | 29k |
   | `ux-expert-audit.md` | Audits, change reviews, launch gate | 70k |
   | `ux-expert-refactor.md` | Turning audit findings into a plan | 12k |
   | `ux-expert-full.md` | Everything | 87k |

2. Upload it: in **ChatGPT**, to a Project's files or a custom GPT's knowledge; in **DeepSeek**, **Grok** or **Gemini**, as a file in the chat. If uploads are not possible, paste the design or refactor bundle; the audit bundle is too long to paste in most chats.
3. Ask, for example: *"Use the ux-expert instructions in the attached file. Write the UX acceptance criteria for these stories: …"*

A bundle gives the assistant the method, criteria and sources, but not your code: paste or attach the screens, flows or code you want reviewed.

To build the assets yourself: `python3 scripts/bundle.py` (writes to `dist/`).
