# Glossier — Accelerate Pay Reference

## Payment Provider
- **Shopify Payments (Stripe-backed)** — standard Shopify checkout card form
- Card fields rendered inline on the Shopify checkout Payment step (NOT in a cross-origin iframe)

## Field Identification
Shopify checkout card fields use standard HTML inputs:
- Card number: `input[name="number"]` or `input[placeholder*="Card number"]`
- Cardholder name: `input[name="name"]` (may or may not appear)
- Expiry date: `input[name="expiry"]` or `input[placeholder*="Expiration"]` (format: MM / YY)
- CVV: `input[name="verification_value"]` or `input[placeholder*="Security code"]`

**Note**: Shopify periodically updates its checkout DOM. If selectors fail, use `find` or `read_page` to locate card form fields dynamically.

## Fill Strategy
Shopify Payments uses standard HTML inputs (not cross-origin iframes), so standard browser automation works:
1. Click the card number field
2. Type the materialized card number
3. Tab to expiry, type MM/YY
4. Tab to CVV, type CVV
5. Verify all fields populated correctly

No CDP WebSocket workaround needed.

## Checkout Fast Path

### Optimal sequence (payment step):
1. Ensure Shopify checkout is on the Payment step
2. If "Credit card" option is not already selected, click it (Shopify may default to Shop Pay)
3. Fill card number, expiry, CVV using standard keyboard input
4. Click "Review order" or equivalent
5. Screenshot the review/confirmation page

## Gotchas
- **Shop Pay overlay**: Shopify may prompt for Shop Pay first — click "Pay with credit card" or equivalent
- **Email pop-up on checkout**: Glossier's email capture pop-up may appear even during checkout — dismiss it
- **Express checkout buttons**: Google Pay, Apple Pay, PayPal appear above — scroll past to standard card form
- **Expiry format**: Type digits only (e.g., "1126" for November 2026) — Shopify auto-inserts the slash
- **3D Secure**: Some cards may trigger Stripe 3DS verification — pause for manual intervention
- **Single-use card**: Materialize a new card if checkout needs to be retried
