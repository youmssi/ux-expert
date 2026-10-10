# Use ux-expert in your project

How to wire ux-expert into a product team's workflow so it is used at the moments that matter: before stories are written, on every UI change, and before each release.

## 1. Install it where the whole team gets it

Commit the skill into the repository, so every developer and every agent working in the repo uses the same version:

```sh
mkdir -p .claude/skills
git clone --depth 1 --branch v1.1.0 https://github.com/youmssi/ux-expert /tmp/ux-expert
cp -r /tmp/ux-expert/skills/ux-expert .claude/skills/
git add .claude/skills/ux-expert && git commit -m "chore: add ux-expert skill v1.1.0"
```

Use the folder your agents read (`.claude/skills/` for Claude Code; see [install.md](install.md) for other clients). To update, repeat with the new tag and review the diff and the [CHANGELOG](../CHANGELOG.md): criterion IDs never change meaning, so stories and reports keep working.

**Or share the MCP server** instead, for clients that use MCP (Cursor, VS Code, Codex, Gemini CLI, Claude Code). Commit a project config such as `.mcp.json`, pinned to the major version:

```json
{
  "mcpServers": {
    "ux-expert": { "command": "npx", "args": ["-y", "ux-expert-mcp@1"] }
  }
}
```

## 2. Tell your agents when to use it

Add this section to your `AGENTS.md` (or `CLAUDE.md`):

```markdown
## UX (ux-expert skill)

- **Before writing stories** for a feature: use the ux-expert skill in Design mode on the
  brief or draft stories. Paste its "UX acceptance criteria" block into each story and
  turn its [INTERACTIVE STEP]s into product-owner decisions.
- **Every pull request that changes UI**: run a ux-expert change review on the diff.
  P0 findings block the merge; P1 findings are fixed in the PR or get a follow-up story.
- **Before each release**: run the ux-expert pre-launch gate. Release only on Go, or on
  Conditional Go with every condition owned and dated.
- **Large UX debt**: run a full audit, then Refactor mode, and add the planned stories to
  the backlog in their order.
- Cite criterion IDs (e.g. FORM-09) in stories, PRs and reports.
```

## 3. Add UX to your story template and Definition of Done

In your story template, add a section the design mode fills in:

```markdown
#### UX acceptance criteria
- [ ] <behaviour> [CRITERION-IDs]
```

In your Definition of Done, add the product-level UX checklist that design mode produces once per product (section "UX Definition of Done"), for example:

```markdown
- [ ] UX acceptance criteria met; screenshots at phone and desktop width attached
- [ ] Keyboard-only and screen-reader pass on changed screens [A11Y-02, A11Y-10]
- [ ] Empty, loading and error states implemented [STATE-02, STATE-04, STATE-07]
```

## 4. The workflow at a glance

| Moment | Mode | Prompt to your agent | Output |
|---|---|---|---|
| Planning a feature | Design | "Use ux-expert to write the UX acceptance criteria for these stories: …" | Criteria per story, open decisions, UX Definition of Done |
| Reviewing a PR | Change review | "Use ux-expert to review the UX of this diff." | Findings on the changed surface, scored P0–P3 |
| Before a release | Pre-launch gate | "Use ux-expert: are we ready to launch?" | Go / Conditional Go / No-Go with conditions |
| Paying down UX debt | Full audit, then Refactor | "Audit the app with ux-expert", then "Plan how to fix these findings safely." | Report, then a sequenced plan of stories |
| One area | Area deep-dive | "Use ux-expert to check our forms." | Findings for that area |

## 5. Let it measure, not guess

Audits are stronger when the agent can run the product and knows your stack:

```sh
npm i -D playwright @axe-core/playwright @playwright/test   # runtime checks and regression guards
npx playwright install chromium
```

- With the app running, the agent uses `scripts/ux_check.mjs` for screenshots, axe, target size, focus and reflow at 320 px, and `scripts/contrast.py` for exact contrast ratios.
- `scripts/probe.py` detects your stack. On Next.js, shadcn/ui, Radix or Playwright projects it tells the agent which [stack pack](../skills/ux-expert/references/stacks.md) to read, so it does not report what the framework already handles; on SwiftUI, Compose, Flutter or React Native it runs the native probes.
- Refactor-mode guards start from the Playwright recipes in the stack pack, which compile against the pinned Playwright version.

## 6. Keep it honest

- Findings are only as good as the evidence: let the agent run the app (screenshots, axe, keyboard) whenever it can, and treat static-only visual findings as Medium confidence.
- Validate the riskiest findings with users (`references/areas/measurement-validation.md` produces a usability test plan).
- Report a wrong or missing criterion upstream: <https://github.com/youmssi/ux-expert/issues>.
