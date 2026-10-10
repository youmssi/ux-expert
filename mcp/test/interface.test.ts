// The public MCP interface (tool names and input fields, prompt names and arguments,
// resource URI scheme) is a stability promise (docs/stability.md). This test fails
// on any change to it; after an intended, additive change run
// `UPDATE_INTERFACE=1 npm test` and commit interface.json.
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync } from 'node:fs';
import { after, before, describe, it } from 'node:test';

import { Client, StreamableHTTPClientTransport } from '@modelcontextprotocol/client';
import { createMcpHandler } from '@modelcontextprotocol/server';

import { createServer, SKILL_URI } from '../src/server.js';
import { findSkillDir } from '../src/skill.js';

const snapshot = new URL('../interface.json', import.meta.url);

describe('public MCP interface', () => {
    const handler = createMcpHandler(() => createServer(findSkillDir()));
    const client = new Client({ name: 'interface-test', version: '1.0.0' }, { versionNegotiation: { mode: 'auto' } });

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

    it('matches interface.json', async () => {
        const { tools } = await client.listTools();
        const { prompts } = await client.listPrompts();
        const current = {
            resource_uri_prefix: SKILL_URI,
            tools: Object.fromEntries(
                tools
                    .map(t => {
                        const schema = t.inputSchema as { properties?: Record<string, unknown>; required?: string[] };
                        return [t.name, { inputs: Object.keys(schema.properties ?? {}).sort(), required: [...(schema.required ?? [])].sort() }];
                    })
                    .sort(([a], [b]) => String(a).localeCompare(String(b)))
            ),
            prompts: Object.fromEntries(
                prompts
                    .map(p => [p.name, (p.arguments ?? []).map(a => `${a.name}${a.required ? '' : '?'}`).sort()])
                    .sort(([a], [b]) => String(a).localeCompare(String(b)))
            )
        };
        if (process.env.UPDATE_INTERFACE === '1') {
            writeFileSync(snapshot, JSON.stringify(current, null, 2) + '\n');
        }
        assert.deepEqual(current, JSON.parse(readFileSync(snapshot, 'utf8')));
    });
});
