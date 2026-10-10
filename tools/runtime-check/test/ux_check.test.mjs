import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { mkdtempSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { before, describe, it } from 'node:test';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const script = join(root, '..', '..', 'skills', 'ux-expert', 'scripts', 'ux_check.mjs');
const fixture = pathToFileURL(join(root, 'fixtures', 'page.html')).href;

describe('ux_check.mjs on a fixture with known problems', () => {
    const out = mkdtempSync(join(tmpdir(), 'ux-check-'));
    let report;

    before(() => {
        execFileSync(process.execPath, [script, fixture, '--out', out, '--widths', '375,1280', '--schemes', 'light,dark'], {
            cwd: root,
            stdio: 'pipe'
        });
        report = JSON.parse(readFileSync(join(out, 'report.json'), 'utf8'));
    });

    it('takes one screenshot per width and color scheme', () => {
        assert.equal(report.runs.length, 4);
        for (const run of report.runs) assert.ok(existsSync(join(out, run.screenshot)), run.screenshot);
    });

    it('reports axe violations for contrast and a missing alt text', () => {
        const rules = new Set(report.runs[0].axe_violations.map(v => v.rule));
        assert.ok(rules.has('color-contrast'), [...rules].join(', '));
        assert.ok(rules.has('image-alt'), [...rules].join(', '));
    });

    it('finds the 16 px target and the focus without indicator, but not the focus-visible ring', () => {
        const desktop = report.runs.find(r => r.width === 1280 && r.scheme === 'light');
        assert.ok(desktop.small_targets.some(t => t.size === '16x16'));
        // WCAG 2.5.8 exempts inline links in text, including text in table cells.
        assert.ok(!desktop.small_targets.some(t => t.element.includes('cell-link')));
        assert.ok(!desktop.small_targets.some(t => t.element.includes('heading-link')));
        assert.ok(desktop.focus_without_indicator.some(e => e.includes('no-focus')));
        assert.ok(!desktop.focus_without_indicator.some(e => e.includes('ring')));
    });

    it('detects horizontal overflow at 320 px and blocked zoom', () => {
        assert.equal(report.reflow.horizontal_overflow, true);
        assert.equal(report.zoom_blocked, true);
    });

    it('names the criteria each check informs', () => {
        assert.deepEqual(report.criteria.reflow, ['A11Y-17', 'RESP-02']);
    });
});
