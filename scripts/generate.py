"""Build everything derived from the criteria catalogue.

The YAML files in ``skills/<skill>/criteria/`` are the source of truth. From
them this script writes:

- the criteria table in each area file, between
  ``<!-- BEGIN GENERATED criteria (<area>) -->`` and ``<!-- END GENERATED criteria -->``;
- the area applicability matrix in ``SKILL.md``, between
  ``<!-- BEGIN GENERATED applicability -->`` and ``<!-- END GENERATED applicability -->``;
- ``criteria/catalogue.json``: every active criterion with its effective phases
  and product types, for tools that should not parse YAML.

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


def check_citations(skill_dir: Path, documents: dict[str, dict], extra_files: list[Path]) -> list[str]:
    """Every criterion ID cited with a known prefix must exist and be active."""
    prefixes = {doc["prefix"] for doc in documents.values()}
    ids = {c["id"] for doc in documents.values() for c in active(doc)}
    problems = []
    for path in sorted(skill_dir.rglob("*.md")) + extra_files:
        for prefix, number in CITATION.findall(path.read_text(encoding="utf-8")):
            cited = f"{prefix}-{number}"
            if prefix in prefixes and cited not in ids:
                problems.append(f"{path}: cites {cited}, which is not an active criterion")
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


def render_catalogue(documents: dict[str, dict]) -> str:
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
            item |= {k: criterion[k] for k in ("name", "check", "fail_signal", "severity", "severity_note", "related") if k in criterion}
            item["phases"] = criterion.get("phases", document["phases"])
            item["applies_to"] = criterion.get("applies_to", area_product_types(document))
            criteria.append(item)
    catalogue = {
        "generated_by": "scripts/generate.py from criteria/*.yaml; do not edit",
        "product_types": list(PRODUCT_TYPES),
        "phases": ["design", "build"],
        "areas": areas,
        "criteria": criteria,
        "retired_ids": retired,
    }
    return json.dumps(catalogue, ensure_ascii=False, indent=1) + "\n"


def replace_blocks(text: str, pattern: re.Pattern, block: str) -> str | None:
    """Replace the single generated block matching ``pattern``; None when it is missing or repeated."""
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        return None
    return text[: matches[0].start()] + block + text[matches[0].end():]


def planned_outputs(skill_dir: Path, documents: dict[str, dict]) -> tuple[dict[Path, str], list[str]]:
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
    outputs[skill_dir / "criteria" / "catalogue.json"] = render_catalogue(documents)
    return outputs, problems


def run(skill_dir: Path, check: bool, extra_files: list[Path] = ()) -> list[str]:
    documents, problems = load_catalogue(skill_dir)
    if problems:
        return problems
    outputs, problems = planned_outputs(skill_dir, documents)
    problems += check_citations(skill_dir, documents, list(extra_files))
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == content:
            continue
        if check:
            problems.append(f"{path}: out of date with criteria/*.yaml; run scripts/generate.py")
        else:
            path.write_text(content, encoding="utf-8")
    return problems


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
