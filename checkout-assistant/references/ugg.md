# UGG Checkout Reference

## Overview
UGG (ugg.com) is a consumer-facing brand owned by Deckers. This reference documents the checkout flow up to the payment step.

## Product Selection
- Products are available across multiple categories: Women, Men, Kids, Home & Gifts, Sale
- Each product page shows:
  - Product image(s)
  - Product name and price
  - Color selection (if available)
  - Size selection (required before adding to cart)
  - "Add to Cart" button
  - "Pay now with Afterpay" option (BNPL)

## Add to Cart Flow
1. Navigate to a product page
2. Select desired color (if applicable)
3. Select desired size (required field)
4. Click "Add to Cart" button
5. Item is added to cart and modal/notification may appear

## Cart Access
- Cart icon in top right header
- Direct URL access: https://www.ugg.com/cart
- Shows cart items, quantities, and totals

## Checkout Process
1. From cart or product page, proceed to checkout
2. System may require authentication (login/signup)
3. Checkout flow includes:
   - Shipping address entry
   - Billing address entry
   - Shipping method selection
   - Payment information entry

## Shipping Address Fields
Expected fields (based on standard checkout flows):
- First Name
- Last Name
- Street Address
- City
- State/Province
- ZIP/Postal Code
- Phone Number
- Email Address (for order confirmation)

## Shipping Methods
UGG advertises "Free Shipping. Free Returns." so standard ground shipping is likely default and free.

## Payment Step
- The payment step includes credit card fields
- Fields visible for entering:
  - Card holder name
  - Card number
  - Expiration date
  - CVV/Security code
  - Billing address (if not same as shipping)

## Alternate Payment Methods
- "Pay now with Afterpay" button visible on product pages
- Afterpay payment integration available
- Other BNPL options may be available at checkout

## Known Blockers
- **CAPTCHA Protection**: Cloudflare CAPTCHA ("Verification Required") appears after certain checkout interactions
  - Triggers on: cart operations, payment section access, and other bot-like activities
  - Cannot be solved programmatically
  - Appears to be: Cloudflare challenge with ID format "40ded894-a75f-806b-a6c3-60fcbe764663"

## Testing Notes
During e2e testing:
- Product added to cart successfully (Goldenstar Hi Artistitch Sandal, size 5, $140)
- Cart access triggered CAPTCHA
- Further navigation blocked until CAPTCHA is solved

## Session Management
- Cookie-based sessions
- Appears to use standard HTTP/HTTPS
- May require session persistence across cart/checkout operations

## Mobile Responsive
- Checkout should be responsive on mobile
- May have mobile-specific checkout flow

## Test Product Used
- Product: Women's Goldenstar Hi Artistitch Sandal
- Color: Chestnut Multi
- Size: 5 (Women's)
- Price: $140.00
- URL: https://www.ugg.com/women-sandals/goldenstar-hi-artistitch/1175133.html?dwvar_1175133_color=CHMU

## Useful Links
- Homepage: https://www.ugg.com/
- Women's Shop: https://www.ugg.com/women/
- Men's Shop: https://www.ugg.com/men/
- Kids Shop: https://www.ugg.com/kids/
- Sale: https://www.ugg.com/master-sale/
- Cart: https://www.ugg.com/cart

## Technical Observations
- Uses Demandware/Salesforce commerce platform (based on URL patterns and form structures)
- Form submission via standard POST requests (not API)
- CAPTCHA verification appears to be Cloudflare-based
- Session tracking via browser cookies
