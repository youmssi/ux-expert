# UX laws, research results and numeric thresholds

A quick reference for areas. **Cite the source** when using a number in a finding. These numbers are guidelines; context can justify exceptions, but the exception must be argued.

Source IDs in brackets (e.g. [src:wcag22]) point to `references/sources.md`, which says how each one was verified. Never state the numbers of an **unconfirmed** source as fact.

## Psychology and interaction laws

| Law / effect | Statement | How to apply in an audit |
|---|---|---|
| **Fitts's law** (Fitts, 1954) | Time to reach a target grows with distance and shrinks with target size | Primary actions large and close to where attention is; destructive actions small and away from frequent ones; screen edges and corners are "infinitely large" targets on desktop |
| **Hick–Hyman law** (1952) | Decision time grows (logarithmically) with the number and complexity of choices | Count the options per decision point; group, default, or progressively disclose when there are more than ~5–7 equal-weight options |
| **Working memory limits** (Miller 1956 "7±2"; Cowan 2001 "about 4 chunks") | People hold only a few items in mind | Never make users remember information across screens; chunk codes and numbers (e.g. `4821 3390`) |
| **Jakob's law** (Nielsen) | Users spend most of their time on other products and expect yours to work the same way | Follow platform and category conventions unless a deviation is clearly better and taught |
| **Tesler's law** (conservation of complexity) | Some complexity cannot be removed, only moved | Ask whether complexity was moved to the system (good) or pushed to the user (bad) |
| **Postel's law** (robustness principle) | Be liberal in what you accept and conservative in what you send | Accept many input formats (phone numbers with spaces, dates); output one clear format |
| **Doherty threshold** (Doherty & Thadani, IBM 1982) [src:doherty-thadani-1982] | Productivity rises sharply when system response is under ~400 ms | Interactive feedback under 400 ms; acknowledge input instantly |
| **Response-time limits** (Miller 1968; Nielsen 1993) [src:nielsen-response-times] | 0.1 s feels instant; 1 s keeps flow of thought; 10 s is the limit of attention | < 0.1 s: no indicator. 0.1–1 s: subtle. 1–10 s: spinner or skeleton. > 10 s: progress plus the ability to cancel or run in the background |
| **Serial position effect** | First and last items are remembered best | Put the most important nav items first and last |
| **Von Restorff (isolation) effect** | The item that differs is remembered and noticed | Only one visually distinct primary action per view |
| **Peak–end rule** (Kahneman) | Experiences are judged by their peak and their end | Invest in success states, completion moments and graceful failure |
| **Zeigarnik effect** | Unfinished tasks are remembered | Progress indicators and checklists drive completion |
| **Goal-gradient effect** (Hull; Kivetz et al. 2006) | Motivation increases near the goal | Show progress; give a head start ("1 of 4 done") |
| **Aesthetic–usability effect** (Kurosu & Kashimura, 1995) | Attractive designs are perceived as easier to use | Visual polish affects trust; it does not excuse usability defects |
| **Law of proximity / common region / similarity** (Gestalt) | Close, enclosed or similar items are seen as groups | Spacing inside a group must be smaller than spacing between groups |
| **Choice overload** (Iyengar & Lepper, 2000) | Too many options reduce action | Curate defaults and recommended options |
| **Default effect** | Most users keep defaults | Defaults must be the safest and most common choice, and never against the user's interest |

## Usability research results commonly cited

- **5 users per round** find, on average, about 85 % of the problems one user group runs into, from Nielsen & Landauer's model with an average detection rate of about 0.31 [src:nielsen-landauer-1993]. It is an average: groups of five found 55–100 % in later work. Run several small rounds, use five per distinct user group, and use 20+ for quantitative measures.
- **First click:** a correct first click strongly predicts task success. The often-quoted "87 % versus 46 %" could not be confirmed [src:bailey-first-click], so use the direction, not the numbers.
- **F-pattern** scanning on text-heavy pages (NN/g eye-tracking, 2006, re-confirmed 2017). Users also show layer-cake, spotted and commitment patterns. Good headings and front-loaded words support scanning.
- **Form validation timing:** government design systems validate on submit by default and advise against validating when the user leaves a field [src:govuk-validation] [src:cms-validation]; studies report more errors when errors appear as soon as a field is left. The widely repeated "inline validation: 22 % more success" claim could not be confirmed [src:wroblewski-inline-2009].
- **System Usability Scale (SUS):** the average is about **68** (50th percentile); scores are not percentages [src:sauro-sus].
- **Banner blindness:** users ignore elements that look like ads (NN/g eye-tracking).

## Numeric thresholds

### Accessibility (WCAG 2.2)
| Criterion | Threshold | Level |
|---|---|---|
| 1.4.3 Contrast (text) | 4.5:1 normal text; 3:1 large text (≥ 24 px regular or ≥ 18.66 px bold) | AA |
| 1.4.6 Enhanced contrast | 7:1 normal; 4.5:1 large | AAA |
| 1.4.11 Non-text contrast | 3:1 for UI component boundaries, focus indicators, meaningful icons and chart elements | AA |
| 1.4.4 Resize text | Usable at 200% text zoom | AA |
| 1.4.10 Reflow | No 2-D scrolling at 320 CSS px wide (400% zoom at 1280) | AA |
| 1.4.12 Text spacing | No loss of content with line-height 1.5, paragraph spacing 2× font size, letter spacing 0.12×, word spacing 0.16× | AA |
| 2.5.8 Target size (minimum) | 24×24 CSS px, or enough spacing around it | AA |
| 2.5.5 Target size (enhanced) | 44×44 CSS px | AAA |
| 2.4.11 Focus not obscured (minimum) | A focused element is not fully hidden by sticky UI | AA |
| 2.4.13 Focus appearance | Focus indicator area ≥ a 2 CSS px perimeter, with 3:1 change contrast | AAA |
| 2.2.1 Timing adjustable | Users can turn off, adjust or extend time limits (≥ 10× or a 20 s warning) | A |
| 2.3.1 Three flashes | No more than 3 flashes per second | A |
| 3.3.7 Redundant entry | Don't ask for the same info twice in one process | A |
| 3.3.8 Accessible authentication (minimum) | No cognitive function test (e.g. transcribing a code by memory, puzzles) without an alternative; allow paste and password managers | AA |

### Platform touch targets
- Apple HIG: **44×44 pt** minimum.
- Material Design: **48×48 dp** minimum, with about 8 dp between targets.

### Typography
- Body text on web: **16 px** minimum for most products (with exceptions for dense pro tools, at around 13–14 px, if they are zoomable and have strong contrast).
- Line length: **45–75 characters** (about 66 ideal) for body copy [src:bringhurst-line-length].
- Line height: **1.4–1.6** for body text; 1.1–1.3 for headings.
- A type scale of about **4–6 sizes** covers almost all product UI.

### Layout
- **4 pt / 8 pt spacing scale** (4, 8, 12, 16, 24, 32, 48, 64…).
- Content max width for reading: about **600–760 px**.
- Common breakpoints: ~**360–414** (phone), **768** (tablet portrait), **1024** (tablet landscape / small laptop), **1280–1440** (desktop).

### Performance (Core Web Vitals, judged at the 75th percentile of real users)
| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | ≤ 2.5 s | ≤ 4.0 s | > 4.0 s |
| INP (Interaction to Next Paint) | ≤ 200 ms | ≤ 500 ms | > 500 ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

### Motion
- Micro-interactions **100–200 ms**; panels and modals **200–300 ms**; large transitions ≤ **500 ms**.
- Ease-out for entering, ease-in for exiting.
- Respect `prefers-reduced-motion`.

### Content
- Error message anatomy: **what happened + why (if useful) + what to do next**.
- Button labels: verb + object ("Create invoice"), usually ≤ 3 words.
- Notifications and toasts: visible long enough to read. A rough guide is ~**1 s per 10–15 words, minimum 4–5 s**. Never auto-dismiss errors or anything with an action that users need.

### Localization
- Plan for translated text to be about **130 %** of the English length for text over 70 characters, and **200–300 %** for strings up to 10 characters (labels, buttons) [src:w3c-text-size].
