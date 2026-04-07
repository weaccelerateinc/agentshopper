# Torrid — Checkout Reference

## Platform & Payment Architecture
- **Storefront**: Demandware (Salesforce Commerce Cloud)
- **Checkout Type**: Multi-step guest/registered user checkout
- **Payment Provider**: Likely Demandware native payments (Stripe or similar) — card form rendered inline
- **Card Entry**: Inline form on Payment step (NOT cross-origin iframe)

## Checkout Flow

### Step 1: Shopping Cart / Bag Review
- **URL**: `/cart` or `/shopping-bag`
- **Elements**:
  - Product listing with image, name, size, price, quantity
  - Estimated order total with savings breakdown
  - "Checkout" button (primary CTA)
  - "Continue Shopping" option

### Step 2: Shipping Address
- **Heading**: "Shipping Address" or similar
- **Fields**:
  - First Name
  - Last Name
  - Address Line 1
  - Address Line 2 (optional)
  - City
  - State/Province (dropdown)
  - Postal Code
  - Country (usually pre-selected as "United States")
  - Phone Number
  - Email Address (optional or pre-filled if logged in)
- **Shipping Method Selection** (after address entry):
  - Standard Shipping
  - Express Shipping
  - Overnight (if available)
  - Select one and continue
- **CTA**: "Continue to Shipping Method" or "Continue to Payment"

### Step 3: Shipping Method Review & Confirmation
- Displays selected shipping method and cost
- May allow changing method
- **CTA**: "Continue to Payment" or similar

### Step 4: Payment (TARGET SCREENSHOT)
- **Heading**: "Payment Information" or "Billing & Payment"
- **Billing Address Section**:
  - Checkbox: "Same as Shipping Address" (usually checked by default)
  - If unchecked, separate billing address form appears
- **Card Details Section**:
  - Card Number input (Demandware inline field or Stripe tokenized input)
  - Cardholder Name (if not auto-filled)
  - Expiration Date (MM / YY or MM / YYYY format)
  - CVV/Security Code (3-4 digits)
  - Checkbox: "Save this card for future purchases"
- **Order Summary Sidebar**:
  - Item list with quantities and prices
  - Subtotal
  - Shipping cost
  - Tax (if applicable)
  - Order Total
- **CTA**: "Review Order", "Place Order", or "Complete Purchase"

## Field Identification & Selectors

### Card Form Fields (Demandware inline)
Standard Demandware payment form selectors (may vary):
- Card Number: `input[name*="number"]` or `input[placeholder*="Card"]`
- Cardholder Name: `input[name*="name"]` or `input[placeholder*="Cardholder"]`
- Expiry: `input[name*="expiry"]` or `input[placeholder*="Expiration"]` (format: MM/YY)
- CVV: `input[name*="cvv"]` or `input[name*="verification"]` or `input[placeholder*="Security"]`

**Dynamic Lookup**: If selectors fail, use `find` to locate:
- "Card number" or "Card Number" field
- "Expiration" or "Expiry" field
- "CVV" or "Security Code" field

### Address Fields
- First Name: `input[name*="firstName"]` or `input[placeholder*="First"]`
- Last Name: `input[name*="lastName"]` or `input[placeholder*="Last"]`
- Address Line 1: `input[name*="address1"]` or `input[placeholder*="Street"]`
- City: `input[name*="city"]` or `input[placeholder*="City"]`
- State/Province: `select[name*="state"]` or similar dropdown
- Postal Code: `input[name*="postal"]` or `input[placeholder*="ZIP"]`
- Phone: `input[name*="phone"]` or `input[type="tel"]`
- Email: `input[name*="email"]` or `input[type="email"]`

## Fill Strategy for Payment Step

### Optimal Sequence (Payment Step)
1. Verify you're on the Payment step (URL contains `/checkout` or `/payment`)
2. If "Same as Shipping" checkbox is checked (default), skip billing address entry
3. If unchecked, fill billing address fields
4. Fill card details:
   - Click card number field
   - Type card number (Demandware may auto-format)
   - Tab to cardholder name (if field exists)
   - Tab to expiration, type MM/YY (Demandware auto-inserts slash if needed)
   - Tab to CVV, type 3-4 digits
5. Optionally check "Save card for future use"
6. Click "Review Order" or equivalent CTA
7. **Screenshot the order review/confirmation page** (NOT the payment form itself to avoid capturing sensitive card data)

## Demandware-Specific Gotchas

### Form Rendering
- Demandware may render form fields as custom HTML/CSS elements (not native `<input>` tags)
- Use `find` with natural language (e.g., "card number field") to locate dynamically
- Dropdowns may be custom select components — test with `form_input` or click + keyboard interaction

### Address Auto-Formatting
- City and State fields may have auto-complete or validation
- Postal code may auto-format or validate against state (U.S. postal rules)
- Wait for validation to complete before proceeding

### Card Field Behavior
- Card number field may show placeholder examples (e.g., "1111 1111 1111 1111")
- Expiration field may auto-format MM/YY with slash insertion
- CVV field typically hides characters after input (dots or asterisks)

### Session / Cart Persistence
- Cart data persists via session/cookie (Demandware DWSID)
- If session expires during checkout, user is redirected to cart
- Use explicit waits and verify page state before filling sensitive fields

### Promo Codes / Gift Cards
- A promo code field may appear before payment step or at review stage
- Optional; can skip if no code to apply

## Checkout Fast Path (No Complications)

1. Have cart with 1+ items ready
2. Click Checkout → Shipping Address form appears
3. Fill address with test data (see account-creator reference for format)
4. Select Standard Shipping, continue
5. Fill card details (see above)
6. Click "Review Order"
7. **Screenshot the order review page** (payment step has been reached and form filled without errors)

## Test Data Template
```
Shipping Address:
- Name: Gary Chao
- Address: 4120 Ivar Ave, Rosemead, CA 91770
- Phone: 6263211250
- Email: gharychao@gmail.com (or test account email)

Billing Address: Same as Shipping (checkbox checked)

Card (DO NOT FILL IN ACTUAL TEST):
- Card Number: [Test card from Stripe/processor]
- Expiry: 12/26 (future date)
- CVV: 123
- Cardholder Name: Gary Chao
```

## Troubleshooting
- **Session Timeout**: If redirected to login during checkout, re-authenticate and restart checkout
- **Cart Cleared**: If items disappear, refresh and re-add from product page
- **Address Validation Error**: Verify postal code matches state; some states have format requirements
- **Card Declined**: Use test card from Stripe documentation for your test environment
- **3D Secure / SCA Challenge**: Some cards trigger additional verification — pause and allow manual completion if needed
