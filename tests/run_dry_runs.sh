#!/usr/bin/env bash
# ──────────────────────────────────────────────────────────────
# run_dry_runs.sh — Validate merchant reference files and
# generate the OpenClaw skill test checklist.
#
# This script:
#  1. Checks all reference files exist across skills
#  2. Validates reference file structure (required sections)
#  3. Prints a test checklist for manual skill invocation
# ──────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== AgentShopper — Reference File Validation ==="
echo "Repo: $REPO_DIR"
echo ""

# 1. Validate reference files exist for all merchants
echo "── Step 1: Reference File Inventory ──"
for skill_dir in account-creator checkout-assistant skills/accelerate-pay; do
    refs_dir="$REPO_DIR/$skill_dir/references"
    if [ -d "$refs_dir" ]; then
        echo "  $skill_dir/references/:"
        for f in "$refs_dir"/*.md; do
            if [ -f "$f" ]; then
                name=$(basename "$f")
                size=$(wc -c < "$f" | tr -d ' ')
                echo "    ✓ $name ($size bytes)"
            fi
        done
    else
        echo "  ✗ $skill_dir/references/ — directory missing!"
    fi
done
echo ""

# 2. Validate structure of reference files
echo "── Step 2: Structure Validation ──"
cd "$REPO_DIR"
python3 tests/dry_run_checkout.py --base-dir "$REPO_DIR" --validate-structure > /tmp/agentshopper_test_plan.json

TOTAL=$(python3 -c "import json; d=json.load(open('/tmp/agentshopper_test_plan.json')); print(d['total_tests'])")
READY=$(python3 -c "import json; d=json.load(open('/tmp/agentshopper_test_plan.json')); print(d['summary']['ready'])")
BLOCKED=$(python3 -c "import json; d=json.load(open('/tmp/agentshopper_test_plan.json')); print(d['summary']['blocked'])")
WARNINGS=$(python3 -c "import json; d=json.load(open('/tmp/agentshopper_test_plan.json')); print(d['summary'].get('warnings', 0))")

echo "  Total merchants: $TOTAL"
echo "  Ready:           $READY"
echo "  Blocked:         $BLOCKED"
echo "  Warnings:        $WARNINGS"
echo ""

# Show any structural issues
python3 -c "
import json
plan = json.load(open('/tmp/agentshopper_test_plan.json'))
for test in plan['tests']:
    for sv in test.get('structure_validation', []):
        if sv.get('missing_sections'):
            print(f\"  ⚠️  {sv['file']}: missing sections: {', '.join(sv['missing_sections'])}\")
"
echo ""

# 3. Print the test checklist
echo "── Step 3: OpenClaw Skill Test Checklist ──"
echo ""
python3 tests/dry_run_checkout.py --base-dir "$REPO_DIR" --checklist

# 4. Summary
echo ""
if [ "$BLOCKED" -eq 0 ]; then
    echo "✅ All reference files present."
    if [ "$WARNINGS" -gt 0 ]; then
        echo "⚠️  Some files have structural warnings — review missing sections above."
    fi
    echo ""
    echo "Next steps:"
    echo "  1. Open OpenClaw with a headed browser"
    echo "  2. Walk through each test case in the checklist above"
    echo "  3. For each skill × merchant combo, invoke the skill and verify the steps"
    echo "  4. Log results and update reference files with any corrections"
else
    echo "❌ Some tests are blocked. Fix missing reference files first."
fi
