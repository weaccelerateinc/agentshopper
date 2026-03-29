#!/usr/bin/env python3
"""Poll agentmail.to inbox, classify emails as promo/order/other, and store results.

Usage:
  python3 ingest_emails.py <api_key> <inbox_email> --state <state_file>
    [--deals <deals_file>] [--prefs <prefs_file>]

Outputs:
  - Updates deals-active.json with new promo deals
  - Prints order JSON to stdout for preference updating
  - Updates state file with last-seen message ID
"""

import argparse
import json
import re
import sys
import os
from datetime import datetime, timedelta, timezone

from agentmail import AgentMail

PROMO_KEYWORDS = [
    "% off", "sale", "discount", "coupon", "promo", "deal", "clearance",
    "save", "offer", "limited time", "flash sale", "bogo", "free shipping",
    "exclusive", "member", "reward", "earn", "points", "code:", "use code",
    "shop now", "don't miss", "last chance", "ending soon", "expires",
    "markdown", "price drop", "special"
]

ORDER_KEYWORDS = [
    "order confirmation", "order #", "order number", "your order",
    "shipping confirmation", "has shipped", "tracking number",
    "receipt", "invoice", "purchase confirmation", "thank you for your order",
    "delivery", "estimated delivery"
]

IGNORE_SENDERS = [
    "noreply@agentmail.to", "no-reply@1password.com", "no-reply@info.1password.com"
]


def classify_email(subject: str, body: str, sender: str) -> str:
    """Classify email as promo, order, or other."""
    sender_lower = sender.lower()
    if any(ignore in sender_lower for ignore in IGNORE_SENDERS):
        return "other"

    text = f"{subject} {body}".lower()

    order_score = sum(1 for kw in ORDER_KEYWORDS if kw in text)
    if order_score >= 2:
        return "order"

    promo_score = sum(1 for kw in PROMO_KEYWORDS if kw in text)
    if promo_score >= 2:
        return "promo"

    return "other"


def extract_deals(subject: str, body: str, sender: str, html: str) -> dict:
    """Extract deal details from a promotional email."""
    # Extract discount percentages
    percents = re.findall(r'(\d{1,2})%\s*off', body.lower())
    discount = f"{percents[0]}% off" if percents else None

    # Extract promo codes
    codes = re.findall(r'(?:code|coupon|promo)[:\s]+([A-Z0-9]{3,20})', body, re.IGNORECASE)
    code = codes[0] if codes else None

    # Extract expiration
    exp_patterns = [
        r'(?:expires?|ends?|valid (?:through|until|thru))[:\s]+(\w+ \d{1,2}(?:,? \d{4})?)',
        r'(?:expires?|ends?)[:\s]+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)',
    ]
    expiration = None
    for pat in exp_patterns:
        match = re.search(pat, body, re.IGNORECASE)
        if match:
            expiration = match.group(1)
            break

    # Extract links
    links = re.findall(r'https?://[^\s<>"\']+', html or body)
    shop_links = [l for l in links if "unsubscribe" not in l.lower()
                  and "privacy" not in l.lower()
                  and "mailto" not in l.lower()]

    # Guess brand from sender
    sender_parts = sender.split("@")
    brand = sender_parts[0].replace("noreply", "").replace("no-reply", "").replace("info", "").strip()
    if "@" in sender:
        domain = sender_parts[1].split(".")[0]
        brand = domain if len(domain) > 2 else brand

    return {
        "brand": brand,
        "subject": subject,
        "discount": discount,
        "code": code,
        "expiration": expiration,
        "link": shop_links[0] if shop_links else None,
        "summary": subject,
        "sender": sender,
        "ingested_at": datetime.now(timezone.utc).isoformat(),
    }


def extract_order(subject: str, body: str, sender: str) -> dict:
    """Extract order details from a confirmation email."""
    # Extract order number
    order_nums = re.findall(r'(?:order\s*(?:#|number|num)?[:\s]*)([A-Z0-9\-]{4,20})', body, re.IGNORECASE)

    # Extract prices
    prices = re.findall(r'\$(\d+(?:\.\d{2})?)', body)

    # Guess brand from sender domain
    brand = ""
    if "@" in sender:
        brand = sender.split("@")[1].split(".")[0]

    return {
        "type": "order",
        "brand": brand,
        "subject": subject,
        "order_number": order_nums[0] if order_nums else None,
        "prices": prices[:5],
        "total": prices[-1] if prices else None,
        "sender": sender,
        "date": datetime.now(timezone.utc).isoformat(),
        "raw_body_preview": body[:1000],
    }


def load_json(path: str, default=None):
    if default is None:
        default = {}
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return default


def save_json(path: str, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def prune_expired_deals(deals: list) -> list:
    """Remove deals older than 30 days."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    return [d for d in deals if d.get("ingested_at", "") > cutoff]


def main():
    parser = argparse.ArgumentParser(description="Ingest emails from agentmail.to")
    parser.add_argument("api_key", help="AgentMail API key")
    parser.add_argument("inbox_email", help="Inbox email address")
    parser.add_argument("--state", default="references/ingest-state.json", help="State file path")
    parser.add_argument("--deals", default="references/deals-active.json", help="Deals file path")
    args = parser.parse_args()

    client = AgentMail(api_key=args.api_key)
    state = load_json(args.state, {"last_seen_ids": []})
    deals = load_json(args.deals, [])
    seen_ids = set(state.get("last_seen_ids", []))

    # Fetch recent messages
    result = client.inboxes.messages.list(inbox_id=args.inbox_email, limit=50)

    new_promos = 0
    new_orders = 0
    orders_found = []

    for msg_item in result.messages:
        msg_id = msg_item.message_id
        if msg_id in seen_ids:
            continue

        seen_ids.add(msg_id)
        subject = msg_item.subject or ""
        sender = str(getattr(msg_item, "from_", ""))

        # Fetch full message to get body content
        try:
            msg = client.inboxes.messages.get(inbox_id=args.inbox_email, message_id=msg_id)
            body = msg.extracted_text or msg.text or ""
            html = msg.extracted_html or msg.html or ""
        except Exception as e:
            print(f"Failed to fetch message {msg_id}: {e}", file=sys.stderr)
            body = ""
            html = ""

        classification = classify_email(subject, body, sender)

        if classification == "promo":
            deal = extract_deals(subject, body, sender, html)
            deals.append(deal)
            new_promos += 1
            print(f"[PROMO] {deal['brand']}: {deal['subject']}", file=sys.stderr)

        elif classification == "order":
            order = extract_order(subject, body, sender)
            orders_found.append(order)
            new_orders += 1
            print(f"[ORDER] {order['brand']}: {order['subject']}", file=sys.stderr)

        else:
            print(f"[SKIP] {sender}: {subject}", file=sys.stderr)

    # Prune old deals
    deals = prune_expired_deals(deals)

    # Save state
    state["last_seen_ids"] = list(seen_ids)[-200:]  # keep last 200
    state["last_poll"] = datetime.now(timezone.utc).isoformat()
    save_json(args.state, state)
    save_json(args.deals, deals)

    # Output summary
    summary = {
        "new_promos": new_promos,
        "new_orders": new_orders,
        "total_active_deals": len(deals),
        "orders": orders_found,
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
