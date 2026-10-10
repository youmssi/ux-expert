"""List the criteria that apply to a product type and phase.

Reads criteria/catalogue.json next to this script's skill (standard library
only, no install needed).

Usage:
    python3 scripts/select_criteria.py --product web-app --phase design
    python3 scripts/select_criteria.py --product mobile --phase build --area forms-input --area accessibility
    python3 scripts/select_criteria.py --product cli --format json

--phase is optional: without it, every criterion is listed (all are auditable).
"""

import argparse
import json
import sys
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parent.parent / "criteria" / "catalogue.json"


def select(catalogue: dict, product: str, phase: str | None, areas: list[str]) -> list[dict]:
    known_areas = {a["area"] for a in catalogue["areas"]}
    unknown = sorted(set(areas) - known_areas)
    if unknown:
        raise ValueError(f"unknown area(s): {', '.join(unknown)}; known: {', '.join(sorted(known_areas))}")
    return [
        c for c in catalogue["criteria"]
        if product in c["applies_to"]
        and (phase is None or phase in c["phases"])
        and (not areas or c["area"] in areas)
    ]


def to_markdown(catalogue: dict, criteria: list[dict], product: str) -> str:
    depth = {a["area"]: a for a in catalogue["areas"]}
    lines: list[str] = []
    current = None
    for c in criteria:
        if c["area"] != current:
            current = c["area"]
            area = depth[current]
            note = f"; {area['applicability_note']}" if area["applicability"][product] == "conditional" else ""
            lines += ["", f"## {current} ({area['prefix']}): {area['applicability'][product]} for {product}{note}"]
        severity = c["severity"] + (f" ({c['severity_note']})" if "severity_note" in c else "")
        lines.append(f"- **{c['id']}** {c['name']}. Fail: {c['fail_signal']}. Severity {severity}.")
    lines.append(f"\n{len(criteria)} criteria.")
    return "\n".join(lines).lstrip("\n") + "\n"


def main(argv: list[str]) -> int:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description="List the ux-expert criteria for a product type and phase.")
    parser.add_argument("--product", required=True, choices=catalogue["product_types"])
    parser.add_argument("--phase", choices=catalogue["phases"])
    parser.add_argument("--area", action="append", default=[], help="limit to an area (repeatable)")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args(argv)
    try:
        criteria = select(catalogue, args.product, args.phase, args.area)
    except ValueError as error:
        parser.error(str(error))
    if args.format == "json":
        print(json.dumps(criteria, ensure_ascii=False, indent=1))
    else:
        print(to_markdown(catalogue, criteria, args.product), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
