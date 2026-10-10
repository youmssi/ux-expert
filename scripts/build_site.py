"""Build the documentation site from the repository's own sources.

Pages: the README (home), install and project guides, the stability policy, the
changelog, one page per area, the searchable criteria catalogue, patterns,
native probes and sources. Nothing is written by hand for the site: it follows
the skill, so it cannot drift from it.

Usage: python3 scripts/build_site.py [out_dir]   (default: site/)
"""

import html
import json
import re
import shutil
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "ux-expert"
REPO = "https://github.com/youmssi/ux-expert"
BLOB = f"{REPO}/blob/main/"
TREE = f"{REPO}/tree/main/"
EXTENSIONS = ["tables", "fenced_code", "toc", "sane_lists"]
HREF = re.compile(r'href="([^"#:]+)(#[^"]*)?"')
SRC = re.compile(r"\[src:([a-z0-9]+(?:-[a-z0-9]+)*)\]")
TABLE = re.compile(r"<table>(.*?)</table>", re.DOTALL)


def pages() -> dict[str, tuple[Path, str]]:
    """{output page: (source file, title)} for every Markdown page."""
    result = {
        "index.html": (ROOT / "README.md", "ux-expert"),
        "install.html": (ROOT / "docs" / "install.md", "Install"),
        "use-in-your-project.html": (ROOT / "docs" / "use-in-your-project.md", "Use in your project"),
        "stability.html": (ROOT / "docs" / "stability.md", "Stability policy"),
        "changelog.html": (ROOT / "CHANGELOG.md", "Changelog"),
        "patterns.html": (SKILL / "references" / "patterns.md", "Proven patterns"),
        "native-probes.html": (SKILL / "references" / "native-probes.md", "Native mobile probes"),
    }
    for area in sorted((SKILL / "references" / "areas").glob("*.md")):
        title = area.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        result[f"areas/{area.stem}.html"] = (area, title)
    return result


LIST_ITEM = re.compile(r"^\s*([-*+]|\d+\.)\s")


def blank_line_before_lists(text: str) -> str:
    """GitHub starts a list right after a paragraph line; Python-Markdown needs a blank line first."""
    lines, fenced = [], False
    for line in text.splitlines():
        if line.startswith(("```", "~~~")):
            fenced = not fenced
        if not fenced and LIST_ITEM.match(line) and lines and lines[-1].strip() and not LIST_ITEM.match(lines[-1]) \
                and not lines[-1].startswith(("    ", "\t", "|")):
            lines.append("")
        lines.append(line)
    return "\n".join(lines) + "\n"


def rewrite_links(body: str, source: Path, page: str, by_source: dict[Path, str]) -> str:
    """Point links at site pages when the target is one, otherwise at the file on GitHub."""
    depth = "../" * page.count("/")

    def replace(match: re.Match) -> str:
        target = (source.parent / match[1]).resolve()
        anchor = match[2] or ""
        if target in by_source:
            return f'href="{depth}{by_source[target]}{anchor}"'
        if target == (SKILL / "references" / "sources.md").resolve():
            return f'href="{depth}sources.html{anchor}"'
        if target.is_relative_to(ROOT):
            base = TREE if target.is_dir() else BLOB
            return f'href="{base}{target.relative_to(ROOT).as_posix()}{anchor}"'
        return match[0]

    body = HREF.sub(replace, body)
    body = SRC.sub(lambda m: f'<a href="{depth}sources.html#src-{m[1]}">[src:{m[1]}]</a>', body)
    # Wide tables scroll inside a focusable region instead of the page.
    body = TABLE.sub(r'<div class="table" role="region" aria-label="Table" tabindex="0"><table>\1</table></div>', body)
    # Code blocks scroll horizontally; keyboard users must be able to reach them.
    return body.replace("<pre>", '<pre tabindex="0">')


def layout(title: str, body: str, page: str, nav: list[tuple[str, str]]) -> str:
    depth = "../" * page.count("/")
    links = "".join(
        f'<li><a href="{depth}{href}"{" aria-current=\"page\"" if href == page else ""}>{html.escape(label)}</a></li>'
        for href, label in nav
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · ux-expert</title>
<link rel="stylesheet" href="{depth}style.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header>
<a class="brand" href="{depth}index.html">ux-expert</a>
<nav aria-label="Main"><ul>{links}</ul></nav>
</header>
<main id="main">
{body}
</main>
<footer><p>Code MIT · content CC BY 4.0 · <a href="{REPO}">Source on GitHub</a></p></footer>
</body>
</html>
"""


def areas_index(catalogue: dict) -> str:
    rows = "".join(
        f'<tr><td><a href="areas/{a["area"]}.html">{html.escape(a["area"].replace("-", " ").capitalize())}</a></td>'
        f'<td><code>{a["prefix"]}</code></td><td>{sum(1 for c in catalogue["criteria"] if c["area"] == a["area"])}</td></tr>'
        for a in catalogue["areas"]
    )
    return ('<h1>Areas</h1><p>Each area has an expert procedure, gotchas and criteria. Read the one your scope needs.</p>'
            '<div class="table" role="region" aria-label="Areas" tabindex="0"><table><thead><tr><th scope="col">Area</th>'
            f'<th scope="col">Prefix</th><th scope="col">Criteria</th></tr></thead><tbody>{rows}</tbody></table></div>')


def criteria_page(catalogue: dict) -> str:
    rows = "".join(
        f'<tr id="{c["id"]}" data-types="{" ".join(c["applies_to"])}" data-phases="{" ".join(c["phases"])}">'
        f'<td><code>{c["id"]}</code></td><td>{html.escape(c["name"])}</td><td>{html.escape(c["fail_signal"])}</td>'
        f'<td>{html.escape(c["severity"])}</td><td><a href="areas/{c["area"]}.html">{c["area"]}</a></td></tr>'
        for c in catalogue["criteria"]
    )
    types = "".join(f'<option value="{t}">{t}</option>' for t in catalogue["product_types"])
    return f"""<h1>Criteria</h1>
<p>Every active criterion, with its permanent ID. Filter by words, product type or phase.</p>
<form class="filters" role="search" onsubmit="return false">
<label>Words <input id="q" type="search" autocomplete="off"></label>
<label>Product type <select id="type"><option value="">All</option>{types}</select></label>
<label>Phase <select id="phase"><option value="">All</option><option value="design">design</option><option value="build">build</option></select></label>
</form>
<p id="count" role="status">{len(catalogue["criteria"])} criteria</p>
<div class="table" role="region" aria-label="Criteria" tabindex="0"><table id="criteria">
<thead><tr><th scope="col">ID</th><th scope="col">Criterion</th><th scope="col">Fail signal</th><th scope="col">Default severity</th><th scope="col">Area</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<script>
(() => {{
  const q = document.getElementById('q'), type = document.getElementById('type'), phase = document.getElementById('phase');
  const rows = [...document.querySelectorAll('#criteria tbody tr')], count = document.getElementById('count');
  function apply() {{
    const words = q.value.toLowerCase().split(/\\s+/).filter(Boolean);
    let shown = 0;
    for (const row of rows) {{
      const ok = words.every(w => row.textContent.toLowerCase().includes(w))
        && (!type.value || row.dataset.types.split(' ').includes(type.value))
        && (!phase.value || row.dataset.phases.split(' ').includes(phase.value));
      row.hidden = !ok;
      shown += ok;
    }}
    count.textContent = shown + (shown === 1 ? ' criterion' : ' criteria');
  }}
  for (const el of [q, type, phase]) el.addEventListener('input', apply);
}})();
</script>"""


def sources_page(catalogue: dict) -> str:
    rows = "".join(
        f'<tr id="src-{s["id"]}"><td><code>{s["id"]}</code></td>'
        f'<td>{f"<a href=\"{html.escape(s["url"])}\">{html.escape(s["title"])}</a>" if "url" in s else html.escape(s["title"])}</td>'
        f'<td>{s["status"]}</td><td>{html.escape(s.get("verified_on", "—"))}</td><td>{html.escape(s["supports"])}</td></tr>'
        for s in catalogue["sources"]
    )
    return ('<h1>Sources</h1><p>The evidence behind the numbers and claims in the skill, and how each was verified. '
            'The numbers of an <strong>unconfirmed</strong> source are never stated as fact.</p>'
            '<div class="table" role="region" aria-label="Sources" tabindex="0"><table><thead><tr><th scope="col">ID</th>'
            '<th scope="col">Source</th><th scope="col">Status</th><th scope="col">Verified</th><th scope="col">Backs</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')


def build(out: Path) -> list[str]:
    if out.exists():
        shutil.rmtree(out)
    (out / "areas").mkdir(parents=True)
    catalogue = json.loads((SKILL / "criteria" / "catalogue.json").read_text(encoding="utf-8"))
    nav = [("areas.html", "Areas"), ("criteria.html", "Criteria"), ("patterns.html", "Patterns"),
           ("install.html", "Install"), ("use-in-your-project.html", "Use it"), ("stability.html", "Stability"),
           ("changelog.html", "Changelog")]
    all_pages = pages()
    by_source = {source.resolve(): page for page, (source, _) in all_pages.items()}
    written = []
    for page, (source, title) in all_pages.items():
        text = source.read_text(encoding="utf-8")
        if page == "index.html":
            # The README's centered title and badges are for GitHub; the site has its own heading.
            text = "# ux-expert\n\nPrincipal-level UX expertise for AI agents.\n\n" + text[text.index("## Introduction"):]
        body = markdown.markdown(blank_line_before_lists(text), extensions=EXTENSIONS)
        (out / page).write_text(layout(title, rewrite_links(body, source, page, by_source), page, nav), encoding="utf-8")
        written.append(page)
    for page, title, body in (("areas.html", "Areas", areas_index(catalogue)),
                              ("criteria.html", "Criteria", criteria_page(catalogue)),
                              ("sources.html", "Sources", sources_page(catalogue))):
        (out / page).write_text(layout(title, body, page, nav), encoding="utf-8")
        written.append(page)
    shutil.copy(ROOT / "docs" / "site" / "style.css", out / "style.css")
    (out / ".nojekyll").write_text("")
    return written


def main(argv: list[str]) -> int:
    out = Path(argv[0]) if argv else ROOT / "site"
    written = build(out)
    print(f"site: {len(written)} pages in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
