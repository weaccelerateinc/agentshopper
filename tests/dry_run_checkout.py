#!/usr/bin/env python3
"""Merchant reference file validation and test plan generator for AgentShopper.

Validates that all merchant reference files exist across skills, checks their
structure, and generates a test checklist for manual OpenClaw skill invocation.

Usage:
  # Validate all merchants and generate test plan
  python3 tests/dry_run_checkout.py

  # Validate a single merchant
  python3 tests/dry_run_checkout.py --merchant allbirds.com

  # List available test configs
  python3 tests/dry_run_checkout.py --list

  # Validate reference file structure (checks for required sections)
  python3 tests/dry_run_checkout.py --validate-structure
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# ── Test Configurations ─────────────────────────────────────────────────────
# Each entry defines a merchant + product + variant to test via OpenClaw skills.
# product_url should point to a widely-available, non-limited item.

TEST_CONFIGS = [
    {
        "merchant": "allbirds.com",
        "name": "Allbirds — Tree Runners",
        "product_url": "https://www.allbirds.com/products/mens-tree-runners",
        "variant": {"color": "Basin Blue", "size": "10"},
        "platform": "shopify-plus",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/allbirds.md",
            "checkout-assistant/references/allbirds.md",
            "skills/accelerate-pay/references/allbirds.md",
        ],
        "expected_issues": [
            "hCaptcha may trigger on Shopify checkout",
            "Shop Pay overlay may need dismissal",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on allbirds.com'",
                "Verify: browser opens allbirds.com/account/login → redirects to accounts.allbirds.com",
                "Verify: email entered, CONTINUE clicked (Shopify New Customer Accounts, passwordless)",
                "Verify: 6-digit verification code retrieved from agentmail inbox",
                "Verify: code entered, account created (no password)",
                "Verify: email saved (passwordless — no password to store)",
            ],
            "checkout-assistant": [
                "Invoke: 'add Allbirds Tree Runners size 10 to cart and checkout'",
                "Verify: browser navigates to product page",
                "Verify: size 10 selected, Add to Cart clicked",
                "Verify: Shopify checkout reached (Information → Shipping → Payment)",
                "Verify: stops at Payment step with screenshot",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: Shopify card fields identified (not iframe-based)",
                "Verify: card number, expiry, CVV filled via keyboard input",
                "Verify: stops before submitting with screenshot",
            ],
        },
    },
    {
        "merchant": "victoriassecret.com",
        "name": "Victoria's Secret — Cotton T-Shirt Bra",
        "product_url": "https://www.victoriassecret.com/us/vs/bras-702702",
        "variant": {"color": "Black", "size": "34C"},
        "platform": "custom",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/victoriassecret.md",
            "checkout-assistant/references/victoriassecret.md",
            "skills/accelerate-pay/references/victoriassecret.md",
        ],
        "expected_issues": [
            "Marketing pop-ups likely to appear",
            "VS credit card promotion overlay during checkout",
            "Bra sizing requires band + cup selection",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on victoriassecret.com'",
                "Verify: browser opens VS unified 'Sign In or Create Account' page",
                "Verify: email entered + CONTINUE clicked (unified flow detects new email)",
                "Verify: additional fields filled (Password, First Name, Last Name)",
                "Verify: check agentmail for verification email if needed",
                "Verify: credentials saved to Keychain",
            ],
            "checkout-assistant": [
                "Invoke: 'add VS Cotton T-Shirt Bra 34C Black to cart'",
                "Verify: browser navigates to product page",
                "Verify: band size 34 + cup size C selected",
                "Verify: color Black selected, Add to Bag clicked",
                "Verify: checkout reached, stops at Payment step",
                "Verify: VS credit card promo dismissed (standard card path chosen)",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: standard card payment option selected (not VS card, not Klarna/Zip)",
                "Verify: card fields identified (check if inline or iframe)",
                "Verify: card details filled, stops before submitting",
            ],
        },
    },
    {
        "merchant": "hoka.com",
        "name": "Hoka — Clifton 10 (existing)",
        "product_url": "https://www.hoka.com/en/us/mens-road/clifton-10/1160025.html",
        "variant": {"color": "Black", "size": "10"},
        "platform": "custom",
        "skills_covered": ["account-creator", "checkout-assistant"],
        "reference_files": [
            "account-creator/references/hoka.md",
            "checkout-assistant/references/hoka.md",
        ],
        "expected_issues": [
            "CAPTCHA on first visit (slide-to-verify)",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on hoka.com'",
                "Verify: browser opens hoka.com/en/us/login/",
                "Verify: 'Join Us' tab clicked",
                "Verify: form fills First Name, Last Name, Email, Password",
                "Verify: membership checkbox checked, 'Join for Free' clicked",
                "Verify: 'Welcome to the crew!' shown, credentials saved",
                "WATCH FOR: CAPTCHA slide-to-verify on first visit",
            ],
            "checkout-assistant": [
                "Invoke: 'add Hoka Clifton 10 size 10 to cart and checkout'",
                "Verify: browser navigates to product page",
                "Verify: size 10 selected, Add to Bag clicked",
                "Verify: checkout reached, stops at Payment step",
            ],
        },
    },
    {
        "merchant": "dsw.com",
        "name": "DSW — existing accelerate-pay reference",
        "product_url": "https://www.dsw.com/",
        "variant": {},
        "platform": "custom",
        "skills_covered": ["accelerate-pay"],
        "reference_files": [
            "skills/accelerate-pay/references/dsw.md",
        ],
        "expected_issues": [
            "Vantiv iframe load delay (~5s)",
            "Unisex sizing display",
        ],
        "test_steps": {
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from DSW checkout /check-out/pay)",
                "Verify: Vantiv iframe detected (vantiv-payframe)",
                "Verify: fill-vantiv-all.sh executed via CDP WebSocket",
                "Verify: all 4 card fields filled in single call",
                "Verify: 'Continue to Review' clicked, screenshot taken",
            ],
        },
    },
    {
        "merchant": "warbyparker.com",
        "name": "Warby Parker — Durand Eyeglasses",
        "product_url": "https://www.warbyparker.com/eyeglasses/durand/whiskey-tortoise",
        "variant": {"color": "Whiskey Tortoise", "width": "Medium"},
        "platform": "shopify-plus",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/warbyparker.md",
            "checkout-assistant/references/warbyparker.md",
            "skills/accelerate-pay/references/warbyparker.md",
        ],
        "expected_issues": [
            "Prescription step may block checkout before payment",
            "Stripe Elements iframes for card fields (not standard HTML inputs)",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on warbyparker.com'",
                "Verify: browser opens warbyparker.com/login → redirects to auth.warbyparker.com (Auth0)",
                "Verify: form fills First Name, Last Name, Email (no password — passwordless auth)",
                "Verify: verification code retrieved from agentmail inbox",
                "Verify: code entered, account created",
                "Verify: email saved (passwordless — no password to store)",
            ],
            "checkout-assistant": [
                "Invoke: 'add Warby Parker Durand in Whiskey Tortoise to cart'",
                "Verify: browser navigates to product page",
                "Verify: color and width selected, 'Select lenses and buy' clicked",
                "Verify: checkout begins — may hit Prescription step before Payment",
                "Verify: stops at Payment step OR Prescription step with screenshot",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: Stripe card fields identified (check if iframe-based Elements)",
                "Verify: card number, expiry, CVV filled via keyboard input",
                "Verify: stops before submitting with screenshot",
                "WATCH FOR: Stripe Elements iframes require clicking into each field separately",
            ],
        },
    },
    {
        "merchant": "glossier.com",
        "name": "Glossier — Boy Brow",
        "product_url": "https://www.glossier.com/products/boy-brow",
        "variant": {"color": "Brown"},
        "platform": "shopify-plus",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/glossier.md",
            "checkout-assistant/references/glossier.md",
            "skills/accelerate-pay/references/glossier.md",
        ],
        "expected_issues": [
            "Aggressive email capture pop-up on every page visit",
            "Shop Pay overlay may need dismissal",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on glossier.com'",
                "Verify: browser opens glossier.com/account/register",
                "Verify: email capture pop-up dismissed",
                "Verify: form fills First Name, Last Name, Email, Password",
                "Verify: Terms checkbox checked (required — blocks signup if unchecked)",
                "Verify: account created, credentials saved to Keychain",
            ],
            "checkout-assistant": [
                "Invoke: 'add Glossier Boy Brow in Brown to cart'",
                "Verify: browser navigates to product page",
                "Verify: shade Brown selected, Add to Bag clicked",
                "Verify: email pop-up dismissed if it reappears",
                "Verify: Shopify checkout reached, stops at Payment step",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: Shopify card fields identified (inline, not iframe)",
                "Verify: card number, expiry, CVV filled via keyboard input",
                "Verify: stops before submitting with screenshot",
            ],
        },
    },
    {
        "merchant": "bombas.com",
        "name": "Bombas — Men's Solids Ankle Sock",
        "product_url": "https://www.bombas.com/products/men-s-solid-ankle-sock-white-large-1",
        "variant": {"color": "White", "size": "Large"},
        "platform": "shopify",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/bombas.md",
            "checkout-assistant/references/bombas.md",
            "skills/accelerate-pay/references/bombas.md",
        ],
        "expected_issues": [
            "Newsletter '20% Off' pop-up on first visit",
            "Amazon Pay / PayPal express buttons may need to be scrolled past",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on bombas.com'",
                "Verify: browser opens bombas.com/account/login (NOT /register — it renders blank)",
                "Verify: '20% Off' newsletter pop-up dismissed",
                "Verify: 'Don't Have An Account? Sign Up' link clicked",
                "Verify: form fills Email, First Name, Last Name, Password",
                "Verify: account created immediately (no verification)",
                "Verify: credentials saved to Keychain",
            ],
            "checkout-assistant": [
                "Invoke: 'add Bombas Men's Ankle Sock White Large to cart'",
                "Verify: browser navigates to product page",
                "Verify: color White and size Large selected, Add to Cart clicked",
                "Verify: Shopify checkout reached, stops at Payment step",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: Shopify card fields identified (inline, not iframe)",
                "Verify: Amazon Pay / PayPal buttons scrolled past",
                "Verify: card number, expiry, CVV filled via keyboard input",
                "Verify: stops before submitting with screenshot",
            ],
        },
    },
    {
        "merchant": "awaytravel.com",
        "name": "Away — The Carry-On",
        "product_url": "https://www.awaytravel.com/products/carry-on-jet-black",
        "variant": {"color": "Jet Black"},
        "platform": "shopify-plus",
        "skills_covered": ["account-creator", "checkout-assistant", "accelerate-pay"],
        "reference_files": [
            "account-creator/references/away.md",
            "checkout-assistant/references/away.md",
            "skills/accelerate-pay/references/away.md",
        ],
        "expected_issues": [
            "Referral discount overlay on first visit",
            "Klarna BNPL prompt at checkout",
            "ID.me verification banner may appear",
        ],
        "test_steps": {
            "account-creator": [
                "Invoke: 'create an account on awaytravel.com'",
                "Verify: browser opens awaytravel.com/login → redirects to accounts.awaytravel.com",
                "Verify: referral overlay dismissed if present",
                "Verify: email entered, CONTINUE clicked (Shopify New Customer Accounts, passwordless)",
                "Verify: 6-digit verification code retrieved from agentmail inbox",
                "Verify: code entered, account created (no password)",
                "Verify: email saved (passwordless — no password to store)",
            ],
            "checkout-assistant": [
                "Invoke: 'add Away Carry-On in Jet Black to cart'",
                "Verify: browser navigates to product page",
                "Verify: color Jet Black selected, Add to Cart clicked",
                "Verify: Shopify checkout reached, stops at Payment step",
                "WATCH FOR: Klarna / referral discount auto-apply after email entry",
            ],
            "accelerate-pay": [
                "Invoke: 'pay with Accelerate' (from checkout payment step)",
                "Verify: Klarna BNPL dismissed, standard credit card selected",
                "Verify: Shopify card fields identified (inline, not iframe)",
                "Verify: card number, expiry, CVV filled via keyboard input",
                "Verify: stops before submitting with screenshot",
                "WATCH FOR: Away may reject prepaid cards",
            ],
        },
    },
]

# ── Required Sections per Skill ─────────────────────────────────────────────
# These headings should appear in reference files for each skill type.

REQUIRED_SECTIONS = {
    "account-creator": ["URL", "Signup Form Fields", "Flow", "Common Issues"],
    "checkout-assistant": ["URL", "Browser Mode", "Product Variant Behavior",
                           "Login Guidance", "Coupon", "Stop Condition"],
    "accelerate-pay": ["Payment Provider", "Field", "Fill Strategy", "Gotchas"],
}


def validate_reference_files(config: dict, base_dir: str) -> list[dict]:
    """Check that all referenced files exist and have non-zero content."""
    results = []
    for ref_file in config.get("reference_files", []):
        full_path = os.path.join(base_dir, ref_file)
        exists = os.path.exists(full_path)
        size = os.path.getsize(full_path) if exists else 0
        results.append({
            "file": ref_file,
            "exists": exists,
            "size_bytes": size,
            "has_content": size > 100,  # Sanity check: not just a stub
        })
    return results


def validate_structure(config: dict, base_dir: str) -> list[dict]:
    """Check that reference files contain expected section headings."""
    results = []
    for ref_file in config.get("reference_files", []):
        full_path = os.path.join(base_dir, ref_file)
        if not os.path.exists(full_path):
            results.append({"file": ref_file, "error": "file not found"})
            continue

        with open(full_path) as f:
            content = f.read()

        # Determine which skill this reference belongs to
        skill = None
        for skill_name in REQUIRED_SECTIONS:
            if skill_name in ref_file:
                skill = skill_name
                break

        if not skill:
            results.append({"file": ref_file, "error": "unknown skill type"})
            continue

        headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        headings_text = " ".join(headings).lower()

        missing = []
        for required in REQUIRED_SECTIONS[skill]:
            if required.lower() not in headings_text:
                missing.append(required)

        results.append({
            "file": ref_file,
            "skill": skill,
            "headings_found": headings,
            "missing_sections": missing,
            "valid": len(missing) == 0,
        })

    return results


def generate_test_plan(merchants: list[str] | None = None, base_dir: str = ".",
                       include_structure: bool = False) -> dict:
    """Generate a structured test plan for OpenClaw skill testing."""
    configs = TEST_CONFIGS
    if merchants:
        configs = [c for c in configs if c["merchant"] in merchants]

    plan = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_tests": len(configs),
        "tests": [],
    }

    for config in configs:
        ref_validation = validate_reference_files(config, base_dir)
        all_refs_exist = all(r["exists"] and r["has_content"] for r in ref_validation)

        test = {
            "merchant": config["merchant"],
            "name": config["name"],
            "product_url": config["product_url"],
            "variant": config["variant"],
            "platform": config["platform"],
            "skills_covered": config["skills_covered"],
            "reference_files_valid": all_refs_exist,
            "reference_file_details": ref_validation,
            "expected_issues": config["expected_issues"],
            "test_steps": config.get("test_steps", {}),
            "status": "ready" if all_refs_exist else "blocked_missing_refs",
        }

        if include_structure:
            test["structure_validation"] = validate_structure(config, base_dir)
            structure_ok = all(
                s.get("valid", False) for s in test["structure_validation"]
                if "error" not in s
            )
            if not structure_ok:
                test["status"] = "warning_incomplete_structure"

        plan["tests"].append(test)

    plan["summary"] = {
        "ready": sum(1 for t in plan["tests"] if t["status"] == "ready"),
        "blocked": sum(1 for t in plan["tests"] if t["status"] == "blocked_missing_refs"),
        "warnings": sum(1 for t in plan["tests"] if t["status"] == "warning_incomplete_structure"),
    }

    return plan


def print_test_checklist(plan: dict):
    """Print a human-readable test checklist from a plan."""
    print("=" * 70)
    print("  AgentShopper — OpenClaw Skill Test Checklist")
    print("=" * 70)
    print()

    for test in plan["tests"]:
        status_icon = "✅" if test["status"] == "ready" else "⚠️" if "warning" in test["status"] else "❌"
        print(f"{status_icon} {test['name']} ({test['merchant']})")
        print(f"   Platform: {test['platform']}")
        print(f"   Product:  {test['product_url']}")
        if test["variant"]:
            print(f"   Variant:  {json.dumps(test['variant'])}")
        print()

        for skill, steps in test.get("test_steps", {}).items():
            print(f"   [{skill}]")
            for i, step in enumerate(steps, 1):
                prefix = "   ⚡" if step.startswith("WATCH FOR") else f"   {i}."
                print(f"     {prefix} {step}")
            print()

        if test["expected_issues"]:
            print("   Known issues:")
            for issue in test["expected_issues"]:
                print(f"     — {issue}")
        print()
        print("-" * 70)
        print()


def main():
    parser = argparse.ArgumentParser(description="AgentShopper test plan generator")
    parser.add_argument("--merchant", help="Test a single merchant (e.g., allbirds.com)")
    parser.add_argument("--list", action="store_true", help="List available test configs")
    parser.add_argument("--validate-structure", action="store_true",
                        help="Also validate reference file section headings")
    parser.add_argument("--checklist", action="store_true",
                        help="Print human-readable test checklist instead of JSON")
    parser.add_argument("--base-dir", default=".", help="Base directory of agentshopper repo")
    args = parser.parse_args()

    if args.list:
        print("Available test configurations:\n")
        for c in TEST_CONFIGS:
            print(f"  {c['merchant']:25s} — {c['name']}")
            print(f"    Platform: {c['platform']}")
            print(f"    Skills:   {', '.join(c['skills_covered'])}")
            print(f"    Product:  {c['product_url']}")
            print()
        return

    merchants = [args.merchant] if args.merchant else None
    plan = generate_test_plan(
        merchants=merchants,
        base_dir=args.base_dir,
        include_structure=args.validate_structure,
    )

    if args.checklist:
        print_test_checklist(plan)
    else:
        print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()
