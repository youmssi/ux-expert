# Evals

Evidence that the skill makes agents better at UX work, and a guard against regressions. Built on the Agent Skills guidance for evaluating skills (agentskills.io, "Evaluating skill output quality").

## What is here

| Path | What |
|---|---|
| `evals.json` | The test cases: realistic prompts, expected output, assertions (Agent Skills format, plus `kind` and `answer_key`) |
| `fixtures/signup-app/` | A small React sign-up, onboarding and dashboard app with **23 seeded defects** and **3 decoys** (correct code that looks suspicious) |
| `fixtures/ai-chat/` | An AI sales assistant with **11 seeded defects** and **1 decoy** |
| `fixtures/clinic-brief/` | A mobile booking brief for design mode |
| `fixtures/*/answers.yaml` | Answer keys: never shown to the agent under test |
| `grade.py` | Grades a report against the answer key (recall, false positives, unknown IDs, format) or the design structure; aggregates a benchmark |
| `run.sh` | Runs every eval with and without the skill in clean workspaces, then grades them |

## How grading works

- **Audit evals:** a seeded defect counts as found when one finding (a `### F-…` block) names its file and any of the criterion IDs the key accepts. A decoy reported the same way is a false positive. Assertions: recall ≥ 0.7, no decoy reported, every cited ID exists, every finding has severity, priority, recommendation and verification.
- **Design eval:** each story has 5–15 tagged acceptance criteria, covers states and accessibility, cites only real IDs, raises at least one `[INTERACTIVE STEP]`, and ends with a UX Definition of Done.
- Qualities a script cannot judge (clarity of recommendations, sensible severities) are reviewed by a person, or by a blind LLM comparison of two versions.

## Run

```sh
pip install -r scripts/requirements.txt
evals/run.sh iteration-1          # 6 agent sessions; costs model tokens
cat evals-workspace/iteration-1/benchmark.json
```

`evals-workspace/` is not committed. When a skill change is meant to improve results, run the previous version as the baseline (`old_skill`) and compare, as the Agent Skills guide describes. Grade a single report by hand with:

```sh
python3 evals/grade.py audit-signup-app path/to/report.md
```

## Results

No clean-context benchmark has been recorded yet; the first run is a maintainer step (it needs an authenticated agent and spends tokens). Record each run's `benchmark.json` summary in this section with the date, the skill version and the model, so changes can be compared over time.
