import typer
import os
import sys
from pathlib import Path
from typing import Optional, List
from rapidfuzz import process, fuzz, utils as fuzz_utils
from .db import TeleportDB
from .tui import select_path

app = typer.Typer(help="Teleport CLI - Smart directory navigation.")
db_instance = None

def get_db():
    global db_instance
    if db_instance is None:
        db_instance = TeleportDB()
    return db_instance

@app.callback()
def callback():
    """
    Teleport CLI tool.
    Use 'tp jump <query>' to navigate or 'tp add' to save a directory.
    """
    pass

@app.command()
def add(path: Optional[str] = typer.Argument(None, help="Path to add. Defaults to current directory.")):
    """Add a directory to the history."""
    db = get_db()
    target_path = path or os.getcwd()
    abs_path = str(Path(target_path).resolve())
    db.add_path(abs_path)
    # Output to stderr to avoid cluttering if captured
    typer.echo(f"Added {abs_path} to history.", err=True)

@app.command()
def save(command: str = typer.Argument(..., help="The shell command to save"), 
         name: str = typer.Option(..., "--name", "-n", help="Alias for the command")):
    """Save a shell command with an alias."""
    db = get_db()
    db.add_command(name, command)
    typer.echo(f"Saved alias '{name}' for command '{command}'", err=True)

@app.command(name="--update")
def update_alias():
    """Alias for update command."""
    update()

@app.command()
def update():
    """
    Update the tool from source (git pull + reinstall).
    """
    import subprocess
    
    # Assuming code is in src/teleport/cli.py, project root is 3 levels up
    project_dir = Path(__file__).parent.parent.parent.resolve()
    
    # Check if we are running in an installed package (site-packages) or local
    # If project_dir doesn't contain pyproject.toml, we might be in site-packages
    if not (project_dir / "pyproject.toml").exists():
         # Maybe we need to clone? 
         # But the user is developing this. Let's assume they run it from source or editable install.
         # If installed via pip install ., the source files are copied to site-packages, so git pull won't work there.
         # But for this task, the user has the source in the workspace.
         # We'll just warn if we can't find git.
         pass

    typer.echo(f"Updating Teleport-CLI...", err=True)
    
    # 1. Try git pull
    if (project_dir / ".git").exists():
        try:
            typer.echo("Running git pull...", err=True)
            subprocess.check_call(["git", "pull"], cwd=project_dir)
        except Exception as e:
            typer.echo(f"Git pull failed: {e}. Continuing with reinstall...", err=True)
    
    # 2. Pip install
    try:
        typer.echo("Reinstalling package...", err=True)
        # Use pip to install the package in the current environment
        subprocess.check_call([sys.executable, "-m", "pip", "install", "."], cwd=project_dir)
        typer.echo("Update complete successfully!", err=True)
    except Exception as e:
        typer.echo(f"Installation failed: {e}", err=True)

@app.command("list")
def list_entries():
    """List all saved commands and frequent paths."""
    db = get_db()
    
    typer.echo("--- Saved Commands ---")
    commands = db.list_commands()
    for alias, cmd, _ in commands:
        typer.echo(f"{alias}: {cmd}")
        
    typer.echo("\n--- Frequent Paths ---")
    paths = db.get_frequent_paths()
    for p, score in paths[:15]:
        typer.echo(f"{p} (Score: {score:.2f})")

@app.command()
def jump(
    query: Optional[List[str]] = typer.Argument(None, help="Search query for directory or alias. Can be multiple words."),
    output_file: Optional[Path] = typer.Option(None, "--output-file", "-o", help="File to write the result to"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Force interactive selection"),
):
    """
    Smart jump to a directory or execute a command.
    """
    db = get_db()
    
    # Join query list into a single string for fuzzy matching
    full_query = " ".join(query) if query else None
    
    # 1. Check for Aliases first (exact match)
    if full_query:
        cmd = db.get_command(full_query)
        if cmd:
            _write_result(f"CMD:{cmd}", output_file)
            return

    # 2. Get Directory Candidates
    frequent_paths = db.get_frequent_paths() # [(path, score), ...]
    
    if not frequent_paths:
        typer.echo("No history yet. Use 'tp add' to add the current directory.", err=True)
        return

    # Normalize scores
    max_score = frequent_paths[0][1] if frequent_paths else 1
    
    candidates = [] 
    for p, score in frequent_paths:
        candidates.append({
            "value": p,
            "display": f"{p} ({score:.1f})",
            "score": score / max_score
        })

    final_list = []
    
    if full_query:
        # Check if query is a path itself
        possible_path = Path(full_query).expanduser().resolve()
        try:
             if possible_path.exists() and possible_path.is_dir():
                 # If user typed a real path, just use it
                 _write_result(f"CD:{possible_path}", output_file)
                 return
        except OSError:
             pass

        # Fuzzy Match
        choices = [c["value"] for c in candidates]
        # scorer=fuzz.WRatio works well for mixed content
        results = process.extract(full_query, choices, scorer=fuzz.WRatio, limit=20)
        
        scored_results = []
        for value, match_score, index in results:
            candidate = candidates[index]
            # Boost score with frecency
            # Match score 0-100. Frecency 0-1.
            # We treat match score as primary, textual match is important.
            # But "doc" matching "Documents" (100) vs "Docker" (100) needs frecency tie break.
            
            combined_score = match_score + (candidate["score"] * 20) # Boost up to 20 pts for frecency
            scored_results.append((candidate["value"], combined_score))
            
        scored_results.sort(key=lambda x: x[1], reverse=True)
        final_list = [x[0] for x in scored_results]
    else:
        # Just frecency
        final_list = [c["value"] for c in candidates[:15]]

    if not final_list:
        typer.echo("No matching paths found.", err=True)
        return

    selected_path = None
    
    # Decision Logic: Jump or Ask
    # If explicit interactive OR (no query AND interactive default for 'tp')
    force_interactive = interactive or (not full_query)
    
    if not force_interactive:
        # Smart Jump: Use top result
        selected_path = final_list[0]
        typer.echo(f"Jumping to: {selected_path}", err=True)
    else:
        # Interactive Menu
        selected_path = select_path(final_list)

    if selected_path:
        # Update history
        db.add_path(selected_path)
        _write_result(f"CD:{selected_path}", output_file)

def _write_result(content: str, output_file: Optional[Path]):
    if output_file:
        with open(output_file, 'w') as f:
            f.write(content)
    else:
        # Strip prefix for stdout user
        clean_content = content.replace("CD:", "").replace("CMD:", "")
        print(clean_content)

if __name__ == "__main__":
    app()
