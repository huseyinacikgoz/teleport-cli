import os
import shutil
from pathlib import Path

def get_db_path() -> Path:
    """
    Returns the database path following Linux XDG Base Directory specification.
    Preferred: ~/.local/share/teleport/db.sqlite
    
    Migrates old ~/.teleport.db if found.
    """
    # Use XDG_DATA_HOME if set, else ~/.local/share
    xdg_data_home = os.environ.get("XDG_DATA_HOME")
    if xdg_data_home:
        data_dir = Path(xdg_data_home)
    else:
        data_dir = Path.home() / ".local" / "share"

    teleport_dir = data_dir / "teleport"
    
    # Ensure directory exists
    try:
        teleport_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass
        
    final_db_path = teleport_dir / "db.sqlite"

    # Migration Check
    old_db = Path.home() / ".teleport.db"
    if old_db.exists() and not final_db_path.exists():
        try:
            shutil.move(str(old_db), str(final_db_path))
            # Also try to move lang.txt if it was there (though likely not)
        except OSError:
            pass
            
    return final_db_path
