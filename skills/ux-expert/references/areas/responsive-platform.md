# Responsive and Platform Fit (RESP)

## Senior mindset

A senior doesn't ask "does it shrink?". They ask **"does it fit how people use this device?"** A phone is used one-handed, in motion, in sunlight, interrupted, with a thumb that reaches the bottom of the screen easily and the top corners poorly (Steven Hoober's field research on how people hold phones). A desktop user has precision pointing, hover, a keyboard and multiple windows. A tablet user may switch between touch and a keyboard.

So "responsive" means **re-prioritizing**, not just re-flowing: what is primary on mobile, what moves into a sheet or menu, what becomes a bottom bar, what becomes a gesture with a visible alternative.

They also respect **platform conventions** (Jakob's law, per platform): iOS users expect back-swipe, large titles, bottom tabs and share sheets; Android users expect the system back button/gesture to work correctly, Material components and a top app bar; desktop users expect keyboard shortcuts, right-click menus, hover tooltips and resizable windows. Cross-platform frameworks often ship "one design for all", which feels foreign everywhere.

## Scope

- **In:** breakpoints and fluid layout, content priority per size, navigation transformation, mobile ergonomics (thumb zone), touch targets and spacing, hover dependence, virtual keyboard (inputs not hidden, correct keyboard types), safe areas, viewport units (`100vh` issues), orientation, iOS HIG and Android Material conventions, system back behavior, gestures, haptics, native share and pickers, PWA (installability, offline, splash), desktop conventions (shortcuts, context menus, window sizes, multi-window), cross-browser and OS support matrix, print styles if relevant.
- **Out:** layout principles at a single size (→ LAY), accessibility conformance (→ A11Y, though target size overlaps), performance on devices (→ PERF).

## Procedure

### Step 1: Define the device/platform matrix
From CTX and analytics: which devices, OSes, browsers and window sizes matter? Default web matrix: 360×800 (Android), 390×844 (iPhone), 768×1024 (tablet portrait), 1024×768, 1280×800 (small laptop), 1440×900, 1920×1080; Chrome, Safari (iOS and macOS), Firefox, Edge. Safari on iOS is mandatory for any consumer web product.

### Step 2: Breakpoint and layout review
- Extract breakpoints (`@media`, Tailwind `sm/md/lg/xl/2xl`, `useMediaQuery`, container queries).
- Are breakpoints **content-driven** (where the layout breaks) rather than device-driven? Are there gaps (e.g. 900–1024 px tablets looking broken)?
- If runtime is available, screenshot critical screens at each width and check: overflow (horizontal scroll), overlapping elements, unreadable tables, cut-off modals, and fixed-width elements.
- **Content priority:** on small screens, is the primary task content first? Are secondary panels collapsed into tabs, sheets or accordions rather than squeezed?
- **Tables on mobile:** horizontal scroll with a sticky first column, a card transformation, or column prioritization (→ DATA).

### Step 3: Mobile ergonomics
- **Thumb zone:** primary and frequent actions within easy reach (bottom/center); navigation in a bottom tab bar (3–5 items) for primary destinations.
- **Targets:** ≥ 44×44 pt (iOS) / 48×48 dp (Android); ≥ 8 px spacing between adjacent targets.
- **No hover dependence:** everything available via tap; `@media (hover: hover)` used to scope hover-only enhancements.
- **Virtual keyboard:** focused inputs scroll into view and aren't covered; sticky footers don't sit on top of the keyboard awkwardly; the correct keyboard type appears (→ FORM-05); `enterkeyhint` set (next/go/send/search).
- **Viewport units:** `100vh` on mobile browsers includes hidden toolbars, so use `100dvh`/`svh`/`lvh`; check for content cut off at the bottom.
- **Safe areas:** `env(safe-area-inset-*)` for notches and home indicators; `viewport-fit=cover` handled; native: `SafeAreaView`, `WindowInsets`.
- **Orientation:** works in both orientations unless essential (WCAG 1.3.4).
- **Pull-to-refresh, swipe gestures:** conventional and with visible alternatives.

### Step 4: Platform conventions (native and cross-platform apps)
- **iOS (HIG):** navigation bar with back button and title, tab bar at the bottom, swipe-from-edge back gesture not blocked, modal sheets with grabbers, standard share sheet, SF Symbols-consistent icons, Dynamic Type, haptics used sparingly and consistently.
- **Android (Material 3):** system back (button and predictive back gesture) navigates correctly and never exits unexpectedly from deep screens; top app bar; FAB where appropriate; snackbars; edge-to-edge with insets; Material You dynamic color where adopted.
- **Cross-platform (React Native/Flutter):** platform-adaptive components (date pickers, switches, alerts, scrolling physics) rather than one look everywhere; check `Platform.OS` branches.
- **Desktop apps (Electron/Tauri) and desktop web apps:** keyboard shortcuts with OS-correct modifiers (⌘ on macOS, Ctrl on Windows/Linux), right-click context menus where users expect them, native menus, window min size handled, high-DPI assets, drag-and-drop of files from the OS, multi-window/tabs behavior.

### Step 5: PWA and web platform features (if relevant)
- Manifest, icons, theme color, installability, offline fallback page, update strategy (no stale app forever), splash.
- Web Share API, file pickers, clipboard, notifications permission at the moment of need (→ ONB-16).

### Step 6: Cross-browser and OS
- Check the `browserslist` support target matches the audience; polyfills; Safari-specific CSS issues (sticky, `gap` in old versions, date inputs, `100vh`), and font rendering differences.
- Note any features used without fallback (e.g. `:has()`, container queries, View Transitions) and whether degradation is graceful.

## Criteria

<!-- BEGIN GENERATED criteria (responsive-platform) -->
<!-- Source: criteria/responsive-platform.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| RESP-01 | Device/platform matrix defined and tested | No defined matrix; untested on iOS Safari | S2 |
| RESP-02 | No horizontal overflow at supported widths | Horizontal scroll or cut-off content | S2–S3 |
| RESP-03 | Content-driven breakpoints without gaps | Broken layouts between breakpoints | S2 |
| RESP-04 | Content re-prioritized on small screens | Desktop layout squeezed; primary task below secondary content | S2–S3 |
| RESP-05 | Mobile navigation pattern appropriate | Core destinations hidden in a hamburger; too many tabs | S2 |
| RESP-06 | Thumb-reachable primary actions | Primary actions only in the top corners | S2 |
| RESP-07 | Touch target size and spacing | < 44 pt / 48 dp; cramped adjacent targets | S2–S3 |
| RESP-08 | No hover dependence | Hover-only menus, actions or info on touch devices | S3 |
| RESP-09 | Virtual keyboard handled | Inputs hidden under the keyboard; wrong keyboard; no `enterkeyhint` | S2–S3 |
| RESP-10 | Viewport units and safe areas correct | `100vh` cut-offs; content under the notch or home indicator | S2 |
| RESP-11 | Orientation support | Locked or broken in landscape | S2 |
| RESP-12 | Platform conventions followed (iOS) | Blocked back swipe; non-standard nav; no Dynamic Type | S2 |
| RESP-13 | Platform conventions followed (Android) | System back exits or misbehaves; no edge-to-edge insets | S2–S3 |
| RESP-14 | Desktop conventions followed | Wrong modifier keys; no context menus where expected; unusable at small window sizes | S2 |
| RESP-15 | Tables and data usable on small screens | Unreadable or unusable data views on mobile | S2 (→ DATA) |
| RESP-16 | Modals and overlays adapt | Desktop modals cut off on mobile; should be full-screen sheets | S2 |
| RESP-17 | PWA quality (if PWA) | Not installable when intended; no offline fallback; stale updates | S2 |
| RESP-18 | Cross-browser support | Broken features in a supported browser; no graceful degradation | S2–S3 |
| RESP-19 | High-DPI and asset quality | Blurry images and icons on retina/high-DPI screens | S1 |
| RESP-20 | Print styles (if users print: invoices, reports, tickets) | Printing produces broken or unusable output | S1–S2 |
<!-- END GENERATED criteria -->

## Code probes

- Breakpoints: `@media`, `min-width:|max-width:`, `\b(sm|md|lg|xl|2xl):`, `useMediaQuery`, `@container`.
- Fixed widths: `width:\s*\d{3,}px`, `w-\[\d{3,}px\]`, `min-width:\s*\d{3,}px`.
- Viewport: `100vh`, `h-screen` (check for `dvh`/`svh` alternatives), `viewport-fit`, `safe-area-inset`, `SafeAreaView`, `useSafeAreaInsets`.
- Hover: `:hover` used for revealing content; `onMouseEnter` with no touch/focus equivalent; `@media (hover`.
- Keyboard: `enterkeyhint`, `inputmode`, `KeyboardAvoidingView`, `windowSoftInputMode`.
- Platform branches: `Platform.OS`, `Platform.select`, `defaultTargetPlatform`, `isIOS|isAndroid`.
- Back handling: `BackHandler`, `onBackPressed`, `PopScope`/`WillPopScope`, `OnBackPressedDispatcher`.
- PWA: `manifest.json`/`manifest.webmanifest`, `serviceWorker.register`, `workbox`.
- Browser support: `browserslist`, `.browserslistrc`, `targets` in Babel/SWC config.
- Print: `@media print`.

## Gotchas

- Chrome device emulation does not reproduce iOS Safari's viewport and virtual-keyboard behaviour. Without iOS Safari, RESP-09 and RESP-10 are Not verified.
- Tailwind breakpoints are mobile-first `min-width`: `md:` applies from 768 px up.
- Judge native apps against the current Apple HIG and Material guidance, and name the version you used.

## Output

- The device/platform matrix with tested/not-tested status.
- A screenshot grid summary (if runtime) per critical screen × width.
- Findings in the standard format; the coverage table (RESP-01 … RESP-20).

## Done when

Every critical screen is checked at the matrix widths (runtime or static reasoning, with confidence marked), mobile ergonomics and keyboard behavior are evaluated, and platform convention compliance is assessed for every shipped platform.
