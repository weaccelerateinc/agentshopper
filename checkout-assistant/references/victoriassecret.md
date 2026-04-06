# Victoria's Secret Checkout Flow

## Purpose
Use this note when logging into an existing Victoria's Secret account, building a cart with one or more products, applying the best available offer, and stopping at payment.

## Platform
- Custom e-commerce (VS Group / Bath & Body Works family)

## URLs
- Product pages: `https://www.victoriassecret.com/us/<category>/<product-slug>`
- Cart (Bag): `https://www.victoriassecret.com/us/bag`
- Checkout: `https://www.victoriassecret.com/us/checkout`

## Browser Mode
Use a headed browser for best results.

## Product Variant Behavior
- Color: selected via color swatch buttons on the product page
- Size: selected via size buttons (e.g., "XS", "S", "M", "L", "XL" for apparel; or band/cup for bras)
- "Add to Bag" activates after both color and size are selected
- Bras have a specialized size selector: band size (30–40) + cup size (AA–DDD) — both must be chosen
- For multi-item carts, repeat the product-page variant selection and add-to-bag for each item

## Common UI Issues
- **Marketing pop-ups**: Aggressive email capture and promotional modals — dismiss them immediately
- **Cookie banner**: Accept cookies if prompted
- **BNPL options**: Klarna and Zip offered at checkout — ignore these and use standard card payment path
- **VS credit card prompts**: Checkout may promote applying for a VS credit card (via Comenity Bank) — decline and use standard payment
- **"Sold Out" variants**: Some size/color combos show as unavailable — skip and try an alternative
- **Multi-step checkout**: Shipping → Payment → Review

## Login Guidance
- Prefer existing saved session if logged in
- Otherwise use the VS account created by account-creator
- Login at https://www.victoriassecret.com/us/account/signin
- Guest checkout is available but logging in is preferred for saved addresses and member offers
- If CAPTCHA appears during login, pause for manual solve

## Coupon / Reward Strategy
- Check structured deals from deal-digest for victoriassecret.com promo codes
- VS frequently runs promotions (e.g., "Buy 2 Get 1 Free" on certain categories) — these apply automatically
- Promo code field is typically visible in the cart (bag) page or early in checkout
- Enter code and click "Apply"
- Some offers are auto-applied and cannot be combined with promo codes — compare totals
- VS Rewards members may have earned rewards that appear during checkout — use the best single discount

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the checkout shows the **Payment** step with credit card entry fields visible. Capture a screenshot and report back.
