# UX audit report template

Write the final report in this structure. Keep the executive part to one screen. Details go below it.

```markdown
# UX Audit: <Product / scope>  ·  <date>  ·  Mode: <mode>

## 1. Executive summary
- **Verdict:** Go | Conditional Go | No-Go (pre-launch mode, or whenever LAUNCH ran)
- **In one sentence:** <the single most important truth about this product's UX>
- **Counts:** P0: n · P1: n · P2: n · P3: n · Strengths: n
- **Top 5 issues** (one line each, linked to findings)
- **Top 5 quick wins** (high priority, XS/S effort)
- **Biggest risk not verified:** <what, and what is needed>

## 2. Product context (from `references/areas/context-discovery.md`)
- Personas, top jobs-to-be-done, critical flows, success metrics, key assumptions

## 3. Scorecard
| Area | Score (0–5) | Pass rate | P0 | P1 | P2 | P3 | Not verified |
|---|---|---|---|---|---|---|---|
| Information architecture | 3 | 78% | 0 | 2 | 3 | 1 | 1 |
| … |

## 4. Cross-cutting themes
For each theme: the root cause, which findings it explains, and the systemic fix.

## 5. Critical flow walkthroughs
For each critical flow: the step table (step · screen · user action · system response · issues), the step count, the decision count, the failure points, and an end-to-end verdict.

## 6. Findings by priority
### P0
### P1
### P2
### P3
(Each finding in the format from finding-format.md)

## 7. Strengths to protect
## 8. Recommended roadmap
- **Now (before launch):** P0s and quick wins
- **Next (≤ 30 days):** P1s, grouped by theme or team
- **Later:** P2/P3, and validation research
- **Measure:** which metrics will prove the fixes worked (from `references/areas/measurement-validation.md`)

## 9. Coverage and limitations
- Sub-skills run, run light, and N/A, with reasons
- Criteria coverage tables per area (or an appendix link)
- What was not verified, and what is needed (runtime access, devices, real users, analytics data)

## Appendix
- A. Inventory / surface map
- B. Full criteria coverage tables
- C. Tool outputs (axe, Lighthouse, contrast calculations)
- D. Screenshots index
```

## Style rules
- Lead with the verdict and the reasons for it. Don't make the reader scroll for the answer.
- Use the users' words and the product's names for things.
- Each recommendation must be a change someone can make on Monday.
- Don't pad. If an area is excellent, say so in one line.
