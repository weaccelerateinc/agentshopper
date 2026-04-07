# Quince Checkout Flow

## Purpose
Use this note when logged into an existing Quince account, adding a product to cart, filling shipping information, and stopping at the payment step.

## Platform
- Quince Direct-to-Consumer Fashion (Shopify-based)

## URLs
- Homepage: `https://www.quince.com/`
- Product pages: `https://www.quince.com/<category>/<product-name>`
- Collections: `https://www.quince.com/<collection-name>` (e.g., `everyday-steals`, `men`, `women`)
- Cart: (auto-managed shopping bag sidebar)
- Login: `https://www.quince.com/log-in`
- Account: `https://www.quince.com/account/my-orders-returns`

## Browser Mode
Use a headed browser.

## Product Selection & Cart
- Browse collections or use search to find products
- Click product to view details page showing:
  - Product images (left side)
  - Product name, price, discount percentage (if applicable)
  - Color swatches (circular buttons)
  - Size options (buttons: XS, S, M, L, XL, XXL, etc.)
  - "In stock" indicator
  - "Add to Bag" button (orange)
- Select color and size before adding to cart
- "Add to Bag" button becomes active once options are selected
- Clicking "Add to Bag" opens a shopping bag sidebar on the right
- Shopping bag shows:
  - Item summary with image, name, size, color, price
  - Quantity controls
  - Subtotal and shipping info
  - "Checkout" button (black/dark)

## Common UI Issues
- **Newsletter pop-ups**: May appear on initial visit — dismiss if present
- **Cookie banner**: May appear — dismiss before interacting
- **Page rendering on checkout**: Checkout pages may initially render blank — applying `document.body.style.zoom='0.5'` via JavaScript can help render the page correctly
- **Free shipping**: Quince offers free standard shipping on all orders (365-day returns standard)
- **Discount banners**: Informational messages about free shipping and returns at top of page

## Login Guidance
- Use existing logged-in session if available
- Otherwise login at `https://www.quince.com/log-in` with account credentials
- After login, you'll be redirected to the account dashboard
- Navigate back to shopping/cart as needed

## Checkout Form Fields
The checkout page is a single form with multiple sections:

### Express Checkout
- Google Pay button
- PayPal button
- Amazon Pay button
- Skip these and use standard card checkout

### Account Section
- Shows logged-in email address
- "Switch account" link available

### Delivery Section
- Country/region dropdown (default: United States)
- First Name (required)
- Last Name (required)
- Address (required)
- Apartment, suite, etc. (optional)
- City (required)
- State (required, dropdown)
- ZIP code (required)
- Phone (optional, but recommended)
- Newsletter opt-in checkbox

### Gift Message Section
- "Add a gift message" checkbox

### Shipping Method Section
- "Enter your shipping address to view available shipping methods" text
- Once address is filled, standard shipping options appear

### Payment Section
- Radio button for payment method selection
- **Card** option shows:
  - Card number field (accepts all major cards)
  - Expiration date field
  - Security code field
  - Card brand icons (Visa, Mastercard, Amex, Discover)
- **Amazon Pay** option
- **PayPal** option
- "Use shipping address as billing address" checkbox

## Order Summary (Right Panel)
- Product list with images and prices
- Subtotal
- Shipping (Free)
- Total amount

## Order Reservation
- Timer displayed: "Hurry! Your order is reserved for XX:XX minutes"
- Default 10-minute reservation window

## Coupon / Discount Strategy
- Discount code field appears in cart sidebar: "Discount code or gift card"
- "Apply" button next to the field
- Enter codes and click Apply
- Code validation happens in real-time
- Quince frequently offers percentage-off promotions
- Free shipping is already included, so focus on product discounts

## Stop Condition
Stop when the Quince checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot showing the payment section with card, expiration date, and security code fields. Do NOT fill in card details. Report back with the screenshot.

## Known Constraints
- Email verification required during signup (one-time code)
- Shipping address is required before payment methods are shown
- Phone number is optional but recommended for order delivery
- Quince ships within continental US primarily (verify region support)
- Free shipping applies to all orders (365-day return window)
