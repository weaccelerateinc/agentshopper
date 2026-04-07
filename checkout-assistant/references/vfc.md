# VF Corporation Merchant Testing - Checkout Reference

## Overview
**Merchant:** VF Corporation (https://www.vfc.com)
**Status:** Corporate holding company (no checkout)
**Actual Site Tested:** Timberland.com (https://www.timberland.com) - VF-owned brand
**Checkout Status:** NOT REACHED - Account creation required first
**Test Date:** April 2026

## VF Corporation Corporate Site
The primary VF Corporation website (vfc.com) is a corporate holding company site with NO consumer e-commerce functionality. It serves as:
- Investor relations portal
- Company information hub
- Brand portfolio showcase
- Career/recruitment site
- NO shopping, cart, or checkout capabilities

## Why Testing Switched to Timberland

As instructed, when the corporate site has no consumer shopping:
1. Confirmed vfc.com is corporate-only
2. Attempted testing on portfolio brands:
   - Vans.com (blocked by Arkose bot detection)
   - The North Face (blocked by Arkose bot detection)
   - Timberland.com (accessible but incomplete signup)

## Timberland.com Checkout Findings

### Checkout Accessibility
- **Status:** Not reached during testing
- **Reason:** Account creation incomplete (prerequisite for checkout)
- **Bot Detection:** Arkose middleware present but passed on homepage

### Expected Checkout Flow (Based on Site Structure)
1. Navigate to products/shoes section
2. Select cheapest available item
3. Add to cart (requires account OR guest checkout)
4. Cart/Checkout page access
5. Shipping information entry
6. Shipping method selection
7. Payment entry step

### Timberland Site Structure
- **Homepage URL:** https://www.timberland.com/en-us
- **Product Categories:** Men's, Women's, Kids, Footwear, Equipment
- **Platform:** Salesforce Commerce Cloud
- **Payment Methods:** Standard credit cards (Visa, Mastercard, Amex, Discover expected)

### Known Product Categories
- Boots (signature Timberland product)
- Shoes (various styles)
- Clothing
- Accessories
- Equipment/Outdoor gear

### Estimated Cheapest Products
Based on typical Timberland pricing:
- Entry-level shoes: $60-80
- Basic clothing items: $30-50
- Likely candidates for "cheapest product" test

## Blockers for Checkout Testing

### Critical: Bot Detection (Arkose)
1. Present on Vans and The North Face (explicit verification modal)
2. May be present on Timberland but less visible on homepage
3. Likely blocks checkout flows
4. Cannot be automated without human interaction

### Account Creation Blocker
- Must complete account signup to proceed
- Form validation issues encountered
- Community Terms checkbox required
- Date of Birth field validation issues

### Additional Expected Blockers
- SMS/OTP verification (may require real phone)
- Email verification link (working with Agentmail)
- Address validation (some retailers validate US addresses)
- Payment form security (CVV verification, fraud checks)

## Recommended Testing Approach

### For Account Creation (Prerequisite)
1. Focus on date of birth field format validation
2. Ensure all checkbox states before submission
3. Allow form to fully process after submission
4. Check email for verification link

### For Checkout Flow
1. **Minimum path:** Browse product → Add to cart → Shipping info → Payment
2. **Shipping Address:** Use provided test address
   - 4120 Ivar Ave, Rosemead, CA 91770
   - Phone: 6263211250
3. **Payment:**
   - Test with mock payment (if available)
   - Likely requires real credit card for final processing
4. **Expected payment methods:**
   - Credit/Debit cards
   - Possibly PayPal
   - Apple Pay/Google Pay (likely)

## Timberland-Specific Considerations

### Loyalty/Rewards Program
- "Timberland VIP" or similar rewards program
- May offer 10% off first purchase with email signup
- Could affect pricing/discounts during checkout

### Regional Specifics
- US-focused commerce site
- Shipping to US addresses expected
- International shipping options possible

### Shipping
- Free shipping thresholds (typically $50+)
- Standard shipping (5-7 business days)
- Expedited options likely available

## Form Fields for Shipping (Estimated)
- First Name
- Last Name
- Street Address
- City
- State
- ZIP Code
- Phone Number
- Email (pre-filled from account)

## Payment Form Fields (Estimated)
- Card Number
- Expiration Date
- CVV
- Billing Address (same as shipping or different)

## Screenshots/Artifacts Needed
- [  ] Signup form with all fields visible
- [  ] Product page with "cheapest" item identified
- [  ] Cart page
- [  ] Shipping information form
- [  ] Payment entry form (payment step)

## Testing Status Summary
- Account Creation: INCOMPLETE (form validation issues)
- Cart Access: NOT TESTED (requires account)
- Shipping Form: NOT REACHED
- Payment Form: NOT REACHED
- Complete Checkout: NOT COMPLETED

## Notes for Future Attempts
1. All VF brands heavily protected with bot detection
2. Timberland was most accessible of the three options tested
3. Manual testing may be required due to Arkose requirements
4. Consider whether test requirements can be met with these protections in place
5. Agentmail email service works for receiving verification
6. SMS verification may require real phone number (Agentmail SMS limitations)
