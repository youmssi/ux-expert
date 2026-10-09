// Copies the skill (the single source of truth) and the license files into the
// package, so the published server works without the repository.
import { cpSync, existsSync, rmSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const packageRoot = join(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = join(packageRoot, '..');
const source = join(repoRoot, 'skills', 'ux-expert');
if (!existsSync(join(source, 'SKILL.md'))) {
    console.error(`copy-skill: no skill at ${source}`);
    process.exit(1);
}
const target = join(packageRoot, 'skill');
rmSync(target, { recursive: true, force: true });
cpSync(source, target, { recursive: true });
for (const file of ['LICENSE', 'LICENSE-CONTENT']) {
    cpSync(join(repoRoot, file), join(packageRoot, file));
}
console.error(`copy-skill: copied ${source} to ${target}`);
