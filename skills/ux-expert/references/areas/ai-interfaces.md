# AI Interfaces (AI)

## Senior mindset

AI features break a core assumption of classic UX: **the system is not deterministic**. The same input can produce different outputs, outputs can be confidently wrong, and capabilities are invisible. A senior designs AI UX around **calibrated trust**: users should trust the AI exactly as much as it deserves, no more and no less.

Their guiding sources: Microsoft's **Guidelines for Human-AI Interaction** (18 guidelines across initially, during interaction, when wrong, and over time) and Google's **People + AI Guidebook**. Their recurring questions:
1. **Does the user know what it can and can't do?** (Capability and limitation clarity.)
2. **Does the user stay in control?** (Stop, edit, undo, approve before consequential actions.)
3. **What happens when it's wrong?** (Easy to verify, easy to correct, easy to dismiss.)
4. **Does it improve over time, and does the user understand what it remembers?**

ChatGPT's interface embodies several of these: an empty state with example prompts (capability discovery), streaming output (perceived speed), a Stop button (control), Edit and Regenerate (correction), a disclaimer that it can make mistakes (calibration), and thumbs up/down (feedback).

## Scope

- **In:** entry points and discoverability, onboarding to AI capabilities, input UX (prompt box, attachments, suggestions, templates, parameters), latency and streaming, interruption, output rendering (Markdown, code, tables, citations), grounding and sources, uncertainty and limitation messaging, error and refusal handling, correction loops (edit, regenerate, versions/branches), agentic actions (previews, approvals, scopes, audit logs, undo), feedback mechanisms, memory and personalization transparency, privacy and training disclosure (→ TRUST-12), safety and abuse handling, rate limits, quotas and cost visibility, model/provider failure fallbacks, evaluation and monitoring hooks.
- **Out:** model quality itself (but flag UX that hides poor quality), general chat layout polish (→ LAY/TYP).

## Procedure

### Step 1: Inventory AI features
List each AI touchpoint: what it does, the trigger (user-initiated vs. proactive), the model/provider, inputs (user data used), outputs, whether it **acts** (writes data, sends messages, spends money, runs code) or only **suggests**, and the latency profile.

Code probes: SDK imports (`openai`, `@anthropic-ai/sdk`, `anthropic`, `ai`/`@ai-sdk/*`, `langchain`, `llamaindex`, `@google/generative-ai`, `ollama`), `stream: true`, `messages: [`, `tools:`/`functions:`, system prompts in code.

### Step 2: Expectations and discoverability (before use)
- The entry point is where the user needs help (in context), not only a separate "AI" tab.
- The empty state shows **what it's good at**, with example prompts/actions tailored to the user's context.
- Limitations are stated in plain words where relevant (knowledge cutoff, can't access X, may be inaccurate). They are short and placed in context, not buried in a modal.
- The AI is clearly labeled as AI (users know when content is AI-generated).

### Step 3: Input UX
- A multi-line input that grows; Enter to send and Shift+Enter for a new line (or the platform convention); the send state is clear; the input is preserved on error.
- Attachments: supported types and limits stated; upload progress; files visible in context.
- Prompt assistance: suggestions, templates, slash commands, or structured inputs for common tasks (users shouldn't need prompt engineering skills for core jobs).
- For generation features, structured controls (tone, length, format) instead of making users phrase everything.

### Step 4: Latency and streaming
- Time to first token/feedback ≤ ~1 s (an immediate "thinking" indicator if the model is slower); stream the output for long responses.
- For multi-step or agentic work: show **progress steps** ("Searching docs… Reading 3 files… Drafting"), so waiting is explainable.
- **Stop** button available during generation; partial output is kept.
- For long tasks: run in the background, notify on completion, and allow leaving the page.
- Avoid layout jumps while streaming (auto-scroll that respects the user scrolling up; → LAY-15).
- Screen readers: announce on completion or in sensible chunks, not every token (→ A11Y-13).

### Step 5: Output quality UX
- Rendering: Markdown, code blocks with copy buttons and language labels, tables, math if relevant; no raw Markdown artifacts.
- **Grounding:** citations/sources linked to the exact passage when answers draw on documents or the web; distinguish "from your data" vs. "general knowledge".
- **Uncertainty:** hedging where appropriate; confidence cues for classifications or extracted fields (highlight low-confidence fields for review).
- **Verification aids:** show the inputs used, diffs for edits (before/after), and previews for actions.
- Actionable outputs: copy, insert, apply, export; apply-to-document shows a diff and supports undo.

### Step 6: Correction and control
- **Edit** the previous prompt and **Regenerate**; ideally keep versions/branches so users can compare and go back.
- Users can **dismiss** suggestions easily (proactive suggestions should be low-friction to ignore: HAX guideline 8).
- Users can **refine** with follow-ups that keep context.
- **Scoped control:** users can choose what context the AI uses (which files, which workspace) and see what it used.

### Step 7: Agentic actions (if the AI acts)
- **Preview before act** for consequential actions (sending email, modifying data, purchases, deleting, running code, external API calls); an explicit approval step with a clear description of the effects.
- Permission scopes visible and adjustable ("can read calendar, can't send email"); least privilege by default.
- An **audit log** of actions taken, with **undo/rollback** where possible.
- Rate and blast-radius limits (bulk actions confirmed with counts → STATE-18).
- An interruption mechanism (stop mid-run) with a clear state of what was and wasn't done.

### Step 8: Failure, refusal and degradation
- Model/provider errors are differentiated: timeout, rate limit/quota ("You've reached today's limit; resets at 14:00"), content refusal (explained politely, with what is possible instead), context too long (a suggestion to shorten or split), and provider outage (fallback model or a clear message; the rest of the product keeps working → STATE-22).
- Retry keeps the user's input and attachments.
- Hallucination mitigation in UX: for high-stakes domains (health, legal, finance), add explicit verification prompts and sources, and avoid auto-applying outputs.

### Step 9: Feedback, memory and privacy
- Feedback: thumbs up/down with an optional reason; a "report a problem" flow; the user is told what happens with the feedback.
- Memory/personalization: the user can see what the AI remembers, edit and delete it, and turn it off; temporary/incognito mode where relevant.
- Data use: clear disclosure of whether prompts and content are stored, for how long, and whether they are used for training; enterprise/admin controls (→ TRUST-12).
- Sensitive data: warnings or redaction when users paste secrets/PII into prompts (in enterprise contexts).

### Step 10: Cost, limits and transparency
- Usage limits and credits visible before users hit them (a progress meter), with a clear upgrade or wait path.
- Model selection (if offered) explained in user terms (speed vs. quality), with a sensible default.
- If outputs are costly or slow, set expectations before starting ("This may take ~2 minutes").

## Criteria

<!-- BEGIN GENERATED criteria (ai-interfaces) -->
<!-- Source: criteria/ai-interfaces.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| AI-01 | Capabilities discoverable | Blank prompt box with no guidance; AI hidden from the moment of need | S2 |
| AI-02 | Limitations communicated in context | No limitation messaging; or only legal boilerplate | S2 |
| AI-03 | AI content labeled | Users can't tell AI-generated from human or system content | S2–S3 |
| AI-04 | Input usability | No multi-line; input lost on error; unclear send behavior | S2 |
| AI-05 | Prompt assistance / structured inputs | Core jobs need prompt-engineering skill | S2 |
| AI-06 | Fast first feedback and streaming | Long blank waits; no streaming for long outputs | S2–S3 |
| AI-07 | Progress for multi-step/agentic work | Opaque long runs | S2 |
| AI-08 | Stop / interrupt | Cannot stop generation or agent runs | S2–S3 |
| AI-09 | Output rendering quality | Raw Markdown; code without copy; broken tables | S1–S2 |
| AI-10 | Grounding and citations | Claims from data or the web without sources | S2–S3 (S3 high-stakes) |
| AI-11 | Uncertainty and verification aids | No diffs or previews; low-confidence fields not flagged | S2–S3 |
| AI-12 | Edit, regenerate and versions | No way to correct or compare | S2 |
| AI-13 | Easy dismissal of suggestions | Intrusive proactive AI that is hard to ignore | S2 |
| AI-14 | Context transparency and control | Users can't see or choose what context was used | S2 |
| AI-15 | Preview and approval before consequential actions | Agents act without confirmation | S4 |
| AI-16 | Scoped permissions and audit log | Broad permissions; no log of actions | S3 |
| AI-17 | Undo/rollback for AI actions | Irreversible AI changes | S3–S4 |
| AI-18 | Differentiated AI errors | One generic error for timeout, limit, refusal and outage | S2 |
| AI-19 | Graceful refusals | Refusals that are unexplained or preachy, with no alternative path | S2 |
| AI-20 | Provider-failure fallback | Whole feature or page breaks when the provider fails | S2–S3 |
| AI-21 | Feedback loop | No way to rate or report outputs | S1–S2 |
| AI-22 | Memory transparency and control | Hidden memory; no view, edit or delete | S3 |
| AI-23 | Data-use disclosure and controls | Training/storage use undisclosed; no admin controls for B2B | S3 (→ TRUST) |
| AI-24 | Limits and cost visibility | Users hit limits without warning | S2 |
| AI-25 | High-stakes domain safeguards | Health/legal/finance outputs auto-applied, without sources or verification | S3–S4 |
| AI-26 | Accessible AI output | Streaming spams screen readers; no keyboard access to actions | S2–S3 |
| AI-27 | Evaluation and monitoring hooks | No logging of failures, feedback or quality signals | S2 (→ MEAS) |
<!-- END GENERATED criteria -->

## Gotchas

- Streams can fail after partial output. Check what the UI shows when the stream breaks halfway, not only when the request fails.
- A disclaimer alone does not meet AI-10 or AI-11. Grounding and verification aids are separate requirements.
- Model and provider names in code are not UX. Judge what users see, control and can recover from.

## Output

- An AI feature inventory (feature · acts or suggests · data used · latency · stakes).
- A HAX-style checklist summary per feature (before / during / when wrong / over time).
- Findings in the standard format; the coverage table (AI-01 … AI-27).

## Done when

Every AI touchpoint is inventoried with its stakes, every acting feature has its approval/undo path verified, failure modes (timeout, limit, refusal, outage) are tested or traced, and data-use transparency is assessed.
