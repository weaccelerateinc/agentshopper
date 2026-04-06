# Allbirds.com Account Creation Flow

## Platform
- Shopify Plus with Shopify New Customer Accounts (unified sign-in/create flow)

## URL
- Login / Register (unified): https://www.allbirds.com/account/login
- Redirects to: `accounts.allbirds.com/authentication/login` (Shopify-hosted auth page)
- There is NO separate /account/register page

## Signup Form Fields
Allbirds uses Shopify's new customer accounts system — a **two-step unified flow**:
1. **Step 1**: Email field + "Continue" button (also offers "Continue with Shop" for Shop Pay users)
2. **Step 2**: If email is new, Shopify sends a **6-digit verification code** to the email. Enter the code to create the account. No password is set — authentication is passwordless via email codes.

There are no First Name, Last Name, or Password fields on the signup form. Name and profile details may be collected later in account settings.

## Flow
1. Navigate to https://www.allbirds.com/account/login (redirects to accounts.allbirds.com)
2. Dismiss cookie consent banner if it appears
3. Enter the agentmail email address in the Email field
4. Uncheck "Email me with news and offers" checkbox if desired (pre-checked by default)
5. Click "Continue"
6. Shopify sends a 6-digit verification code to the email address
7. Check agentmail inbox for the verification code using check_inbox.py
8. Enter the 6-digit code on the verification page
9. Account is created — passwordless authentication
10. Save email (no password) to Apple Keychain or note that auth is passwordless

## Password Requirements
- **No password** — Allbirds uses Shopify's passwordless new customer accounts. Authentication is via email verification codes each time.

## Common Issues
- **Passwordless flow**: There is no password to generate or save — the user authenticates via email code each login
- **"Continue with Shop" button**: Shop Pay users can sign in via Shop — ignore this and use the email flow for agentmail
- **Verification code delivery**: The 6-digit code email may take a few seconds — poll agentmail inbox
- **Cookie banner**: May overlay the page on first visit — dismiss before interacting
- **No hCaptcha on auth page**: The Shopify new customer accounts auth page typically doesn't show hCaptcha (unlike classic Shopify registration)
