# Warby Parker — Accelerate Pay Reference

## Payment Provider
- **Stripe (direct integration)** — Warby Parker integrates with Stripe directly, not via Shopify Payments
- Card fields may be rendered via Stripe Elements (iframe-based) or inline depending on checkout version

## Field Identification
Warby Parker's custom checkout may use Stripe Elements, which renders card fields inside iframes:
- Look for iframes with `src` containing `js.stripe.com/v3`
- Card number: `input[name="cardnumber"]` or Stripe Element iframe for card number
- Expiry: `input[name="exp-date"]` or Stripe Element iframe for expiry (format: MM / YY)
- CVV: `input[name="cvc"]` or Stripe Element iframe for CVC

**Note**: If Stripe Elements are used, each field lives in its own iframe. This requires either keyboard input focused on each iframe, or CDP WebSocket approach to execute inside each iframe context.

## Fill Strategy
Check whether card fields are inline or inside Stripe Element iframes:

**If inline (standard HTML inputs):**
1. Click the card number field
2. Type the materialized card number
3. Tab to expiry, type MM/YY
4. Tab to CVV, type CVV digits

**If Stripe Elements (iframe-based):**
1. Locate each Stripe Element iframe via `read_page` or DOM inspection
2. Click into the card number iframe
3. Type card number via keyboard simulation (Stripe Elements intercept typed input)
4. Click into expiry iframe, type MM/YY
5. Click into CVV iframe, type CVV
6. Verify masked values appear in each field

## Checkout Fast Path

### Optimal sequence (payment step):
1. Ensure checkout is on the Payment step (may follow a Prescription step)
2. Select "Credit card" payment method if multiple options shown
3. Fill card fields via keyboard input (iframe or inline)
4. Click "Review Order" or equivalent
5. Screenshot the review page

## Gotchas
- **Prescription step may precede payment**: Warby Parker checkout includes a prescription verification step for eyeglasses — the payment step comes after
- **Stripe Elements iframes**: Each card field may be in its own iframe — cannot tab between them, must click into each one
- **3D Secure**: Stripe may trigger 3DS verification pop-up — pause for manual intervention if it appears
- **Single-use card**: Materialize a new card if checkout needs to be retried
- **Non-prescription items**: Sunglasses and accessories skip the prescription step and go directly to payment
