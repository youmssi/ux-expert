### UXE-19 — Every fix comes with a Playwright guard that compiles

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-18  ·  **Size:** S

#### Why

Refactor mode asks for a regression guard per story, but agents wrote guards from memory: CSS selectors that
check nothing about accessibility, axe scans of closed menus, `.exclude()` calls that silence every rule, and
API calls that no longer exist. Tests then pass while users still fail.

#### Decision

A Playwright stack pack (ADR-007), verified against microsoft/playwright at a recorded commit (1.64): gotchas that
make tests pass while users fail (`toBeVisible` on `opacity: 0`, `force: true`, service workers hiding routes,
per-platform baselines), probes for weak guards, and eight recipes mapped to criteria. A runtime-check test
type-checks every recipe against the pinned `@playwright/test` and `@axe-core/playwright`.

#### Behaviour

| Where | Before | After |
|---|---|---|
| Refactor-mode guards | Written from memory | Start from recipes that compile against Playwright 1.64 |
| Playwright projects | No pack | `probe.py` detects Playwright and flags CSS locators, forced clicks, axe exclusions, missing a11y guards |
| CI | — | Recipes type-check; a broken recipe fails the build |

#### Acceptance criteria

- [ ] Each gotcha links to its file in microsoft/playwright at the verified commit
- [ ] All recipes type-check in CI against the pinned versions (tested)
- [ ] Refactor mode points to the recipes

#### Out of scope

- Running the recipes against a sample app (they target the project being audited).
- Cypress or WebdriverIO packs.
