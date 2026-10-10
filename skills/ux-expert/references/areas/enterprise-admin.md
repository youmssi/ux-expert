# Enterprise Administration (ADMIN)

## Senior mindset

The admin is a **second user with a different job**: keep the organization secure, compliant and within budget, usually under time pressure and with little patience for exploration. Admin UX failures are expensive in a specific way: one wrong click locks out a whole company, leaves a former employee with access, or adds a surprise to the invoice.

Principles:
1. **No lockouts.** Changes that can block sign-in (SSO, 2FA policies) are tested before they are enforced, and there is always a way back.
2. **Leavers lose access everywhere.** Deprovisioning covers accounts, sessions and tokens.
3. **Preview before impact.** Every change that affects many people or money shows who and how much first.
4. **Evidence on demand.** Audit logs answer *who did what, when, from where*, with before and after values.

## Scope

- **In:** admin console structure, SSO (SAML, OIDC) setup and enforcement, provisioning and deprovisioning (SCIM, directory sync, just-in-time), roles and permissions, org policies, bulk operations, audit logs, seats and org billing, usage limits, org data export and retention, domain verification, admin-managed API keys.
- **Out:** sharing of individual objects (→ COLLAB), personal security settings (→ TRUST-15, TRUST-17), checkout and plan purchase (→ COMM), developer API design (→ DX).

## Procedure

### Step 1: Map admin jobs
List the admin's top jobs: add and remove people, set up SSO, change roles, set policies, answer "who accessed X?", manage seats and invoices, export data. For each, find the screen and count steps.

### Step 2: SSO and lockout safety
Walk the SSO setup: configuration, test sign-in, enforcement, and recovery. Check: enforcement is impossible before a successful test (ADMIN-02); an owner can still sign in if the identity provider fails (ADMIN-03); the order of steps cannot strand the only owner.

### Step 3: Joiners, movers, leavers
- Joiner: invited or provisioned with a least-privilege role (ADMIN-06).
- Mover: role change takes effect immediately and is logged.
- Leaver: removed in the directory → account deactivated, sessions ended, personal tokens revoked, content kept (ADMIN-04, COLLAB-11).

### Step 4: Roles and policies
Is there a role matrix? Do custom roles preview their effective permissions? Do policies say whom they affect and from when, and do affected members see why they are blocked (ADMIN-10, ADMIN-16)?

### Step 5: Bulk, destructive and billing actions
Bulk import: per-row validation and a partial-failure report. Deletion of members or workspaces: impact summary, typed confirmation, grace period. Seat changes: cost and proration preview (ADMIN-11).

### Step 6: Audit and data
Trigger a few security-relevant events (role change, policy change, export) and find them in the audit log with actor, time, target, IP or device, and before/after values. Check org export and retention settings.

## Criteria

<!-- BEGIN GENERATED criteria (enterprise-admin) -->
<!-- Source: criteria/enterprise-admin.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| ADMIN-01 | Admin console separate and findable | Admin settings mixed into personal settings, or hidden from admins | S2 (→ IA-16) |
| ADMIN-02 | SSO tested before it is enforced | Enforcing SSO without a successful test sign-in; the setup can lock everyone out | S3–S4 (S4 when the organization can be locked out) |
| ADMIN-03 | Break-glass access | No owner can sign in when the identity provider fails or is misconfigured | S3 |
| ADMIN-04 | Deprovisioning removes access | Removing a user in the directory leaves their account, sessions or tokens active | S3 (→ COLLAB-15) |
| ADMIN-05 | Roles and effective permissions visible | No role matrix; custom roles saved without a preview of what they allow | S2–S3 |
| ADMIN-06 | Least-privilege defaults | New members join as admins or with full access by default | S3 |
| ADMIN-07 | Bulk operations validated per row | Bulk import or invite fails as a whole, or partly, with no per-row report | S2–S3 |
| ADMIN-08 | Audit log for security-relevant events | No audit log, or entries without actor, time, target and before/after values | S2–S3 |
| ADMIN-09 | Destructive admin actions guarded | Workspace or member deletion with no impact summary or grace period, and data lost | S3–S4 (S4 when data is lost; → TRUST-14) |
| ADMIN-10 | Policies state their scope and timing | Org-wide policy (2FA, sharing limits) applied with no notice to the people it affects | S2–S3 |
| ADMIN-11 | Seats and charges previewed | Seat changes charged with no preview of cost, proration or who holds a seat | S3 (→ COMM-13, TRUST-07) |
| ADMIN-12 | Usage against limits visible | Limits reached with no prior warning or usage view | S2 (→ STATE-21) |
| ADMIN-13 | Organization data export and retention | No org-level export; retention not configurable or not stated | S2–S3 (→ TRUST-10) |
| ADMIN-14 | No single admin as a point of failure | Only one admin possible; ownership cannot be transferred | S2 |
| ADMIN-15 | Domain capture announced | Personal accounts on a company domain absorbed into the organization without notice | S3 |
| ADMIN-16 | Members see the policies that apply to them | Members blocked by a policy with no explanation or admin contact | S2 (→ STATE-19) |
| ADMIN-17 | API keys and tokens governed | Keys cannot be listed, scoped, expired or revoked by admins | S3 (→ DX) |
<!-- END GENERATED criteria -->

## Gotchas

- Just-in-time (JIT) provisioning creates accounts at first sign-in but never removes them; JIT alone is not deprovisioning (ADMIN-04).
- SCIM deactivation often leaves existing sessions and personal API tokens valid until they expire. Check token revocation in code, not only the user status.
- Audit logs that say "settings updated" without the setting and its old and new values do not support an investigation; judge ADMIN-08 on content, not presence.
- "Admin" in a small-team plan and "admin" in an enterprise plan are often different roles with the same name. Check which one the audited flow uses.

## Output

- The admin jobs table with screens and step counts.
- The SSO and joiner–mover–leaver walkthroughs with their results.
- Findings in the standard format; the coverage table (ADMIN-01 … ADMIN-17).

## Done when

The admin jobs are mapped, lockout and deprovisioning paths are verified (or marked unverified with reduced confidence), and every bulk, destructive and billing action is checked for a preview.
