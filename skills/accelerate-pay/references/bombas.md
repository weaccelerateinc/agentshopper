# Bombas — Accelerate Pay Reference

## Payment Provider
- **Shopify Payments (Stripe-backed)** — standard Shopify checkout card form
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
2. If "Credit card" option is not selected, click it (may default to Shop Pay or Amazon Pay)
3. Fill card number, expiry, CVV using standard keyboard input
4. Click "Review order" or equivalent
5. Screenshot the review/confirmation page

## Gotchas
- **Amazon Pay / PayPal prominence**: Bombas may prominently display Amazon Pay and PayPal express buttons — scroll past to the standard card form
- **Shop Pay overlay**: If Shop Pay prompt appears, click "Pay with credit card" instead
- **Expiry format**: Type digits only (e.g., "1126") — Shopify auto-inserts the slash
- **3D Secure**: Some cards may trigger Stripe 3DS verification — pause for manual intervention
- **Single-use card**: Materialize a new card if checkout needs to be retried
- **Standard Shopify (not Plus)**: Checkout UI may differ slightly from Shopify Plus stores — fewer customization features, but card fields are the same
