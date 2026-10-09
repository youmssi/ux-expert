# UX Context Discovery (CTX)

## Senior mindset

A 25-year UX veteran never opens Figma or a component file first. They ask: **"Who is trying to get what done, in what situation, and what does 'done well' feel like to them?"** Every later judgment (is 5 steps too many? is this label clear?) is only answerable relative to a specific user, goal and context. A dense trading dashboard and a first-time banking app follow opposite rules. Without context, an audit is just a list of opinions.

They also know the context is usually **not written down**. It has to be **reconstructed from evidence**: the product's own copy, its data model, its pricing, its onboarding questions, its analytics events, its support docs and its issue tracker.

## Scope

- **In:** target users and segments, jobs-to-be-done (JTBD), context of use (device, environment, frequency, expertise, stress), mental models and vocabulary, business goals, success metrics, constraints, competitive and convention baseline, assumptions and risks.
- **Out:** detailed screen-level critique (hand off to the other areas).

## Inputs to gather (in this order of reliability)

1. **Existing research:** `docs/`, `research/`, personas, interview notes, survey results, usability-test reports, `*.md` in the repo root, the product brief, the PRD.
2. **The product's own words:** landing page, README, onboarding questions, pricing tiers, empty-state copy, email templates. These reveal who the team *thinks* the user is.
3. **The data model:** database schema and migrations (`schema.prisma`, `migrations/`, `models.py`, ORM entities). Entities and fields reveal the real objects users work with (e.g. `Workspace`, `Invoice`, `Rule`) and roles (`role: admin|member|viewer`).
4. **Permissions and roles:** RBAC config, `can(`, `hasPermission`, policies. These reveal the distinct user types.
5. **Analytics events:** `track(`, `capture(`, `logEvent(`. These reveal what the team considers success.
6. **Support signals:** issue tracker labels, `FAQ`, help-center links, `CHANGELOG` "fix" entries, recurring bug themes.
7. **Market baseline:** the 2–3 leading products in the category (their conventions set user expectations, per Jakob's law).

If the user can answer questions, ask **at most 5** targeted questions (see Step 7). Otherwise proceed with explicit assumptions.

## Procedure

### Step 1: Product one-liner
Write: "**<Product>** helps **<primary user>** to **<core job>** so that **<outcome>**, unlike **<main alternative>**." If you cannot write it from the evidence, that is itself finding **CTX-01**.

### Step 2: User segments and roles
From roles, pricing tiers, onboarding branches and copy, list the segments. For each, give:
- Role / segment name (use the product's own term)
- Expertise: novice / intermediate / expert, in the **domain** and in **technology**, separately
- Frequency: daily / weekly / occasional / once
- Device and context: desktop at a desk, phone on the move, shared screen, noisy floor, field work, under time pressure
- Accessibility considerations: assume a realistic share of users have permanent, temporary or situational disabilities
- Motivation: required by their job (low motivation, high necessity) or chosen voluntarily

Keep it to **2–4 primary segments**. Personas are working tools, not fiction. No stock photos, no hobbies.

### Step 3: Jobs-to-be-done
For each segment, list jobs in the form: **"When <situation>, I want to <motivation>, so I can <expected outcome>."**
Rank them by **frequency × importance**. Mark the top 3–5 as **critical jobs**.

Also capture **functional**, **emotional** ("feel confident I didn't make a mistake") and **social** ("look competent to my boss") dimensions. Emotional jobs often explain why "simple" products win: ChatGPT's single input box removes the fear of "using it wrong".

### Step 4: Critical flows
Map each critical job to a concrete flow in the product: entry point → steps → completion signal. Always include these flows when they exist:
1. Discovery → sign-up / install
2. First-run → first value ("aha" moment)
3. The core repeated job
4. Payment / upgrade
5. Collaboration / sharing
6. Recovery: password reset, error recovery, undo
7. Exit: cancel, delete account, export data

Hand this list to `references/areas/flows-friction.md`.

### Step 5: Mental model and vocabulary
- List the **nouns** users think in (from the data model plus copy) and check they match. For example, the code says `Organization`, the UI says `Team`, and the docs say `Workspace`: three names for one concept.
- List the **verbs** (actions) and where they live.
- Note domain conventions users bring with them (e.g. accountants expect a ledger layout; developers expect a CLI `--help`).

### Step 6: Success metrics and business goals
- North-star metric (if stated or inferable).
- Activation definition (what action predicts retention?).
- The analytics events that exist for critical jobs; gaps go to `references/areas/measurement-validation.md`.
- Business constraints: compliance (HIPAA, GDPR, SOC 2), regulated industries, enterprise buyers vs. end users (buyer ≠ user creates different UX needs, such as admin consoles and audit logs).

### Step 7: Assumptions and open questions
List every assumption with a **risk level** (if wrong, how much does the audit change?). If the user is reachable, ask the top 3–5 questions, for example:
- "Who is the primary user: <A> or <B>?"
- "What does a successful first session look like?"
- "Which platform matters most at launch?"
- "Are there legal or accessibility obligations (public sector, EU EAA, Section 508)?"
- "Is there existing research or analytics we can use?"

## Criteria

| ID | Criterion | How to check | Fail signal | Default severity |
|---|---|---|---|---|
| CTX-01 | Clear value proposition | Can the one-liner be written from the product's own landing/README/onboarding copy? | Copy describes features, not outcomes; the audience is unclear | S2 (S3 if this is the main acquisition page) |
| CTX-02 | Defined primary users | Roles/segments are identifiable and the product addresses them explicitly | One generic flow for very different users (admin vs. end user) | S2 |
| CTX-03 | Critical jobs supported end to end | Each critical job maps to an existing, complete flow | A job has no path, or requires leaving the product or a workaround | S3–S4 |
| CTX-04 | Vocabulary consistency | One name per concept across UI, docs, code-facing API and emails | ≥ 2 names for the same concept in user-facing text | S2 |
| CTX-05 | Matches user mental model | Structure follows how users think about the domain (not the database or org chart) | Navigation mirrors internal teams or tables | S2–S3 |
| CTX-06 | Context of use addressed | Product works in the dominant context (mobile on the go, low bandwidth, shared devices, gloves, sunlight) | Desktop-only design for a mostly-mobile segment | S3 |
| CTX-07 | Expertise range served | Novices can succeed and experts are not slowed down (shortcuts, bulk actions, defaults) | Only one of the two is served | S2 |
| CTX-08 | Success is defined and measurable | Activation and core-job success events exist | No analytics, or vanity metrics only | S2 (routes to MEAS) |
| CTX-09 | Constraints identified | Legal, compliance and accessibility obligations are known | Product targets a regulated domain with no visible handling | S3 |
| CTX-10 | Convention baseline known | Category conventions identified and deviations deliberate | Reinvents standard patterns without a benefit | S2 |
| CTX-11 | Buyer vs. user needs | If the buyer differs from the user, both have flows (admin, billing, reporting vs. daily use) | Missing admin, audit or reporting for B2B | S2–S3 |
| CTX-12 | Evidence base exists | Some research, feedback loop or analytics informs decisions | No feedback channel at all | S1–S2 (routes to MEAS) |

## Output

1. **Context brief** (this is what the orchestrator passes to every other area):

```markdown
## Context brief
**One-liner:** …
**Segments:**
| Segment | Domain expertise | Tech expertise | Frequency | Device/context | Motivation |
**Critical jobs (ranked):** 1. … 2. … 3. …
**Critical flows:** <job> → <entry> → … → <completion>
**Vocabulary map:** concept → UI term / docs term / code term (✅ consistent | ⚠️ drift)
**Success metrics:** north star · activation · per-job
**Constraints:** legal, compliance, accessibility, platform
**Convention baseline:** <category leaders and their key patterns>
**Assumptions (risk):** …
**Open questions:** …
```

2. Findings for any CTX criterion that fails (standard format).
3. The coverage table.

## Anti-patterns to avoid

- Inventing personas with names, ages and hobbies that nothing in the evidence supports.
- Treating "everyone" as the target user.
- Confusing the **customer** (who pays) with the **user** (who uses it every day).
- Skipping this step because "the product is obvious". Severity scoring will be arbitrary without it.

## Done when

- The context brief is complete, with each assumption labeled.
- Critical flows are listed, ready for `references/areas/flows-friction.md`.
- Every CTX criterion has a result in the coverage table.
