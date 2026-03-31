---
name: accelerate-pay
description: Fill credit card payment forms using Accelerate wallet materialization. Use when a checkout page, payment form, or any website asks for credit card number, expiry, and CVV — and the user wants to pay with Accelerate. Triggers on "pay with accelerate", "fill in card", "use accelerate", "enter payment", "fill payment", or when stopped at a payment step during checkout. Requires an active Accelerate session (auth via OTP to <FIRST_NAME>'s phone).
---

# Accelerate Pay

Fill credit card fields on any website using materialized card details from the Accelerate wallet.

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
2. If not authenticated → run auth flow (OTP to <FIRST_NAME>'s phone)
3. Materialize payment for the order amount
4. Fill the card fields in the browser
5. Screenshot and confirm — do NOT submit payment unless user says so

## Auth Flow (only when session is expired)

```bash
cd ~/. openclaw/workspace/skills/agent-shop/accelerate
node cli.js session-status
```

If expired or no session:

```bash
node cli.js auth-start --phone <PHONE> --first-name <FIRST_NAME> --last-name <LAST_NAME> --email <EMAIL>
```

Ask user for OTP (sent to <FIRST_NAME>'s phone), then:

```bash
node cli.js auth-verify --phone <PHONE> --otp <CODE>
```

## Payment Materialization

### 1. Check session

```bash
cd ~/.openclaw/workspace/skills/agent-shop/accelerate
node cli.js session-status
```

Confirm `is_authenticated: true`. If not, run auth flow above.

### 2. List cards (if needed)

```bash
node cli.js cards
```

<FIRST_NAME>'s preferred card: Capital One ending in 8502
- Payment source ID: `<PAYMENT_SOURCE_ID>`

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

**For DSW (Vantiv iframe):** Set ALL card fields in a single CDP call — no keyboard presses needed:
```bash
bash scripts/fill-vantiv-all.sh <card_number> <exp_month_2digit> <exp_year_2digit> <cvv>
```
Wait ~5s for the iframe to load after reaching `/check-out/pay`, then run the script. See `references/dsw.md` for the full fast path.

**For other merchants:** Follow the general approach below.

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
browser act: click selector="iframe#vantiv-payframe"
browser act: press key="Tab"  (focus card number)
browser act: press key="4"    (type each digit)
browser act: press key="1"
...
browser act: press key="Tab"  (move to next field)
```

**Step 2: Select/dropdown fields (expiry month)** — Keyboard `press` works for text inputs but NOT for `<select>` dropdowns inside cross-origin iframes. For those, use **CDP WebSocket** to execute JS directly inside the iframe:

1. List browser tabs to find the iframe's `targetId` (type=iframe, URL contains the payment provider domain)
2. Connect via CDP WebSocket and run `Runtime.evaluate`:

```bash
node --experimental-websocket -e "
const ws = new WebSocket('ws://127.0.0.1:18800/devtools/page/<IFRAME_TARGET_ID>');
ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: \"const m=document.getElementById('expMonth');if(m){m.value='<MM>';m.dispatchEvent(new Event('change',{bubbles:true}));'ok'}else{'not found'}\"
    }
  }));
};
ws.onmessage = (e) => {
  const msg = JSON.parse(e.data);
  if(msg.id===1){console.log(JSON.stringify(msg.result));ws.close();process.exit(0);}
};
setTimeout(()=>{process.exit(1);},5000);
"
```

Replace `<IFRAME_TARGET_ID>` with the iframe's targetId from `browser tabs`, and `<MM>` with the two-digit month (e.g., `11` for November).

**Known iframe providers and their field IDs:**
- **Vantiv/Worldpay eProtect**: `expMonth` (select), `expYear` (select), card number (input), CVV (input)
- **Stripe Elements**: Uses separate iframes per field — each has its own targetId

#### Billing address
If billing address is required, use the checkout profile from `skills/checkout-assistant/references/checkout-profile.json`.

### 5. Stop and confirm

After filling card fields:
- Take a screenshot
- Report what was filled
- Do NOT click "Place Order" / "Submit" / "Pay Now" unless the user explicitly asks

## Important Notes

- Materialized card numbers are **single-use** — if the checkout fails, re-materialize
- Session expires after ~1 hour — re-auth via OTP if needed
- Amount must match the actual checkout total in cents
- Never display the full card number in chat — only mention last 4 digits
- The `verification_payload` param is only needed if Accelerate requires re-verification of the physical card (rare)
