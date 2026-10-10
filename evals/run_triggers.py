"""Measure how reliably the skill's description triggers.

Follows the Agent Skills guide "Optimizing skill descriptions": each query in
trigger_queries.json runs several times with the skill installed, and the
trigger rate is recorded. A should-trigger query passes above 0.5, a
should-not-trigger query below it.

Usage: python3 evals/run_triggers.py [--runs 3]
Costs model tokens (20 queries x runs agent sessions). Uses Claude Code in
headless mode; change triggered() for another agent.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUERIES = Path(__file__).resolve().parent / "trigger_queries.json"
THRESHOLD = 0.5


def triggered(workdir: Path, query: str) -> bool:
    """True when the agent invoked the ux-expert skill while handling the query."""
    result = subprocess.run(
        ["claude", "-p", query, "--output-format", "stream-json", "--verbose", "--max-turns", "2"],
        cwd=workdir, capture_output=True, text=True, timeout=600,
    )
    for line in result.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        for block in event.get("message", {}).get("content", []) if isinstance(event.get("message"), dict) else []:
            if block.get("type") == "tool_use" and block.get("name") == "Skill" and block.get("input", {}).get("skill") == "ux-expert":
                return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    if not shutil.which("claude"):
        print("claude CLI not found; adapt triggered() to your agent", file=sys.stderr)
        return 1
    queries = json.loads(QUERIES.read_text(encoding="utf-8"))
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        shutil.copytree(ROOT / "skills" / "ux-expert", work / ".claude" / "skills" / "ux-expert")
        for q in queries:
            rate = sum(triggered(work, q["query"]) for _ in range(args.runs)) / args.runs
            passed = rate > THRESHOLD if q["should_trigger"] else rate < THRESHOLD
            results.append({**q, "trigger_rate": round(rate, 2), "passed": passed})
            print(f"{'PASS' if passed else 'FAIL'} {rate:.2f} {'+' if q['should_trigger'] else '-'} {q['query'][:70]}")
    passed = sum(r["passed"] for r in results)
    print(json.dumps({"passed": passed, "total": len(results), "results": results}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
