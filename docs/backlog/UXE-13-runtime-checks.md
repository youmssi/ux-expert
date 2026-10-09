### UXE-13 — Audits measure the running product instead of guessing from code

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-12  ·  **Size:** L

#### Why

Static analysis caps visual and behavioural findings at Medium confidence: CSS can be overridden, focus styles come from libraries, and contrast depends on what actually renders. Agents need a repeatable way to collect measured evidence when the product can run.

#### Decision

Ship two scripts in the skill: `ux_check.mjs` (Playwright and axe-core, resolved from the project it runs in, so the skill adds no dependency of its own) and `contrast.py` (standard library, for agents without Node or MCP). Results are evidence for findings, mapped to criterion IDs, never findings by themselves. A test harness with a fixture of known problems runs both in CI with a real Chromium.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `scripts/ux_check.mjs` | — | Screenshots per width and scheme; axe WCAG 2.2 A/AA violations; targets under 24 px; focus without indicator; overflow at 320 px; blocked zoom; `report.json` with criterion IDs |
| `scripts/contrast.py` | — | WCAG ratio and pass/fail, same reference values as the MCP tool |
| `references/codebase-recon.md`, `SKILL.md` | "Run axe and Lighthouse if possible" | When and how to run the scripts, and to verify each item before reporting it |
| `tools/runtime-check/` and CI | — | Fixture page with known problems, 5 tests against Chromium |

#### Acceptance criteria

- [ ] On the fixture, the check reports contrast and missing alt text (axe), the 16 px target, the focus without indicator, the 320 px overflow and blocked zoom (tested)
- [ ] It does not flag an element whose `outline: none` has a `:focus-visible` replacement (tested)
- [ ] `contrast.py` and the MCP tool agree on reference values (tested)
- [ ] A missing dependency produces an instruction, not a stack trace

#### Out of scope

- Lighthouse performance runs (PERF evidence stays manual; budgets in CI are a team's choice).
- Comparison with design files.
