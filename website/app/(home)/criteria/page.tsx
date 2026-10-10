import type { Metadata } from 'next';
import Link from 'next/link';
import catalogue from '@/generated/catalogue.json';
import { CriteriaExplorer, type Criterion } from '@/components/criteria-explorer';

export const metadata: Metadata = {
  title: 'Criteria',
  description: `All ${catalogue.criteria.length} ux-expert criteria with permanent IDs, filterable by area, product type, phase and severity.`,
};

export default function CriteriaPage() {
  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-12 sm:px-6">
      <h1 className="text-3xl font-semibold tracking-tight">Criteria</h1>
      <p className="mt-3 max-w-2xl text-muted-foreground">
        Every active criterion, with the permanent ID you can cite in stories, tickets and reports. Each area page explains
        the procedure behind its criteria; <Link href="/docs/reference/severity-and-scoring" className="text-foreground underline underline-offset-2">severity and scoring</Link> explains the S0–S4 scale.
      </p>
      <div className="mt-10">
        <CriteriaExplorer
          criteria={catalogue.criteria as Criterion[]}
          areas={catalogue.areas.map(a => ({ area: a.area, prefix: a.prefix }))}
          productTypes={catalogue.product_types}
        />
      </div>
    </div>
  );
}
