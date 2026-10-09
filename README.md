# ux-expert

Senior UX expertise packaged for AI agents.

`ux-expert` gives any AI agent (Claude, ChatGPT, Gemini, DeepSeek, Grok, Codex, Cursor…) the method of a principal UX engineer, so it can:

- **Design:** turn user stories into precise UX requirements and acceptance criteria before the backlog is written *(v0.2)*.
- **Refactor:** find the gaps in an existing product and plan the fixes in a safe order *(v0.2)*.
- **Audit:** review a product or a change across 22 areas of UX, score every finding the same way, and give a launch verdict: Go, Conditional Go or No-Go.

Every judgement starts from the user's goal, cites its evidence and its source, and is checked against a catalogue of more than 460 permanent, ID'd criteria (e.g. `FORM-09`). Those IDs let you trace a rule from the design phase through to the launch report.

> **Status:** pre-release (v0.1 in progress). See the [roadmap](docs/backlog/README.md).

## Coverage

| Foundation | Visual & interaction | Robustness | Platform & system | Specialist & go-to-market |
|---|---|---|---|---|
| Users and goals | Layout and hierarchy | Empty, loading and error states | Perceived performance | i18n and localization |
| Information architecture | Typography | Accessibility (WCAG 2.2 AA) | Responsive and platform | Data display and search |
| Flows and friction | Color and theming | Content and UX writing | Design system | Developer experience |
| | Interaction and feedback | Onboarding and activation | Trust, ethics and privacy | AI interfaces |
| | Forms and input | | | Measurement and validation |
| | | | | Launch readiness |

## Install

`ux-expert` follows the open [Agent Skills](https://agentskills.io) format, so it works in any agent that supports skills.

| Agent | How |
|---|---|
| Claude Code | `/plugin marketplace add youmssi/ux-expert`, then `/plugin install ux-expert@ux-expert` *(from v0.1)* |
| Any Agent Skills client (Codex, Gemini CLI, Cursor…) | Copy `skills/ux-expert/` into the client's skills directory |
| MCP clients (ChatGPT connectors, IDE agents…) | `npx ux-expert-mcp` *(v0.3)* |
| Chat apps without skills or MCP | Upload the single-file bundle from the GitHub release *(v0.3)* |

## Use

Ask in plain words, for example:

- "Run a full UX audit of this app."
- "Are we ready to launch?"
- "Audit the checkout flow."
- "Check accessibility only."
- "Review the developer experience of our SDK."

## Contributing

Read [`AGENTS.md`](AGENTS.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md). Work follows one story per branch, squash-merged into `develop`; releases go from `develop` to `main`.

## License

- Code (scripts, MCP server, tooling): [MIT](LICENSE)
- Content (skill text, criteria, references): [CC BY 4.0](LICENSE-CONTENT)

See [ADR-003](docs/adr/ADR-003-licensing.md) for the reasoning.
