# Information Architecture (IA)

## Senior mindset

IA is the **skeleton** of the product. A beautiful UI on a bad skeleton still fails, because users cannot form a reliable map in their head. A senior IA reviewer asks three questions on every screen, taken from the classic wayfinding model:
1. **Where am I?** (location cues)
2. **What can I do or find here?** (scent and labels)
3. **Where can I go next, and how do I get back?** (navigation and escape routes)

They don't judge a menu by how it looks. They judge it by **whether a first-time user predicts correctly what is behind each label** (information scent), and whether the structure follows the **user's mental model rather than the org chart or the database schema**.

Products known for simplicity (ChatGPT, Cal.com, Linear) share one IA trait: **a very small number of top-level destinations** (often 3–6), with everything else reachable through context (the object you are on) or search/command palettes.

## Scope

- **In:** global, local, contextual and utility navigation; hierarchy depth and breadth; labeling; grouping and categorization; settings structure; search as navigation; breadcrumbs; URLs and deep links; back-button behavior; cross-links; 404/not-found; sitemap coherence.
- **Out:** visual styling of navigation (→ LAY/COL/TYP), search result ranking and filters (→ DATA), step-by-step task flows (→ FLOW).

## Procedure

### Step 1: Reconstruct the actual sitemap
- Use the surface map from `codebase-recon.md`. Draw the hierarchy as an indented tree from the routes.
- Find **every navigation component**: `Sidebar`, `Navbar`, `Header`, `TabBar`, `BottomNav`, `Menu`, `Breadcrumb`, `CommandPalette`, `Footer`, `SettingsNav`. List their items, order, icons and labels.
- Identify **orphan routes** (exist in the router but are linked from nowhere) and **dead links** (linked but no route).

### Step 2: Measure the structure
- **Breadth:** the number of items in each nav level. Flag a global nav with > 7 top-level items unless it is strongly grouped.
- **Depth:** the clicks or levels from home to each critical-job screen. Critical jobs should be reachable in **≤ 3 levels** (not a law, but a strong heuristic: each level is a chance to lose scent).
- **Balance:** compare a wide-and-shallow structure with a narrow-and-deep one. Research (e.g. Larson & Czerwinski 1998) favors moderate breadth over deep hierarchies.

### Step 3: Evaluate labels
For each nav label, check:
- Is it the **user's word** (from the CTX vocabulary map), not internal jargon ("Entities", "Objects", "Resources", "Misc", "Management")?
- Is it **specific and distinct** from its siblings (no overlap like "Reports" vs. "Analytics" vs. "Insights")?
- Is it **front-loaded** (the key word first) and **consistent in grammar** (all nouns, or all verbs)?
- Does the **page title match the label** that led to it? A mismatch breaks the scent.

### Step 4: Evaluate wayfinding on each critical-flow screen
- Current location is indicated (active nav state, page title, breadcrumb).
- An escape route exists (back, close, cancel, home/logo).
- On deep or detail pages: a parent context link.
- In multi-tenant products: the current workspace, org or project is always visible and switchable.

### Step 5: URLs, deep links and history
- URLs are readable, stable and **shareable**. Do filters, tabs, pagination and selected items persist in the URL when users would want to share or bookmark them?
- The browser **Back** button behaves as expected: modals opened by URL close on Back; multi-step wizards don't trap users or lose data.
- Refreshing a page keeps the user's place.
- Mobile: deep links / universal links open the right screen.

### Step 6: Settings and secondary IA
Settings are where IA usually decays. Check grouping (account vs. workspace vs. billing vs. notifications vs. integrations), search within settings, and whether destructive settings are separated ("Danger zone").

### Step 7: Optional validation recommendations
When the IA is uncertain, recommend **tree testing** (e.g. Treejack-style: users find items in a text-only tree; success rate and directness per task) or **card sorting** (open or closed) to ground the structure in user mental models. Hand off to MEAS.

## Criteria

<!-- BEGIN GENERATED criteria (information-architecture) -->
<!-- Source: criteria/information-architecture.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Check | Fail signal | Default severity |
|---|---|---|---|---|
| IA-01 | Top-level navigation is small and meaningful | Count global nav items | > 7 ungrouped items; items of very different importance at the same level | S2 |
| IA-02 | Critical jobs are shallow | Levels or clicks from home to each critical job | > 3 levels, or the job is only reachable via search | S2–S3 |
| IA-03 | Labels in the user's language | Compare labels with the CTX vocabulary | Internal jargon, acronyms, "Misc/Other/General" buckets | S2 |
| IA-04 | Labels are mutually exclusive | Sibling labels with overlapping meaning | Users can't predict which one holds an item | S2 |
| IA-05 | Grouping follows mental model | Groups reflect user tasks or objects | Grouping mirrors teams, tech layers or DB tables | S2–S3 |
| IA-06 | You-are-here cues | Active nav state, page titles, breadcrumbs on deep pages | No active state; page `<title>` generic or identical across pages | S2 |
| IA-07 | Escape routes everywhere | Every screen and modal has back, close or cancel | Dead-end screens; modals with no close; flows without exit | S3 |
| IA-08 | Label–destination match | Nav label text vs. destination H1/title | Label "Billing" leads to "Subscription management" | S1–S2 |
| IA-09 | No orphan or dead routes | Router vs. links | Orphans (unreachable features) or 404 links | S2 (S3 if critical) |
| IA-10 | Shareable, stable URLs | Filters, tabs and selection in URL; readable slugs | State lost on refresh or share; opaque IDs only where names are expected | S2 |
| IA-11 | Back button and history correct | Runtime: Back after modal, wizard and filters | Back exits the app, or loses the form | S2–S3 |
| IA-12 | Context (tenant/project) always visible | Workspace switcher and current context indicator | User can act in the wrong workspace without noticing | S3 (S4 if destructive) |
| IA-13 | Consistent nav across the product | The same nav component and placement on all screens | Nav moves, changes order or disappears between sections | S2 |
| IA-14 | Search or command palette for large IA | Products with many objects or pages have a global search / ⌘K | Large product with nav-only findability | S2 |
| IA-15 | Useful 404 / not-found | Not-found page offers search, home and likely destinations | Blank or developer error page | S2 |
| IA-16 | Settings well structured | Clear groups, danger zone separated, searchable if large | Single long page mixing personal and org settings and destructive actions | S2 |
| IA-17 | Cross-linking between related objects | Detail pages link to related objects (invoice → customer) | Users must go back to the list and search again | S2 |
| IA-18 | Utility nav where expected | Account/profile top-right (web), help, notifications in conventional places | Unconventional placement (Jakob's law) | S1–S2 |
| IA-19 | Mobile navigation pattern fits | Bottom tab bar (3–5 items) for primary destinations on mobile; no hamburger-only for core jobs | Core destinations hidden behind a hamburger | S2 |
| IA-20 | Footer / secondary IA for marketing sites | Legal, pricing, docs, contact and status reachable | Missing legal or contact links | S2 (→ TRUST, LAUNCH) |
<!-- END GENERATED criteria -->

## Code probes

- Routes: see `codebase-recon.md` §2.
- Nav definitions: `navItems`, `menuItems`, `sidebarLinks`, `routes.ts`, `<Link href=`, `<NavLink`, `router.push(`, `navigate(`.
- Page titles: `<title>`, `metadata = {`, `useTitle`, `document.title`, `<Head>`.
- Active states: `aria-current="page"`, `isActive`, `activeClassName`.
- URL state: `useSearchParams`, `URLSearchParams`, `query.` (Next), `useQueryState`. If filters live only in `useState`, they are not shareable.
- Not-found: `not-found.tsx`, `404.tsx`, `*` catch-all routes.

## Anti-patterns

- **Org-chart navigation** ("Sales", "Ops", "Engineering" as sections).
- **"Junk drawer" categories** (Misc, More, Other, Tools).
- **Mystery-meat navigation:** icon-only items without labels or tooltips for non-universal concepts.
- **Hamburger-hiding** the core jobs on mobile.
- **Duplicate entry points with different names** for the same destination.
- **Modal-on-modal** stacking that destroys location awareness.

## Output

- The reconstructed sitemap tree, with depth per critical job.
- A nav-label table: label · destination title · user term? · issues.
- Findings in the standard format.
- The coverage table (IA-01 … IA-20).

## Done when

Every critical job has a known path and depth, every nav label is evaluated, wayfinding is checked on every critical-flow screen, and URL/back behavior is verified (runtime) or explicitly marked Not verified.
