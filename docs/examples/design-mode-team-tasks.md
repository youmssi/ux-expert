# Example: design mode on a sample brief

This is a worked example of `references/design-mode.md`. It is also the
reference output for the design-mode evals (UXE-10).

**Input brief:** *Teamly is a web app where small teams (3–15 people) share and
track tasks. Draft stories: TEAM-1 Sign up, TEAM-2 Create the first project,
TEAM-3 Invite teammates. Launch in English and French. EU customers.*

---

# UX requirements: Teamly

## 1. Frame and context brief

**One-liner:** Teamly helps **small-team leads** to **get everyone's tasks in
one shared place** so that **nothing falls through the cracks**, unlike chat
threads and spreadsheets.

- **Product type:** `web-app` (desktop first, usable on phones).
- **Locales:** `en`, `fr`. **Legal:** EU (GDPR consent, EAA accessibility).
- **Segments:** team lead (sets up and invites; weekly-to-daily use; medium tech
  skills); team member (joins by invitation; daily use; low motivation to learn a
  new tool).
- **Critical jobs:** 1. Lead gets the team's tasks into one place. 2. Member sees
  what they must do today. 3. Lead sees what is late.
- **Activation (assumption to validate):** a project with ≥ 3 tasks and ≥ 1
  invited teammate who accepted, within 7 days [ONB-01, MEAS-03].

## 2. Critical flows

**Sign-up → first value (lead)**

| # | Step | Inputs | Decisions | Notes |
|---|---|---|---|---|
| 1 | Sign up | Email + password, or Google/Microsoft SSO | 1 (method) | Name and company deferred [FORM-01, ONB-05] |
| 2 | Create first project | Project name (prefilled "My team") | 0–1 (template) | Templates offered, blank allowed [ONB-10] |
| 3 | Add first tasks | Task titles | 0 | Inline add, Enter to add the next one [FORM-24] |
| 4 | Invite teammates | Emails (paste a list) | 0 | Skippable, reminder later [ONB-08] |

**Targets:** 4 steps, 2 required fields before the first task, 1 seam (email
verification, non-blocking [ONB-06]); first task created in under 2 minutes.
Removed from the draft: the "company size" and "role" questions at sign-up,
which personalize nothing [ONB-07].

## 3. Stories

#### UX requirements: TEAM-1 Sign up

**User and job:** a team lead wants to start using Teamly without commitment, so
they can try it with their real tasks.
**Flow position:** sign-up → first value, step 1 of 4. **Areas:** FORM, TRUST, ONB, STATE, A11Y, CONT, INT

| Where | What the user sees and can do |
|---|---|
| Sign-up page | SSO buttons (Google, Microsoft) and an email + password form; link to sign in |
| After submit | Lands directly in "Create your first project"; a banner asks to verify the email |

**UX acceptance criteria**

- [ ] The form asks only for email and password; name is asked later, when the first comment is posted [FORM-01, ONB-05]
- [ ] Google and Microsoft SSO are offered above the form [ONB-05, TRUST-15]
- [ ] Every field has a visible label above it; the placeholder never replaces the label [FORM-02]
- [ ] Email and password fields use `autocomplete="email"` and `"new-password"`; paste is allowed and password managers can save the credentials [FORM-06, FORM-16, A11Y-25]
- [ ] Password rules (at least 15 characters, no composition rules, per NIST SP 800-63B-4) are shown before typing; a show/hide toggle exists [FORM-16]
- [ ] Errors appear on submit, next to each field, and say how to fix it ("Enter an email like name@company.com"); focus moves to the first error, and each error clears as soon as the field is corrected [FORM-09, FORM-10, FORM-11, CONT-06]
- [ ] "Email already registered" offers "Sign in" and "Reset password" links, and keeps the typed email [STATE-08, FLOW-15]
- [ ] Network or server error: the form keeps its input and shows a retry message; the button is never left spinning [FORM-12, STATE-05]
- [ ] The submit button reads "Create account", shows a loading state and cannot submit twice [FORM-14, FORM-15]
- [ ] Email verification does not block use: the user lands in the product with a dismissible banner and a "Resend" link [ONB-06]
- [ ] The marketing-email checkbox is unchecked by default and separate from accepting the Terms [TRUST-01, TRUST-11]
- [ ] The whole form works with the keyboard only, and errors are announced to screen readers [A11Y-02, A11Y-13]
- [ ] No CAPTCHA puzzle; abuse is handled by rate limiting or an invisible check [FORM-18]
- [ ] All copy exists in English and French; the French labels fit without truncation at 320 px width [I18N-07, RESP-02]

**Measured by:** `signup_started`, `signup_completed` with `method`, and `signup_error` with a `reason` [MEAS-02, MEAS-06]

**Open decisions:** see D1.

#### UX requirements: TEAM-2 Create the first project

**User and job:** a new lead wants to see their team's work in Teamly quickly, so
they can judge whether it is worth inviting the team.
**Flow position:** step 2–3 of 4. **Areas:** ONB, FLOW, STATE, FORM, CONT, A11Y, INT, LAY

| Where | What the user sees and can do |
|---|---|
| First-run screen | One question, "What is your team working on?", with a prefilled name, 3 templates and "Start blank" |
| Project board | Template tasks or an empty board with an inline "Add a task" field focused |

**UX acceptance criteria**

- [ ] The first-run screen has one primary action ("Create project"); templates are secondary [ONB-09, LAY-02]
- [ ] The project name is prefilled ("My team") and editable later; creating needs no other input [FORM-08, FLOW-03]
- [ ] Templates show a preview of their tasks before they are chosen [ONB-10, FLOW-05]
- [ ] Empty board: explains in one sentence what to add and focuses the "Add a task" field [STATE-02, CONT-08]
- [ ] Enter adds a task and keeps focus in the field for the next one [FORM-24, FLOW-16]
- [ ] A task title of 200+ characters wraps without breaking the board [STATE-14, TYP-13]
- [ ] Loading the board shows a skeleton shaped like task cards; no blank screen [STATE-04]
- [ ] If saving a task fails, it stays in the list marked "Not saved" with Retry; nothing is lost [STATE-07, STATE-08, INT-07]
- [ ] No product tour on first visit; at most one dismissible tip at the "Add a task" field [ONB-11, ONB-12]
- [ ] Keyboard: every action (create, add, edit, delete) is reachable, and focus is visible [A11Y-02, A11Y-04]
- [ ] Deleting a task can be undone for 10 seconds from the toast; no confirmation dialog [INT-19, FLOW-19]

**Measured by:** `project_created` with `template`, `task_created`, and time from sign-up to first task [ONB-02, MEAS-02]

**Open decisions:** none.

#### UX requirements: TEAM-3 Invite teammates

**User and job:** a lead wants teammates in the project without chasing them, so
the whole team's tasks live in one place.
**Flow position:** step 4 of 4. **Areas:** ONB, FORM, CONT, TRUST, STATE, A11Y, I18N

| Where | What the user sees and can do |
|---|---|
| Invite dialog | Paste or type emails, see who will join, send |
| Invitee's email | The project name, who invited them, one "Join <project>" button |
| Invitee's first screen | The project they were invited to, with their name prefilled from SSO when available |

**UX acceptance criteria**

- [ ] The field accepts a pasted list separated by commas, spaces or new lines, and shows each address as a removable chip [FORM-07]
- [ ] Invalid addresses are marked individually, with the reason; valid ones are not blocked [FORM-10]
- [ ] The dialog states what invitees will see ("They will see all tasks in Marketing") [TRUST-13]
- [ ] Inviting is skippable; a reminder appears on the board after 2 days, once [ONB-08, TRUST-05]
- [ ] The send button reads "Send 3 invites" with the count; success names who was invited [CONT-03, CONT-09]
- [ ] The email subject is "Ana invited you to Marketing on Teamly", in the invitee's language when known [CONT-18, I18N-02]
- [ ] The join link opens the invited project directly after sign-up or sign-in, even on another device [ONB-14, FLOW-11]
- [ ] An expired or already-used invite shows who to ask for a new one, with a "Request access" button [FLOW-12, STATE-19]
- [ ] Inviting an email that is already a member says so instead of sending a duplicate [STATE-08]
- [ ] The dialog traps focus, closes with Esc and returns focus to "Invite" [INT-11, A11Y-06]

**Measured by:** `invite_sent` with `count`, `invite_accepted`, and accept rate within 7 days [ONB-02, MEAS-03]

**Open decisions:** see D2.

## 4. Open product decisions and missing stories

```
[INTERACTIVE STEP] D1. Can visitors try Teamly before signing up?
- Option A — Guest board stored locally, converted at sign-up: fastest time-to-value [ONB-04, ONB-03]; more build work, data migration on sign-up.
- Option B — Sign-up first (current draft): simpler; one more step before value.
Recommendation: B for launch, A as an experiment once activation is measured, because the sign-up is already 1 step with SSO.

[INTERACTIVE STEP] D2. Can members invite others, or only leads?
- Option A — Anyone can invite: faster spread, risk of unwanted members [TRUST-13].
- Option B — Leads only, members can request: more control, slower spread.
Recommendation: A with a lead-visible member list and removal, because teams of 3–15 rarely need gatekeeping.
```

**Missing stories found:** password reset [FLOW-14, TRUST-16]; account deletion
and data export [TRUST-10]; email-verification resend and expiry [FLOW-12];
notification settings for invite reminders [CONT-17, TRUST-21].

## 5. UX Definition of Done (every story)

From `select_criteria.py --product web-app --phase build`, grouped:

- [ ] **States:** every fetch has loading, empty, error and retry states; no infinite spinner; errors are caught and reported [STATE-04, STATE-05, STATE-07, STATE-10, STATE-23]
- [ ] **Accessibility:** keyboard operable, visible focus, labels and names, status messages announced, contrast ≥ 4.5:1 for text and ≥ 3:1 for UI, targets ≥ 24×24 CSS px, axe clean [A11Y-01, A11Y-02, A11Y-04, A11Y-10, A11Y-13, A11Y-15, A11Y-20]
- [ ] **Forms:** labels associated, correct input types and autocomplete, focus on the first error, no double submit [FORM-03, FORM-05, FORM-06, FORM-11, FORM-15]
- [ ] **Design system:** tokens for color, spacing and type; existing components reused [DS-03, DS-05, DS-06]
- [ ] **i18n:** every string externalized with ICU plurals; dates and numbers through `Intl` [I18N-01, I18N-04, I18N-12, I18N-14]
- [ ] **Performance:** LCP ≤ 2.5 s and INP ≤ 200 ms on the story's routes (mobile profile) [PERF-01, PERF-02]
- [ ] **Measurement:** the story's events are tracked, with no personal data in properties [MEAS-02, MEAS-05]
- [ ] **Evidence:** screenshots at 375 px and 1440 px, in English and French, attached to the PR

## 6. Traceability (excerpt)

| Criterion | Stories |
|---|---|
| FORM-01 Only necessary fields | TEAM-1 |
| ONB-06 Non-blocking verification | TEAM-1 |
| ONB-10 Templates, samples or examples | TEAM-2 |
| ONB-14 Invite flow preserves context | TEAM-3 |
| TRUST-13 Visibility and sharing clarity | TEAM-3, D2 |
| STATE-08 Errors actionable | TEAM-1, TEAM-2, TEAM-3 |
