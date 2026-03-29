#!/usr/bin/env python3
"""Poll agentmail.to inbox for new messages. Used to catch verification emails.

Usage:
  python3 check_inbox.py <api_key> <inbox_email> [--wait <seconds>] [--keyword <keyword>]

Options:
  --wait      Max seconds to poll (default: 120)
  --keyword   Filter messages containing this keyword in subject/body (default: verify,confirm,welcome)

Output: JSON with message details including links found in the body.
"""

import argparse
import json
import re
import sys
import time

from agentmail import AgentMail


def extract_links(text: str) -> list[str]:
    """Extract all URLs from text."""
    if not text:
        return []
    return re.findall(r'https?://[^\s<>"\']+', text)


def find_verification_link(links: list[str]) -> str | None:
    """Find the most likely verification/confirmation link."""
    keywords = ["verify", "confirm", "activate", "validate", "registration", "account"]
    for link in links:
        lower = link.lower()
        if any(kw in lower for kw in keywords):
            return link
    # If no keyword match, return the first non-unsubscribe link
    for link in links:
        if "unsubscribe" not in link.lower():
            return link
    return links[0] if links else None


def main():
    parser = argparse.ArgumentParser(description="Poll agentmail inbox for verification emails")
    parser.add_argument("api_key", help="AgentMail API key")
    parser.add_argument("inbox_email", help="Inbox email address (inbox_id)")
    parser.add_argument("--wait", type=int, default=120, help="Max seconds to poll")
    parser.add_argument("--keyword", default="verify,confirm,welcome,activate", help="Comma-separated keywords to filter")
    args = parser.parse_args()

    client = AgentMail(api_key=args.api_key)
    keywords = [k.strip().lower() for k in args.keyword.split(",")]
    start = time.time()
    seen_ids = set()

    # Get existing messages to skip them
    try:
        existing = client.inboxes.messages.list(inbox_id=args.inbox_email, limit=50)
        for msg in existing.messages:
            seen_ids.add(msg.message_id)
    except Exception:
        pass

    print(f"Polling inbox {args.inbox_email} for up to {args.wait}s...", file=sys.stderr)

    while time.time() - start < args.wait:
        try:
            result = client.inboxes.messages.list(inbox_id=args.inbox_email, limit=10)
            for msg in result.messages:
                if msg.message_id in seen_ids:
                    continue
                seen_ids.add(msg.message_id)

                subject = (msg.subject or "").lower()
                body = (msg.extracted_text or msg.text or "").lower()
                html = (msg.extracted_html or msg.html or "")

                if any(kw in subject or kw in body for kw in keywords):
                    all_links = extract_links(html) or extract_links(msg.text or "")
                    verification_link = find_verification_link(all_links)

                    output = {
                        "found": True,
                        "message_id": msg.message_id,
                        "subject": msg.subject,
                        "from": msg.from_ if hasattr(msg, 'from_') else str(getattr(msg, 'from_address', '')),
                        "body_preview": (msg.extracted_text or msg.text or "")[:500],
                        "verification_link": verification_link,
                        "all_links": all_links[:10],
                    }
                    print(json.dumps(output, indent=2))
                    return

        except Exception as e:
            print(f"Poll error: {e}", file=sys.stderr)

        time.sleep(5)

    print(json.dumps({"found": False, "error": "Timed out waiting for verification email"}))
    sys.exit(1)


if __name__ == "__main__":
    main()
