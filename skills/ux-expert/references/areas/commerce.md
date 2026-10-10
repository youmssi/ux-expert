# Commerce and Payments (COMM)

## Senior mindset

Payment is the moment of **highest intent and highest anxiety**. The user has decided; now any surprise (a new fee, a cleared form, an unclear charge) turns intent into doubt. A senior audits commerce for two things at once: *can people pay without friction*, and *does every number and promise hold up*?

Principles:
1. **No surprises.** The total, the renewal and the refund terms are known before the pay button.
2. **Never lose the order.** Errors, bank challenges and retries keep everything the user entered.
3. **Charge exactly once.** Double charges are the fastest way to lose a customer and gain a chargeback.
4. **Honest prices.** A discount compares against a price that was really charged [src:eu-price-indication].

## Scope

- **In:** cart, checkout, guest checkout, payment methods and fields, strong customer authentication (3-D Secure), payment errors, double-charge prevention, order review, confirmation and receipts, discounts and promo codes, plan upgrades and downgrades, billing self-service, failed renewals (dunning), refunds and returns, order status, mobile store purchases.
- **Out:** pricing page and plan comparison (→ LAUNCH-05), trial, renewal and cancellation terms and dark patterns (→ TRUST-06 to TRUST-09), general form design (→ FORM), org seats (→ ADMIN-11).

## Procedure

### Step 1: Map the purchase paths
List every way money moves: first purchase, upgrade, add-on, renewal, refund. For each, record steps, where the total is first shown in full, and where the user must sign in.

### Step 2: Walk checkout with test cards
Use the provider's test mode (Stripe, Adyen, Braintree, Paddle and app stores all provide one):
- a successful card, then a declined card, then a card that triggers a 3-D Secure challenge;
- double-click the pay button; reload during processing; go back after paying.
Record what the user sees and whether entered data survives (COMM-06, 07, 08).

### Step 3: Price integrity
Compare the price shown at each step with what the backend charges. Check strike-through and "was" prices against price history, and fees added late (COMM-01, COMM-11).

### Step 4: After the purchase
Confirmation screen and receipt email (COMM-10), order status (COMM-17), refund path (COMM-16), invoices and payment method updates (COMM-14).

### Step 5: Subscriptions
Upgrade and downgrade previews with proration and effective date (COMM-13). Failed renewal: warning, grace period and update link before access ends (COMM-15).

### Step 6: Mobile (if applicable)
Store purchases restorable on a new device (COMM-19); the store's purchase sheet is not wrapped in extra confirmation screens.

## Criteria

<!-- BEGIN GENERATED criteria (commerce) -->
<!-- Source: criteria/commerce.yaml. Edit the YAML, then run scripts/generate.py. -->
| ID | Criterion | Fail signal | Default severity |
|---|---|---|---|
| COMM-01 | Full price known before the final step | Taxes, fees or shipping first appear at the last step | S3 (→ TRUST-07) |
| COMM-02 | Guest checkout or deferred account | Account creation forced before payment without a reason | S2–S3 |
| COMM-03 | Cart persistent and editable | Cart emptied by reload or sign-in; quantities not editable | S2–S3 |
| COMM-04 | Payment methods fit the market | Card only where wallets or local methods dominate | S2–S3 (→ I18N-23) |
| COMM-05 | Payment fields easy to complete | No cc- autocomplete tokens, wrong keyboard, spaces in card numbers rejected | S2–S3 (→ FORM-05, FORM-06, FORM-07) |
| COMM-06 | Payment authentication inside the flow | A 3-D Secure or bank challenge loses the order or returns to an empty page | S3–S4 (S4 when the payment cannot be completed) |
| COMM-07 | Payment errors specific and recoverable | Generic error after a decline; entered details cleared | S3 (→ STATE-08) |
| COMM-08 | No double charge | Retry or double tap creates a second charge | S3–S4 (S4 when money is taken twice; → FORM-15) |
| COMM-09 | Order review before paying | No summary of items, delivery and total before the pay button | S2–S3 (→ TRUST-14) |
| COMM-10 | Confirmation and receipt | No order number or next steps on screen; no receipt by email | S2–S3 (→ CONT-18) |
| COMM-11 | Honest reference prices | Strike-through price that was never charged; in the EU, not the lowest price of the prior 30 days | S3 (→ TRUST-06) |
| COMM-12 | Promo code field does not distract | Large empty promo field at payment; invalid codes fail without a reason | S1–S2 |
| COMM-13 | Plan changes previewed | Upgrade or downgrade charges without showing amount, proration and effective date | S3 (→ TRUST-08) |
| COMM-14 | Billing self-serve | Invoices, payment method or billing details only through support | S2 |
| COMM-15 | Failed renewals handled before access ends | Access removed at a failed renewal with no warning, grace period or update link | S3 |
| COMM-16 | Refund and return terms findable | Terms not shown before purchase or in order history | S2 (→ LAUNCH-14) |
| COMM-17 | Order status visible | No status or tracking after purchase | S2 |
| COMM-18 | Trust at the moment of payment | Unknown processor, mismatched business name or no secure context on the payment step | S2–S3 (→ TRUST-20) |
| COMM-19 | Store purchases restorable on mobile | Digital purchases cannot be restored on a new device | S3 |
<!-- END GENERATED criteria -->

## Gotchas

- Disabling the pay button does not prevent double charges on network retries. Look for an idempotency key on the payment request (COMM-08); providers support one.
- Hosted payment elements handle the 3-D Secure challenge, but custom code after the redirect often loses the order state. Test with the provider's 3-D Secure test card, not a plain success card.
- Prices displayed from front-end config or a CMS can drift from the prices the backend charges. Compare both sources before reporting COMM-01 as fine.
- App store rules on digital goods and external payment links differ by region and change often. Check the current guidelines instead of assuming a rule.

## Output

- The purchase-path table with steps and where the full total first appears.
- The test-card matrix: card × outcome × what the user saw × data kept.
- Findings in the standard format; the coverage table (COMM-01 … COMM-19).

## Done when

Every purchase path is mapped, the test-card matrix is run (or marked not runnable with reduced confidence), and every displayed price is traced to what is charged.
