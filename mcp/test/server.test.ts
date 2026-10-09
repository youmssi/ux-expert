import assert from 'node:assert/strict';
import { existsSync } from 'node:fs';
import { after, before, describe, it } from 'node:test';

import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { StdioClientTransport } from '@modelcontextprotocol/client/stdio';
import { createMcpHandler } from '@modelcontextprotocol/server';

import { createServer, SKILL_URI } from '../src/server.js';
import { findSkillDir } from '../src/skill.js';

const skillDir = findSkillDir();

function textOf(result: { content?: unknown }): string {
    const [first] = (result.content ?? []) as { type: string; text?: string }[];
    return first?.text ?? '';
}

describe('ux-expert MCP server (in-process, 2026-07-28)', () => {
    const handler = createMcpHandler(() => createServer(skillDir));
    const client = new Client({ name: 'test', version: '1.0.0' }, { versionNegotiation: { mode: 'auto' } });

    before(async () => {
        await client.connect(
            new StreamableHTTPClientTransport(new URL('http://test.local/mcp'), {
                fetch: (url, init) => handler.fetch(new Request(url, init))
            })
        );
    });

    after(async () => {
        await client.close();
        await handler.close();
    });

    it('negotiates the 2026-07-28 protocol revision', () => {
        assert.equal(client.getNegotiatedProtocolVersion(), '2026-07-28');
    });

    it('exposes every skill file as a resource', async () => {
        const { resources } = await client.listResources();
        const uris = resources.map(r => r.uri);
        for (const path of ['SKILL.md', 'references/areas/forms-input.md', 'references/sources.md', 'criteria/catalogue.json']) {
            assert.ok(uris.includes(`${SKILL_URI}${path}`), path);
        }
        const { contents } = await client.readResource({ uri: `${SKILL_URI}SKILL.md` });
        assert.match((contents[0] as { text: string }).text, /^---\nname: ux-expert/);
    });

    it('offers the design, audit and refactor prompts', async () => {
        const { prompts } = await client.listPrompts();
        assert.deepEqual(prompts.map(p => p.name).sort(), ['ux-audit', 'ux-design', 'ux-refactor']);
        const design = await client.getPrompt({ name: 'ux-design', arguments: { product_type: 'web-app', brief: 'Sign-up story' } });
        const message = (design.messages[0]?.content as { text: string }).text;
        assert.match(message, /Design mode for a web-app/);
        assert.match(message, /# Design mode: UX requirements before the backlog/);
        assert.match(message, /--- Brief ---\n\nSign-up story$/);
    });

    it('marks every tool read-only', async () => {
        const { tools } = await client.listTools();
        assert.deepEqual(tools.map(t => t.name).sort(), ['contrast_ratio', 'get_criterion', 'launch_gate', 'list_criteria', 'read_area', 'score_finding']);
        assert.ok(tools.every(t => t.annotations?.readOnlyHint === true && t.annotations?.destructiveHint === false));
    });

    it('lists criteria with structured content', async () => {
        const result = await client.callTool({ name: 'list_criteria', arguments: { product_type: 'web-app', phase: 'design', areas: ['forms-input'] } });
        const structured = result.structuredContent as { count: number; criteria: { id: string }[] };
        assert.ok(structured.count > 10);
        assert.ok(structured.criteria.every(c => c.id.startsWith('FORM-')));
        assert.match(textOf(result), /^\d+ criteria for web-app, phase design:/);
    });

    it('returns a criterion with its sources, and an error for an unknown one', async () => {
        const found = await client.callTool({ name: 'get_criterion', arguments: { id: 'form-09' } });
        const criterion = JSON.parse(textOf(found)) as { id: string; sources: { id: string }[]; area_file: string };
        assert.equal(criterion.id, 'FORM-09');
        assert.deepEqual(criterion.sources.map(s => s.id), ['govuk-validation', 'cms-validation']);
        assert.equal(criterion.area_file, `${SKILL_URI}references/areas/forms-input.md`);
        const missing = await client.callTool({ name: 'get_criterion', arguments: { id: 'FORM-99' } });
        assert.equal(missing.isError, true);
    });

    it('scores findings, decides the gate and computes contrast', async () => {
        const scored = await client.callTool({ name: 'score_finding', arguments: { severity: 'S3', reach: 'R2', confidence: 'High', effort: 'S' } });
        assert.deepEqual(scored.structuredContent, { priority: 'P1', base_priority: 'P1', validate_first: false, quick_win: true });
        const gate = await client.callTool({
            name: 'launch_gate',
            arguments: { open_p0: 0, unowned_p1: 1, critical_criteria_not_verified: 0, critical_flow_unverified: false }
        });
        assert.equal((gate.structuredContent as { verdict: string }).verdict, 'Conditional Go');
        const contrast = await client.callTool({ name: 'contrast_ratio', arguments: { foreground: '#9CA3AF', background: '#FFFFFF' } });
        assert.equal((contrast.structuredContent as { ratio: number }).ratio, 2.54);
        const invalid = await client.callTool({ name: 'contrast_ratio', arguments: { foreground: 'grey', background: '#fff' } });
        assert.equal(invalid.isError, true);
    });

    it('rejects invalid tool arguments before running the tool', async () => {
        const result = await client.callTool({ name: 'score_finding', arguments: { severity: 'S9', reach: 'R1', confidence: 'High' } });
        assert.equal(result.isError, true);
    });
});

describe('ux-expert MCP server (stdio binary)', { skip: !existsSync('dist/index.js') && 'run npm run build first' }, () => {
    it('serves over stdio from the built package', async () => {
        const client = new Client({ name: 'test', version: '1.0.0' });
        await client.connect(new StdioClientTransport({ command: process.execPath, args: ['dist/index.js'] }));
        try {
            const { tools } = await client.listTools();
            assert.equal(tools.length, 6);
        } finally {
            await client.close();
        }
    });
});
