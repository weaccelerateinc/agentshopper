# Bombas.com Account Creation Flow

## Platform
- Standard Shopify (not Plus)

## URL
- Login page: https://www.bombas.com/account/login
- Signup is accessed FROM the login page — click "Don't Have An Account? Sign Up" link at the bottom
- **Note**: https://www.bombas.com/account/register renders a BLANK page — do NOT use it

## Signup Form Fields
After clicking "Sign Up" on the login page, the form shows:
- Email (required)
- First Name (required) + Last Name (required) — side by side on same row
- Password (required, with show/hide toggle)
- "Sign Up" button
- "Continue with Facebook" button (social signup)
- "Continue with Google" button (social signup)
- Terms/Privacy notice text (implicit acceptance on signup)

## Flow
1. Navigate to https://www.bombas.com/account/login
2. Dismiss cookie consent banner ("I Decline" button) if it appears
3. Click "Don't Have An Account? Sign Up" link at the bottom of the login form
4. The page switches to the Sign Up form (same URL)
5. Fill in Email, First Name, Last Name, Password
6. Click "Sign Up" button
7. Email verification: **Not required** — account is typically active immediately
8. Confirmation: redirected to account dashboard
9. Save credentials to Apple Keychain

## Password Requirements
- Minimum 5 characters (Shopify default)
- No strict complexity rules publicly documented

## Common Issues
- **Blank /account/register page**: The direct register URL renders empty — always use the login page and click "Sign Up"
- **Cookie consent banner**: Shows "I Decline" / "I Agree" / "Cookie Settings" — dismiss before interacting with the form
- **Social login options**: Facebook and Google signup are available but should be skipped for agentmail-based accounts
- **Newsletter incentive pop-up**: "Want 20% Off?" pop-up may appear — dismiss if present
- **Promo banner**: Site banner shows "20% Off First Order with Code COMFORT20" — this is informational, not blocking
- **hCaptcha**: May trigger — if it appears, ask user to solve manually
- **Duplicate email**: If email is already registered, an inline error is shown
