### UXE-9 — People can use ux-expert in any assistant, and wire it into their project

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-8  ·  **Size:** S

#### Why

Chat assistants such as the ChatGPT web app, DeepSeek or Grok load neither skill folders nor local MCP servers, and teams need to know *when* in their workflow to use the package, not only how to install it.

#### Decision

Generate release assets from the skill (never hand-copied): one Markdown bundle per mode with instructions for the assistant at the top, plus a zip of the skill for clients that install skills by upload. Link each client's official skills documentation (from agentskills/agentskills) rather than asserting install paths that differ by client and version.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `scripts/bundle.py` | — | Builds `ux-expert-{design,audit,refactor,full}.md` and `ux-expert-skill.zip` into `dist/`; the design bundles carry a design-phase criteria table in place of the selector script |
| `.github/workflows/release.yml` | npm publish only | Creates the GitHub release with the assets and the CHANGELOG section as notes |
| `docs/install.md` | — | Install per tool: Claude Code, Claude apps, Agent Skills clients, MCP clients, chat assistants |
| `docs/use-in-your-project.md` | — | Committing the skill, an AGENTS.md section, story template and Definition of Done additions, the workflow by moment |

#### Acceptance criteria

- [ ] Each bundle starts with instructions for the assistant and contains every file its mode needs (tested)
- [ ] The skill zip contains exactly the skill folder under `ux-expert/` (tested)
- [ ] A release tag produces a GitHub release with the 4 bundles and the zip
- [ ] The install guide covers every channel and links official client documentation
- [ ] The project guide says what to do at each moment: planning, PR, release, UX debt

#### Out of scope

- Hosted copies of the bundles (they are attached to releases).
