### UXE-15 — Audits cover collaboration, admin, notifications, commerce, help and visual polish

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-14  ·  **Size:** L

#### Why

Web SaaS products live or die on surfaces the 22 areas only touched in passing: shared documents and
permissions, admin consoles bought by IT, notifications, checkout and billing, help, and the visual polish
people judge first. Agents either skipped them or scattered findings across unrelated areas.

#### Decision

Six new areas, each with its own prefix, procedure, gotchas and criteria in YAML: `collaboration` (COLLAB),
`enterprise-admin` (ADMIN), `notifications` (NOTIF), `commerce` (COMM), `in-product-help` (HELP),
`aesthetics-delight` (AES). Overlaps point to the existing owner (`related`) instead of duplicating it:
pricing terms stay in TRUST, message wording in CONT, motion rules in INT. Collaboration, admin and
commerce are `conditional` on the product actually having them. Aesthetics criteria must be observable
("mixed radii for the same element"), never taste ("looks dated"). Platform and legal facts are checked
against primary sources where reachable, otherwise recorded as secondary.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `references/areas/` | 22 areas, 465 criteria | 28 areas, 565 criteria |
| `SKILL.md` | No route for these topics | Area table rows, applicability matrix, description mentions checkout, notifications, collaboration and admin consoles |
| `criteria/sources.yaml` | — | Apple and Android notification permissions (primary), one-click unsubscribe and EU price-reduction rules (secondary) |
| Published counts | Hand-edited | Checked against the catalogue by `scripts/test_counts.py` |

#### Acceptance criteria

- [ ] Every new criterion has an observable fail signal and a severity that passes the calibration rules
- [ ] Every new area has Scope (with outs pointing to existing areas), Procedure, Gotchas, Output, Done when
- [ ] Every number cites a recorded source; legal claims from unreachable sites are marked secondary
- [ ] Counts in README, SKILL.md, MCP package and plugin manifest match the catalogue (tested)

#### Out of scope

- Seeded-defect eval fixtures for the new areas (follow-up).
- Region-by-region payment and consumer law.
