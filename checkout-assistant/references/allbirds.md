# Allbirds Checkout Flow

## Purpose
Use this note when logging into an existing Allbirds account, building a cart with one or more products, applying the best available discount, and stopping at payment.

## Platform
- Shopify Plus — standard Shopify checkout flow

## URLs
- Product pages: `https://www.allbirds.com/products/<slug>`
- Cart: `https://www.allbirds.com/cart`
- Checkout: Shopify-hosted checkout at `https://www.allbirds.com/.../checkouts/...`

## Browser Mode
Use a headed browser. Shopify bot detection (hCaptcha) is less aggressive in visible sessions.

## Product Variant Behavior
- Color: selected via swatch buttons on the product page (circular color tiles)
- Size: selected via size buttons (numeric grid, e.g., "8", "9", "10")
- "Add to Cart" button becomes active only after size is selected
- Some products show "Notify Me" instead of "Add to Cart" if out of stock — skip those
- For multi-item carts, repeat the product-page selection and add-to-cart for each item before proceeding to checkout

## Common UI Issues
- **Shipping country modal**: A "Where are we shipping to?" modal appears on first visit with a country dropdown and "CONFIRM" button — select "United States" and click CONFIRM before interacting with the product page
- **Cookie consent banner**: May overlay the page on first visit — dismiss it
- **Marketing pop-up**: Email capture modal may appear — close it via the X button
- **Express checkout buttons**: Shop Pay, Apple Pay, PayPal buttons appear above the standard checkout — use the standard "Checkout" button instead
- **Shopify checkout is multi-step**: Information → Shipping → Payment — each is a separate page
- **Guest checkout**: Available — Shopify allows checkout without an account, but logging in is preferred for saved addresses

## Login Guidance
- Prefer existing saved session if already logged in
- Otherwise use the Allbirds account created by account-creator
- Login at https://www.allbirds.com/account/login — this redirects to `accounts.allbirds.com` (Shopify New Customer Accounts, passwordless)
- Authentication is via email + 6-digit verification code (no password) — check agentmail inbox for the code
- After login, navigate back to the cart if items were added before login

## Coupon / Reward Strategy
- Check structured deals from deal-digest for allbirds.com codes first
- Shopify discount code field appears on the checkout Information or Payment step
- Enter code in "Discount code" field and click "Apply"
- Try one code at a time; keep the one with the best discount
- Allbirds occasionally offers sitewide sales (no code needed) — check if discount is already applied
- Some promo codes are single-use — if rejected, move to the next candidate

## Reusable Checkout Profile
Use a local `references/checkout-profile.json` file for shipping/contact fields during checkout. Do not commit that file. If it is missing, create it from `references/checkout-profile.template.json`.

## Stop Condition
Stop when the Shopify checkout reaches the **Payment** step and the credit card form is visible. Capture a screenshot at that point and report back.
