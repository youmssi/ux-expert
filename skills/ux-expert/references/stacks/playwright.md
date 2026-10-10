# Playwright Test

<!-- Generated from criteria/stacks/playwright.yaml by scripts/generate.py. Edit the YAML, then run the script. -->

Read when the project uses Playwright, or when a finding or refactor step needs a regression guard. It maps criteria to Playwright checks that keep a fix fixed, and lists Playwright behaviour that makes tests pass while users still fail.

Verified against Playwright Test 1.64 on 2026-10-10, reading https://github.com/microsoft/playwright@`d9f2fd3`. Detected by dependency `@playwright/test`, `playwright` or file `playwright.config.ts`, `playwright.config.js`, `playwright.config.mjs`. If the project uses another major version, check the gotchas against its docs.

## Where the evidence is

| What | Where |
|---|---|
| Existing UX guards | `toMatchAriaSnapshot`, `AxeBuilder` (`@axe-core/playwright`), `toHaveScreenshot`, `toHaveAccessibleName`, `toHaveAccessibleErrorMessage`, `toBeFocused` in `*.spec.ts` |
| Preferences and devices covered | `use` blocks and projects in `playwright.config.*`: `colorScheme`, `reducedMotion`, `forcedColors`, `contrast`, `locale`, `timezoneId`, `devices[...]` |
| States covered | `page.route` with `route.fulfill({ status })` or `route.abort()`, `context.setOffline`, `page.clock` in tests |
| Baselines | `*-snapshots/` folders next to specs; file names carry the browser and platform (`-chromium-linux.png`) |

## Gotchas

- Role-based locators (`getByRole` with a name) give early feedback on roles and accessible names, but Playwright states they do not replace accessibility audits. A suite of `getByRole` tests is not evidence for A11Y-01. (A11Y-01, A11Y-10) Source: [docs/src/locators.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/locators.md).
- axe scans the page in its current state. Menus, dialogs and error messages are only checked if the test opens them first; `.include()` can then scope the scan to the revealed part. (A11Y-01) Source: [docs/src/accessibility-testing-js.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/accessibility-testing-js.md).
- `.exclude()` skips every axe rule on the element and all its descendants, not just the known issue, so it can hide new violations. Prefer `.disableRules()` for a specific rule, or a snapshot of known violations. (A11Y-01, A11Y-33) Source: [docs/src/accessibility-testing-js.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/accessibility-testing-js.md).
- `toBeVisible` treats `opacity: 0` elements as visible. A test can pass on a control users cannot see; check opacity or a screenshot for visibility findings. (INT-01, A11Y-04) Source: [docs/src/actionability.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/actionability.md).
- `force: true` skips actionability checks, so a click succeeds on a control covered by another element or disabled for users. Tests that need it usually hide an overlay or layering defect. (LAY-16, LAY-17) Source: [docs/src/actionability.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/actionability.md).
- Screenshot baselines are per browser and platform (fonts and rendering differ). Baselines made on a laptop fail on Linux CI; generate and update them in the CI environment. (DS-14) Source: [docs/src/test-snapshots-js.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/test-snapshots-js.md).
- `toHaveScreenshot` disables animations by default and hides the caret; `page.screenshot` leaves animations running. Evidence screenshots can catch a mid-transition frame that the visual test never sees. (DS-14, INT-08) Source: [docs/src/api/params.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/api/params.md).
- `locale` and `timezoneId` change the browser only, not the test runner, so dates formatted in the test code use the runner's settings. Compare against fixed strings, not values computed in the test. (I18N-12, I18N-13) Source: [docs/src/emulation.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/emulation.md).
- Requests made by a service worker (including Mock Service Worker) are invisible to `page.route`, so error-state tests silently test nothing. Set `serviceWorkers` to `'block'` for those tests. (STATE-07, STATE-22) Source: [docs/src/network.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/network.md).
- `page.clock.install()` must run before any other clock call; then `fastForward` fires due timers at once. This is how session-expiry and inactivity warnings are tested without waiting. (STATE-12, A11Y-23) Source: [docs/src/clock.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/clock.md).
- Since 1.64, device descriptors forward `screen`, so media queries see the emulated screen size. Responsive tests written before may change results after the upgrade. (RESP-02, RESP-04) Source: [docs/src/release-notes-js.md](https://github.com/microsoft/playwright/blob/d9f2fd3e2232ace8e317a84eda6cb86e25bcf49c/docs/src/release-notes-js.md).

## Probes

Files: `.ts`, `.js`, `.mjs`. Run with `python3 scripts/probe.py <project root>`; a hit is a place to look, not a finding.

| Probe | Kind | Pattern | Look for | Criteria |
|---|---|---|---|---|
| `playwright-css-locator` | review | `locator\(\s*['"`][.#\[]` | CSS selectors where `getByRole` or `getByLabel` would also check roles and names; often the element has none. | A11Y-10, A11Y-11 |
| `playwright-force-click` | smell | `force:\s*true` | A click forced past actionability checks; the real control may be covered or disabled for users. | LAY-17, INT-03 |
| `playwright-axe-exclude` | review | `\.exclude\(` | Elements removed from every axe rule; check the exclusion is still needed and as narrow as possible. | A11Y-01 |
| `playwright-a11y-guards` | inventory | `AxeBuilder\|toMatchAriaSnapshot\|toHaveAccessibleName\|toHaveAccessibleErrorMessage\|toBeFocused` | Accessibility guards in the suite. Zero hits means no regression protection for A11Y fixes. | A11Y-33, DS-14 |
| `playwright-preference-emulation` | inventory | `reducedMotion\|colorScheme\|forcedColors\|contrast:\|locale:\|timezoneId` | User preferences and locales the suite covers; compare with the product's themes and markets. | INT-09, COL-12, COL-14, I18N-12 |

## Recipes

### Name and structure of a dialog, as users of assistive technology get them (A11Y-10, A11Y-11, INT-11)

```ts
test('delete dialog is named and offers both choices', async ({ page }) => {
  await page.goto('/projects/42');
  await page.getByRole('button', { name: 'Delete project' }).click();
  await expect(page.getByRole('alertdialog')).toMatchAriaSnapshot(`
    - alertdialog "Delete this project?":
      - button "Cancel"
      - button "Delete project"
  `);
});
```

### Escape closes the dialog and focus returns to its trigger (A11Y-06, INT-11)

```ts
test('focus returns to the trigger', async ({ page }) => {
  await page.goto('/settings');
  const trigger = page.getByRole('button', { name: 'Edit profile' });
  await trigger.click();
  await expect(page.getByRole('dialog')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.getByRole('dialog')).toBeHidden();
  await expect(trigger).toBeFocused();
});
```

### Automated WCAG A/AA scan of a critical screen, including revealed UI (A11Y-01)

```ts
import AxeBuilder from '@axe-core/playwright';

test('checkout has no detectable WCAG A/AA violations', async ({ page }) => {
  await page.goto('/checkout');
  await page.getByRole('button', { name: 'Choose delivery' }).click();
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

### Field errors are announced, not only shown (FORM-10, A11Y-24)

```ts
test("email error is the field's accessible error message", async ({ page }) => {
  await page.goto('/signup');
  await page.getByLabel('Email').fill('ana@');
  await page.getByRole('button', { name: 'Create account' }).click();
  await expect(page.getByLabel('Email')).toHaveAccessibleErrorMessage(/valid email/i);
});
```

### A server error shows an actionable message, and offline is handled (STATE-07, STATE-08, STATE-11)

```ts
test('failed save keeps input and explains', async ({ page, context }) => {
  await page.route('**/api/projects', route => route.fulfill({ status: 500, body: '{}' }));
  await page.goto('/projects/new');
  await page.getByLabel('Name').fill('Roadmap');
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByRole('alert')).toContainText(/try again/i);
  await expect(page.getByLabel('Name')).toHaveValue('Roadmap');

  await context.setOffline(true);
  await page.getByRole('button', { name: 'Create' }).click();
  await expect(page.getByRole('alert')).toContainText(/offline/i);
});
```

### Session expiry warns before signing out (STATE-12, A11Y-23)

```ts
test('inactivity warning appears before logout', async ({ page }) => {
  await page.clock.install();
  await page.goto('/dashboard');
  await page.clock.fastForward('25:00');
  await expect(page.getByRole('alertdialog', { name: /still there/i })).toBeVisible();
});
```

### Dark mode and reduced motion, as a screenshot guard (COL-12, INT-09, DS-14)

```ts
test.use({ colorScheme: 'dark', reducedMotion: 'reduce' });

test('dashboard in dark mode', async ({ page }) => {
  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard-dark.png', {
    mask: [page.getByTestId('live-clock')],
  });
});
```

### No horizontal scrolling at 320 CSS px (A11Y-17, RESP-02)

```ts
test('pricing reflows at 320 px', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 800 });
  await page.goto('/pricing');
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
  );
  expect(overflow).toBe(false);
});
```
