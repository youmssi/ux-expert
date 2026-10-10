// Every code recipe in a stack pack must compile against the pinned versions of
// the libraries it uses, so a recipe cannot drift from the real API.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, it } from 'node:test';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const catalogue = JSON.parse(readFileSync(join(root, '..', '..', 'skills', 'ux-expert', 'criteria', 'catalogue.json'), 'utf8'));
const tsc = join(root, 'node_modules', '.bin', process.platform === 'win32' ? 'tsc.cmd' : 'tsc');

// Imports each recipe expects to be in scope, per stack.
const PRELUDE = { playwright: "import { test, expect } from '@playwright/test';" };

describe('stack pack recipes', () => {
    const recipes = catalogue.stacks.flatMap(s => (s.recipes ?? []).map(r => ({ stack: s.id, ...r })));

    it('there are recipes to check', () => assert.ok(recipes.length > 0));

    it('every TypeScript recipe type-checks', () => {
        // Inside the package so its node_modules resolve; removed afterwards.
        const dir = mkdtempSync(join(root, '.recipes-'));
        try {
            recipes.forEach((r, i) => {
                assert.ok(['ts', 'tsx'].includes(r.language), `${r.stack}: ${r.title} is ${r.language}`);
                const lines = r.code.split('\n');
                const imports = lines.filter(l => l.startsWith('import '));
                const body = lines.filter(l => !l.startsWith('import '));
                writeFileSync(join(dir, `recipe-${i}.${r.language}`), [PRELUDE[r.stack] ?? '', ...imports, ...body].join('\n'));
            });
            // Bundler resolution matches how Playwright Test loads TypeScript specs.
            writeFileSync(join(dir, 'tsconfig.json'), JSON.stringify({
                compilerOptions: { target: 'es2022', module: 'esnext', moduleResolution: 'bundler', esModuleInterop: true, strict: true, noEmit: true, skipLibCheck: true, jsx: 'react-jsx' },
                include: ['*.ts', '*.tsx']
            }));
            try {
                execFileSync(tsc, ['-p', join(dir, 'tsconfig.json')], { stdio: 'pipe' });
            } catch (error) {
                const map = recipes.map((r, i) => `recipe-${i}: ${r.stack} — ${r.title}`).join('\n');
                assert.fail(`${error.stdout}\n${map}`);
            }
        } finally {
            rmSync(dir, { recursive: true, force: true });
        }
    });
});
