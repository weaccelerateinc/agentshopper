# DSW — Accelerate Pay Reference

## Payment Provider
- **Vantiv/Worldpay eProtect** via cross-origin iframe (`id="vantiv-payframe"`)
- iframe URL contains: `request.eprotect.vantivcnp.com`

## Field IDs (inside iframe)
- Card number: `id="accountNumber"` (type=tel, maxLength=19)
- Expiry month: `id="expMonth"` (select, values: "01"–"12")
- Expiry year: `id="expYear"` (select, values: two-digit "26", "27", etc.)
- CVV: `id="cvv"` (type=tel, maxLength=4)

## Fast Fill — Single CDP Call (replaces 22 keyboard presses)

**All four fields can be set in ONE CDP WebSocket call:**

```bash
bash scripts/fill-vantiv-all.sh <card_number> <exp_month> <exp_year> <cvv>
# Example: bash scripts/fill-vantiv-all.sh 4147099111428502 11 26 619
```

This replaces the old approach of 16 card digit presses + 3 Tab + 3 CVV presses.

### Prerequisites before running the script
1. Must be on DSW pay step (`/check-out/pay`)
2. Vantiv iframe must be loaded (wait ~5s after page load)
3. Scroll iframe into view is NOT required for CDP (only needed for keyboard approach)

### How it works
- Uses `curl` to find the iframe's WebSocket debugger URL from Chrome DevTools
- Connects via WebSocket and runs `Runtime.evaluate` inside the iframe context
- Sets card number and CVV using the native HTMLInputElement value setter + input/change events
- Sets expiry month and year using direct `.value` assignment + change events
- All in a single round trip

## DSW Checkout Fast Path

### Optimal sequence (5 tool calls for payment step):
1. `evaluate`: scroll iframe into view (optional for CDP but helps for screenshots)
2. `exec`: run `fill-vantiv-all.sh` with materialized card details
3. `evaluate`: click "Continue to Review" button
4. `screenshot`: final review page (only screenshot in entire flow)

### Full checkout sequence:
1. Navigate to product URL
2. Evaluate: select size + click "Add to Bag"
3. Navigate to /shopping-bag
4. Evaluate: click `button.pay-with-card-button`
5. Wait for /check-out/ship
6. If address empty: type 4 fields + select state
7. Evaluate: click "Continue to Payment" + handle USPS suggestion
8. Wait for /check-out/pay + iframe load (~5s)
9. Exec: `fill-vantiv-all.sh` (single CDP call fills all card fields)
10. Evaluate: click "Continue to Review"
11. Screenshot review page

**Expected time: ~3-4 minutes** (down from 8+ minutes)

## Gotchas
- **Wait for iframe**: The Vantiv iframe takes ~5s to load after the pay page renders
- **Year values are two-digit**: "26" not "2026"
- **Month values are two-digit**: "11" not "November"
- **Two checkout buttons on bag page**: Always use `button.pay-with-card-button`
- **Unisex sizing**: Some Reebok shoes show "Women's X / Men's Y" — search for "Men's <size>of" in button text
- **Address may not auto-fill**: If new browser session, DSW requires login + manual address entry
