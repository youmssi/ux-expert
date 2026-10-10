"""Build the release assets for clients that cannot load the skill folder or MCP.

Writes to dist/ (not committed):
- bundles/ux-expert-<mode>.md: one Markdown file per mode, to upload or paste into
  any chat assistant (ChatGPT, DeepSeek, Grok, Gemini…);
- ux-expert-skill.zip: the skill folder, for clients that install skills by upload.

Standard library only. Usage: python3 scripts/bundle.py [output_dir]
"""

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ux-expert"
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.DOTALL)

SHARED = ["references/finding-format.md", "references/severity-and-scoring.md", "references/laws-and-numbers.md", "references/sources.md",
          "references/patterns.md"]
AREAS = sorted(f"references/areas/{p.name}" for p in (SKILL / "references" / "areas").glob("*.md"))
STACKS = sorted(f"references/stacks/{p.name}" for p in (SKILL / "references" / "stacks").glob("*.md"))
BUNDLES = {
    "design": {
        "task": "turn a brief or user stories into UX requirements and testable acceptance criteria (Design mode)",
        "files": ["SKILL.md", "references/design-mode.md", "assets/story-ux.md", "references/areas/context-discovery.md",
                  "references/areas/flows-friction.md", "references/laws-and-numbers.md", "references/sources.md"],
        "design_criteria": True,
    },
    "audit": {
        "task": "audit a product, flow, area or change, and decide launch readiness (audit modes)",
        "files": ["SKILL.md", *SHARED, "references/codebase-recon.md", "references/native-probes.md", "references/stacks.md", *STACKS, "references/report-template.md", *AREAS],
        "design_criteria": False,
    },
    "refactor": {
        "task": "turn audit findings into a sequenced, guarded refactor plan (Refactor mode)",
        "files": ["SKILL.md", "references/refactor-mode.md", *SHARED],
        "design_criteria": False,
    },
    "full": {
        "task": "design, audit and refactor (every mode)",
        "files": ["SKILL.md", "references/design-mode.md", "references/refactor-mode.md", "assets/story-ux.md", *SHARED,
                  "references/codebase-recon.md", "references/native-probes.md", "references/stacks.md", *STACKS, "references/report-template.md", *AREAS],
        "design_criteria": True,
    },
}


def skill_version() -> str:
    match = re.search(r'^\s+version: "([^"]+)"', (SKILL / "SKILL.md").read_text(encoding="utf-8"), re.MULTILINE)
    if not match:
        raise SystemExit("bundle: no metadata.version in SKILL.md")
    return match.group(1)


def design_criteria_table() -> str:
    catalogue = json.loads((SKILL / "criteria" / "catalogue.json").read_text(encoding="utf-8"))
    rows = [c for c in catalogue["criteria"] if "design" in c["phases"]]
    lines = [
        "Design-phase criteria (the bundle's replacement for `scripts/select_criteria.py`). Keep the rows whose",
        "product types include yours, then keep only what each story touches.",
        "",
        "| ID | Criterion | Fail signal | Severity | Product types |",
        "|---|---|---|---|---|",
    ]
    lines += [f"| {c['id']} | {c['name']} | {c['fail_signal']} | {c['severity']} | {', '.join(c['applies_to'])} |" for c in rows]
    return "\n".join(lines)


def section(path: str, body: str) -> str:
    return f"\n\n<!-- ===== FILE: {path} ===== -->\n\n{body.strip()}\n"


def build_bundle(mode: str, spec: dict, version: str) -> str:
    header = (
        f"# ux-expert {version}: {mode} bundle\n\n"
        f"Instructions for an AI assistant: you are a principal UX engineer. Use this file to {spec['task']}.\n"
        "Follow `SKILL.md` first; it tells you which section to read for each step. File paths mentioned in the text\n"
        "(such as `references/areas/forms-input.md`) refer to the sections of this file marked `FILE:`. Where the text\n"
        "says to run a script or call a tool you do not have, use the tables in this file instead.\n\n"
        "Source: https://github.com/youmssi/ux-expert. Content licensed under CC BY 4.0; credit \"ux-expert by youmssi\".\n\n"
        "Sections: " + ", ".join(f"`{f}`" for f in spec["files"]) + ("" if not spec["design_criteria"] else ", `criteria (design phase)`")
    )
    parts = [header]
    for path in spec["files"]:
        parts.append(section(path, FRONTMATTER.sub("", (SKILL / path).read_text(encoding="utf-8"))))
    if spec["design_criteria"]:
        parts.append(section("criteria (design phase)", design_criteria_table()))
    return "".join(parts)


def build_zip(target: Path) -> None:
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(SKILL.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                archive.write(path, Path("ux-expert") / path.relative_to(SKILL))


def build(out_dir: Path) -> dict[str, int]:
    """Write every asset; return {file name: estimated tokens} for the bundles."""
    version = skill_version()
    bundles_dir = out_dir / "bundles"
    bundles_dir.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for mode, spec in BUNDLES.items():
        text = build_bundle(mode, spec, version)
        name = f"ux-expert-{mode}.md"
        (bundles_dir / name).write_text(text, encoding="utf-8")
        sizes[name] = len(text) // 4
    build_zip(out_dir / "ux-expert-skill.zip")
    return sizes


def main() -> int:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    for name, tokens in build(out_dir).items():
        print(f"{name}: about {tokens:,} tokens")
    print(f"ux-expert-skill.zip written to {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
