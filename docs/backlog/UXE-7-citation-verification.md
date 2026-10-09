### UXE-7 — Every number in the skill can be traced to a checked source

**Type:** fix  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-6  ·  **Size:** M

#### Why

Agents repeat what the skill says with authority. Several figures were written from memory: if one is wrong, every audit that uses it is wrong in the same way, and users lose trust in the whole package.

#### Decision

A sources catalogue (`criteria/sources.yaml`, with a schema) records each source, what it backs, and how it was verified: **primary** (checked against the source's own text or official repository), **secondary** (confirmed through reputable sources quoting it), **unconfirmed** (searched, not confirmed: its numbers are not stated as fact), **unchecked** (classic references no threshold depends on). Criteria list their sources; text cites them as `[src:<id>]`; the generator renders `references/sources.md` and rejects unknown citations. Primary sources unreachable through the network proxy were read from their official GitHub repositories (w3c/wcag, GoogleChrome/web-vitals, w3c/i18n-drafts).

#### Behaviour

| Where | Before | After |
|---|---|---|
| `criteria/sources.yaml`, `sources.schema.json` | — | 20 sources: 3 primary, 13 secondary, 3 unconfirmed, 1 unchecked group |
| Criteria | No sources | 73 criteria list their sources |
| `references/sources.md` | — | Generated bibliography with status and verification |
| FORM-09 and forms area | "Validate on blur" | Validate on submit by default, live re-validation while correcting (GOV.UK and CMS design systems; early errors increase mistakes) |
| `laws-and-numbers.md` | First-click 87/46 %, inline validation +22 %, Penzo top-aligned labels stated as fact | Stated as unconfirmed, direction only; 5-users rule with its variance; text expansion per W3C table |
| Accessibility mindset | "30–40 %" without source | GDS 2017 (30–40 % of 142 issues) and Deque (57 % by volume, vendor) |
| Examples | Password minimum 12; validation on leaving a field | NIST SP 800-63B-4 minimum 15; validation on submit |

#### Acceptance criteria

- [ ] Every numeric threshold or research figure in the skill cites a source, or is labelled as an estimate
- [ ] Every source has a status, and verified sources say when and against what
- [ ] Numbers from unconfirmed sources are not stated as fact anywhere
- [ ] An unknown source cited by a criterion or in text fails the generator (tested)
- [ ] Guidance contradicted by verified sources is corrected in the criteria, areas and examples

#### Out of scope

- Re-checking sources on a schedule (a follow-up: re-verify yearly, or when a standard publishes a new version).
