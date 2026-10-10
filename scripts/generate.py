"""Build everything derived from the criteria catalogue.

The YAML files in ``skills/<skill>/criteria/`` are the source of truth. From
them this script writes:

- the criteria table in each area file, between
  ``<!-- BEGIN GENERATED criteria (<area>) -->`` and ``<!-- END GENERATED criteria -->``;
- the area applicability matrix in ``SKILL.md``, between
  ``<!-- BEGIN GENERATED applicability -->`` and ``<!-- END GENERATED applicability -->``;
- ``criteria/catalogue.json``: every active criterion with its effective phases,
  product types and sources, for tools that should not parse YAML;
- ``references/sources.md``: the bibliography, from ``criteria/sources.yaml``;
- the priority matrix and launch-gate tables in ``references/severity-and-scoring.md``,
  from ``criteria/scoring.yaml``;
- ``references/patterns.md``: proven patterns, from ``criteria/patterns.yaml``;
- ``references/native-probes.md``: code search probes for native mobile stacks,
  from ``criteria/probes.yaml`` (also in ``catalogue.json`` for ``scripts/probe.py``);
- ``references/stacks.md`` and ``references/stacks/<id>.md``: stack packs for
  frameworks, component libraries and test tools, from ``criteria/stacks/*.yaml``;
- ``criteria/ids.lock.json``: every published criterion, pattern and probe ID. It
  only grows: an ID in the lock that disappears from the YAML is an error, because
  published IDs are permanent (retire a criterion instead; see docs/stability.md).

Usage:
    python3 scripts/generate.py           # validate the catalogue, rewrite the outputs
    python3 scripts/generate.py --check   # validate, and fail if an output is out of date
"""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
CRITERIA_BLOCK = re.compile(r"<!-- BEGIN GENERATED criteria \((?P<area>[a-z0-9-]+)\) -->\n.*?<!-- END GENERATED criteria -->", re.DOTALL)
PRIORITY_BLOCK = re.compile(r"<!-- BEGIN GENERATED priority-matrix -->\n.*?<!-- END GENERATED priority-matrix -->", re.DOTALL)
GATE_BLOCK = re.compile(r"<!-- BEGIN GENERATED launch-gate -->\n.*?<!-- END GENERATED launch-gate -->", re.DOTALL)
MATRIX_BLOCK = re.compile(r"<!-- BEGIN GENERATED applicability -->\n.*?<!-- END GENERATED applicability -->", re.DOTALL)
PRODUCT_TYPES = {
    "web-app": "Web app",
    "marketing-site": "Marketing site",
    "mobile": "Mobile",
    "desktop": "Desktop",
    "cli": "CLI",
    "sdk-api": "SDK/API",
    "ai-feature": "AI feature",
}
DEPTH_LABELS = {"run": "Run", "light": "Light", "conditional": "Conditional", "n/a": "N/A"}
CITATION = re.compile(r"\b([A-Z][A-Z0-9]*)-(\d{2,})\b")
SOURCE_CITATION = re.compile(r"\[src:([a-z0-9]+(?:-[a-z0-9]+)*)\]")


SOURCES_FILE = "sources.yaml"
SCORING_FILE = "scoring.yaml"
PATTERNS_FILE = "patterns.yaml"
PROBES_FILE = "probes.yaml"
NOT_AREAS = {SOURCES_FILE, SCORING_FILE, PATTERNS_FILE, PROBES_FILE}
# Probe patterns also run in ripgrep, which has no lookaround or backreferences.
NOT_PORTABLE = re.compile(r"\(\?<?[=!]|\(\?<\w|\\[1-9]")
PROBE_KINDS = {
    "inventory": "locate and count",
    "review": "each hit needs a look, often fine",
    "smell": "usually a defect; confirm before reporting",
}
SOURCE_STATUS = {
    "primary": "checked against the source's own text",
    "secondary": "confirmed through reputable secondary sources",
    "unconfirmed": "could not be confirmed; its numbers are not stated as fact",
    "unchecked": "classic reference; no threshold depends on it",
}


def schema_errors(schema_path: Path, document, path: Path) -> list[str]:
    validator = Draft202012Validator(json.loads(schema_path.read_text(encoding="utf-8")))
    errors = sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path))
    return [f"{path}: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]


def load_sources(criteria_dir: Path) -> tuple[list[dict], list[str]]:
    path = criteria_dir / SOURCES_FILE
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    problems = schema_errors(criteria_dir / "sources.schema.json", document, path)
    if problems:
        return [], problems
    ids = [s["id"] for s in document["sources"]]
    problems += [f"{path}: duplicate source ID {i}" for i in sorted({i for i in ids if ids.count(i) > 1})]
    return document["sources"], problems


def load_scoring(criteria_dir: Path) -> tuple[dict, list[str]]:
    path = criteria_dir / SCORING_FILE
    scoring = yaml.safe_load(path.read_text(encoding="utf-8"))
    problems = schema_errors(criteria_dir / "scoring.schema.json", scoring, path)
    if not problems:
        defaults = [i for i, rule in enumerate(scoring["launch_gate"]) if not rule["when_any"]]
        if defaults != [len(scoring["launch_gate"]) - 1]:
            problems.append(f"{path}: launch_gate needs exactly one default rule (empty when_any), in last position")
    return scoring, problems


def load_patterns(criteria_dir: Path, documents: dict[str, dict]) -> tuple[dict, list[str]]:
    path = criteria_dir / PATTERNS_FILE
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    problems = schema_errors(criteria_dir / "patterns.schema.json", data, path)
    if problems:
        return data, problems
    systems = {s["id"] for s in data["design_systems"]}
    ids = {c["id"] for doc in documents.values() for c in active(doc)}
    seen: set[str] = set()
    for pattern in data["patterns"]:
        if pattern["id"] in seen:
            problems.append(f"{path}: duplicate pattern ID {pattern['id']}")
        seen.add(pattern["id"])
        if pattern["design_system"] not in systems:
            problems.append(f"{path}: {pattern['id']} names unknown design system '{pattern['design_system']}'")
        problems += [f"{path}: {pattern['id']} cites {c}, which is not an active criterion" for c in pattern["criteria"] if c not in ids]
    return data, problems


def load_probes(criteria_dir: Path, documents: dict[str, dict], sources: list[dict]) -> tuple[dict, list[str]]:
    path = criteria_dir / PROBES_FILE
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    problems = schema_errors(criteria_dir / "probes.schema.json", data, path)
    if problems:
        return data, problems
    platforms = {p["id"] for p in data["platforms"]}
    source_ids = {s["id"] for s in sources}
    ids = {c["id"] for doc in documents.values() for c in active(doc)}
    for platform in data["platforms"]:
        problems += [f"{path}: platform {platform['id']} cites unknown source '{s}'" for s in platform["sources"] if s not in source_ids]
    seen: set[str] = set()
    for probe in data["probes"]:
        where = f"{path}: {probe['id']}"
        if probe["id"] in seen:
            problems.append(f"{where}: duplicate probe ID")
        seen.add(probe["id"])
        if probe["platform"] not in platforms:
            problems.append(f"{where}: unknown platform '{probe['platform']}'")
        problems += [f"{where}: cites {c}, which is not an active criterion" for c in probe["criteria"] if c not in ids]
        problems += pattern_problems(where, probe)
    return data, problems


def pattern_problems(where: str, probe: dict) -> list[str]:
    """A probe pattern must run in Python and ripgrep, match its example and miss its counter-example."""
    if NOT_PORTABLE.search(probe["pattern"]):
        return [f"{where}: pattern uses lookaround or a backreference, which ripgrep does not support"]
    try:
        pattern = re.compile(probe["pattern"])
    except re.error as error:
        return [f"{where}: pattern does not compile: {error}"]
    problems = []
    if not pattern.search(probe["example"]):
        problems.append(f"{where}: pattern does not match its example")
    if "counter_example" in probe and pattern.search(probe["counter_example"]):
        problems.append(f"{where}: pattern matches its counter-example")
    return problems


def load_stacks(criteria_dir: Path, documents: dict[str, dict], probe_ids: set[str]) -> tuple[list[dict], list[str]]:
    """Load criteria/stacks/*.yaml; probe IDs must be unique across native probes and every stack."""
    ids = {c["id"] for doc in documents.values() for c in active(doc)}
    stacks, problems, seen = [], [], set(probe_ids)
    for path in sorted((criteria_dir / "stacks").glob("*.yaml")):
        stack = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = schema_errors(criteria_dir / "stack.schema.json", stack, path)
        problems += errors
        if errors:
            continue
        if stack["id"] != path.stem:
            problems.append(f"{path}: id '{stack['id']}' must match the file name '{path.stem}'")
        cited = [c for g in stack["gotchas"] for c in g["criteria"]]
        cited += [c for p in stack.get("probes", []) for c in p["criteria"]]
        cited += [c for r in stack.get("recipes", []) for c in r["criteria"]]
        problems += [f"{path}: cites {c}, which is not an active criterion" for c in sorted(set(cited)) if c not in ids]
        for probe in stack.get("probes", []):
            where = f"{path}: {probe['id']}"
            if probe["id"] in seen:
                problems.append(f"{where}: duplicate probe ID")
            seen.add(probe["id"])
            problems += pattern_problems(where, probe)
        stacks.append(stack)
    return stacks, problems


def load_catalogue(skill_dir: Path) -> tuple[dict[str, dict], list[dict], list[str]]:
    """Return {area: document}, the sources, and the list of problems found in the catalogue."""
    criteria_dir = skill_dir / "criteria"
    sources, problems = load_sources(criteria_dir)
    documents: dict[str, dict] = {}
    for path in sorted(criteria_dir.glob("*.yaml")):
        if path.name in NOT_AREAS:
            continue
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = schema_errors(criteria_dir / "schema.json", document, path)
        problems += errors
        if errors:
            continue
        if document["area"] != path.stem:
            problems.append(f"{path}: area '{document['area']}' must match the file name '{path.stem}'")
        documents[path.stem] = document
    problems += check_consistency(criteria_dir, documents)
    source_ids = {s["id"] for s in sources}
    for area, document in documents.items():
        for criterion in document["criteria"]:
            for source in criterion.get("sources", []):
                if source not in source_ids:
                    problems.append(f"{criteria_dir / f'{area}.yaml'}: {criterion['id']} cites unknown source '{source}'")
    return documents, sources, problems


def area_product_types(document: dict) -> list[str]:
    return [t for t in PRODUCT_TYPES if document["applicability"][t] != "n/a"]


def check_consistency(criteria_dir: Path, documents: dict[str, dict]) -> list[str]:
    problems = []
    first_seen: dict[str, str] = {}
    prefixes = {doc["prefix"] for doc in documents.values()}
    for area, document in documents.items():
        path = criteria_dir / f"{area}.yaml"
        if "conditional" in document["applicability"].values() and "applicability_note" not in document:
            problems.append(f"{path}: a conditional applicability needs an applicability_note")
        allowed_types = set(area_product_types(document))
        for criterion in document["criteria"]:
            criterion_id = criterion["id"]
            if not criterion_id.startswith(document["prefix"] + "-"):
                problems.append(f"{path}: {criterion_id} does not use the area prefix {document['prefix']}")
            if criterion_id in first_seen:
                problems.append(f"{path}: duplicate criterion ID {criterion_id}, first defined in {first_seen[criterion_id]}.yaml")
            first_seen.setdefault(criterion_id, area)
            low, _, high = criterion["severity"].partition("–")
            if high and low > high:
                problems.append(f"{path}: {criterion_id} severity range {criterion['severity']} is reversed")
            extra = set(criterion.get("applies_to", [])) - allowed_types
            if extra:
                problems.append(f"{path}: {criterion_id} applies_to {sorted(extra)}, where the area is n/a")
    for area, document in documents.items():
        for criterion in document["criteria"]:
            for target in criterion.get("related", []):
                if target not in prefixes and target not in first_seen:
                    problems.append(f"{criteria_dir / f'{area}.yaml'}: {criterion['id']} relates to unknown '{target}'")
    return problems


def check_citations(skill_dir: Path, documents: dict[str, dict], sources: list[dict], extra_files: list[Path]) -> list[str]:
    """Every criterion ID cited with a known prefix must be active; every [src:<id>] must exist."""
    prefixes = {doc["prefix"] for doc in documents.values()}
    ids = {c["id"] for doc in documents.values() for c in active(doc)}
    source_ids = {s["id"] for s in sources}
    problems = []
    for path in sorted(skill_dir.rglob("*.md")) + extra_files:
        text = path.read_text(encoding="utf-8")
        for prefix, number in CITATION.findall(text):
            cited = f"{prefix}-{number}"
            if prefix in prefixes and cited not in ids:
                problems.append(f"{path}: cites {cited}, which is not an active criterion")
        for source in SOURCE_CITATION.findall(text):
            if source not in source_ids:
                problems.append(f"{path}: cites [src:{source}], which is not in criteria/sources.yaml")
    return problems


def active(document: dict) -> list[dict]:
    return [c for c in document["criteria"] if c.get("status", "active") == "active"]


def render_table(document: dict) -> str:
    criteria = active(document)
    with_check = any("check" in c for c in criteria)
    header = ["ID", "Criterion"] + (["Check"] if with_check else []) + ["Fail signal", "Default severity"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for criterion in criteria:
        details = [criterion[k] for k in ("severity_note",) if k in criterion]
        if criterion.get("related"):
            details.append("→ " + ", ".join(criterion["related"]))
        severity = criterion["severity"] + (f" ({'; '.join(details)})" if details else "")
        cells = [criterion["id"], criterion["name"]] + ([criterion.get("check", "—")] if with_check else [])
        cells += [criterion["fail_signal"], severity]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_criteria_block(document: dict) -> str:
    return (
        f"<!-- BEGIN GENERATED criteria ({document['area']}) -->\n"
        f"<!-- Source: criteria/{document['area']}.yaml. Edit the YAML, then run scripts/generate.py. -->\n"
        f"{render_table(document)}\n"
        "<!-- END GENERATED criteria -->"
    )


def render_matrix_block(documents: dict[str, dict]) -> str:
    lines = [
        "<!-- BEGIN GENERATED applicability -->",
        "<!-- Source: the applicability field of criteria/*.yaml. Run scripts/generate.py after editing. -->",
        "| Area (`references/areas/…`) | " + " | ".join(PRODUCT_TYPES.values()) + " |",
        "|---|" + "---|" * len(PRODUCT_TYPES),
    ]
    notes = []
    for area, document in documents.items():
        cells = [DEPTH_LABELS[document["applicability"][t]] for t in PRODUCT_TYPES]
        lines.append(f"| `{area}.md` ({document['prefix']}) | " + " | ".join(cells) + " |")
        if "applicability_note" in document:
            notes.append(f"- **{document['prefix']}**: {document['applicability_note']}.")
    return "\n".join(lines + [""] + notes + ["<!-- END GENERATED applicability -->"])


def render_sources(sources: list[dict]) -> str:
    lines = [
        "# Sources",
        "",
        "<!-- Generated from criteria/sources.yaml by scripts/generate.py. Edit the YAML, then run the script. -->",
        "",
        "The evidence behind the numbers and claims in this skill. Cite a source by its ID.",
        "Status: " + "; ".join(f"**{k}**: {v}" for k, v in SOURCE_STATUS.items()) + ".",
        "",
        "| ID | Source | Status | Verified | Backs |",
        "|---|---|---|---|---|",
    ]
    for s in sources:
        name = f"[{s['title']}]({s['url']})" if "url" in s else s["title"]
        by = ", ".join(str(s[k]) for k in ("publisher", "year") if k in s)
        verified = s.get("verified_on", "—") + (f" ({s['verified_against']})" if "verified_against" in s else "")
        lines.append(f"| `{s['id']}` | {name}{f' — {by}' if by else ''} | {s['status']} | {verified} | {s['supports']} |")
    return "\n".join(lines) + "\n"


def render_priority_matrix(scoring: dict) -> str:
    reaches = ["R3", "R2", "R1"]
    lines = ["<!-- BEGIN GENERATED priority-matrix -->",
             "<!-- Source: criteria/scoring.yaml. Run scripts/generate.py after editing. -->",
             "|  | " + " | ".join(f"**{r}**" for r in reaches) + " |", "|---|---|---|---|"]
    for severity, row in scoring["priority_matrix"].items():
        lines.append(f"| **{severity}** | " + " | ".join(row[r] for r in reaches) + " |")
    return "\n".join(lines + ["<!-- END GENERATED priority-matrix -->"])


def render_launch_gate(scoring: dict) -> str:
    lines = ["<!-- BEGIN GENERATED launch-gate -->",
             "<!-- Source: criteria/scoring.yaml (checked in this order). Run scripts/generate.py after editing. -->",
             "| Verdict | Rule |", "|---|---|"]
    lines += [f"| **{rule['verdict']}** | {rule['rule']} |" for rule in scoring["launch_gate"]]
    return "\n".join(lines + ["<!-- END GENERATED launch-gate -->"])


def render_patterns(patterns: dict) -> str:
    systems = {s["id"]: s for s in patterns["design_systems"]}
    lines = [
        "# Proven patterns",
        "",
        "<!-- Generated from criteria/patterns.yaml by scripts/generate.py. Edit the YAML, then run the script. -->",
        "",
        "Patterns from public design systems of widely used products, read from their repositories at the commits",
        "below. Cite a pattern by its ID in a recommendation when it fits the finding; follow the source for detail.",
        "",
        "| Design system | Repository | Commit |",
        "|---|---|---|",
    ]
    lines += [f"| {s['name']} | {s['repository']} | `{s['commit'][:7]}` |" for s in patterns["design_systems"]]
    lines += ["", "| ID | Pattern | From | Rule | Criteria |", "|---|---|---|---|---|"]
    for p in patterns["patterns"]:
        lines.append(f"| `{p['id']}` | [{p['name']}]({p['source']}) | {systems[p['design_system']]['name']} | {p['rule']} | {', '.join(p['criteria'])} |")
    return "\n".join(lines) + "\n"


def render_probes(probes: dict) -> str:
    lines = [
        "# Native mobile probes",
        "",
        "<!-- Generated from criteria/probes.yaml by scripts/generate.py. Edit the YAML, then run the script. -->",
        "",
        "Code search probes for iOS, Android, Flutter and React Native, used in recon (`references/codebase-recon.md`)",
        "and by the areas that cite them. Run them all at once with `python3 scripts/probe.py <project root>`, or",
        "search one pattern with Grep or `rg`. A hit is a place to look, never a finding by itself: open the code and",
        "check it against the criterion before reporting. In the tables, `\\|` is an escaped `|`; `probe.py` and",
        "`criteria/catalogue.json` carry the raw patterns.",
        "",
        "Kinds: " + "; ".join(f"**{k}**: {v}" for k, v in PROBE_KINDS.items()) + ".",
    ]
    for platform in probes["platforms"]:
        lines += ["", f"## {platform['name']}", "",
                  f"Files: {', '.join(f'`{e}`' for e in platform['extensions'])} · detected by {platform['detect']} · "
                  f"sources: {', '.join(f'[src:{s}]' for s in platform['sources'])}", ""]
        lines += [f"- {note}" for note in platform["notes"]]
        lines += ["", "| Probe | Kind | Pattern | Look for | Criteria |", "|---|---|---|---|---|"]
        for p in probes["probes"]:
            if p["platform"] == platform["id"]:
                pattern = p["pattern"].replace("|", "\\|")
                lines.append(f"| `{p['id']}` | {p['kind']} | `{pattern}` | {p['look_for']} | {', '.join(p['criteria']) or '—'} |")
    return "\n".join(lines) + "\n"


LOCK_FILE = "ids.lock.json"
# Major version of the catalogue.json layout; bump only with a major release (docs/stability.md).
CATALOGUE_SCHEMA_VERSION = 1


def lock_problems_and_content(criteria_dir: Path, documents: dict[str, dict], patterns: dict, probes: dict, stacks: list[dict]) -> tuple[list[str], str]:
    """Return the problems with published IDs and the updated lock (the old lock plus new IDs)."""
    path = criteria_dir / LOCK_FILE
    old = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"criteria": {}, "patterns": [], "probes": []}
    criteria = {c["id"]: area for area, doc in documents.items() for c in doc["criteria"]}
    current = {"stacks": {s["id"] for s in stacks}, "patterns": {p["id"] for p in patterns["patterns"]}, "probes": {p["id"] for p in probes["probes"]} | {p["id"] for s in stacks for p in s.get("probes", [])}}
    problems = []
    for criterion_id, area in old["criteria"].items():
        if criterion_id not in criteria:
            problems.append(f"{path}: published criterion {criterion_id} was removed; set status: retired instead")
        elif criteria[criterion_id] != area:
            problems.append(f"{path}: published criterion {criterion_id} moved from {area} to {criteria[criterion_id]}")
    old.setdefault("stacks", [])
    for kind in ("stacks", "patterns", "probes"):
        problems += [f"{path}: published {kind[:-1]} {i} was removed; published IDs are permanent" for i in old[kind] if i not in current[kind]]
    lock = {
        "about": "Published IDs. Maintained by scripts/generate.py: it adds new IDs and rejects removed ones. Do not edit.",
        "criteria": dict(sorted((old["criteria"] | criteria).items())),
        "stacks": sorted(set(old["stacks"]) | current["stacks"]),
        "patterns": sorted(set(old["patterns"]) | current["patterns"]),
        "probes": sorted(set(old["probes"]) | current["probes"]),
    }
    return problems, json.dumps(lock, indent=1) + "\n"


STACK_KINDS = {"framework": "Frameworks", "component-library": "Component libraries", "testing": "Test tools"}


def source_link(stack: dict, source: str) -> str:
    """Link a gotcha's source file at the verified commit; 'owner/repo:path' points into a repository in 'also'."""
    repository, commit, path = stack["verified"]["repository"], stack["verified"]["commit"], source
    if ":" in source:
        name, path = source.split(":", 1)
        other = next(a for a in stack["verified"].get("also", []) if a["repository"].endswith("/" + name))
        repository, commit = other["repository"], other["commit"]
    return f"[{path}]({repository}/blob/{commit}/{path})"


def render_stack(stack: dict) -> str:
    v = stack["verified"]
    repos = [f"{v['repository']}@`{v['commit'][:7]}`"] + [f"{a['repository']}@`{a['commit'][:7]}`" for a in v.get("also", [])]
    detect = [f"dependency {', '.join(f'`{d}`' for d in stack['detect'].get('dependencies', []))}"] if "dependencies" in stack["detect"] else []
    detect += [f"file {', '.join(f'`{f}`' for f in stack['detect']['files'])}"] if "files" in stack["detect"] else []
    lines = [
        f"# {stack['name']}",
        "",
        f"<!-- Generated from criteria/stacks/{stack['id']}.yaml by scripts/generate.py. Edit the YAML, then run the script. -->",
        "",
        stack["summary"],
        "",
        f"Verified against {stack['name']} {v['version']} on {v['verified_on']}, reading {', '.join(repos)}. "
        f"Detected by {' or '.join(detect)}. If the project uses another major version, check the gotchas against its docs.",
        "",
        "## Where the evidence is",
        "",
        "| What | Where |",
        "|---|---|",
    ]
    lines += [f"| {e['what']} | {e['where']} |" for e in stack["evidence"]]
    lines += ["", "## Gotchas", ""]
    for g in stack["gotchas"]:
        criteria = f" ({', '.join(g['criteria'])})" if g["criteria"] else ""
        lines.append(f"- {g['text']}{criteria} Source: {source_link(stack, g['source'])}.")
    if stack.get("probes"):
        lines += ["", "## Probes", "",
                  f"Files: {', '.join(f'`{e}`' for e in stack['extensions'])}. Run with `python3 scripts/probe.py <project root>`; "
                  "a hit is a place to look, not a finding.", "",
                  "| Probe | Kind | Pattern | Look for | Criteria |", "|---|---|---|---|---|"]
        for p in stack["probes"]:
            pattern = p["pattern"].replace("|", "\\|")
            lines.append(f"| `{p['id']}` | {p['kind']} | `{pattern}` | {p['look_for']} | {', '.join(p['criteria']) or '—'} |")
    if stack.get("recipes"):
        lines += ["", "## Recipes"]
        for r in stack["recipes"]:
            # Criteria on their own line: headings feed tables of contents, where links would nest.
            lines += ["", f"### {r['title']}", "", f"Criteria: {', '.join(r['criteria'])}.", "", f"```{r['language']}", r["code"].rstrip("\n"), "```"]
    return "\n".join(lines) + "\n"


def render_stack_index(stacks: list[dict]) -> str:
    lines = [
        "# Stack packs",
        "",
        "<!-- Generated from criteria/stacks/*.yaml by scripts/generate.py. Edit the YAML, then run the script. -->",
        "",
        "What a framework, component library or test tool changes about UX findings: where the evidence is, defaults",
        "that turn generic findings into false positives, common ways teams break built-in behaviour, and probes.",
        "Read a pack only when recon detects its stack (`python3 scripts/probe.py <project root>` lists them).",
        "Each pack records the version and commit it was verified against.",
        "",
        "| Pack | Kind | Detected by | Verified against |",
        "|---|---|---|---|",
    ]
    for s in sorted(stacks, key=lambda s: (list(STACK_KINDS).index(s["kind"]), s["id"])):
        detect = ", ".join(f"`{d}`" for d in s["detect"].get("dependencies", []) + s["detect"].get("files", []))
        lines.append(f"| [{s['name']}](stacks/{s['id']}.md) | {STACK_KINDS[s['kind']]} | {detect} | {s['verified']['version']}, {s['verified']['verified_on']} |")
    return "\n".join(lines) + "\n"


def render_catalogue(documents: dict[str, dict], sources: list[dict], scoring: dict, patterns: dict, probes: dict, stacks: list[dict]) -> str:
    areas, criteria, retired = [], [], []
    for area, document in documents.items():
        entry = {"area": area, "prefix": document["prefix"], "file": f"references/areas/{area}.md",
                 "applicability": document["applicability"]}
        if "applicability_note" in document:
            entry["applicability_note"] = document["applicability_note"]
        areas.append(entry)
        for criterion in document["criteria"]:
            if criterion.get("status", "active") != "active":
                retired.append(criterion["id"])
                continue
            item = {"id": criterion["id"], "area": area}
            item |= {k: criterion[k] for k in ("name", "check", "fail_signal", "severity", "severity_note", "related", "sources") if k in criterion}
            item["phases"] = criterion.get("phases", document["phases"])
            item["applies_to"] = criterion.get("applies_to", area_product_types(document))
            criteria.append(item)
    catalogue = {
        "generated_by": "scripts/generate.py from criteria/*.yaml; do not edit",
        "schema_version": CATALOGUE_SCHEMA_VERSION,
        "product_types": list(PRODUCT_TYPES),
        "phases": ["design", "build"],
        "areas": areas,
        "criteria": criteria,
        "retired_ids": retired,
        "sources": sources,
        "scoring": scoring,
        "design_systems": patterns["design_systems"],
        "patterns": patterns["patterns"],
        "platforms": probes["platforms"],
        "probes": probes["probes"],
        "stacks": stacks,
    }
    return json.dumps(catalogue, ensure_ascii=False, indent=1) + "\n"


def replace_blocks(text: str, pattern: re.Pattern, block: str) -> str | None:
    """Replace the single generated block matching ``pattern``; None when it is missing or repeated."""
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        return None
    return text[: matches[0].start()] + block + text[matches[0].end():]


def planned_outputs(skill_dir: Path, documents: dict[str, dict], sources: list[dict], scoring: dict, patterns: dict, probes: dict, stacks: list[dict]) -> tuple[dict[Path, str], list[str]]:
    """Return {path: expected content} for every generated output, and the problems found."""
    outputs: dict[Path, str] = {}
    problems: list[str] = []
    areas_dir = skill_dir / "references" / "areas"
    for area, document in documents.items():
        path = areas_dir / f"{area}.md"
        if not path.exists():
            problems.append(f"{path}: missing area file for criteria/{area}.yaml")
            continue
        text = path.read_text(encoding="utf-8")
        found = [m["area"] for m in CRITERIA_BLOCK.finditer(text)]
        updated = replace_blocks(text, CRITERIA_BLOCK, render_criteria_block(document)) if found == [area] else None
        if updated is None:
            problems.append(f"{path}: expected exactly one generated criteria block for '{area}'")
        else:
            outputs[path] = updated
    for path in sorted(areas_dir.glob("*.md")):
        if path.stem not in documents:
            problems.append(f"{path}: no criteria/{path.stem}.yaml for this area")
    skill_md = skill_dir / "SKILL.md"
    updated = replace_blocks(skill_md.read_text(encoding="utf-8"), MATRIX_BLOCK, render_matrix_block(documents))
    if updated is None:
        problems.append(f"{skill_md}: expected exactly one generated applicability block")
    else:
        outputs[skill_md] = updated
    scoring_md = skill_dir / "references" / "severity-and-scoring.md"
    text = scoring_md.read_text(encoding="utf-8")
    for pattern, block in ((PRIORITY_BLOCK, render_priority_matrix(scoring)), (GATE_BLOCK, render_launch_gate(scoring))):
        text = replace_blocks(text, pattern, block) if text is not None else None
    if text is None:
        problems.append(f"{scoring_md}: expected exactly one generated priority-matrix block and one launch-gate block")
    else:
        outputs[scoring_md] = text
    outputs[skill_dir / "criteria" / "catalogue.json"] = render_catalogue(documents, sources, scoring, patterns, probes, stacks)
    outputs[skill_dir / "references" / "patterns.md"] = render_patterns(patterns)
    outputs[skill_dir / "references" / "native-probes.md"] = render_probes(probes)
    outputs[skill_dir / "references" / "sources.md"] = render_sources(sources)
    outputs[skill_dir / "references" / "stacks.md"] = render_stack_index(stacks)
    for stack in stacks:
        outputs[skill_dir / "references" / "stacks" / f"{stack['id']}.md"] = render_stack(stack)
    stacks_dir = skill_dir / "references" / "stacks"
    known = {f"{s['id']}.md" for s in stacks}
    problems += [f"{p}: no criteria/stacks/{p.stem}.yaml for this pack" for p in sorted(stacks_dir.glob("*.md")) if p.name not in known]
    lock_problems, lock = lock_problems_and_content(skill_dir / "criteria", documents, patterns, probes, stacks)
    problems += lock_problems
    outputs[skill_dir / "criteria" / LOCK_FILE] = lock
    return outputs, problems


def run(skill_dir: Path, check: bool, extra_files: list[Path] = ()) -> list[str]:
    documents, sources, problems = load_catalogue(skill_dir)
    scoring, scoring_problems = load_scoring(skill_dir / "criteria")
    problems += scoring_problems
    if problems:
        return problems
    patterns, problems = load_patterns(skill_dir / "criteria", documents)
    probes, probe_problems = load_probes(skill_dir / "criteria", documents, sources)
    problems += probe_problems
    if problems:
        return problems
    stacks, problems = load_stacks(skill_dir / "criteria", documents, {p["id"] for p in probes["probes"]})
    if problems:
        return problems
    outputs, problems = planned_outputs(skill_dir, documents, sources, scoring, patterns, probes, stacks)
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            problems.append(f"{path}: out of date with criteria/*.yaml; run scripts/generate.py")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    # After writing, so citations are checked against the regenerated tables.
    return problems + check_citations(skill_dir, documents, sources, list(extra_files))


def main() -> int:
    check = "--check" in sys.argv[1:]
    problems = []
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        if (skill_md.parent / "criteria").is_dir():
            problems += run(skill_md.parent, check, sorted((ROOT / "docs" / "examples").glob("*.md")))
    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print(f"{len(problems)} problem(s) found")
        return 1
    print("ok: criteria catalogue is valid and generated outputs are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
