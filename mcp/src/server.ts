import { readFileSync } from 'node:fs';

import { McpServer } from '@modelcontextprotocol/server';
import * as z from 'zod/v4';

import { contrastRatio, findPatterns, launchGate, scoreFinding, selectCriteria } from './logic.js';
import { listSkillFiles, loadCatalogue, mimeType, readSkillFile } from './skill.js';
import type { Catalogue, Criterion, ProductType } from './skill.js';

export const SKILL_URI = 'skill://ux-expert/';
const VERSION = (JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8')) as { version: string }).version;

const INSTRUCTIONS = `ux-expert gives you a principal UX engineer's method.
- Design (before building): use the "ux-design" prompt, or read ${SKILL_URI}references/design-mode.md.
- Audit or review: use the "ux-audit" prompt; read ${SKILL_URI}SKILL.md first.
- Refactor plan from audit findings: use the "ux-refactor" prompt.
Tools: list_criteria and get_criterion query the 565 criteria; read_area returns an area's procedure;
find_patterns returns proven patterns from public design systems to cite in recommendations;
score_finding and launch_gate apply the scoring rules; contrast_ratio computes WCAG contrast.
Every finding cites evidence; never state numbers from an "unconfirmed" source as fact.`;

const readOnly = { readOnlyHint: true, destructiveHint: false, idempotentHint: true, openWorldHint: false };

function criterionLine(c: Criterion): string {
    const note = c.severity_note ? ` (${c.severity_note})` : '';
    return `- **${c.id}** ${c.name}. Fail: ${c.fail_signal}. Severity ${c.severity}${note}.`;
}

function text(value: string) {
    return { type: 'text' as const, text: value };
}

/** Builds one server instance; the skill directory is read once per instance. */
export function createServer(skillDir: string): McpServer {
    const catalogue: Catalogue = loadCatalogue(skillDir);
    const productTypes = catalogue.product_types as [ProductType, ...ProductType[]];
    const areaNames = catalogue.areas.map(a => a.area) as [string, ...string[]];
    const read = (path: string) => readSkillFile(skillDir, path);

    const server = new McpServer({ name: 'ux-expert', version: VERSION }, { instructions: INSTRUCTIONS });

    for (const path of listSkillFiles(skillDir)) {
        server.registerResource(
            path,
            `${SKILL_URI}${path}`,
            { title: `ux-expert: ${path}`, description: `File ${path} of the ux-expert skill`, mimeType: mimeType(path) },
            async uri => ({ contents: [{ uri: uri.href, mimeType: mimeType(path), text: read(path) }] })
        );
    }

    server.registerPrompt(
        'ux-design',
        {
            title: 'UX requirements before building',
            description: 'Turn a brief or user stories into UX requirements and testable acceptance criteria tagged with criterion IDs.',
            argsSchema: z.object({
                product_type: z.enum(productTypes).describe('The kind of product'),
                brief: z.string().describe('The brief, epics or draft stories, in any format')
            })
        },
        ({ product_type, brief }) => ({
            messages: [
                {
                    role: 'user' as const,
                    content: text(
                        [
                            `Use the ux-expert skill in Design mode for a ${product_type}. Follow the design-mode procedure below exactly.`,
                            `Use the list_criteria tool (product_type "${product_type}", phase "design") to select criteria, and fill the story template for each story.`,
                            '--- SKILL.md ---', read('SKILL.md'),
                            '--- references/design-mode.md ---', read('references/design-mode.md'),
                            '--- assets/story-ux.md ---', read('assets/story-ux.md'),
                            '--- Brief ---', brief
                        ].join('\n\n')
                    )
                }
            ]
        })
    );

    server.registerPrompt(
        'ux-audit',
        {
            title: 'UX audit',
            description: 'Audit a product, flow, area or change with evidence, consistent severity and, for a pre-launch gate, a Go/No-Go verdict.',
            argsSchema: z.object({
                mode: z.enum(['full-audit', 'pre-launch-gate', 'scoped-audit', 'area-deep-dive', 'change-review']).describe('Audit mode'),
                scope: z.string().optional().describe('What to audit: repository path, URL, flow, area or diff')
            })
        },
        ({ mode, scope }) => ({
            messages: [
                {
                    role: 'user' as const,
                    content: text(
                        [
                            `Use the ux-expert skill in "${mode}" mode${scope ? ` on: ${scope}` : ''}. Follow SKILL.md below.`,
                            `Read area procedures with the read_area tool or the ${SKILL_URI}references/areas/ resources, score findings with score_finding, and decide with launch_gate.`,
                            '--- SKILL.md ---', read('SKILL.md'),
                            '--- references/finding-format.md ---', read('references/finding-format.md'),
                            '--- references/severity-and-scoring.md ---', read('references/severity-and-scoring.md')
                        ].join('\n\n')
                    )
                }
            ]
        })
    );

    server.registerPrompt(
        'ux-refactor',
        {
            title: 'UX refactor plan',
            description: 'Turn audit findings into a sequenced plan of shippable, guarded stories.',
            argsSchema: z.object({ findings: z.string().describe('The audit report or the list of findings') })
        },
        ({ findings }) => ({
            messages: [
                {
                    role: 'user' as const,
                    content: text(
                        [
                            'Use the ux-expert skill in Refactor mode. Follow the refactor-mode procedure below exactly.',
                            '--- references/refactor-mode.md ---', read('references/refactor-mode.md'),
                            '--- Findings ---', findings
                        ].join('\n\n')
                    )
                }
            ]
        })
    );

    server.registerTool(
        'list_criteria',
        {
            title: 'List UX criteria',
            description: 'List the ux-expert criteria that apply to a product type, optionally for one phase (design or build) and some areas.',
            inputSchema: z.object({
                product_type: z.enum(productTypes),
                phase: z.enum(['design', 'build']).optional().describe('design: specify in stories; build: verify in code. Omit for all (audit).'),
                areas: z.array(z.enum(areaNames)).optional().describe('Limit to these areas')
            }),
            outputSchema: z.object({ count: z.number(), criteria: z.array(z.record(z.string(), z.unknown())) }),
            annotations: readOnly
        },
        async ({ product_type, phase, areas }) => {
            const criteria = selectCriteria(catalogue, product_type, phase, areas ?? []);
            const body = criteria.map(criterionLine).join('\n');
            return {
                content: [text(`${criteria.length} criteria for ${product_type}${phase ? `, phase ${phase}` : ''}:\n${body}`)],
                structuredContent: { count: criteria.length, criteria: criteria as unknown as Record<string, unknown>[] }
            };
        }
    );

    server.registerTool(
        'get_criterion',
        {
            title: 'Get a UX criterion',
            description: 'Get one criterion by ID (e.g. FORM-09), with its sources and the area file that explains it.',
            inputSchema: z.object({ id: z.string().describe('Criterion ID such as FORM-09') }),
            annotations: readOnly
        },
        async ({ id }) => {
            const wanted = id.trim().toUpperCase();
            const criterion = catalogue.criteria.find(c => c.id === wanted);
            if (!criterion) {
                const retired = catalogue.retired_ids.includes(wanted) ? ' It is retired.' : '';
                return { content: [text(`No active criterion ${wanted}.${retired} Use list_criteria to browse.`)], isError: true };
            }
            const sources = catalogue.sources.filter(s => criterion.sources?.includes(s.id));
            const area = catalogue.areas.find(a => a.area === criterion.area);
            const result = { ...criterion, sources, area_file: `${SKILL_URI}${area?.file ?? ''}` };
            return { content: [text(JSON.stringify(result, null, 1))] };
        }
    );

    server.registerTool(
        'read_area',
        {
            title: 'Read a UX area',
            description: 'Return an area reference: expert mindset, procedure, criteria, code probes, gotchas and output format.',
            inputSchema: z.object({ area: z.enum(areaNames) }),
            annotations: readOnly
        },
        async ({ area }) => ({ content: [text(read(`references/areas/${area}.md`))] })
    );

    server.registerTool(
        'find_patterns',
        {
            title: 'Find proven UX patterns',
            description: 'Find patterns from public design systems (GOV.UK, GitHub Primer, Shopify Polaris, IBM Carbon) that satisfy a criterion or match words, to cite in a recommendation.',
            inputSchema: z.object({
                criterion_id: z.string().optional().describe('Criterion ID such as FORM-09'),
                query: z.string().optional().describe('Words that must all appear in the pattern, e.g. "empty state"')
            }),
            annotations: readOnly
        },
        async ({ criterion_id, query }) => {
            const patterns = findPatterns(catalogue, criterion_id, query);
            if (patterns.length === 0) {
                return { content: [text('No matching pattern. Try fewer words, or list_criteria to find related criteria.')] };
            }
            const lines = patterns.map(p => `- **${p.id}** ${p.name}: ${p.rule} (${p.criteria.join(', ')}) ${p.source}`);
            return { content: [text(lines.join('\n'))] };
        }
    );

    server.registerTool(
        'score_finding',
        {
            title: 'Score a UX finding',
            description: 'Compute a finding priority (P0–P3) from severity, reach and confidence, and whether it is a quick win.',
            inputSchema: z.object({
                severity: z.enum(['S0', 'S1', 'S2', 'S3', 'S4']),
                reach: z.enum(['R1', 'R2', 'R3']),
                confidence: z.enum(['High', 'Medium', 'Low']),
                effort: z.enum(['XS', 'S', 'M', 'L', 'XL']).optional()
            }),
            outputSchema: z.object({
                priority: z.string(),
                base_priority: z.string(),
                validate_first: z.boolean(),
                quick_win: z.boolean().nullable()
            }),
            annotations: readOnly
        },
        async ({ severity, reach, confidence, effort }) => {
            const scored = scoreFinding(catalogue.scoring, severity, reach, confidence, effort);
            const flag = scored.validate_first ? ' (validate first)' : '';
            return { content: [text(`${scored.priority}${flag}`)], structuredContent: { ...scored } };
        }
    );

    server.registerTool(
        'launch_gate',
        {
            title: 'Launch gate verdict',
            description: 'Decide Go, Conditional Go or No-Go from the audit counts, using the skill launch-gate rules.',
            inputSchema: z.object({
                open_p0: z.number().int().min(0).describe('Open P0 findings'),
                unowned_p1: z.number().int().min(0).describe('P1 findings without an owner and a date'),
                critical_criteria_not_verified: z.number().int().min(0).describe('Not verified rows for FLOW, STATE, A11Y or TRUST on critical flows'),
                critical_flow_unverified: z.boolean().describe('A critical flow was never verified end to end')
            }),
            outputSchema: z.object({ verdict: z.string(), rule: z.string(), triggered_by: z.array(z.string()) }),
            annotations: readOnly
        },
        async facts => {
            const { verdict, rule, triggered_by } = launchGate(catalogue.scoring, facts);
            return { content: [text(`${verdict}: ${rule}`)], structuredContent: { verdict, rule, triggered_by } };
        }
    );

    server.registerTool(
        'contrast_ratio',
        {
            title: 'WCAG contrast ratio',
            description: 'Compute the WCAG 2.2 contrast ratio of two #rgb/#rrggbb colors and whether it passes for text and UI components.',
            inputSchema: z.object({
                foreground: z.string().describe('Text or UI color, e.g. #6B7280'),
                background: z.string().describe('Background color, e.g. #FFFFFF'),
                font_size_px: z.number().positive().optional().describe('Rendered font size in CSS px, to decide large text'),
                bold: z.boolean().optional()
            }),
            outputSchema: z.object({
                ratio: z.number(),
                large_text: z.boolean().nullable(),
                passes: z.object({ text_aa: z.boolean(), text_aaa: z.boolean(), non_text_aa: z.boolean() })
            }),
            annotations: readOnly
        },
        async ({ foreground, background, font_size_px, bold }) => {
            try {
                const result = contrastRatio(foreground, background, font_size_px, bold ?? false);
                return { content: [text(`${result.ratio}:1`)], structuredContent: { ...result } };
            } catch (error) {
                return { content: [text((error as Error).message)], isError: true };
            }
        }
    );

    return server;
}
