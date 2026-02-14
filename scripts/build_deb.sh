#!/bin/bash
set -e

APP_NAME="teleport-cli"
VERSION="1.0.0"
ARCH="all"
DEB_NAME="${APP_NAME}_${VERSION}_${ARCH}"
BUILD_DIR="build/debian/${DEB_NAME}"
INSTALL_DIR="/opt/${APP_NAME}"

# Clean Build
echo "Building ${DEB_NAME}..."
rm -rf build/debian
mkdir -p "${BUILD_DIR}/DEBIAN" "${BUILD_DIR}${INSTALL_DIR}" "${BUILD_DIR}/etc/profile.d"

# Copy Files
cp -r src "${BUILD_DIR}${INSTALL_DIR}/"
cp pyproject.toml "${BUILD_DIR}${INSTALL_DIR}/"
cp scripts/teleport.sh "${BUILD_DIR}${INSTALL_DIR}/teleport.sh"
cp README.md "${BUILD_DIR}${INSTALL_DIR}/"

# Control File
cat > "${BUILD_DIR}/DEBIAN/control" <<EOF
Package: ${APP_NAME}
Version: ${VERSION}
Section: utils
Priority: optional
Architecture: ${ARCH}
Depends: python3, python3-pip, python3-venv
Maintainer: Huseyin Acikgoz <huseyin@huseyinacikgoz.com.tr>
Description: Minimalist Linux Directory Jumper
 Teleport-CLI learns your habits and helps you jump between directories.
 Features interactive menu, fuzzy search, and command aliases.
EOF

# Post-Install
cat > "${BUILD_DIR}/DEBIAN/postinst" <<EOF
#!/bin/bash
set -e
INSTALL_DIR="${INSTALL_DIR}"

if [ ! -d "\${INSTALL_DIR}/venv" ]; then
    python3 -m venv "\${INSTALL_DIR}/venv" > /dev/null 2>&1
fi
"\${INSTALL_DIR}/venv/bin/pip" install --upgrade pip --quiet
"\${INSTALL_DIR}/venv/bin/pip" install "\${INSTALL_DIR}" --quiet

chmod -R a+rX "\${INSTALL_DIR}"
chmod +x "\${INSTALL_DIR}/teleport.sh"

echo "Teleport-CLI v${VERSION} Installed."
EOF
chmod 755 "${BUILD_DIR}/DEBIAN/postinst"

# Pre-Remove
cat > "${BUILD_DIR}/DEBIAN/prerm" <<EOF
#!/bin/bash
rm -rf "${INSTALL_DIR}/venv"
EOF
chmod 755 "${BUILD_DIR}/DEBIAN/prerm"

# Default Profile
echo "source ${INSTALL_DIR}/teleport.sh" > "${BUILD_DIR}/etc/profile.d/teleport.sh"

# Build Package
dpkg-deb --build "${BUILD_DIR}" > /dev/null
mv "${BUILD_DIR}.deb" .
echo "Done: ${DEB_NAME}.deb"
