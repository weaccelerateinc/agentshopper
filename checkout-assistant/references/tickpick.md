# TickPick Checkout Flow

## Purpose
Use this note when logged into an existing TickPick account, searching for an event ticket, selecting a specific ticket listing, and stopping at the payment step where credit card fields are visible.

## Platform
- Custom ticket marketplace platform (TickPick)
- No shipping address required (digital ticket delivery)
- Billing/contact fields required on checkout

## URLs
- Homepage: https://www.tickpick.com
- Event search: https://www.tickpick.com/concerts/<artist-name>-tickets/ (example: /concerts/daniel-caesar-tickets/)
- Ticket selection: Individual event page with seating chart and price listings
- Checkout URL: `https://www.tickpick.com/checkout/?listingId=<id>&quantity=<qty>&listingType=TP&price=<price>&e=<eventId>&s=<sectionId>&r=<rowId>`

## Browser Mode
Use a headed browser.

## Event/Ticket Search Flow
1. Navigate to https://www.tickpick.com
2. Click "Buy" button in top nav OR search by event/artist in search box
3. Select desired event from results (search for cheapest available soonest event in any sport per task requirements)
4. Event detail page shows:
   - Event name, date, time, venue
   - Seating chart on right side
   - List of available sections with pricing on left
   - Each section shows: Section #, Row #, Quantity available, Price per ticket, Deal badge (if applicable)

## Ticket Selection
- Click on a section in the list to select it
- A modal appears asking "How many tickets?" with options: 1, 2, 3, 4, 5, Any
- Select quantity (typically 1 for agent use case)
- Modal closes and section is now selected (shown highlighted)
- Bottom of section list shows a blue "Checkout" or "Continue to checkout" button
- Click the button to proceed to checkout

## Checkout Steps

### Step 1: Contact Info
- Quantity selector (dropdown to change quantity if needed)
- "Buyer Phone Number" field (required):
  - Country code selector (defaults to +1 for US)
  - Phone number field (10 digits for US)
  - Checkbox: "Receive information about your order via text messages"
- Submit button: "Continue to checkout" (blue button at bottom of left panel)

### Step 2: Payment
- Right panel shows order summary:
  - Event name, date, time, venue, section, row
  - Total (USD): price breakdown (Price + Quantity × Service Fees)
  - Savings badge (if applicable)
- Left panel shows payment method options:
  - "New Credit Card" button (for manual card entry)
  - "PayPal" button
  - "Klarna" button (BNPL - "From $13/month or 0% interest")
  - "Google Pay" button
- Credit card form fields (when "New Credit Card" is selected):
  - Card number (required)
  - Expiry date (MM/YY format, required)
  - CVC/CVV (3 digits, required)
  - Cardholder name (required)
  - Billing address fields (required)

## Common UI Elements
- **Mobile transfer delivery**: Tickets delivered electronically via app/email (no physical delivery)
- **View restrictions note**: Seating view descriptions shown (e.g., "Obstructed View", "Limited Side or Rear View")
- **No shipping address**: Only billing address required; tickets are digital
- **Guarantees banner**: "BuyerTrust Guarantee" and "BestPrice Guarantee" displayed on checkout

## Cart Timer
- Carts have a ~10-minute hold timer
- If timer expires, select a different ticket and restart checkout
- No retry mechanism — must select new ticket

## Discount/Promo Strategy
- TickPick advertises "No Hidden Fees" prominently
- Service fees are $0 (noted on checkout summary as "Service Fees $0")
- No visible coupon/promo code field on standard checkout
- Klarna offers BNPL option ("From $13/month or 0% interest with Klarna")

## Reusable Checkout Profile
- Use provided test data for billing/contact info
- First Name: Gary, Last Name: Chao
- Address: 4120 Ivar Ave, Rosemead, CA 91770
- Phone: 6263211250
- Email: gharychao@gmail.com (for confirmation, if needed)
- Do NOT use personal/sensitive card data — stop at payment step

## Stop Condition
Stop when the checkout reaches the **Payment** step and credit card form is visible (fields for card number, expiry, CVC, cardholder name, and billing address). Capture a screenshot showing the payment method options and form fields. DO NOT enter card information or complete the purchase.

## Browser State / Session Persistence
- Assume user is already logged in from account-creator flow
- Session should persist across page navigation
- If session expires, log back in using account credentials from account-creator
