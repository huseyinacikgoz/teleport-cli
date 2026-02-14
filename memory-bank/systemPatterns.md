# System Patterns: Teleport

## Architecture
- **Shell Wrapper (`scripts/teleport.sh`):** Acts as the entry point (`tp`). Handles commands that require changing the shell's state (`cd`), since subprocesses (like Python) cannot change the parent shell's working directory.
- **Python Backend (`src/teleport/cli.py`):** Core logic for parsing commands, querying database, managing history, and rendering TUI.
- **SQLite Database (`~/.local/share/teleport/db.sqlite`):** Stores directories (with visit counts/scores) and command aliases.

## Key Design Patterns
1.  **Wrapper Pattern:** The `tp` function wraps the Python call to orchestrate `cd` or `eval`. It uses a temporary file to exchange data (target directory or command string).
2.  **Singleton Database:** A single `TeleportDB` instance manages connections.
3.  **Command Pattern (Typer):** Each CLI command (`add`, `scan`, `save`) is implemented as a distinct Typer command function.
4.  **Localization Strategy:** Simple key-value store (`STRINGS` dict) switched by a config file (`lang.txt`).

## Critical Implementation Paths
- **Jump Logic:** `tp <query>` -> Python fuzzy search -> Output `CD:<path>` to temp file -> Wrapper reads temp file -> Wrapper executes `cd <path>`.
- **Scan Logic:** `tp scan` -> Python scans directories (depth 1) -> Adds valid paths to DB -> Output summary.
- **Installation:** `install.sh` handles detection (Ubuntu/Debian vs. Others) and performs either package install or manual setup.
