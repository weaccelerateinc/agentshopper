# Best Buy Account Creation Flow

## Platform
- Best Buy proprietary e-commerce platform with Akamai bot detection

## URL
- Main site: https://www.bestbuy.com
- Signup page: https://www.bestbuy.com/identity/newAccount (with dynamic token parameter)
- Account dashboard: https://www.bestbuy.com/customer/myaccount

## Signup Form Fields
The "Create an Account" form includes:
- First Name (required)
- Last Name (required)
- Email Address (required)
- Password (required, with show/hide toggle; example pattern shown: "Nine+twelve=21")
- Confirm Password (required, with show/hide toggle and match validation)
- Mobile Phone Number (required)
- "Use for Account Recovery" checkbox (optional)
- Terms and Conditions, Privacy Policy, My Best Buy Terms links
- "Create an Account" button (blue)
- Google Sign-In option (bottom)

## Flow
1. Navigate to https://www.bestbuy.com
2. Click "Create an account" button (bottom right of homepage)
3. Wait for signup page to load (URL becomes /identity/newAccount with token)
4. Fill in all required fields (First Name, Last Name, Email, Password, Confirm Password, Phone)
5. Click "Create an Account" button
6. Account is created and user is redirected to /customer/myaccount (Account Home)
7. Email verification: Not required — account is active immediately
8. Confirmation: User sees "Sign Out" option and account navigation menu

## Password Requirements
- Minimum 15 characters
- Must include uppercase, lowercase, numbers, and special characters (based on example "Nine+twelve=21")
- Strong password validation enforced

## Common Issues & Bot Detection
- **Akamai Bot Detection**: Best Buy uses aggressive bot protection that may block automated signup attempts
  - Issue: "Sorry, something went wrong. Please try again." error message
  - Mitigation: Use natural delays between form fills (1-2 seconds per field), avoid rapid-fire interactions
  - If blocked, the signup form shows an error but fields remain filled
- **Form Submission Failures**: First submission attempt may fail silently; reload page and retry
- **Rate Limiting**: Multiple signup attempts from same IP/session may trigger temporary blocks
- **Session Tokens**: Signup URL requires a valid session token (tid parameter); tokens expire and new ones are issued per page load

## Account Recovery
- Phone number provided during signup is used for account recovery via SMS
- Email is primary contact for account communications
- Recovery phone checkbox allows user to specify if number should be used for recovery

## Integration Notes
- Account creation is successful when redirected to /customer/myaccount
- No email verification required — account is immediately usable
- Phone number format is auto-formatted (e.g., 6263211250 → 626-321-1250)
- Account can immediately be used for shopping and checkout
