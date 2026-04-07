# TicketNetwork - Account Creation Reference

## Overview
TicketNetwork (https://www.ticketnetwork.com) is a ticket marketplace for buying and selling tickets to concerts, sports, and theater events. Account creation is required to purchase tickets.

## Registration URL
- Main site: https://www.ticketnetwork.com
- Registration page: https://secure2.ticketnetwork.com/?register=true

## Registration Form Fields
The registration form located at `secure2.ticketnetwork.com` contains the following fields:

### Required Fields
1. **Email**: Email address for account
   - Placeholder: "email@example.com"
   - Type: email input
   - Must be a valid email address

2. **Password**: Account password
   - Type: password input (can show/hide with "SHOW" button)
   - Requirements:
     - 12-24 characters
     - At least one letter
     - At least one number

### Optional/Preference Fields
3. **Email Preferences Checkbox**: "Yes, I want TicketNetwork.com to send me event updates and ticket discounts."
   - Type: checkbox
   - Default: checked/enabled
   - Links to Privacy Policy

4. **reCAPTCHA Verification**: "I'm not a robot"
   - Type: reCAPTCHA checkbox
   - Must be completed before registration

### Submission
- **Register Account Button**: Blue button at bottom of form to submit registration

## Form Behavior Notes
- The registration form uses a two-tab interface: "Sign In" and "Register"
- Form appears to be loaded dynamically/asynchronously
- Input validation occurs on form submission
- Google OAuth alternative available ("Or, register with... Google")

## Password Requirements
Clearly displayed on the form:
- 12-24 characters
- One letter (uppercase or lowercase)
- One number

## Navigation
- Top header has TicketNetwork logo linking back to main site
- Navigation options: Sports, Concerts, Theater categories
- Contact number: 860-533-4080
- Links to: About Us, Help, Terms & Conditions, Privacy Policy, Consumer Privacy Rights

## Post-Registration
After successful registration, a verification email will be sent to the provided email address. Users need to verify their email to complete account setup.

## Known Challenges
- Registration form inputs may require special handling due to dynamic form structure
- Form validation is strict and provides specific error messages
- Cookie requirements for login/registration functionality
- Form fields may not capture input using standard automation tools - may require alternative input methods or timing adjustments

## Mobile Considerations
- 100% Money-Back Guarantee displayed on footer
- Form is designed to work on both desktop and mobile

## Additional Information
- TicketNetwork is primarily for ticket exchange/resale (secondary marketplace)
- Ticket prices may be above face value
- No shipping address required for digital ticket delivery
