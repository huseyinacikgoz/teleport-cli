import sqlite3
import time
from pathlib import Path
from typing import List, Tuple, Optional
from .utils import get_db_path

class TeleportDB:
    def __init__(self):
        self.db_path = get_db_path()
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                path TEXT PRIMARY KEY,
                count INTEGER DEFAULT 1,
                last_visited REAL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                alias TEXT PRIMARY KEY,
                command TEXT,
                description TEXT
            )
        ''')
        self.conn.commit()

    def add_path(self, path: str):
        path = str(Path(path).resolve())
        now = time.time()
        
        self.cursor.execute("SELECT count FROM history WHERE path = ?", (path,))
        row = self.cursor.fetchone()
        
        if row:
            count = row[0] + 1
            self.cursor.execute("UPDATE history SET count = ?, last_visited = ? WHERE path = ?", (count, now, path))
        else:
            self.cursor.execute("INSERT INTO history (path, count, last_visited) VALUES (?, ?, ?)", (path, 1, now))
        
        self.conn.commit()

    def get_frequent_paths(self) -> List[Tuple[str, float]]:
        """Return paths sorted by frecency score."""
        self.cursor.execute("SELECT path, count, last_visited FROM history")
        rows = self.cursor.fetchall()
        
        scored_paths = []
        now = time.time()
        
        for path, count, last_visited in rows:
            path_obj = Path(path)
            if not path_obj.exists():
                # Clean up deleted paths lazily
                self.cursor.execute("DELETE FROM history WHERE path = ?", (path,))
                continue

            score = self._calculate_score(count, last_visited, now)
            scored_paths.append((path, score))
            
        self.conn.commit()  # To commit deletions if any
        return sorted(scored_paths, key=lambda x: x[1], reverse=True)

    def _calculate_score(self, count: int, last_visited: float, now: float) -> float:
        """Calculate frecency score based on frequency and recency."""
        diff_hours = (now - last_visited) / 3600
        
        if diff_hours < 1:
            recency_mult = 4.0
        elif diff_hours < 24:
            recency_mult = 2.0
        elif diff_hours < 168:  # 1 week
            recency_mult = 0.5
        else:
            recency_mult = 0.25
            
        return count * recency_mult

    def add_command(self, alias: str, command: str, description: str = ""):
        self.cursor.execute("INSERT OR REPLACE INTO commands (alias, command, description) VALUES (?, ?, ?)", 
                            (alias, command, description))
        self.conn.commit()

    def get_command(self, alias: str) -> Optional[str]:
        self.cursor.execute("SELECT command FROM commands WHERE alias = ?", (alias,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def list_commands(self) -> List[Tuple[str, str, str]]:
        self.cursor.execute("SELECT alias, command, description FROM commands")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
