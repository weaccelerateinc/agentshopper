# Newegg.com Checkout Flow

## Platform
- Custom e-commerce platform (not Shopify)

## URLs
- Homepage: https://www.newegg.com/
- Checkout (secured): https://secure.newegg.com/shop/checkout

## Product Selection & Cart
- Products are accessible from category navigation menus
- Computer Peripherals > Mouse Pad & Keyboard Accessories contains affordable items
- "Add to Cart" button is orange with + icon
- After adding to cart, a confirmation popup appears with "PROCEED TO CHECKOUT" button
- Total price includes item cost and free shipping (varies by product)

## Checkout Flow Overview
Checkout has 2 main steps:
1. **SHIPPING** — Collect address and phone information
2. **PAYMENT** — Select payment method

## Step 1: Shipping Address Entry
### Form Fields (must be filled):
- **Full name (first and last name)** — single text field
- **Country/Region** — dropdown, defaults to "United States"
- **Address** — text field with autocomplete
  - Starts with "Start typing your address to search"
  - Autocomplete suggestions appear (e.g., "4120 Ivar Ave Rosemead CA 91770-1321")
  - Can accept typed address or select from suggestions
- **Apartment/Suite/Unit** (optional) — secondary address field
- **City** — text field, auto-filled when address is selected
- **State** — dropdown, auto-filled when address is selected (defaults to "Alaska")
- **ZIP Code** — text field, auto-filled when address is selected
- **Phone** — country code dropdown (defaults to "US +1") + number field
  - Phone is formatted automatically (e.g., "6263211250" becomes "(626) 321-1250")
- **Delivery instructions (access code, note)** — optional expandable field
- **Save this address** checkbox (checked by default)
- **Set as default** checkbox (checked by default)

### Shipping Form Buttons
- **"Use this shipping address"** button (orange, top right or bottom)
- **"Change"** link (appears after address is confirmed, top right)

### Form Behavior
- Address autocomplete works with partial input
- All location fields auto-populate when address is selected via autocomplete
- Phone number auto-formats as user types
- Form validates before allowing progression to payment

## Step 2: Payment Method Selection
### Available Payment Methods
- **Add a credit or debit card** option (primary method)
- **Newegg Store Credit Card** — Pay with Newegg Store Credit Card (with "Learn how" and "See details" links)
- **PayPal** — Pay with PayPal
- **Venmo** — Pay with Venmo
- **BitPay** — Pay with cryptocurrency
- **Paze** — Fast & secure checkout offered by banks & credit unions

### Order Summary (Right Column)
- Item(s): price (e.g., $16.99)
- Shipping: FREE or cost
- Tax: calculated amount (e.g., $1.66)
- **Total**: final amount (e.g., $18.65)

### Payment Form Button
- **"Use this payment method"** button (disabled until a payment method is selected)
- Text: "Select a payment method to continue. You'll still have a chance to review your order before it's final."

## Common Issues
- **reCAPTCHA**: May trigger during checkout — user must solve manually if it appears
- **Bot detection**: Site has anti-bot measures — interact slowly and naturally
- **Region dialog**: May appear on initial page load — dismiss with "Stay at United States"
- **Cookie banner**: May appear — dismiss with "Reject Non-Essential" or "Accept All"
- **Blank page rendering**: If page renders blank, try: `document.body.style.zoom='0.5'` in console
- **Form validation**: All required fields must be filled before progression
- **Address verification**: Autocomplete helps ensure valid US addresses
- **Payment method lag**: May take 1-2 seconds for payment methods to fully load after shipping selection

## Payment Step Characteristics
- Payment step shows 2 sections: "Your credit cards" and "Other payment methods"
- Multiple payment options available (credit cards, digital wallets, BNPL options)
- **DO NOT enter card details** unless explicitly required for testing
- Form allows users to continue even without selecting a payment method (on some flows)
- Final review step occurs after payment method selection

## Order Review & Confirmation
- After selecting payment method, user reaches final order review screen
- Final screen shows shipping address, order items, and total cost
- "Place Order" or similar button completes the purchase
- Confirmation page shows order number and confirmation email message
