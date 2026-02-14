# Active Context: Teleport

## Current Focus
We have just finalized **version 1.0.0 (Stable)**. The focus is on ensuring the stability of the installation script (`install.sh`) and refining user experience (documentation, messages).

## Recent Changes
- **Universal Install (`install.sh`):** Supports both Debian-based (.deb) and other Linux distros (manual install).
- **Scan Feature (`tp scan`):** Automatically adds subdirectories (depth 1) to the database.
- **Smart Jump:** Improved fuzzy matching threshold and logic (`process.extractOne`), search for exact matches first.
- **Branding:** Renamed "Teleport-CLI" to "Teleport" in all user facing texts.
- **Bilingual Documentation:** Completely revamped README to be cleaner and bilingual.

## Next Steps
- Monitor user feedback (GitHub Issues).
- Consider adding more shell integrations (Fish, etc.).
- Potential UI enhancements (Custom themes).

## Active Decisions
- Keep `tp scan` depth at 1 for now to prevent database clutter.
- Stick to manual `/opt` installation for non-Debian systems until proper packages (AUR/RPM) are created.
