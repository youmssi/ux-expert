"""Repository rules the Agent Skills spec validator does not cover.

Checks every skill under ``skills/``:
- ``SKILL.md`` stays within the line budget;
- every relative Markdown link resolves to a file inside the skill directory;
- criterion IDs in criteria tables are well formed and unique across the skill.

Usage: python3 scripts/validate.py [repo_root]
Exits 1 and lists every problem when a rule is broken.
"""

import re
import sys
from pathlib import Path

MAX_SKILL_LINES = 500
CRITERION_ROW = re.compile(r"^\|\s*([A-Z0-9]+-\d+)\s*\|", re.MULTILINE)
CRITERION_ID = re.compile(r"^[A-Z][A-Z0-9]*-\d{2,}$")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")
FENCED_CODE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def prose(md: Path) -> str:
    """Text outside code: examples and search patterns in code are not links or criteria."""
    text = FENCED_CODE.sub("", md.read_text(encoding="utf-8"))
    return INLINE_CODE.sub("", text)


def check_line_budget(skill_dir: Path) -> list[str]:
    skill_md = skill_dir / "SKILL.md"
    lines = len(skill_md.read_text(encoding="utf-8").splitlines())
    if lines > MAX_SKILL_LINES:
        return [f"{skill_md}: {lines} lines, budget is {MAX_SKILL_LINES}; move detail to references/"]
    return []


def check_links(skill_dir: Path) -> list[str]:
    problems = []
    root = skill_dir.resolve()
    for md in sorted(skill_dir.rglob("*.md")):
        for target in LINK.findall(prose(md)):
            if target.startswith(EXTERNAL):
                continue
            resolved = (md.parent / target.split("#", 1)[0]).resolve()
            if not resolved.is_relative_to(root):
                problems.append(f"{md}: link '{target}' leaves the skill directory")
            elif not resolved.exists():
                problems.append(f"{md}: link '{target}' points to a missing file")
    return problems


def check_criterion_ids(skill_dir: Path) -> list[str]:
    problems = []
    seen: dict[str, Path] = {}
    for md in sorted(skill_dir.rglob("*.md")):
        for criterion_id in CRITERION_ROW.findall(prose(md)):
            if not CRITERION_ID.match(criterion_id):
                problems.append(f"{md}: malformed criterion ID '{criterion_id}' (expected PREFIX-NN)")
            elif criterion_id in seen:
                problems.append(f"{md}: duplicate criterion ID '{criterion_id}', first defined in {seen[criterion_id]}")
            else:
                seen[criterion_id] = md
    return problems


def validate(repo_root: Path) -> list[str]:
    skill_dirs = sorted(p.parent for p in (repo_root / "skills").glob("*/SKILL.md"))
    if not skill_dirs:
        return [f"{repo_root / 'skills'}: no skill found (expected skills/<name>/SKILL.md)"]
    problems = []
    for skill_dir in skill_dirs:
        problems += check_line_budget(skill_dir)
        problems += check_links(skill_dir)
        problems += check_criterion_ids(skill_dir)
    return problems


def main() -> int:
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    problems = validate(repo_root)
    for problem in problems:
        print(f"error: {problem}")
    if problems:
        print(f"{len(problems)} problem(s) found")
        return 1
    print("ok: all skills pass the repository rules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
