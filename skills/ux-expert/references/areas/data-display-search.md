# Data Display, Search and Filtering (DATA)

## Senior mindset

Data UIs serve **decisions and actions**, not decoration. The senior asks of every table, chart or dashboard: **"What question does the user bring here, and how fast can they answer it and act on the answer?"** A dashboard with 24 charts and no clear question is a wall of noise. A table where you can't sort by the column you care about forces an export to Excel, which is a signal the UI failed.

Their principles:
- **Overview first, zoom and filter, then details on demand** (Shneiderman's visual information-seeking mantra).
- **Data-ink ratio** (Tufte): remove non-data decoration (heavy gridlines, 3D, gradients) so the data stands out.
- **The right chart for the question:** comparison → bars; trend over time → lines; part-to-whole (few parts) → a stacked bar or (sparingly) a pie/donut; distribution → histogram/box plot; relationship → scatter. A table when users need exact values.
- **Search is a conversation:** the system should understand typos, synonyms and partial input, show results instantly, explain what it searched, and never dead-end.
- **Scale is a design input:** design for 0, 1, 10, 10,000 and 10 million rows.

## Scope

- **In:** tables/grids (columns, alignment, density, headers, sticky elements, responsive behavior), lists and cards, record detail views, dashboards (KPIs, layout, comparisons, context), charts (type choice, axes, labels, legends, color, accessibility), search (input, autocomplete, scope, typo tolerance, ranking signals visible to users, highlighting, zero results), filters and facets (visibility, applied-state chips, counts, clear all, URL persistence), sorting, pagination vs. infinite scroll vs. "load more", selection and bulk actions, inline editing, import/export, saved views, and real-time updates.
- **Out:** performance of large data (→ PERF; reference it), general empty/error states (→ STATE; but search zero-results is covered here).

## Procedure

### Step 1: Identify data surfaces and their questions
For each data surface: what is the **user question** (from CTX jobs)? e.g. "Which invoices are overdue and by how much?", "Did sign-ups drop this week?", "Which rule failed for this customer?". Judge every design choice against the question.

### Step 2: Tables and lists
- **Columns:** the most important (identifying) column first; columns ordered by task priority; sensible defaults with show/hide and reorder for power users; no more than users can scan (often 5–8 visible on desktop by default).
- **Alignment:** text left, numbers **right** (with tabular figures, the same decimal places), dates consistent, status as text + icon/color.
- **Headers:** clear, with units in the header ("Amount (EUR)"), sortable affordance, sticky on scroll; the first column sticky on horizontal scroll.
- **Density:** row height fits the users (compact for experts, comfortable default) with an optional density toggle; zebra stripes or row dividers for wide tables; a hover highlight.
- **Row actions:** visible on hover **and** focus and on touch (→ INT-18), with an overflow menu for less common actions; the whole row clickable for "open" (but not conflicting with inner controls).
- **Empty cells:** an explicit "—" or "Not set", not blank (blank is ambiguous: loading? zero? missing?).
- **Large values:** abbreviation (1.2M) with the exact value on hover or in detail.
- **Responsive:** see RESP-15.

### Step 3: Selection and bulk actions
- Checkboxes with a header "select all" stating its scope ("Select all 2,340 results" vs. "Select 50 on this page").
- A bulk action bar appears on selection, with a count; destructive bulk actions confirmed with the count (→ STATE-18).
- Shift-click range selection for power users.
- Selection persists across pagination (or the UI clearly says it doesn't).

### Step 4: Search
- **Placement:** in the conventional location (top of a list or global header); keyboard shortcut (`/` or ⌘K) for frequent use.
- **Behavior:** instant results or debounced (~150–300 ms); autocomplete/suggestions; recent searches; **typo tolerance** and synonyms; partial matching; search across the fields users expect (name, email, ID); and the **scope** is shown (searching "in this project" vs. "everywhere").
- **Results:** match highlighting; result count; useful snippets; grouping by type for global search; and ranking that puts exact matches first.
- **Zero results:** echo the query; suggest spelling corrections; offer to broaden the scope or clear filters; show popular items; never a bare "No results".
- **Query persistence:** in the URL (shareable; Back works; → IA-10).

### Step 5: Filters, facets and sorting
- Filters visible for frequent dimensions (not all hidden in a drawer); facet counts when helpful ("Open (12)").
- **Applied filters shown as removable chips**, with a "Clear all".
- Instant apply for single-select/quick filters; an explicit "Apply" for complex multi-field filter panels (especially on mobile).
- Filters that would produce zero results are disabled or show (0).
- Sort control shows the current sort and direction; the default sort matches the main question (most recent, most urgent).
- Filter, sort and pagination state persisted in the URL and/or as **saved views** for repeated use.

### Step 6: Pagination and loading more
- **Pagination** for goal-directed lookup and when position matters (admin tables; users need to return to "page 3").
- **Infinite scroll** for browsing feeds; it breaks the footer, Back-position restoration and "find again", so it needs scroll restoration and should not be used where the footer has important links.
- **"Load more"** as a middle ground.
- Show the total count when it is known; for very large sets, "1–50 of many" is acceptable.
- Page size options for power users.

### Step 7: Dashboards and KPIs
- **One question per widget**; the most important KPIs at the top-left (F/Z reading pattern; → LAY).
- Each KPI has **context**: comparison to the previous period or a target, the direction of change with a meaningful color (and a non-color cue), and the time range clearly shown and adjustable globally.
- Definitions available (hover or info icon: "Active users = users with ≥ 1 session in 7 days").
- Drill-down from a KPI to the underlying records.
- Data freshness ("Updated 5 min ago") and timezone of aggregations shown.
- No vanity widgets; fewer, better charts.

### Step 8: Charts
- **Chart type** matches the question (see the mindset). Avoid 3D, dual y-axes (often misleading), pies with > ~5 slices, and truncated bar axes that exaggerate differences (bars start at 0).
- Axes labeled with units; readable tick labels; direct labeling preferred over legends when possible; legends ordered like the data.
- Color: a categorical palette with ≤ ~7 colors, color-blind safe; a sequential or diverging palette for magnitude (→ COL-11); highlight color used for the focus series.
- Tooltips show exact values; keyboard-accessible data points or an accessible alternative (a data table, a summary sentence) (→ A11Y-14).
- Empty, loading and error states for each chart (→ STATE).
- Consistent formatting of numbers, dates and units (→ I18N).

### Step 9: Editing, import and export
- Inline editing: a clear edit affordance, save/cancel (Enter/Esc), validation inline, and an optimistic update with error rollback.
- Import: a template download, column mapping, preview, validation with row-level errors, partial success handling, and undo or rollback.
- Export: CSV/XLSX of **what the user sees** (current filters and columns) or everything, stated clearly; large exports done in the background with notification.

## Criteria

<!-- BEGIN GENERATED criteria (data-display-search) -->
<!-- Source: criteria/data-display-search.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| DATA-01 | Each data surface answers a clear question | Dashboards or tables with no clear purpose | S2 |
| DATA-02 | Column priority and defaults | Identifier not first; irrelevant columns dominate | S2 |
| DATA-03 | Numeric alignment and formatting | Numbers left-aligned; inconsistent decimals; no units | S2 |
| DATA-04 | Sticky headers and first column for large tables | Context lost when scrolling | S2 |
| DATA-05 | Explicit empty cells | Blank cells with ambiguous meaning | S1–S2 |
| DATA-06 | Accessible row actions | Hover-only; unclear clickable rows | S2 |
| DATA-07 | Bulk selection scope clarity | "Select all" ambiguous; selection silently lost | S2–S3 |
| DATA-08 | Search findability and tolerance | No typo tolerance; wrong fields searched; scope unclear | S2–S3 |
| DATA-09 | Search results usable | No highlighting, count or grouping | S2 |
| DATA-10 | Helpful zero results | Bare "No results" | S2 |
| DATA-11 | Filters visible and applied state clear | Hidden filters; no chips or clear-all | S2 |
| DATA-12 | Sort clarity and sensible default | No sort indicator; default order irrelevant to the task | S2 |
| DATA-13 | State in URL / saved views | Filters, sort and search lost on refresh or share | S2 |
| DATA-14 | Appropriate pagination strategy | Infinite scroll in admin tables; no position restoration | S2 |
| DATA-15 | Scales to large data | Unbounded rendering; missing totals; freezing | S2–S3 (→ PERF) |
| DATA-16 | KPIs have context | Numbers with no comparison, period or definition | S2 |
| DATA-17 | Drill-down and details on demand | Dead-end charts and KPIs | S2 |
| DATA-18 | Data freshness shown | Unknown staleness on operational dashboards | S2 |
| DATA-19 | Correct chart type and honest axes | Misleading charts (truncated bars, 3D, dual axes, overloaded pies) | S2–S3 |
| DATA-20 | Chart labeling and legends | Missing units and axis labels; legend far from the data | S2 |
| DATA-21 | Chart accessibility | No text alternative; color-only series; mouse-only tooltips | S2–S3 |
| DATA-22 | Inline editing safety | Unclear edit mode; no cancel; silent failures | S2 |
| DATA-23 | Import validation and recovery | All-or-nothing imports with vague errors | S2–S3 |
| DATA-24 | Export clarity | Unclear export scope; huge exports block the UI | S2 |
| DATA-25 | Real-time updates non-disruptive | Rows jump while the user is reading or selecting | S2 |
<!-- END GENERATED criteria -->

## Code probes

- Tables: `<table`, `DataGrid`, `@tanstack/react-table`, `ag-grid`, `MUI DataGrid`, `antd Table`, `columns = [`.
- Alignment: `text-right|text-align:\s*right|align:\s*['"]right` on numeric columns; `tabular-nums`.
- Search: `search`, `useDebounce`, `debounce\(`, `fuse.js`, `algolia`, `meilisearch`, `typesense`, `elasticsearch`, `ILIKE`, `LIKE '%`.
- Filters/sort in URL: `useSearchParams`, `nuqs`, `query-string`.
- Pagination: `page=`, `cursor`, `InfiniteScroll`, `useInfiniteQuery`, `IntersectionObserver`, `loadMore`.
- Charts: `recharts`, `chart.js`, `echarts`, `victory`, `nivo`, `d3`, `visx`, `highcharts`, `plotly`.
- Export/import: `csv`, `xlsx`, `papaparse`, `exceljs`, `download`.

## Output

- A data surfaces table (surface · user question · verdict).
- A search behavior test table (query · expected · actual).
- A chart review table (chart · question · type OK? · labeling · a11y).
- Findings in the standard format; the coverage table (DATA-01 … DATA-25).

## Done when

Every data surface on critical flows has its question stated and judged, search and filter behavior is tested (runtime) or reasoned from code with confidence marked, and every chart is reviewed for type, honesty and accessibility.
