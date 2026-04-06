# Glossier.com Account Creation Flow

## Platform
- Shopify Plus

## URL
- Register: https://www.glossier.com/account/register
- Login: https://www.glossier.com/account/login

## Signup Form Fields
Navigate to the register URL. The form has:
- First name (required)
- Last name (required)
- Email (required)
- Password (required)
- Checkbox: "By clicking here, I agree to the Terms of Use and Privacy Policy" (required)
- Checkbox: "Sign up for emails on products, events, and goings-on" (optional)
- Checkbox: "Get our texts!" SMS opt-in (optional)
- "Create an account" button
- Also shows: "Sign in to Glossier.com" link below

## Flow
1. Navigate to https://www.glossier.com/account/register
2. No aggressive email pop-up was observed during testing — but if one appears, close it via the X button
3. Fill in First name, Last name, Email, Password
4. Check the Terms of Use agreement checkbox (required)
5. Optionally uncheck the email and SMS opt-in checkboxes
6. Click "Create an account" button
7. Email verification: **May be required** — check agentmail inbox
8. If verification email arrives, click the verification link
9. Confirmation: redirected to account page
10. Save credentials to Apple Keychain

## Password Requirements
- Minimum 5 characters (Shopify default)
- No strict complexity rules publicly documented

## Common Issues
- **Email signup footer**: A persistent email signup section appears in the page footer (with "Email Address" input) — this is NOT the account creation form, just a newsletter signup widget. Ignore it
- **Locale redirect**: Glossier may redirect to a localized version (e.g., /en-th/) based on detected location — this does not affect account creation but prices may show in local currency
- **Terms checkbox required**: The Terms of Use checkbox must be checked or the form will not submit
- **hCaptcha**: Shopify hCaptcha may trigger — if it appears, ask user to solve manually
- **Membership incentive**: Glossier may advertise member perks during signup (free gifts, limited-edition items) — no action needed, just complete the form
