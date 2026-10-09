import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { dirname, extname, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

export type ProductType = 'web-app' | 'marketing-site' | 'mobile' | 'desktop' | 'cli' | 'sdk-api' | 'ai-feature';
export type Phase = 'design' | 'build';
export type Depth = 'run' | 'light' | 'conditional' | 'n/a';

export interface Criterion {
    id: string;
    area: string;
    name: string;
    check?: string;
    fail_signal: string;
    severity: string;
    severity_note?: string;
    related?: string[];
    sources?: string[];
    phases: Phase[];
    applies_to: ProductType[];
}

export interface Area {
    area: string;
    prefix: string;
    file: string;
    applicability: Record<ProductType, Depth>;
    applicability_note?: string;
}

export interface Source {
    id: string;
    title: string;
    status: 'primary' | 'secondary' | 'unconfirmed' | 'unchecked';
    supports: string;
    publisher?: string;
    year?: number;
    url?: string;
    verified_on?: string;
    verified_against?: string;
}

export interface GateRule {
    verdict: 'No-Go' | 'Conditional Go' | 'Go';
    when_any: GateFact[];
    rule: string;
}

export type GateFact = 'open_p0' | 'critical_flow_unverified' | 'unowned_p1' | 'critical_criteria_not_verified';

export interface Scoring {
    priority_matrix: Record<string, Record<string, string>>;
    low_confidence_drop: number;
    quick_win: { priorities: string[]; efforts: string[] };
    launch_gate: GateRule[];
}

export interface Pattern {
    id: string;
    name: string;
    design_system: string;
    source: string;
    observed_on: string;
    rule: string;
    criteria: string[];
}

export interface DesignSystem {
    id: string;
    name: string;
    repository: string;
    commit: string;
}

export interface Catalogue {
    product_types: ProductType[];
    phases: Phase[];
    areas: Area[];
    criteria: Criterion[];
    retired_ids: string[];
    sources: Source[];
    scoring: Scoring;
    design_systems: DesignSystem[];
    patterns: Pattern[];
}

const TEXT_TYPES: Record<string, string> = {
    '.md': 'text/markdown',
    '.json': 'application/json',
    '.yaml': 'application/yaml',
    '.py': 'text/x-python'
};

/**
 * Locates the skill: copied into the package as `skill/` when published, or
 * `skills/ux-expert/` in the repository during development. Fails fast when
 * neither exists, because the server has nothing to serve without it.
 */
export function findSkillDir(): string {
    const here = dirname(fileURLToPath(import.meta.url));
    const candidates = [join(here, '..', 'skill'), join(here, '..', '..', 'skills', 'ux-expert')];
    const found = candidates.find(dir => existsSync(join(dir, 'SKILL.md')));
    if (!found) {
        throw new Error(`ux-expert skill not found; looked in: ${candidates.join(', ')}`);
    }
    return found;
}

export function loadCatalogue(skillDir: string): Catalogue {
    return JSON.parse(readFileSync(join(skillDir, 'criteria', 'catalogue.json'), 'utf8')) as Catalogue;
}

/** Every text file of the skill, as paths relative to the skill root with forward slashes. */
export function listSkillFiles(skillDir: string): string[] {
    const files: string[] = [];
    const walk = (dir: string) => {
        for (const entry of readdirSync(dir, { withFileTypes: true })) {
            const path = join(dir, entry.name);
            if (entry.isDirectory()) {
                walk(path);
            } else if (extname(entry.name) in TEXT_TYPES) {
                files.push(relative(skillDir, path).split(sep).join('/'));
            }
        }
    };
    walk(skillDir);
    return files.sort();
}

export function mimeType(path: string): string {
    return TEXT_TYPES[extname(path)] ?? 'text/plain';
}

/** Reads a skill file; refuses any path that resolves outside the skill directory. */
export function readSkillFile(skillDir: string, path: string): string {
    const root = resolve(skillDir);
    const target = resolve(root, path);
    if (target !== root && !target.startsWith(root + sep)) {
        throw new Error(`path outside the skill: ${path}`);
    }
    return readFileSync(target, 'utf8');
}
