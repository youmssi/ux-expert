# Codebase recon: how to see the product through its code

Shared procedure used by `SKILL.md` (Phase 1) and by any area that needs to locate evidence. Use the fastest search tools available (Grep/Glob, or `rg`/`find`). Read excerpts, not entire large files.

## 1. Detect product type and stack

| Look for | Indicates |
|---|---|
| `package.json` deps: `next`, `react`, `vue`, `nuxt`, `svelte`, `@sveltejs/kit`, `@angular/core`, `solid-js`, `astro`, `remix`, `@tanstack/router` | Web front-end framework |
| `react-native`, `expo`, `flutter` (`pubspec.yaml`), `*.xcodeproj` / `Package.swift` with SwiftUI, `build.gradle` with Compose | Mobile |
| `electron`, `tauri` (`tauri.conf.json`) | Desktop |
| `clap`, `commander`, `yargs`, `click`, `typer`, `cobra`, `oclif`, `bin` field in package.json | CLI |
| Published library manifest (`Cargo.toml` `[lib]`, `pyproject.toml`, `package.json` `main`/`exports`, `go.mod`) with no UI | SDK / library: DX is primary |
| `openapi.yaml`, `*.proto`, `graphql` schema, route handlers | API surface |
| `openai`, `@anthropic-ai/sdk`, `anthropic`, `ai` (Vercel), `langchain`, `llamaindex`, model ids in config | AI features |
| `tailwind.config.*`, `*.module.css`, `styled-components`, `@emotion`, `vanilla-extract`, `stitches`, `sass` | Styling system |
| `@radix-ui`, `@headlessui`, `shadcn` (`components/ui`), `@mui`, `antd`, `@chakra-ui`, `@mantine`, `react-aria` | Component library |
| `i18next`, `react-intl`, `next-intl`, `vue-i18n`, `@lingui`, `*.po`, `locales/`, `messages/*.json` | i18n |
| `posthog`, `segment`, `@amplitude`, `mixpanel`, `gtag`, `plausible`, `@vercel/analytics` | Analytics |
| `playwright`, `cypress`, `@testing-library`, `jest-axe`, `axe-core`, `storybook`, `chromatic`, `percy` | Testing and visual QA |

## 2. Build the surface map

**Routes / screens**
- Next.js app router: `app/**/page.(tsx|jsx)`, `layout.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`
- Next.js pages router: `pages/**/*.(tsx|jsx)`
- Remix / React Router: `routes/**`, `createBrowserRouter`, `<Route path=`
- SvelteKit: `src/routes/**/+page.svelte`; Nuxt: `pages/**/*.vue`; Angular: `RouterModule.forRoot`, `Routes = [`
- React Native: `createStackNavigator`, `expo-router` `app/**`
- Flutter: `MaterialPageRoute`, `GoRoute(`
- CLI: command definitions (`#[derive(Subcommand)]`, `.command(`, `@click.command`)
- SDK: public exports (`index.ts` exports, `pub fn` in `lib.rs`, `__init__.py`)

**Overlays and transient UI:** search for `Dialog`, `Modal`, `Drawer`, `Sheet`, `Popover`, `Toast`, `toast(`, `Snackbar`, `Tooltip`, `confirm(`, `alert(`.

**Emails and notifications:** `emails/`, `templates/`, `react-email`, `mjml`, `*.hbs`, push-notification payloads.

Record the result as a table: `area | route/screen | file | purpose | in critical flow? (y/n)`.

## 3. Design-system assets

- Tokens: `tokens.*`, `theme.*`, `:root {` CSS variables, `tailwind.config` `theme.extend`, `design-tokens.json`, Style Dictionary configs.
- Shared components: `components/ui/`, `packages/ui/`, `design-system/`.
- Drift probes (count occurrences):
  - Hard-coded colors: `#[0-9a-fA-F]{3,8}\b`, `rgb\(`, `hsl\(` outside token files
  - Arbitrary Tailwind values: `\[[0-9.]+px\]`, `text-\[#`, `bg-\[#`
  - Inline styles: `style=\{\{`
  - Magic z-index: `z-index:\s*\d{3,}`, `z-\[\d+\]`
  - Font sizes not on the scale: `font-size:\s*\d+px`

## 4. States and resilience probes

- Loading: `isLoading`, `isPending`, `Skeleton`, `Spinner`, `Suspense`, `loading.tsx`
- Errors: `ErrorBoundary`, `error.tsx`, `catch\s*\(`, `.catch(`, `onError`, empty catch `catch\s*(\(\w*\))?\s*\{\s*\}`
- Empty: `length === 0`, `EmptyState`, `no results`, `isEmpty`
- Offline: `navigator.onLine`, `online`/`offline` events, service workers

## 5. Content and strings

- If i18n exists, the message catalogs are the **full copy inventory**. Read them as a document.
- If not: search JSX/templates for string literals, e.g. `>[A-Z][a-z]+[^<{]*<` and `placeholder="`, `aria-label="`, `title="`.
- Error copy: `"Something went wrong"`, `"Error"`, `"Invalid"`, `"Oops"`, `"Failed"`.

## 6. Accessibility quick probes

`outline:\s*none|outline:\s*0`, `<div[^>]*onClick`, `<img(?![^>]*alt=)`, `tabIndex=\{?["']?[1-9]`, `aria-hidden="true"` on focusable elements, `role="button"` without key handlers, `autoFocus`, `user-scalable=no`, `maximum-scale=1`.

## 7. Runtime ability

- Check for a dev script: `npm run dev`, `pnpm dev`, `cargo run`, `flutter run`, `expo start`.
- Check for a browser: Playwright/Chromium (e.g. `/opt/pw-browsers`), or a browser tool.
- If it runs, run `node scripts/ux_check.mjs <url>` from the project root for each critical-flow screen (needs `npm i -D playwright @axe-core/playwright`). It saves screenshots at 375, 768 and 1440 px in light and dark mode, and reports axe violations (WCAG 2.2 A/AA), targets under 24 px, focus without a visible indicator, overflow at 320 px and blocked zoom, each mapped to criterion IDs. Look at the screenshots for the visual criteria (attention order, primary action, density). Check each reported item before turning it into a finding. Record terminal transcripts for CLIs.
- For a contrast pair from code or a screenshot, run `python3 scripts/contrast.py <fg> <bg> [--size px] [--bold]`.
- If it does not run: say so in the report. Visual and behavioral findings stay at Medium confidence or lower.

## 8. Output of recon

```markdown
## Inventory
- Product type(s): …
- Stack: …
- Runtime: available / not available (reason)
### Surface map
| Area | Route/screen | File | Purpose | Critical flow |
### Key flows (draft)
1. Sign-up: /signup → /verify → /onboarding/1..3 → /dashboard
### Design system
- Tokens: path · Components: path · Drift counts: colors N, spacing N, font sizes N
### Gaps
- …
```
