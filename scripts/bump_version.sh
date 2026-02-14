#!/bin/bash
NEW_VERSION="$1"

if [ -z "$NEW_VERSION" ]; then
    echo "Usage: ./scripts/bump_version.sh <new_version>"
    exit 1
fi

echo "Bumping version to $NEW_VERSION..."

# 1. pyproject.toml
sed -i "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml

# 2. src/teleport/cli.py
sed -i "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" src/teleport/cli.py

# 3. scripts/build_deb.sh
sed -i "s/VERSION=\".*\"/VERSION=\"$NEW_VERSION\"/" scripts/build_deb.sh

# 4. scripts/teleport.sh
sed -i "s/Teleport v.*/Teleport v$NEW_VERSION/" scripts/teleport.sh

# 5. README.md (Badge)
sed -i "s/version-.*-blue/version-$NEW_VERSION-blue/" README.md

# 6. install.sh
sed -i "s/Installer v.*/Installer v$NEW_VERSION/" install.sh

echo "Done! All files updated to v$NEW_VERSION."
