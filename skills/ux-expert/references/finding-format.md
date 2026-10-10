# Finding format (mandatory for every area)

Every issue reported by any area uses exactly this structure. Consistent findings can be merged, sorted and tracked by a machine or a person.

## Template

```markdown
### F-<NNN> · <CRITERION-ID> · <Short title stating the problem, not the fix>

- **Skill / criterion:** <area name> / <CRITERION-ID> (<criterion name>)
- **Location:** <file:line | route | screen | component | command | endpoint> (list all locations; for more than 5, give a count plus the first 5)
- **Evidence (<static | runtime | measured | inferred>):**
  <code excerpt, measured value, screenshot path, tool output, or reasoning chain>
- **Observed:** <what is there now, factually>
- **Expected:** <what should be there, and the standard/principle/research it comes from>
- **User impact:** <which persona, in which job, experiences what consequence>
- **Severity:** S<0-4> · **Reach:** R<1-3> · **Confidence:** <High | Medium | Low> · **Effort:** <XS | S | M | L | XL>
- **Priority:** P<0-3>  (computed from severity-and-scoring.md)
- **Recommendation:** <concrete change: what, where, to what value. Code-level when possible. Cite a proven pattern from `references/patterns.md` by ID when one fits>
- **Verification:** <how to prove it is fixed: test, measurement, check, or user test task>
- **Related:** <other finding IDs or criterion IDs>
```

## Evidence types

| Type | Meaning | Confidence ceiling |
|---|---|---|
| `measured` | Output of a tool or calculation on real values (axe, Lighthouse, a contrast ratio computed from actual token hex values, a step count from the route graph) | High |
| `runtime` | Observed in the running product (browser, device, CLI execution), ideally with a screenshot or transcript | High |
| `static` | Read in source code, config or assets without running it | High for logic and structure; **Medium** for visual or behavioral outcomes (CSS can be overridden, conditions can differ at runtime) |
| `inferred` | Expert judgement from principles, with no direct observation | **Low** to Medium; must state the reasoning |

## Writing rules

1. **Title = the problem.** "Delete account has no confirmation" ✅ — "Add confirmation dialog" ❌.
2. **One root cause per finding.** If the fix differs, they are different findings.
3. **Systemic issues** (same cause in many places) get one finding with `Location: 37 occurrences, e.g. …`, and a recommendation that fixes the cause (e.g. introduce a token), not each instance.
4. **No unexplained jargon.** If you use "Fitts's law", add a half-sentence explanation the first time.
5. **Quote code exactly**, with a file path and line number.
6. **Recommendations must be implementable.** Give target values (e.g. "raise `--text-muted` from `#9CA3AF` to `#6B7280`, which brings the contrast on white from 2.5:1 to 4.8:1").
7. **Positive findings** (strengths) use the same header with `✅` instead of an ID and no severity, so they can be protected from regressions.

## Coverage table (returned by every area)

```markdown
| Criterion | Name | Result | Evidence | Finding(s) |
|---|---|---|---|---|
| LAY-01 | Spacing scale | Fail | measured | F-004 |
| LAY-02 | Alignment grid | Pass | static | — |
| LAY-07 | Thumb zone placement | Not verified | — | needs device run |
| LAY-09 | Print layout | N/A | — | no print use case |
```

Result values: `Pass` · `Partial` · `Fail` · `N/A` (does not apply; give the reason) · `Not verified` (applies but could not be checked; say what is needed).
