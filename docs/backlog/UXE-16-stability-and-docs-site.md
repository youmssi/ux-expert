### UXE-16 — Teams can depend on IDs and interfaces, and read the package as a website

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-15  ·  **Size:** M

#### Why

Teams cite criterion IDs in stories and reports and call MCP tools by name. Until now their permanence was a
written rule that no check enforced. Reading 28 area files on GitHub is also slow for people who are not
running an agent: product managers, designers and reviewers.

#### Decision

A stability policy (`docs/stability.md`, ADR-006) lists what is public. Each promise has a check: an
append-only `criteria/ids.lock.json` maintained by the generator, a `schema_version` in `catalogue.json`,
and an MCP interface snapshot. A documentation site is generated from the same sources by a small script
(Python-Markdown, no site framework), published to GitHub Pages from `main`, and audited in CI with the
skill's own `ux_check.mjs`. Publishing 1.0.0 (tag, GitHub release, npm) is a maintainer action, not part of
this story.

#### Behaviour

| Where | Before | After |
|---|---|---|
| Removing a criterion, pattern or probe ID | Passes CI | Fails `generate.py --check`; retiring is the supported path |
| Changing an MCP tool, input or prompt | Passes CI | Fails `interface.test.ts` until `mcp/interface.json` is updated in the same PR |
| Documentation | Markdown on GitHub | A site with area pages, a filterable criteria catalogue, sources and guides |
| CI | Fixture checks only | The site must have no axe violations, small targets, hidden focus or reflow overflow |

#### Acceptance criteria

- [ ] Removing a published ID fails the check; retiring it passes (tested)
- [ ] Adding a criterion adds it to the lock in the same generator run (tested)
- [ ] The MCP interface snapshot fails on a renamed tool or input (tested by design: deep equality)
- [ ] Every internal link on the site resolves; no link points at a `.md` file on the site (tested)
- [ ] The site passes `ux_check.mjs` at 320, 375 and 1280 px in light and dark mode (tested)

#### Out of scope

- Publishing the 1.0.0 release (maintainer: release PR, tag, npm token).
- A custom domain for the site.
