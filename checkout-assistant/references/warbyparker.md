# Warby Parker Checkout Flow

## Purpose
Use this note when logging into an existing Warby Parker account, building a cart with one or more items, applying the best available discount, and stopping at payment.

## Platform
- Shopify Plus with custom checkout (includes prescription verification step)

## URLs
- Eyeglasses: `https://www.warbyparker.com/eyeglasses/<frame-name>/<color>`
- Sunglasses: `https://www.warbyparker.com/sunglasses/<frame-name>/<color>`
- Best sellers: `https://www.warbyparker.com/collections/best-selling-glasses-and-sunglasses`
- Cart: `https://www.warbyparker.com/cart`
- Login: `https://www.warbyparker.com/login` (redirects to auth.warbyparker.com — Auth0 hosted)

## Browser Mode
Use a headed browser. Shopify Plus bot detection is less aggressive in visible sessions.

## Product Variant Behavior
- Color: selected via color swatch thumbnails on the product page
- Frame width: Warby Parker offers "Narrow", "Medium", "Wide", and "Extra Wide" widths — select from a width selector if present
- Lens type: Standard single-vision lenses are the default; progressive and readers are upgrade options
- CTA button is **"Select lenses and buy"** (NOT "Add to Cart") — this leads to a lens type selection step before adding to cart
- **Prescription**: Warby Parker requires a prescription for eyeglasses orders — this comes up during checkout, not on the product page
- For non-prescription items (sunglasses, accessories), no prescription step applies

## Common UI Issues
- **Virtual Try-On prompt**: Warby Parker may prompt to try frames virtually via camera — dismiss it
- **Prescription step in checkout**: After adding to cart, checkout will ask for prescription details (upload, enter manually, or have WP contact your doctor). For testing, this step will block order completion — stop at this point or the payment step, whichever comes first
- **No aggressive pop-ups**: Warby Parker is clean compared to other DTC sites
- **Cookie banner**: May appear on first visit — dismiss

## Login Guidance
- Prefer existing saved session if already logged in
- Otherwise use the Warby Parker account created by account-creator
- Login at https://www.warbyparker.com/login — this redirects to `auth.warbyparker.com` (Auth0, passwordless)
- Authentication is via email + verification code (no password) — check agentmail inbox for the code
- If login issues arise, check for hCaptcha challenge on the Auth0 page

## Coupon / Reward Strategy
- Check structured deals from deal-digest for warbyparker.com codes
- Warby Parker rarely offers public promo codes — most discounts are through referral links or seasonal sales
- Discount code field appears during Shopify checkout
- Try one code at a time; keep the best discount
- Insurance benefits may apply but require manual input — skip for automated checkout

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the checkout reaches the **Payment** step with card entry fields visible, OR when the **Prescription** step is reached (whichever comes first). Capture a screenshot and report back. Note which step caused the stop.
