#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def parse_args():
    p = argparse.ArgumentParser(description='Select likely coupon candidates for a merchant from deals-active.json')
    p.add_argument('deals_file', help='Path to deals-active.json')
    p.add_argument('--merchant', required=True, help='Merchant/domain/brand to match, e.g. hoka')
    p.add_argument('--limit', type=int, default=3, help='Max candidates to emit')
    return p.parse_args()


def normalize(text):
    return (text or '').strip().lower()


def parse_expiration(value):
    if not value:
        return None
    for fmt in ('%Y-%m-%d', '%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%dT%H:%M:%S', '%m/%d/%Y'):
        try:
            dt = datetime.strptime(value, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            pass
    return None


def main():
    args = parse_args()
    merchant = normalize(args.merchant)
    deals = json.loads(Path(args.deals_file).read_text())
    now = datetime.now(timezone.utc)
    ranked = []

    for deal in deals:
        brand = normalize(deal.get('brand'))
        sender = normalize(deal.get('sender'))
        title = normalize(deal.get('title') or deal.get('subject'))
        code = (deal.get('promo_code') or deal.get('code') or '').strip()
        if not code:
            continue
        haystack = ' '.join([brand, sender, title])
        if merchant not in haystack:
            continue

        exp = parse_expiration(deal.get('expires_at') or deal.get('expiration') or deal.get('expires'))
        if exp and exp < now:
            continue

        discount = 0
        raw_discount = str(deal.get('discount') or '')
        digits = ''.join(ch for ch in raw_discount if ch.isdigit())
        if digits:
            discount = int(digits)

        urgency = 0
        if exp:
            hours = (exp - now).total_seconds() / 3600
            urgency = 1000 - max(hours, 0)

        score = discount * 10 + urgency
        ranked.append({
            'score': score,
            'code': code,
            'brand': deal.get('brand'),
            'discount': deal.get('discount'),
            'expires': deal.get('expires_at') or deal.get('expiration') or deal.get('expires'),
            'source': deal.get('title') or deal.get('subject') or deal.get('sender')
        })

    ranked.sort(key=lambda x: x['score'], reverse=True)
    print(json.dumps(ranked[:args.limit], indent=2))


if __name__ == '__main__':
    main()
