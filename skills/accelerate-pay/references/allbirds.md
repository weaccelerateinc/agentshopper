# Allbirds — Accelerate Pay Reference

## Payment Provider
- **Shopify Payments** (Stripe-based) — standard credit card form
- Card fields rendered inline on the Shopify checkout Payment step (NOT in a cross-origin iframe)

## Field Identification
Shopify checkout card fields use standard HTML inputs within the checkout page:
- Card number: `input[name="number"]` or `input[placeholder*="Card number"]`
- Cardholder name: `input[name="name"]` (may or may not appear depending on Shopify config)
- Expiry date: `input[name="expiry"]` or `input[placeholder*="Expiration"]` (format: MM / YY)
- CVV: `input[name="verification_value"]` or `input[placeholder*="Security code"]`

**Note**: Shopify periodically updates its checkout DOM structure. If the selectors above fail, use `find` or `read_page` to locate the card form fields dynamically.

## Fill Strategy
Since Shopify Payments uses standard HTML inputs (not a cross-origin iframe like Vantiv), standard browser automation works:
1. Click the card number field
2. Type the materialized card number
3. Tab to expiry, type MM/YY
4. Tab to CVV, type CVV
5. Verify all fields populated correctly

No CDP WebSocket workaround needed (unlike DSW's Vantiv iframe).

## Checkout Fast Path

### Optimal sequence (payment step):
1. Ensure Shopify checkout is on the Payment step
2. If "Credit card" payment option is not already selected, click it (Shopify may default to Shop Pay)
3. Fill card number, expiry, CVV using standard keyboard input
4. Click "Review order" or equivalent button
5. Screenshot the review/confirmation page

## Gotchas
- **Shop Pay overlay**: Shopify may prompt for Shop Pay first — click "Pay with credit card" or equivalent to show standard card fields
- **Express checkout buttons**: Apple Pay / Google Pay / PayPal buttons appear above — scroll past to standard card form
- **Expiry format**: Shopify expects MM / YY with the space and slash auto-inserted — just type digits (e.g., "1126" for November 2026)
- **3D Secure**: Some cards may trigger Stripe 3D Secure verification pop-up — if so, pause for manual intervention
- **Single-use card**: If checkout fails after card fill, materialize a new card number before retrying
