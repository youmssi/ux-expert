### UXE-17 — Visitors understand ux-expert and install it from the README

**Type:** chore  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-3  ·  **Size:** S

#### Why

The README is the package's landing page on GitHub. It reads like an internal
note: no status badges, the value buried below install details, nothing on how
the package works or how to get involved. Visitors decide in seconds whether a
project is serious and worth installing.

#### Decision

Follow the structure of established open-source READMEs (reference: Plunk):
centered title, tagline and badges; a short introduction with positioning;
features as bold labels; install; community and contributing; license. Badges
show only facts that are true today: CI status on `develop`, the two licenses,
and Agent Skills compatibility. Release and stars badges come with the first
release.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `README.md` | Plain title, mixed install and roadmap notes | Centered header with badges; Introduction, Features, How it works, Install, Usage, Roadmap, Contributing (with contributors image), License |

#### Acceptance criteria

- [ ] Every badge renders and shows a true fact (no "no releases found", no unknown license)
- [ ] The first screen says what the package is, who it is for and why it is different
- [ ] Install instructions for each channel are marked with the version that makes them work
- [ ] Every relative link in the README resolves
- [ ] Wording follows `docs/engineering/content.md` §5 (plain words, no marketing filler)

#### Out of scope

- A social preview image (needs a design asset; follow-up when a docs site
  exists, UXE-16).
