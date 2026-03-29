#!/usr/bin/env python3
"""Update user shopping preferences from orders or manual input.

Usage:
  # From order data (pipe from ingest_emails.py)
  python3 update_preferences.py <prefs_file> --order '<order_json>'

  # Manual tuning
  python3 update_preferences.py <prefs_file> --boost "brand:nike" --weight 8
  python3 update_preferences.py <prefs_file> --suppress "category:apparel"
  python3 update_preferences.py <prefs_file> --unsuppress "category:apparel"
  python3 update_preferences.py <prefs_file> --show
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

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
    """Guess product categories from text."""
    text_lower = text.lower()
    found = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(cat)
    return found if found else ["general"]


def load_prefs(path: str) -> dict:
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {
        "brands": {},
        "categories": {},
        "price_range": {"min": None, "max": None},
        "suppressed": [],
        "purchase_history": [],
        "manual_boosts": [],
        "updated_at": None,
    }


def save_prefs(path: str, prefs: dict):
    prefs["updated_at"] = datetime.now(timezone.utc).isoformat()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w") as f:
        json.dump(prefs, f, indent=2)


def update_from_order(prefs: dict, order: dict):
    """Update preferences from an order confirmation."""
    brand = order.get("brand", "").lower()
    if brand:
        prefs["brands"][brand] = prefs["brands"].get(brand, 0) + 3

    # Guess categories from subject + body
    text = f"{order.get('subject', '')} {order.get('raw_body_preview', '')}"
    categories = guess_categories(text)
    for cat in categories:
        prefs["categories"][cat] = prefs["categories"].get(cat, 0) + 2

    # Update price range
    total = order.get("total")
    if total:
        try:
            price = float(total)
            if prefs["price_range"]["min"] is None or price < prefs["price_range"]["min"]:
                prefs["price_range"]["min"] = price
            if prefs["price_range"]["max"] is None or price > prefs["price_range"]["max"]:
                prefs["price_range"]["max"] = price
        except (ValueError, TypeError):
            pass

    # Add to history (keep last 50)
    prefs["purchase_history"].append({
        "date": order.get("date", datetime.now(timezone.utc).isoformat()),
        "brand": brand,
        "subject": order.get("subject", ""),
        "order_number": order.get("order_number"),
    })
    prefs["purchase_history"] = prefs["purchase_history"][-50:]


def boost_preference(prefs: dict, type_value: str, weight: int):
    """Manually boost a preference. type_value format: 'brand:nike' or 'category:running-shoes'"""
    ptype, value = type_value.split(":", 1)
    value = value.lower()

    if ptype == "brand":
        prefs["brands"][value] = prefs["brands"].get(value, 0) + weight
    elif ptype == "category":
        prefs["categories"][value] = prefs["categories"].get(value, 0) + weight

    prefs["manual_boosts"].append({
        "type": ptype, "value": value, "weight": weight,
        "date": datetime.now(timezone.utc).isoformat()
    })
    print(f"✅ Boosted {ptype}:{value} by {weight}")


def suppress_preference(prefs: dict, type_value: str):
    """Suppress a type:value from appearing in digests."""
    if type_value not in prefs["suppressed"]:
        prefs["suppressed"].append(type_value)
        print(f"🚫 Suppressed: {type_value}")
    else:
        print(f"Already suppressed: {type_value}")


def unsuppress_preference(prefs: dict, type_value: str):
    """Remove suppression."""
    if type_value in prefs["suppressed"]:
        prefs["suppressed"].remove(type_value)
        print(f"✅ Unsuppressed: {type_value}")
    else:
        print(f"Not suppressed: {type_value}")


def show_preferences(prefs: dict):
    """Display current preferences."""
    print("=== Shopping Preferences ===\n")

    print("📊 Brand Scores:")
    for brand, score in sorted(prefs["brands"].items(), key=lambda x: -x[1]):
        print(f"  {brand}: {score}")

    print("\n📂 Category Scores:")
    for cat, score in sorted(prefs["categories"].items(), key=lambda x: -x[1]):
        print(f"  {cat}: {score}")

    print(f"\n💰 Price Range: ${prefs['price_range']['min'] or '?'} – ${prefs['price_range']['max'] or '?'}")

    if prefs["suppressed"]:
        print(f"\n🚫 Suppressed: {', '.join(prefs['suppressed'])}")

    print(f"\n🛒 Purchase History: {len(prefs['purchase_history'])} orders")
    for p in prefs["purchase_history"][-5:]:
        print(f"  [{p.get('date', '?')[:10]}] {p.get('brand', '?')}: {p.get('subject', '?')}")


def main():
    parser = argparse.ArgumentParser(description="Update shopping preferences")
    parser.add_argument("prefs_file", help="Path to user-preferences.json")
    parser.add_argument("--order", help="Order JSON string to learn from")
    parser.add_argument("--boost", help="Boost a preference (format: type:value)")
    parser.add_argument("--weight", type=int, default=5, help="Weight for boost (default: 5)")
    parser.add_argument("--suppress", help="Suppress a type:value")
    parser.add_argument("--unsuppress", help="Unsuppress a type:value")
    parser.add_argument("--show", action="store_true", help="Show current preferences")
    args = parser.parse_args()

    prefs = load_prefs(args.prefs_file)

    if args.show:
        show_preferences(prefs)
        return

    if args.order:
        order = json.loads(args.order)
        update_from_order(prefs, order)
        print(f"✅ Updated preferences from order: {order.get('brand', 'unknown')}")

    if args.boost:
        boost_preference(prefs, args.boost, args.weight)

    if args.suppress:
        suppress_preference(prefs, args.suppress)

    if args.unsuppress:
        unsuppress_preference(prefs, args.unsuppress)

    save_prefs(args.prefs_file, prefs)


if __name__ == "__main__":
    main()
