# Teleflora Account Creation Reference

## Overview
Teleflora (https://www.teleflora.com) is an online florist that allows customers to send flowers and gifts. Account creation is required for checkout.

## Signup Page
- URL: https://www.teleflora.com/account/login.jsp (has "CREATE A NEW ACCOUNT" button)
- Alternative direct URL: https://www.teleflora.com/account/signup.jsp

## Required Signup Fields
1. **Email Address** (required)
   - Input type: email
   - Field name: email address

2. **Password** (required)
   - Input type: password
   - Password requirements: At least 7 characters, must contain both letters and numbers

3. **Confirm Password** (required)
   - Input type: password
   - Must match the password field

4. **First Name** (required)
   - Input type: text

5. **Last Name** (required)
   - Input type: text

6. **Phone Number** (required)
   - Input type: tel
   - Used to contact recipient for delivery

7. **Birthday** (optional but has fields)
   - Fields: Month dropdown, Day dropdown
   - No Year field visible

8. **Gender** (optional)
   - Dropdown: "Select Gender"
   - Options: Female, Male, Select Gender

9. **Marital Status** (optional)
   - Dropdown: "Select Marital Status"
   - Options include: Married, Single, Living with partner, Divorced

## Form Submission
- Submit button is located below the marital status field (requires scrolling)
- Form validation occurs before submission
- Required fields must be filled before submission

## Important Notes
- Email popup/modal may appear on page load offering 20% off - can be dismissed
- Form uses JavaScript-based submission
- URL structure suggests JSP backend
- Session ID parameter required for signup requests

## Test Account Credentials Used
- Email: garysmod@agentmail.to
- Password: AgentShop2026!
- First Name: Gary
- Last Name: Chao
- Phone: 6263211250

## Known Issues/Blockers
- Form submission validation may reject incomplete entries
- Birthday field defaults need to be populated for successful submission
- Form may require additional hidden fields for successful account creation
