#!/usr/bin/env python3
"""Generate a strong random password suitable for ecommerce account signups.

Usage: python3 generate_password.py [--length 16]

Output: A password string that satisfies common requirements:
  - At least 1 uppercase, 1 lowercase, 1 digit, 1 special character
  - Default 16 characters
"""

import argparse
import secrets
import string


def generate_password(length: int = 16) -> str:
    upper = secrets.choice(string.ascii_uppercase)
    lower = secrets.choice(string.ascii_lowercase)
    digit = secrets.choice(string.digits)
    special = secrets.choice("!@#$%&*")
    remaining = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%&*")
                        for _ in range(length - 4))
    password = list(upper + lower + digit + special + remaining)
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--length", type=int, default=16)
    args = parser.parse_args()
    print(generate_password(args.length))
