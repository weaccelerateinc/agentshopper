# UGG Account Creation Reference

## Overview
UGG (ugg.com) is a consumer-facing brand owned by Deckers. This reference documents the signup flow on the UGG website.

## Signup URL
- **Primary Signup**: https://www.ugg.com/ -> Click "My Account" -> "Create Account"
- **Direct Signup Modal**: Account creation happens via a modal/dropdown overlay on the homepage

## Signup Form Fields
The UGG signup form includes the following fields:
- **Email Address** (required) - text input, type="email"
- **Password** (required) - text input, type="password" with show/hide toggle
- **Terms Checkbox 1** (required) - "Yes, I want to join the UGG Rewards program. By joining UGG Rewards, I verify that I am 13 years of age or older and I agree to the Terms & Conditions and Privacy Policy"
- **Terms Checkbox 2** (optional) - "Add me to the UGG email list to hear about collaborations, price drops and more. I understand that UGG does not share or sell personal information."

## Signup Process
1. Navigate to https://www.ugg.com/
2. Click "My Account" button in top right
3. Click "Create Account" link
4. Fill in email address
5. Fill in password
6. Check both checkboxes (at minimum, the first one is required)
7. Click "Create Account" button

## Email Verification
- UGG does NOT appear to require explicit email verification before account creation
- The account may be created immediately, or a verification email may be sent
- Status unclear due to proxy limitations preventing email API access during testing

## Known Issues/Blockers
- **CAPTCHA Protection**: UGG has Cloudflare protection that triggers a CAPTCHA challenge ("Verification Required") when unusual activity is detected from automated tools
- The CAPTCHA appears after certain interactions (e.g., adding items to cart, accessing account)
- This CAPTCHA cannot be solved programmatically and blocks further interaction

## Login Flow
- Email address and password fields are available on the same modal
- "Log In" button for existing users
- "Create Account" link for new users

## Account Status After Signup
After submitting the signup form, the modal closes and user is returned to homepage. The signup appears to be successful, though verification status is uncertain.

## Technical Notes
- Forms use standard HTML form submission
- No AJAX requirements for form submission visible
- Cookie-based session management
- User agent: Standard Chrome browser

## Related Pages
- Login: https://www.ugg.com/ -> "My Account" -> "Login"
- Products: Various category pages (Women, Men, Kids, etc.)
- Cart: Cart icon in top right, or direct access via /cart

## Form Validation
- Password field includes a tooltip explaining password requirements
- Email field validates email format
- Both checkboxes must be checked to submit form
