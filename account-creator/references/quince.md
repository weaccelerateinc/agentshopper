# Quince.com Account Creation Flow

## Platform
- Quince Direct-to-Consumer Fashion (Shopify-based)

## URL
- Login/Signup page: https://www.quince.com/log-in
- Single unified login/signup form at the same URL

## Signup Form Fields
The login page shows:
- Email (required) — "Continue" button advances to next step
- Password (required) — "Continue" button to submit
- "Continue with Google" button (social signup)
- Terms/Privacy notice at bottom

## Flow
1. Navigate to https://www.quince.com/log-in
2. Enter email address
3. Click "Continue" button
4. If email does NOT exist: Shows "WELCOME BACK!" message with password field (this is actually signup for new email)
5. If email already exists: Shows "Incorrect password, please try again" message
6. For new account: Enter password and click "Continue"
7. **Email Verification Required**: Quince sends a one-time code (6 digits) to the email
8. Check email inbox (via agentmail API or dashboard)
9. Enter the code on the Quince page — typically expires in 10 minutes
10. Upon code verification: Account is created and logged in, redirected to account dashboard
11. Save credentials to Apple Keychain

## Password Requirements
- Minimum 8 characters (appears to include special characters)
- Example: AgentShop2026! (works fine)
- No publicly documented complexity rules but mixed case + numbers + special chars recommended

## Email Verification
- **Required**: One-time code (6-digit) is sent to the signup email
- Code appears in inbox within seconds
- Can be resent by clicking "Resend" link on the verification page
- Code expires in ~10 minutes (shows countdown timer: "expire in 10 minutes")

## Common Issues
- **Email already registered**: Shows "Incorrect password" message even for signup flow — use a different email or existing credentials
- **Code verification timeout**: If code expires, click "Resend" to get a new one
- **Social login**: "Continue with Google" is available but should be skipped for agentmail-based accounts
- **Two-step authentication**: Not observed during testing — standard single-step flow
- **Page rendering**: Some pages may render blank initially — applying `document.body.style.zoom='0.5'` via JavaScript can help with rendering issues on checkout pages

## Notes
- Uses one-time code (OTC) based verification instead of email link clicks
- The "Welcome Back!" message appears for NEW emails (confusing UX but correct behavior)
- Free shipping and 365-day returns are prominently displayed
- Account creation is immediate upon code verification
