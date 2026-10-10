'use client';
import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import { buttonVariants } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';

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
  phases: string[];
  applies_to: string[];
}

interface Props {
  criteria: Criterion[];
  areas: { area: string; prefix: string }[];
  productTypes: string[];
}

interface Filters {
  q: string;
  area: string;
  type: string;
  phase: string;
  severity: string;
}

const EMPTY: Filters = { q: '', area: '', type: '', phase: '', severity: '' };
const TYPE_LABELS: Record<string, string> = {
  'web-app': 'Web app',
  'marketing-site': 'Marketing site',
  mobile: 'Mobile',
  desktop: 'Desktop',
  cli: 'CLI',
  'sdk-api': 'SDK / API',
  'ai-feature': 'AI feature',
};

const areaLabel = (area: string) => area.replace(/-/g, ' ').replace(/^\w/, c => c.toUpperCase());

/** "S2–S3" → [2, 3]; "S3" → [3]. */
function severityLevels(severity: string): number[] {
  const levels = [...severity.matchAll(/S([0-4])/g)].map(m => Number(m[1]));
  if (levels.length === 2) return Array.from({ length: levels[1] - levels[0] + 1 }, (_, i) => levels[0] + i);
  return levels;
}

function readFilters(): Filters {
  const params = new URLSearchParams(window.location.search);
  return { q: params.get('q') ?? '', area: params.get('area') ?? '', type: params.get('type') ?? '', phase: params.get('phase') ?? '', severity: params.get('severity') ?? '' };
}

function matches(c: Criterion, f: Filters): boolean {
  const words = f.q.toLowerCase().split(/\s+/).filter(Boolean);
  const text = `${c.id} ${c.name} ${c.fail_signal} ${c.check ?? ''} ${c.area}`.toLowerCase();
  return (
    words.every(w => text.includes(w)) &&
    (!f.area || c.area === f.area) &&
    (!f.type || c.applies_to.includes(f.type)) &&
    (!f.phase || c.phases.includes(f.phase)) &&
    (!f.severity || severityLevels(c.severity).includes(Number(f.severity)))
  );
}

const fieldClass =
  'h-10 w-full rounded-md border border-input bg-background px-3 text-sm text-foreground shadow-xs placeholder:text-muted-foreground';

export function CriteriaExplorer({ criteria, areas, productTypes }: Props) {
  const [filters, setFilters] = useState<Filters>(EMPTY);

  // Filters live in the URL so a filtered list can be shared; a #ID anchor is never hidden by them.
  useEffect(() => {
    const initial = readFilters();
    const target = decodeURIComponent(window.location.hash.slice(1));
    const targetCriterion = criteria.find(c => c.id === target);
    setFilters(targetCriterion && !matches(targetCriterion, initial) ? EMPTY : initial);
    if (targetCriterion) requestAnimationFrame(() => document.getElementById(target)?.scrollIntoView());
  }, [criteria]);

  useEffect(() => {
    const params = new URLSearchParams();
    for (const [key, value] of Object.entries(filters)) if (value) params.set(key, value);
    const query = params.toString();
    window.history.replaceState(null, '', `${window.location.pathname}${query ? `?${query}` : ''}${window.location.hash}`);
  }, [filters]);

  const shown = useMemo(() => criteria.filter(c => matches(c, filters)), [criteria, filters]);
  const set = (key: keyof Filters) => (event: { target: { value: string } }) => setFilters(f => ({ ...f, [key]: event.target.value }));
  const active = Object.values(filters).some(Boolean);

  return (
    <div>
      <form role="search" aria-label="Filter criteria" className="grid gap-4 sm:grid-cols-2 lg:grid-cols-[2fr_repeat(4,1fr)]" onSubmit={e => e.preventDefault()}>
        <label className="grid gap-1.5 text-sm font-medium">
          Words
          <input type="search" value={filters.q} onChange={set('q')} placeholder="e.g. contrast, undo, FORM-09" className={fieldClass} />
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Area
          <select value={filters.area} onChange={set('area')} className={fieldClass}>
            <option value="">All areas</option>
            {areas.map(a => (
              <option key={a.area} value={a.area}>
                {areaLabel(a.area)} ({a.prefix})
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Product type
          <select value={filters.type} onChange={set('type')} className={fieldClass}>
            <option value="">All types</option>
            {productTypes.map(t => (
              <option key={t} value={t}>
                {TYPE_LABELS[t] ?? t}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Phase
          <select value={filters.phase} onChange={set('phase')} className={fieldClass}>
            <option value="">Design and build</option>
            <option value="design">Design</option>
            <option value="build">Build</option>
          </select>
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Severity
          <select value={filters.severity} onChange={set('severity')} className={fieldClass}>
            <option value="">Any severity</option>
            {[4, 3, 2, 1, 0].map(s => (
              <option key={s} value={s}>
                Can be S{s}
              </option>
            ))}
          </select>
        </label>
      </form>

      <div className="mt-6 flex flex-wrap items-center gap-3 border-b pb-4">
        <p role="status" className="text-sm font-medium">
          {shown.length === criteria.length ? `All ${criteria.length} criteria` : `${shown.length} of ${criteria.length} criteria`}
        </p>
        {active ? (
          <button type="button" onClick={() => setFilters(EMPTY)} className={buttonVariants({ variant: 'outline', size: 'sm' })}>
            Clear filters
          </button>
        ) : null}
      </div>

      {shown.length === 0 ? (
        <div className="py-16 text-center">
          <p className="font-medium">No criterion matches these filters.</p>
          <p className="mt-1 text-sm text-muted-foreground">Try fewer words, or clear a filter.</p>
          <button type="button" onClick={() => setFilters(EMPTY)} className={`${buttonVariants({ variant: 'outline' })} mt-4`}>
            Clear filters
          </button>
        </div>
      ) : (
        <ul className="divide-y">
          {shown.map(c => (
            <li key={c.id} id={c.id} className="criterion -mx-3 rounded-md px-3 py-5">
              <article aria-labelledby={`${c.id}-name`}>
                <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
                  <a href={`#${c.id}`} className="inline-flex min-h-6 items-center font-mono text-sm font-semibold underline-offset-2 hover:underline">
                    {c.id}
                  </a>
                  <h2 id={`${c.id}-name`} className="font-semibold">
                    {c.name}
                  </h2>
                  <Badge variant="secondary" className="ml-auto font-mono">
                    {c.severity}
                  </Badge>
                </div>
                <dl className="mt-2 grid gap-x-4 gap-y-1 text-sm [overflow-wrap:anywhere] sm:grid-cols-[8rem_1fr]">
                  {c.check ? (
                    <>
                      <dt className="text-muted-foreground">Check</dt>
                      <dd>{c.check}</dd>
                    </>
                  ) : null}
                  <dt className="text-muted-foreground">Fail signal</dt>
                  <dd>{c.fail_signal}</dd>
                  {c.severity_note ? (
                    <>
                      <dt className="text-muted-foreground">Severity note</dt>
                      <dd>{c.severity_note}</dd>
                    </>
                  ) : null}
                  {c.related?.length ? (
                    <>
                      <dt className="text-muted-foreground">Related</dt>
                      <dd>{c.related.join(', ')}</dd>
                    </>
                  ) : null}
                  {c.sources?.length ? (
                    <>
                      <dt className="text-muted-foreground">Sources</dt>
                      <dd className="flex flex-wrap gap-x-3">
                        {c.sources.map(s => (
                          <Link key={s} href={`/docs/reference/sources#${s}`} className="inline-flex min-h-6 items-center font-mono text-xs underline underline-offset-2">
                            {s}
                          </Link>
                        ))}
                      </dd>
                    </>
                  ) : null}
                </dl>
                <p className="mt-2 text-xs text-muted-foreground">
                  <Link href={`/docs/areas/${c.area}`} className="underline underline-offset-2">
                    {areaLabel(c.area)}
                  </Link>{' '}
                  · {c.phases.join(' and ')} · {c.applies_to.map(t => TYPE_LABELS[t] ?? t).join(', ')}
                </p>
              </article>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
