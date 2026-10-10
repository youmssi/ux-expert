# Collaboration (COLLAB)

## Senior mindset

Collaboration UX is **trust in shared state**. Every person must be able to answer, at any moment: *who can see this, who is here, what changed, and is my work safe?* A collaborative product fails worst not when it looks dated but when someone loses an hour of edits, or a private document turns out to be public.

Principles:
1. **Access is part of the object.** Who can see and edit is shown where the content is, not only in settings.
2. **Never lose work.** Concurrent and offline edits merge or conflict visibly; silent overwrite is a blocker.
3. **Attribution builds trust.** Who changed what, and when, with a way back.
4. **Signal over noise.** People follow shared work through notifications and feeds; volume without filtering makes them stop reading.

## Scope

- **In:** sharing and permissions on objects, invites and access requests, link sharing, presence and awareness, concurrent and offline editing, version history, comments and mentions, activity feeds, assignment and handoffs, external collaborators, what happens to content when people leave.
- **Out:** organization-wide administration, SSO and provisioning (→ ADMIN), notification channels and preferences (→ NOTIF), first-run invite as activation (→ ONB-14), generic conflict and offline states (→ STATE).

## Procedure

### Step 1: Model the shared objects
List each shared object type (document, project, board, record, thread) with its roles, sharing options (people, groups, link, public) and the default for a new object. Note where the default is broader than the creator would expect (COLLAB-04).

### Step 2: Walk the access lifecycle
For one object: share with a teammate → the invitee opens the link → a third person without access opens it → access is removed while the document is open. Check each screen against COLLAB-01, 03, 15. Check the backend enforces access on every request, not only the UI.

### Step 3: Test concurrency
With two sessions (two browsers or devices): edit the same field at once, edit while one is offline then reconnect, delete an item the other is editing. Record what each person sees. Silent loss is COLLAB-06 or COLLAB-14 at S4.

### Step 4: History, comments and mentions
- Version history: attributed, restorable, and restoring is itself undoable.
- Comments: anchored to the content, survive edits, can be resolved and reopened.
- Mentions: autocomplete only people who can see the content, or warn and offer to share.

### Step 5: Awareness and noise
Presence (avatars, cursors, "editing now") is visible but does not cover content. Activity feeds can be filtered by person, type and object. Collaboration notifications are batched (→ NOTIF-08).

### Step 6: People leaving
Remove a member who owns content. The content stays, ownership transfers to someone with a clear role, and links keep working.

## Criteria

<!-- BEGIN GENERATED criteria (collaboration) -->
<!-- Source: criteria/collaboration.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| COLLAB-01 | Access visible on the object | Users cannot tell who can see or edit what they are looking at | S2–S3 (S3 when private content is exposed; → TRUST-13) |
| COLLAB-02 | Roles explained in plain words | Role names with no statement of what each allows | S2 (→ ADMIN-05) |
| COLLAB-03 | Invite and request-access paths | "You don't have access" with no way to request it; invitee lands on a generic home page | S2–S3 (→ ONB-14, STATE-19) |
| COLLAB-04 | Link-sharing scope stated before sharing | Public link created by default, or its scope hidden behind the copy button | S3 (S4 when private data becomes public; → TRUST-13) |
| COLLAB-05 | Presence of others shown | Two people edit the same object without knowing it | S2 |
| COLLAB-06 | Concurrent edits never lose work | Last write wins silently and work is lost | S3–S4 (S4 when work is lost; → STATE-13) |
| COLLAB-07 | Change history with attribution and restore | No way to see who changed what, or to restore a previous version | S2–S3 |
| COLLAB-08 | Comments anchored to content | Comments detach or disappear when the content they point to is edited | S2 |
| COLLAB-09 | Mentions reach people who can see the content | Mentioning someone without access fails silently | S2 |
| COLLAB-10 | Collaboration notifications batched | One notification per edit or keystroke; no digest | S2 (→ NOTIF-08) |
| COLLAB-11 | Content survives member removal | Content orphaned or data lost when a member leaves or is removed | S3–S4 (S4 when data is lost; → ADMIN-09) |
| COLLAB-12 | Activity feed filterable | Every event in one unfiltered stream | S1–S2 |
| COLLAB-13 | Handoffs explicit | No assignee or status where work passes between people; unclear whose turn it is | S2 |
| COLLAB-14 | Offline edits sync or conflict visibly | Offline work lost silently on reconnect | S3–S4 (S4 when work is lost; → STATE-11) |
| COLLAB-15 | Access removal takes effect at once | A removed member keeps viewing or editing in an open session or through a token | S3 (→ TRUST-17) |
| COLLAB-16 | Awareness indicators do not obstruct | Other people's cursors or selections cover content and cannot be hidden | S1 |
| COLLAB-17 | External collaborators marked | No sign that a participant is outside the organization | S2–S3 (S3 in regulated or confidential work) |
<!-- END GENERATED criteria -->

## Gotchas

- Real-time libraries (Yjs, Automerge, Liveblocks) merge text and lists, not business rules: two people can still book the same slot or approve the same request. Check application-level conflicts separately.
- Toggling "offline" in browser devtools does not reproduce a sleeping laptop or a dropped mobile connection; reconnect after minutes, not seconds, before judging COLLAB-14.
- Access checks often live only in the UI. A removed member's open tab, cached page or API token may keep working; test the API directly for COLLAB-15.
- "Anyone with the link" links get pasted into public channels and indexed. Judge link scope by the data it exposes, not by how hidden the link looks.

## Output

- The shared-object table: object, roles, sharing options, default scope.
- The access lifecycle and concurrency test results, with what each participant saw.
- Findings in the standard format; the coverage table (COLLAB-01 … COLLAB-17).

## Done when

Every shared object type has its access model documented, the access lifecycle and concurrency tests are run (or marked not runnable with reduced confidence), and every case of possible lost work is either cleared or reported.
