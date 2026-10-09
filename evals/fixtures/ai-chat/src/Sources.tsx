type Citation = { title: string; url: string; quote: string };

export function Sources({ citations }: { citations: Citation[] }) {
  if (citations.length === 0) {
    return null;
  }
  return (
    <aside aria-label="Sources">
      <h2>Sources</h2>
      <ol>
        {citations.map(c => (
          <li key={c.url}>
            <a href={c.url}>{c.title}</a>
            <blockquote>{c.quote}</blockquote>
          </li>
        ))}
      </ol>
    </aside>
  );
}
