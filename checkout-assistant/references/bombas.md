# Bombas Checkout Flow

## Purpose
Use this note when logging into an existing Bombas account, building a cart with one or more products, applying the best available discount, and stopping at payment.

## Platform
- Standard Shopify (not Plus)

## URLs
- Product pages: `https://www.bombas.com/products/<product-name>`
- Collections: `https://www.bombas.com/collections/<category>` (e.g., `mens-socks`, `womens-socks`)
- Cart: `https://www.bombas.com/cart`
- Login: `https://www.bombas.com/account/login`

## Browser Mode
Use a headed browser.

## Product Variant Behavior
- Color: selected via color swatch buttons on the product page
- Size: selected via size buttons (e.g., "Small", "Medium", "Large" for socks; specific sizes for shoes)
- "Add to Cart" button should be active once color and size are selected
- Multi-packs (4-Pack, 8-Pack, 12-Pack) are **tabs on the same product page** (not separate products) — click the pack size tab to switch. Each tab shows a different per-pair price (e.g., Single $14/pair, 4-Pack $12.50/pair)
- For multi-item carts, repeat product page → variant selection → add-to-cart for each item

## Common UI Issues
- **"Want 20% Off?" pop-up**: Bombas shows a newsletter incentive pop-up on first visit — dismiss it immediately before interacting with the page
- **Cookie banner**: May appear on first visit — dismiss
- **Express checkout buttons**: Amazon Pay and PayPal buttons may appear in cart — use the standard "Checkout" button instead
- **Standard Shopify checkout**: Multi-step — Information → Shipping → Payment
- **Free shipping threshold**: Orders over $75 get free shipping — cart may show a progress bar toward this threshold
- **Guest checkout**: Available on standard Shopify

## Login Guidance
- Prefer existing saved session if already logged in
- Otherwise use the Bombas account created by account-creator
- Login at https://www.bombas.com/account/login
- After login, navigate back to cart if items were added before login

## Coupon / Reward Strategy
- Check structured deals from deal-digest for bombas.com codes
- Bombas frequently offers percentage-off codes via email campaigns (20% off is common for first orders)
- Discount code field appears on the Shopify checkout Information or Payment step
- Enter code in "Discount code" field and click "Apply"
- Try one code at a time; keep the best discount
- First-order discounts may conflict with sale prices — compare totals

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the Shopify checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot and report back.
