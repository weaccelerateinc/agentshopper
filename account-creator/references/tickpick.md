# TickPick Account Creation Flow

## Platform
- Custom e-commerce platform (ticket marketplace)
- No direct registration URL; signup accessed from homepage modal

## URL
- Homepage: https://www.tickpick.com
- Account login: https://www.tickpick.com/account/signin (inferred from UI)
- Signup is accessed via modal button on homepage — click "Sign Up" button in top-right nav

## Signup Form Fields
After clicking "Sign Up", a modal presents:
- Social signup options: "Continue with Google", "Continue with Apple"
- "Continue with Email" button
- Clicking "Continue with Email" shows:
  - Email field (required)
  - Two options:
    - "Send Signup Code" (6-digit code verification flow)
    - "Sign up with Password" (email + password)

## Flow (Password Route — Recommended)
1. Navigate to https://www.tickpick.com
2. Click "Sign Up" button in top-right navigation
3. A modal opens with signup options
4. Click "Continue with Email"
5. Click "Sign up with Password"
6. Fill in Email field
7. Fill in Password field (must meet requirements: 7+ chars, special char, capital letter)
8. Review/accept terms: "By purchasing a ticket or signing up, you agree to the user agreement and privacy policy"
9. Click "Sign Up" button
10. Email verification: **Not required** — account is active immediately and user is logged in
11. Confirmation: redirected to homepage with account logged in (profile avatar visible in top-right)

## Password Requirements
- Minimum 7 characters
- Must contain at least one special character
- Must contain at least one capital letter

## Alternative Flow (Code Verification)
- Click "Send Signup Code" instead of password signup
- Email receives 6-digit verification code
- Use Agentmail API to poll for code if needed: `curl -s -H "Authorization: Bearer <API_KEY>" "https://api.agentmail.to/v0/inboxes/<email>/messages?limit=10"`
- Enter code to complete signup

## Common Issues
- **Social login options**: Google and Apple signup are available but should be skipped for agentmail-based accounts
- **No password verification field**: TickPick shows password as dots but does not require re-entry
- **Modal-only signup**: The direct signup URL does not exist — must use homepage modal
- **Implicit login**: Account is immediately active; no separate login step required after signup
- **Terms acceptance**: Implicit acceptance via signup — no separate checkbox required

## Post-Signup
- User is automatically logged in
- Profile avatar (initial letter in circle) appears in top-right
- Redirect to homepage is typical; user can immediately browse or search tickets
