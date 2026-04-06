# Away Account Creation Flow

## Platform
- Shopify Plus with Shopify New Customer Accounts (unified sign-in/create flow)

## URL
- Login / Register (unified): https://www.awaytravel.com/login
- Redirects to: `accounts.awaytravel.com/authentication/login` (Shopify-hosted auth page)
- **Note**: /register also redirects to the same unified auth page. There is NO separate registration form.

## Signup Form Fields
Away uses Shopify's new customer accounts system — a **two-step unified flow** (identical to Allbirds):
1. **Step 1**: "Continue with Shop" button + Email field + "CONTINUE" button. Checkbox: "Email me with news and offers" (pre-checked)
2. **Step 2**: If email is new, Shopify sends a **6-digit verification code** to the email. Enter the code to create the account. No password is set — authentication is passwordless via email codes.

There are no First Name, Last Name, or Password fields on the signup form.

## Flow
1. Navigate to https://www.awaytravel.com/login (redirects to accounts.awaytravel.com)
2. Enter the agentmail email address in the Email field
3. Uncheck "Email me with news and offers" checkbox if desired (pre-checked by default)
4. Click "CONTINUE"
5. Shopify sends a 6-digit verification code to the email address
6. Check agentmail inbox for the verification code using check_inbox.py
7. Enter the 6-digit code on the verification page
8. Account is created — passwordless authentication
9. Save email (no password) to Apple Keychain or note that auth is passwordless

## Password Requirements
- **No password** — Away uses Shopify's passwordless new customer accounts. Authentication is via email verification codes each time.

## Common Issues
- **Passwordless flow**: There is no password to generate or save — the user authenticates via email code each login
- **"Continue with Shop" button**: Shop Pay users can sign in via Shop — ignore this and use the email flow for agentmail
- **Verification code delivery**: The 6-digit code email may take a few seconds — poll agentmail inbox
- **No referral overlay on auth page**: The referral program overlay does not appear on the Shopify-hosted auth page (may appear on the main site)
- **No hCaptcha on auth page**: The Shopify new customer accounts auth page typically doesn't show hCaptcha
