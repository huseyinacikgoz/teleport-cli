# Project Brief: Teleport

Minimalist, smart directory navigation tool for Linux.

## Overview
Teleport is a CLI utility that learns frequently visited directories and allows users to jump to them instantly using fuzzy search, interactive menus, or saved aliases. It is designed to be lightweight, fast, and user-friendly, with full bilingual support (English/Turkish).

## Core Goals
- **Minimalism:** No background daemons, simple SQLite database.
- **Speed:** Instant directory switching.
- **Usability:** Interactive TUI for multiple matches.
- **Localization:** Native support for Turkish users.
- **Universal Linux Support:** Works on Debian, Arch, Fedora, etc.

## Key Features
- **Smart Jump (`tp <query>`):** Fuzzy search for best match.
- **Scan (`tp scan`):** Auto-discover subdirectories.
- **Aliases (`tp save`):** Shortcut for long commands.
- **Clean (`tp clean`):** Manage history easily.
- **Config (`tp config`):** Switch languages instantly.
