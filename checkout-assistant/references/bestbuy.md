# Best Buy Checkout Flow

## Purpose
Use this note when logged into an existing Best Buy account, building a cart with one or more products, and stopping at the payment step without entering card details.

## Platform
- Best Buy proprietary e-commerce platform with Akamai bot detection

## URLs
- Homepage: https://www.bestbuy.com
- Search: https://www.bestbuy.com/site/searchpage.jsp (e.g., `?st=HDMI%20cable`)
- Product pages: `https://www.bestbuy.com/product/<product-name>/<sku>`
- Cart: https://www.bestbuy.com/cart
- Checkout: https://www.bestbuy.com/checkout (multi-step flow)
- Account: https://www.bestbuy.com/customer/myaccount

## Browser Mode
Use a headed browser.

## Product Search & Selection
- Use the search bar to find inexpensive items (e.g., "HDMI cable")
- Search results show multiple products with pricing, ratings, and stock status
- Click on a product to view full details, including price ($19.99 for HDMI cables is typical)
- Verify "In Stock" status before adding to cart
- Availability options show: Pickup (Ready Today) or Shipping (Get it by Thu, Apr X)

## Add to Cart
- Scroll down on product page to find the "Add to cart" button (blue button)
- Click the button
- Product is added to cart; page may redirect to cart automatically
- Confirm item appears in cart at https://www.bestbuy.com/cart

## Cart Page
- Displays all items with quantity, unit price, and subtotal
- Shows cart total ($0.00 if empty)
- "Continue Shopping" button to return to browsing
- "Checkout" button (blue) to proceed to checkout flow

## Checkout Flow (Multi-Step)
Best Buy uses a linear checkout with these steps:
1. **Cart Review** — confirm items and quantities
2. **Shipping Address & Contact** — enter or select address, phone, email
3. **Shipping Method** — select ground, 2-day, next-day, or pickup
4. **Payment** — enter credit card details (STOP HERE)

## Shipping & Contact Information
- Address: Use profile data from references/checkout-profile.json if available
- Email: Provide a valid email (or use secondary email from account credentials)
- Phone: Use phone number associated with account or provided during signup
- Shipping method defaults to Ground; express options available for additional fee
- All fields are typically required

## Common UI Elements
- **Session timeout**: Best Buy may log out user after inactivity; refresh page and re-login if needed
- **Address validation**: System validates address format; may suggest corrections
- **Shipping cost**: Calculated based on zip code and method selected
- **Promo codes**: Discount code field may appear on checkout page
- **Bot detection**: May see CAPTCHA or "verify you're human" page; complete if needed
- **Free shipping threshold**: Some orders qualify for free shipping based on subtotal

## Coupon / Discount Strategy
- Check for Best Buy coupons or discount codes from deal-digest
- Best Buy frequently offers percentage-off codes or free shipping promotions
- Enter code in discount/coupon field if available during checkout
- Apply and verify savings before proceeding to payment

## Login Guidance
- Prefer existing saved session if already logged in (check for "Hi, [Name]" in header)
- Otherwise, log in at https://www.bestbuy.com/account/login using account-creator credentials
- After login, navigate to product pages or search results to build cart

## Stop Condition
**Stop when the Best Buy checkout reaches the Payment step** (final step) and the credit card entry form is visible. At this point:
- All shipping, contact, and shipping method information is confirmed
- Order summary shows subtotal, tax estimate, and total
- Credit card form is displayed but NOT filled in
- Capture a screenshot showing the payment form and report back

## Known Issues
- **Akamai bot detection**: May block automated checkout attempts — use natural interaction delays
- **Cart session expiration**: Items may be removed from cart if session expires; re-add if needed
- **Address validation**: International or non-standard addresses may be rejected; use standard US format
- **Shipping delays**: During peak times, shipping estimates may be longer than usual
