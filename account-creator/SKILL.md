---
name: account-creator
description: Create burner accounts on ecommerce websites using agentmail.to for email and headed browser automation. Handles signup form filling, email verification (including 2FA), and saves credentials to Apple Passwords (macOS Keychain). Use when asked to create an account, sign up, or register on an ecommerce site. Currently supports hoka.com with extensible merchant support. Triggers on "create account", "sign up on", "register on", "make an account", "burner account".
---

# Account Creator

Create ecommerce accounts using agentmail.to email, headed browser, and Apple Passwords (macOS Keychain) credential storage.

## Setup (First-Time Only)

If `references/config.md` shows "(not configured)", run setup:

1. Ask user for their **agentmail.to API key** (get from https://console.agentmail.to)
2. Ask user for the **agentmail.to email address** to use for all signups
3. Ask user for **profile details**: first name, last name
4. Update `references/config.md` with all values
5. Verify macOS Keychain access: run `security list-keychains` to confirm default keychain is available

## Per-Account Creation Flow

### 1. Read Config
Read `references/config.md` for API key, email, and profile details.

### 2. Generate Password
```bash
python3 scripts/generate_password.py --length 16
```

### 3. Read Merchant Guide
Read the merchant-specific file from `references/` (e.g., `references/hoka.md`). Follow its step-by-step flow.

### 4. Browser Signup
Use the **headed browser** (not headless) to complete signup:
- Navigate to the merchant's signup URL
- Dismiss cookie banners / popups
- Fill form fields: first name, last name, email, password
- **Always opt-in to promotions/marketing/newsletter checkboxes**
- Submit the registration form
- Take a screenshot after submission for confirmation

**If CAPTCHA appears:** Stop and ask user to solve it manually, then continue.

### 5. Email Verification
Poll the agentmail inbox for the verification email:
```bash
python3 scripts/check_inbox.py <api_key> <inbox_email> --wait 120
```
- Parse the JSON output for `verification_link`
- Navigate to the verification link in the browser
- Confirm verification succeeded (screenshot)

### 6. Save to Apple Passwords
```bash
bash scripts/save_to_keychain.sh <domain> <email> <password>
```

### 7. Confirm to User
Report success with:
- Website
- Email used
- Password stored in Apple Passwords (don't display the password itself)
- Screenshot of completed registration

## Adding New Merchants

Create a new file in `references/` named `<domain>.md` following the pattern in `references/hoka.md`:
- Signup URL
- Form field names/layout
- Password requirements
- Verification flow specifics
- Common issues

## Dependencies
- **agentmail** Python package: `pip3 install agentmail`
- **macOS Keychain** (`security` CLI): built into macOS
- **Headed browser**: browser tool with headless=false

## Troubleshooting
- **Keychain access denied:** May need to allow terminal access in System Settings → Privacy → Automation
- **Verification email not arriving:** Increase --wait timeout, check spam filters on agentmail
- **CAPTCHA blocking signup:** Pause and ask user to solve manually
- **Form fields changed:** Update the merchant reference file with new selectors
