import Link from 'next/link';
import { ArrowRight, CheckCircle2, ClipboardList, GitPullRequest, Layers, Rocket, Search, ShieldCheck, Wrench } from 'lucide-react';
import { Tab, Tabs } from 'fumadocs-ui/components/tabs';
import { CodeBlock, Pre } from 'fumadocs-ui/components/codeblock';
import catalogue from '@/generated/catalogue.json';
import { Badge } from '@/components/ui/badge';
import { buttonVariants } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/cn';
import { repoUrl } from '@/lib/shared';

const counts = [
  { value: catalogue.criteria.length, label: 'criteria with permanent IDs' },
  { value: catalogue.areas.length, label: 'areas of UX' },
  { value: catalogue.stacks.length, label: 'stack packs, source-verified' },
  { value: catalogue.probes.length, label: 'native mobile probes' },
  { value: catalogue.sources.length, label: 'sources, each with its status' },
];

const modes = [
  { icon: ClipboardList, title: 'Design', prompt: '“Write the UX acceptance criteria for these stories.”', text: 'UX requirements, acceptance criteria and a Definition of Done for each story, before anything is built.', href: '/docs/modes/design' },
  { icon: Wrench, title: 'Refactor', prompt: '“Plan how to fix these findings safely.”', text: 'A sequenced plan of stories, each shippable alone and protected by a regression guard.', href: '/docs/modes/refactor' },
  { icon: Layers, title: 'Full audit', prompt: '“Run a full UX audit of this app.”', text: 'Every area that applies, findings with evidence, and a coverage table that says what was not verified.', href: '/docs/reference/skill' },
  { icon: Rocket, title: 'Launch gate', prompt: '“Are we ready to launch?”', text: 'An explicit Go, Conditional Go or No-Go, with the blockers and the conditions to meet.', href: '/docs/reference/severity-and-scoring' },
  { icon: Search, title: 'Scoped audit', prompt: '“Audit the checkout flow.”', text: 'One flow, screen or area in depth, such as accessibility only, with the same evidence and scoring.', href: '/docs/reference/skill' },
  { icon: GitPullRequest, title: 'Change review', prompt: '“Review the UX of this pull request.”', text: 'Findings and regressions in the changed UI, before they reach users.', href: '/docs/reference/skill' },
];

const steps = [
  { title: 'Recon', text: 'Maps routes, states and components, detects the stack, and reads the matching stack packs before judging anything.' },
  { title: 'Areas', text: 'Runs the areas that apply to the product, from forms and accessibility to AI interfaces, each with an expert procedure.' },
  { title: 'Verdict', text: 'Scores every finding the same way (severity × reach → priority) and ends with a launch verdict.' },
];

function Section({ id, title, intro, children }: { id: string; title: string; intro?: string; children: React.ReactNode }) {
  return (
    <section aria-labelledby={id} className="mx-auto w-full max-w-6xl px-4 py-16 sm:px-6 sm:py-20">
      <h2 id={id} className="text-2xl font-semibold tracking-tight sm:text-3xl">
        {title}
      </h2>
      {intro ? <p className="mt-3 max-w-2xl text-muted-foreground">{intro}</p> : null}
      <div className="mt-10">{children}</div>
    </section>
  );
}

function ExampleFinding() {
  return (
    <Card className="gap-0 py-0 text-sm" aria-label="Example finding">
      <div className="flex flex-wrap items-center gap-2 border-b px-5 py-3">
        <Badge variant="outline" className="font-mono">F-004</Badge>
        <Link href="/criteria#COL-03" className="inline-flex min-h-6 items-center px-1 font-mono text-xs underline underline-offset-2">COL-03</Link>
        <span className="ml-auto text-xs text-muted-foreground">Example finding</span>
      </div>
      <div className="space-y-3 px-5 py-4">
        <p className="font-semibold leading-snug">Helper text is too faint to read on light backgrounds</p>
        <dl className="grid grid-cols-[auto_1fr] gap-x-3 gap-y-1.5">
          <dt className="text-muted-foreground">Location</dt>
          <dd className="font-mono text-xs leading-5">app/globals.css:12 · 14 forms</dd>
          <dt className="text-muted-foreground">Evidence</dt>
          <dd>
            Measured: <code className="font-mono text-xs">#9CA3AF</code> on white is <strong>2.54:1</strong>
          </dd>
          <dt className="text-muted-foreground">Expected</dt>
          <dd>At least 4.5:1 for meaningful text (WCAG 2.2, 1.4.3)</dd>
          <dt className="text-muted-foreground">Fix</dt>
          <dd>
            Use <code className="font-mono text-xs">#6B7280</code>: <strong>4.83:1</strong>
          </dd>
        </dl>
      </div>
      <div className="flex flex-wrap items-center gap-2 border-t bg-muted/50 px-5 py-3">
        <Badge variant="secondary">Severity S3</Badge>
        <Badge variant="secondary">Reach R2</Badge>
        <Badge variant="secondary">Confidence High</Badge>
        <Badge className="ml-auto">Priority P1</Badge>
      </div>
    </Card>
  );
}

function VerdictCard() {
  return (
    <Card className="gap-0 py-0 text-sm" aria-label="Example launch verdict">
      <div className="flex items-center gap-2 border-b px-5 py-3">
        <ShieldCheck className="size-4 text-brand" aria-hidden="true" />
        <span className="font-semibold">Launch verdict</span>
        <span className="ml-auto text-xs text-muted-foreground">Example</span>
      </div>
      <div className="px-5 py-4">
        <p className="text-lg font-semibold">Conditional Go</p>
        <p className="mt-1 text-muted-foreground">0 P0 open; 2 P1 still need an owner and a date.</p>
        <ul className="mt-4 space-y-2">
          {['Assign owners to F-007 and F-011', 'Verify checkout end to end on mobile', 'Re-run the accessibility scan after the contrast fix'].map(item => (
            <li key={item} className="flex gap-2">
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
              {item}
            </li>
          ))}
        </ul>
      </div>
    </Card>
  );
}

export default function HomePage() {
  return (
    <div className="flex flex-1 flex-col">
      {/* Hero */}
      <section className="border-b">
        <div className="mx-auto grid w-full max-w-6xl items-center gap-12 px-4 py-16 sm:px-6 sm:py-24 lg:grid-cols-[1.1fr_1fr]">
          <div>
            <Badge variant="brand">Agent Skill · MCP server · v1.1</Badge>
            <h1 className="mt-5 text-4xl font-semibold tracking-tight text-balance sm:text-5xl">
              Principal-level UX expertise for your AI agent
            </h1>
            <p className="mt-5 max-w-xl text-lg text-pretty text-muted-foreground">
              ux-expert lets any agent design, refactor and audit a product the way a principal UX engineer would: user
              goals first, evidence for every finding, the same severity every time, and a launch verdict.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link href="/docs/getting-started/install" className={buttonVariants({ size: 'lg' })}>
                Get started <ArrowRight aria-hidden="true" />
              </Link>
              <Link href="/criteria" className={buttonVariants({ variant: 'outline', size: 'lg' })}>
                Browse the {catalogue.criteria.length} criteria
              </Link>
            </div>
            <p className="mt-6 text-sm text-muted-foreground">
              Works with Claude, ChatGPT, Gemini, Codex, Cursor, DeepSeek, Grok and any agent that supports Agent Skills or MCP.
            </p>
          </div>
          <ExampleFinding />
        </div>
      </section>

      {/* Counts */}
      <section aria-label="What the package contains" className="border-b bg-muted/40">
        <dl className="mx-auto grid w-full max-w-6xl grid-cols-2 gap-6 px-4 py-10 sm:grid-cols-3 sm:px-6 lg:grid-cols-5">
          {counts.map(c => (
            <div key={c.label} className="flex flex-col">
              <dt className="text-sm text-muted-foreground">{c.label}</dt>
              <dd className="order-first text-3xl font-semibold tracking-tight tabular-nums">{c.value}</dd>
            </div>
          ))}
        </dl>
      </section>

      <Section id="modes" title="One skill, six ways to use it" intro="Ask in plain words. The skill picks the mode, reads only the areas the task needs, and returns work your team can act on.">
        <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {modes.map(m => (
            <li key={m.title}>
              <Card className="relative h-full">
                <CardHeader>
                  <m.icon className="size-5 text-brand" aria-hidden="true" />
                  <CardTitle className="mt-2 text-base">
                    <Link href={m.href} className="after:absolute after:inset-0 hover:underline">
                      {m.title}
                    </Link>
                  </CardTitle>
                  <CardDescription className="italic">{m.prompt}</CardDescription>
                </CardHeader>
                <CardContent className="text-sm">{m.text}</CardContent>
              </Card>
            </li>
          ))}
        </ul>
      </Section>

      <div className="border-y bg-muted/40">
        <Section id="how" title="How an audit works" intro="Evidence before opinions: every finding cites a file and line, a route or a measurement, and says how confident it is.">
          <div className="grid gap-10 lg:grid-cols-[1fr_1fr]">
            <ol className="space-y-6">
              {steps.map((s, i) => (
                <li key={s.title} className="flex gap-4">
                  <span className="flex size-8 shrink-0 items-center justify-center rounded-full border bg-background text-sm font-semibold tabular-nums">
                    {i + 1}
                  </span>
                  <div>
                    <h3 className="font-semibold">{s.title}</h3>
                    <p className="mt-1 text-muted-foreground">{s.text}</p>
                  </div>
                </li>
              ))}
            </ol>
            <VerdictCard />
          </div>
        </Section>
      </div>

      <Section id="install" title="Install in a minute" intro="The same knowledge ships as an Agent Skill, an MCP server and single-file bundles for chat assistants.">
        <Tabs items={['Claude Code', 'MCP clients', 'Any Agent Skills client', 'Chat apps']} className="max-w-3xl">
          <Tab value="Claude Code">
            <CodeBlock title="In Claude Code">
              <Pre>
                <code>{'/plugin marketplace add youmssi/ux-expert\n/plugin install ux-expert@ux-expert'}</code>
              </Pre>
            </CodeBlock>
          </Tab>
          <Tab value="MCP clients">
            <CodeBlock title="mcp.json (Cursor, VS Code, Codex, Gemini CLI…)">
              <Pre>
                <code>{'{\n  "mcpServers": {\n    "ux-expert": { "command": "npx", "args": ["-y", "ux-expert-mcp@1"] }\n  }\n}'}</code>
              </Pre>
            </CodeBlock>
          </Tab>
          <Tab value="Any Agent Skills client">
            <CodeBlock title="From your project root">
              <Pre>
                <code>{'git clone --depth 1 --branch v1.1.0 https://github.com/youmssi/ux-expert /tmp/ux-expert\ncp -r /tmp/ux-expert/skills/ux-expert .claude/skills/ux-expert'}</code>
              </Pre>
            </CodeBlock>
          </Tab>
          <Tab value="Chat apps">
            <p className="text-sm">
              For ChatGPT, DeepSeek, Grok and other chat apps without skills or MCP, upload the bundle for your mode from the{' '}
              <a href={`${repoUrl}/releases/latest`} className="underline underline-offset-2">
                latest GitHub release
              </a>
              .
            </p>
          </Tab>
        </Tabs>
        <p className="mt-6 text-sm text-muted-foreground">
          Next: <Link href="/docs/getting-started/use-in-your-project" className="text-foreground underline underline-offset-2">use it in your project</Link>.
        </p>
      </Section>

      <div className="border-t bg-muted/40">
        <Section id="stacks" title="Knows your stack, from the source" intro="Stack packs record what a framework changes about UX findings. Each is read from the project's own repository at a recorded commit and re-verified every six months.">
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {catalogue.stacks.map(s => (
              <li key={s.id}>
                <Card className="h-full gap-2 py-5">
                  <CardHeader className="px-5">
                    <CardTitle className="text-base">
                      <Link href={`/docs/stacks/${s.id}`} className="hover:underline">
                        {s.name}
                      </Link>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="px-5 text-sm text-muted-foreground">
                    Verified against {s.verified.version} at <span className="font-mono">{s.verified.commit.slice(0, 7)}</span>,{' '}
                    {s.gotchas.length} gotchas{s.probes?.length ? `, ${s.probes.length} probes` : ''}
                    {'recipes' in s && Array.isArray(s.recipes) && s.recipes.length ? `, ${s.recipes.length} recipes` : ''}.
                  </CardContent>
                </Card>
              </li>
            ))}
          </ul>
        </Section>
      </div>

      <section className="border-t">
        <div className="mx-auto flex w-full max-w-6xl flex-col items-start gap-6 px-4 py-16 sm:px-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h2 className="text-2xl font-semibold tracking-tight">Give your agent a UX expert</h2>
            <p className="mt-2 text-muted-foreground">Open source: code under MIT, content under CC BY 4.0.</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link href="/docs" className={buttonVariants({ size: 'lg' })}>
              Read the docs
            </Link>
            <a href={repoUrl} className={cn(buttonVariants({ variant: 'outline', size: 'lg' }))}>
              View on GitHub
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}
