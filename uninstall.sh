#!/usr/bin/env bash
# Universal Uninstaller for day-trader-india
# Cleanly removes all 12 skills and rules from Antigravity, Claude Code, Cursor, and Codex.

set -e

echo "============================================================"
echo "  Day Trader India (day-trader-india) Uninstaller           "
echo "============================================================"

SKILLS=(
    "trader-scanner"
    "trader-fii-dii"
    "trader-oi"
    "trader-news"
    "trader-entry"
    "trader-exit"
    "trader-timemachine"
    "trader-budget"
    "trader-risk"
    "trader-broker"
    "trader-alerts"
    "trader-analyst"
)

removed_count=0

remove_skills_from() {
    local target_dir="$1"
    local name="$2"
    if [ -d "$target_dir" ]; then
        echo "-> Removing from $name ($target_dir)..."
        for s in "${SKILLS[@]}"; do
            if [ -d "$target_dir/$s" ]; then
                rm -rf "$target_dir/$s"
                echo "   ✗ Removed $s"
                removed_count=$((removed_count + 1))
            fi
        done
    fi
}

# 1. Antigravity (~/.agents/skills and ~/.gemini/skills)
remove_skills_from "$HOME/.agents/skills" "Google Antigravity (~/.agents)"
remove_skills_from "$HOME/.gemini/skills" "Google Antigravity (~/.gemini)"

# 2. Claude Code (~/.claude/skills)
remove_skills_from "$HOME/.claude/skills" "Claude Code"

# 3. Codex (~/.codex/skills)
remove_skills_from "$HOME/.codex/skills" "Codex"

# 4. Cursor (~/.cursor/rules)
if [ -f "$HOME/.cursor/rules/day-trader-india.mdc" ]; then
    echo "-> Removing from Cursor (~/.cursor/rules)..."
    rm -f "$HOME/.cursor/rules/day-trader-india.mdc"
    echo "   ✗ Removed day-trader-india.mdc"
    removed_count=$((removed_count + 1))
fi

echo "============================================================"
if [ "$removed_count" -gt 0 ]; then
    echo "  Cleaned up $removed_count skills/rules across all harnesses. "
    echo "  day-trader-india has been successfully uninstalled.        "
else
    echo "  No installed day-trader-india skills were found.          "
fi
echo "============================================================"
