# Product Context: Teleport

## Why this exists?
Traditional `cd` commands are tedious for frequently navigating deep directory structures. Alias managers are often complex or environment-dependent. Teleport aims to solve this by learning from the user and providing a smart, fuzzy-matched navigation system.

## Problems Solved
- **Tedious Typing:** Eliminates the need to type full paths like `cd /var/www/html/project/src`.
- **Memory Load:** No need to remember exact path names; fuzzy search handles partial queries.
- **Complex Aliases:** Instead of managing `.bashrc` aliases manually, Teleport provides a dedicated command (`tp save`) for it.

## How it works
1.  **Learn:** User adds directories manually (`tp add`) or scans a folder (`tp scan`).
2.  **Search:** User types `tp <query>` (e.g., `tp pro`).
3.  **Jump:** Based on frequency and match score, Teleport either jumps directly or presents a menu.

## User Experience Goals
- **Zero Config:** Just install and use.
- **Fast:** Sub-second response time.
- **Clean Output:** Beautiful TUI using Rich library.
- **Language Support:** Feels native to Turkish users.
