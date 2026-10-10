### UXE-6 — Agents avoid the mistakes they would otherwise make in each area

**Type:** refactor  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-5  ·  **Size:** M

#### Why

The Agent Skills authoring guidance calls gotchas "the highest-value content" in a skill: concrete corrections to mistakes an agent makes without being told. The area files had procedures and criteria but no gotchas, offered menus where a default was needed, and nothing kept files within the token budget as content grows.

#### Decision

Every area gets a Gotchas section (3–4 corrections, each about a framework, standard or tool behaviour that defies a reasonable assumption). Size is enforced per file instead of rewriting content that is already within budget (largest file ≈ 3,600 estimated tokens).

#### Behaviour

| Where | Before | After |
|---|---|---|
| `references/areas/*.md` | No gotchas | A `## Gotchas` section before `## Output` in all 22 areas (77 items) |
| `references/areas/accessibility.md` | "VoiceOver, NVDA or TalkBack" | A default screen-reader and browser pairing, with a confidence rule when none is available |
| `SKILL.md` | — | Area briefs and the sequential run tell the agent to read each area's Gotchas first |
| `scripts/validate.py` | Line budget for `SKILL.md` only | Also an estimated token budget (5,000, about 4 characters per token) for every Markdown file in the skill |

#### Acceptance criteria

- [ ] All 22 area files have a Gotchas section with concrete, checkable corrections (no generic advice)
- [ ] `SKILL.md` routes the agent to the gotchas before findings are written
- [ ] A Markdown file over the token budget fails `validate.py` with its estimated size (tested)
- [ ] Every skill file stays within the budget

#### Out of scope

- Citation verification of the numbers in the content (UXE-7).
- Changes driven by eval results (UXE-10, UXE-11).
