# ADR-003: MIT for code, CC BY 4.0 for content

- **Status:** accepted
- **Date:** 2026-10-09
- **Story:** UXE-1

## Context

The repository holds two kinds of work: **code** (validation scripts, later the
MCP server) and **content** (skill text, criteria, references). The goal is the
widest adoption by people, companies and AI agents, while the author keeps
credit for the expertise.

## Options considered

1. **MIT for everything.** Simple and permissive. But MIT is written for
   software, and attribution of reused *content* is weakly defined.
2. **MIT for code, CC BY 4.0 for content.** Each license fits its material.
   CC BY 4.0 allows any use, including commercial use and adaptation, as long
   as credit is given. Cons: two license files to explain.
3. **Copyleft (GPL / CC BY-SA).** Protects openness, but discourages adoption
   inside companies and products.
4. **No license.** All rights reserved by default; nobody can legally reuse it.

## Decision

Option 2: code under MIT (`LICENSE`), content under CC BY 4.0
(`LICENSE-CONTENT`). The skill's frontmatter says
`license: CC-BY-4.0 (content), MIT (code). See LICENSE files.`

## Consequences

- Anyone can use and adapt the package commercially, with attribution for the
  content.
- Third-party material quoted in the content (standards, guidelines) stays under
  its own terms; we cite it and quote only short excerpts.
- Changing the license later only applies to future versions; copies of
  released versions keep their terms.
