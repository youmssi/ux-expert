### UXE-12 — Recommendations point to proven patterns from products people trust

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-11  ·  **Size:** M

#### Why

A finding says what is wrong; teams also want to know what good looks like in products that are known to work. Claims such as "app X does Y" go stale and cannot be checked, so they would weaken the package's evidence standard.

#### Decision

Source patterns from the **public design systems** of widely used products, which document their patterns openly and version them in public repositories: GOV.UK (government services), GitHub Primer (GitHub), Shopify Polaris (Shopify admin) and IBM Carbon (IBM products). Each pattern is read from the repository at a recorded commit, summarized in our own words, dated, and linked to the criteria it satisfies.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `criteria/patterns.yaml` and schema | — | 4 design systems (repository and commit) and 17 patterns (rule, source link at the commit, date, criteria) |
| `references/patterns.md` | — | Generated table; `SKILL.md` and the finding format tell agents to cite a pattern ID in recommendations |
| Generator | — | Rejects unknown criteria and design systems in patterns; adds patterns to `catalogue.json` |
| MCP server | 6 tools | + `find_patterns` (by criterion and/or words) |
| Bundles | — | Include `references/patterns.md` |

#### Acceptance criteria

- [ ] Every pattern links to a file that exists in its repository at the recorded commit
- [ ] Every pattern lists only active criteria (enforced by the generator, tested)
- [ ] Rules are summaries, not copied text
- [ ] `find_patterns` returns `govuk-validation` for FORM-09 and matches words (tested)

#### Out of scope

- Screenshots or claims about specific app screens.
- More design systems (Atlassian, Material, Apple HIG): add with the same rules.
