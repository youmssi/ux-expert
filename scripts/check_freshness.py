"""Flag stack packs whose verification is older than the allowed age.

Frameworks change fast: a pack verified against an old release can turn a correct
finding into a false positive. Run monthly (.github/workflows/freshness.yml); a stale
pack is re-read against its repository's current docs, then `verified` is updated.

Usage: python3 scripts/check_freshness.py [--max-age-days 183] [--today YYYY-MM-DD]
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STACKS = ROOT / "skills" / "ux-expert" / "criteria" / "stacks"


def stale_packs(stacks_dir: Path, today: date, max_age_days: int) -> list[str]:
    problems = []
    for path in sorted(stacks_dir.glob("*.yaml")):
        verified = yaml.safe_load(path.read_text(encoding="utf-8"))["verified"]
        age = (today - date.fromisoformat(verified["verified_on"])).days
        if age > max_age_days:
            problems.append(f"criteria/stacks/{path.name}: verified {age} days ago "
                            f"against {verified['repository']}@{verified['commit'][:7]} ({verified['version']}); re-read the current docs")
    return problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--max-age-days", type=int, default=183)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = parser.parse_args(argv)
    problems = stale_packs(STACKS, args.today, args.max_age_days)
    for problem in problems:
        print(f"stale: {problem}")
    print(f"{len(problems)} stale pack(s)" if problems else "ok: every stack pack was verified recently")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
