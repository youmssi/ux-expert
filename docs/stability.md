# Stability policy

From 1.0.0, `ux-expert` follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
This page says what is public, so you know what an upgrade can change. Anything not listed is
internal and can change in any release.

## Public and stable within a major version

| What | Promise | Enforced by |
|---|---|---|
| **Criterion IDs** (`FORM-09`) | An ID never disappears, never changes area and never changes meaning. A criterion that no longer applies is retired (`status: retired`), and its ID is never reused. Wording, fail signals and default severities can be clarified in a minor release. | `criteria/ids.lock.json`, checked by `scripts/generate.py --check` |
| **Pattern and probe IDs** (`govuk-validation`, `ios-fixed-font-size`) | Never removed or reused. Their rules and regular expressions can be improved in a minor release. | `criteria/ids.lock.json` |
| **Stack pack IDs** (`nextjs`, `shadcn-ui`) | A pack keeps its ID and its page `references/stacks/<id>.md`. Its gotchas follow the stack's releases and change in minor releases. | `criteria/ids.lock.json` |
| **Skill layout** | `SKILL.md`, `references/areas/<area>.md`, `references/*.md` named in `SKILL.md`, `criteria/catalogue.json`, `scripts/*` named in `SKILL.md` keep their paths. Areas and references can be added. | `skills-ref validate`, link checks in `scripts/validate.py` |
| **`criteria/catalogue.json`** | Keys present in `schema_version` 1 keep their name and type. New keys can be added; read the file tolerantly. | `schema_version` field; `scripts/test_generate.py` |
| **MCP server** | Tool names, their input fields and which are required; prompt names and arguments; the `skill://ux-expert/` resource URIs. New tools, prompts and optional inputs can be added. | `mcp/interface.json`, checked by `mcp/test/interface.test.ts` |
| **Severity and priority scales** | S0–S4, R1–R3, P0–P3 and the launch-gate verdicts keep their names and order. | `criteria/scoring.schema.json` |

## Not covered

- The text of procedures, gotchas and examples: it improves in every release.
- The number of criteria in a selection: new criteria and areas change counts in minor releases.
- Bundles for chat assistants: their content follows the skill; the file names per mode stay.
- Default severities: recalibrated when evidence says so, with a changelog entry.

## Versions

| Change | Version |
|---|---|
| New criteria, areas, patterns, probes, tools, prompts, optional inputs; clarified wording | minor |
| Fixes to content, scripts or the server that keep the public surface | patch |
| Removing or renaming anything in the table above; changing a criterion's meaning; a required input added to a tool | major, with a migration note in `CHANGELOG.md` |

Pin the version you rely on: the plugin marketplace entry, the npm package (`ux-expert-mcp@1`) or a
release tag (`v1.0.0`) of this repository.
