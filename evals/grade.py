"""Grade ux-expert eval outputs and aggregate a benchmark.

Audit evals are graded against the fixture's answer key: a seeded defect is
found when one finding names its file and any of its criterion IDs; a decoy is
a false positive under the same rule. Design evals are graded on structure.
Assertion results follow the Agent Skills eval format (grading.json).

Usage:
    python3 evals/grade.py <eval-id> <report.md> [--out grading.json]
    python3 evals/grade.py --benchmark <iteration-dir>
Standard library plus PyYAML (scripts/requirements.txt).
"""

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

import yaml

EVALS_DIR = Path(__file__).resolve().parent
CATALOGUE = EVALS_DIR.parent / "skills" / "ux-expert" / "criteria" / "catalogue.json"
CITATION = re.compile(r"\b([A-Z][A-Z0-9]*)-(\d{2,})\b")
FINDING_START = re.compile(r"^#{2,4} +F-\d+", re.MULTILINE)
REQUIRED_FIELDS = ("Severity", "Priority", "Recommendation", "Verification")
RECALL_TARGET = 0.7


def load_catalogue_ids() -> tuple[set[str], set[str]]:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    return {c["id"] for c in catalogue["criteria"]}, {a["prefix"] for a in catalogue["areas"]}


def cited_ids(text: str, prefixes: set[str]) -> set[str]:
    return {f"{p}-{n}" for p, n in CITATION.findall(text) if p in prefixes}


def finding_blocks(report: str) -> list[str]:
    starts = [m.start() for m in FINDING_START.finditer(report)]
    return [report[a:b] for a, b in zip(starts, starts[1:] + [len(report)])]


def matches(block: str, key: dict) -> bool:
    return key["file"] in block and any(re.search(rf"\b{re.escape(c)}\b", block) for c in key["criteria"])


def assertion(text: str, passed: bool, evidence: str) -> dict:
    return {"text": text, "passed": passed, "evidence": evidence}


def grade_audit(report: str, answer_key: dict, ids: set[str], prefixes: set[str]) -> dict:
    blocks = finding_blocks(report)
    found = [d["id"] for d in answer_key["defects"] if any(matches(b, d) for b in blocks)]
    false_positives = [n["id"] for n in answer_key["decoys"] if any(matches(b, n) for b in blocks)]
    unknown = sorted(cited_ids(report, prefixes) - ids)
    incomplete = [i + 1 for i, b in enumerate(blocks) if not all(f in b for f in REQUIRED_FIELDS)]
    total = len(answer_key["defects"])
    recall = len(found) / total if total else 0.0
    missed = [d["id"] for d in answer_key["defects"] if d["id"] not in found]
    return {
        "metrics": {"findings": len(blocks), "recall": round(recall, 3), "found": found, "missed": missed,
                    "false_positives": false_positives, "unknown_ids": unknown, "incomplete_findings": incomplete},
        "assertion_results": [
            assertion(f"Recall of seeded defects is at least {RECALL_TARGET}", recall >= RECALL_TARGET,
                      f"{len(found)}/{total} found; missed: {', '.join(missed) or 'none'}"),
            assertion("No decoy is reported as a defect", not false_positives,
                      f"false positives: {', '.join(false_positives) or 'none'}"),
            assertion("Every cited criterion ID exists in the catalogue", not unknown, f"unknown: {', '.join(unknown) or 'none'}"),
            assertion("Every finding has severity, priority, recommendation and verification", bool(blocks) and not incomplete,
                      f"{len(blocks)} findings; incomplete: {incomplete or 'none'}"),
        ],
    }


def story_sections(report: str, keys: list[str]) -> dict[str, str]:
    positions = sorted((report.find(k), k) for k in keys if report.find(k) >= 0)
    sections = {}
    for i, (start, key) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(report)
        sections[key] = report[start:end]
    return sections


def grade_design(report: str, ids: set[str], prefixes: set[str], stories=("CARE-1", "CARE-2", "CARE-3")) -> dict:
    sections = story_sections(report, list(stories))
    counts, coverage = {}, {}
    for story in stories:
        lines = [l for l in sections.get(story, "").splitlines() if l.strip().startswith("- [") and cited_ids(l, prefixes)]
        counts[story] = len(lines)
        cited = cited_ids(sections.get(story, ""), prefixes)
        coverage[story] = any(c.startswith("STATE-") for c in cited) and any(c.startswith("A11Y-") for c in cited)
    unknown = sorted(cited_ids(report, prefixes) - ids)
    return {
        "metrics": {"criteria_per_story": counts, "states_and_a11y": coverage, "unknown_ids": unknown},
        "assertion_results": [
            assertion("Each story has between 5 and 15 tagged acceptance criteria", all(5 <= n <= 15 for n in counts.values()), str(counts)),
            assertion("Every story covers states and accessibility", all(coverage.values()), str(coverage)),
            assertion("Every cited criterion ID exists in the catalogue", not unknown, f"unknown: {', '.join(unknown) or 'none'}"),
            assertion("At least one [INTERACTIVE STEP] is raised", "[INTERACTIVE STEP]" in report, "searched for [INTERACTIVE STEP]"),
            assertion("A UX Definition of Done section is present", bool(re.search(r"Definition of Done", report, re.I)), "searched for the heading"),
        ],
    }


def grade(eval_id: str, report: str) -> dict:
    spec = next(e for e in json.loads((EVALS_DIR / "evals.json").read_text(encoding="utf-8"))["evals"] if e["id"] == eval_id)
    ids, prefixes = load_catalogue_ids()
    if spec["kind"] == "audit":
        answer_key = yaml.safe_load((EVALS_DIR / spec["answer_key"]).read_text(encoding="utf-8"))
        result = grade_audit(report, answer_key, ids, prefixes)
    else:
        result = grade_design(report, ids, prefixes)
    passed = sum(a["passed"] for a in result["assertion_results"])
    total = len(result["assertion_results"])
    result["summary"] = {"passed": passed, "failed": total - passed, "total": total, "pass_rate": round(passed / total, 3)}
    return result


def benchmark(iteration: Path) -> dict:
    """Aggregate <iteration>/<eval>/<config>/grading.json into run_summary per config."""
    rates: dict[str, list[float]] = {}
    for grading in sorted(iteration.glob("*/*/grading.json")):
        rates.setdefault(grading.parent.name, []).append(json.loads(grading.read_text())["summary"]["pass_rate"])
    summary = {config: {"pass_rate": {"mean": round(statistics.mean(v), 3), "stddev": round(statistics.pstdev(v), 3), "runs": len(v)}}
               for config, v in rates.items()}
    if "with_skill" in summary and "without_skill" in summary:
        summary["delta"] = {"pass_rate": round(summary["with_skill"]["pass_rate"]["mean"] - summary["without_skill"]["pass_rate"]["mean"], 3)}
    return {"run_summary": summary}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("eval_id", nargs="?")
    parser.add_argument("report", nargs="?", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--benchmark", type=Path)
    args = parser.parse_args()
    if args.benchmark:
        result = benchmark(args.benchmark)
        (args.benchmark / "benchmark.json").write_text(json.dumps(result, indent=2) + "\n")
    elif args.eval_id and args.report:
        result = grade(args.eval_id, args.report.read_text(encoding="utf-8"))
        if args.out:
            args.out.write_text(json.dumps(result, indent=2) + "\n")
    else:
        parser.error("give <eval-id> <report.md>, or --benchmark <iteration-dir>")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
