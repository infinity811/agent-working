#!/bin/bash
#
# Agent Working Screensaver - Installer
# For macOS
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="agent-working"

echo "Installing agent-working..."

# Create install directory if needed
mkdir -p "$INSTALL_DIR"

# Copy script
cp "$SCRIPT_DIR/agent_working.py" "$INSTALL_DIR/$SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Detect shell and add to PATH if needed
SHELL_RC=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

# Check if PATH already includes install dir
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    if [[ -n "$SHELL_RC" ]]; then
        echo "" >> "$SHELL_RC"
        echo "# Agent Working Screensaver" >> "$SHELL_RC"
        echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_RC"
        echo "Added $INSTALL_DIR to PATH in $SHELL_RC"
    fi
fi

echo ""
echo "Installed successfully!"
echo ""
echo "To use now, run:"
echo "  source $SHELL_RC"
echo "  agent-working"
echo ""
echo "Or open a new terminal and type: agent-working"
