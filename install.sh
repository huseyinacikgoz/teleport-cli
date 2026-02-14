#!/bin/bash
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

APP_NAME="teleport-cli"
INSTALL_DIR="/opt/${APP_NAME}"
BIN_DIR="/usr/local/bin"

echo -e "${BLUE}Teleport Installer v1.0.0${NC}"
echo "---------------------------"

# Function: Manual Install (Universal)
install_manual() {
    echo -e "${BLUE}[*] Detected non-Debian system (Arch/Fedora/etc). Starting manual install...${NC}"
    
    # Check dependencies
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Error: python3 is required.${NC}"
        exit 1
    fi
    
    # Prepare Directory
    echo "Creating install directory: ${INSTALL_DIR}"
    sudo rm -rf "${INSTALL_DIR}"
    sudo mkdir -p "${INSTALL_DIR}"
    
    # Copy Files
    echo "Copying files..."
    sudo cp -r src "${INSTALL_DIR}/"
    sudo cp pyproject.toml "${INSTALL_DIR}/"
    sudo cp scripts/teleport.sh "${INSTALL_DIR}/teleport.sh"
    sudo chmod +x "${INSTALL_DIR}/teleport.sh"
    
    # Setup Venv
    echo "Setting up Python environment..."
    sudo python3 -m venv "${INSTALL_DIR}/venv"
    sudo "${INSTALL_DIR}/venv/bin/pip" install --upgrade pip --quiet
    sudo "${INSTALL_DIR}/venv/bin/pip" install "${INSTALL_DIR}" --quiet
    
    # Symlink
    echo "Creating symlink..."
    sudo ln -sf "${INSTALL_DIR}/teleport.sh" "${BIN_DIR}/tp"
    
    echo -e "${GREEN}Success! Teleport installed manually.${NC}"
}

# 1. Detect Package Manager
if command -v apt-get &> /dev/null; then
    # Debian/Ubuntu
    echo -e "${BLUE}[*] Detected Debian/Ubuntu system.${NC}"
    echo "Building .deb package..."
    chmod +x scripts/build_deb.sh
    ./scripts/build_deb.sh > /dev/null
    
    LATEST_DEB=$(ls *.deb | sort -V | tail -n 1)
    if [ -z "$LATEST_DEB" ]; then
        echo -e "${RED}Build failed.${NC}"
        exit 1
    fi
    
    echo "Installing ${LATEST_DEB}..."
    sudo apt install "./$LATEST_DEB" --reinstall

else
    # Arch, Fedora, openSUSE, etc.
    install_manual
fi

echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}Please restart your terminal to start using Teleport.${NC}"
