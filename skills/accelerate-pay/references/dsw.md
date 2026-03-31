# DSW — Accelerate Pay Reference

## Payment Provider
- **Vantiv/Worldpay eProtect** via cross-origin iframe (`id="vantiv-payframe"`)
- iframe URL contains: `request.eprotect.vantivcnp.com`

## Field Tab Order (inside iframe)
1. Card Number (text input) — auto-focused after first Tab from iframe click
2. Expiry Month (select dropdown) — `id="expMonth"`, values: `"01"` through `"12"`
3. Expiry Year (select dropdown) — `id="expYear"`, values: two-digit years `"26"`, `"27"`, etc.
4. Security Code / CVV (password-type input)

## Fast Fill Sequence

### 1. Card number + CVV via keyboard press
```
browser act: click selector="iframe#vantiv-payframe"
browser act: press key="Tab"
# Type card number one digit at a time with press
browser act: press key="4"
browser act: press key="1"
... (all 16 digits)
# Skip month/year with Tabs (fix via CDP after)
browser act: press key="Tab"  → month
browser act: press key="Tab"  → year
browser act: press key="Tab"  → CVV
# Type CVV digits
browser act: press key="6"
browser act: press key="1"
browser act: press key="9"
```

### 2. Expiry month + year via CDP WebSocket
Find the iframe targetId:
```bash
curl -s http://127.0.0.1:18800/json | python3 -c "
import sys, json
for t in json.load(sys.stdin):
    if 'eprotect' in t.get('url',''):
        print(t['webSocketDebuggerUrl']); break
"
```

Set month and year (use IIFE to avoid redeclaration errors):
```bash
node --experimental-websocket -e "
const ws = new WebSocket('<WS_URL_FROM_ABOVE>');
ws.onopen = () => {
  ws.send(JSON.stringify({
    id: 1,
    method: 'Runtime.evaluate',
    params: {
      expression: \"(function(){var mo=document.getElementById('expMonth');var yr=document.getElementById('expYear');mo.value='<MM>';mo.dispatchEvent(new Event('change',{bubbles:true}));yr.value='<YY>';yr.dispatchEvent(new Event('change',{bubbles:true}));return 'month='+mo.value+' year='+yr.value})()\"
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

Replace `<MM>` with two-digit month (e.g., `11`) and `<YY>` with two-digit year (e.g., `26`).

### 3. Click Continue to Review
```
browser act: evaluate → find button with text "Continue to Review" → click
```

## DSW Checkout Notes
- **Checkout URL**: Pay step is at `/check-out/pay`
- **Two checkout buttons on bag page**: Always use `button.pay-with-card-button` to avoid PayPal popup
- **10% welcome code**: Applied on the bag page under "Enter offer code" — some items (Nike) are excluded from promos

## Gotchas
- **Variable redeclaration**: If running multiple CDP evaluations in the same iframe session, use IIFE `(function(){...})()` wrappers to avoid `SyntaxError: Identifier has already been declared`
- **Year values are two-digit**: `"26"` not `"2026"`
- **Month values are two-digit**: `"11"` not `"November"`
- **Keyboard press works for text inputs but NOT for selects** inside the iframe — always use CDP for dropdowns
