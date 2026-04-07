# Backcountry.com Account Creation Flow

## Platform
- Custom platform (likely Salesforce Commerce Cloud) with passwordless authentication

## URL
- Home page: https://www.backcountry.com
- Signup/Login: Modal accessed via "Sign In" button in header (no dedicated signup page URL)

## Authentication Method
- **Passwordless Email Authentication**: Uses email verification codes instead of passwords
- No traditional password during signup — verification code sent to email

## Signup Form Fields
The modal "Sign In or Sign Up" shows:
- Email (required)
- "Remember me" checkbox
- Continue button
- Social options: "Continue with Google"
- "Sign In With Password" option (for existing accounts)
- Terms/Privacy notice: links to Terms of Use, Summit Club's Terms & Conditions, and Privacy Policy

## Flow
1. Navigate to https://www.backcountry.com
2. Click "Sign In" button in the top right header (account icon)
3. Modal "Sign In or Sign Up" appears with email field
4. Enter email address (e.g., garysmod@agentmail.to)
5. Check "Remember me" checkbox (optional)
6. Click "Continue" button
7. Page transitions to "Check Your Email" with 4-digit code entry fields
8. **Email Verification**: Retrieve 4-digit code from agentmail inbox (expires in 10 minutes)
9. Enter the 4-digit code in the input fields (auto-advances between fields)
10. Account is created and verified automatically
11. Confirmation: "Account Created" modal appears with green checkmark
12. Optional: Phone number entry modal for faster future logins — can "Skip for now"
13. Confirmation: redirected to homepage logged in with "Welcome! Summit Club Member" message

## Key Observations
- **No Password Required**: Passwordless flow uses email codes only
- **Automatic Account Creation**: First-time email creates the account immediately upon code verification
- **Summit Club Membership**: New accounts are automatically enrolled in the Summit Club program
- **Code Expiration**: Verification codes expire in 10 minutes
- **Phone Number Optional**: Phone can be added but is not required for account creation
- **Modal-Only Signup**: No dedicated signup page — all authentication happens in modals on the homepage

## Common Issues
- **Code Expires**: Verification codes expire after 10 minutes — may need to use "Resend" if too slow
- **Email Not Received**: Use agentmail API to check email or resend code via "Resend" button
- **Modal Rendering**: Modals may have rendering issues on some screen sizes (zoom issues observed)
- **Zoom Sensitivity**: Page may render blank on scroll — using `document.body.style.zoom='0.7'` can fix rendering
- **Post-Signup**: After successful verification, Summit Club membership is default (no upgrade step)

## Account Status After Creation
- Email verified ✓
- Account active ✓
- Summit Club Member status ✓
- Password: N/A (passwordless system)
- Additional onboarding: Optional phone number addition
