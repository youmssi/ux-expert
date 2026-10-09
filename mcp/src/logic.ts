import type { Catalogue, Criterion, GateFact, GateRule, Phase, ProductType, Scoring } from './skill.js';

export function selectCriteria(catalogue: Catalogue, product: ProductType, phase?: Phase, areas: string[] = []): Criterion[] {
    const known = new Set(catalogue.areas.map(a => a.area));
    const unknown = areas.filter(a => !known.has(a));
    if (unknown.length > 0) {
        throw new Error(`unknown area(s): ${unknown.join(', ')}; known: ${[...known].sort().join(', ')}`);
    }
    return catalogue.criteria.filter(
        c => c.applies_to.includes(product) && (!phase || c.phases.includes(phase)) && (areas.length === 0 || areas.includes(c.area))
    );
}

const PRIORITIES = ['P0', 'P1', 'P2', 'P3'];

export interface ScoredFinding {
    priority: string;
    base_priority: string;
    validate_first: boolean;
    quick_win: boolean | null;
}

/** Applies the priority matrix, then the low-confidence drop, from criteria/scoring.yaml. */
export function scoreFinding(scoring: Scoring, severity: string, reach: string, confidence: string, effort?: string): ScoredFinding {
    const base = scoring.priority_matrix[severity]?.[reach];
    if (!base) {
        throw new Error(`no priority for severity ${severity} and reach ${reach}`);
    }
    const validateFirst = confidence === 'Low';
    const drop = validateFirst ? scoring.low_confidence_drop : 0;
    const priority = PRIORITIES[Math.min(PRIORITIES.indexOf(base) + drop, PRIORITIES.length - 1)] ?? base;
    const quickWin = effort ? scoring.quick_win.priorities.includes(priority) && scoring.quick_win.efforts.includes(effort) : null;
    return { priority, base_priority: base, validate_first: validateFirst, quick_win: quickWin };
}

export type GateFacts = Record<GateFact, number | boolean>;

/** The first launch-gate rule with a true condition applies; the last rule is the default. */
export function launchGate(scoring: Scoring, facts: GateFacts): GateRule & { triggered_by: GateFact[] } {
    for (const rule of scoring.launch_gate) {
        const triggered = rule.when_any.filter(fact => Boolean(facts[fact]));
        if (rule.when_any.length === 0 || triggered.length > 0) {
            return { ...rule, triggered_by: triggered };
        }
    }
    throw new Error('launch_gate has no default rule');
}

function parseHex(color: string): [number, number, number] {
    const hex = color.trim().replace(/^#/, '');
    const full = hex.length === 3 ? [...hex].map(c => c + c).join('') : hex;
    if (!/^[0-9a-fA-F]{6}$/.test(full)) {
        throw new Error(`"${color}" is not a #rgb or #rrggbb color; composite alpha colors over their background first`);
    }
    return [0, 2, 4].map(i => parseInt(full.slice(i, i + 2), 16) / 255) as [number, number, number];
}

function luminance(color: string): number {
    const [r, g, b] = parseHex(color).map(c => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)) as [number, number, number];
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export interface ContrastResult {
    ratio: number;
    large_text: boolean | null;
    passes: { text_aa: boolean; text_aaa: boolean; non_text_aa: boolean };
}

/**
 * WCAG 2.2 contrast ratio (SC 1.4.3, 1.4.6, 1.4.11). Large text is 24 CSS px,
 * or 18.66 CSS px bold (18 pt / 14 pt bold); without a size, text is judged as
 * normal text.
 */
export function contrastRatio(foreground: string, background: string, fontSizePx?: number, bold = false): ContrastResult {
    const [lighter, darker] = [luminance(foreground), luminance(background)].sort((a, b) => b - a) as [number, number];
    const ratio = Math.round(((lighter + 0.05) / (darker + 0.05)) * 100) / 100;
    const large = fontSizePx === undefined ? null : fontSizePx >= 24 || (bold && fontSizePx >= 18.66);
    return {
        ratio,
        large_text: large,
        passes: {
            text_aa: ratio >= (large ? 3 : 4.5),
            text_aaa: ratio >= (large ? 4.5 : 7),
            non_text_aa: ratio >= 3
        }
    };
}
