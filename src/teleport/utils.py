import os
import sys
from pathlib import Path

def get_db_path() -> Path:
    """Returns the path to the database file based on the OS."""
    if os.name == 'nt':
        base_dir = Path(os.environ.get('USERPROFILE', Path.home()))
    else:
        base_dir = Path.home()
    
    return base_dir / ".teleport.db"

def is_interactive() -> bool:
    """Check if we are running in an interactive terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()
