#!/usr/bin/env python3
"""Score and rank active deals against user preferences.

Usage:
  python3 score_deals.py <deals_file> <prefs_file>

Output: JSON array of deals sorted by relevance score (highest first).
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone


CATEGORY_KEYWORDS = {
    "running-shoes": ["running", "run", "runner", "clifton", "bondi", "speedgoat", "mach",
                       "pegasus", "vaporfly", "ultraboost", "gel-kayano", "ghost"],
    "walking-shoes": ["walking", "walk", "transport", "gaviota"],
    "sandals": ["sandal", "slide", "flip flop", "ora"],
    "boots": ["boot", "hiking boot", "kaha"],
    "apparel": ["shirt", "tee", "shorts", "pants", "jacket", "hoodie", "legging",
                "sports bra", "tank", "vest"],
    "accessories": ["hat", "cap", "sock", "bag", "backpack", "sunglasses", "watch",
                    "headband", "gloves"],
    "underwear": ["underwear", "bra", "panty", "panties", "lingerie", "boxer", "brief"],
}


def guess_categories(text: str) -> list[str]:
    text_lower = text.lower()
    found = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(cat)
    return found if found else ["general"]


def is_suppressed(deal: dict, suppressed: list[str]) -> bool:
    """Check if deal matches any suppressed preferences."""
    brand = deal.get("brand", "").lower()
    categories = guess_categories(deal.get("subject", "") + " " + deal.get("summary", ""))

    for s in suppressed:
        stype, sval = s.split(":", 1)
        if stype == "brand" and sval.lower() == brand:
            return True
        if stype == "category" and sval in categories:
            return True
    return False


def score_deal(deal: dict, prefs: dict) -> float:
    """Score a deal based on user preferences."""
    score = 0.0
    brand = deal.get("brand", "").lower()
    text = f"{deal.get('subject', '')} {deal.get('summary', '')}"
    categories = guess_categories(text)

    # Brand match (×3 weight)
    brand_score = prefs.get("brands", {}).get(brand, 0)
    score += brand_score * 3

    # Category match (×2 weight)
    for cat in categories:
        cat_score = prefs.get("categories", {}).get(cat, 0)
        score += cat_score * 2

    # Discount depth (×1 weight)
    discount = deal.get("discount", "")
    if discount:
        import re
        nums = re.findall(r'(\d+)', discount)
        if nums:
            pct = int(nums[0])
            score += pct * 0.5  # 50% off = +25 points

    # Expiration urgency — within 48h gets 1.5× multiplier
    # (We'd need parsed dates for this, skip if not available)

    # Base score so new/unknown deals still appear
    score += 1.0

    return round(score, 2)


def main():
    parser = argparse.ArgumentParser(description="Score deals against preferences")
    parser.add_argument("deals_file", help="Path to deals-active.json")
    parser.add_argument("prefs_file", help="Path to user-preferences.json")
    args = parser.parse_args()

    if not os.path.exists(args.deals_file):
        print(json.dumps([]))
        return

    with open(args.deals_file) as f:
        deals = json.load(f)

    prefs = {}
    if os.path.exists(args.prefs_file):
        with open(args.prefs_file) as f:
            prefs = json.load(f)

    suppressed = prefs.get("suppressed", [])

    scored = []
    for deal in deals:
        if is_suppressed(deal, suppressed):
            continue
        deal["relevance_score"] = score_deal(deal, prefs)
        scored.append(deal)

    scored.sort(key=lambda d: -d["relevance_score"])
    print(json.dumps(scored, indent=2))


if __name__ == "__main__":
    main()
