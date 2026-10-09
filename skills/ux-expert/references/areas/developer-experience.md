# Developer Experience (DX)

## Senior mindset

For a developer product, **the API is the UI, the README is the landing page, and the error message is the support team**. A senior DX reviewer applies the same UX principles (goal before screen, minimal steps, clear feedback, consistency, recovery) to code-level interfaces.

Their central metric is **time to first success** (often "time to Hello World", TTHW): from "I found this" to "it worked in my code". Stripe and Twilio became category leaders partly because that time was minutes: copy-paste-able snippets with real keys, consistent APIs, and error messages that tell you how to fix the problem.

They also know developers **read code before docs** and **docs before support**, and that they **judge quality by the first error message they hit**.

## Scope

- **In:** discovery → install → first call; README and quick start; API surface design (naming, consistency, defaults, progressive complexity, the pit of success); type definitions and IDE ergonomics (autocomplete, docstrings); error messages, error types and codes; validation of inputs and configs; logging and debuggability; CLI ergonomics (help, flags, output formats, exit codes, color/TTY behavior, interactivity); configuration and data formats (e.g. JSON schemas); documentation (concepts, guides, API reference, examples, recipes, troubleshooting, changelog, migration guides); versioning and deprecation; cross-language/binding parity; platform support and packaging; performance expectations and limits; sandbox or playground; community and support paths.
- **Out:** end-user UI of tools built on top (other areas), internal code quality not visible to integrators.

## Procedure

### Step 1: Identify developer personas and jobs
From CTX: e.g. "backend developer embedding the engine in Node.js", "Python data engineer running batch evaluation", "mobile developer on iOS/Android", "platform engineer operating it in production". Jobs: install, evaluate the first thing, integrate with their data loading, handle errors, deploy, upgrade, debug a wrong result.

### Step 2: Time-to-first-success walkthrough
Literally follow the README/quick start for each primary language **as written** (runtime if possible, in a clean environment):

| Step | Instruction (verbatim) | Worked? | Time | Friction / ambiguity |
|---|---|---|---|---|

Check that:
- Install commands are correct and complete (package name, version, platform prerequisites, native binary availability for OS/architecture).
- The first example is **copy-paste runnable** (imports included, sample data provided or linked, no undefined variables, matching the current API version).
- The expected output is shown, so the developer knows it worked.
- Count the steps and concepts needed before the first success.

### Step 3: API surface review
Read the public exports (`index.ts`, `lib.rs` `pub` items, `__init__.py`, Go exported identifiers, Java/Kotlin/C# public classes):
- **Naming:** consistent verbs (`evaluate`/`evaluateAll` vs. mixing `run`/`exec`/`evaluate`), idiomatic per language (camelCase in JS/Java, snake_case in Python/Rust, PascalCase exports in Go/C#), no abbreviations that need a glossary.
- **Consistency across bindings:** the same concepts, option names, defaults and error shapes in every language (accounting for idioms). A parity table is the key artifact.
- **Progressive complexity:** the simple case is one line with good defaults; advanced options are available without changing the simple path.
- **Pit of success:** the easiest way to use it is the correct and safe way (e.g. compile/load once and reuse instead of re-parsing per call; async by default where I/O happens; resource cleanup is automatic or obvious).
- **Types:** complete TypeScript declarations / type hints / generics; no `any` in public signatures; docstrings visible in IDE hovers; examples in docstrings.
- **Inputs:** accept common forms (string or object, path or buffer); validate early with precise errors.
- **Breaking-change hygiene:** semver, deprecation warnings before removal, a migration guide.

### Step 4: Error and diagnostic UX (critical)
Trigger, or read in code, the common failures: wrong input shape, missing file, invalid config/model JSON, expression syntax errors, type mismatches, timeouts, native library load failures, version mismatches.

Each error should have:
- **What failed**, in domain terms (not "unwrap on None" or "panicked at…"),
- **Where:** file/node/field/path/line:column (e.g. `nodes[3].expression at col 14`),
- **Why**, and the expected vs. actual value,
- **How to fix** (a suggestion, a "did you mean…?", a doc link),
- a **stable error code/type** for programmatic handling,
- **consistent structure across bindings** (same codes, same fields).

Also check: no process crashes on bad input (errors returned, not panics or segfaults), stack traces available in debug mode but not dumped to end users, and logs/tracing hooks for production debugging (e.g. a trace mode that shows which rules or nodes evaluated and why).

### Step 5: CLI ergonomics (if a CLI exists)
Following conventions such as clig.dev:
- `--help` and `-h` on every command, with examples; `--version`.
- Sensible defaults; flags over positional arguments for clarity; long and short forms.
- Output: human-readable by default when on a TTY; `--json`/machine output for scripts; no color when not a TTY or when `NO_COLOR` is set.
- Exit codes: 0 for success, non-zero on failure, documented.
- Progress for long operations; quiet (`-q`) and verbose (`-v`) modes.
- Confirmation for destructive operations, with `--yes`/`--force` for automation.
- Typos: "did you mean…" suggestions for subcommands.
- Errors to stderr, data to stdout.

### Step 6: Documentation architecture
Check the presence and quality of the four types (the Diátaxis framework):
1. **Tutorials** (learning-oriented: quick start, first project).
2. **How-to guides** (task-oriented: "load decisions from S3", "handle errors", "deploy to Lambda").
3. **Reference** (complete API, config schema, expression language, error codes).
4. **Explanation** (concepts: the decision model, the evaluation semantics, performance characteristics).

Plus: a per-language README with the same structure, a changelog, a migration guide per major version, troubleshooting/FAQ (native binary issues, platform support), runnable examples in the repo kept in CI (examples that rot are worse than none), search on the docs site, and a version selector.

### Step 7: Packaging, platforms and trust
- A platform/architecture support matrix (OS, CPU architecture, runtime versions) stated clearly; prebuilt binaries for common targets; a clear message when unsupported.
- Package metadata: description, homepage, repository, license, keywords; README renders on the registry page.
- Release notes; signed releases or provenance where expected; security policy (`SECURITY.md`).
- Benchmarks and performance claims reproducible.
- Support channels: issues, discussions or Discord; contribution guide.

## Criteria

<!-- BEGIN GENERATED criteria (developer-experience) -->
<!-- Source: criteria/developer-experience.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| DX-01 | Fast time to first success | > ~5 minutes or > ~5 steps to the first working result; extra concepts required upfront | S2–S3 |
| DX-02 | Quick start runnable as written | Missing imports or data; outdated API; failing commands | S3 |
| DX-03 | Expected output shown | Developer can't tell whether it worked | S1–S2 |
| DX-04 | Install clarity and platform support | Unclear prerequisites; missing binaries; vague unsupported-platform errors | S2–S3 |
| DX-05 | Consistent, idiomatic naming | Mixed verbs; non-idiomatic casing; cryptic abbreviations | S2 |
| DX-06 | Cross-language parity | Different option names, defaults, features or error shapes per binding without reason | S2–S3 |
| DX-07 | Progressive complexity and good defaults | The simple case requires advanced configuration | S2 |
| DX-08 | Pit of success | The easy way is slow, unsafe or incorrect (e.g. re-parsing per call) | S2 |
| DX-09 | Complete types and IDE docs | `any` in public types; no docstrings | S2 |
| DX-10 | Actionable error messages | Errors lack what/where/why/fix | S3 |
| DX-11 | Stable error codes/types | Only string messages; inconsistent structures | S2 |
| DX-12 | No crashes on bad input | Panics, segfaults or process exit on invalid input | S4 |
| DX-13 | Debuggability / tracing | No way to see why a result was produced | S2–S3 |
| DX-14 | CLI conventions | No help, wrong exit codes, no machine output, colors in pipes | S2 |
| DX-15 | Docs cover all four types | Missing how-tos, reference or concepts | S2 |
| DX-16 | Examples tested in CI | Examples broken or diverging from the API | S2 |
| DX-17 | Versioning and migrations | Breaking changes without semver, deprecation or a guide | S3 |
| DX-18 | Changelog and release notes | Missing or uninformative | S1–S2 |
| DX-19 | Package metadata and registry pages | Missing description, links or README on registries | S1 |
| DX-20 | Performance and limits documented | Unknown limits; unclear performance characteristics | S1–S2 |
| DX-21 | Playground / sandbox | No way to try without installing (when it's a natural fit) | S1–S2 |
| DX-22 | Support and contribution paths | No issue templates, security policy or contribution guide | S1 |
<!-- END GENERATED criteria -->

## Code probes

- Public API: `export (function|class|const)` in entry files; `pub fn|pub struct|pub enum` in `lib.rs`; `__all__`; exported Go identifiers.
- Panics on input paths: `unwrap\(\)|expect\(|panic!\(` in code reachable from public APIs; `process.exit` in libraries.
- Error types: `enum \w*Error`, `class \w+Error extends`, `thiserror`, error code constants.
- `any` in public types: `: any\b` in `*.d.ts`.
- CLI: `clap`, `#[command(`, `commander`, `yargs`, `click`, `--json`, `NO_COLOR`, `isatty`, `process.exitCode`.
- Docs: `README*`, `docs/`, `examples/` (and whether CI runs them: check workflow files for `examples`).
- Release: `CHANGELOG`, `release-please`, `changesets`, `SECURITY.md`, `CONTRIBUTING.md`.

## Output

- A TTFS walkthrough table per primary language.
- A cross-binding parity table (concept · Node · Python · Go · Java · … · consistent?).
- An error message catalog review (scenario · current message · rating · rewrite).
- A docs coverage matrix (Diátaxis types × topics).
- Findings in the standard format; the coverage table (DX-01 … DX-22).

## Done when

The quick start was executed (or carefully traced) for each primary language, the parity table is complete, the top error scenarios are evaluated with rewrites proposed, and docs coverage is mapped.
