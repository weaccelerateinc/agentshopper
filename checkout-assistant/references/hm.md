# H&M Checkout Flow

## Purpose
Use this note when logging into an existing H&M account, selecting a product, adding to cart, and stopping at the payment step.

## Platform
- Custom e-commerce platform (not Shopify)

## URLs
- Main store: https://www.hm.com/en_us/index.html
- Collections: https://www.hm.com/en_us/shop/<category> (e.g., women, men, kids)
- Product pages: https://www.hm.com/en_us/products/<product-id>
- Cart: https://www.hm.com/en_us/cart

## Browser Mode
Use a headed browser.

## Navigation & Product Selection
- Start from main page or navigate directly to product page
- Use "WOMEN", "MEN", "KIDS", "HOME", "BEAUTY" navigation tabs
- For quick testing, select cheapest in-stock item (e.g., basic socks, beanie, essential tees)
- Product page shows:
  - Price
  - Size selector (if applicable)
  - Color/variant selector
  - "Add to Bag" or "Add to Cart" button

## Product Variant Behavior
- Color: selected via color swatches or dropdown
- Size: selected via size dropdown or button grid
- Stock status: shown as "In Stock" or "Out of Stock"
- Multiple variants may be on same page; select size/color before adding to cart
- Quick test items (socks, beanies) typically have minimal variants

## Add to Cart
- Click "Add to Bag" or "Add to Cart" button
- Cart updates and/or modal appears confirming item added
- Navigate to cart or continue shopping

## Cart Page
- URL: https://www.hm.com/en_us/cart
- Shows:
  - List of items with price, quantity, size, color
  - Subtotal
  - Shipping method selector (standard, express, etc.)
  - Promo code / discount code field
  - "Checkout" button

## Common UI Issues
- **Cookie banner**: Appears on first visit — dismiss via "ONLY REQUIRED COOKIES" or decline non-essential cookies
- **Shipping location banner**: Shows "We've set your shipping location to United States" with "SELECT ANOTHER OPTION HERE" link — verify location is correct
- **Newsletter pop-up**: May appear on first visit — dismiss if present
- **Promotional banners**: "UP TO 50% OFF SITEWIDE" — informational only
- **Page rendering**: Some pages may render blank when scrolled; use `document.body.style.zoom='0.5'` if blank areas appear
- **Performance**: Pages may load slowly; wait 2-3 seconds before interacting

## Coupon / Discount Strategy
- H&M frequently offers percentage-off codes via email
- Discount code field is visible on cart page
- Enter code in discount field and apply
- Compare savings before and after code application
- "UP TO 50% OFF SITEWIDE" may be built-in seasonal sale (not a code)

## Checkout Flow
1. From cart, click "Checkout" button
2. **Shipping Information** step:
   - Email (may pre-fill if logged in)
   - Full Name
   - Address, City, State, ZIP
   - Phone number
   - Shipping method (Standard, Express, etc.)
3. **Payment** step:
   - Credit card fields (Cardholder name, card number, expiry, CVV)
   - Billing address (may auto-fill from shipping)
   - Place Order button
4. **Stop at Payment**: Do NOT fill card details; capture screenshot and exit

## Reusable Checkout Profile
Store shipping/contact info locally (e.g., `checkout-profile.json`). Do not commit credentials or sensitive data.

## Login Guidance
- If account exists, log in via account icon → "Sign In"
- Alternatively, proceed as guest (guest checkout available)
- For test account, use credentials created by account-creator

## Stop Condition
Stop when the checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot showing:
- Payment form with card fields (name, number, expiry, CVV)
- Billing address section (if separate)
- "Place Order" or "Complete Order" button
- Do NOT enter card details
- Report back with screenshot and cart total

## Potential Blockers
- **Address validation**: H&M may validate address format; use the provided test address: 4120 Ivar Ave, Rosemead, CA 91770
- **Phone format**: Ensure phone follows US format (10 digits or with country code)
- **Size/color out of stock**: May prevent checkout — select different item or color/size variant
- **Geo-restrictions**: Some products/promotions may be US-only
- **Payment methods**: H&M may not accept all card types; standard Visa/Mastercard typically works for testing
