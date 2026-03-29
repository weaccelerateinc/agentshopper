---
name: deal-digest
description: Monitor promotional emails from agentmail.to inbox, learn user purchase preferences from order confirmations, and deliver daily personalized deal summaries to Slack. Also supports manual preference tuning. Use when asked about deals, promotions, coupons, discounts, sale alerts, deal summary, deal digest, shopping preferences, or "what deals do I have". Triggers on "deals", "promotions", "coupons", "digest", "sale alerts", "shopping preferences", "tune my preferences", "what's on sale".
---

# Deal Digest

Monitor promo emails, learn shopping preferences, deliver daily personalized deal summaries.

## Setup

Requires agentmail.to config from the `account-creator` skill. Read `../account-creator/references/config.md` for API key and email.

Config file: `references/config.json`
```json
{
  "agentmail_api_key": "<from account-creator>",
  "inbox_email": "garysmod@agentmail.to",
  "digest_frequency": "daily",
  "digest_time": "09:00",
  "digest_channel": "slack",
  "timezone": "America/Los_Angeles"
}
```

If `references/config.json` doesn't exist or is incomplete, read the agentmail config from `../account-creator/references/config.md` and create it.

## Core Workflows

### 1. Email Ingestion (Scheduled)

Run every 6 hours via cron or heartbeat:

```bash
python3 scripts/ingest_emails.py <api_key> <inbox_email> --state references/ingest-state.json
```

This script:
- Polls inbox for new messages since last check
- Classifies each email as **promo**, **order**, or **other**
- Promo emails → parsed into `references/deals-active.json`
- Order emails → fed to preference updater
- Updates `references/ingest-state.json` with last-seen message ID

### 2. Preference Learning (Automatic)

When order confirmation emails are detected during ingestion:

```bash
python3 scripts/update_preferences.py references/user-preferences.json --order '<order_json>'
```

Extracts: brand, product category, price, item details. Updates weighted preference scores in `references/user-preferences.json`.

### 3. Manual Preference Tuning

When user says things like "I like running shoes", "ignore apparel", "I prefer Nike":

```bash
python3 scripts/update_preferences.py references/user-preferences.json --boost "category:running-shoes" --weight 10
python3 scripts/update_preferences.py references/user-preferences.json --suppress "category:apparel"
python3 scripts/update_preferences.py references/user-preferences.json --boost "brand:nike" --weight 8
```

Supported commands:
- `--boost "type:value"` with `--weight N` — increase preference score
- `--suppress "type:value"` — add to suppressed list (will be filtered out)
- `--unsuppress "type:value"` — remove from suppressed list
- `--show` — display current preferences

### 4. Deal Scoring

```bash
python3 scripts/score_deals.py references/deals-active.json references/user-preferences.json
```

Scores each active deal by:
- Brand match (×3 weight)
- Category match (×2 weight)
- Price alignment (×1 weight)
- Discount depth (×1 weight)
- Expiration urgency — within 48h gets 1.5× bump

Output: ranked JSON list of deals with relevance scores.

### 5. Daily Digest Delivery

```bash
python3 scripts/format_digest.py references/deals-active.json references/user-preferences.json
```

Generates a formatted summary. Send via Slack using the `message` tool:
- Top 5 most relevant deals as "🔥 Top Picks"
- Remaining deals as "📬 Other Deals"
- Include discount codes, expiration dates, direct links
- Note what preferences drove the ranking

### Digest Format
```
🛍️ Deal Digest — March 28

🔥 Top Picks for You:
• HOKA: 15% off Clifton styles (code: MEMBER15) — expires Apr 2
• Nike: 30% off running shoes — ends this weekend

📬 Other Deals:
• Allbirds: Free shipping $100+
• Victoria's Secret: BOGO 50% off

🧠 Based on: running shoes, HOKA, Nike preferences
```

## Cron Setup

Set up two cron jobs:

1. **Email ingestion** — every 6 hours:
   - `schedule: { kind: "cron", expr: "0 */6 * * *", tz: "America/Los_Angeles" }`
   - Task: run `ingest_emails.py`, then `update_preferences.py` for any orders found

2. **Daily digest** — every day at 9 AM:
   - `schedule: { kind: "cron", expr: "0 9 * * *", tz: "America/Los_Angeles" }`
   - Task: run `score_deals.py`, then `format_digest.py`, send result to Slack

## File Reference

- `references/config.json` — skill configuration
- `references/deals-active.json` — currently active deals (auto-managed, expire old ones)
- `references/user-preferences.json` — learned + manually tuned preferences
- `references/ingest-state.json` — last poll timestamp/message ID

## Expiration

Deals older than 30 days or past their expiration date are automatically pruned during ingestion.
