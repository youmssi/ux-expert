### UXE-2 — Any skills-capable agent can install and load ux-expert

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-1  ·  **Size:** M

#### Why

The draft content is 23 interdependent skills that read files across each
other's folders. That breaks the Agent Skills specification and fails when only
part of it is installed. Agents and users need one package that installs in one
step and validates against the spec.

#### Decision

One self-contained skill, with areas as references
([ADR-001](../adr/ADR-001-one-self-contained-skill.md)). Validation uses the
reference validator `skills-ref` (agentskills/agentskills, pinned commit) plus
a repository script for rules the spec does not cover.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `skills/ux-expert/SKILL.md` | — | Orchestrator: modes, routing to areas, procedure, gotchas; frontmatter with name, description (≤ 1,024 characters, names every area), license and metadata |
| `skills/ux-expert/references/` | — | Shared references (finding format, severity and scoring, codebase recon, laws and numbers, report template) and `areas/<area>.md` for the 22 areas |
| `scripts/validate.py` | — | Checks: unique criterion IDs, every relative link resolves inside the skill, `SKILL.md` ≤ 500 lines, no link leaves the skill root; code blocks and inline code are ignored. Covered by unit tests |
| `.github/workflows/ci.yml` | — | Runs both checks on pull requests to `develop` and `main` |
| `.claude-plugin/marketplace.json` | — | Lists the `ux-expert` plugin |

#### Acceptance criteria

- [ ] `skills-ref validate skills/ux-expert` passes
- [ ] `python3 scripts/validate.py` passes, and fails with a precise message when an ID is duplicated, a link is broken or `SKILL.md` exceeds 500 lines (checked with temporary bad inputs)
- [ ] No file in `skills/` references a path outside `skills/ux-expert/`
- [ ] Every one of the 465 criteria from the draft is present exactly once, with its ID unchanged
- [ ] `SKILL.md` tells the agent **when** to read each reference file
- [ ] CI runs on pull requests and is green on this story's PR
- [ ] The README install instructions match the manifest

#### Out of scope

- Rewriting or trimming the area content (UXE-6).
- Criteria as data (UXE-3).
- Design and refactor modes (UXE-4, UXE-5).
