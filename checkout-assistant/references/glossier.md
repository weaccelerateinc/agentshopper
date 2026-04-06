# Glossier Checkout Flow

## Purpose
Use this note when logging into an existing Glossier account, building a cart with one or more products, applying the best available discount, and stopping at payment.

## Platform
- Shopify Plus — custom checkout with Shopify Checkout Extensibility

## URLs
- Product pages: `https://www.glossier.com/products/<product-name>`
- Collections: `https://www.glossier.com/collections/<category>`
- Cart: `https://www.glossier.com/cart`
- Login: `https://www.glossier.com/account/login`

## Browser Mode
Use a headed browser.

## Product Variant Behavior
- Shade/Color: selected via swatch buttons on the product page (common for makeup products)
- Size: some products offer size variants (e.g., mini vs full size) — select from a dropdown or button group
- "Add to Bag" button should be active once required variants are selected
- For multi-item carts, repeat product page → variant selection → add-to-bag for each item
- Some products have no variants (e.g., skincare basics) — "Add to Bag" is immediately clickable

## Common UI Issues
- **Email capture pop-up**: Glossier shows an aggressive email pop-up on every page visit — close it immediately via the X button before interacting with any page elements. It may reappear on navigation
- **Sticky mobile footer**: On smaller viewports a sticky email signup footer may overlap buttons — scroll past or close it
- **Express checkout buttons**: Shop Pay, PayPal, Google Pay buttons appear above standard checkout — use the standard "Checkout" button
- **Shopify checkout is multi-step**: Information → Shipping → Payment
- **Guest checkout**: Available via Shopify but logging in is preferred for saved addresses

## Login Guidance
- Prefer existing saved session if already logged in
- Otherwise use the Glossier account created by account-creator
- Login at https://www.glossier.com/account/login
- After login, navigate back to cart if items were added before login

## Coupon / Reward Strategy
- Check structured deals from deal-digest for glossier.com codes
- Glossier runs seasonal sales and occasionally offers membership perks (free gifts with purchase)
- Discount code field appears on the Shopify checkout Information or Payment step
- Enter code in "Discount code" field and click "Apply"
- Try one code at a time; keep the best discount
- Free shipping thresholds may apply — check if order qualifies

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the Shopify checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot and report back.
