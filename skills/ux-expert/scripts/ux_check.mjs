// Runtime UX checks on a running page: screenshots per width and color scheme,
// axe (WCAG 2.2 A/AA rules), reflow at 320 px, small targets, focus visibility
// and zoom blocking. Every check names the criterion IDs it informs.
//
// Usage (from the project root, where the dependencies are installed):
//   npm i -D playwright @axe-core/playwright && npx playwright install chromium
//   node <skill>/scripts/ux_check.mjs <url> [--out ux-check] [--widths 375,768,1440] [--schemes light,dark]
//
// Set UX_CHECK_CHROMIUM to a Chromium executable to use an installed browser.
// Results are evidence for findings ("measured"), not findings by themselves:
// check each item before reporting it (e.g. a small target may have enough spacing).

import { createRequire } from 'node:module';
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const AXE_TAGS = ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'];
const MIN_TARGET = 24; // WCAG 2.5.8, CSS px
const REFLOW_WIDTH = 320; // WCAG 1.4.10, CSS px
const FOCUS_SAMPLE = 25;

function parseArgs(argv) {
    const args = { url: null, out: 'ux-check', widths: [375, 768, 1440], schemes: ['light', 'dark'] };
    for (let i = 0; i < argv.length; i++) {
        const value = argv[i + 1];
        if (argv[i] === '--out') (args.out = value), i++;
        else if (argv[i] === '--widths') (args.widths = value.split(',').map(Number)), i++;
        else if (argv[i] === '--schemes') (args.schemes = value.split(',')), i++;
        else if (!args.url) args.url = argv[i];
    }
    if (!args.url) {
        throw new Error('usage: node ux_check.mjs <url> [--out dir] [--widths 375,768,1440] [--schemes light,dark]');
    }
    return args;
}

/** Resolves a dependency from the project the script runs in, not from the skill folder. */
async function load(name) {
    const require = createRequire(pathToFileURL(join(process.cwd(), 'package.json')));
    try {
        return await import(pathToFileURL(require.resolve(name)).href);
    } catch {
        throw new Error(`missing dependency "${name}": run "npm i -D playwright @axe-core/playwright" in this project`);
    }
}

async function smallTargets(page) {
    return page.$$eval('a[href], button, input:not([type=hidden]), select, textarea, [role=button], [role=link], [tabindex]:not([tabindex="-1"])', (nodes, min) =>
        nodes
            .map(node => ({ node, box: node.getBoundingClientRect() }))
            .filter(({ box }) => box.width > 0 && box.height > 0 && (box.width < min || box.height < min))
            .filter(({ node }) => !(node.tagName === 'A' && node.closest('p, li') && getComputedStyle(node).display === 'inline'))
            .slice(0, 50)
            .map(({ node, box }) => ({
                element: node.outerHTML.slice(0, 120),
                size: `${Math.round(box.width)}x${Math.round(box.height)}`
            })),
        MIN_TARGET
    );
}

async function focusWithoutIndicator(page) {
    const missing = [];
    await page.locator('body').click({ position: { x: 1, y: 1 } }).catch(() => {});
    for (let i = 0; i < FOCUS_SAMPLE; i++) {
        await page.keyboard.press('Tab');
        const result = await page.evaluate(() => {
            const el = document.activeElement;
            if (!el || el === document.body) return null;
            const focused = getComputedStyle(el);
            const snapshot = s => [s.outlineStyle, s.outlineWidth, s.outlineColor, s.boxShadow, s.borderColor, s.backgroundColor].join('|');
            const before = snapshot(focused);
            el.blur();
            const after = snapshot(getComputedStyle(el));
            el.focus();
            const visible = focused.outlineStyle !== 'none' && parseFloat(focused.outlineWidth) > 0;
            return { element: el.outerHTML.slice(0, 120), changed: before !== after, visible };
        });
        if (!result) break;
        if (!result.changed && !result.visible) missing.push(result.element);
    }
    return [...new Set(missing)];
}

async function run() {
    const args = parseArgs(process.argv.slice(2));
    const playwright = await load('playwright');
    const chromium = playwright.chromium ?? playwright.default?.chromium;
    const axeModule = await load('@axe-core/playwright');
    const AxeBuilder = axeModule.AxeBuilder ?? axeModule.default?.default ?? axeModule.default;
    mkdirSync(args.out, { recursive: true });

    const browser = await chromium.launch({ executablePath: process.env.UX_CHECK_CHROMIUM || undefined });
    const report = { url: args.url, checked_at: new Date().toISOString(), runs: [], reflow: null, zoom_blocked: null };
    try {
        for (const scheme of args.schemes) {
            for (const width of args.widths) {
                const context = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme });
                const page = await context.newPage();
                await page.goto(args.url, { waitUntil: 'networkidle' });
                const screenshot = `${width}-${scheme}.png`;
                await page.screenshot({ path: join(args.out, screenshot), fullPage: true });
                const axe = await new AxeBuilder({ page }).withTags(AXE_TAGS).analyze();
                report.runs.push({
                    width,
                    scheme,
                    screenshot,
                    axe_violations: axe.violations.map(v => ({
                        rule: v.id,
                        impact: v.impact,
                        help: v.help,
                        wcag: v.tags.filter(t => /^wcag\d{3,}$/.test(t)),
                        count: v.nodes.length,
                        targets: v.nodes.slice(0, 5).map(n => n.target.join(' '))
                    })),
                    small_targets: await smallTargets(page),
                    focus_without_indicator: width === Math.max(...args.widths) ? await focusWithoutIndicator(page) : undefined
                });
                await context.close();
            }
        }
        const context = await browser.newContext({ viewport: { width: REFLOW_WIDTH, height: 800 } });
        const page = await context.newPage();
        await page.goto(args.url, { waitUntil: 'networkidle' });
        report.reflow = await page.evaluate(min => ({
            width: min,
            horizontal_overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
            scroll_width: document.documentElement.scrollWidth
        }), REFLOW_WIDTH);
        report.zoom_blocked = await page.evaluate(() => {
            const content = document.querySelector('meta[name=viewport]')?.getAttribute('content') ?? '';
            return /user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b/i.test(content);
        });
        await context.close();
    } finally {
        await browser.close();
    }
    report.criteria = {
        axe_violations: ['A11Y-01', 'A11Y-14', 'A11Y-15', 'COL-02', 'COL-05'],
        small_targets: ['A11Y-20', 'LAY-12', 'RESP-07'],
        focus_without_indicator: ['A11Y-04'],
        reflow: ['A11Y-17', 'RESP-02'],
        zoom_blocked: ['A11Y-31'],
        screenshots: ['LAY-01', 'LAY-02', 'COL-12', 'RESP-04']
    };
    writeFileSync(join(args.out, 'report.json'), JSON.stringify(report, null, 2) + '\n');
    const violations = report.runs.reduce((n, r) => n + r.axe_violations.length, 0);
    console.log(`ux_check: ${report.runs.length} runs, ${violations} axe rule violations, reflow overflow: ${report.reflow.horizontal_overflow}, zoom blocked: ${report.zoom_blocked}`);
    console.log(`ux_check: report and screenshots in ${args.out}/`);
}

run().catch(error => {
    console.error(`ux_check: ${error.message}`);
    process.exit(1);
});
