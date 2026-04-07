# Mercari Checkout Flow

## Purpose
Use this note when logged into an existing Mercari account, finding and purchasing a product, and stopping at the payment step.

## Platform
- Peer-to-peer marketplace
- Custom checkout (not Shopify)

## URLs
- Homepage: `https://www.mercari.com`
- Product pages: `https://www.mercari.com/us/item/<item-id>/`
- Transaction/checkout: `https://www.mercari.com/transaction/buy/<item-id>/`
- Account dashboard: `https://www.mercari.com/mypage/`

## Browser Mode
Use a headed browser.

## Product Selection Guidance
- Mercari is a peer-to-peer marketplace with individual seller listings
- Products vary in price and condition (New, Like New, Good, Fair)
- Search or browse by category to find items
- Recommended: Look for low-cost items ($1-5) to minimize test transaction impact
- Skip auction-style listings (offers) — use "Buy Now" items only
- Item listings show price, condition, seller rating, and shipping info

## Buyer Flow
1. **Login**: Ensure logged into Mercari account (account-creator creates this)
2. **Browse**: Navigate to https://www.mercari.com or search for a product
3. **Select item**: Click on a "Buy Now" product listing
4. **View product details**: Page shows price, condition, seller, shipping options
5. **Click "Buy now"**: Button takes you to the checkout/transaction page
6. **Checkout page** (`/transaction/buy/<item-id>/`):
   - Delivery address section: Shows pre-filled shipping address from account profile
   - "Edit" link to modify address if needed
   - Order summary: Item(s), price, delivery cost, buyer protection fee, tax, total
   - Payment section: Shows available payment methods (PayPal, Venmo, Card)
   - "Add new card" option to enter credit card
   - "Confirm and pay" button to finalize purchase

## Shipping & Address
- Delivery address is auto-populated from the buyer's account profile
- Address can be edited via "Edit" link on checkout page
- Mercari calculates shipping based on item weight and destination
- Shipping may show a discount (e.g., "Limited time shipping discount")
- Some items include "Free shipping" if seller absorbed the cost

## Payment Methods
- **PayPal**: "Pay instantly with PayPal" — redirects to PayPal login/authorization
- **Venmo**: "Pay with your Venmo account" — requires Venmo authentication
- **Card**: "Add new card" option — renders inline card form on payment step
- Multiple payment methods can be added

## Card Form (if using card payment)
- Card number field
- Cardholder name field (may be pre-filled)
- Expiration date field
- CVV/security code field
- "Confirm and pay" button submits the transaction

## Mercari-Specific Behavior
- **Buyer Protection Fee**: Mercari charges a small fee (~$0.05 per $1 item) as buyer protection
- **No email confirmation required**: Transaction proceeds directly with card submission
- **Shipping discount**: Mercari occasionally offers limited-time shipping discounts
- **Seller communication**: Can message seller before/after purchase (not part of checkout)
- **Return window**: Mercari offers buyer protection but not explicit return policy at checkout

## Common UI Issues
- **Cookie consent banner**: May appear — dismiss with "Got it"
- **Out of stock**: Listings can be claimed by other buyers — if item becomes unavailable, select a different product
- **Shipping variants**: Mercari offers multiple shipping methods from seller perspective; buyer typically has one option pre-selected
- **Buyer protection prompt**: Page mentions fraud protection — this is informational
- **Multiple sellers same item**: If searching, multiple listings may exist for similar items — prices and conditions vary by seller

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields if custom address needed. Do not commit that file. If missing, create from `references/checkout-profile.template.json`.

**Note**: Mercari auto-fills address from account profile, so custom profile may not be necessary.

## Stop Condition
Stop when the checkout page reaches the **Payment** step with payment method options visible and card form accessible. Capture a screenshot and report back. **Do NOT click "Confirm and pay"** — this would complete the actual transaction.
