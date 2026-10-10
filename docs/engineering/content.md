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
  rules (legal, data loss, trust) override it, and every criterion must be able
  to reach the level they require, through its range or its `severity_note`
  (`scripts/test_calibration.py`): WCAG-sourced criteria reach S3, lost user
  work reaches S4, legal and consent failures reach S3. S4 stays rare as a
  default.

## 4. Evidence and sources

- Every number (threshold, statistic, research result) cites its source with
  `[src:<id>]` in text and `sources:` on the criterion; the source is recorded in
  `criteria/sources.yaml` with its status (primary, secondary, unconfirmed,
  unchecked) and how it was verified. An estimate or rule of thumb says so.
- Prefer primary sources: when a site is unreachable, read the official source
  repository (e.g. w3c/wcag) and record the commit.
- Never state the numbers of an **unconfirmed** source as fact; keep only the
  direction of the finding, or drop it.
- Examples from real products describe **publicly observable** behaviour, carry
  the date they were observed, and never quote ratings, revenue or adoption
  figures that cannot be verified.

## 5. Proven patterns

- `criteria/patterns.yaml` records patterns from public design systems, read from
  their repositories at a recorded commit; `references/patterns.md` is generated.
- Summarize each rule in our own words (no copied text), link the source file at
  that commit, date it, and list the criteria it satisfies. The generator rejects
  unknown criteria.
- Prefer design systems that publish their guidance openly over claims about how
  an app looks: they are verifiable and versioned.

## 6. Writing style

- Plain words, short sentences, active voice, imperative mood for procedures.
- Name things the way practitioners do, and explain a law or acronym in half a
  sentence the first time it appears in a file.
- Tables for criteria and comparisons; numbered lists for procedures; code
  blocks for search patterns and templates.
- Neutral, precise tone. No marketing language and no filler.

## 7. Gotchas

- Every area file has a `## Gotchas` section before `## Output`: 3–5 concrete
  corrections about framework, standard or tool behaviour that defies a
  reasonable assumption. Generic advice ("be careful with…") does not belong
  there.
- When an agent makes a mistake in a run (false positive, missed issue, wasted
  step), add a one-line correction to the relevant gotchas list. That is the
  fastest way to improve the skill.

## 8. Stack packs

- A pack (`criteria/stacks/<id>.yaml`, schema `criteria/stack.schema.json`) adds what a framework, component library
  or test tool changes about findings. It never restates a criterion; it cites criteria by ID.
- Read the stack's own repository at a recorded commit (clone it; docs sites are often unreachable or newer than the
  release the project uses). Record the version and commit in `verified`, and summarize in your own words.
- Every gotcha names its source file in that repository. A gotcha is behaviour that defies a reasonable assumption:
  a default that makes a generic finding a false positive, or a convention that silently leaves a gap.
- Probes follow the native-probe rules: portable regular expressions, an example, a counter-example for review
  and smell probes.
- Re-verify a pack when `scripts/check_freshness.py` flags it (monthly, older than about six months) or when the
  stack ships a major version.
