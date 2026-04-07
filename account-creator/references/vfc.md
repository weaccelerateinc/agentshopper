# VF Corporation Merchant Testing - Account Creation Reference

## Overview
**Merchant:** VF Corporation (https://www.vfc.com)
**Status:** Corporate holding company site (non-consumer)
**Actual Site Tested:** Timberland.com (https://www.timberland.com) - VF-owned brand
**Test Date:** April 2026

## Key Findings

### VF Corporation Corporate Site
- **URL:** https://www.vfc.com
- **Nature:** Holding company website with no consumer shopping functionality
- **Content:** Company information, investor relations, brands portfolio (Vans, The North Face, Timberland, Dickies, JanSport, Smartwool, Eastpak, Altra, Icebreaker, Kipling, Napapijri)
- **Navigation:** Menu sections include Company, Brands, Responsibility, News, Investors, Careers, Contact

### Portfolio Brands Evaluated
1. **Vans.com** - Could not complete signup due to Arkose bot detection middleware requiring "Press & Hold" verification (requires human interaction)
2. **The North Face (thenorthface.com)** - Blocked by same Arkose bot detection system with modal dialogs
3. **Timberland.com** - Successfully loaded and attempted signup

## Timberland Account Creation Flow

### Signup Form Location
- URL with sign-up modal: https://www.timberland.com/en-us#panel=sign-up
- Modal appears when clicking "Join Now" button on homepage

### Form Fields Required
1. **First Name** - Text input, required
2. **Last Name** - Text input, required
3. **Date of Birth** - Text input, format MM/DD/YYYY, required
4. **Mobile Number** - Tel input with +1 country code default
5. **Email** - Email input, required
6. **Password** - Password input with requirements:
   - 8 or more characters
   - 1 uppercase letter
   - 1 lowercase letter
   - 1 number

### Checkboxes (All Required for Submission)
- SMS/Text message consent checkbox (optional but recommended)
- Sign up for latest Timberland offers checkbox
- I agree to Community Terms of Service checkbox (REQUIRED - form validation)
- I accept Timberland's Terms and Conditions checkbox (REQUIRED - form validation)

### Test Credentials Used
- Email: garysmod@agentmail.to
- Password: AgentShop2026! (meets all requirements)
- First Name: Gary
- Last Name: Chao
- Date of Birth: 01/01/1990
- Phone: 6263211250

## Blockers and Challenges

### Primary Challenge: Bot Detection System
Both Vans and The North Face use **Arkose** fraud detection that requires:
- "Press & Hold" button interaction to verify human interaction
- This cannot be automated programmatically
- Blocks all account creation and checkout flows

### Secondary Challenge: Timberland Form Validation
- Form validation issues on submission (fields being cleared)
- Multiple checkbox validation states required
- Form appeared to reject submission even with all fields filled

## Form Validation Rules
- Date of Birth field validation appears strict
- All three consent checkboxes must be checked (not just terms)
- Community Terms checkbox validation is critical

## Recommendations for Future Testing

1. **Use manual testing** for VF brands due to Arkose presence
2. **Alternative approaches:**
   - Test on browsers with user-like behavior (avoid detection)
   - Use headless browser with human-like interactions
   - Consider timing/delays between form fills

3. **For checkout testing:**
   - Arkose blocks access to cart/checkout flows
   - Would require passing bot detection first
   - Consider simpler VF brand alternatives if available

## Account Status
- Account creation: INCOMPLETE (form validation issues)
- Signup form: ACCESSIBLE
- Bot detection: CONFIRMED on Vans and The North Face

## Notes
- Timberland.com uses Salesforce Commerce Cloud platform
- VF Corporation sites are heavily bot-protected
- SMS verification requirement may require real phone number (Agentmail may not support SMS)
