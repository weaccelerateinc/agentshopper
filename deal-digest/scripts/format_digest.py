#!/usr/bin/env python3
"""Format scored deals into a readable digest message.

Usage:
  python3 format_digest.py <deals_file> <prefs_file> [--top N] [--date YYYY-MM-DD]

Output: Formatted digest text to stdout.
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone


def format_deal_line(deal: dict) -> str:
    """Format a single deal as a bullet point."""
    brand = deal.get("brand", "Unknown").title()
    subject = deal.get("subject", "")
    discount = deal.get("discount", "")
    code = deal.get("code")
    expiration = deal.get("expiration")
    link = deal.get("link")

    parts = [f"*{brand}*: "]

    if discount:
        parts.append(f"{discount}")
        if subject and discount.lower() not in subject.lower():
            parts.append(f" — {subject}")
    else:
        parts.append(subject)

    if code:
        parts.append(f" (code: `{code}`)")

    if expiration:
        parts.append(f" — expires {expiration}")

    if link:
        parts.append(f"\n  <{link}>")

    return "• " + "".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Format deal digest")
    parser.add_argument("deals_file", help="Path to deals-active.json")
    parser.add_argument("prefs_file", help="Path to user-preferences.json")
    parser.add_argument("--top", type=int, default=5, help="Number of top picks")
    parser.add_argument("--date", default=None, help="Date for header (default: today)")
    args = parser.parse_args()

    # Load scored deals
    if not os.path.exists(args.deals_file):
        print("No active deals found.")
        return

    with open(args.deals_file) as f:
        deals = json.load(f)

    if not deals:
        print("📭 No active deals right now. Check back tomorrow!")
        return

    # Sort by relevance score if present
    deals.sort(key=lambda d: -d.get("relevance_score", 0))

    # Load prefs for context
    prefs = {}
    if os.path.exists(args.prefs_file):
        with open(args.prefs_file) as f:
            prefs = json.load(f)

    # Header
    date_str = args.date or datetime.now(timezone.utc).strftime("%B %-d")
    lines = [f"🛍️ *Deal Digest — {date_str}*\n"]

    # Top picks
    top = deals[:args.top]
    rest = deals[args.top:]

    if top:
        lines.append("🔥 *Top Picks for You:*")
        for deal in top:
            lines.append(format_deal_line(deal))
        lines.append("")

    # Other deals
    if rest:
        lines.append("📬 *Other Deals:*")
        for deal in rest[:10]:  # cap at 10 others
            lines.append(format_deal_line(deal))
        if len(rest) > 10:
            lines.append(f"  _...and {len(rest) - 10} more_")
        lines.append("")

    # Preference context
    top_brands = sorted(prefs.get("brands", {}).items(), key=lambda x: -x[1])[:3]
    top_cats = sorted(prefs.get("categories", {}).items(), key=lambda x: -x[1])[:3]
    context_parts = [b[0].title() for b in top_brands] + [c[0].replace("-", " ").title() for c in top_cats]
    if context_parts:
        lines.append(f"🧠 _Based on: {', '.join(context_parts)} preferences_")

    total = len(deals)
    lines.append(f"\n📊 {total} active deal{'s' if total != 1 else ''} tracked")

    print("\n".join(lines))


if __name__ == "__main__":
    main()
