import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { contrastRatio, findPatterns, launchGate, scoreFinding, selectCriteria } from '../src/logic.js';
import { findSkillDir, loadCatalogue } from '../src/skill.js';

const catalogue = loadCatalogue(findSkillDir());

describe('selectCriteria', () => {
    it('keeps only design-phase criteria for the product', () => {
        const ids = new Set(selectCriteria(catalogue, 'web-app', 'design').map(c => c.id));
        assert.ok(ids.has('FORM-01'));
        assert.ok(!ids.has('FORM-06'), 'autocomplete tokens are build only');
    });

    it('leaves out criteria narrowed to other products', () => {
        assert.ok(!selectCriteria(catalogue, 'web-app').some(c => c.id === 'RESP-12'));
        assert.ok(selectCriteria(catalogue, 'mobile').some(c => c.id === 'RESP-12'));
    });

    it('matches the Python selector count for web-app design', () => {
        assert.equal(selectCriteria(catalogue, 'web-app', 'design').length, 353);
    });

    it('rejects an unknown area and lists the known ones', () => {
        assert.throws(() => selectCriteria(catalogue, 'web-app', undefined, ['forms']), /unknown area\(s\): forms; known: accessibility/);
    });
});

describe('findPatterns', () => {
    it('combines the criterion filter and every query word', () => {
        assert.deepEqual(findPatterns(catalogue, 'FORM-09').map(p => p.id), ['govuk-validation']);
        assert.ok(findPatterns(catalogue, undefined, 'saving forms').every(p => p.id === 'primer-saving'));
        assert.equal(findPatterns(catalogue, 'FORM-09', 'empty').length, 0);
    });
});

describe('scoreFinding', () => {
    it('applies the priority matrix', () => {
        assert.equal(scoreFinding(catalogue.scoring, 'S3', 'R3', 'High').priority, 'P0');
        assert.equal(scoreFinding(catalogue.scoring, 'S2', 'R1', 'Medium').priority, 'P3');
    });

    it('drops one level for low confidence and flags validation', () => {
        const scored = scoreFinding(catalogue.scoring, 'S4', 'R3', 'Low');
        assert.deepEqual([scored.base_priority, scored.priority, scored.validate_first], ['P0', 'P1', true]);
    });

    it('never drops below P3', () => {
        assert.equal(scoreFinding(catalogue.scoring, 'S0', 'R1', 'Low').priority, 'P3');
    });

    it('marks quick wins only when effort is given', () => {
        assert.equal(scoreFinding(catalogue.scoring, 'S2', 'R2', 'High', 'XS').quick_win, true);
        assert.equal(scoreFinding(catalogue.scoring, 'S2', 'R2', 'High', 'L').quick_win, false);
        assert.equal(scoreFinding(catalogue.scoring, 'S2', 'R2', 'High').quick_win, null);
    });
});

describe('launchGate', () => {
    const clean = { open_p0: 0, unowned_p1: 0, critical_criteria_not_verified: 0, critical_flow_unverified: false };

    it('is Go when nothing blocks', () => {
        assert.equal(launchGate(catalogue.scoring, clean).verdict, 'Go');
    });

    it('is No-Go with an open P0, even when other conditions also hold', () => {
        const gate = launchGate(catalogue.scoring, { ...clean, open_p0: 1, unowned_p1: 2 });
        assert.deepEqual([gate.verdict, gate.triggered_by], ['No-Go', ['open_p0']]);
    });

    it('is No-Go when a critical flow was never verified', () => {
        assert.equal(launchGate(catalogue.scoring, { ...clean, critical_flow_unverified: true }).verdict, 'No-Go');
    });

    it('is Conditional Go with unowned P1s or unverified critical criteria', () => {
        assert.equal(launchGate(catalogue.scoring, { ...clean, unowned_p1: 1 }).verdict, 'Conditional Go');
        assert.equal(launchGate(catalogue.scoring, { ...clean, critical_criteria_not_verified: 3 }).verdict, 'Conditional Go');
    });
});

describe('contrastRatio', () => {
    it('matches known WCAG values', () => {
        assert.equal(contrastRatio('#000', '#fff').ratio, 21);
        assert.equal(contrastRatio('#6B7280', '#FFFFFF').ratio, 4.83);
        assert.equal(contrastRatio('#9CA3AF', '#FFFFFF').ratio, 2.54);
    });

    it('uses the large-text threshold at 24 px, or 18.66 px bold', () => {
        const grey = '#959595'; // about 3:1 on white
        assert.equal(contrastRatio(grey, '#fff', 16).passes.text_aa, false);
        assert.equal(contrastRatio(grey, '#fff', 24).passes.text_aa, true);
        assert.equal(contrastRatio(grey, '#fff', 19, true).passes.text_aa, true);
    });

    it('rejects colors it cannot compute', () => {
        assert.throws(() => contrastRatio('rgba(0,0,0,.5)', '#fff'), /composite alpha colors/);
    });
});
