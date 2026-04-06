# VictoriasSecret.com Account Creation Flow

## Platform
- Custom e-commerce (Bath & Body Works / Victoria's Secret group)

## URL
- Login / Register (unified): https://www.victoriassecret.com/us/account/signin

## Signup Form Fields
Victoria's Secret uses a **unified two-step flow** titled "Sign In or Create Account":
1. **Step 1**: Email Address field + "CONTINUE" button
2. **Step 2**: If the email is new, the page expands to show additional fields for account creation (Password, First Name, Last Name, etc.). If the email is already registered, it shows a password field for sign-in.

The initial page does NOT show all fields upfront — only the Email field and CONTINUE button are visible.

## Flow
1. Navigate to https://www.victoriassecret.com/us/account/signin
2. A "Shipping outside United States?" banner may appear — click "STAY ON THIS SITE"
3. Dismiss cookie consent banner (click "OK") if it appears
4. Enter the agentmail email address in the "Email Address*" field
5. Click "CONTINUE"
6. If email is new: additional registration fields appear (Password, First Name, Last Name, etc.)
7. Fill in the additional fields
8. Click "Create Account" (or equivalent submit button)
9. Email verification: **May be required** — check agentmail inbox for verification link
10. If verification email arrives, click the verification link
11. Confirmation: redirected to account dashboard
12. Save credentials to Apple Keychain

## Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

## Common Issues
- **Unified sign-in/create flow**: There is NO separate "Create Account" tab — the form adapts after you enter an email and click CONTINUE
- **Shipping location banner**: A "Shipping outside United States?" banner appears on first visit — click "STAY ON THIS SITE" before interacting with the form
- **Cookie consent banner**: "Cookies and Tracking Technologies" dialog with "OK" / "PREFERENCES" buttons appears on first visit — dismiss it
- **Slow page load**: The sign-in form takes several seconds to render after the page chrome loads — wait for the spinner to finish
- **Dual account system**: Victoria's Secret has a standard e-commerce account AND a separate credit card account (via Comenity Bank) — only create the standard e-commerce account
- **Pop-up modals**: Marketing modals and email capture pop-ups may overlay the page — dismiss before interacting
- **CAPTCHA**: May trigger on repeated attempts — if it appears, ask user to solve manually
