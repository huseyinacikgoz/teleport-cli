# Tech Context: Teleport

## Technologies Used
- **Language:** Python 3.10+ (CLI Logic), Bash/Zsh (Shell Wrapper).
- **Core Dependencies:**
    - `typer`: CLI framework.
    - `rich`: Beautiful TUI rendering.
    - `rapidfuzz`: Fuzzy matching algorithm.
- **Database:** SQLite (built-in).
- **Standards:** XDG Base Directory Specification (`~/.local/share/teleport`).

## Development Setup
- **Linux:** Ubuntu/Debian, Arch, Fedora, Mint.
- **Project Structure:**
    - `src/teleport/`: Python package.
    - `scripts/`: Shell scripts (build, run, bump version).
    - `pyproject.toml`: Build configuration.
    - `install.sh`: Master installer.

## Constraints
- **Shell Support:** Currently Bash and Zsh are prioritized.
- **Permissions:** `sudo` required for installation (`/opt` and `/usr/local/bin`).
- **Dependencies:** User must have Python 3 and basic build tools.

## Tool Usage Patterns
- **Build System:** `dpkg-deb` for packaging (Debian).
- **Version Control:** Git, with custom `scripts/bump_version.sh` for easy updates.
