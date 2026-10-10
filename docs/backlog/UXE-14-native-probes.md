### UXE-14 — Audits of native mobile apps find evidence in SwiftUI, Compose, Flutter and React Native code

**Type:** feature  ·  **Repos:** ux-expert  ·  **Dependencies:** UXE-13  ·  **Size:** M

#### Why

Recon probes were written for the web and React. On a native or cross-platform app, an agent fell back on
guesses: it flagged SwiftUI string literals as unlocalized (they are localized), missed `TextScaler.noScaling`
switching off text scaling app-wide, and had no way to find custom tap targets without roles.

#### Decision

Probes are data (`criteria/probes.yaml`, same approach as ADR-004): platform, kind (inventory, review, smell),
pattern, what to look for, criteria, and an example and counter-example the generator checks. Patterns must
run in both Python `re` and ripgrep, so agents can use them with Grep, `rg` or the bundled
`scripts/probe.py` (standard library, reads `catalogue.json`). Each platform has notes on what is *not* a
defect there. API behaviour is checked against each platform's own source or documentation, recorded as
sources.

#### Behaviour

| Where | Before | After |
|---|---|---|
| `references/native-probes.md` | — | 41 probes over iOS, Android, Flutter and React Native, with platform notes and sources |
| `scripts/probe.py` | — | Detects platforms, runs the probes, prints hits per probe with file and line |
| `references/codebase-recon.md`, `areas/accessibility.md`, `SKILL.md` | Two lines of React Native and Flutter route patterns | Point to the probes and the script |
| Audit and full bundles | — | Include the probes |

#### Acceptance criteria

- [ ] Every probe matches its example and does not match its counter-example (checked by `generate.py --check`)
- [ ] A pattern with lookaround or a backreference is rejected
- [ ] `probe.py` detects each platform, finds seeded smells with file and line, skips dependency folders (tested)
- [ ] Every API claim in the platform notes cites a source with status `primary`

#### Out of scope

- Runtime checks on devices or simulators (Accessibility Inspector, Accessibility Scanner).
- Desktop native stacks (AppKit, WinUI).
