#!/bin/bash
# Save credentials to macOS Keychain (Apple Passwords).
#
# Usage: save_to_keychain.sh <website> <email> <password>
#
# Saves as an internet password visible in the Passwords app.

set -euo pipefail

WEBSITE="${1:?Usage: save_to_keychain.sh <website> <email> <password>}"
EMAIL="${2:?Missing email}"
PASSWORD="${3:?Missing password}"

# Add as internet password to default keychain
security add-internet-password \
  -a "$EMAIL" \
  -s "$WEBSITE" \
  -w "$PASSWORD" \
  -r "htps" \
  -l "$WEBSITE ($EMAIL)" \
  -T "" \
  2>/dev/null

echo "✅ Saved to Apple Passwords: $WEBSITE ($EMAIL)"
