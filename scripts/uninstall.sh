#!/bin/bash

APP_NAME="teleport-cli"

echo "Uninstalling Teleport-CLI..."

# 1. Check if installed via apt/dpkg
if dpkg -l | grep -q "${APP_NAME}"; then
    echo "Files installed via package manager detected."
    echo "Removing package..."
    sudo apt remove -y "${APP_NAME}"
    echo "Package removed."
else
    echo "No system package found."
fi

# 2. Check for Pip Installation
echo "Checking for pip installation..."
if pip show "${APP_NAME}" &> /dev/null; then
    echo "Removing pip package..."
    pip uninstall -y "${APP_NAME}"
    echo "Pip package removed."
fi

# 3. Clean Shell Configs (Best Effort)
echo "Cleaning shell configuration files..."

FILES=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
TARGET_Script="scripts/teleport"

for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        # Check if file contains our script source
        if grep -q "$TARGET_Script" "$FILE"; then
            echo "Found reference in $FILE. Creating backup as $FILE.bak and removing line..."
            cp "$FILE" "$FILE.bak"
            # Remove lines containing 'scripts/teleport'
            sed -i "/scripts\/teleport/d" "$FILE"
        fi
    fi
done

echo "Uninstallation complete. Please restart your terminal."
