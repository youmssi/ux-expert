"""Run the native mobile probes (references/native-probes.md) over a project.

Standard library only. Reads the probes from criteria/catalogue.json.
Usage: python3 scripts/probe.py <project root> [--platform ios,android,flutter,react-native] [--max-hits 20]
Prints JSON: the platforms detected, then per probe its kind, criteria, hit count and first hits.
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


def run(root: Path, platforms: list[str] | None, max_hits: int) -> dict:
    catalogue = json.loads(CATALOGUE.read_text(encoding="utf-8"))
    files = list(source_files(root))
    selected = platforms if platforms else detect(root, files)
    known = {p["id"]: p for p in catalogue["platforms"]}
    unknown = [p for p in selected if p not in known]
    if unknown:
        raise ValueError(f"unknown platform(s) {', '.join(unknown)}; known: {', '.join(known)}")
    results = []
    for platform_id in selected:
        extensions = set(known[platform_id]["extensions"])
        probes = [p for p in catalogue["probes"] if p["platform"] == platform_id]
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
        for probe in probes:
            results.append({"probe": probe["id"], "platform": platform_id, "kind": probe["kind"], "criteria": probe["criteria"],
                            "look_for": probe["look_for"], "count": counts[probe["id"]], "hits": hits[probe["id"]]})
    return {"root": str(root), "platforms": selected, "results": results}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run the native mobile probes over a project.")
    parser.add_argument("root", type=Path)
    parser.add_argument("--platform", help="comma-separated platform IDs; default: detected from the project")
    parser.add_argument("--max-hits", type=int, default=20, help="hits listed per probe (all are counted)")
    args = parser.parse_args(argv)
    if not args.root.is_dir():
        parser.error(f"{args.root} is not a directory")
    try:
        report = run(args.root.resolve(), args.platform.split(",") if args.platform else None, args.max_hits)
    except ValueError as error:
        parser.error(str(error))
    if not report["platforms"]:
        print("probe: no native platform detected (no .swift, .kt, pubspec.yaml or react-native/expo dependency)", file=sys.stderr)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
