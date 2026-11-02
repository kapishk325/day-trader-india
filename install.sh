#!/usr/bin/env bash
# Universal Installer for day-trader-india
# Supports: Google Antigravity, Claude Code, Cursor, and Codex.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "$PWD")"
TARGET="${1:-auto}"

echo "============================================================"
echo "  Day Trader India (day-trader-india) Universal Installer   "
echo "============================================================"

# List of all 12 skills
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

installed_count=0

# 1. Google Antigravity Target
install_antigravity() {
    local dest="$HOME/.agents/skills"
    echo "-> Installing to Google Antigravity ($dest)..."
    mkdir -p "$dest"
    for s in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$s" ]; then
            rm -rf "$dest/$s"
            cp -r "$SCRIPT_DIR/$s" "$dest/$s"
            echo "   ✓ Installed $s"
            installed_count=$((installed_count + 1))
        fi
    done
    echo "✓ Antigravity installation complete!"
}

# 2. Claude Code Target
install_claude() {
    local dest="$HOME/.claude/skills"
    echo "-> Installing to Claude Code ($dest)..."
    mkdir -p "$dest"
    for s in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$s" ]; then
            rm -rf "$dest/$s"
            cp -r "$SCRIPT_DIR/$s" "$dest/$s"
            echo "   ✓ Installed $s"
            installed_count=$((installed_count + 1))
        fi
    done
    echo "✓ Claude Code installation complete!"
}

# 3. Cursor Target
install_cursor() {
    local dest="$HOME/.cursor/rules"
    echo "-> Installing to Cursor ($dest)..."
    mkdir -p "$dest"
    if [ -f "$SCRIPT_DIR/.cursor/rules/day-trader-india.mdc" ]; then
        cp "$SCRIPT_DIR/.cursor/rules/day-trader-india.mdc" "$dest/day-trader-india.mdc"
        echo "   ✓ Installed Cursor Rule: day-trader-india.mdc"
        installed_count=$((installed_count + 1))
    fi
    echo "✓ Cursor installation complete!"
}

# 4. Codex Target
install_codex() {
    local dest="$HOME/.codex/skills"
    echo "-> Installing to Codex ($dest)..."
    mkdir -p "$dest"
    for s in "${SKILLS[@]}"; do
        if [ -d "$SCRIPT_DIR/$s" ]; then
            rm -rf "$dest/$s"
            cp -r "$SCRIPT_DIR/$s" "$dest/$s"
            echo "   ✓ Installed $s"
            installed_count=$((installed_count + 1))
        fi
    done
    echo "✓ Codex installation complete!"
}

case "$TARGET" in
    antigravity)
        install_antigravity
        ;;
    claude)
        install_claude
        ;;
    cursor)
        install_cursor
        ;;
    codex)
        install_codex
        ;;
    all)
        install_antigravity
        install_claude
        install_cursor
        install_codex
        ;;
    auto|*)
        echo "Detecting installed AI coding harnesses..."
        detected=0
        if [ -d "$HOME/.agents" ] || command -v agy >/dev/null 2>&1; then
            install_antigravity
            detected=1
        fi
        if [ -d "$HOME/.claude" ] || command -v claude >/dev/null 2>&1; then
            install_claude
            detected=1
        fi
        if [ -d "$HOME/.cursor" ]; then
            install_cursor
            detected=1
        fi
        if [ -d "$HOME/.codex" ]; then
            install_codex
            detected=1
        fi

        if [ "$detected" -eq 0 ]; then
            echo "No standard global config directories found. Installing to ~/.agents and ~/.claude by default..."
            install_antigravity
            install_claude
        fi
        ;;
esac

echo "============================================================"
echo "  Success! 12 Indian Day Trading skills are now available.  "
echo "  Start a new session or run /trader-scanner to begin.      "
echo "============================================================"
