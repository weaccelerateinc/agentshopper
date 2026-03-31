---
name: accelerate-pay
description: Fill credit card payment forms using Accelerate wallet materialization. Use when a checkout page, payment form, or any website asks for credit card number, expiry, and CVV — and the user wants to pay with Accelerate. Triggers on "pay with accelerate", "fill in card", "use accelerate", "enter payment", "fill payment", or when stopped at a payment step during checkout. Requires an active Accelerate session (auth via OTP).
---

# Accelerate Pay

Fill credit card fields on any website using materialized card details from the Accelerate wallet.

## Setup

1. **Configure** `references/config.md` with your Accelerate profile:
   - Phone number (for OTP)
   - First name, last name, email
   - Preferred payment source ID (from `node cli.js cards`)
2. **Install** the Accelerate CLI: `cd <repo>/accelerate && npm install`
3. **Authenticate** at least once to create a session

## Prerequisites

- Active Accelerate session (stored at `~/.agentshop/accelerate-session.json`)
- If session is expired or missing, re-authenticate first (see Auth Flow below)
- A visible payment form in the browser with card number, expiry, and CVV fields

## Merchant-Specific References

Before filling payment on a known merchant, read its reference file for the exact field IDs, tab order, and CDP commands:
- **DSW**: `references/dsw.md` — Vantiv eProtect iframe, keyboard + CDP fill sequence
- Add new merchant files as they are tested

## Quick Flow

1. Check session status
2. If not authenticated → run auth flow (OTP to user's phone)
3. Materialize payment for the order amount
4. Fill the card fields in the browser
5. Screenshot and confirm — do NOT submit payment unless user says so

## Auth Flow (only when session is expired)

```bash
cd <repo>/accelerate
node cli.js session-status
```

If expired or no session:

```bash
node cli.js auth-start --phone <PHONE> --first-name <FIRST> --last-name <LAST> --email <EMAIL>
```

Ask user for OTP (sent to their phone), then:

```bash
node cli.js auth-verify --phone <PHONE> --otp <CODE>
```

## Payment Materialization

### 1. Check session

```bash
cd <repo>/accelerate
node cli.js session-status
```

Confirm `is_authenticated: true`. If not, run auth flow above.

### 2. List cards (if needed)

```bash
node cli.js cards
```

Use the preferred card from `references/config.md`.

### 3. Materialize

```bash
node cli.js payment-materialize --payment-source-id <PAYMENT_SOURCE_ID> --amount-cents <AMOUNT>
```

Where `<AMOUNT>` is the order total in cents (e.g., $227.16 → `22716`).

The response returns:
- `cardNumber` — full card number to fill
- `expiry` — MM/YY format
- `cvv` — security code

### 4. Fill payment form in browser

Use the browser tool to type the materialized card details into the payment form fields:

- **Card Number**: Type the full `cardNumber` value
- **Expiry Month/Year**: Type or select from the `expiry` value (MM/YY)
- **Security Code / CVV**: Type the `cvv` value

#### Common field patterns

Different sites label card fields differently. Look for:
- Card number: "Card Number", "Credit Card Number", "Card number"
- Expiry: May be one field (MM/YY) or two separate fields (Month + Year)
- CVV: "Security Code", "CVV", "CVC", "Card Code"

#### Handling secure payment iframes (Vantiv, Stripe, etc.)

Many merchants use **cross-origin payment iframes** (Vantiv/Worldpay eProtect, Stripe Elements, etc.) that block normal DOM access. Use this approach:

**Step 1: Card number and CVV** — Click the iframe element, then use `press` key actions to type digits. Tab navigates between fields inside the iframe.

```
browser act: click selector="iframe#<IFRAME_ID>"
browser act: press key="Tab"  (focus card number)
browser act: press key="4"    (type each digit)
browser act: press key="1"
...
browser act: press key="Tab"  (move to next field)
```

**Step 2: Select/dropdown fields (expiry month/year)** — Keyboard `press` works for text inputs but NOT for `<select>` dropdowns inside cross-origin iframes. For those, use **CDP WebSocket** to execute JS directly inside the iframe:

1. Find the iframe's WebSocket URL:
```bash
curl -s http://127.0.0.1:18800/json | python3 -c "
import sys, json
for t in json.load(sys.stdin):
    if '<PAYMENT_PROVIDER_DOMAIN>' in t.get('url',''):
        print(t['webSocketDebuggerUrl']); break
"
```

2. Set select values via CDP:
```bash
node --experimental-websocket -e "
const ws = new WebSocket('<WS_URL>');
ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: \"(function(){var mo=document.getElementById('<MONTH_ID>');var yr=document.getElementById('<YEAR_ID>');mo.value='<MM>';mo.dispatchEvent(new Event('change',{bubbles:true}));yr.value='<YY>';yr.dispatchEvent(new Event('change',{bubbles:true}));return 'month='+mo.value+' year='+yr.value})()\"
    }
  }));
};
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if(msg.id===1){console.log(msg.result.value||JSON.stringify(msg.result));ws.close();process.exit(0);}
};
setTimeout(()=>{process.exit(1);},5000);
"
```

**Important:** Always wrap CDP expressions in IIFE `(function(){...})()` to avoid variable redeclaration errors across multiple evaluations.

**Known iframe providers and their field IDs:**
- **Vantiv/Worldpay eProtect**: iframe `id="vantiv-payframe"`, month `id="expMonth"`, year `id="expYear"` — see `references/dsw.md`
- **Stripe Elements**: Separate iframes per field — each has its own targetId

#### Billing address
If billing address is required, use the checkout profile from the checkout-assistant skill's `references/checkout-profile.json`.

### 5. Stop and confirm

After filling card fields:
- Take a screenshot of the final checkout/review page
- Report what was filled (last 4 digits only)
- Do NOT click "Place Order" / "Submit" / "Pay Now" unless the user explicitly asks

## Important Notes

- Materialized card numbers are **single-use** — if the checkout fails, re-materialize
- Session expires after ~1 hour — re-auth via OTP if needed
- Amount must match the actual checkout total in cents
- Never display the full card number in chat — only mention last 4 digits
- The `verification_payload` param is only needed if Accelerate requires re-verification of the physical card (rare)
