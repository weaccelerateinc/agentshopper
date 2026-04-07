# Torrid — Account Creator Reference

## Platform Architecture
- **Storefront**: Demandware (Salesforce Commerce Cloud) powered e-commerce
- **Authentication**: Email/password account creation with phone and postal code verification
- **Device Verification**: Initial page load triggers device verification challenge before displaying content

## Signup Form Fields & Selectors

### Step 1: Initial Information Collection
- **Email Address**: `input[type="email"]` labeled "EMAIL ADDRESS"
- **Phone Number**: `input[type="tel"]` labeled "PHONE NUMBER"
- **Postal Code**: `input[type="text"]` labeled "ZIP/POSTAL CODE"
- **CTA**: Button labeled "Continue" or "Next" to proceed

### Step 2: Account Details (Password & Personal Info)
- **Email** (pre-filled): Read-only display of email from Step 1
- **First Name**: `input[type="text"]` labeled "FIRST NAME"
- **Last Name**: `input[type="text"]` labeled "LAST NAME"
- **Password**: `input[type="password"]` labeled "PASSWORD"
- **Confirm Password**: `input[type="password"]` labeled "CONFIRM PASSWORD"
- **Age Confirmation**: Yes/No buttons for "ARE YOU AT LEAST 18 YEARS OF AGE OR OVER?" (required)

### Step 3: Additional Details (Birthday, Address)
After clicking "Yes" on age confirmation, form expands to include:
- **Birthdate (Month)**: Dropdown `select[name*="month"]` or similar for month selection (e.g., "January", "February", etc.)
- **Birthdate (Year)**: Dropdown `select[name*="year"]` or `input[type="text"]` for year (format: YYYY, e.g., "1990")
- **Country**: Dropdown defaulting to "UNITED STATES"
- **Address Line 1**: Text input for street address
- **Address Line 2** (optional): Text input for apartment/suite number
- **City**: Text input for city
- **State/Province**: Dropdown for state selection
- **CTA**: Button labeled "Create Account" or similar to submit

## Gotchas & Notes

### Device Verification
- **First load** of torrid.com triggers a "Verifying the device..." screen with a loading spinner
- This is a Demandware security measure; wait 3-5 seconds for device verification to complete before interacting with forms

### Form Validation
- Password must meet specific requirements (visible checklist):
  - 8-24 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one special character (e.g., `!@#$%^&*()_+-=[]{}|;':",./<>?`)
- Age confirmation ("YES" to 18+) is **mandatory** — form does not proceed without this selection
- Phone and postal code are required fields on initial screen

### Demandware Quirks
- Form may use Demandware's proprietary AJAX for progression (not full page reload)
- Dropdown selects may be rendered as custom UI elements — use `find` to locate them dynamically if standard select selectors fail
- Final account creation button may appear as "Create Account" or "CONTINUE" depending on page variant

### Optional Email Signup
- A modal may appear prompting to join Torrid Rewards program or opt into email marketing
- This is optional and can be dismissed; proceed to account verification regardless

## Email Verification
- After account creation, a confirmation email is sent to the provided email address
- Email contains a verification link or code
- Polling the Agentmail API at `api.agentmail.to/v0/inboxes/{email}/messages` with Bearer token can retrieve the email
- Extract verification token from email body and complete verification to activate account

## Test Data Template
```
Email: {test_email}@agentmail.to
Password: AgentShop2026!  (or similar strong password)
Phone: 6263211250
Postal Code: 91770
First Name: Gary
Last Name: Chao
Birthdate: January 1, 1990 (or any date making account holder 18+)
Address: 4120 Ivar Ave, Rosemead, CA 91770
```

## Fill Strategy
1. Wait for device verification to complete
2. Fill initial form (Email, Phone, Postal Code) and click Continue
3. On Step 2, fill First Name, Last Name, Password, Confirm Password
4. Click "Yes" for age confirmation
5. On Step 3, fill Birthdate (Month/Year), Address fields
6. Click "Create Account"
7. Poll Agentmail for verification email
8. Extract and follow verification link
9. Confirm account is active by attempting login
