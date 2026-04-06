# Victoria's Secret — Accelerate Pay Reference

## Payment Provider
- **Comenity Bank** processes VS credit card transactions
- Standard credit card payments likely use a mainstream processor (Stripe, Braintree, or similar)
- Card fields may be rendered inline or within an iframe depending on the payment path

## Field Identification
Inspect the VS checkout payment step for card input fields:
- Card number: Look for `input[name*="cardNumber"]` or `input[id*="cardNumber"]`
- Cardholder name: `input[name*="nameOnCard"]` or `input[id*="nameOnCard"]`
- Expiry month: `select[name*="expMonth"]` or `input` (may be dropdown or text)
- Expiry year: `select[name*="expYear"]` or `input` (may be dropdown or text)
- CVV: `input[name*="cvv"]` or `input[name*="securityCode"]`

**Note**: If fields are inside an iframe, use CDP WebSocket approach to fill (similar to DSW's Vantiv handler). Use `read_page` or browser DevTools to identify the exact structure.

## Fill Strategy
1. Navigate to the VS checkout Payment step
2. Decline any VS credit card application prompts — select standard credit card payment
3. Locate card fields (check if inline or inside iframe)
4. If inline: standard keyboard input works (click field, type value, tab to next)
5. If iframe: use CDP WebSocket to execute inside iframe context
6. Fill card number, name, expiry, CVV
7. Verify fields are populated correctly

## Checkout Fast Path

### Optimal sequence (payment step):
1. Ensure checkout is on Payment step
2. Dismiss VS credit card promotional prompt if shown
3. Select "Credit Card" or "Debit Card" payment option
4. Dismiss Klarna/Zip BNPL prompts if they overlay the form
5. Fill card fields
6. Click "Review Order" or equivalent
7. Screenshot review page

## Gotchas
- **VS Credit Card push**: Checkout aggressively promotes the Victoria's Secret credit card — always decline and choose standard card payment
- **BNPL overlays**: Klarna and Zip may present modals or inline options — dismiss or scroll past to standard card form
- **Comenity vs standard**: The payment form for VS credit card holders is DIFFERENT from the standard credit card form — ensure you're on the standard payment path
- **Expiry format**: May use separate month/year dropdowns instead of a single MM/YY field — check the DOM structure
- **Billing address**: VS may require billing address entry at the payment step if it differs from shipping — use checkout-profile data
- **Single-use card**: Materialize a new card if checkout needs to be retried
