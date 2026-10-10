// The documentation site (website/, built with `npm run build`) is checked with the
// skill's own runtime checks: a UX package should pass its own audit.
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createReadStream, existsSync, mkdtempSync, readFileSync, statSync } from 'node:fs';
import { createServer } from 'node:http';
import { tmpdir } from 'node:os';
import { dirname, extname, join, normalize } from 'node:path';
import { fileURLToPath } from 'node:url';
import { after, before, describe, it } from 'node:test';

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, '..');
const repo = join(root, '..', '..');
const out = join(repo, 'website', 'out');
const script = join(repo, 'skills', 'ux-expert', 'scripts', 'ux_check.mjs');
const PAGES = ['', 'criteria/', 'docs/', 'docs/areas/forms-input/', 'docs/stacks/playwright/', 'docs/getting-started/install/', 'docs/reference/sources/'];
const run = promisify(execFile);
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.json': 'application/json', '.svg': 'image/svg+xml', '.png': 'image/png', '.woff2': 'font/woff2', '.txt': 'text/plain' };

/** Serves the static export the way GitHub Pages does: directories serve index.html. */
function serve(dir) {
  return createServer((req, res) => {
    let path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname)).replace(/^(\.\.[/\\])+/, '');
    let file = join(dir, path);
    if (existsSync(file) && statSync(file).isDirectory()) file = join(file, 'index.html');
    if (!existsSync(file) && existsSync(`${file}.html`)) file = `${file}.html`;
    if (!existsSync(file)) {
      res.writeHead(404).end('not found');
      return;
    }
    res.writeHead(200, { 'content-type': TYPES[extname(file)] ?? 'application/octet-stream' });
    createReadStream(file).pipe(res);
  });
}

describe('documentation site passes ux_check', () => {
  const work = mkdtempSync(join(tmpdir(), 'ux-site-'));
  const reports = {};
  let server;

  before(async () => {
    assert.ok(existsSync(join(out, 'index.html')), 'build the site first: (cd website && npm ci && npm run build)');
    server = serve(out).listen(0);
    await new Promise(resolve => server.once('listening', resolve));
    const base = `http://127.0.0.1:${server.address().port}/`;
    for (const page of PAGES) {
      const dir = join(work, page.replace(/\//g, '_') || 'home');
      // Async: the static server runs in this process and must keep answering.
      await run(process.execPath, [script, base + page, '--out', dir, '--widths', '320,375,1280'], { cwd: root });
      reports[page] = JSON.parse(readFileSync(join(dir, 'report.json'), 'utf8'));
    }
  });

  after(() => server?.close());

  for (const page of PAGES) {
    it(`/${page}: no axe violations, small targets or hidden focus; reflows at 320 px; zoom allowed`, () => {
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
