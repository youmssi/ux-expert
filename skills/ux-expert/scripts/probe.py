"""Run the native mobile probes (references/native-probes.md) and stack pack probes
(references/stacks.md) over a project.

Standard library only. Reads the probes from criteria/catalogue.json.
Usage: python3 scripts/probe.py <project root> [--platform ios,android,flutter,react-native] [--stack nextjs,shadcn-ui] [--max-hits 20]
Prints JSON: the platforms and stack packs detected (with the pack to read), then per probe its kind, criteria,
hit count and first hits.
A hit is a place to look, not a finding: open the code and check it before reporting.
Comment lines are skipped.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

CATALOGUE = Path(__file__).resolve().parent.parent / "criteria" / "catalogue.json"
SKIP_DIRS = {".git", "node_modules", "build", "dist", "Pods", "Carthage", "DerivedData", ".dart_tool", ".gradle",
             ".expo", ".next", "vendor", ".venv", "__pycache__", ".idea", ".build"}
MAX_FILE_BYTES = 1_000_000
# Line comments and doc comments in all four languages; code in comments is not shipped.
COMMENT = re.compile(r"\s*(//|/\*|\*)")


def source_files(root: Path):
    """Every file under root, without descending into dependency and build folders."""
    for directory, subdirs, names in os.walk(root):
        subdirs[:] = sorted(d for d in subdirs if d not in SKIP_DIRS)
        for name in sorted(names):
            yield Path(directory) / name


def detect(root: Path, files: list[Path]) -> list[str]:
    found = []
    suffixes = {p.suffix for p in files}
    if ".swift" in suffixes:
        found.append("ios")
    if ".kt" in suffixes or any(p.name == "AndroidManifest.xml" for p in files):
        found.append("android")
    if (root / "pubspec.yaml").exists():
        found.append("flutter")
    package = root / "package.json"
    if package.exists():
        try:
            manifest = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            manifest = {}
        deps = {**manifest.get("dependencies", {}), **manifest.get("devDependencies", {})}
        if "react-native" in deps or "expo" in deps:
            found.append("react-native")
    return found


def read_manifest(root: Path) -> dict:
    try:
        return json.loads((root / "package.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def detect_stacks(root: Path, stacks: list[dict]) -> list[str]:
    """Stacks whose dependency is in package.json or whose marker file is at the project root."""
    manifest = read_manifest(root)
    deps = {**manifest.get("dependencies", {}), **manifest.get("devDependencies", {})}
    return [s["id"] for s in stacks
            if any(d in deps for d in s["detect"].get("dependencies", []))
            or any((root / f).exists() for f in s["detect"].get("files", []))]


def scan(root: Path, files: list[Path], extensions: set[str], probes: list[dict], max_hits: int) -> dict[str, tuple[int, list[dict]]]:
    compiled = [(p, re.compile(p["pattern"])) for p in probes]
    hits: dict[str, list[dict]] = {p["id"]: [] for p in probes}
    counts = dict.fromkeys(hits, 0)
    for path in files:
        if path.suffix not in extensions or path.stat().st_size > MAX_FILE_BYTES:
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for number, line in enumerate(lines, 1):
            if COMMENT.match(line):
                continue
            for probe, pattern in compiled:
                if pattern.search(line):
                    counts[probe["id"]] += 1
                    if len(hits[probe["id"]]) < max_hits:
                        hits[probe["id"]].append({"file": str(path.relative_to(root)), "line": number, "text": line.strip()[:160]})
    return {i: (counts[i], hits[i]) for i in hits}


def result(probe: dict, key: str, target: str, found: tuple[int, list[dict]]) -> dict:
    return {"probe": probe["id"], key: target, "kind": probe["kind"], "criteria": probe["criteria"],
            "look_for": probe["look_for"], "count": found[0], "hits": found[1]}


def run(root: Path, platforms: list[str] | None, max_hits: int, stacks: list[str] | None = None) -> dict:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    files = list(source_files(root))
    known = {p["id"]: p for p in catalogue["platforms"]}
    known_stacks = {s["id"]: s for s in catalogue.get("stacks", [])}
    # A flag limits the run to what it names; with no flag, everything detected runs.
    selected = platforms if platforms is not None else ([] if stacks is not None else detect(root, files))
    selected_stacks = stacks if stacks is not None else ([] if platforms else detect_stacks(root, list(known_stacks.values())))
    for kind, chosen, valid in (("platform", selected, known), ("stack", selected_stacks, known_stacks)):
        unknown = [i for i in chosen if i not in valid]
        if unknown:
            raise ValueError(f"unknown {kind}(s) {', '.join(unknown)}; known: {', '.join(valid)}")
    results = []
    for platform_id in selected:
        probes = [p for p in catalogue["probes"] if p["platform"] == platform_id]
        found = scan(root, files, set(known[platform_id]["extensions"]), probes, max_hits)
        results += [result(p, "platform", platform_id, found[p["id"]]) for p in probes]
    for stack_id in selected_stacks:
        stack = known_stacks[stack_id]
        probes = stack.get("probes", [])
        found = scan(root, files, set(stack.get("extensions", [])), probes, max_hits)
        results += [result(p, "stack", stack_id, found[p["id"]]) for p in probes]
    return {
        "root": str(root),
        "platforms": selected,
        "stacks": [{"id": i, "name": known_stacks[i]["name"], "read": f"references/stacks/{i}.md"} for i in selected_stacks],
        "results": results,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the native mobile and stack pack probes over a project.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--platform", help="comma-separated platform IDs; default: detected from the project")
    parser.add_argument("--stack", help="comma-separated stack pack IDs (e.g. nextjs,shadcn-ui); default: detected from the project")
    parser.add_argument("--max-hits", type=int, default=20, help="hits listed per probe (all are counted)")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        parser.error(f"{args.root} is not a directory")
    try:
        report = run(args.root.resolve(), args.platform.split(",") if args.platform else None, args.max_hits,
                     args.stack.split(",") if args.stack else None)
    except ValueError as error:
        parser.error(str(error))
    if not report["platforms"] and not report["stacks"]:
        print("probe: no native platform or stack pack detected", file=sys.stderr)
    for stack in report["stacks"]:
        print(f"probe: {stack['name']} detected; read {stack['read']}", file=sys.stderr)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
