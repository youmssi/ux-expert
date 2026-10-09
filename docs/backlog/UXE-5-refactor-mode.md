### UXE-5 — Teams can plan a deep UX refactor safely

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-4  ·  **Size:** M

#### Why

An audit lists problems but does not say how to fix many of them without
breaking what works. A team facing a deep refactor needs the fixes grouped by
root cause, ordered by dependency and risk, and protected against regressions.

#### Decision

Add a **refactor** mode. It runs the audit, then turns the findings into a
sequenced plan of stories: foundations first (tokens, shared components, error
handling), then flows, then polish. Each step has a regression guard.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `SKILL.md` modes | … + Design | + Refactor |
| `references/refactor-mode.md` | — | Procedure: audit → group by root cause → dependency graph → sequence (foundations → systemic fixes → flows → polish) → regression guards (visual, a11y and flow tests) → stories in the team's template |

#### Acceptance criteria

- [ ] Systemic findings (e.g. no tokens, many hard-coded colors) become one foundation story that comes before the screen-level stories depending on it
- [ ] Each planned story names the findings it closes, its regression guard and how to verify it
- [ ] The plan keeps every step shippable on its own (no long-lived branch)
- [ ] "Strengths to protect" from the audit become explicit regression guards
- [ ] Output stories follow the story template and carry criterion IDs

#### Out of scope

- Executing the refactor in code.
