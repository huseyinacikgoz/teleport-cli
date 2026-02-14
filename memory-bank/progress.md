# Progress: Teleport

## What works
- **Universal Install (`install.sh`)**: Tested and works on Debian/Ubuntu/Mint (deb) and others (manual).
- **Jump (`tp <query>`)**: Fuzzy search and interactive selection are solid.
- **Scan (`tp scan`)**: Correctly identifies first-level subdirectories.
- **Aliases (`tp save`)**: Command saving and execution work perfectly.
- **Localization (`tp config`)**: Instant switch between English and Turkish.
- **Clean (`tp clean`)**: History management is robust.

## What's left to build
- **Fish/Zsh Native Plugins**: Currently relies on `teleport.sh` wrapper. Native plugins (oh-my-zsh/fish) could be better.
- **Official Repos**: Packages for AUR, RPM, Homebrew (Linux).
- **Themes**: User customizable TUI themes.

## Current Status
**Stable (v1.0.0)** - Ready for public release.

## Known Issues
- None reported yet.

## Evolution of project decisions
- Originally planned cross-platform (Windows/Mac), pivoted to **Linux-first** to maximize shell integration quality.
- Removed complex update/uninstall commands from CLI in favor of system package managers (`apt remove`).
- Adopted XDG Base Directory structure (`~/.local/share`) for cleaner configuration.
