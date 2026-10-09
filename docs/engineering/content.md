# Content rules

Most of this repository is knowledge for agents, not code. These rules keep it
expert, accurate and cheap to load. They follow the Agent Skills specification
and its authoring guidance (agentskills.io, `docs/skill-creation/` in
`agentskills/agentskills`), plus what is specific to this package.

## 1. Add what the agent lacks, cut what it knows

- Every paragraph must change what an agent does. Ask: *would the agent get
  this wrong without this sentence?* If not, cut it.
- No textbook definitions ("WCAG is a set of guidelines…"). Thresholds,
  procedures, fail signals, gotchas and judgement calls are the value.
- Prefer one clear **default** with a short escape hatch over a menu of equal
  options.

## 2. Structure for progressive disclosure

- `SKILL.md` holds only what is needed on every run: when to use which mode,
  the procedure, the gotchas. Under 500 lines; every Markdown file stays under
  about 5,000 tokens (`validate.py` estimates 4 characters per token).
- Detail lives in `references/`, one focused file per concern. `SKILL.md` says
  **when** to read each file ("Read `references/areas/forms-input.md` when the
  scope includes a form"), never a bare "see references/".
- Paths are relative to the skill root. A reference never depends on a file
  outside its skill directory.
- Reference chains stay shallow: `SKILL.md` → reference. A reference may point
  to the shared references (`finding-format.md`, `severity-and-scoring.md`)
  that `SKILL.md` already told the agent to read; it does not start new chains.

## 3. Criteria

- Criteria live in `skills/ux-expert/criteria/<area>.yaml` (schema:
  `criteria/schema.json`); the tables in the area files are generated, never
  edited by hand.
- Each criterion has a permanent ID (`<PREFIX>-<NN>`), a name, a fail signal
  and a default severity, plus an optional check, severity note and related
  areas or criteria.
- Each area sets its `applicability` per product type and default `phases`;
  a criterion overrides `phases` or narrows `applies_to` only when it differs.
  `design` means "specify it in stories and designs"; `build` means "implement
  and test it in code". Every criterion is auditable.
- Cite criteria by ID anywhere (skill files, examples). The generator rejects
  IDs that do not exist or are retired. IDs are never renumbered or reused; a criterion
  that no longer applies is retired, not deleted.
- A criterion is **observable**: someone else checking the same product would
  reach the same result. "Feels modern" is not a criterion.
- Default severity follows `references/severity-and-scoring.md`. Escalation
  rules (legal, data loss, trust) override it.

## 4. Evidence and sources

- Every number (threshold, statistic, research result) cites its source: a
  standard (WCAG 2.2 SC 1.4.3), a vendor guideline (Apple HIG), or a study
  (author, year). An estimate or rule of thumb says so.
- Prefer primary sources. Secondary summaries are acceptable only until the
  citation-verification story (UXE-7) checks them.
- Examples from real products describe **publicly observable** behaviour, carry
  the date they were observed, and never quote ratings, revenue or adoption
  figures that cannot be verified.

## 5. Writing style

- Plain words, short sentences, active voice, imperative mood for procedures.
- Name things the way practitioners do, and explain a law or acronym in half a
  sentence the first time it appears in a file.
- Tables for criteria and comparisons; numbered lists for procedures; code
  blocks for search patterns and templates.
- Neutral, precise tone. No marketing language and no filler.

## 6. Gotchas

- Every area file has a `## Gotchas` section before `## Output`: 3–5 concrete
  corrections about framework, standard or tool behaviour that defies a
  reasonable assumption. Generic advice ("be careful with…") does not belong
  there.
- When an agent makes a mistake in a run (false positive, missed issue, wasted
  step), add a one-line correction to the relevant gotchas list. That is the
  fastest way to improve the skill.
