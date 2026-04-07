# Newegg.com Account Creation Flow

## Platform
- Custom e-commerce platform (not Shopify)

## URL
- Login page: https://secure.newegg.com/identity/signin
- Signup is accessed FROM the login page — click "Sign Up" link at the bottom
- Direct signup URL: https://secure.newegg.com/identity/signup

## Signup Form Fields
The signup form shows:
- First and Last Name (single field, required)
- Email Address (required)
- Mobile Phone Number (optional)
- Password (required, with show/hide toggle)
- "Subscribe for exclusive e-mail offers and discounts" checkbox (checked by default)
- "SIGN UP" button
- Links to Privacy Notice and Terms of Use
- "Sign In with Google" button (social signup)
- "Sign In with Apple" button (social signup)

## Flow
1. Navigate to https://secure.newegg.com/identity/signin
2. Dismiss any region/location dialogs ("Stay at United States")
3. Dismiss cookie consent banner ("Reject Non-Essential" or "Accept All")
4. Click "Sign Up" link at the bottom of the login form
5. The page navigates to https://secure.newegg.com/identity/signup
6. Fill in First and Last Name, Email, Password (phone is optional)
7. Click "SIGN UP" button
8. Email verification: **Not required** — account is typically active immediately
9. Confirmation: redirected to homepage with account logged in
10. Account status shows in top right corner: "Welcome, [First Name] [Last Name]" with "Account & Lists" dropdown

## Password Requirements
- Must contain uppercase and lowercase letters (ABC, abc)
- Must contain at least one number (123)
- Must contain at least one special character (#@$)
- Must be 8-30 characters long
- Requirements are shown as checkmarks as you type

## Common Issues
- **Region/Location Dialog**: A popup may appear asking to select country/region — click "Stay at United States"
- **Cookie consent banner**: Shows "Manage Preferences" / "Accept All" / "Reject Non-Essential" — dismiss before interacting
- **Bot Detection & reCAPTCHA**: Newegg has reCAPTCHA and bot detection — interact naturally and slowly
- **Social login options**: Google and Apple signup are available but should be skipped for agentmail-based accounts
- **Newsletter subscription**: Checkbox is pre-checked for exclusive offers — can be left as-is
- **Blank page rendering**: If the page renders blank, try: `document.body.style.zoom='0.5'` in console
- **Duplicate email**: If email is already registered, an error message is displayed
- **Page load delays**: Newegg may have slow page loads — wait 2-3 seconds between actions

## Account Verification
- Email verification is NOT required for account activation
- Account becomes active immediately after signup
- Users can proceed to shopping/checkout without email confirmation
