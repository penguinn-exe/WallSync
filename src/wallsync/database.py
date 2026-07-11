import sqlite3
from pathlib import Path


DB_PATH = Path.home() / ".local/share/wallsync/wallsync.db"


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS wallpapers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE,
        filename TEXT,
        extension TEXT,
        size INTEGER,
        width INTEGER,
        height INTEGER,
        last_shown TIMESTAMP,
        sha256 TEXT
    );
    """)

    conn.commit()

    return conn
