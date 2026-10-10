// Checks the built site (run `npm run build` first): every internal link resolves,
// and every area, stack pack and criterion from the catalogue has its page.
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, it } from 'node:test';

const site = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(site, 'out');
const catalogue = JSON.parse(readFileSync(join(site, 'generated', 'catalogue.json'), 'utf8'));
const htmlFiles = readdirSync(out, { recursive: true }).map(String).filter(f => f.endsWith('.html'));
const read = path => readFileSync(join(out, path), 'utf8');

/** A site URL path → the file the static host serves for it. */
function fileFor(path) {
  const clean = decodeURIComponent(path.split(/[?#]/)[0]);
  if (clean.endsWith('/')) return join(out, clean, 'index.html');
  return existsSync(join(out, clean)) ? join(out, clean) : join(out, `${clean}.html`);
}

describe('built site', () => {
  it('was built (run npm run build)', () => assert.ok(existsSync(join(out, 'index.html'))));

  it('has a page for every area and stack pack, and llms.txt for agents', () => {
    for (const a of catalogue.areas) assert.ok(existsSync(fileFor(`/docs/areas/${a.area}/`)), a.area);
    for (const s of catalogue.stacks) assert.ok(existsSync(fileFor(`/docs/stacks/${s.id}/`)), s.id);
    assert.ok(existsSync(join(out, 'llms.txt')));
  });

  it('lists every criterion in the explorer with its ID as an anchor', () => {
    const html = read('criteria/index.html');
    for (const c of catalogue.criteria) assert.ok(html.includes(`id="${c.id}"`), c.id);
  });

  it('every internal link resolves to a built page or file', () => {
    const broken = new Set();
    for (const file of htmlFiles) {
      for (const [, href] of read(file).matchAll(/href="(\/[^"]*)"/g)) {
        if (href.startsWith('//')) continue;
        if (!existsSync(fileFor(href))) broken.add(`${file} → ${href}`);
      }
    }
    assert.deepEqual([...broken].slice(0, 20), []);
  });

  it('no docs page links to a Markdown source on the site', () => {
    const md = htmlFiles.flatMap(f => [...read(f).matchAll(/href="(\/[^"]*\.md)"/g)].map(m => `${f} → ${m[1]}`));
    assert.deepEqual(md.filter(l => !l.includes('/llms.mdx/')), []);
  });
});
