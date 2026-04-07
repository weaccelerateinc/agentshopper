# Teleflora Checkout Reference

## Overview
Teleflora is an online florist that allows customers to order flower arrangements and bouquets for delivery. The checkout process requires product selection, recipient details, and payment information.

## Product Selection & Cart

### Product Page
- Products are accessed by category (e.g., Birthday Flowers)
- Each product shows multiple size/quality options with different prices
- Example: "Make a Wish" bouquet
  - Standard: $39.99
  - Deluxe: $49.99
  - Premium: $59.99

### Required Fields on Product Page
1. **Recipient Zip Code** (required)
   - Input type: text
   - Used to determine delivery availability and options
   - Example: 91770

2. **Delivery Date** (required)
   - Input type: date field with calendar picker
   - Format: Calendar picker (not standard text format like MM/DD/YYYY)
   - Must select via calendar widget, not text entry
   - Requires future date selection

3. **Optional Add-Ons**
   - Mylar Balloons: $5.99 to $15.99 (select quantity)
   - Birthday Card: $8.99 (handwritten option)
   - Chocolates: $9.99 to $29.99 (small, medium, large)

### Cart Actions
- Click "ADD TO CART" button to add item to cart
- Item is added with all selected options
- Proceeds to next step in checkout flow

## Checkout Flow

### Step 1: Product Selection
- Select bouquet/arrangement
- Choose size/quality
- Enter recipient zip code
- Select delivery date using calendar
- Add optional extras (balloons, card, chocolates)
- Click "ADD TO CART"

### Step 2: Recipient & Delivery Information
- Recipient zip code
- Delivery date
- Option to "Find Zip Code" or "Use Address Book"

### Step 3: Payment & Billing Information
- (Not fully tested - signup/account creation required)
- Expected fields: billing address, payment method
- May allow billing address same as shipping address

## Important Technical Notes

### Form Validation
- Date field uses calendar picker widget, not standard text input
- Entering date as text (MM/DD/YYYY) triggers validation error: "Error: Delivery date is required"
- Must use calendar date picker interface for proper date selection
- Zip code is required before checkout can proceed

### Session Handling
- Uses request IDs in URL parameters (_requestid=)
- Session-based cart (requires login or guest checkout)
- ZIP code validation is server-side

### Error Handling
- Shows validation errors at top of page in red alert box
- Format: "Error: [field] is required"
- Requires field correction before re-submission

## Cart Management
- Shopping cart accessible via header link
- Can view cart details
- Supports quantity adjustments
- Requires recipient information for delivery

## Checkout Sequence
1. Browse flowers by category
2. Select product and options
3. Enter recipient zip code
4. Select delivery date (via calendar picker)
5. Add to cart
6. Proceed to checkout
7. Enter billing/payment information
8. Confirm order

## Known Issues/Blockers
- Date field requires calendar picker interface - text input alone fails validation
- Account creation form has validation issues (missing Birthday Year field for successful submission)
- Form submission may require additional hidden/dynamic fields
- ZIP code-based delivery availability validation
- May require guest checkout for test transactions

## Test Account Information
- Email: garysmod@agentmail.to
- Password: AgentShop2026!
- Name: Gary Chao
- Phone: 6263211250
- Test Address: 4120 Ivar Ave, Rosemead, CA 91770
- Test Recipient Zip: 91770

## Pricing Structure
- Flowers: $39.99 - $59.99 (depending on size)
- Taxes, delivery, and upgrades not included in listed prices
- Optional add-ons: $5.99 - $29.99
- Financing available: "Pay as little as $15.00 today" (Learn More link)
