import defaultMdxComponents from 'fumadocs-ui/mdx';
import type { ComponentProps } from 'react';
import type { MDXComponents } from 'mdx/types';

// Wide tables scroll inside a region keyboard users can reach and screen readers can name
// (axe: scrollable-region-focusable; A11Y-02, A11Y-17).
function Table(props: ComponentProps<'table'>) {
  return (
    <div role="region" aria-label="Table" tabIndex={0} className="relative my-6 overflow-auto prose-no-margin">
      <table {...props} />
    </div>
  );
}

export function getMDXComponents(components?: MDXComponents) {
  return {
    ...defaultMdxComponents,
    table: Table,
    ...components,
  } satisfies MDXComponents;
}

export const useMDXComponents = getMDXComponents;

declare global {
  type MDXProvidedComponents = ReturnType<typeof getMDXComponents>;
}
