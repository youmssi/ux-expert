# Notification Systems (NOTIF)

## Senior mindset

Every notification spends the user's attention. Spend it well and people come back on time; spend it badly and they turn notifications off, which also silences the security alert you will need them to see later. A senior designs notifications as a **system**: an inventory of types, each with a reason, an audience, a channel matched to urgency, and a control.

Principles:
1. **Earn the permission.** Ask for push in context, after the user sees why it helps; the system prompt usually appears once [src:apple-user-notifications] [src:android-notification-permission].
2. **Urgency picks the channel.** Security and money events reach people; promotions wait politely.
3. **Every type is controllable,** except the few that must not be (receipts, security), and those are never used for marketing.
4. **One event, one message.** Batch, digest and deduplicate.

## Scope

- **In:** the notification inventory, channels (in-app, push, email, SMS), permission requests, preferences and unsubscribe, batching and digests, timing and time zones, deep links, read state, interruption levels and Android channels, notification actions, lock-screen privacy, delivery monitoring.
- **Out:** the wording of each message (→ CONT-17, CONT-18), lifecycle and onboarding sequences (→ ONB-15), consent rules for marketing in general (→ TRUST), toasts as UI feedback (→ INT-14).

## Procedure

### Step 1: Build the inventory
Search for senders: email templates, push payloads, in-app notification creation, SMS providers (`sendgrid`, `postmark`, `resend`, `ses`, `firebase-admin`, `apns`, `expo-notifications`, `twilio`, `novu`, `knock`). For each type record: trigger, audience, channel(s), transactional or marketing, controllable or not, owner. No inventory is itself NOTIF-01.

### Step 2: Channel versus urgency

| Urgency | Examples | Channel |
|---|---|---|
| Act now, security or money | sign-in from a new device, payment failed | push or SMS **and** email; in-app on next visit |
| Act soon | mention, assignment, approval request | push or in-app, with a digest fallback |
| For information | weekly summary, tips, product news | email or in-app, opt-in |

Flag mismatches both ways (NOTIF-02, NOTIF-12).

### Step 3: Permission and preferences
- Push permission: requested after a user action that shows the value, never at first launch (NOTIF-03). After a denial: explain and deep-link to system settings (NOTIF-04).
- Preferences: per type and per channel (NOTIF-05). Unsubscribing from marketing keeps transactional messages (NOTIF-06).
- Bulk email: one-click unsubscribe headers and a visible link (NOTIF-07) [src:rfc8058-one-click].

### Step 4: Volume and timing
Simulate a busy day: ten comments on one object, a burst of status changes. Count messages per channel. Check batching, digests, quiet hours and the recipient's time zone (NOTIF-08, NOTIF-09).

### Step 5: Landing and state
Open each notification type: it lands on the item with context (NOTIF-10); reading it anywhere clears it everywhere (NOTIF-11); an in-app center keeps what toasts drop (NOTIF-14).

### Step 6: Mobile specifics (if applicable)
Interruption level per type (iOS passive, active, time-sensitive, critical) [src:apple-user-notifications]; one Android channel per type (NOTIF-13); safe notification actions (NOTIF-15); sensitive content hidden on the lock screen (NOTIF-16).

## Criteria

<!-- BEGIN GENERATED criteria (notifications) -->
<!-- Source: criteria/notifications.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| NOTIF-01 | Notification inventory | No list of notification types with trigger, audience, channel and owner | S2 |
| NOTIF-02 | Channel matches urgency | Security alerts only in-app; promotions sent as push or SMS | S2–S3 |
| NOTIF-03 | Push permission asked in context | OS permission prompt on first launch, before any value is shown | S2–S3 (→ ONB-16) |
| NOTIF-04 | Denied permission recoverable | After a denial the feature fails silently; no path to system settings | S2 |
| NOTIF-05 | Preferences per type and channel | Notifications are all on or all off | S2 |
| NOTIF-06 | Transactional and marketing messages separated | Unsubscribing from marketing stops receipts or security alerts, or marketing is sent without consent as "transactional" | S2–S3 (→ TRUST-21) |
| NOTIF-07 | One-click unsubscribe for bulk email | Unsubscribing needs a sign-in or several steps; no List-Unsubscribe header pair | S3 (→ TRUST-21) |
| NOTIF-08 | Batching and digests | A burst of separate notifications for one chain of events | S2 |
| NOTIF-09 | Timing respects the recipient | Non-urgent messages sent at night in the recipient's time zone | S2 (→ I18N-13) |
| NOTIF-10 | Deep links land on the subject | Tapping a notification opens the home screen instead of the item | S2 |
| NOTIF-11 | Read state consistent across channels | Badges and unread counts stay after the item is read elsewhere | S1–S2 |
| NOTIF-12 | Interruption level honest | Promotions marked time-sensitive or high importance | S2–S3 |
| NOTIF-13 | Android channels per notification type | One channel for everything; users cannot mute one type | S2 |
| NOTIF-14 | In-app notification center | Important notices appear only as toasts that disappear | S2 (→ INT-14) |
| NOTIF-15 | Notification actions safe | Destructive or paying actions available from a notification without confirmation | S3 |
| NOTIF-16 | Sensitive content hidden on lock screens | Health, financial or private message content shown on the lock screen by default | S3 |
| NOTIF-17 | Delivery monitored | No tracking of bounces, failures or opt-outs for critical messages | S2 (→ LAUNCH-15) |
| NOTIF-18 | Content says what happened and what to do | Generic "You have a new notification" | S1–S2 (→ CONT-17) |
<!-- END GENERATED criteria -->

## Gotchas

- On iOS, requesting authorization again after a denial returns the stored answer without a prompt [src:apple-user-notifications]. An "Enable notifications" button that calls the API again does nothing; it must open Settings.
- On Android 13+, notifications are off by default for new installs. An app targeting 12L or lower gets the permission dialog automatically, usually at startup, when it creates its first channel [src:android-notification-permission]; check `targetSdkVersion` before blaming the code for NOTIF-03.
- Preference pages often control only marketing email. Check push and in-app types too, and that transactional types are labeled as always on.
- Email providers' "unsubscribe" handling may live only in the provider dashboard; search the provider config, not just the code, before reporting NOTIF-07.

## Output

- The notification inventory table, with channel and control per type.
- The volume simulation: messages per channel for a busy day.
- Findings in the standard format; the coverage table (NOTIF-01 … NOTIF-18).

## Done when

Every notification type is in the inventory with its channel and control, the permission and unsubscribe paths are walked, and a busy-day simulation is recorded.
