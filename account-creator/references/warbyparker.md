# Warby Parker Account Creation Flow

## Platform
- Custom (NOT standard Shopify) — uses Auth0 for authentication at auth.warbyparker.com

## URL
- Login: https://www.warbyparker.com/login (redirects to auth.warbyparker.com)
- Register: Navigate to login page, then click "Create an account" link
- Direct signup URL: auth.warbyparker.com/u/signup/identifier (but state param required, so always start from warbyparker.com/login)
- **Note**: /account/login and /signup are 404s — always use /login

## Signup Form Fields
The signup page at auth.warbyparker.com shows:
- "Sign up with Google" button (social signup)
- "Sign up with Apple" button (social signup)
- OR (divider)
- First Name* (required)
- Last Name* (required)
- Email address* (required)
- "Create account" button
- **No Password field** — Warby Parker uses passwordless authentication (email verification code or magic link)

## Flow
1. Navigate to https://www.warbyparker.com/login (redirects to auth.warbyparker.com)
2. Click "Don't have an account? Create an account" link at the bottom
3. Fill in First Name, Last Name, Email address
4. Click "Create account" button
5. Warby Parker sends a verification email/code to the email address
6. Check agentmail inbox for verification and complete it
7. Account is created — passwordless authentication
8. Save email to Apple Keychain (no password — auth is passwordless via email)

## Password Requirements
- **No password** — Warby Parker uses passwordless Auth0 authentication. Users authenticate via email verification codes or magic links.

## Common Issues
- **Auth0 hosted page**: Signup is NOT on warbyparker.com — it's on auth.warbyparker.com. The redirect happens automatically when navigating to /login
- **Passwordless**: No password to generate or save — authentication is via email
- **Social signup options**: Google and Apple Sign-In are offered but should be skipped for agentmail-based accounts (use email signup instead)
- **No standard Shopify flow**: Despite being a Shopify Plus store, Warby Parker uses custom Auth0 authentication, not Shopify's native customer accounts
- **No hCaptcha visible**: Auth0 page did not show CAPTCHA during testing, but may trigger on suspicious behavior
- **"Fill with Accelerate" button**: May appear in bottom-right corner (browser extension) — ignore it
