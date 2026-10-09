# Contributing to ux-expert

This guide is the workflow every change follows, from picking a story to
releasing it. The rules live in `AGENTS.md`, `docs/engineering/principles.md`
(code) and `docs/engineering/content.md` (skill content); read them before your
first change.

## 1. Branches

| Branch | Role | Who writes to it |
|---|---|---|
| `main` | Released versions, tagged `vX.Y.Z` | Release PRs only (`develop` → `main`) |
| `develop` | The next release, always green | Squash-merged story PRs only |
| `uxe-<n>-<slug>` | One story | Its author |

Nothing is committed directly to `main` or `develop`.

## 2. One story, one branch, merged before the next

1. Take the next story from `docs/backlog/README.md` and its number `UXE-<n>`.
   If the story is only a line in the roadmap, first write its story file from
   `docs/templates/story.md` (that is part of the story's PR).
2. Branch from an up-to-date `develop`:

   ```bash
   git fetch origin develop
   git checkout -b uxe-<n>-<slug> origin/develop
   ```

3. Build the story, its checks and its documentation on that branch.
4. Open a **draft** pull request against `develop` early.
5. **Merge the story into `develop` before starting the next one.** A story is
   finished only when its PR is squash-merged.

**Never stack a story on another unmerged story.** If a story depends on
unmerged work, finish and merge that work first.

## 3. What a story contains

Stories live in `docs/backlog/` and use `docs/templates/story.md`:

- **Why**: the user problem, in two or three sentences.
- **Decision(s)**: what was chosen and when, when the story needed a choice.
- **Behaviour**: a short table of what changes where.
- **Acceptance criteria**: testable bullets, including edge cases.
- **Out of scope**: what this story deliberately does not do.

A choice with lasting consequences (skill layout, criterion schema,
distribution channel, license, MCP interface) gets an ADR in `docs/adr/`
(template: `docs/templates/adr.md`).

## 4. Before opening (or marking ready) the pull request

Every check below passes locally; CI runs the same ones and blocks the merge.

```bash
python3 -m unittest discover -s scripts -p "test_*.py"
python3 scripts/validate.py
skills-ref validate skills/ux-expert
```

And:

- Every criterion you add has a unique, never-used ID and a cited source for
  any number it contains.
- Generated files are regenerated with their script, never edited by hand.
- Content that changes agent behaviour names how it was checked (eval run from
  UXE-10 onward; until then, a manual run on a sample product, summarized in
  the PR).
- `CHANGELOG.md` has an entry under `Unreleased` when users of the package will
  notice the change.
- Dead content left behind by the change is removed or retired.

## 5. Commits and pull requests

- **Commits:** Conventional Commits, `<type>(<scope>): <description>`, a body
  that explains *what changed and why*, and a `Refs: UXE-<n>` trailer.
  Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `build`.
  Common scopes: `skill`, `criteria`, `areas`, `scripts`, `mcp`, `ci`, `docs`.
- **PR title** = the squash commit title.
- **PR body** follows `.github/pull_request_template.md`.
- **No AI authorship trace** in commits, PRs, comments or file headers.
- Keep PRs reviewable in one sitting. When a story is too big, split it (schema
  → generator → content migration), each part mergeable alone.

## 6. Review and merge

1. CI is green on the latest commit.
2. Every review thread is answered: fixed (name the commit) or explained.
3. Mark the PR ready and **squash-merge** into `develop`; delete the branch.
4. Only then start the next story from the updated `develop`.

A failing check is fixed at its root cause. Never skip or disable a check to
get green; never push an empty commit to re-trigger CI.

## 7. Releasing

1. Open a release PR `develop` → `main` listing the stories it ships and any
   breaking changes with their migration notes.
2. Bump the version (skill metadata, plugin manifest, MCP package when it
   exists) and move `CHANGELOG.md` entries from `Unreleased` to the version.
3. When CI is green, merge with a **merge commit** and tag `vX.Y.Z` on `main`.
4. Publish channels in order: Git tag (Agent Skills + Claude plugin
   marketplace), then npm (MCP server), then bundles attached to the GitHub
   release. Confirm each install path works before announcing.

## 8. Definition of done

- [ ] Acceptance criteria met and checked
- [ ] Checks green locally and in CI
- [ ] Docs updated (story, ADR, README, CHANGELOG) when behaviour changed
- [ ] Squash-merged into `develop`, branch deleted
