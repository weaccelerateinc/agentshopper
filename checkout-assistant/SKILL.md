---
name: checkout-assistant
description: Log into supported ecommerce sites with the user’s existing account, gather coupon codes and active deals discovered by deal-digest, then guide or execute cart and checkout steps in a headed browser until the final payment screen. Use when asked to log in, add one or more items to cart, apply coupons or member rewards, optimize discount usage, or stop at payment for review. Start with hoka.com and prefer user-visible, headed browser sessions with screenshots before payment submission.
---

# Checkout Assistant

Log into a supported merchant account, build a cart with one or more requested items, apply the best available coupon or member reward, and stop at the payment/review step with a screenshot.

## Scope

Use this skill only for user-authorized shopping on accounts the user owns. Do not submit payment unless the user explicitly asks.

Initial supported merchant:
- `hoka.com`

## Inputs

Expect either:
- a single product URL with optional size / color / quantity, or
- a list of items, each with product URL plus optional size / color / quantity

Also expect:
- whether to stop before payment submission (default: yes)
- whether to reuse the saved checkout profile or collect a new one

## Read First

1. Read `../account-creator/references/config.md` for the account-creation context.
2. Read `../deal-digest/references/deals-active.json` if it exists.
3. Read merchant notes from `references/hoka.md`.
4. Read `references/checkout-profile.json` if it exists.
5. If `references/checkout-profile.json` does not exist, read `references/checkout-profile.template.json`, collect the missing fields from the user, and create the local profile file before continuing.

The reusable checkout profile should contain:
- phone
- first name
- last name
- address line 1
- address line 2 (optional)
- city
- state
- zip
- country

Never commit a real `references/checkout-profile.json` containing personal data.

## Setup for a New User

Before the first checkout for a new user:
- copy `references/checkout-profile.template.json` to `references/checkout-profile.json`
- fill in the user’s shipping/contact values
- confirm the merchant login exists and can be accessed safely through the user’s browser or password manager
- keep `checkout-profile.json` local/private; do not publish it to GitHub

## Checkout Workflow

### 1. Collect login state

For merchants previously created with `account-creator`, first try the browser with the existing saved login state/cookies. If the session is logged out:
- ask the user for permission to use the stored account credentials
- retrieve credentials from Apple Passwords / macOS Keychain manually through the browser password manager or user assistance
- never print the password in chat

### 2. Gather candidate discounts

Build a candidate list from `../deal-digest/references/deals-active.json`:
- prioritize deals where `brand` or sender clearly matches the merchant
- include merchant-specific promo code, expiration, and source email metadata when available
- ignore expired deals
- if multiple codes exist, try the most specific merchant code first, then the highest discount, then the most urgent expiration
- if the merchant forbids stacking, keep the best single code that successfully applies

If no structured deal file exists, proceed without coupons and tell the user.

### 3. Use a headed browser

Use a visible browser session, not headless. For Hoka and similar merchants, headed sessions are preferred because login/cart flows may fail or get blocked in headless mode.

### 4. Cart-building actions

Support both single-item and multi-item carts.

For each requested item:
- open the product URL
- verify color from the URL or choose the requested color if needed
- choose size if required
- choose quantity if specified
- add the item to cart
- confirm the cart count increased or the line item appears
- handle cookie banners / modals / promotional overlays

For Hoka specifically, repeat the product-page flow for each item before entering checkout. Do not assume the cart only contains one product.

### 5. Login

If cart or checkout requires auth:
- navigate to the login flow
- sign in with the existing user account
- if MFA or CAPTCHA appears, pause and ask the user to complete it manually in the visible browser
- continue once the page reflects successful login

### 6. Checkout profile, rewards, and coupon application

- enter checkout after the full cart is built
- prefill shipping/contact details from `references/checkout-profile.json` when available
- if the checkout profile is missing, ask the user for it once and save it for future runs
- inspect merchant-native rewards first (for Hoka: membership rewards / welcome boosts shown in checkout)
- find promo / coupon code field
- try candidate coupons or rewards one at a time, serially
- after each attempt, confirm whether the code/reward applied or was rejected
- keep notes on which option produced the best total
- if the merchant forbids stacking, keep the single best reward/coupon and stop trying others
- do not brute force or spam many codes; only try a small, relevant set

### 7. Stop before payment

Default behavior:
- continue through shipping / review until the page asks for payment details or displays the final payment/review screen
- capture a screenshot
- report the applied code, current subtotal/discount if visible, and that the flow is waiting for payment confirmation

Do not click Pay / Place Order / Submit Payment unless the user explicitly requests it.

## Merchant Notes

- Read `references/hoka.md` for Hoka-specific login and checkout guidance.
- If the product URL already encodes color or variant params, treat them as preselected but verify visually.
- If the site says a size is unavailable, stop and ask the user for an alternative.
- For Hoka, this flow should be reusable for any supported Hoka product URL, not just a single product.
- For Hoka, use the same reusable checkout profile and login flow across future purchases unless the user asks to override them.

## Files

- `references/hoka.md` — Hoka-specific checkout notes
- `references/checkout-profile.template.json` — template for collecting a reusable shipping/contact profile
- `scripts/select_best_coupon.py` — pick likely codes from deal-digest output

## Output to User

Return:
- merchant
- items added
- selected sizes/colors/quantities
- applied reward/coupon result
- current checkout stage
- screenshot path or attachment before payment

## Safety / Limits

- Never expose stored passwords in chat.
- Never submit payment without explicit confirmation.
- Never commit private checkout-profile data.
- Pause for CAPTCHA / MFA / unusual verification.
- Prefer one calm headed session over repeated retries.
