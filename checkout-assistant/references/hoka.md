# Hoka Checkout Flow

## Purpose

Use this note when logging into an existing Hoka account, building a reusable Hoka cart with one or more products, applying the best available reward or discount, and stopping at payment.

## URLs

- Product pages live under `https://www.hoka.com/en/us/...`
- Account / login entry point: `https://www.hoka.com/en/us/login/`
- Cart and checkout may also prompt inline login after add-to-bag

## Browser Mode

Use a headed browser. Prior work showed headless flows were more likely to get blocked by bot protection, while visible browser sessions worked better for legitimate supervised checkout.

## Product Variant Behavior

- Hoka product URLs may already contain a color param like `?dwvar_<sku>_color=LRMT`
- Color may already be preselected from the URL; verify before clicking another swatch
- Size may not be preselected even if a query param exists; verify selected state explicitly
- Add-to-Bag can remain disabled until a valid size is selected
- This flow should work for any Hoka product page with the same size/color/add-to-cart pattern, not just a single SKU
- For multi-item carts, repeat the product-page variant selection and add-to-cart flow for each item before checkout

## Common UI Issues

- Cookie banners or marketing popups may appear and cover buttons
- "Add to Bag" may exist in DOM but not be actionable until size is chosen
- Member pricing or welcome promos may appear after login
- Promo code field is usually visible in cart or order summary during checkout

## Login Guidance

- Prefer existing saved session if already logged in
- Otherwise use the existing Hoka account created by account-creator
- If login triggers CAPTCHA or anti-bot challenge, pause for manual solve

## Coupon / Reward Strategy

- Check structured deals from deal-digest for HOKA / hoka.com codes first
- Inspect Hoka membership rewards shown directly in checkout, including welcome boosts and member rewards
- Try one likely code or one merchant-native reward at a time
- Keep the best successful single option only
- If Hoka says only one reward or discount can be used, do not stack; compare totals and keep the better result

## Reusable Checkout Profile

Use a local `references/checkout-profile.json` file for shipping/contact fields during Hoka checkout. Do not commit that file. If it is missing, create it from `references/checkout-profile.template.json` and fill in the user’s profile before checkout.

## Stop Condition

Stop when the checkout page is asking for payment details or when the final review/payment step is visible. Capture a screenshot at that point and report back.
