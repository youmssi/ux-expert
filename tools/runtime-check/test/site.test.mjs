// The documentation site is checked with the skill's own runtime checks:
// a UX package should pass its own audit.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { before, describe, it } from 'node:test';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const repo = join(root, '..', '..');
const script = join(repo, 'skills', 'ux-expert', 'scripts', 'ux_check.mjs');
const PAGES = ['index', 'criteria', 'sources', 'areas/forms-input', 'install', 'stacks/nextjs'];

describe('documentation site passes ux_check', () => {
    const work = mkdtempSync(join(tmpdir(), 'ux-site-'));
    const site = join(work, 'site');
    const reports = {};

    before(() => {
        execFileSync(process.env.PYTHON ?? 'python3', [join(repo, 'scripts', 'build_site.py'), site], { stdio: 'pipe' });
        for (const page of PAGES) {
            const out = join(work, page.replace('/', '-'));
            execFileSync(process.execPath, [script, pathToFileURL(join(site, `${page}.html`)).href, '--out', out, '--widths', '320,375,1280'], {
                cwd: root,
                stdio: 'pipe'
            });
            reports[page] = JSON.parse(readFileSync(join(out, 'report.json'), 'utf8'));
        }
    });

    for (const page of PAGES) {
        it(`${page}: no axe violations, small targets or hidden focus; reflows at 320 px; zoom allowed`, () => {
            const report = reports[page];
            for (const run of report.runs) {
                assert.deepEqual(run.axe_violations.map(v => `${v.rule} ${v.targets.join(', ')}`), [], `${run.width} ${run.scheme}`);
                assert.deepEqual(run.small_targets, [], `${run.width} ${run.scheme}`);
                assert.deepEqual(run.focus_without_indicator ?? [], [], `${run.width} ${run.scheme}`);
            }
            assert.equal(report.reflow.horizontal_overflow, false);
            assert.equal(report.zoom_blocked, false);
        });
    }
});
