### UXE-10 — We can measure whether the skill makes agents better at UX work

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-9  ·  **Size:** L

#### Why

Without evals, nobody knows whether the skill finds real problems, invents false ones, or helps at all compared with an agent working alone. Every content change is a guess.

#### Decision

Follow the Agent Skills eval method: realistic prompts, run with and without the skill in clean contexts, graded by assertions, aggregated into a benchmark. Audit evals use fixtures with **seeded defects and decoys** and an answer key, so recall and false positives are graded by a script rather than by opinion. Fixtures and answer keys live in `evals/` at the repository root, outside the installed skill, so users do not download them.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `evals/evals.json` | — | 3 cases: audit of a web sign-up app, audit of an AI assistant, design mode on a mobile brief |
| `evals/fixtures/` | — | signup-app (23 defects, 3 decoys), ai-chat (11 defects, 1 decoy), clinic-brief; answer keys separate and never copied into the agent's workspace |
| `evals/grade.py` | — | Recall, false positives, unknown IDs, finding completeness; design structure; `grading.json` and `benchmark.json` |
| `evals/run.sh` | — | Clean workspaces per run, with and without the skill, then grading and benchmark |
| CI | — | Grader tests; answer keys must reference real files and criteria; fixtures must not reveal answers |

#### Acceptance criteria

- [ ] Every seeded defect and decoy points to a real fixture file and real criterion IDs (tested)
- [ ] Fixtures contain no hint of the answers (tested)
- [ ] The grader scores a perfect report 100 %, catches decoys, and reports unknown IDs and incomplete findings (tested)
- [ ] The runner never exposes the answer keys and isolates each run
- [ ] The README explains how to run, grade and record results

#### Out of scope

- Recording the first clean-context benchmark: it needs an authenticated agent and spends tokens, so it is a maintainer step (see `evals/README.md`).
- Trigger evals for the description (UXE-11).
