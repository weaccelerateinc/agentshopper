# Mercari Account Creation Flow

## Platform
- Peer-to-peer marketplace
- Custom checkout (not Shopify)

## URL
- Signup page: https://www.mercari.com/signup/?login_callback=%2F
- Homepage: https://www.mercari.com

## Signup Form Fields
The signup form on the dedicated signup page shows:
- Social login options: Continue with Google, Continue with Facebook, Continue with Apple
- Email address (required)
- Password (required, with show/hide toggle)
- Password strength indicator
- Terms & Privacy checkbox ("I agree to the Mercari Terms of Service and Privacy Policy")
- "Sign up" button (appears as submit button)

## Flow
1. Navigate to https://www.mercari.com
2. Click "Sign up" button in the top right
3. Page redirects to signup form at https://www.mercari.com/signup/?login_callback=%2F
4. Dismiss cookie consent banner if present ("Review details" / "Got it" buttons)
5. Fill in Email address
6. Fill in Password (8+ characters recommended for strength indicator)
7. Check the terms checkbox (required for form submission)
8. Click "Sign up" button
9. Email verification: **Not required** — account is typically active immediately
10. Confirmation: redirected to account dashboard/profile page (https://www.mercari.com/mypage/)
11. Username is auto-generated (e.g., ghrych1d)

## Password Requirements
- Minimum 8 characters (displays "Strong" strength indicator for good passwords)
- No strict complexity rules publicly documented

## Phone Verification
- **Not observed during signup flow** — account creation completes without phone verification
- May be required for selling or certain account features, but not for buyer registration

## Common Issues
- **Cookie consent banner**: Shows "Review details" / "Got it" buttons — dismiss with "Got it"
- **FedCM errors**: Google Sign-In may show FedCM abort errors in console — does not block form submission
- **Social login options**: Google, Facebook, and Apple signup are available but should be skipped for agentmail-based accounts
- **Form validation**: Email and password fields are validated client-side — ensure proper format
- **Terms checkbox**: Must be checked before submission — form will not submit without it
- **Duplicate email**: If email is already registered, submission may be blocked with inline error
- **reCAPTCHA**: May be present but does not typically block automated signup in standard testing
