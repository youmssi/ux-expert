"""Render the criteria catalogue into the area reference files.

The YAML files in ``skills/<skill>/criteria/`` are the source of truth. Each
area file in ``references/areas/`` holds a generated table between markers:

    <!-- BEGIN GENERATED criteria (<area>) -->
    <!-- END GENERATED criteria -->

Usage:
    python3 scripts/generate.py           # validate the catalogue, rewrite the tables
    python3 scripts/generate.py --check   # validate, and fail if a table is out of date
"""

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
BLOCK = re.compile(r"<!-- BEGIN GENERATED criteria \((?P<area>[a-z0-9-]+)\) -->\n.*?<!-- END GENERATED criteria -->", re.DOTALL)


def load_catalogue(skill_dir: Path) -> tuple[dict[str, dict], list[str]]:
    """Return {area: document} and the list of problems found in the catalogue."""
    criteria_dir = skill_dir / "criteria"
    validator = Draft202012Validator(json.loads((criteria_dir / "schema.json").read_text(encoding="utf-8")))
    documents: dict[str, dict] = {}
    problems: list[str] = []
    for path in sorted(criteria_dir.glob("*.yaml")):
        document = yaml.safe_load(path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(document), key=lambda e: list(e.absolute_path))
        problems += [f"{path}: {'/'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}" for e in errors]
        if errors:
            continue
        if document["area"] != path.stem:
            problems.append(f"{path}: area '{document['area']}' must match the file name '{path.stem}'")
        documents[path.stem] = document
    return documents, problems + check_consistency(criteria_dir, documents)


def check_consistency(criteria_dir: Path, documents: dict[str, dict]) -> list[str]:
    problems = []
    first_seen: dict[str, str] = {}
    prefixes = {doc["prefix"] for doc in documents.values()}
    for area, document in documents.items():
        path = criteria_dir / f"{area}.yaml"
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
    for area, document in documents.items():
        for criterion in document["criteria"]:
            for target in criterion.get("related", []):
                if target not in prefixes and target not in first_seen:
                    problems.append(f"{criteria_dir / f'{area}.yaml'}: {criterion['id']} relates to unknown '{target}'")
    return problems


def render_table(document: dict) -> str:
    active = [c for c in document["criteria"] if c.get("status", "active") == "active"]
    with_check = any("check" in c for c in active)
    header = ["ID", "Criterion"] + (["Check"] if with_check else []) + ["Fail signal", "Default severity"]
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    for criterion in active:
        details = [criterion[k] for k in ("severity_note",) if k in criterion]
        if criterion.get("related"):
            details.append("→ " + ", ".join(criterion["related"]))
        severity = criterion["severity"] + (f" ({'; '.join(details)})" if details else "")
        cells = [criterion["id"], criterion["name"]] + ([criterion.get("check", "—")] if with_check else [])
        cells += [criterion["fail_signal"], severity]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_block(document: dict) -> str:
    return (
        f"<!-- BEGIN GENERATED criteria ({document['area']}) -->\n"
        f"<!-- Source: criteria/{document['area']}.yaml. Edit the YAML, then run scripts/generate.py. -->\n"
        f"{render_table(document)}\n"
        "<!-- END GENERATED criteria -->"
    )


def sync(skill_dir: Path, documents: dict[str, dict], write: bool) -> list[str]:
    """Rewrite (or compare) every generated block; return the problems found."""
    problems = []
    areas_dir = skill_dir / "references" / "areas"
    for area, document in documents.items():
        path = areas_dir / f"{area}.md"
        if not path.exists():
            problems.append(f"{path}: missing area file for criteria/{area}.yaml")
            continue
        text = path.read_text(encoding="utf-8")
        blocks = list(BLOCK.finditer(text))
        if len(blocks) != 1 or blocks[0]["area"] != area:
            problems.append(f"{path}: expected exactly one generated criteria block for '{area}'")
            continue
        updated = text[: blocks[0].start()] + render_block(document) + text[blocks[0].end():]
        if updated == text:
            continue
        if write:
            path.write_text(updated, encoding="utf-8")
        else:
            problems.append(f"{path}: criteria table is out of date with criteria/{area}.yaml; run scripts/generate.py")
    for path in sorted(areas_dir.glob("*.md")):
        if path.stem not in documents:
            problems.append(f"{path}: no criteria/{path.stem}.yaml for this area")
    return problems


def run(skill_dir: Path, check: bool) -> list[str]:
    documents, problems = load_catalogue(skill_dir)
    if problems:
        return problems
    return sync(skill_dir, documents, write=not check)


def main() -> int:
    check = "--check" in sys.argv[1:]
    problems = []
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        if (skill_md.parent / "criteria").is_dir():
            problems += run(skill_md.parent, check)
    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print(f"{len(problems)} problem(s) found")
        return 1
    print("ok: criteria catalogue is valid and tables are up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
