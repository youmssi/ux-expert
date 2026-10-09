### UXE-4 — Teams get UX acceptance criteria before writing the backlog

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-3  ·  **Size:** M

#### Why

Today the skill can only audit what already exists. Most UX defects are cheaper
to prevent in design: during system design, before the stories are written.
Teams need each story to carry precise, testable UX criteria that trace to the
same IDs the audit uses later.

#### Decision

Add a **design** mode to `SKILL.md`. Input: a product brief or a set of epics
and stories (any format). Output: per story, the UX requirements and acceptance
criteria, each tagged with criterion IDs, plus a product-level UX Definition of
Done.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `SKILL.md` modes | Audit, pre-launch gate, scoped, area deep-dive, change review | + Design |
| `references/design-mode.md` | — | Procedure: context discovery → flow design (remove, merge, reorder) → select criteria with `phase: design` per story and product type → write acceptance criteria → list open product decisions as `[INTERACTIVE STEP]` |
| `references/templates/story-ux.md` | — | A "UX acceptance criteria" block that drops into any story template |

#### Acceptance criteria

- [ ] Given a sample brief (web SaaS sign-up and onboarding), the mode produces, for each story, acceptance criteria that are observable, testable and tagged with criterion IDs
- [ ] Every story gets edge cases from the states, accessibility and content areas (empty, error, keyboard, copy), not only the happy path
- [ ] Product decisions are not guessed: they appear as `[INTERACTIVE STEP]` with options and a recommendation
- [ ] The produced UX Definition of Done is reusable as a checklist in a contributing guide
- [ ] Output fits the story template in `docs/templates/story.md` without restructuring it

#### Out of scope

- Generating whole stories from scratch (the team writes the stories; the mode
  adds UX criteria).
- Visual design or mockups.
