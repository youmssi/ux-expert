"""Repository rules the Agent Skills spec validator does not cover.

Checks every skill under ``skills/``:
- ``SKILL.md`` stays within the line budget, and every Markdown file within its
  estimated token budget (about 4 characters per token);
- every relative Markdown link resolves to a file inside the skill directory.

Criterion IDs are validated with the catalogue by scripts/generate.py.

Usage: python3 scripts/validate.py [repo_root]
Exits 1 and lists every problem when a rule is broken.
"""

import re
import sys
from pathlib import Path

MAX_SKILL_LINES = 500
# The spec recommends < 5,000 tokens for SKILL.md; references follow the same
# budget so each loads cheaply on demand. Estimated as characters / 4.
MAX_FILE_TOKENS = 5000
CHARS_PER_TOKEN = 4
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
EXTERNAL = ("http://", "https://", "mailto:", "#")
FENCED_CODE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def prose(md: Path) -> str:
    """Text outside code: examples and search patterns in code are not links."""
    text = FENCED_CODE.sub("", md.read_text(encoding="utf-8"))
    return INLINE_CODE.sub("", text)


def check_line_budget(skill_dir: Path) -> list[str]:
    skill_md = skill_dir / "SKILL.md"
    lines = len(skill_md.read_text(encoding="utf-8").splitlines())
    if lines > MAX_SKILL_LINES:
        return [f"{skill_md}: {lines} lines, budget is {MAX_SKILL_LINES}; move detail to references/"]
    return []


def check_token_budget(skill_dir: Path) -> list[str]:
    problems = []
    for md in sorted(skill_dir.rglob("*.md")):
        tokens = len(md.read_text(encoding="utf-8")) // CHARS_PER_TOKEN
        if tokens > MAX_FILE_TOKENS:
            problems.append(f"{md}: about {tokens} tokens, budget is {MAX_FILE_TOKENS}; split it or cut what agents already know")
    return problems


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



def validate(repo_root: Path) -> list[str]:
    skill_dirs = sorted(p.parent for p in (repo_root / "skills").glob("*/SKILL.md"))
    if not skill_dirs:
        return [f"{repo_root / 'skills'}: no skill found (expected skills/<name>/SKILL.md)"]
    problems = []
    for skill_dir in skill_dirs:
        problems += check_line_budget(skill_dir)
        problems += check_token_budget(skill_dir)
        problems += check_links(skill_dir)
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
