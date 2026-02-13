# Teleport-CLI

A cross-platform directory navigation tool that learns from your habits.
(Works on Linux, macOS, and Windows)

## Features
- **Smart Jump**: `tp <query>` uses fuzzy matching to find the best directory.
- **Interactive**: Select from a list if multiple matches are found.
- **Frecency**: Tracks frequency and recency of your visits.
- **Cross-Platform**: Full support for Linux, macOS, and Windows.
- **Command Snippets**: Save and run complex commands.

## Installation

1. Install the Python package:
   ```bash
   pip install .
   ```

2. Add the shell integration to your config file:

   ### Bash (~/.bashrc)
   ```bash
   source /path/to/teleport-cli/scripts/teleport.bash
   ```

   ### Zsh (~/.zshrc)
   ```zsh
   source /path/to/teleport-cli/scripts/teleport.zsh
   ```

   ### PowerShell ($PROFILE)
   ```powershell
   . /path/to/teleport-cli/scripts/teleport.ps1
   ```

## Usage

- **Add current directory**: `tp add`
- **Jump to a directory**: `tp <query>` (e.g., `tp doc`)
- **Interactive Selection**: `tp` (no arguments)
- **Save a command**: `tp save "command" --name alias`
- **List history/commands**: `tp list`
