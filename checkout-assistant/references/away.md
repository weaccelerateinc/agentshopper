# Away Checkout Flow

## Purpose
Use this note when logging into an existing Away account, building a cart with one or more items, applying the best available discount, and stopping at payment.

## Platform
- Shopify Plus

## URLs
- Product pages: `https://www.awaytravel.com/products/<product-variant>-<color>`
- Carry-on collection: `https://www.awaytravel.com/collections/carry-on-luggage`
- Cart: `https://www.awaytravel.com/cart`
- Login: `https://www.awaytravel.com/login`

## Browser Mode
Use a headed browser.

## Product Variant Behavior
- Color: selected via color swatch buttons on the product page (e.g., Jet Black, Coast Blue, Brick)
- Size: Away suitcases come in defined sizes (Carry-On, Bigger Carry-On, Medium, Large) — these are typically separate product pages, not variants on one page
- Material: Some products have hardside vs softside variants — these may also be separate product pages
- "Add to Cart" button should be active once color is selected
- Bundling: Away offers luggage sets as separate products — navigate to the set product page if buying a bundle
- For multi-item carts, repeat product page → color selection → add-to-cart for each item

## Common UI Issues
- **Referral discount overlay**: Away's referral program may show a banner or pop-up offering $40 off — dismiss unless you want to apply it
- **ID.me verification prompt**: Away offers hero discounts (military, first responder, student, healthcare) via ID.me — this may appear as a banner. Ignore for standard checkout
- **Cookie banner**: May appear on first visit — dismiss
- **Express checkout buttons**: Shop Pay, Apple Pay, Klarna may appear above standard checkout — use the standard "Checkout" button
- **Shopify Plus checkout**: Multi-step — Information → Shipping → Payment
- **Referral discounts at checkout**: After entering email in checkout, referral discount may auto-apply

## Login Guidance
- Prefer existing saved session if already logged in
- Otherwise use the Away account created by account-creator
- Login at https://www.awaytravel.com/login — this redirects to `accounts.awaytravel.com` (Shopify New Customer Accounts, passwordless)
- Authentication is via email + 6-digit verification code (no password) — check agentmail inbox for the code
- After login, navigate back to cart if items were added before login

## Coupon / Reward Strategy
- Check structured deals from deal-digest for awaytravel.com codes
- Referral codes are Away's primary discount mechanism ($40 off, or varying amounts)
- Referral discounts are only valid on suitcases and bags (not accessories)
- Referral discounts can stack up to 5 codes ($200 max savings) — but only one per checkout typically
- Discount code field appears in the Shopify checkout (usually top-right area on the order summary)
- Enter code and click "Apply"
- Away rarely runs public percentage-off sales — most deals are through referral links

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the Shopify checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot and report back.
