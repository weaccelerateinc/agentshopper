# AgentShopper 🛍️

AI-powered shopping automation skills for [OpenClaw](https://github.com/openclaw/openclaw). Create burner ecommerce accounts automatically and get personalized daily deal digests — powered by [agentmail.to](https://agentmail.to) for disposable email, headed browser automation for signups, and smart preference learning from your purchase history.

---

## Table of Contents

- [Overview](#overview)
- [How It Works](#how-it-works)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Onboarding & Setup](#onboarding--setup)
- [Skills](#skills)
  - [account-creator](#-account-creator)
  - [deal-digest](#-deal-digest)
- [Usage Examples](#usage-examples)
- [Adding New Merchants](#adding-new-merchants)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

AgentShopper is a pair of [OpenClaw](https://github.com/openclaw/openclaw) skills that automate two tedious parts of online shopping:

1. **Creating accounts** — No more filling out signup forms. Tell your agent "create an account on hoka.com" and it handles the rest: form filling, email verification, password generation, and credential storage.

2. **Tracking deals** — Promotional emails pile up and go unread. AgentShopper reads them for you, learns what you actually buy, and delivers a daily ranked summary of the deals most relevant to you.

Both skills use [agentmail.to](https://agentmail.to) as a programmable email inbox — your agent gets its own email address that it can read and act on autonomously.

## How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                        AgentShopper                          │
│                                                              │
│  ┌─────────────────┐         ┌─────────────────────────┐     │
│  │ account-creator  │         │     deal-digest          │     │
│  │                  │         │                          │     │
│  │  1. Open browser │         │  1. Poll inbox (6h)      │     │
│  │  2. Fill signup  │────────▶│  2. Classify emails      │     │
│  │  3. Verify email │  promo  │  3. Parse deals          │     │
│  │  4. Save creds   │ emails  │  4. Learn preferences    │     │
│  └─────────────────┘  flow   │  5. Score & rank         │     │
│          │              in    │  6. Daily digest → Slack  │     │
│          ▼                    └─────────────────────────┘     │
│  ┌─────────────┐                       │                     │
│  │ Apple        │                       ▼                     │
│  │ Passwords    │              ┌─────────────────┐           │
│  │ (Keychain)   │              │  Slack Channel   │           │
│  └─────────────┘              └─────────────────┘           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              agentmail.to inbox                        │   │
│  │  (receives signup verifications + promotional emails)  │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

**The flow:**

1. You ask your OpenClaw agent to create an account on a supported site
2. `account-creator` opens a real browser, fills the signup form with your profile + agentmail.to email, generates a strong password, and submits
3. If the site sends a verification email, the agent reads it from agentmail.to and clicks the link
4. Credentials are saved to Apple Passwords (macOS Keychain)
5. Over time, the site sends promotional emails to your agentmail.to address
6. `deal-digest` polls the inbox every 6 hours, classifies emails, and extracts deals
7. Order confirmation emails teach the system what you actually buy
8. Every morning at 9 AM, you get a personalized deal summary in Slack — ranked by what matters to you

---

## Prerequisites

Before installing AgentShopper, make sure you have:

### Required

| Dependency | Why | How to get it |
|---|---|---|
| **OpenClaw** | Agent runtime | [github.com/openclaw/openclaw](https://github.com/openclaw/openclaw) |
| **agentmail.to account** | Programmable email inbox | Sign up at [console.agentmail.to](https://console.agentmail.to) |
| **agentmail.to API key** | Authenticate inbox API calls | Create in agentmail.to console → API Keys |
| **agentmail.to email address** | The inbox your agent uses | Create an inbox in agentmail.to console |
| **Python 3.10+** | Runs the processing scripts | `brew install python` or system Python |
| **agentmail Python SDK** | API client for inbox access | `pip install agentmail` |
| **macOS** | Keychain credential storage | Required for `security` CLI |

### Required for deal-digest

| Dependency | Why | How to get it |
|---|---|---|
| **Slack channel** | Where daily digests are delivered | Configure Slack in OpenClaw |

### Optional but recommended

| Dependency | Why | How to get it |
|---|---|---|
| **Headed browser** | Visual browser for signup automation | Set `browser.headless: false` in OpenClaw config |

> **Note:** The headed browser lets you see what the agent is doing and manually solve CAPTCHAs when they appear. Headless mode may work for some sites but will fail on sites with anti-bot detection.

---

## Installation

### Option 1: ClawHub (recommended)

```bash
clawhub install account-creator
clawhub install deal-digest
```

### Option 2: GitHub (manual)

```bash
# Clone the repo
git clone https://github.com/weaccelerateinc/agentshopper.git
cd agentshopper

# Copy skills to your OpenClaw workspace
cp -r account-creator ~/.openclaw/workspace/skills/
cp -r deal-digest ~/.openclaw/workspace/skills/

# Install Python dependency
pip install agentmail
```

### Verify installation

After installing, your OpenClaw workspace should look like:

```
~/.openclaw/workspace/skills/
├── account-creator/
│   ├── SKILL.md
│   ├── references/
│   │   ├── config.example.md
│   │   └── hoka.md
│   └── scripts/
│       ├── check_inbox.py
│       ├── generate_password.py
│       └── save_to_keychain.sh
└── deal-digest/
    ├── SKILL.md
    ├── references/
    │   ├── config.example.json
    │   └── user-preferences.example.json
    └── scripts/
        ├── format_digest.py
        ├── ingest_emails.py
        ├── score_deals.py
        └── update_preferences.py
```

---

## Onboarding & Setup

### Step 1: Get your agentmail.to credentials

1. Go to [console.agentmail.to](https://console.agentmail.to) and create an account
2. Create an **API key** — copy it, you'll need it shortly
3. Create an **inbox** — this gives you an email address like `yourname@agentmail.to`

### Step 2: Configure account-creator

The easiest way: just ask your agent to create an account somewhere. On first use, it will prompt you for:

- **agentmail.to API key** — paste the key from step 1
- **agentmail.to email address** — the inbox address from step 1
- **First name** and **Last name** — used for signup forms

The agent saves this to `account-creator/references/config.md`. You can also create this file manually:

```markdown
# Account Creator Configuration

## AgentMail
- **API Key:** am_your_api_key_here
- **Email:** yourname@agentmail.to

## Profile
- **First Name:** Jane
- **Last Name:** Doe
- **Password:** (auto-generated per signup)

## Credential Storage
- **Method:** Apple Passwords (macOS Keychain)
```

### Step 3: Configure deal-digest

Copy the example config and fill in your details:

```bash
cd ~/.openclaw/workspace/skills/deal-digest/references/
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "agentmail_api_key": "am_your_api_key_here",
  "inbox_email": "yourname@agentmail.to",
  "digest_frequency": "daily",
  "digest_time": "09:00",
  "digest_channel": "slack",
  "timezone": "America/Los_Angeles"
}
```

**Configuration options:**

| Field | Description | Default |
|---|---|---|
| `agentmail_api_key` | Your agentmail.to API key | (required) |
| `inbox_email` | Your agentmail.to inbox address | (required) |
| `digest_frequency` | `"daily"` or `"weekly"` | `"daily"` |
| `digest_time` | Time to send digest (24h format) | `"09:00"` |
| `digest_channel` | Delivery channel: `"slack"`, `"telegram"`, etc. | `"slack"` |
| `timezone` | Your timezone (IANA format) | `"America/Los_Angeles"` |

### Step 4: Initialize preference tracking

Copy the example files to create your initial (empty) state:

```bash
cd ~/.openclaw/workspace/skills/deal-digest/references/
cp user-preferences.example.json user-preferences.json
echo '[]' > deals-active.json
echo '{"last_seen_ids": [], "last_poll": null}' > ingest-state.json
```

### Step 5: Set up cron jobs

Ask your OpenClaw agent to set up the cron jobs, or create them manually:

**Email ingestion (every 6 hours):**
```
Schedule: 0 */6 * * * (America/Los_Angeles)
Task: Run deal-digest email ingestion — poll inbox, classify, parse deals
```

**Daily digest (every day at 9 AM):**
```
Schedule: 0 9 * * * (America/Los_Angeles)  
Task: Score deals, format digest, send to Slack
```

Or just tell your agent: *"Set up the deal-digest cron jobs"* — it knows what to do.

### Step 6: Seed your preferences (optional)

If you already know what you like, you can seed preferences before any orders come in:

```
"I like running shoes"
"I like Nike and HOKA"
"Ignore apparel deals"
```

The agent will update your preference profile accordingly.

---

## Skills

### 🔑 account-creator

Automates ecommerce account signup using a headed browser, agentmail.to for email, and Apple Passwords for credential storage.

#### What it does

1. Opens a **real browser** (headed, visible to you)
2. Navigates to the merchant's signup page
3. Fills in your profile details (name, email, password)
4. Generates a **strong random password** (16 chars, uppercase + lowercase + digits + special)
5. Opts into **promotions and newsletters** (always on)
6. Submits the form
7. If a verification email is sent, **polls agentmail.to inbox** and clicks the verification link
8. Saves credentials to **Apple Passwords** (macOS Keychain)
9. Reports success with a confirmation screenshot

#### CAPTCHA handling

Some sites (like hoka.com) have aggressive anti-bot detection. When a CAPTCHA appears, the agent:
- Detects it and **pauses**
- Asks you to **solve it manually** in the browser window
- Continues automatically once you've passed it

#### Supported merchants

| Merchant | Signup URL | Verification | Notes |
|---|---|---|---|
| **hoka.com** | `/en/us/login/` → "Join Us" tab | None (instant) | CAPTCHA on first visit, membership program |

More merchants can be added by creating reference files (see [Adding New Merchants](#adding-new-merchants)).

#### Password generation

Passwords are generated using Python's `secrets` module (cryptographically secure):
- 16 characters by default
- At least 1 uppercase, 1 lowercase, 1 digit, 1 special character (`!@#$%&*`)
- Characters are shuffled randomly

---

### 📬 deal-digest

Monitors your agentmail.to inbox for promotional emails, learns what you buy, and delivers a personalized daily deal summary.

#### Email classification

Every email is classified into one of three categories:

| Category | Detection | What happens |
|---|---|---|
| **Promo** | Contains 2+ promo keywords (% off, sale, coupon, deal, etc.) | Parsed into active deals |
| **Order** | Contains 2+ order keywords (order confirmation, shipped, tracking, etc.) | Fed to preference learner |
| **Other** | Neither promo nor order, or from ignored senders | Skipped |

#### Deal parsing

From each promotional email, the system extracts:
- **Brand** — inferred from sender domain
- **Discount** — percentage off (regex: `\d+% off`)
- **Promo code** — any code following "code:", "coupon:", "promo:" (regex)
- **Expiration date** — dates following "expires", "ends", "valid through"
- **Links** — first non-unsubscribe URL for the "shop now" link

#### Preference learning

Preferences are built from two sources:

**Automatic (from orders):**
- Each order confirmation email updates brand scores (+3) and category scores (+2)
- Price range tracks min/max of purchases
- Purchase history maintained (last 50 orders)

**Manual tuning:**
- Boost: `"I like Nike"` → brand:nike score increases
- Suppress: `"Ignore apparel"` → apparel category filtered from digests
- Unsuppress: `"Show me apparel again"` → removes the filter

#### Deal scoring algorithm

Each deal gets a relevance score based on:

| Factor | Weight | Description |
|---|---|---|
| Brand match | ×3 | Score from preference profile for this brand |
| Category match | ×2 | Score for matched product categories |
| Discount depth | ×0.5 per % | 50% off = +25 points, 10% off = +5 points |
| Base score | +1 | Ensures new/unknown deals still appear |

Deals are sorted highest score first. Suppressed categories/brands are filtered out entirely.

#### Digest format

Delivered daily to your configured channel:

```
🛍️ Deal Digest — March 28

🔥 Top Picks for You:
• HOKA: 15% off Clifton styles (code: MEMBER15) — expires Apr 2
  https://www.hoka.com/en/us/sale/
• Nike: 30% off running shoes — ends this weekend
  https://www.nike.com/sale

📬 Other Deals:
• Allbirds: Free shipping on orders over $100
  https://www.allbirds.com

🧠 Based on: HOKA, Nike, Running Shoes preferences

📊 3 active deals tracked
```

Top 5 deals shown as "Top Picks", remaining as "Other Deals" (capped at 10). Deals older than 30 days are automatically pruned.

---

## Usage Examples

### Creating accounts

```
> "Create an account on hoka.com"
> "Sign me up on nike.com"
> "Register a burner account on allbirds.com"
```

### Managing deals

```
> "What deals do I have?"
> "Show me today's deals"
> "Run the deal digest now"
```

### Tuning preferences

```
> "I like running shoes"
> "Boost Nike brand preference"
> "Ignore underwear deals"
> "Stop suppressing apparel"
> "Show my shopping preferences"
```

### Checking status

```
> "When does the next digest run?"
> "How many active deals are tracked?"
```

---

## Adding New Merchants

To add support for a new ecommerce site, create a reference file at:

```
account-creator/references/<domain>.md
```

Use this template (based on the hoka.md example):

```markdown
# <Site Name> Account Creation Flow

## URL
- Account page: https://www.<domain>/signup

## Signup Form Fields
Navigate to the URL. The form has:
- First Name
- Last Name
- Email Address
- Password
- (list any other fields)
- (note any checkboxes — promotions, terms, etc.)
- Submit button label

## Flow
1. Navigate to signup URL
2. (Note any cookie banners or popups to dismiss)
3. Fill in form fields
4. Check promotional opt-in boxes
5. Click submit button
6. (Does it need email verification? Yes/No)
7. (If yes: what does the verification email look like?)
8. Save credentials

## Common Issues
- (CAPTCHA? What kind?)
- (Password requirements: length, character types)
- (Any anti-bot detection?)
- (Email verification timing?)
```

**Tips:**
- Test the signup flow manually first to understand the form structure
- Note exact button labels and field names — the agent uses these to find elements
- Document any CAPTCHAs or bot detection you encounter
- Note whether email verification is required or if accounts activate immediately

---

## Architecture

### File structure

```
account-creator/
├── SKILL.md                          # Agent instructions
├── references/
│   ├── config.md                     # Your agentmail + profile config (gitignored)
│   ├── config.example.md             # Template for new users
│   └── hoka.md                       # Hoka.com signup flow docs
└── scripts/
    ├── generate_password.py          # Cryptographic password generator
    ├── check_inbox.py                # Poll agentmail.to for verification emails
    └── save_to_keychain.sh           # Save credentials to macOS Keychain

deal-digest/
├── SKILL.md                          # Agent instructions
├── references/
│   ├── config.json                   # Your config (gitignored)
│   ├── config.example.json           # Template for new users
│   ├── user-preferences.json         # Learned + manual preferences (gitignored)
│   ├── user-preferences.example.json # Empty template
│   ├── deals-active.json             # Current active deals (gitignored)
│   └── ingest-state.json             # Poll state tracking (gitignored)
└── scripts/
    ├── ingest_emails.py              # Poll inbox → classify → parse
    ├── update_preferences.py         # Learn from orders + manual tuning
    ├── score_deals.py                # Rank deals by user relevance
    └── format_digest.py              # Generate Slack-formatted summary
```

### Data flow

```
agentmail.to inbox
    │
    ├── Promo emails ──→ ingest_emails.py ──→ deals-active.json
    │                                              │
    ├── Order emails ──→ ingest_emails.py ──→ update_preferences.py ──→ user-preferences.json
    │                                                                          │
    └── Manual input ("I like X") ──→ update_preferences.py ────────────────────┘
                                                                               │
                                                          score_deals.py ◄─────┘
                                                               │
                                                          format_digest.py
                                                               │
                                                          Slack / Telegram
```

### Cron schedule

| Job | Schedule | Script chain | Delivery |
|---|---|---|---|
| Email ingestion | `0 */6 * * *` | `ingest_emails.py` → `update_preferences.py` | Silent |
| Daily digest | `0 9 * * *` | `ingest_emails.py` → `score_deals.py` → `format_digest.py` | Slack |

---

## Troubleshooting

### account-creator

| Problem | Cause | Solution |
|---|---|---|
| CAPTCHA appears | Anti-bot detection | Solve manually in the browser, agent continues after |
| "Page not found" on signup URL | Site changed their URL | Update the merchant reference file with new URL |
| Verification email never arrives | Spam filter or delay | Increase `--wait` timeout (default 120s), check agentmail.to console |
| Keychain access denied | macOS permissions | Allow terminal access in System Settings → Privacy → Automation |
| Browser timeout | OpenClaw browser connection lost | Restart gateway: `openclaw gateway restart` |

### deal-digest

| Problem | Cause | Solution |
|---|---|---|
| No deals in digest | No promo emails received yet | Create more accounts, or forward existing promos to agentmail.to |
| Emails classified as "other" | Not enough keyword matches | Adjust `PROMO_KEYWORDS` in `ingest_emails.py` |
| Wrong brand detected | Brand parsed from sender domain | Deals from complex domains may need manual correction |
| Digest not sending | Cron job not set up | Ask agent to set up cron jobs, or create manually |
| Preferences not updating | No order emails detected | `ORDER_KEYWORDS` threshold is 2 — ensure confirmation emails have standard language |

### General

| Problem | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: agentmail` | SDK not installed | `pip install agentmail` |
| agentmail API errors | Invalid/expired API key | Check key at [console.agentmail.to](https://console.agentmail.to) |
| Agent doesn't trigger skill | Description mismatch | Use trigger phrases: "create account", "deals", "digest" |

---

## Contributing

### Adding merchants

The easiest way to contribute is adding support for new ecommerce sites:

1. Fork the repo
2. Create `account-creator/references/<domain>.md` following the template above
3. Test the signup flow with the agent
4. Submit a PR with the reference file

### Improving deal parsing

The email classification and deal extraction logic is in `deal-digest/scripts/ingest_emails.py`. PRs welcome for:

- Better promo keyword detection
- Smarter brand extraction from sender addresses
- Improved discount/coupon code parsing
- Expiration date normalization

### General guidelines

- Keep scripts self-contained (no external dependencies beyond `agentmail`)
- Test scripts standalone before submitting
- Don't commit personal config files (they're gitignored)
- Update SKILL.md if you change the workflow

---

## License

MIT — see [LICENSE](LICENSE) for details.
