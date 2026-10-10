// Builds the site's docs content from the repository, so the site can never drift
// from the skill: every page below is generated from a source file at build time.
// Output: content/docs/** (Markdown + meta.json) and generated/catalogue.json.
import { mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync, copyFileSync } from 'node:fs';
import { basename, dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const site = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repo = resolve(site, '..');
const skill = join(repo, 'skills', 'ux-expert');
const out = join(site, 'content', 'docs');
const BLOB = 'https://github.com/youmssi/ux-expert/blob/main/';
const TREE = 'https://github.com/youmssi/ux-expert/tree/main/';

const catalogue = JSON.parse(readFileSync(join(skill, 'criteria', 'catalogue.json'), 'utf8'));
const prefixes = new Set(catalogue.areas.map(a => a.prefix));
const activeIds = new Set(catalogue.criteria.map(c => c.id));

// Areas in the order SKILL.md presents them, with its "read when" text as the description.
const skillMd = readFileSync(join(skill, 'SKILL.md'), 'utf8');
const areaRows = [...skillMd.matchAll(/^\| `([a-z0-9-]+)\.md` \| ([A-Z0-9]+) \| (.+?) \|$/gm)].map(m => ({ area: m[1], prefix: m[2], when: m[3] }));

/** Source file (repo-relative) → { slug, title?, description? } */
const pages = new Map([
    ['docs/install.md', { slug: 'getting-started/install', description: 'Install the skill or the MCP server in your agent.' }],
    ['docs/use-in-your-project.md', { slug: 'getting-started/use-in-your-project', description: 'Wire ux-expert into a product repository: when to call it and what it produces.' }],
    ['skills/ux-expert/references/design-mode.md', { slug: 'modes/design', description: 'From a brief or user stories to UX acceptance criteria and a Definition of Done.' }],
    ['skills/ux-expert/references/refactor-mode.md', { slug: 'modes/refactor', description: 'From audit findings to a sequenced, guarded improvement plan.' }],
    ['skills/ux-expert/SKILL.md', { slug: 'reference/skill', title: 'The orchestrator (SKILL.md)', description: 'Modes, phases and area selection, as the agent reads them.' }],
    ['skills/ux-expert/references/codebase-recon.md', { slug: 'reference/codebase-recon', description: 'How the agent maps a codebase before judging it.' }],
    ['skills/ux-expert/references/finding-format.md', { slug: 'reference/finding-format', description: 'The exact structure of every finding and coverage table.' }],
    ['skills/ux-expert/references/severity-and-scoring.md', { slug: 'reference/severity-and-scoring', description: 'Severity, reach, confidence, priority and the launch gate.' }],
    ['skills/ux-expert/references/report-template.md', { slug: 'reference/report-template', description: 'The structure of the final audit report.' }],
    ['skills/ux-expert/references/laws-and-numbers.md', { slug: 'reference/laws-and-numbers', description: 'Thresholds and research results, each with its source.' }],
    ['skills/ux-expert/references/patterns.md', { slug: 'reference/patterns', description: 'Proven patterns from public design systems, linked to criteria.' }],
    ['skills/ux-expert/references/native-probes.md', { slug: 'reference/native-probes', description: 'Code search probes for SwiftUI, Compose, Flutter and React Native.' }],
    ['skills/ux-expert/references/stacks.md', { slug: 'stacks', title: 'Stack packs', description: 'What Next.js, shadcn/ui, Radix and Playwright change about UX findings.' }],
    ['docs/stability.md', { slug: 'project/stability', description: 'What stays stable within a major version.' }],
    ['CHANGELOG.md', { slug: 'project/changelog', description: 'Every notable change, per release.' }],
]);
for (const row of areaRows) {
    pages.set(`skills/ux-expert/references/areas/${row.area}.md`, { slug: `areas/${row.area}`, description: `Read when the scope includes: ${row.when.replace(/\*\*/g, '').toLowerCase()}` });
}
for (const stack of catalogue.stacks) {
    pages.set(`skills/ux-expert/references/stacks/${stack.id}.md`, { slug: `stacks/${stack.id}`, description: stack.summary });
}
const bySource = new Map([...pages].map(([src, p]) => [resolve(repo, src), `/docs/${p.slug}`]));
bySource.set(resolve(skill, 'references', 'sources.md'), '/docs/reference/sources');

/** Rewrites one Markdown line outside code: links, source citations, criterion IDs. */
function rewriteProse(text, sourceFile) {
    // Relative links → site pages, or the file on GitHub.
    text = text.replace(/\]\(([^)\s#:]+)(#[^)\s]*)?\)/g, (match, target, anchor = '') => {
        const abs = resolve(dirname(sourceFile), target);
        if (bySource.has(abs)) return `](${bySource.get(abs)}${anchor})`;
        if (abs.startsWith(repo)) {
            const rel = relative(repo, abs).split('\\').join('/');
            return `](${(/\.[a-z]+$/i.test(rel) ? BLOB : TREE) + rel}${anchor})`;
        }
        return match;
    });
    // [src:id] → the source's entry on the sources page.
    text = text.replace(/\[src:([a-z0-9-]+)\]/g, (_, id) => `[\\[src:${id}\\]](/docs/reference/sources#${id})`);
    // Bare criterion IDs → the criteria explorer; skip text already inside link labels or URLs.
    return text.replace(/(^|[^\w\-[/#])([A-Z][A-Z0-9]*)-(\d{2,})\b(?![\]\w])/g, (match, lead, prefix, number) => {
        const id = `${prefix}-${number}`;
        return prefixes.has(prefix) && activeIds.has(id) ? `${lead}[${id}](/criteria#${id})` : match;
    });
}

function transform(markdown, sourceFile) {
    let fenced = false;
    const lines = markdown
        .replace(/^---\n[\s\S]*?\n---\n/, '') // SKILL.md frontmatter
        .replace(/<!--[\s\S]*?-->\n?/g, '') // generated-block markers
        .split('\n')
        .map(line => {
            if (/^\s*(```|~~~)/.test(line)) fenced = !fenced;
            if (fenced || /^\s*(```|~~~)/.test(line)) return line;
            // Keep inline code untouched.
            return line.split(/(`[^`]*`)/).map(part => (part.startsWith('`') ? part : rewriteProse(part, sourceFile))).join('');
        });
    return lines.join('\n');
}

function frontmatter(fields) {
    const body = Object.entries(fields)
        .filter(([, v]) => v)
        .map(([k, v]) => `${k}: ${JSON.stringify(v)}`)
        .join('\n');
    return `---\n${body}\n---\n\n`;
}

function writePage(slug, title, description, body) {
    const file = join(out, `${slug.endsWith('/') ? slug + 'index' : slug}.md`);
    mkdirSync(dirname(file), { recursive: true });
    writeFileSync(file, frontmatter({ title, description }) + body.trimStart());
}

rmSync(out, { recursive: true, force: true });
mkdirSync(out, { recursive: true });

for (const [src, page] of pages) {
    const file = resolve(repo, src);
    const raw = readFileSync(file, 'utf8');
    const h1 = raw.replace(/^---\n[\s\S]*?\n---\n/, '').match(/^# (.+)$/m);
    const title = page.title ?? (h1 ? h1[1] : basename(src, '.md'));
    const body = transform(raw.replace(/^---\n[\s\S]*?\n---\n/, '').replace(/^# .+\n/m, ''), file);
    // A folder landing page (stacks) becomes the folder's index.
    const slug = src.endsWith('references/stacks.md') ? 'stacks/index' : page.slug;
    writePage(slug, title, page.description, body);
}

// Sources: one heading per source so citations can link to it.
const sourcesBody = [
    'The evidence behind the numbers and claims in the skill, and how each was verified. The numbers of an **unconfirmed** source are never stated as fact.',
    '',
    ...catalogue.sources.flatMap(s => [
        `## ${s.id}`,
        '',
        `**${s.url ? `[${s.title}](${s.url})` : s.title}**${[s.publisher, s.year].filter(Boolean).length ? ` — ${[s.publisher, s.year].filter(Boolean).join(', ')}` : ''}`,
        '',
        `- **Status:** ${s.status}${s.verified_on ? ` · **Verified:** ${s.verified_on}` : ''}`,
        ...(s.verified_against ? [`- **Against:** ${s.verified_against}`] : []),
        `- **Backs:** ${s.supports}`,
        '',
    ]),
].join('\n');
writePage('reference/sources', 'Sources', 'Every source, its verification status and what it backs.', sourcesBody);

// Sidebar order.
const meta = (dir, data) => writeFileSync(join(out, dir, 'meta.json'), JSON.stringify(data, null, 2) + '\n');
meta('', { pages: ['index', 'getting-started', 'modes', 'areas', 'stacks', 'reference', 'project'] });
meta('getting-started', { title: 'Getting started', defaultOpen: true, pages: ['install', 'use-in-your-project'] });
meta('modes', { title: 'Modes', pages: ['design', 'refactor'] });
meta('areas', { title: `Areas (${catalogue.areas.length})`, pages: areaRows.map(r => r.area) });
meta('stacks', { title: 'Stack packs', pages: ['index', ...catalogue.stacks.map(s => s.id)] });
meta('reference', {
    title: 'Reference',
    pages: ['skill', 'finding-format', 'severity-and-scoring', 'codebase-recon', 'report-template', 'laws-and-numbers', 'patterns', 'native-probes', 'sources'],
});
meta('project', { title: 'Project', pages: ['stability', 'changelog'] });

// Introduction, written for people (the README is written for GitHub).
writePage(
    'index',
    'Introduction',
    'Principal-level UX expertise for AI agents: design, refactor and audit with evidence, consistent severity and a launch verdict.',
    `ux-expert gives any AI agent the working method of a principal UX engineer. It works from the user's goal, backs every finding with evidence and a source, scores severity the same way every time, and ends with a launch verdict: Go, Conditional Go or No-Go.

## What you can ask

| You say | Mode | You get |
|---|---|---|
| "Write the UX acceptance criteria for these stories" | [Design](/docs/modes/design) | UX requirements, acceptance criteria and a Definition of Done per story |
| "Run a full UX audit of this app" | Full audit | A prioritized report across the areas that apply |
| "Plan how to fix these findings safely" | [Refactor](/docs/modes/refactor) | Sequenced stories, each with a regression guard |
| "Are we ready to launch?" | Launch gate | A Go, Conditional Go or No-Go verdict with conditions |
| "Review the UX of this pull request" | Change review | Findings and regressions in the changed UI |

## What it contains

- **${catalogue.areas.length} areas and ${catalogue.criteria.length} criteria** with permanent IDs, browsable in the [criteria explorer](/criteria).
- **${catalogue.stacks.length} stack packs** for [Next.js, shadcn/ui, Radix and Playwright](/docs/stacks), verified against each project's repository.
- **${catalogue.probes.length} native probes** for [SwiftUI, Compose, Flutter and React Native](/docs/reference/native-probes).
- **${catalogue.patterns.length} proven patterns** from [public design systems](/docs/reference/patterns), and every number traced to a [source](/docs/reference/sources).

Start with [Install](/docs/getting-started/install), then [Use it in your project](/docs/getting-started/use-in-your-project).
`,
);

// The criteria explorer and the home page read the catalogue directly; each page
// links "edit on GitHub" to its real source file.
mkdirSync(join(site, 'generated'), { recursive: true });
const sourceOf = Object.fromEntries([...pages].map(([src, p]) => [src.endsWith('references/stacks.md') ? 'stacks/index' : p.slug, src]));
sourceOf['reference/sources'] = 'skills/ux-expert/criteria/sources.yaml';
writeFileSync(join(site, 'generated', 'sources.json'), JSON.stringify(sourceOf, null, 2) + '\n');
copyFileSync(join(skill, 'criteria', 'catalogue.json'), join(site, 'generated', 'catalogue.json'));

const count = readdirSync(out, { recursive: true }).filter(f => String(f).endsWith('.md')).length;
console.log(`sync-content: ${count} pages from the repository`);
