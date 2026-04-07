# H&M Account Creation Flow

## Platform
- Custom platform (not Shopify)
- H&M Membership program

## URLs
- Main site: https://www.hm.com/en_us/index.html
- Direct subdomain (geo-blocked): https://www2.hm.com/en_us/index.html — may return "Access Denied"
- Signup accessed via: Click account icon (top-right) on any page

## Signup Modal
The signup is presented as a modal dialog titled "BECOME AN H&M MEMBER" with:
- Email (required, verified with checkmark on entry)
- Create a password (required, with show/hide toggle)
- Date of birth (required, MM/DD/YYYY format)
- Optional: "ADD MORE INFO TO EARN MORE POINTS" (expandable section)

## Password Requirements
- 8-25 characters only
- Minimum 1 number
- Minimum 1 uppercase letter
- Minimum 1 lowercase letter
- No spaces

## Flow
1. Navigate to https://www.hm.com/en_us/index.html (or click "United States" on entrance page if geo-blocked)
2. Handle cookie consent: Click "COOKIES AND SERVICES SETTINGS" → "ONLY REQUIRED COOKIES"
3. Click account icon (top-right) to open sign-in modal
4. Enter email address (agentmail format: garysmod@agentmail.to)
5. Click "CONTINUE" button
6. Modal switches to "BECOME AN H&M MEMBER" form
7. Fill in password (must meet all 5 requirements above)
8. Fill in date of birth (MM/DD/YYYY)
9. Optional: Expand "ADD MORE INFO TO EARN MORE POINTS" for first/last name and address fields
10. Click "CREATE ACCOUNT" button (or similar submit button)
11. Email verification: Unknown — may require verification email from agentmail
12. Check agentmail inbox: `curl -s -H "Authorization: Bearer <API_KEY>" "https://api.agentmail.to/v0/inboxes/<email>/messages?limit=10"`

## Known Issues
- **Password input field**: May not accept keyboard input reliably; try clicking eye icon first, then entering password
- **Date of birth validation**: Must be in exact MM/DD/YYYY format (no alternative formats observed)
- **Geo-restriction**: www2.hm.com may return "Access Denied" — use www.hm.com instead
- **Modal scrolling**: Content scrolls within the modal; scroll down to see all fields and submit button
- **Cookie consent**: Two-step process — initial "ACCEPT ALL" vs. settings panel

## Reusable Account Profile
Store credentials locally for subsequent sessions. Do not commit credentials to repository.

## Email Verification
- Email must be verified; agentmail provides API access to check inbox
- Verification link will arrive in agentmail inbox
- H&M Membership is the loyalty program — first-time signup may auto-activate or require email click

## Common Issues & Workarounds
- **Password field not accepting input**: Try clicking the visibility toggle (eye icon) first
- **Date of birth field empty after entry**: Ensure format is MM/DD/YYYY with forward slashes
- **Modal stuck/unresponsive**: Dismiss (X button) and re-open account modal
- **"H&M MEMBERSHIP" link in modal**: Provides information about the loyalty program
- **Performance**: Page may be slow on first load; wait 2-3 seconds before interacting with form
