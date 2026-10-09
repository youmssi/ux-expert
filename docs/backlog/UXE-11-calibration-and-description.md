### UXE-11 — Severities follow the rules, and the skill activates when it should

**Type:** fix  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-10  ·  **Size:** M

#### Why

Default severities were set area by area and never checked against the skill's own escalation rules, so a legal accessibility failure could be scored S2 and lost work S3. The description listed what the skill covers rather than when to use it, which the Agent Skills guide identifies as the main cause of skills not triggering.

#### Decision

Calibrate against the escalation rules in `severity-and-scoring.md`, enforced by tests on the real catalogue, rather than adjusting by feel. Rewrite the description in the guide's style (imperative, user intent, explicit about requests that never say "UX") and add the guide's trigger eval: 20 queries, half near-misses. Calibration against reviewed eval runs follows once the first benchmark exists.

#### Behaviour

| Where | Before | After |
|---|---|---|
| 17 WCAG-sourced criteria | Capped at S2 | S2–S3, S3 where accessibility law applies |
| FORM-21, STATE-16, FLOW-10, STATE-11 | Capped at S3 | S3–S4, S4 when user-created content is lost |
| IA-20, TRUST-20, CONT-17, I18N-23 | Capped at S2 | S2–S3 with the legal condition |
| `scripts/test_calibration.py` | — | The three escalation rules, and S4 kept rare, checked on the catalogue |
| `SKILL.md` description | A list of covered topics | "Use this skill whenever…", by user intent (772 characters) |
| `evals/trigger_queries.json`, `run_triggers.py` | — | 20 queries and a trigger-rate runner |

#### Acceptance criteria

- [ ] The calibration tests fail on the previous catalogue and pass on the new one
- [ ] WCAG references kept in notes where they were (2.4.4, 1.3.5, 3.3.7, 2.5.2)
- [ ] The description stays under 1,024 characters and passes `skills-ref validate`
- [ ] The trigger set has 10 positives, most not naming the domain, and 10 near-miss negatives (tested)

#### Out of scope

- Running the trigger and output evals (maintainer step; they spend model tokens).
