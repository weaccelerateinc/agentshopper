# Hoka.com Account Creation Flow

## URL
- Account page: https://www.hoka.com/en/us/login/
- (Old register URL /account-register is dead — use login page and click "Join Us" tab)

## Signup Form Fields
Navigate to the login URL, then click the **"Join Us" tab**. The form has:
- First Name (ref: textbox "* First Name")
- Last Name (ref: textbox "* Last Name")
- Email Address (ref: textbox "* Email Address")
- Password (ref: textbox "* Password")
- Phone Number (optional — "Opt-In for more exclusive benefits!")
- Zip Code (optional — "Get notified for local events!")
- Birthday (optional — "Receive a free gift every year!", format mm/yyyy)
- Membership checkbox (required — must click to accept terms)
- "Join for Free" button

## Flow
1. Navigate to https://www.hoka.com/en/us/login/
2. CAPTCHA may appear (slide-to-verify) — if so, ask user to solve manually
3. Click "Join Us" tab
4. Fill in First Name, Last Name, Email, Password
5. Click the membership agreement checkbox (opt-in to promotions)
6. Click "Join for Free" button
7. Account is created immediately — NO email verification required
8. Confirmation: page shows "Welcome to the crew!" with membership dashboard
9. Save credentials to Apple Keychain

## Common Issues
- **CAPTCHA on first visit** — Hoka uses aggressive anti-bot. User must solve manually
- Password requirements: 8+ chars, uppercase, lowercase, number, special char
- No email verification needed — account is active immediately after signup
- The old /account-register URL is dead (404) — always use /login/ + "Join Us" tab
