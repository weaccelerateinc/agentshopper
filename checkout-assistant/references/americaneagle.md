# American Eagle Checkout Flow

## Merchant Information
- **Merchant**: American Eagle Outfitters (ae.com)
- **URL**: https://www.ae.com/us/en/checkout
- **Checkout Type**: Multi-step form with shipping and payment sections

## Checkout Navigation Flow

### Step 1: Delivery Options
- **Ship To Me** (Selected by default)
- Free Store Pickup (Alternative option)
- Affects shipping method options available

### Step 2: Shipping Information
Required fields with validation:
1. **Email**: Contact email for order updates
   - Validation: Email format required
   - Visual indicator: Green checkmark when valid

2. **First Name**: Customer first name
   - Validation: Text field
   - Visual indicator: Green checkmark when filled

3. **Last Name**: Customer last name
   - Validation: Text field
   - Visual indicator: Green checkmark when filled

4. **Street Address**: Primary address line
   - Validation: Text field
   - Visual indicator: Green checkmark when filled

5. **Apt #, Floor, etc.**: Optional secondary address line
   - Not required
   - Text field

6. **City**: City name
   - Validation: Text field
   - Visual indicator: Green checkmark when filled
   - Test value: Rosemead

7. **State**: Dropdown selection
   - Validation: Required
   - Contains all 50 US states and territories
   - Test value: California (CA)

8. **Zip Code**: 5-digit postal code
   - Validation: Numeric, 5 digits
   - Visual indicator: Green checkmark when valid
   - Test value: 91770

### Step 3: Shipping Method
After address entry, shipping options appear:
- **Standard**: Free shipping (estimated 4-5 business days)
- **Two Day**: $15.00
- **Overnight**: $25.00

All options show estimated delivery dates.

### Step 4: Payment Section
Located below shipping method selection.

#### Payment Method Options:
1. **Credit or Debit Card** (Default)
   - Credit Card Number field (iframe-based input)
   - Exp. (MM/YY) field (iframe-based input)
   - CVV field (iframe-based input)
   - Phone Number field (required, must match card statement)

2. **PayPal** (Radio option)

3. **Afterpay** (Radio option)
   - Displays installment info: "4 interest-free payments of $38.09 every 2 weeks"

4. **Klarna** (Radio option)
   - Displays installment info: "4 interest-free payments of $38.09"

5. **Cash App Pay** (Radio option)

#### Billing Address:
- Checkbox for "Same as Shipping Address"
- If unchecked, separate billing form appears

### Step 5: Optional Information
- **Real Rewards Credit Card Offer**: 30% off first purchase, 16% back in rewards
- **Email Sign-up**: AE Emails and Aerie Emails subscription options
- **Donations**: Optional $1 donation to mental health support

### Step 6: Order Summary
Displays:
- Merchandise total
- Item discounts
- Shipping cost (or discount if free)
- Tax (state-dependent)
- Final order total

### Step 7: Submit
- **Place Order** button (bottom of form)
- Requires affirmation of Privacy Notice and Terms of Use

## Form Validation Details

### Real-time Validation:
- Green checkmark appears next to valid fields
- Fields show placeholder text in initial state
- Validation occurs on blur/change events

### Field Order (Left to Right):
- Email and optional secondary fields in top section
- Name fields (First/Last) side by side
- Address field spanning full width
- City and State side by side
- Zip Code field
- Continue with shipping method selection

## Test Checkout Data
- Email: gharychao@gmail.com (or test account email)
- First Name: Gary
- Last Name: Chao
- Street Address: 4120 Ivar Ave
- City: Rosemead
- State: CA (California)
- Zip Code: 91770

## Payment Fields
- Credit Card Number: Hidden/masked iframe input
- Exp Date: MM/YY format via iframe
- CVV: 3-4 digit security code via iframe
- Phone: Required, must match credit card statement

## Notes
- All address fields use live validation
- Shipping method changes may update tax/total
- Real Rewards loyalty program integrated throughout
- Multiple payment options available
- Form retains field values on validation errors
- Payment fields are iframe-based for PCI compliance

## Blockers/Considerations
- CAPTCHA may appear (use blocker if testing)
- Real Rewards enrollment may interrupt flow
- Email verification may be required
- Certain discount codes may have restrictions
- Address validation may flag unusual formats
