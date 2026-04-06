# Away — Accelerate Pay Reference

## Payment Provider
- **Shopify Payments (Stripe-backed)** — standard Shopify Plus checkout card form
- Klarna also available as BNPL option — ignore Klarna and use standard card path
- Card fields rendered inline on the Shopify checkout Payment step (NOT in a cross-origin iframe)

## Field Identification
Standard Shopify checkout card fields:
- Card number: `input[name="number"]` or `input[placeholder*="Card number"]`
- Cardholder name: `input[name="name"]` (may or may not appear)
- Expiry date: `input[name="expiry"]` or `input[placeholder*="Expiration"]` (format: MM / YY)
- CVV: `input[name="verification_value"]` or `input[placeholder*="Security code"]`

**Note**: Shopify periodically updates its checkout DOM. If selectors fail, use `find` or `read_page` to locate card form fields dynamically.

## Fill Strategy
Standard Shopify Payments HTML inputs — standard browser automation works:
1. Click the card number field
2. Type the materialized card number
3. Tab to expiry, type MM/YY
4. Tab to CVV, type CVV
5. Verify all fields populated correctly

No CDP WebSocket workaround needed.

## Checkout Fast Path

### Optimal sequence (payment step):
1. Ensure Shopify checkout is on the Payment step
2. Dismiss Klarna BNPL prompt if it appears (select "Credit card" option)
3. Fill card number, expiry, CVV using standard keyboard input
4. Click "Review order" or equivalent
5. Screenshot the review/confirmation page

## Gotchas
- **Klarna BNPL overlay**: Klarna Pay-in-4 option may be prominently displayed — select standard "Credit card" instead
- **Shop Pay / Apple Pay**: Express checkout buttons appear above — scroll past to standard card form
- **Referral discount auto-apply**: After entering email, a referral discount may auto-apply and change the total — verify the amount matches expectations before filling card
- **Expiry format**: Type digits only (e.g., "1126") — Shopify auto-inserts the slash
- **3D Secure**: Some cards may trigger Stripe 3DS verification — pause for manual intervention
- **Single-use card**: Materialize a new card if checkout needs to be retried
- **No prepaid gift cards**: Away does not accept prepaid gift cards — ensure the Accelerate materialized card is not flagged as prepaid
